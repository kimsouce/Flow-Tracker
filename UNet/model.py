import torch
import torch.nn as nn
import torch.nn.functional as F

from model_parts import _conv_, _conv_block_, _downsample_, _upsample_, _context_block_

class SAR(nn.Module) :
    def __init__(self, scale, in_channels, out_channels, channels, kernel_size, stride, dilation, bias) :
        # Inheritance
        super(SAR, self).__init__()

        self._conv_in_ = nn.Sequential(
                                    _conv_block_(in_channels, channels, kernel_size, stride, dilation, bias),
                                    _conv_block_(channels, channels, kernel_size, stride, dilation, bias)
                                    )
        self._conv_out_ = _conv_(channels, out_channels, 1, stride, dilation, bias)
        self._cb_ = _context_block_(channels * 8, kernel_size, stride, dilation, bias)
        self._down_1_ = _downsample_(scale, channels, channels * 2, kernel_size, stride, dilation, bias)
        self._down_2_ = _downsample_(scale, channels * 2, channels * 4, kernel_size, stride, dilation, bias)
        self._down_3_ = _downsample_(scale, channels * 4, channels * 8, kernel_size, stride, dilation, bias)
        self._up_1_ = _upsample_(channels * 8, channels * 4, kernel_size, stride, dilation, bias)
        self._up_2_ = _upsample_(channels * 4, channels * 2, kernel_size, stride, dilation, bias)
        self._up_3_ = _upsample_(channels * 2, channels, kernel_size, stride, dilation, bias)

    def forward(self, x) :
        out = self._conv_in_(x)
        sk_1 = out
        out = self._down_1_(out)
        sk_2 = out
        out = self._down_2_(out)
        sk_3 = out
        out = self._down_3_(out)
        out = self._cb_(out)
        out = self._up_1_(out, sk_3)
        out = self._up_2_(out, sk_2)
        out = self._up_3_(out, sk_1)
        out = self._conv_out_(out)

        return out

    def initialize_weights(self) :
        for m in self.modules() :
            if isinstance(m, (nn.Conv2d, nn.ConvTranspose2d)) :
                # Apply Xavier Uniform Initialization
                torch.nn.init.xavier_uniform_(m.weight.data)

                if m.bias is not None :
                    m.bias.data.zero_()

def Generator(scale, in_channels, out_channels, channels, kernel_size, stride, dilation, bias) :
    return SAR(scale, in_channels, out_channels, channels, kernel_size, stride, dilation, bias)