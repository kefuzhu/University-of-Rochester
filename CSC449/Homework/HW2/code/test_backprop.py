import unittest
import pickle
import numpy as np
from layer import Conv2D, MaxPool2D, FullyConnected


class TestBackProp(unittest.TestCase):
    def setUp(self):
        with open('../data/conv_cases.pkl', 'rb') as conv_f, \
             open('../data/max_pool_cases.pkl', 'rb') as max_pool_f, \
             open('../data/fc_cases.pkl', 'rb') as fc_f:
            self.conv_cases = pickle.load(conv_f)
            self.max_pool_cases = pickle.load(max_pool_f)
            self.fc_cases = pickle.load(fc_f)

    def test_conv_backprop(self):
        for case in self.conv_cases:
            weight = case['weight']
            out_c, in_c, h, w = weight.shape
            bias = case['bias']
            x = case['x']
            out = case['out']
            stride = case['stride']
            pad = case['pad']
            grad_output = case['grad_output']
            grad_x = case['grad_x']
            grad_w = case['grad_w']
            grad_b = case['grad_b']

            conv = Conv2D(in_channel=in_c,
                          out_channel=out_c,
                          kernel_size=(h, w),
                          stride=stride,
                          padding=pad)
            conv.W = weight
            conv.b = bias
            test_out = conv(x)
            dv_x, dv_W, dv_b = conv.backward(x, grad_output)

            self.assertTrue(np.allclose(out, test_out, rtol=0.0001))

            self.assertTrue(np.allclose(grad_x, dv_x, rtol=0.0001))
            self.assertTrue(np.allclose(grad_w, dv_W, rtol=0.0001))
            self.assertTrue(np.allclose(grad_b, dv_b, rtol=0.0001))

    def test_max_pool_backprop(self):
        for case in self.max_pool_cases:
            kernel = (case['kernel'], case['kernel'])
            stride = case['stride']
            pad = case['pad']
            x = case['x']
            out = case['out']
            grad_output = case['grad_output']
            grad_x = case['grad_x']

            max_pool = MaxPool2D(kernel_size=kernel, stride=stride, padding=pad)
            test_out = max_pool(x)
            dv_x = max_pool.backward(x, grad_output)

            self.assertTrue(np.allclose(out, test_out))

            self.assertTrue(np.allclose(grad_x, dv_x, rtol=0.0001))

    def test_fc_backprop(self):
        for case in self.fc_cases:
            weight = case['weight']
            out_c, in_c = weight.shape
            bias = case['bias']
            x = case['x'].astype(np.float32)
            out = case['out']
            grad_output = case['grad_output']
            grad_x = case['grad_x']
            grad_w = case['grad_w']
            grad_b = case['grad_b']

            fc = FullyConnected(d_in=in_c, d_out=out_c)
            fc.W = weight
            fc.b = bias
            test_out = fc(x)
            dv_x, dv_W, dv_b = fc.backward(x, grad_output)

            self.assertTrue(np.allclose(out, test_out, rtol=0.0001))

            self.assertTrue(np.allclose(grad_x, dv_x, rtol=0.001))
            self.assertTrue(np.allclose(grad_w, dv_W))
            self.assertTrue(np.allclose(grad_b, dv_b))


if __name__ == '__main__':
    unittest.main()

