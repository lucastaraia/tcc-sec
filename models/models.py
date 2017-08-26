Scan = db.define_table("scan",
                               Field('Id','integer'),
                               Field('GatewayIp','string'),
                               Field('Interface','string'),
                               Field('IdTipoStatusScan','integer'),
                               Field('DataInicioScan','datetime'),
                               format="%(Scan)s",
                               migrate=False
                               )
