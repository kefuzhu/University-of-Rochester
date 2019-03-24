import os
from os.path import join, isdir
from os import makedirs
import argparse
import json
import numpy as np
import torch

import cv2
import time as time
from util import crop_chw, gaussian_shaped_labels, cxy_wh_2_rect1, rect1_2_cxy_wh, cxy_wh_2_bbox
from network import DCFNet
from eval_otb import eval_auc

# base dataset path and setting
parser = argparse.ArgumentParser(description='Test DCFNet on OTB')
parser.add_argument('--dataset', metavar='SET', default='OTB2013',
                    choices=['OTB2013', 'OTB2015'], help='tune on which dataset')
parser.add_argument('--model', metavar='PATH', default='param.pth')
parser.add_argument('--visualization', action='store_true', help='visualize the tracked bbox')
args = parser.parse_args()

# by default, we ship the data to GPU 0. you can sepcify it later
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")


class TrackerConfig(object):
    # These are the default hyper-params for DCFNet
    # OTB2013 / AUC(0.635)
    crop_sz = 125
    lambda0 = 1e-4
    padding = 2
    output_sigma_factor = 0.1
    interp_factor = 0.01
    num_scale = 3
    scale_step = 1.0275
    scale_factor = scale_step ** (np.arange(num_scale) - num_scale / 2)
    min_scale_factor = 0.2
    max_scale_factor = 5
    scale_penalty = 0.9925
    scale_penalties = scale_penalty ** (np.abs((np.arange(num_scale) - num_scale / 2)))

    net_input_size = [crop_sz, crop_sz]
    net_average_image = np.array([104, 117, 123]).reshape(-1, 1, 1).astype(np.float32)
    output_sigma = crop_sz / (1 + padding) * output_sigma_factor
    y = gaussian_shaped_labels(output_sigma, net_input_size)
    # the rfft reduce the output as half, due to conjugate symmetry
    yf = torch.rfft(torch.Tensor(y).view(1, 1, crop_sz, crop_sz).to(device), signal_ndim=2)
    # add the hanning of the input image
    cos_window = torch.Tensor(np.outer(np.hanning(crop_sz), np.hanning(crop_sz))).to(device)


def preprocess_patch(im, target_pos, target_sz, config):
    """
    preprocess patch for the input of network
    :param im: input image (h, w, 3)
    :param target_pos: center coordinate of the target box, tuple (cx, cy)
    :param target_sz: width and hight of the target box, tuple (w, h)
    :param config: TrackConfig
    :return: patch: (3, config.crop_sz, config.crop_sz)
    """
    # enlarge the cropping scale
    window_sz = target_sz * (1 + config.padding)
    # change the expression of box coordinate
    bbox = cxy_wh_2_bbox(target_pos, window_sz)
    # crop z in the next frame
    patch = crop_chw(im, bbox, config.crop_sz)
    # mean deduction
    patch = patch - config.net_average_image
    return patch


dataset = args.dataset
base_path = join('dataset', dataset)
json_path = join('dataset', dataset + '.json')
annos = json.load(open(json_path, 'r'))
videos = sorted(annos.keys())

visualization = args.visualization

# default parameter and load feature extractor network
config = TrackerConfig()
net = DCFNet(config)

# load model
try:
    net.load_param(args.model)
except:
    pass
    pre_trained_model = torch.load(args.model)
    new = list(pre_trained_model.items())
    net_kvpair = net.state_dict()
    count = 0
    for key,value in net_kvpair.items():
        layer_name, weights=new[count]
        net_kvpair[key] = weights
        count += 1
    net.load_state_dict(net_kvpair)
net.eval().to(device)

