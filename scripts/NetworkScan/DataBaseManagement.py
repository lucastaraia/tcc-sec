import sqlite3
from datetime import datetime
global dbPath
dbPath = 'Scans.db'

def InsertScan(GatewayIp, Interface):
    conn = sqlite3.connect(dbPath)
    c = conn.cursor()
    c.execute('INSERT INTO SCAN(GatewayIp, Interface, IdTipoStatusScan, DataInicioScan) VALUES (?, ?, ?, ?)', (GatewayIp, Interface, 1, str(datetime.now())))
    conn.commit()
    conn.close()
    return c.lastrowid

def InsertScanDispositivo(IdScan, Ip, Mac, NomeFabricante, NomeOs):
    conn = sqlite3.connect(dbPath)
    c = conn.cursor()
    c.execute('INSERT INTO ScanDispositivo(IdScan, Ip, Mac, NomeFabricante, nomeOs) VALUES (?, ?, ?, ?, ?)', (IdScan, Ip, Mac, NomeFabricante, nomeOs))
    conn.commit()
    conn.close()
    return c.lastrowid

def InsertScanDipositivoPorta(IdScanDispositivo, Porta, Nome):
    conn = sqlite3.connect(dbPath)
    c = conn.cursor()
    c.execute('INSERT INTO ScanDispositivoPorta(IdScanDispositivo, Porta, Nome) VALUES (?, ?, ?)', (IdScanDispositivo, Porta, Nome))
    conn.commit()
    conn.close()

def UpdateScanStatus(IdScan, IdTipoStatusScan):
    conn = sqlite3.connect(dbPath)
    c = conn.cursor()
    c.execute('UPDATE SCAN SET IdTipoStatusScan = ? WHERE Id = ?', (IdTipoStatusScan, IdScan))
    conn.commit()
    conn.close()