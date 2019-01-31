import numpy as np
import cv2

# Signature: Kefu Zhu


class CV249:
    def cvt_to_gray(self, img):
        # Note that cv2.imread will read the image to BGR space rather than RGB space

        # GRAY = 0.299*R + 0.587*G + 0.114*B

        # TODO: your implementation

        # Convert BGR image to grayscale image
        img_gray = np.dot(img,[0.114, 0.587, 0.299])

        # Return the grayscale image
        return img_gray


    def blur(self, img, kernel_size=(3, 3)):
        """smooth the image with box filter
        
        Arguments:
            img {np.array} -- input array
        
        Keyword Arguments:
            kernel_size {tuple} -- kernel size (default: {(3, 3)})
        
        Returns:
            np.array -- blurred image
        """
        # TODO: your implementation

        # Create box filter with given kernel size
        box_filter = np.ones(kernel_size)
        box_filter = box_filter/box_filter.size
        # Convolve the box filter with the input image
        img_blur = cv2.filter2D(img,-1,box_filter)

        # Return the blurred image
        return img_blur


    def sharpen_laplacian(self, img):
        """sharpen the image with laplacian filter
        
        Arguments:
            img {np.array} -- input image
        
        Returns:
            np.array -- sharpened image
        """

        # subtract the laplacian from the original image 
        # when have a negative center in the laplacian kernel

        # TODO: your implementation
        
        # Create the laplacian filter
        laplacian_filter = np.array([0,1,0,1,-4,1,0,1,0]).reshape(3,3)
        # Convolve the laplacian filter with the input image
        laplacian = cv2.filter2D(img,-1,laplacian_filter)
        # Subtract the laplacian from the original image
        my_sharp = img - laplacian

        # Return the sharpen image
        return my_sharp


    def unsharp_masking(self, img):
        """sharpen the image via unsharp masking
        
        Arguments:
            img {np.array} -- input image
        
        Returns:
            np.array -- sharpened image
        """
        # use don't use cv2 in this function
        
        # TODO: your implementation

        # Create box filter with given kernel size (3,3)
        box_filter = np.ones((3,3))
        box_filter = box_filter/box_filter.size
        # Convolve the box filter with the input image
        img_blur = cv2.filter2D(img,-1,box_filter)
        
        my_unsharp = img + 1*(img - img_blur)

        return my_unsharp

    def edge_det_sobel(self, img):
        """detect edges with sobel filter
        
        Arguments:
            img {np.array} -- input image
        
        Returns:
            [np.array] -- edges
        """

        # TODO: your implementation
        
        # Horizontal derivative filter (Sobel)
        dx = np.array([-1,0,1,-2,0,2,-1,0,1]).reshape(3,3)
        # Vertical derivative filter (Sobel)
        dy = np.array([-1,-2,-1,0,0,0,1,2,1]).reshape(3,3)

        # E = sqrt(dx*I)^2 + (dy*I)^2) 
        # * : cross correlation
        my_sobel = np.sqrt(cv2.filter2D(img,-1,dx)**2 + cv2.filter2D(img,-1,dy)**2).astype(np.uint8)

        return my_sobel



