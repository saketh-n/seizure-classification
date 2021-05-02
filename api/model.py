# Model definitions for all classifiers
# EEGNet architecture is from the original authors from the Army Research Laboratory
# Source: https://github.com/vlawhern/arl-eegmodels/blob/master/EEGModels.py

from tensorflow.keras.models import Model
from tensorflow.keras.layers import Dense, Activation, Dropout
from tensorflow.keras.layers import Conv2D, AveragePooling2D
from tensorflow.keras.layers import SeparableConv2D, DepthwiseConv2D
from tensorflow.keras.layers import BatchNormalization
from tensorflow.keras.layers import SpatialDropout2D
from tensorflow.keras.layers import Input, Flatten
from tensorflow.keras.constraints import max_norm


def EEGNet(nb_classes, channels=64, samples=128,
           dropout_rate=0.5, kernel_length=64, f1=8,
           d=2, f2=16, norm_rate=0.25, dropout_type='Dropout'):
    """ Keras Implementation of EEGNet
    http://iopscience.iop.org/article/10.1088/1741-2552/aace8c/meta
    Note that this implements the newest version of EEGNet and NOT the earlier
    version (version v1 and v2 on arxiv). We strongly recommend using this
    architecture as it performs much better and has nicer properties than
    our earlier version. For example:

        1. Depth-wise Convolutions to learn spatial filters within a
        temporal convolution. The use of the depth_multiplier option maps
        exactly to the number of spatial filters learned within a temporal
        filter. This matches the setup of algorithms like FBCSP which learn
        spatial filters within each filter in a filter-bank. This also limits
        the number of free parameters to fit when compared to a fully-connected
        convolution.

        2. Separable Convolutions to learn how to optimally combine spatial
        filters across temporal bands. Separable Convolutions are Depth-wise
        Convolutions followed by (1x1) Point-wise Convolutions.


    While the original paper used Dropout, we found that SpatialDropout2D
    sometimes produced slightly better results for classification of ERP
    signals. However, SpatialDropout2D significantly reduced performance
    on the Oscillatory dataset (SMR, BCI-IV Dataset 2A). We recommend using
    the default Dropout in most cases.

    Assumes the input signal is sampled at 128Hz. If you want to use this model
    for any other sampling rate you will need to modify the lengths of temporal
    kernels and average pooling size in blocks 1 and 2 as needed (double the
    kernel lengths for double the sampling rate, etc). Note that we haven't
    tested the model performance with this rule so this may not work well.

    The model with default parameters gives the EEGNet-8,2 model as discussed
    in the paper. This model should do pretty well in general, although it is
    advised to do some model searching to get optimal performance on your
    particular dataset. We set f2 = f1 * d (number of input filters = number of output filters)
    for the SeparableConv2D layer. We haven't extensively tested other values of this
    parameter (say, f2 < f1 * d for compressed learning, and f2 > f1 * d for
    overcomplete). We believe the main parameters to focus on are f1 and d.
    Inputs:

      nb_classes      : int, number of classes to classify
      channels, samples  : number of channels and time points in the EEG data
      dropout_rate     : dropout fraction
      kernel_length      : length of temporal convolution in first layer. We found
                        that setting this to be half the sampling rate worked
                        well in practice. For the SMR dataset in particular
                        since the data was high-passed at 4Hz we used a kernel
                        length of 32.
      f1, f2          : number of temporal filters (f1) and number of point-wise
                        filters (f2) to learn. Default: f1 = 8, f2 = f1 * d.
      d               : number of spatial filters to learn within each temporal
                        convolution. Default: d = 2
      dropout_type     : Either SpatialDropout2D or Dropout, passed as a string.
    """

    if dropout_type == 'SpatialDropout2D':
        dropout_type = SpatialDropout2D
    elif dropout_type == 'Dropout':
        dropout_type = Dropout
    else:
        raise ValueError('dropout_type must be one of SpatialDropout2D '
                         'or Dropout, passed as a string.')

    input1 = Input(shape=(channels, samples, 1))

    ##################################################################
    block1 = Conv2D(f1, (1, kernel_length), padding='same',
                    input_shape=(channels, samples, 1),
                    use_bias=False)(input1)
    block1 = BatchNormalization()(block1)
    block1 = DepthwiseConv2D((channels, 1), use_bias=False,
                             depth_multiplier=d,
                             depthwise_constraint=max_norm(1.))(block1)
    block1 = BatchNormalization()(block1)
    block1 = Activation('elu')(block1)
    block1 = AveragePooling2D((1, 4))(block1)
    block1 = dropout_type(dropout_rate)(block1)

    block2 = SeparableConv2D(f2, (1, 16),
                             use_bias=False, padding='same')(block1)
    block2 = BatchNormalization()(block2)
    block2 = Activation('elu')(block2)
    block2 = AveragePooling2D((1, 8))(block2)
    block2 = dropout_type(dropout_rate)(block2)

    flatten = Flatten(name='flatten')(block2)

    dense = Dense(nb_classes, name='dense',
                  kernel_constraint=max_norm(norm_rate))(flatten)
    softmax = Activation('softmax', name='softmax')(dense)

    return Model(inputs=input1, outputs=softmax)