speed = []
# loop videos
for video_id, video in enumerate(videos):  # run without resetting
    video_path_name = annos[video]['name']
    init_rect = np.array(annos[video]['init_rect']).astype(np.float)
    image_files = [join(base_path, video_path_name, 'img', im_f) for im_f in annos[video]['image_files']]
    n_images = len(image_files)

    tic = time.time()  # time start

    target_pos, target_sz = rect1_2_cxy_wh(init_rect)  # OTB label is 1-indexed

    im = cv2.imread(image_files[0])  # HxWxC

    # confine results
    min_sz = np.maximum(config.min_scale_factor * target_sz, 4)
    max_sz = np.minimum(im.shape[:2], config.max_scale_factor * target_sz)

    patch = preprocess_patch(im, target_pos, target_sz, config)

    # update the initial correlation kernel
    net.update(torch.Tensor(np.expand_dims(patch, axis=0)).to(device))

    # res store the tracking result
    res = [cxy_wh_2_rect1(target_pos, target_sz)]  # save in .txt
    # patch_crop: store num_scale kinds of different scales of z
    patch_crop = np.zeros((config.num_scale, patch.shape[0], patch.shape[1], patch.shape[2]), np.float32)
    for f in range(1, n_images):  # track
        # read the f th image
        im = cv2.imread(image_files[f])
        # add multi-scale search region z to patch_crop
        for i in range(config.num_scale):
            window_sz = target_sz * (config.scale_factor[i] * (1 + config.padding))
            bbox = cxy_wh_2_bbox(target_pos, window_sz)
            patch_crop[i, :] = crop_chw(im, bbox, config.crop_sz)

        # mean deduction
        search = patch_crop - config.net_average_image
        # get the response by forward the DCFnet
        response = net(torch.Tensor(search).to(device))
        # find the peak value and location in different scale z
        peak, idx = torch.max(response.view(config.num_scale, -1), 1)
        # penalize the peak value in different scale
        peak = peak.data.to('cpu').numpy() * config.scale_penalties
        # choose the index of best scale
        best_scale = np.argmax(peak)
        # get the coordination of the peak response in z
        r_max, c_max = np.unravel_index(idx[best_scale].to('cpu'), config.net_input_size)
        # r_shift: row shift
        r_shift = r_max - config.net_input_size[0] if r_max > config.net_input_size[0] / 2 else r_max
        # c_shift: column shift
        c_shift = c_max - config.net_input_size[1] if c_max > config.net_input_size[1] / 2 else c_max
        window_sz = target_sz * (config.scale_factor[best_scale] * (1 + config.padding))
        # rescale back the box size to the original one
        target_pos = target_pos + np.array([c_shift, r_shift]) * window_sz / config.net_input_size
        target_sz = np.minimum(np.maximum(window_sz / (1 + config.padding), min_sz), max_sz)

        # model update
        patch = preprocess_patch(im, target_pos, target_sz, config)
        net.update(torch.Tensor(np.expand_dims(patch, axis=0)).to(device), lr=config.interp_factor)


        res.append(cxy_wh_2_rect1(target_pos, target_sz))  # 1-index

        if visualization:
            im_show = im
            cv2.rectangle(im_show, (int(target_pos[0] - target_sz[0] / 2), int(target_pos[1] - target_sz[1] / 2)),
                          (int(target_pos[0] + target_sz[0] / 2), int(target_pos[1] + target_sz[1] / 2)),
                          (0, 255, 0), 3)
            cv2.putText(im_show, str(f), (40, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2, cv2.LINE_AA)
            vis_root = 'visualization'
            save_path = os.path.join(vis_root, image_files[f])
            save_folder = '/'.join(save_path.split('/')[:-1])
            if not os.path.exists(save_folder):
                os.makedirs(save_folder)
            cv2.imwrite(save_path, im_show)

    toc = time.time() - tic
    fps = n_images / toc
    speed.append(fps)
    print('{:3d} Video: {:12s} Time: {:3.1f}s\tSpeed: {:3.1f}fps'.format(video_id, video, toc, fps))

    # save result
    test_path = join('result', dataset, 'DCFNet_test')
    if not isdir(test_path): makedirs(test_path)
    result_path = join(test_path, video + '.txt')
    with open(result_path, 'w') as f:
        for x in res:
            f.write(','.join(['{:.2f}'.format(i) for i in x]) + '\n')

print('***Total Mean Speed: {:3.1f} (FPS)***'.format(np.mean(speed)))

eval_auc(dataset, 'DCFNet_test', 0, 1)
