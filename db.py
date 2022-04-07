def verify(cnx):
    cxt = cnx.cursor()
    cxt.execute("CREATE TABLE IF NOT EXISTS names (name TEXT, email TEXT, ip TEXT, time INTEGER, PRIMARY KEY(name))")