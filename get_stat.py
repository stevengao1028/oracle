
# !/usr/bin/env python
# -*- coding: UTF-8 -*-
import psutil
import time
import urllib2
import json
import socket
import requests
from datetime import datetime

class sys_info:
    def __init__(self):
        self.data = {}
    # def cpu_stat():
    #     cpu = []
    #     cpuinfo = {}
    #     f = open("/proc/cpuinfo")
    #     lines = f.readlines()
    #     f.close()
    #     for line in lines:
    #         if line == '\n':
    #             cpu.append(cpuinfo)
    #             cpuinfo = {}
    #         if len(line) < 2: continue
    #         name = line.split(':')[0].rstrip()
    #         var = line.split(':')[1]
    #         cpuinfo[name] = var
    #     return cpu
    def host_name(self):
        return socket.gethostname()

    def host_time(self):
        now_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        return now_time


    def cpu_info(self):
        cpu={}
        cpu['rate']=psutil.cpu_percent()
        cpu['lcount']=psutil.cpu_count()
        cpu['pcount']=psutil.cpu_count(logical=False)
        # cpu['times']=psutil.cpu_times()
        return cpu

    def memory_info(self):
        mem = {}
        f = open("/proc/meminfo")
        lines = f.readlines()
        f.close()
        for line in lines:
            if len(line) < 2: continue
            elif line.split(':')[0] in ['MemTotal','MemFree','MemAvailable','SwapTotal','SwapFree','Buffers','Cached']:
                name = line.split(':')[0]
                var = int(line.split(':')[1].split()[0]) / 1024
                mem[name] = var
        mem['MemUsed'] = mem['MemTotal'] - mem['MemFree'] - mem['Buffers'] - mem['Cached']
        return mem


    def load_info(self):
        loadavg = {}
        f = open("/proc/loadavg")
        con = f.read().split()
        f.close()
        loadavg['lavg_1']=float(con[0])
        loadavg['lavg_5']=float(con[1])
        loadavg['lavg_15']=float(con[2])
        # loadavg['nr']=float(con[0])
        loadavg['last_pid']=int(con[4])
        return loadavg


    def uptime_info(self):
        uptime = {}
        f = open("/proc/uptime")
        con = f.read().split()
        f.close()
        all_sec = float(con[0])
        MINUTE,HOUR,DAY = 60,3600,86400
        uptime['day'] = int(all_sec / DAY )
        uptime['hour'] = int((all_sec % DAY) / HOUR)
        uptime['minute'] = int((all_sec % HOUR) / MINUTE)
        uptime['second'] = int(all_sec % MINUTE)
        uptime['Free rate'] = float(con[1]) / float(con[0])
        return uptime

    def net_info(self):
        net = []
        f = open("/proc/net/dev")
        lines = f.readlines()
        f.close()
        for line in lines[2:]:
            con = line.split()
            intf = {}
            intf['interface'] = con[0].lstrip(":")
            intf['ReceiveBytes'] = int(con[1])
            # intf['ReceivePackets'] = int(con[2])
            # intf['ReceiveErrs'] = int(con[3])
            # intf['ReceiveDrop'] = int(con[4])
            # intf['ReceiveFifo'] = int(con[5])
            # intf['ReceiveFrames'] = int(con[6])
            # intf['ReceiveCompressed'] = int(con[7])
            # intf['ReceiveMulticast'] = int(con[8])
            intf['TransmitBytes'] = int(con[9])
            # intf['TransmitPackets'] = int(con[10])
            # intf['TransmitErrs'] = int(con[11])
            # intf['TransmitDrop'] = int(con[12])
            # intf['TransmitFifo'] = int(con[13])
            # intf['TransmitFrames'] = int(con[14])
            # intf['TransmitCompressed'] = int(con[15])
            # intf['TransmitMulticast'] = int(con[16])
            # intf = dict(
            #     zip(
            #         ('interface', 'ReceiveBytes', 'ReceivePackets',
            #          'ReceiveErrs', 'ReceiveDrop', 'ReceiveFifo',
            #          'ReceiveFrames', 'ReceiveCompressed', 'ReceiveMulticast',
            #          'TransmitBytes', 'TransmitPackets', 'TransmitErrs',
            #          'TransmitDrop', 'TransmitFifo', 'TransmitFrames',
            #          'TransmitCompressed', 'TransmitMulticast'),
            #         (con[0].rstrip(":"), int(con[1]), int(con[2]),
            #          int(con[3]), int(con[4]), int(con[5]),
            #          int(con[6]), int(con[7]), int(con[8]),
            #          int(con[9]), int(con[10]), int(con[11]),
            #          int(con[12]), int(con[13]), int(con[14]),
            #          int(con[15]), int(con[16]),)
            #     )
            # )
            net.append(intf)
        return net

    def disk_info(self,diskname):
        hd={}
        disk_info=psutil.disk_usage(diskname)
        hd['name'] = diskname
        hd['total'] = disk_info.total/(1024*1024*1024)
        hd['used'] = disk_info.used/(1024*1024*1024)
        hd['free'] = disk_info.free / (1024 * 1024 * 1024)
        hd['percent'] =disk_info.percent / (1024 * 1024 * 1024)
        return hd
    def all_info(self):
        self.data['name'] = self.host_name()
        self.data['time'] = self.host_time()
        self.data['cpu']=self.cpu_info()
        self.data['disk']=self.disk_info("/")
        self.data['mem']=self.memory_info()
        self.data['uptime']=self.uptime_info()
        self.data['net']=self.net_info()
        self.data['load']=self.load_info()
        return self.data


if __name__ == "__main__":
    while True:
        send_info = sys_info()
        data = send_info.all_info()
        print data
        req = urllib2.Request("http://192.168.50.81:8888", json.dumps(data), {'Content-Type': 'application/json'})
        f = urllib2.urlopen(req)
        response = f.read()
        print response
        f.close()
        time.sleep(5)







