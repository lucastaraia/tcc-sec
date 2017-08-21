def scanNetwork(network):
    returnlist = []
    import nmap
    nm = nmap.PortScanner()
    a = nm.scan(hosts=network, arguments='-O')
    for k, v in a['scan'].iteritems():
        if str(v['status']['state']) == 'up':
            try:
                try:
                    if 'Windows' in str(v['osmatch']):
                        os = 'Windows'
                    elif 'Linux'in str(v['osmatch']):
                        os = 'Linux'
                    else:
                        os = 'Outro'
                except:
                    os = 'Outro'
                try:
                    vendor = str(v['vendor'][v['addresses']['mac']])
                except:
                    vendor = 'Indefinido'
                try:
                    mac = str(v['addresses']['mac'])
                except Exception, e:
                    mac = 'Indefinido'
                
                try:
                    keys = v['tcp'].keys()
                except:
                    keys = []

                portas = []
                for porta in keys:
                    portas.append([porta, v['tcp'][porta]['name']])

                returnlist.append([str(v['addresses']['ipv4']), mac, vendor, os, portas])
            except Exception, e:
                pass

    return returnlist
