import sqlite3
from datetime import datetime
global dbPath
dbPath = '../../models/Scans.db'

def InsertScan(gatewayIp, interface):
    conn = sqlite3.connect(dbPath)
    c = conn.cursor()
    c.execute('INSERT INTO SCAN(gatewayIp, interface, idTipoStatusScan, dataInicioScan) VALUES (?, ?, ?, ?)', (gatewayIp, interface, 1, str(datetime.now().strftime("%d/%m/%Y %H:%M:%S"))))
    conn.commit()
    conn.close()
    return c.lastrowid

def InsertScanDispositivo(idScan, ip, mac, nomeFabricante, nomeOs):
    conn = sqlite3.connect(dbPath)
    c = conn.cursor()
    c.execute('INSERT INTO ScanDispositivo(IdScan, Ip, Mac, NomeFabricante, nomeOs) VALUES (?, ?, ?, ?, ?)', (idScan, ip, mac, nomeFabricante, nomeOs))
    conn.commit()
    conn.close()
    return c.lastrowid

def InsertScanDipositivoPorta(idScanDispositivo, porta, nome):
    conn = sqlite3.connect(dbPath)
    c = conn.cursor()
    c.execute('INSERT INTO ScanDispositivoPorta(idScanDispositivo, porta, nome) VALUES (?, ?, ?)', (idScanDispositivo, porta, nome))
    conn.commit()
    conn.close()

def UpdateScanStatus(idScan, idTipoStatusScan):
    conn = sqlite3.connect(dbPath)
    c = conn.cursor()
    c.execute('UPDATE SCAN SET idTipoStatusScan = ? WHERE id = ?', (idTipoStatusScan, idScan))
    conn.commit()
    conn.close()