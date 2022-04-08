class options:
    send_anonymous_usage_stats = True
    webhooks = False # If set to true, configure in the webhooks class.
    auto_update = True # If set to true, the faucet will automatically update itself when a new version is released.
    lazy_load_domains = False # If set to true, the faucet will load domains from Namebase when the program starts.
    # This may lead to issues if you don't restart the program frequently and you try to load domains into that faucet that
    # came into your Namebase account before the last time you restarted the program. However, it will make loading names
    # much faster, and is reccomended if you have over 1-2k names.
    test = False
    test2 = True
    test3 = False

class encryption:
    # CHANGE THIS CHANGE THIS CHANGE THIS CHANGE THIS CHANGE THIS CHANGE THIS CHANGE THIS CHANGE THIS CHANGE THIS
    session_key = "secret" # CHANGE THIS! You must change this to a random string with no spaces and no meaning or words.
    # You should use something like http://nathanwoodburn/generator/ with max settings.
    # CHANGE THIS CHANGE THIS CHANGE THIS CHANGE THIS CHANGE THIS CHANGE THIS CHANGE THIS CHANGE THIS CHANGE THIS

class info:
    nb_cookie = "s%3A0000000000000000000000000000000000f000000000000000000000000"
    # To get your Namebase cookie, go to your Namebase dashboard, go into developer mode, 
    # click application, then double click the value for "namebase-main".
    faucet_name = "HandyFaucet" # Name of the faucet.
    faucet_address = "0x0000000000000000000000000000000000000000" # Address of the faucet.
    connections = { # Add any communities/connections for your faucet.
        "Discord": "https://discord.gg/yourdiscord",
        "Telegram": "https://t.me/yourtelegram",
        "Your Website": "https://yourwebsite.com/",
    }

class webserver:
    port = 8082 # Web port
    host = "127.0.0.1" # Where the server will listen, not the domain. Use 127.0.0.1 for local connections or 0.0.0.0 for public connections.

class admin: # The admin panel is used to load names and manage data and options. It is accessable from {yourdomain}/admin.
    path = "admin" # The path the admin panel is accessable from. It is highly reccommended to change this for extra security.
    # For example, if you set the path to "admin", the admin panel will be accessable from {yourdomain}/admin.
    # CHANGE THIS CHANGE THIS CHANGE THIS CHANGE THIS CHANGE THIS CHANGE THIS CHANGE THIS CHANGE THIS CHANGE THIS
    password = "p@$$w0rd" # CHANGE THIS! Password of the admin.
    # CHANGE THIS CHANGE THIS CHANGE THIS CHANGE THIS CHANGE THIS CHANGE THIS CHANGE THIS CHANGE THIS CHANGE THIS
    pin = 1234 # MUST be a 4 digit number. 

class webhooks: # Make sure to enable in the options class.
    # For all of the following webhooks, you can set whether certain actions will trigger webhooks,
    # the message for that action, and the URL for that action.
    # For each webhook url, you can just set the url to "default_url" (no quotes) to use the default URL.
    # If you don't want to use the default URL, you can set the url to the URL you want to use in quotes.
    default_url = "https://discord.com/api/webhooks/000000000000/ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    notify_server_start = False # If set to true, the webhook will be triggered when the server starts.
    notify_server_start_message = "@RunDavidMC The server has started."
    server_start_url = default_url

    notify_admin_login = False # It is highly recommended you configure this and set it to true to get notified when an admin logs in.
    admin_login_message = "@RunDavidMC An admin has logged in."
    admin_login_url = default_url

    notify_out_of_names = False # If set to true, the faucet will notify you when there are no more names left.
    out_of_names_message = "@RunDavidMC There are no more names left! Please refill the faucet."
    out_of_names_url = default_url

    notify_name_send_error = False # If set to true, the faucet will notify you when a name could not be sent, along with the error.
    name_send_error_message = "@RunDavidMC There was an error sending a name." # After the message, it will also send " | ERROR: {error}"
    name_send_error_url = default_url

    notify_faucet_use = False # If set to true, the faucet will notify you when a name is claimed.
    faucet_use_message = "@RunDavidMC A name was claimed!" # After the message, it will also send " | Name: {name}"
    faucet_use_url = default_url
