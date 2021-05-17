
# -*- coding: utf-8 -*-
import socket
import struct
import time

class iCloudClient(object):
    
    def __init__(self, serverhost = 'localhost', serverport = 8888, buffersize = 4096, timeout = -1, sleeptime = 0):
        self.serverhost = serverhost
        self.serverport = serverport
        self.buffersize = buffersize
        self.timeout    = timeout
        self.sleeptime  = sleeptime
        self.mysocket   = None
    
    def establishTCP(self):
        try:
            self.mysocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.mysocket.connect((self.serverhost, self.serverport))
            if(self.timeout > 0):
                self.mysocket.settimeout(self.timeout)
            return True
        except Exception as e:
            print '[socket]connect error -',
            print e
            return False
    
    def closeTCP(self):
        if(self.mysocket):
            self.mysocket.close()
    
    def handle(self, nameprex, int16data, baseline, scale, freq, segnum, aggmethod):
        mybuffer = self.writeBYFile(nameprex, int16data, baseline, scale, freq, segnum, aggmethod)
        seqid    = 0
        istart   = 0
        ilen     = self.buffersize - 4
        pkgnum   = 1.0 * len(mybuffer)/ilen
        try:
            vflag = True
            while(vflag):
                pkg_buff  = mybuffer[istart:istart + ilen]
                istart  += ilen
                seqid   += 1
                pkg_len = len(pkg_buff)
                if(pkgnum <= 1):
                    pkg_head = 0xFF
                    pkg_flag = 0x00
                    vflag    = False
                else:
                    if(seqid == 1):
                        pkg_head = 0xFF
                        pkg_flag = 0x0A
                    elif(seqid < pkgnum):
                        pkg_head = 0xFF
                        pkg_flag = 0x0B
                    else:
                        pkg_head = 0xFF
                        pkg_flag = 0x0C
                        vflag    = False
                fmt     = '!2BH{}s'.format(pkg_len)
                tcpbyte = struct.pack(fmt, pkg_head, pkg_flag, pkg_len, pkg_buff)
                bret = 1
                self.mysocket.sendall(tcpbyte)
                time.sleep(self.sleeptime)
            recvdata = ''
            recvlen  = 0
            pkg_len  = 0
            while(True):
                bret      = 2
                tcpbyte   = self.mysocket.recv(self.buffersize)
                recvdata += tcpbyte
                recvlen  += len(tcpbyte)
                if(pkg_len == 0 and recvlen > 4):
                    pkg_head, pkg_flag, pkg_len = struct.unpack('!2BH', recvdata[:4])
                if(pkg_len > 0  and pkg_len + 4 == recvlen):
                    break
            return recvdata[4:]
        except Exception as e:
            if(bret == 1):
                print '[socket]send error -',
            elif(bret == 2):
                print '[socket]recv error -',
            else:
                print '[socket]unknown error -',
            print e
            return ''
    
    def writeBYFile(self, nameprex, int16data, baseline, scale, freq, segnum, aggmethod):
        leadC, frameC = int16data.shape
        if(leadC == 1):
            title = ['II']
        elif(leadC == 8):
            title = ['II','III','V1','V2','V3','V4','V5','V6']
        else:
            raise TypeError('please check the parameter [int16data]!');
        outbuffer  = "<?xml version=\"1.0\" encoding=\"UTF-8\" ?>\n"
        outbuffer += "<ECG-Data>\n"
        outbuffer += "<head>\n"
        outbuffer += "<dev>IECG</dev>\n"
        outbuffer += "<ver>1</ver>\n"
        outbuffer += ("<seq>"       + nameprex       + "</seq>\n")
        outbuffer += ("<freq>"      + str(freq)      + "</freq>\n")
        outbuffer += ("<base>"      + str(baseline)  + "</base>\n")
        outbuffer += ("<scale>"     + str(scale)     + "</scale>\n")
        outbuffer += "<unit>mV</unit>\n"
        outbuffer += ("<aggmethod>" + str(aggmethod) + "</aggmethod>\n")
        outbuffer += ("<segnum>"    + str(segnum)    + "</segnum>\n")
        outbuffer += "</head>\n"
        for i in xrange(leadC):
            outbuffer += ("<data lead=\"" + title[i] + "\">")
            for j in xrange(frameC):
                outbuffer += (str(int16data[i,j]) + " ")
            outbuffer += "</data>\n"
        outbuffer += "</ECG-Data>"
        return outbuffer
