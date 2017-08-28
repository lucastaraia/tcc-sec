#from construct import Field
#from models import db
#from construct import Field

Scan = db.define_table("scan",
                       Field('id', 'integer'),
                       Field('GatewayIp', 'string'),
                       Field('Interface', 'string'),
                       Field('IdTipoStatusScan', 'integer'),
                       Field('DataInicioScan', 'datetime'),
                       format="%(Scan)s",
                       migrate=False
                       ),

ScanDispositivo = db.define_table("ScanDispositivo",
                                  Field('id', 'integer'),
                                  Field('IdScan', 'integer'),
                                  Field('Ip', 'string'),
                                  Field('Mac', 'string'),
                                  Field('NomeFabricante', 'string'),
                                  Field('nomeOs', 'string'),
                                  format="%(Scan)s",
                                  migrate=False
                                  ),

ScanDispositivoPorta = db.define_table("ScanDispositivoPorta",
                                       Field('IdScanDispositivoPorta', 'integer'),
                                       Field('Porta', 'integer'),
                                       Field('Nome', 'string'),
                                       format="%(Scan)s",
                                       migrate=False
                                       ),

TipoStatusScan = db.define_table("TipoStatusScan",
                                 Field('id', 'integer'),
                                 Field('Nome', 'string'),
                                 format="%(Scan)s",
                                 migrate=False
                                 ),

Usuario = db.define_table("Usuario",
                          Field('id', 'integer'),
                          Field('Nome', 'string'),
                          Field('Senha', 'string'),
                          format="%(Scan)s",
                          migrate=False
                          ),

Sqlite_sequence = db.define_table("sqlite_sequence",
                                  Field('name', 'string'),
                                  Field('seq', 'integer'),
                                  format="%(Scan)s",
                                  migrate=False
                                  )



