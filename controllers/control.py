# coding=utf-8
import commands
import itertools
import os
import platform
import re
import socket
import struct
from datetime import datetime

def login(): ######## Tela Login #######
    form = auth.login()
    form.element(_name='password')['_placeholder'] = "Senha"
    form.element(_name='username')['_placeholder'] = "Usuário"
    #form.element(_name='password')['_class'] = ""

    return response.render("estrutura/login.html", form=form)



@auth.requires_login()
def dash(): ######## Tela dashboard ########
    ##qtde_os = qtde_so()
    from subprocess import check_output
    saida_ip_externo = commands.getoutput('sudo curl ifconfig.pro')
    ip_externo = saida_ip_externo.split("\n")

    ips = check_output(['hostname', '--all-ip-addresses'])

    idScan = db(db.Scan).select()[-1].id
    gatewayIp = db(db.Scan).select()[-1].gatewayIp

    windows_disp = db((db.ScanDispositivo.nomeOs == "Windows") & (db.ScanDispositivo.idScan == idScan)).select().as_list()
    count_windows = len(windows_disp)

    linux_disp = db((db.ScanDispositivo.nomeOs == "Linux") & (db.ScanDispositivo.idScan == idScan)).select().as_list()
    count_linux = len(linux_disp)

    outros_disp = db((db.ScanDispositivo.nomeOs == "Outro") & (db.ScanDispositivo.idScan == idScan)).select().as_list()
    count_outros = len(outros_disp)

    dispositivos = db(db.ScanDispositivo.idScan == idScan).select().as_list()
    portas = []

    for disp in dispositivos:
        porta = db(db.ScanDispositivoPorta.idScanDispositivo == disp['id']).select().as_list()
        disp['qtdPortas'] = len(porta)
        for por in porta:
            portas.append(por)
    
    count_portas = len(portas)

    return response.render("estrutura/dash.html", ip_externo=ip_externo, ips=ips, count_windows=count_windows,
                           count_linux=count_linux, count_outros=count_outros, count_portas=count_portas, count_disp=len(dispositivos),
                           windows_disp=windows_disp, linux_disp=linux_disp, outros_disp=outros_disp, disp=dispositivos, gatewayIp=gatewayIp)

@auth.requires_login()
def relatorio(): ######## Tela Relatório ########
    return response.render("estrutura/relatorio.html")

def GetQtdPortasAbertas():
    porta = request.vars['porta']
    idScan = db(db.Scan).select()[-1].id

    qtd = db((db.ScanDispositivo.id == db.ScanDispositivoPorta.idScanDispositivo) & (db.ScanDispositivo.idScan == idScan) & (db.ScanDispositivoPorta.porta == porta)).select().as_list()
    return len(qtd)

def buscaScans():
    data = request.vars['data']
    ip = request.vars['ip']
    comando = '''SELECT 	s.dataInicioScan,   
        sd.ip,
        sd.mac,
        sd.nomeFabricante,
        sd.nomeOs,
        IFNULL((SELECT group_concat(porta, ', ') FROM ScanDispositivoPorta sp WHERE sp.idScanDispositivo = sd.id), '') AS portas
    FROM Scan s
    INNER JOIN ScanDispositivo sd
        ON s.id = sd.idScan
    '''

    if ip:
        comando += 'WHERE sd.ip like\'' + str(ip) + '%\''
    elif ip and data:
        comando += 'AND s.dataInicioScan like \'' + str(data) + '%\''
    else:
        comando += 'WHERE s.dataInicioScan like \'' + str(data) + '%\''

    dispositivos = db.executesql(comando)

    return response.render("estrutura/gridRelatorio.html", dispositivos=dispositivos)

@auth.requires_login()
def scan(): ######## Tela Scan onde 'starta' os scans ########
    return response.render('estrutura/scan.html')

def hydra():
    saida_hydra = commands.getoutput("sudo hydra -L ~/wordlist -P ~/wordlist http-get://192.168.0.1:80")
    if 'successfully' in saida_hydra:
        retorno_hydra = True
    else:
        retorno_hydra = False

    return retorno_hydra

def script_scan():
    saida_script = commands.getoutput("sudo python /var/www/web2py/applications/tcc/scripts/NetworkScan/NetworkScan.py")
    if 'True' in saida_script:
        retorno_script_scan = True
    else:
        retorno_script_scan = False

    return retorno_script_scan

