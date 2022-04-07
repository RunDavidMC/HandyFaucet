from queue import Empty


class options:
    send_anonymous_usage_stats = True
    webhooks = False # If set to true, configure in the webhooks class.
    faucet_name = "IoniFaucet" # Name of the faucet.
    auto_update = True # If set to true, the faucet will automatically update itself when a new version is released.

class info:
    nb_cookie = "s%3A00000000000000000000000000000000000000000000000"
    # To get your Namebase cookie, go to your Namebase dashboard, go into developer mode, 
    # click application, then double click the value for "namebase-main".

class webserver:
    port = 8082 # Web port
    host = "127.0.0.1" # Where the server will listen, not the domain. Use 127.0.0.1 for local connections or 0.0.0.0 for public connections.

class webhooks: # Make sure to enable in the options class.
    empty = 0
