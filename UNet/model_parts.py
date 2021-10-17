import torch
import torch.nn as nn
import torch.nn.functional as F

class _conv_(nn.Module) :
    def __init__(self, in_channels, out_channels, kernel_size, stride, dilation, bias) :
        # Inheritance
        super(_conv_, self).__init__()

        # Initialize Layer
        self._conv_ = nn.Conv2d(
                            in_channels = in_channels,
                            out_channels = out_channels,
                            kernel_size = kernel_size,
                            stride = stride,
                            padding = (dilation * (kernel_size - 1)) // 2 ,
                            dilation = dilation,
                            bias = bias
                            )

    def forward(self, x) :
        return self._conv_(x)

    def initialize_weights(self) :
        for m in self.modules() :
            if isinstance(m, nn.Conv2d) :
                # Apply Xavier Uniform Initialization
                torch.nn.init.xavier_uniform_(m.weight.data)

                if m.bias is not None :
                    m.bias.data.zero_()

class _conv_block_(nn.Module) :
    def __init__(self, in_channels, out_channels, kernel_size, stride, dilation, bias) :
        # Inheritance
        super(_conv_block_, self).__init__()

        # Initialize Layer
        self._layer_ = nn.Sequential(
                                _conv_(in_channels, out_channels, kernel_size, stride, dilation, bias),
                                nn.ReLU(inplace = True)
                                )

    def forward(self, x) :
        return self._layer_(x)

    def initialize_weights(self) :
        for m in self.modules() :
            if isinstance(m, nn.Conv2d) :
                # Apply Xavier Uniform Initialization
                torch.nn.init.xavier_uniform_(m.weight.data)

                if m.bias is not None :
                    m.bias.data.zero_()

class _residual_channel_attention_block_(nn.Module) :
    def __init__(self, in_channels, kernel_size, stride, dilation, bias) :
        # Inheritance
        super(_residual_channel_attention_block_, self).__init__()

        # Initialize Layer
        self._layer_ = _conv_block_(in_channels, in_channels, kernel_size, stride, dilation, bias)
        self._attention_ = nn.Sequential(
                                    nn.AdaptiveAvgPool2d(1),
                                    _conv_(in_channels, in_channels // 4, 1, stride, dilation, bias),
                                    nn.LeakyReLU(negative_slope = 0.2, inplace = True),
                                    _conv_(in_channels // 4, in_channels, 1, stride, dilation, bias),
                                    nn.Sigmoid()
                                    )

    def forward(self, x) :
        out = self._layer_(x)
        out = out * self._attention_(out)
        out = out + x

        return out

    def initialize_weights(self) :
        for m in self.modules() :
            if isinstance(m, nn.Conv2d) :
                # Apply Xavier Uniform Initialization
                torch.nn.init.xavier_uniform_(m.weight.data)

                if m.bias is not None :
                    m.bias.data.zero_()

class _residual_group_(nn.Module) :
    def __init__(self, in_channels, kernel_size, stride, dilation, bias) :
        # Inheritance
        super(_residual_group_, self).__init__()

        # Initialize Layer
        self._cab_1_ = _residual_channel_attention_block_(in_channels, kernel_size, stride, dilation, bias)
        self._cab_2_ = _residual_channel_attention_block_(in_channels, kernel_size, stride, dilation, bias)
        self._cab_3_ = _residual_channel_attention_block_(in_channels, kernel_size, stride, dilation, bias)
        self._layer_ = _conv_(in_channels, in_channels, kernel_size, stride, dilation, bias)

    def forward(self, x) :
        out = self._cab_1_(x)
        out = self._cab_2_(out)
        out = self._cab_3_(out)
        out = self._layer_(out)
        out = x + out

        return out

    def initialize_weights(self) :
        for m in self.modules() :
            if isinstance(m, nn.Conv2d) :
                # Apply Xavier Uniform Initialization
                torch.nn.init.xavier_uniform_(m.weight.data)

                if m.bias is not None :
                    m.bias.data.zero_()

class _context_block_(nn.Module) :
    def __init__(self, in_channels, kernel_size, stride, dilation, bias) :
        # Inheritance
        super(_context_block_, self).__init__()

        # Initialize Layer
        self._conv_in_ = _conv_block_(in_channels, in_channels, kernel_size, stride, dilation, bias)
        self._conv_out_ = _conv_(in_channels, in_channels, kernel_size, stride, dilation, bias)
        self._d_1_ = _conv_(in_channels, in_channels, kernel_size, stride, dilation, bias)
        self._d_2_ = _conv_(in_channels, in_channels, kernel_size, stride, dilation * 2, bias)
        self._d_3_ = _conv_(in_channels, in_channels, kernel_size, stride, dilation * 3, bias)
        self._d_4_ = _conv_(in_channels, in_channels, kernel_size, stride, dilation * 4, bias)
        self._bottleneck_ = _conv_(in_channels * 4, in_channels, 1, stride, dilation, bias)


    def forward(self, x) :
        out = self._conv_in_(x)
        skip_connection = out
        out = torch.cat([self._d_1_(out), self._d_2_(out), self._d_2_(out), self._d_2_(out)], dim = 1)
        out = self._bottleneck_(out)
        out = skip_connection + out
        out = self._conv_out_(out)
        out = x + out

        return out

    def initialize_weights(self) :
        for m in self.modules() :
            if isinstance(m, nn.Conv2d) :
                # Apply Xavier Uniform Initialization
                torch.nn.init.xavier_uniform_(m.weight.data)

                if m.bias is not None :
                    m.bias.data.zero_()

class _downsample_(nn.Module) :
    def __init__(self, scale, in_channels, out_channels, kernel_size, stride, dilation, bias) :
        # Inheritance
        super(_downsample_, self).__init__()

        # Initialize Layer
        self._layer_ = nn.Sequential(
                                nn.MaxPool2d(kernel_size = scale, stride = scale),
                                _conv_block_(in_channels, out_channels, kernel_size, stride, dilation, bias),
                                _residual_group_(out_channels, kernel_size, stride, dilation, bias)
                                )

    def forward(self, x) :
        return self._layer_(x)

    def initialize_weights(self) :
        for m in self.modules() :
            if isinstance(m, nn.Conv2d) :
                # Apply Xavier Uniform Initialization
                torch.nn.init.xavier_uniform_(m.weight.data)

                if m.bias is not None :
                    m.bias.data.zero_()

class _upsample_(nn.Module) :
    def __init__(self, in_channels, out_channels, kernel_size, stride, dilation, bias) :
        # Inheritance
        super(_upsample_, self).__init__()

        # Initialize Layer
        self._up_ = nn.ConvTranspose2d(
                                in_channels = in_channels,
                                out_channels = out_channels,
                                kernel_size = 2,
                                stride = 2,
                                bias = bias,
                                dilation = dilation)
        self._bottleneck_ = _conv_(in_channels, out_channels, 1, stride, dilation, bias)
        self._layer_ = nn.Sequential(
                                _conv_block_(out_channels, out_channels, kernel_size, stride, dilation, bias),
                                _residual_group_(out_channels, kernel_size, stride, dilation, bias)
                                )
        

    def forward(self, x, skip) :
        out = self._up_(x)
        out = torch.cat((out, skip), dim = 1)
        out = self._bottleneck_(out)

        return self._layer_(out)

    def initialize_weights(self) :
        for m in self.modules() :
            if isinstance(m, (nn.Conv2d, nn.ConvTranspose2d)) :
                # Apply Xavier Uniform Initialization
                torch.nn.init.xavier_uniform_(m.weight.data)

                if m.bias is not None :
                    m.bias.data.zero_()