# HandyFaucet
 
#### HandyFaucet is a program that anyone can use to run their own Handshake domain faucet.

## Setup

Make sure you have Python and Git installed on your system.

To get started, download the [latest release](https://github.com/RunDavidMC/HandyFaucet/releases/latest) or use ``git clone https://github.com/RunDavidMC/HandyFaucet.git``. 
However, if you download a release rather than using git, the auto updater WILL NOT WORK.

Once you have downloaded the program, navigate to its directory and run ``pip install -r requirements.txt``.

Copy the contents of ``example.config.py`` into a new file named ``config.py``, and configure everything to your liking.
Make sure you change ``secret``, ``path``, ``password``, and ``pin``.

You're ready to go!
Just run ``python3 main.py`` to start the program, and navigate to your admin path to load names!
