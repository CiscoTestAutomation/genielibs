# Python
import logging
import time
from os.path import basename

# Genie
from genie.harness.utils import connect_device
from genie.metaparser.util.exceptions import SchemaEmptyParserError

# pyATS
from pyats.utils.fileutils import FileUtils
from pyats.aetest.steps import Steps

# Unicon
from unicon.core.errors import SubCommandFailure
from unicon.core.errors import ConnectionError

# ISSU
from genie.libs.sdk.apis.iosxe.issu.verify import (
    is_issu_in_state,
    is_issu_terminal_state_reached_on_slot,
    is_issu_rollback_timer_in_state,
)

# PLATFORM
from genie.libs.sdk.apis.iosxe.platform.get import get_platform_standby_rp
from genie.libs.sdk.apis.iosxe.platform.verify import is_platform_slot_in_state

# UTILS
from genie.libs.sdk.apis.utils import reconnect_device

log = logging.getLogger(__name__)


def prepare_issu(device, image, path, address, overwrite=False,
                 protocol="tftp", disks=None, timeout_seconds=600):
    """ Prepare image and check device before starting issu process
        Args:
            device ('obj'): Device object
            image ('str'): Image name
            path ('str'): Path on dsetr
            overwrite ('bool'): Flag to overwrite existing file
            protocol ('str'): Protocol to be used on copying image to device
            address ('str'): Address of server from where image will be copied.
            disks ('list'): List of disks where image will be copied
            timeout_seconds ('int'): Maximum duration to wait for file copy
        Raises:
            Exception: Failed preparing ISSU image
        Returns:
            None
    """
    if disks is None:
        disks = ["bootflash:", "stby-bootflash:"]

    for disk in disks:
        try:
            copy_issu_image_to_disk(
                device=device,
                disk=disk,
                path=path,
                protocol=protocol,
                address=address,
                image=image,
                timeout_seconds=timeout_seconds,
                overwrite=overwrite,
            )
        except Exception as e:
            raise Exception(e)


def copy_issu_image_to_disk(device, disk, path, address, image,
                            protocol="tftp", timeout_seconds=600, 
                            wait_time_after_copy=0, overwrite=False):
    """ Copy image from a server to disk
        Args:
            device ('obj'): Device object
            disk ('str'): Disk name
            address ('str'): Server address
            path ('str'): Path on server
            protocol ('str'): Transfer protocol
            image ('str'): Image name
            timeout_seconds ('int'): Maximum duration to wait for file copy
            wait_time_after_copy ('int'): Wait time after file copy
            overwrite ('bool'): Flag to overwrite existing file
        Raises:
            Exception: Failed copying ISSU image to disk
        Returns:
            None
    """

    from_url = "{protocol}://{address}/{path}/{image}".format(
        protocol=protocol, address=address, path=path, image=image
    )

    filetransfer = FileUtils.from_device(device)

    filetransfer.copyfile(
        source=from_url, destination=disk, device=device,
        timeout_seconds=timeout_seconds, overwrite=overwrite
    )

    time.sleep(wait_time_after_copy)

    output = device.execute(
        "dir {disk}{image}".format(disk=disk, image=basename(image))
    )
    if "Error" not in output:
        log.info("Copied ISSU image to '{disk}'".format(disk=disk))
    else:
        raise Exception(
            "Unable to copy ISSU image to '{disk}'".format(disk=disk)
        )


