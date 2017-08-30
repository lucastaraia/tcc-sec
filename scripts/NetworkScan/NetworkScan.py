import time
import os
import sys
import logging
import math
from time import sleep
import urllib2 as urllib
import traceback

from scapy.all import *
import scan
import DataBaseManagement as db

def func_scan():
    try:
        def GetGatewayIp():
            getGateway_p = sr1(IP(dst="google.com", ttl=0) / ICMP() / "XXXXXXXXXXX", verbose=False)
            return getGateway_p.src


        def getDefaultInterface(returnNet=False):
            def long2net(arg):
                if (arg <= 0 or arg >= 0xFFFFFFFF):
                    raise ValueError("illegal netmask value", hex(arg))
                return 32 - int(round(math.log(0xFFFFFFFF - arg, 2)))

            def to_CIDR_notation(bytes_network, bytes_netmask):
                network = scapy.utils.ltoa(bytes_network)
                netmask = long2net(bytes_netmask)
                net = "%s/%s" % (network, netmask)
                if netmask < 16:
                    return None
                return net

            iface_routes = [route for route in scapy.config.conf.route.routes if route[3]
                            == scapy.config.conf.iface and route[1] != 0xFFFFFFFF]
            network, netmask, _, interface, address = max(
                iface_routes, key=lambda item: item[1])
            net = to_CIDR_notation(network, netmask)
            if net:
                if returnNet:
                    return net
                else:
                    return interface


        def scanNetwork():
            global hostsList
            try:
                hostsList = scan.scanNetwork(getDefaultInterface(True))
            except:
                raise SystemExit


        def getDefaultInterfaceMAC():
            try:
                defaultInterfaceMac = get_if_hwaddr(defaultInterface)
                if defaultInterfaceMac == "" or not defaultInterfaceMac:
                    defaultInterfaceMac = raw_input(header)
                    return defaultInterfaceMac
                else:
                    return defaultInterfaceMac
            except:
                defaultInterfaceMac = raw_input(header)
                return defaultInterfaceMac


        defaultInterface = getDefaultInterface()
        defaultGatewayIP = GetGatewayIp()
        defaultInterfaceMac = getDefaultInterfaceMAC()

        global defaultGatewayMacSet
        defaultGatewayMacSet = False
        idScan = db.InsertScan(defaultGatewayIP, defaultInterface)
        scanNetwork()

        for host in hostsList:
            idDispositivo = db.InsertScanDispositivo(idScan, host[0], host[1], host[2], host[3])
            try:
                for porta in host[4]:
                    db.InsertScanDipositivoPorta(idDispositivo, porta[0], porta[1])
            except:
                pass

        db.UpdateScanStatus(idScan, 2)

        return True

    except Exception as error:
        return str(error)

print func_scan()