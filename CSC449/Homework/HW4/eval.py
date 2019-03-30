import torch
import json
import matplotlib.pyplot as plt
import numpy as np
import argparse
import pickle
import os
from torchvision import transforms
from build_vocab import Vocabulary
from network import Encoder, Decoder
from PIL import Image
from pycocotoolscap.coco import COCO
from pycocoevalcap.eval import COCOEvalCap
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')


def load_image(image_path, transform=None):
    image = Image.open(image_path)
    image = image.resize([224, 224], Image.LANCZOS)

    if transform is not None:
        image = transform(image).unsqueeze(0)

    return image


def main(args):
    # Image preprocessing
    transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize((0.485, 0.456, 0.406),
                             (0.229, 0.224, 0.225))])

    # Load vocabulary
    with open(args.vocab_path, 'rb') as f:
        vocab = pickle.load(f)

    # Build models
    encoder = Encoder(args.embed_size).eval()
    decoder = Decoder(args.embed_size, args.hidden_size, len(vocab), args.num_layers)
    encoder = encoder.to(device)
    decoder = decoder.to(device)

    # Load the trained model parameters
    encoder.load_state_dict(torch.load(args.encoder_path))
    decoder.load_state_dict(torch.load(args.decoder_path))

    # load validation image set
    lis = os.listdir(args.image_dir)
    num = len(lis)
    captions = []
    for i in range(num):

        im_pth = os.path.join(args.image_dir, lis[i])

        image = load_image(im_pth, transform)
        image_tensor = image.to(device)

        # Generate an caption from the image
        feature = encoder(image_tensor)
        sampled_ids = decoder.sample(feature)
        sampled_ids = sampled_ids[0].cpu().numpy()  # (1, max_seq_length) -> (max_seq_length)

        # Convert word_ids to words
        sampled_caption = []
        for word_id in sampled_ids:
            word = vocab.idx2word[word_id]
            if word == '<start>':
                continue
            if word == '<end>':
                break

            sampled_caption.append(word)

        sentence = ' '.join(sampled_caption)
        cap= {}
        id = int(lis[i][14:-4]) #extract image id
        cap['image_id'] = id
        cap['caption'] =  sentence
        captions.append(cap)
    # save results
    with open('captions_res.json', 'w') as f:
        json.dump(captions, f)

    # evaluation with coco-caption evaluation tools
    coco = COCO(args.caption_path)
    cocoRes = coco.loadRes('captions_res.json')
    cocoEval = COCOEvalCap(coco, cocoRes)
    cocoEval.params['image_id'] = cocoRes.getImgIds()
    cocoEval.evaluate()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--image_dir', type=str, default='data/img100', help='directory for val images')
    parser.add_argument('--encoder_path', type=str, default='models/encoder.ckpt',
                        help='path for trained encoder')
    parser.add_argument('--decoder_path', type=str, default='models/decoder.ckpt',
                        help='path for trained decoder')
    parser.add_argument('--vocab_path', type=str, default='data/vocab.pkl', help='path for vocabulary wrapper')

    # Model parameters (should be same as paramters in train.py)
    parser.add_argument('--embed_size', type=int, default=256, help='dimension of word embedding vectors')
    parser.add_argument('--hidden_size', type=int, default=512, help='dimension of lstm hidden states')
    parser.add_argument('--num_layers', type=int, default=1, help='number of layers in lstm')
    parser.add_argument('--caption_path', type=str, default='data/annotations/captions_val2014.json',
                        help='path for val annotation json file')
    args = parser.parse_args()
main(args)