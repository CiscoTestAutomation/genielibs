'''
Viptela specific clean stages
'''

# Python
import re
import time
import logging

# pyATS
from pyats import aetest
from pyats.async_ import pcall
from pyats.utils.fileutils import FileUtils

# Genie
from genie.utils import Dq
from genie.abstract import Lookup
from genie.libs import clean
from genie.libs.clean.utils import (clean_schema, _apply_configuration,
                                    handle_rommon_exception)
from genie.libs.clean.recovery.iosxe.sdwan.recovery import recovery_worker as sdwan_recovery_worker
from genie.libs.clean.recovery.recovery import _disconnect_reconnect
from genie.metaparser.util.schemaengine import Optional, Or
from genie.utils.timeout import Timeout
from genie.libs.clean import BaseStage
from genie.libs.clean.stages.stages import Connect as BaseConnect

from genie.libs.sdk.libs.abstracted_libs.iosxe.subsection import get_default_dir

# Unicon
from unicon.eal.dialogs import Statement, Dialog

# Logger
log = logging.getLogger(__name__)


class SoftwareInstall(BaseStage):
    """Software install

Stage Schema
------------
software_install:
    origin:
        files (list): Image files location on the server.
        hostname (str): Hostname or address of the server.
    protocol (str): Protocol used for copy operation. 
    vpn (int): Vpn number used to copy.
    timeout (int, optional): Copy operation timeout in seconds. Defaults to 600.

Example
-------
software_install:
    origin:
        files:
            - /home/user/viptela-20.3.4-x86_64.tar.gz
        hostname: 10.1.1.1
    protocol: ftp # only ftp is supported
    vpn: 512
    timeout: 900
"""

    version = ''

    # =================
    # Argument Defaults
    # =================
    TIMEOUT = 600

    # ============
    # Stage Schema
    # ============
    schema = {
        'origin': {
            'files': list,
            'hostname': str,
        },
        'protocol': str,
        'vpn': int,
        Optional('timeout'): int,
    }

    # ==============================
    # Execution order of Stage steps
    # ==============================
    exec_order = ['software_install', 'software_activate']

    def software_install(self,
                         steps,
                         device,
                         origin,
                         protocol,
                         vpn,
                         timeout=TIMEOUT):

        with steps.start("Installing viptela software") as step:

            # capture software status before installation
            device.execute('show software')

            hostname = origin['hostname']
            filename = origin['files'][0]

            username = Dq(device.testbed.raw_config).contains_key_value(
                'testbed',
                'servers').contains(hostname,
                                    level=-1).get_values('username', 0)
            password = Dq(device.testbed.raw_config).contains_key_value(
                'testbed',
                'servers').contains(hostname,
                                    level=-1).get_values('password', 0)

            if username and password:
                output = device.execute(
                    f'request software install {protocol}://{username}:{password}@{hostname}/{filename} vpn {vpn}',
                    timeout=timeout)
            else:
                output = ''
                step.failed(
                    f"Server {hostname} credential couldn't be found in testbed yaml. Please check and update testbed yaml accordingly."
                )

            m = re.search(r'.*Successfully installed version: (?P<ver>\S+)',
                          output)
            if m:
                self.version = m.groupdict()['ver']

            if not self.version:
                step.failed('Failed to install software.')

    def software_activate(self, steps, device, timeout):

        with steps.start("Activating viptela software") as step:

            _, password = device.api.get_username_password()

            device.sendline(f'request software activate {self.version}')
            device.expect([r'Are you sure you want to proceed\? \[yes,NO\]'],
                          timeout=60)
            device.sendline('yes')
            try:
                device.expect([r'System Ready'], timeout=timeout)
            except Exception:
                # 'System Ready' message might not be appeared.
                # In that case, move forward with best effort.
                pass

            device.sendline()
            device.expect(['login:'])
            device.sendline('admin')
            device.expect(['Password:'])
            device.sendline('admin')
            device.expect(['Password:'])
            device.sendline(password)
            device.expect(['Re-enter password:'])
            device.sendline(password)

            step.passed(f"{self.version} is successfully installed.")