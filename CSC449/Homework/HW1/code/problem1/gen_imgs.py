import os
import cv2
from cv249 import CV249

gen_img_path = '../../result_imgs'


def write_img(img, fname):
    if img is not None:
        path = os.path.join(gen_img_path, fname)
        cv2.imwrite(path, img)
        print("image write to {}.".format(path))


if __name__ == '__main__':
    if not os.path.exists(gen_img_path):
        os.mkdir(gen_img_path)

    img = cv2.imread('../../data/lena.tiff')
    cv = CV249()

    write_img(cv.cvt_to_gray(img), 'gray.jpg')
    write_img(cv.blur(img, (3, 3)), 'blur.jpg')
    write_img(cv.sharpen_laplacian(img), 'sharpen.jpg')
    write_img(cv.unsharp_masking(img), 'unsharp_mask.jpg')
    write_img(cv.edge_det_sobel(img), 'edge.jpg')