def perform_issu(device, image, disk, timeout=1200, reconnect_via=None, steps=Steps()):
    """ Execute ISSU on device
        Args:
            device ('obj'): Device object
            image ('str'): Image name on disk
            disk ('str'): Disk where is located image
            timeout ('int'): Timeout in second for each section
        Raise:
            None
        Returns:
            None
    """

    with steps.start("Command 'issu loadversion'") as step:

        slot_number = get_platform_standby_rp(device=device)

        if not slot_number:
            raise ValueError("Could not retrieve standby rp slot number")

        # Load version
        standby_slot = "R{}".format(slot_number)
        try:
            issu_loadversion(
                device=device, standby_slot=slot_number,
                disk=disk, image=image, timeout=timeout
            )
        except Exception:
            step.failed("Unable to execute 'issu loadversion'")

    with steps.start("Command 'issu runversion'") as step:

        if not is_platform_slot_in_state(
            device=device, slot=standby_slot, state="ok, standby"
        ):
            step.failed(
                "Slot {slot} is not in 'ok, standby' state".format(
                    slot=standby_slot
                )
            )

        if not is_issu_terminal_state_reached_on_slot(
            device=device, slot=standby_slot
        ):
            step.failed(
                "Slot {slot} has not reached terminal state".format(
                    slot=standby_slot
                )
            )

        # Run version
        try:
            issu_runversion(device=device, timeout=timeout, reconnect_via=reconnect_via)
        except (Exception, ConnectionError) as e:
            step.failed(e)

    with steps.start("Command 'issu acceptversion'") as step:

        in_state = is_issu_in_state(
            device=device, slot=standby_slot, expected_state="runversion"
        )

        if not in_state:
            step.failed("Issu is not in state 'runversion'")

        # Accept version
        try:
            issu_acceptversion(device=device, timeout=timeout)
        except Exception as e:
            step.failed(e)

    with steps.start(
        "Save running-configuration to startup-configuration"
    ) as step:

        filetransfer = FileUtils.from_device(device)
        filetransfer.copyconfiguration(
            source="running-config",
            destination="startup-config",
            device=device,
        )

    with steps.start("Command 'issu commitversion'") as step:

        in_state = is_issu_in_state(
            device=device, slot=standby_slot, expected_state="acceptversion"
        )

        if not in_state:
            step.failed("Issu is not in state 'acceptversion'")

        in_state = is_issu_rollback_timer_in_state(
            device=device, slot=standby_slot, expected_state="inactive"
        )

        if not in_state:
            step.failed("Issu rollback timer is not 'inactive'")

        # Commit version
        try:
            issu_commitversion(device=device, timeout=timeout)
        except Exception as e:
            step.failed(e)

    with steps.start("Reload standby slot") as step:

        slot_number = get_platform_standby_rp(device=device)

        if not slot_number:
            raise ValueError("Could not retrieve standby rp slot number")

        standby_slot = "R{}".format(slot_number)
        try:
            reload_issu_slot(device=device, slot=standby_slot, timeout=timeout)
        except Exception as e:
            step.failed(e)


def issu_loadversion(device, standby_slot, disk, image, timeout=1200):
    """ Execute issu loadversion command on device
        Args:
            device ('obj'): Device object
            standby_slot ('int'): Standby slot number
            disk ('str'): Disk name
            image ('str'): Image name
            timeout ('int'): Time out in seconds
        Raise:
            Exception: Failed to load version on device
        Returns:
            None
    """
    log.info("Loading version on slot {slot}".format(slot=standby_slot))

    try:
        output = device.execute(
            "issu loadversion rp {srp} file {disk}{image}".format(
                srp=standby_slot, disk=disk, image=image
            ),
            timeout=timeout,
        )
    except Exception as e:
        raise Exception("Unable to execute 'issu loadversion'")

    if "FAILED" in output:
        device.execute("issu abortversion", timeout=timeout)
        raise Exception("Unable to execute 'issu loadversion'")


def issu_runversion(device, timeout=300, reconnect_via=None):
    """ Execute issu runversion on device
        Args:
            device ('obj'): Device object
            timeout ('int'): Timeout in seconds
        Raise:
            Exception Failed to reconnect to device
        Returns:
            None
    """
    log.info("Running version")
    try:
        output = device.execute("issu runversion", timeout=timeout)
    except SubCommandFailure:
        # Timeout Unicon SubCommandFailure expected
        # Wait a bit as the device is booting with the ISSU upgrade image
        pass

    log.info("Reconnecting device")
    try:
        reconnect_device(device=device, max_time=timeout, via=reconnect_via)
    except Exception as e:
        log.error("Failed to reconnect to device {dev}")
        raise ConnectionError(
            "Failed to connect to device {dev}".format(dev=device.name)
        )


