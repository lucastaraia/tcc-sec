import datetime
import time
ts = time.time()
st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
def gravar(log, erro = False):
    with open("log.txt", "w") as text_file:
        text_file.writelines('[' + st + '] - ' + 'Erro: ' if erro else '[' + st + '] - ' + 'Log: ' + str(log))