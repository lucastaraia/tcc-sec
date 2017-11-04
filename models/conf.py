# -*- coding: utf-8 -*-
db = DAL("sqlite://Scans.db", folder="/var/www/web2py/applications/tcc/models", auto_import=True)

from gluon.tools import Auth

#Configuração Auth
auth = Auth(db, controller="control",function="login")
auth.settings.formstyle = "divs"
auth.settings.login_next = URL(a='tcc', c='control', f='dash')
auth.settings.remember_me_form = False
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.settings.actions_disabled = ['register']
auth.settings.expiration = 3600  # seconds

#Mensagens de Erro
auth.messages.logged_in = 'Bem Vindo'
auth.messages.access_denied = 'Acesso negado! Contate o administrador'
auth.messages.invalid_username = 'Usuario Inválido '
auth.messages.invalid_login = 'Usuario ou Senha Inválidos'
auth.messages.invalid_password = 'Senha Inválida'
auth.messages.login_button = "Entrar"
auth.messages.label_email = 'E-mail'
auth.messages.label_password = 'Password'