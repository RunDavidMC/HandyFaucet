def verify(cxt):
    cxt.execute("CREATE TABLE IF NOT EXISTS claims (name TEXT, email TEXT, ip TEXT, time INTEGER, PRIMARY KEY(name))")
    cxt.execute("CREATE TABLE IF NOT EXISTS names (name TEXT, PRIMARY KEY(name))")