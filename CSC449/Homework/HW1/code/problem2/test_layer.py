import unittest
import numpy as np
import pickle
from layer import Conv2D, MaxPool2D, AvgPool2D


class TestLayer(unittest.TestCase):
    def setUp(self):
        with open('../../data/conv_cases.pkl', 'rb') as conv_f, \
             open('../../data/max_pool_cases.pkl', 'rb') as max_pool_f, \
             open('../../data/avg_pool_cases.pkl', 'rb') as avg_pool_f:
            self.conv_cases = pickle.load(conv_f)
            self.max_pool_cases = pickle.load(max_pool_f)
            self.avg_pool_cases = pickle.load(avg_pool_f)
    
    def test_conv(self):
        for case in self.conv_cases:
            weight = case['weight']
            out_c, in_c, h, w = weight.shape
            bias = case['bias']
            x = case['x']
            out = case['out']
            stride = case['stride']
            pad = case['pad']
            
            conv = Conv2D(in_channel=in_c,
                          out_channel=out_c,
                          kernel_size=(h, w),
                          stride=stride,
                          padding=pad)
            conv.W = weight
            conv.b = bias
            test_out = conv(x)

            self.assertTrue(np.allclose(out, test_out))

    def test_max_pool(self):
        for case in self.max_pool_cases:
            kernel = (case['kernel'], case['kernel'])
            stride = case['stride']
            pad = case['pad']
            x = case['x']
            out = case['out']

            max_pool = MaxPool2D(kernel_size=kernel, stride=stride, padding=pad)
            test_out = max_pool(x)

            self.assertTrue(np.allclose(out, test_out))

    def test_avg_pool(self):
        for case in self.avg_pool_cases:
            kernel = (case['kernel'], case['kernel'])
            stride = case['stride']
            pad = case['pad']
            x = case['x']
            out = case['out']

            avg_pool = AvgPool2D(kernel_size=kernel, stride=stride, padding=pad)
            test_out = avg_pool(x)

            self.assertTrue(np.allclose(out, test_out))


if __name__ == '__main__':
    unittest.main()