@auth.requires_login()
def settings(): ######## Tela de Configurações ########
    ### Serviços - iniciar/parar/reiniciar ###
    server = get_server()
    saida_apache = commands.getoutput('sudo /etc/init.d/apache2 status')
    dict_apache = saida_apache.split("\n")
    retorno_apache = None
    for line in dict_apache:
        if 'running' in line:
            retorno_apache = 'Ativo'
            break
        else:
            retorno_apache = 'Inativo'

    saida_openvpn = commands.getoutput('sudo /etc/init.d/openvpn status')
    dict_openvpn = saida_openvpn.split("\n")
    retorno_openvpn = None
    for line in dict_openvpn:
        if 'inactive' in line:
            retorno_openvpn = 'Inativo'
            break
        else:
            retorno_openvpn = 'Ativo'

    saida_ssh = commands.getoutput('sudo /etc/init.d/ssh status')
    dict_ssh = saida_ssh.split("\n")
    retorno_ssh = None
    for line in dict_ssh:
        if 'inactive' in line:
            retorno_ssh = 'Inativo'
            break
        else:
            retorno_ssh = 'Ativo'

    ### Termina Serviços ###

    ### Sistema Operacional ###
    saida_os = commands.getoutput("lsb_release -a")
    dict_os = saida_os.split("\n")
    dict_os1 = dict_os[1].split("\t")
    retorno_dict_os = dict_os1[1]

    ### LOAD ###

    saida_load = commands.getoutput("uptime")
    dict_load = saida_load.split(":")
    retorno_dict_load = dict_load[4]

    return response.render('estrutura/settings.html', retorno_apache=retorno_apache, dict_apache=dict_apache,
                           dict_openvpn=dict_openvpn, retorno_openvpn=retorno_openvpn, retorno_ssh=retorno_ssh,
                           dict_ssh=dict_ssh, server=server, retorno_dict_os=retorno_dict_os, retorno_dict_load=retorno_dict_load)

############################

def iniciar_servico_apache():
    try:
        os.system('sudo /etc/init.d/apache2 start')
    except Exception as error:
        return error

def parar_servico_apache():
    try:
        os.system('sudo /etc/init.d/apache2 stop')
    except Exception as error:
        return error


def reiniciar_servico_apache():
    try:
        os.system('sudo /etc/init.d/apache2 restart')
    except Exception as error:
        return error

############################

def iniciar_servico_openvpn():
    try:
        os.system("sudo /etc/init.d/openvpn start")
    except Exception as error:
        return error

def parar_servico_openvpn():
    try:
        os.system("sudo /etc/init.d/openvpn stop")
    except Exception as error:
        return error


def reiniciar_servico_openvpn():
    try:
        os.system("sudo /etc/init.d/openvpn restart")
    except Exception as error:
        return error

############################

def iniciar_servico_ssh():
    try:
        os.system("sudo /etc/init.d/ssh start")
    except Exception as error:
        return error

def parar_servico_ssh():
    try:
        os.system("sudo /etc/init.d/ssh stop")
    except Exception as error:
        return error


def reiniciar_servico_ssh():
    try:
        os.system("sudo /etc/init.d/ssh restart")
    except Exception as error:
        return error

#######################################################################

def get_ip(): ### Função que retorna endereço ip das interfaces LAN/WLAN ###
    global ip
    f = os.popen('ifconfig')
    for iface in [' '.join(i) for i in iter(lambda: list(itertools.takewhile(lambda l: not l.isspace(),f)), [])]:
        if re.findall('^(eth|wlan)[0-9]',iface) and re.findall('RUNNING',iface):
            ip = re.findall('(?<=inet\saddr:)[0-9\.]+',iface)
            if ip:
                return ip[0]
    return ip


def gateway(): ### Retorna endereço IP do gateway ###
    """Read the default gateway directly from /proc."""
    with open("/proc/net/route") as fh:
        for line in fh:
            fields = line.strip().split()
            if fields[1] != '00000000' or not int(fields[3], 16) & 2:
                continue

            return socket.inet_ntoa(struct.pack("<L", int(fields[2], 16)))

'''Funções Teste
ip_interno = commands.getoutput('sudo ifconfig eth1 | grep "inet\ addr" | cut -d: -f2 | cut -d" " -f1') '''


#######################################################################


def qtde_host(): ######## Quantidade de host na rede, irá retornar todos dispositivos que estão conectados ########
    saida_host = commands.getoutput('sudo nmap -sP 192.168.100.0/24 | grep hosts')
    dict_host = saida_host.split(" ")

    return dict_host[5]


#def qtde_so(): ######## Retorna quantidade de Windows e Linux conectados à rede ########
#    qtde_os = {}
#    qtde_os['Windows'] = commands.getoutput('sudo nmap --top-ports 1 -O -F -n -Pn -r 192.168.1.0/24 | grep "Running: "> /tmp/os; echo "$(cat /tmp/os | grep -i Windows | wc -l)"')
#    qtde_os['Linux'] = commands.getoutput('sudo nmap --top-ports 1 -O -F -n -Pn -r 192.168.1.0/24 | grep "Running: "> /tmp/os; echo "$(cat /tmp/os | grep -i Linux | wc -l)"')

    #return str(qtde_os).replace('{','').replace('}','')


def get_server(): ######## Informações de hardware/software da Raspberry ########
    server = {}
    #var = platform.platform()
    #server['distribuicao'] = var.split('-')[6]
    #server['versao'] = var.split('-')[7]
    server['arch'] = platform.processor()
    server['host'] = platform.uname()[1]
    server['kernel'] = platform.uname()[2]
    server['pythonv'] = platform.python_version()
    server['memory'] = int(commands.getoutput("cat /proc/meminfo | grep MemTotal").split(':')[1].split('k')[0])/1000
    disk = os.statvfs("/")
    totalBytes = float(disk.f_bsize*disk.f_blocks)
    server['disk'] = "%.2f GBytes" % (totalBytes/1024/1024/1024)

    #var = commands.getoutput("atop | grep cpu")
    return server


### Função para mostrar hora real time ###
def atualiza_hora():
    from datetime import datetime
    item = str(datetime.now().strftime('%H:%M:%S - %d/%m/%Y'))

    return item
