""" NXOS ACI Specific Clean Stages """

import logging
import time

from genie.libs.clean.utils import clean_schema
from genie.metaparser.util.schemaengine import Optional
from genie.utils.timeout import Timeout

from pyats import aetest

from unicon.eal.dialogs import Statement, Dialog

log = logging.getLogger(__name__)

@clean_schema({
    Optional("cleaning_timeout"): int,
    Optional("reload_timeout"): int,
    Optional("sleep_after_reload"): int,
    Optional("copy_boot_image"): {
        'origin': {
            Optional('files'): list,
            'hostname': str
        },
        'destination': {
            'directory': str,
        },
        'protocol': str,
        Optional('timeout'): int,
    }
})
@aetest.test
def fabric_clean(section, steps, device, cleaning_timeout=90, reload_timeout=800,
                 sleep_after_reload=60, copy_boot_image=None):
    """ This stage will clean NXOS ACI nodes.

    The stage will execute the following commands, where <boot_image>
    is the currently running image if it exists, or the image copied to the
    device (if applicable)::
        - '/bin/setup-clean-config.sh'
        - '/bin/setup-bootvars.sh <boot_image>'

    Finally the stage will reload the node.

    Stage Schema
    ------------
    fabric_clean:

        cleaning_timeout (int, optional): Max time for cleaning scripts to execute.
            Defaults to 90.

        reload_timeout (int, optional): Max time for reload. Defaults to 800.

        sleep_after_reload (int, optional): Time in seconds to sleep after the
            device completes reloading. Defaults to 60.

        copy_boot_image (dict, optional):

            origin:

                files (list): Image files location on the server.

                hostname (str): Hostname or address of the server to copy from.
                    This must exist in the testbed under the 'servers' block.

            destination:

                directory (str): Location on the device where the images
                    should be copied to.

            protocol (str): Protocol used for copy operation.

            timeout (int, optional): Max time allowed for copy operation in
                seconds. Defaults to 300.

    Example
    -------
    fabric_clean:
        cleaning_timeout: 90
        copy_boot_image:
            origin:
                files: [/my_switch_image.bin]
                hostname: my_server_from_testbed
            destination:
                directory: '/bootflash'
            protocol: scp
    """
    if copy_boot_image:
        copy_boot_image.setdefault('timeout', 300)

    with steps.start("Cleaning the device") as step:
        if copy_boot_image:
            result = device.api.execute_clean_node_fabric(
                hostname=copy_boot_image['origin']['hostname'],
                copy_protocol=copy_boot_image['protocol'],
                image=copy_boot_image['origin']['files'][0],
                destination_dir=copy_boot_image['destination']['directory'],
                copy_max_time=copy_boot_image['timeout'],
                max_time=cleaning_timeout)
        else:
            result = device.api.execute_clean_node_fabric(
                max_time=cleaning_timeout)

        if not result:
            step.failed("Failed to clean the device")
        else:
            step.passed("Successfully cleaned the device")

    with steps.start("Reloading '{dev}'".format(dev=device.name)):

        reload_dialog = Dialog([
            Statement(
                pattern=r".*This command will reload the chassis\, Proceed \(y\/n\)\? \[n\]\:.*",
                action='sendline(y)'
            ),
        ])

        device.sendline('reload')
        reload_dialog.process(device.spawn)

    with steps.start("Waiting for {dev} to reload".format(dev=device.hostname)) as step:
        timeout = Timeout(reload_timeout, 60)
        while timeout.iterate():
            timeout.sleep()
            device.destroy()

            try:
                device.connect(learn_hostname=True)
            except Exception:
                log.info("{dev} is not reloaded".format(dev=device.hostname))
            else:
                step.passed("{dev} has successfully reloaded".format(dev=device.hostname))

        step.failed("{dev} failed to reboot".format(dev=device.hostname))

    log.info("Sleeping for '{}' seconds for '{}' to stabilize."
             .format(sleep_after_reload, device.name))

    time.sleep(sleep_after_reload)
