# coding=utf-8
import commands
import os
import itertools
import re
import socket, struct

def login():
    return response.render("estrutura/login.html")

def dash():
    saida_ip_externo = commands.getoutput('sudo curl ifconfig.pro')
    ip_externo = saida_ip_externo.split("\n")

    from subprocess import check_output
    ips = check_output(['hostname', '--all-ip-addresses'])

    return response.render("estrutura/dash.html", ip_externo=ip_externo, ips=ips)

def relatorio():
    return response.render("estrutura/relatorio.html")

def teste():
    return response.render("estrutura/teste.html")

def scan():
    return response.render('estrutura/scan.html')

def settings():
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

    return response.render('estrutura/settings.html', retorno_apache=retorno_apache, dict_apache=dict_apache,
                           dict_openvpn=dict_openvpn, retorno_openvpn=retorno_openvpn, retorno_ssh=retorno_ssh,
                           dict_ssh=dict_ssh)

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

def get_ip():
    f = os.popen('ifconfig')
    for iface in [' '.join(i) for i in iter(lambda: list(itertools.takewhile(lambda l: not l.isspace(),f)), [])]:
        if re.findall('^(eth|wlan)[0-9]',iface) and re.findall('RUNNING',iface):
            ip = re.findall('(?<=inet\saddr:)[0-9\.]+',iface)
            if ip:
                return ip[0]
    return ip


def gateway():
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

def qtde_host():
    saida_host = commands.getoutput('sudo nmap -sP 192.168.100.0/24 | grep hosts')
    dict_host = saida_host.split(" ")
    print dict_host
    return dict_host[5]


'''for line in dict_:
        if 'running' in line:
            retorno_apache = 'Ativo'
            break
        else:
            retorno_apache = 'Inativo'''
