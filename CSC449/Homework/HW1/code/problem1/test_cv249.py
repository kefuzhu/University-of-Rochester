import unittest
from cv249 import CV249
import numpy as np
import cv2


class TestCV249(unittest.TestCase):
    def setUp(self):
        self.img = cv2.imread('../../data/lena.tiff')
        self.cv = CV249()

    def test_cvt_to_gray(self):
        my_gray = self.cv.cvt_to_gray(self.img)
        gray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
        self.assertTrue(np.mean(gray - my_gray) < 2e-3)

    def test_blur(self):
        box_filtered_img = cv2.blur(self.img, ksize=(3, 3))
        box_filtered_img2 = self.cv.blur(self.img, kernel_size=(3, 3))
        self.assertTrue(np.all(box_filtered_img == box_filtered_img2))

    def test_sharpen_laplacian(self):
        sharpened_img = self.img - cv2.Laplacian(self.img, -1, ksize=1)
        sharpened_img2 = self.cv.sharpen_laplacian(self.img)
        self.assertTrue(np.all(sharpened_img == sharpened_img2))

    def test_unsharp_masking(self):
        masked_img = self.img - cv2.blur(self.img, ksize=(3, 3))
        unsharp_mask_img = self.img + masked_img

        unsharp_mask_img2 = self.cv.unsharp_masking(self.img)
        self.assertTrue(np.all(unsharp_mask_img == unsharp_mask_img2))

    def test_edge_det_sobel(self):
        g_x = cv2.Sobel(self.img, -1, 1, 0)
        g_y = cv2.Sobel(self.img, -1, 0, 1)
        g = np.sqrt(g_x ** 2 + g_y ** 2).astype(np.uint8)

        g2 = self.cv.edge_det_sobel(self.img)
        self.assertTrue(np.all(g == g2))


if __name__ == '__main__':
    unittest.main()
