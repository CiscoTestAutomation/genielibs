'''
ncs540/IOSXR specific clean stages
'''

# Python
import os
import time
import logging
import re

# Genie
from genie.utils.timeout import Timeout
from genie.libs.clean import BaseStage
from genie.metaparser.util.schemaengine import Optional

# Unicon
from unicon.eal.dialogs import Statement, Dialog

# Logger
log = logging.getLogger(__name__)


class InstallImage(BaseStage):
    """This stage installs the provided image onto your device using the install CLI.

Stage Schema
------------
install_image:

    image (list): Image to install on the device.

    protocol (str, optional): Protocol (http or ftp) used for the install operation.
         Defaults to http.

    server (str, optional): Hostname or address of the server to install.

    vrf (str, optional): Vrf used to copy. Defaults to default.

    install_timeout (int, optional): Max time in seconds allowed for install
        operations. Defaults to 300.

    commit_sleep (int, optional): Time in seconds to sleep before executing
        'install commit'. Defaults to 180.

Example
-------
install_image:
    image:
        - /path/image.iso
    install_timeout: 1500
    commit_sleep: 200

or

install_image:
    image:
        - /http_path/image.iso
    protocol: http
    server: 10.1.1.1
    vrf: default
    install_timeout: 2700
    commit_sleep: 180
"""

    # =================
    # Argument Defaults
    # =================
    PROTOCOL = 'http'
    SERVER = ''
    VRF = 'default'
    INSTALL_TIMEOUT = 1400
    COMMIT_SLEEP = 180
    TIMEOUT = 60
    # ============
    # Stage Schema
    # ============
    schema = {
        'image': list,
        Optional('protocol'): str,
        Optional('server'): str,
        Optional('vrf'): str,
        Optional('install_timeout'): int,
        Optional('commit_sleep'): int,
    }

    # ==============================
    # Execution order of Stage steps
    # ==============================
    exec_order = [
        'check_in_progress_installs',
        'install_and_replace',
        'check_install_replace_complete',
        'install_commit',
        'check_install_commit_complete'
    ]

    def check_in_progress_installs(self, steps, device, timeout=TIMEOUT):

        with steps.start("Running install commit to clear any in progress "
                         "installs") as step:
            def install_in_progress():
                step.failed("The command 'install commit' aborted. Another Install operation is in progress ")

            install_commit_dialog = Dialog([
                Statement(
                    pattern=r".*Failed to start commit: No install operation is in progress to commit.*",
                    action=None,
                    loop_continue=True,
                    continue_timer=False),
                 Statement(
                    pattern=r".*Failed to start commit: 'Install' detected the 'warning' condition 'Packaging operation in progress.*",
                    action=install_in_progress,
                    loop_continue=True,
                    continue_timer=False),
                ])

            try:
                output = device.execute('install commit',
                            reply=install_commit_dialog,
                            timeout=timeout)
            except Exception as e:
                step.failed("The command 'install commit' failed. Reason: "
                            "{}".format(str(e)))

    def install_and_replace(self, steps, device, image, install_timeout=INSTALL_TIMEOUT,\
                            protocol=PROTOCOL, server=SERVER, vrf=VRF):
        with steps.start("Installing image " + image[0]) as step:

            def install_replace_failure():
                step.failed("The command 'install replace' failed")

            install_replace_dialog = Dialog([
                Statement(
                    pattern=r"^Continue\?\s+\[yes\/no\]\:.*$",
                    action="sendline()",
                    loop_continue=True,
                    continue_timer=False),
                Statement(
                    pattern=r".*Install replace operation(.*)has started.*",
                    loop_continue=True,
                    continue_timer=False),
                 Statement(
                    pattern=r".*Install operation will continue in the background.*",
                    loop_continue=True,
                    continue_timer=False),
                Statement(
                    pattern=r".*Failed to start replace.*",
                    action=install_replace_failure,
                    loop_continue=True,
                    continue_timer=False),
                ],
                )

            try:
                if server:
                    install_replace_command = "install replace {protocol}://{server};{vrf}/{image}".format(protocol=protocol,\
                     server=server, vrf=vrf, image=image[0])
                else:
                    install_replace_command = "install replace {0}".format(image[0])

                device.execute(install_replace_command,
                               reply=install_replace_dialog,
                            )
                # Timeout for install operation
                log.info("Sleeping for {install_timeout} seconds to wait for the install to run in the background"
                         .format(install_timeout=str(install_timeout)))
                time.sleep(install_timeout)
            except Exception as e:
                step.failed("Failed to install the image. Reason: "
                            "{}".format(str(e)))

    def check_install_replace_complete(self, steps, device):
         with steps.start("Checking the install replace status") as step:
            status_failure_pattern = r".*State:\s+Failure.*"
            try:
                output = device.execute('show install request')
                if re.search(status_failure_pattern, output):
                    device.execute("show install log detail")
                    step.failed("The command 'install replace' is aborted ")
            except Exception as e:
                step.failed("The command 'install replace' failed. Reason: "
                               "{}".format(str(e)))

    def install_commit(self, steps, device, commit_sleep=COMMIT_SLEEP):

        with steps.start("Completing install") as step:
            install_commit_dialog = Dialog([
                Statement(
                    pattern=r".*Install commit operation(.*)has started.*",
                    action=None,
                    loop_continue=True,
                    continue_timer=False),
                Statement(
                    pattern=r".*Install operation will continue in the background.*",
                    action=None,
                    loop_continue=True,
                    continue_timer=False)
                ])
            try:
                device.execute('install commit',
                            reply=install_commit_dialog,
                            timeout=commit_sleep)
                log.info("Sleeping for {sleep} seconds to wait for all nodes to come up"
                         .format(sleep=str(commit_sleep)))
                time.sleep(commit_sleep)
            except Exception as e:
                step.failed("The command 'install commit' failed. Install operation is in progress. Reason: "
                            "{}".format(str(e)))

    def check_install_commit_complete(self, steps, device):
         with steps.start("Checking the install commit status") as step:
            status_failure_pattern = r".*State:\s+Failure.*"
            try:
                output = device.execute('show install request')
                if re.search(status_failure_pattern, output):
                    device.execute("show install log detail")
                    step.failed("The command 'install commit' is aborted ")
            except Exception as e:
                step.failed("The command 'install commit' failed. Reason: "
                               "{}".format(str(e)))

