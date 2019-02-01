import numpy as np

# Signature: Kefu Zhu

class Conv2D(object):
    """2D convolutional layer.

    Arguments:
        in_channel: number of input channel
        out_channel: number of output channel
        kernel_size (tuple): the shape of the kernel. It is a tuple = (
            kernel_height, kernel_width).
        strides (int or tuple): the strides of the convolution operation.
            padding (int or tuple): number of zero paddings.
        weights_init (obj):  an object instantiated using any initializer class
                in the "initializer" module.
        bias_init (obj):  an object instantiated using any initializer class
                in the "initializer" module.
        name (str): the name of the layer.

    Attributes:
        W (np.array): the weights of the layer. A 4D array of shape (
            out_channels, in_channels, kernel_height, kernel_width).
        b (np.array): the biases of the layer. A 1D array of shape (
            out_channels).
        kernel_size (tuple): the shape of the filter. It is a tuple = (
            out_channels, in_channels, kernel_height, kernel_width).
        strides (tuple): the strides of the convolution operation. A tuple = (
            height_stride, width_stride).
        padding (tuple): the number of zero paddings along the height and
            width. A tuple = (height_padding, width_padding).
        name (str): the name of the layer.

    """

    def __init__(
            self, in_channel, out_channel, kernel_size, stride, padding):
        self.W = np.random.randn(*kernel_size)
        self.b = np.random.randn(kernel_size[0], 1)
        self.kernel_size = kernel_size
        self.stride = (stride, stride) if type(stride) == int else stride
        self.padding = (padding, padding) if type(padding) == int else padding

    def __repr__(self):
        return "{}({}, {}, {})".format(
            self.name, self.kernel_size, self.stride, self.padding
        )
    
    def __call__(self, x):
        return self.forward(x)

    def forward(self, x):
        """Compute the layer output.

        Args:
            x (np.array): the input of the layer. A 3D array of shape (
                in_channels, in_heights, in_weights).

        Returns:
            The output of the layer. A 3D array of shape (out_channels,
                out_heights, out_weights).

        """
        p, s = self.padding, self.stride
        x_padded = np.pad(
            x, ((0, 0), (p[0], p[0]), (p[1], p[1])), mode='constant'
        )

        # check dimensions
        assert (x.shape[1] - self.W.shape[2] + 2 * p[0]) / s[0] + 1 > 0, \
                'Height doesn\'t work'
        assert (x.shape[2] - self.W.shape[3] + 2 * p[1]) / s[1] + 1 > 0, \
                'Width doesn\'t work'

        # TODO: Put your code below

        # Parameters
        W = self.W # (out_channels, in_channels, kernel_height, kernel_width)
        bias = self.b # out_channels
        out_channels,in_channels,filter_height,filter_width  = W.shape
        img_height = x.shape[1]
        img_width = x.shape[2]
        stride_height = s[0] if s[0] != 0 else 1
        stride_width = s[1] if s[1] != 0 else 1

        # Initialize empty feature map
        feature_maps = np.zeros((out_channels,
                                (img_height - filter_height + 2 * p[0])//s[0] + 1,
                                (img_width - filter_width + 2 * p[1])//s[1] + 1))

        # Convolve the image by each filter
        for filter_index in range(out_channels):
            # Obtain the current filter
            _filter = W[filter_index,:] # (in_channels, kernel_height, kernel_width)
            # Loop through each row in the feature map
            for row in range(feature_maps.shape[1]):
                # Loop through each column in the feature map
                for column in range(feature_maps.shape[2]):
                    # Start row index for the convolution area
                    row_start = row*stride_height
                    # End row index for the convolution area
                    row_end = row*stride_height + filter_height
                    # Start column index for the convolution area
                    column_start = column*stride_width
                    # End column index for the convolution area
                    column_end = column*stride_width + filter_width
                    # Convolution area
                    conv_area = x_padded[:,row_start:row_end,column_start:column_end]
                    # Perform element-wise multiplication, add the bias, and store the result value in the feature map
                    feature_maps[filter_index,row,column] = np.sum(conv_area * _filter) + bias[filter_index]

        # Return the feature map
        return feature_maps



class MaxPool2D:
    def __init__(self, kernel_size, stride, padding, name="MaxPool2D"):
        self.kernel_size = kernel_size
        self.stride = (stride, stride) if type(stride) == int else stride
        self.padding = (padding, padding) if type(padding) == int else padding
        self.name = name

    def __repr__(self):
        return "{}({}, {}, {})".format(
        self.name, self.kernel_size, self.stride, self.padding
    )

    def __call__(self, x):
        return self.forward(x)

    def forward(self, x):
        """Compute the layer output.
        
        Arguments:
            x {[np.array]} -- the input of the layer. A 3D array of shape (
                              in_channels, in_heights, in_weights).
        Returns:
            The output of the layer. A 3D array of shape (out_channels,
                out_heights, out_weights).
        """
        p, s = self.padding, self.stride
        x_padded = np.pad(
            x, ((0, 0), (p[0], p[0]), (p[1], p[1])), mode='constant'
        )

        # check dimensions
        assert (x.shape[1] - self.kernel_size[0] + 2 * p[0]) / s[0] + 1 > 0, \
                'Height doesn\'t work'
        assert (x.shape[2] - self.kernel_size[1] + 2 * p[1]) / s[1] + 1 > 0, \
                'Width doesn\'t work'

        # TODO: Put your code below
        
        # Parameters
        in_channels, img_height, img_width = x.shape
        filter_size = self.kernel_size[0]
        stride = self.stride[0]
        pad = self.padding[0]

        # Initialize empty feature map
        feature_maps = np.zeros((in_channels,
                                (img_height - filter_size + 2 * pad)//stride + 1,
                                (img_width - filter_size + 2 * pad)//stride + 1))

        # Perform max pooling on each channel independently
        for c in range(in_channels):
            # Obtain the channel
            channel = x_padded[c,:] # (in_channels, kernel_height, kernel_width)
            # Loop through each row in the feature map
            for row in range(feature_maps.shape[1]):
                # Loop through each column in the feature map
                for column in range(feature_maps.shape[2]):
                    # Start row index for the convolution area
                    row_start = row*stride
                    # End row index for the convolution area
                    row_end = row*stride + filter_size
                    # Start column index for the convolution area
                    column_start = column*stride
                    # End column index for the convolution area
                    column_end = column*stride + filter_size
                    # Pooling area
                    pool_area = x_padded[c,row_start:row_end,column_start:column_end]
                    # Perform max pooling and store the value in the feature map
                    feature_maps[c,row,column] = np.max(pool_area)

        # Return the feature map
        return feature_maps



class AvgPool2D:
    def __init__(self, kernel_size, stride, padding, name="MaxPool2D"):
        self.kernel_size = kernel_size
        self.stride = (stride, stride) if type(stride) == int else stride
        self.padding = (padding, padding) if type(padding) == int else padding
        self.name = name

    def __repr__(self):
        return "{}({}, {}, {})".format(
        self.name, self.kernel_size, self.stride, self.padding
    )

    def __call__(self, x):
        return self.forward(x)

    def forward(self, x):
        """Compute the layer output.
        
        Arguments:
            x {[np.array]} -- the input of the layer. A 3D array of shape (
                              in_channels, in_heights, in_weights).
        Returns:
            The output of the layer. A 3D array of shape (out_channels,
                out_heights, out_weights).
        """
        p, s = self.padding, self.stride
        x_padded = np.pad(
            x, ((0, 0), (p[0], p[0]), (p[1], p[1])), mode='constant'
        )

        # check dimensions
        assert (x.shape[1] - self.kernel_size[0] + 2 * p[0]) / s[0] + 1 > 0, \
                'Height doesn\'t work'
        assert (x.shape[2] - self.kernel_size[1] + 2 * p[1]) / s[1] + 1 > 0, \
                'Width doesn\'t work'

        # TODO: Put your code below
        
        # Parameters
        in_channels, img_height, img_width = x.shape
        filter_size = self.kernel_size[0]
        stride = self.stride[0]
        pad = self.padding[0]

        # Initialize empty feature map
        feature_maps = np.zeros((in_channels,
                                (img_height - filter_size + 2 * pad)//stride + 1,
                                (img_width - filter_size + 2 * pad)//stride + 1))

        # Perform max pooling on each channel independently
        for c in range(in_channels):
            # Obtain the channel
            channel = x_padded[c,:] # (in_channels, kernel_height, kernel_width)
            # Loop through each row in the feature map
            for row in range(feature_maps.shape[1]):
                # Loop through each column in the feature map
                for column in range(feature_maps.shape[2]):
                    # Start row index for the convolution area
                    row_start = row*stride
                    # End row index for the convolution area
                    row_end = row*stride + filter_size
                    # Start column index for the convolution area
                    column_start = column*stride
                    # End column index for the convolution area
                    column_end = column*stride + filter_size
                    # Pooling area
                    pool_area = x_padded[c,row_start:row_end,column_start:column_end]
                    # Perform max pooling and store the value in the feature map
                    feature_maps[c,row,column] = np.mean(pool_area)

        # Return the feature map
        return feature_maps

