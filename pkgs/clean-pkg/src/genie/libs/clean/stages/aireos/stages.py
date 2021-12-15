'''
AIREOS specific clean stages
'''

# Python
import logging

# pyATS
from pyats.async_ import pcall
from pyats.utils.secret_strings import to_plaintext,SecretString 

# Genie
from genie.abstract import Lookup
from genie.libs import clean
from genie.metaparser.util.schemaengine import Optional
from genie.utils.timeout import Timeout
from genie.libs.clean import BaseStage
from genie.libs.clean.stages.stages import PowerCycle as BasePowerCycle

# Unicon
from unicon.eal.dialogs import Statement, Dialog

# Logger
log = logging.getLogger(__name__)

class CliBoot(BaseStage):
    """This stage boot the device from CLI using the following steps:

    - Using the provided info to download the requested boot image
    - Waiting for the image download
    - Reboot the device

Stage Schema
------------
CliBoot:

    filename (str): The name of the file to be using to download.

    username (str, optional): FTP username if using FTP protocol
    
    password (str, optional): FTP password if using FTP protocol

    protocol (str): Supporting TFTP/FTP, default is FTP

    path (str): A path to the image location

    tftp_server (str): an IP address for tftp server
    


Example
-------
cli_boot:
    filename: 'AIR-CT3504-K9-8-8-111-0.aes'
    timeout: 1000
    username: rcpuser
    password: cisco123$
    protocol: ftp
    tftp_server: 10.10.2.10
    path: /auto/my-ftp/
"""
    # =================
    # Argument Defaults
    # =================
    RELOAD_TIMEOUT = 800
    PROTOCOL='ftp'
    USERNAME=None
    PASSWORD=None

    # ============
    # Stage Schema
    # ============
    schema = {
        'filename': str,
        'tftp_server': str,
        'protocol': str,
        'path': str,
        Optional('username'): str,
        Optional('password'): str,
        Optional('timeout'): int,
    }

    # ==============================
    # Execution order of Stage steps
    # ==============================
    exec_order = [
        'cli_boot',
        'reload_device',
        'wait_for_prompt'
    ]
            
    def cli_boot(self, steps, device, filename, path, tftp_server, \
                 protocol=PROTOCOL,username=USERNAME, password=PASSWORD
    ):      
        with steps.start("Setting up to download image {name}".format(name=device.name)) as step:

            device.execute(['transfer download datatype code',
                            f'transfer download serverip {tftp_server}',
                            f'transfer download path {path}',
                            f'transfer download filename {filename}'
                        ])
            if 'tftp' in protocol:
                device.execute('transfer download mode tftp')
            else:
                device.execute(['transfer download mode ftp',
                               f'transfer download username {username}',
                               f'transfer download password {password}'
                            ])

            device.execute('transfer download start')

    def reload_device(self, steps, device):
        with steps.start("Reboot the device {}".format(device.name)) as step:
            log.info("Device is reloading")
            device.reload()
            device.destroy()

    def wait_for_prompt(self, steps, device, reload_time=RELOAD_TIMEOUT):
        with steps.start("Waiting for {name} to reload".format(name=device.name)) \
            as step:
            timeout = Timeout(reload_time, 10)
            while timeout.iterate():
                timeout.sleep()
                device.destroy()

                try:
                    device.connect(learn_hostname=True)
                except Exception as e:
                    connect_exception = e
                    log.info('{} is not ready'.format(device.name))
                else:
                    step.passed("{} has successfully reloaded".format(device.name))
            
            step.failed(f"{device.name} failed to reload", from_exception=connect_exception)
