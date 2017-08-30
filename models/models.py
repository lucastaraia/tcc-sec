Scan = db.define_table("Scan",
                       Field('id', 'integer'),
                       Field('gatewayIp', 'string'),
                       Field('interface', 'string'),
                       Field('idTipoStatusScan', 'integer'),
                       Field('dataInicioScan', 'datetime'),
                       format="%(Scan)s",
                       migrate=False
                       ),

ScanDispositivo = db.define_table("ScanDispositivo",
                                  Field('id', 'integer'),
                                  Field('idScan', 'integer'),
                                  Field('ip', 'string'),
                                  Field('mac', 'string'),
                                  Field('nomeFabricante', 'string'),
                                  Field('nomeOs', 'string'),
                                  format="%(ScanDispositivo)s",
                                  migrate=False
                                  ),

ScanDispositivoPorta = db.define_table("ScanDispositivoPorta",
                                       Field('idScanDispositivo', 'integer'),
                                       Field('porta', 'integer'),
                                       Field('nome', 'string'),
                                       format="%(ScanDispositivoPorta)s",
                                       migrate=False
                                       ),

TipoStatusScan = db.define_table("TipoStatusScan",
                                 Field('id', 'integer'),
                                 Field('nome', 'string'),
                                 format="%(TipoStatusScan)s",
                                 migrate=False
                                 ),

Usuario = db.define_table("Usuario",
                          Field('id', 'integer'),
                          Field('nome', 'string'),
                          Field('senha', 'string'),
                          format="%(Usuario)s",
                          migrate=False
                          )
