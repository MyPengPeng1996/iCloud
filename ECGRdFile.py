# -*- coding: utf-8 -*-
import numpy
import scipy.io.matlab.mio as mysio

# read data from the cpsc2018 database
def cpsc2018load_matfile(filename, leadC):
    fileC   = mysio.loadmat(filename)
    ecgdata = fileC['ECG']['data'][0,0]
    if(leadC == 1):
        ecgdata  = ecgdata[1,:]                                      # may be lead II
        ecgdata  = ecgdata.reshape((1,-1))
    elif(leadC == 8):
        ecgdata  = ecgdata[[1,2,6,7,8,9,10,11],:]                    # may be lead II,III and V1-V6
    else:
        raise TypeError('please check the parameter [leadC]!')
    int16data = numpy.round(ecgdata * 1000).astype('int16')          # a loss of precision
    baseline  = 0
    scale     = 0.001
    freq      = 500
    return (int16data, baseline, scale, freq)

# read data from your electrocardiogram databases
# add your code
