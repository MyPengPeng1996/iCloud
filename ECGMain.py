
# -*- coding: utf-8 -*-
from ECGRdFile import cpsc2018load_matfile
from ECGSocket import iCloudClient

if __name__ == '__main__':
    
    # -----------------------------------------------------
    # Environment
    #   Anaconda2-4.3.1
    # -----------------------------------------------------
    # The values allowed for the following parameters
    # [leadC]
    #   1 or 8
    # [segnum]
    #   an integer that is greater than 1
    # [aggmethod]
    #   101: equation (3) with m1 = 1 and m2 = 1
    #   102: equation (3) with m1 = 1 and m2 = 2
    srcdir    = 'D:/CPSC2018DB/'
    nameprex  = 'A0001'
    leadC     = 8
    segnum    = 6
    aggmethod = 101
    
    # communicate with the server
    myclient = iCloudClient(serverhost = 'localhost', serverport = 8888)
    if(myclient.establishTCP()):
        int16data, baseline, scale, freq = cpsc2018load_matfile(srcdir + nameprex + '.mat', leadC)
        xmlrecv = myclient.handle(nameprex, int16data, baseline, scale, freq, segnum, aggmethod)
        print xmlrecv.decode('UTF8')
        #print xmlrecv.decode('GB2312')
        myclient.closeTCP()