def issu_acceptversion(device, timeout=300):
    """ Execute issu acceptversion on device
        Args:
            device ('obj'): Device object
            timeout ('int'): Timeout in seconds
        Raise:
            Exception: Failed executing 'issu acceptversion' command
        Returns:
            None
    """

    try:
        output = device.execute("issu acceptversion", timeout=timeout)
    except Exception as e:
        raise Exception("Unable to execute 'issu acceptversion'")

    if "FAILED" in output:
        log.error(
            "Failed executing command 'issu acceptversion'" "Aborting ISSU"
        )
        device.execute("issu abortversion", timeout=timeout)
        raise Exception("Unable to execute 'issu acceptversion'")


def issu_commitversion(device, timeout=1200):
    """ Execute issu commitversion on device
        Args:
            device ('obj'): Device object
            timeout ('int'): Timeout in seconds
        Raise:
            Exception: Failed executing 'issu commitversion' command
        Returns:
            None
    """
    log.info("Commiting version")
    try:
        output = device.execute("issu commitversion", timeout=timeout)
    except Exception as e:
        log.error(
            "Failed executing command 'issu acceptversion'" "Aborting ISSU"
        )
        device.execute("issu abortversion", timeout=timeout)
        raise Exception("Unable to execute 'issu commitversion'")

    if "FAILED" in output:
        log.error(
            "Failed executing command 'issu acceptversion'" "Aborting ISSU"
        )
        device.execute("issu abortversion", timeout=timeout)
        raise Exception("Unable to execute 'issu commitversion'")


def reload_issu_slot(device, slot, wait_time=60, timeout=1200):
    """ Reload slot on device
        Args:
            device ('obj'): Device object
            slot ('str'):  Slot to be reloaded
            wait_time ('int'): Time to wait in seconds after slot reload
        Raise:
            Exception
    """
    log.info("Reloading slot {slot}".format(slot=slot))
    try:
        output = device.execute(
            "hw-module slot {slot} reload".format(slot=slot), timeout=timeout
        )
    except Exception as e:
        raise Exception(
            "Unable to reload slot {slot} on device {dev}".format(
                slot=slot, dev=device.name
            )
        )

    log.info("Sleeping for {sec} seconds".format(sec=wait_time))
    time.sleep(wait_time)


def downgrade_issu_image_on_router(
    device, upgraded_image, downgrade_image, disk="bootflash:", timeout=500
):
    """ Execute software downgrade on router
        Args:
            device ('obj'): Device object
            upgraded_image ('str'): Name of current installed image
            downgrade_image ('str'): Name of image to be used in downgrade
            disk ('str'): Disk name            
            timeout ('int'): Timeout in seconds
        Raise:
            SubCommandFailure: Failed downgrading image on device
            ConnectionError: Failed reconnecting to device
        Returns:
            None

    """

    commands = (
        "no boot system {disk}{upgraded_image}\n"
        "boot system {disk}{downgrade_image}".format(
            downgrade_image=downgrade_image,
            disk=disk,
            upgraded_image=upgraded_image,
        )
    )

    slot_number = get_platform_standby_rp(device=device)

    if not slot_number:
        raise ValueError("Could not retrieve standby rp slot number")

    standby_slot = "R{}".format(slot_number)

    if not is_platform_slot_in_state(
        device=device, slot=standby_slot, state="ok, standby"
    ):
        raise ValueError(
            "Slot {slot} is not in 'ok, standby' state".format(
                slot=standby_slot
            )
        )

    log.info("Applying configuration to device {dev}".format(dev=device.name))
    try:
        device.configure(commands)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not apply the following configuratin on "
            "device {dev}:\n{config}".format(dev=device.name, config=commands)
        )

    log.info("Saving changes on device {dev}".format(dev=device.name))
    try:
        device.execute("write memory", timeout=timeout)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not execute command 'write memory' on "
            "device {dev}".format(dev=device.name)
        )

    log.info("Reloading device {dev}".format(dev=device.name))
    try:
        device.reload(timeout=timeout)
    except SubCommandFailure as e:
        # Timeout Unicon SubCommandFailure expected
        pass

    log.info(
        "Waiting {sec} seconds before reconnecting to device".format(
            sec=timeout
        )
    )

    time.sleep(timeout)

    log.info("Reconnecting device")
    try:
        reconnect_device(device=device, max_time=timeout)
    except Exception as e:
        raise ConnectionError(
            "Failed to connect to device {dev}".format(dev=device.name)
        )
