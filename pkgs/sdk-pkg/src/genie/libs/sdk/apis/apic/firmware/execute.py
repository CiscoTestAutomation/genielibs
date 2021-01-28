""" Execute type APIs for APIC """

import time
import logging

from genie.utils.timeout import Timeout

log = logging.getLogger(__name__)

def execute_clear_firmware_repository(device, sleep_after_delete=5):
    """ Clears the firmware repository.

    Args:
        device (obj): Device to execute on

        sleep_after_delete (int, optional): Time in seconds to sleep
            after clearing the firmware repository. Defaults to 5.

    Returns:
        True if firmware repository is emptied
        False if firmware repository cannot be emptied

    Raises:
        N/A

    """

    images = device.api.get_firmware_repository_images()
    if not images:
        return True

    for image in images:
        device.execute('firmware repository delete {}'.format(image))

    log.info('Sleeping for {} seconds to ensure the repository updates'
             .format(sleep_after_delete))
    time.sleep(sleep_after_delete)

    if device.api.get_firmware_repository_images():
        return False
    else:
        return True

def execute_install_controller_group_firmware(
        device,
        controller_image,
        error_patterns=None,
        controller_upgrade_max_time=1800,
        controller_upgrade_check_interval=60,
        controller_reconnect_max_time=900,
        controller_reconnect_check_interval=60,
        controller_upgrade_after_reconnect_max_time=300,
        controller_upgrade_after_reconnect_check_interval=60
):
    """ Installs the controller image onto the controller(s) and verifies install
    completed.

    Args:
        device (obj): Device to execute on

        controller_image (str): Image to install. This must exist in the
            firmware repository.

        error_patterns (list, optional): Any extra error patterns for executing
            'firmware upgrade controller-group'. Defaults to None.

        controller_upgrade_max_time (int, optional): Max time in seconds allowed
            for verifying controller upgrade. Defaults to 1800.

        controller_upgrade_check_interval (int, optional): How often in seconds
            to check upgrade status. Defaults to 60.

        controller_reconnect_max_time (int optional): Max time in seconds allowed
            for reconnecting to controller if the connection is lost. Defaults
            to 900.

        controller_reconnect_check_interval (int, optional): How often in
            seconds to attempt reconnect. Defaults to 60.

        controller_upgrade_after_reconnect_max_time (int, optional): Max time
            in seconds allowed for verifying controller upgrade after reconnect.
            Defaults to 300.

        controller_upgrade_after_reconnect_check_interval (int, optional): How
            often in seconds to check upgrade status after reconnect. Defaults
            to 60.

    Returns:
        True if install succeeds
        False if install failed

    Raises:
        N/A
    """
    errors = [r".*Command execution failed.*"]
    if error_patterns:
        errors.extend(error_patterns)

    device.configure(['firmware',
                      'controller-group',
                      'firmware-version {}'.format(controller_image)])

    try:
        device.execute('firmware upgrade controller-group',
                       error_pattern=errors)
    except Exception as e:
        log.error("Firmware upgrade command failed: {}".format(str(e)))
        return False

    try:
        result = device.api.verify_firmware_upgrade_status(
            status='success',
            firmware_group='controller-group',
            max_time=controller_upgrade_max_time,
            check_interval=controller_upgrade_check_interval)
    except Exception as e:
        # An exception is expected to be raised when upgrading a
        # controller-group with only one controller as the device
        # will drop the connection during the upgrade process
        log.info("Reattempting connection in-case there was only "
                 "one controller. Error message: {}".format(str(e)))

        # Attempt device reconnection
        timeout = Timeout(controller_reconnect_max_time,
                          controller_reconnect_check_interval)

        while timeout.iterate():
            timeout.sleep()
            device.destroy()
            try:
                device.connect(learn_hostname=True)
            except Exception:
                log.info("Cannot connect to {dev}".format(
                    dev=device.hostname))
            else:
                break

        # If not connected after timeout, fail
        if not device.connected:
            return False

        # Reconnected, so check firmware upgrade status
        result = device.api.verify_firmware_upgrade_status(
            status='success',
            firmware_group='controller-group',
            max_time=controller_upgrade_after_reconnect_max_time,
            check_interval=controller_upgrade_after_reconnect_check_interval)

    return result

def execute_install_switch_group_firmware(
        device,
        switch_image,
        switch_node_ids,
        switch_group_name='switches',
        clear_switch_group=True,
        error_patterns=None,
        switch_upgrade_max_time=2700,
        switch_upgrade_check_interval=60,
        stabilize_switch_group_config_sleep=120,
        controller_reconnect_max_time=900,
        controller_reconnect_check_interval=60,
):
    """ Installs the switch image on the switch(s) and then verifies the install
    completed.

    Args:
        device (obj): Device to execute on

        switch_image (str): Image to install. This must exist in the
            firmware repository.

        switch_node_ids (str): String of node IDs to install the image on. The
            node IDs must be separated by a comma.

        switch_group_name (str, optional): Name for the switch-group that will
            be configured. Defaults to switches.

        clear_switch_group (bool, optional): Whether or not to clear the
            switch-group configuration before applying new configuration.
            Defaults to True.

        error_patterns (list, optional): Any extra error patterns for executing
            'firmware upgrade switch-group {name}'. Defaults to None.

        switch_upgrade_max_time (int, optional): Max time in seconds allowed for
            verifying upgrade status. Defaults to 2700.

        switch_upgrade_check_interval (int, optional): How often in seconds to
            check upgrade status. Defaults to 60.

        stabilize_switch_group_config_sleep (int, optional): How long in seconds
            to sleep after configuring switch-group. Defaults to 120.

        controller_reconnect_max_time (int optional): Max time in seconds allowed
            for reconnecting to controller if the connection is lost. Defaults
            to 900.

        controller_reconnect_check_interval (int, optional): How often in
            seconds to attempt reconnect. Defaults to 60.

    Returns:
        True if install succeeds
        False if install failed

    Raises:
        N/A

    """

    errors = [r".*Command execution failed.*"]
    if error_patterns:
        errors.extend(error_patterns)

    if clear_switch_group:
        log.info("Clearing switch-group configuration because the "
                 "argument 'clear_switch_group' is True")

        device.configure(['firmware',
                          'no switch-group {}'.format(switch_group_name)])

    device.configure(['firmware',
                      'switch-group {}'.format(switch_group_name),
                      'switch {}'.format(switch_node_ids),
                      'firmware-version {}'.format(switch_image)])

    log.info("Sleeping for '{}' seconds to allow the newly configured switch-group "
             "to stabilize".format(stabilize_switch_group_config_sleep))
    time.sleep(stabilize_switch_group_config_sleep)

    try:
        device.execute(
            'firmware upgrade switch-group {}'.format(switch_group_name),
            error_pattern=error_patterns
        )
    except Exception as e:
        log.error("Firmware upgrade command failed: {}".format(str(e)))
        return False

    try:
        result = device.api.verify_firmware_upgrade_status(
            status='success',
            firmware_group='switch-group {}'.format(switch_group_name),
            max_time=switch_upgrade_max_time,
            check_interval=switch_upgrade_check_interval)
    except Exception as e:
        # An exception can be raised if the controller does not respond to
        # the 'show firmware upgrade status' command. Disconnect and reconnect
        # to ensure the controller is ready for commands to be issued.
        log.info("Reattempting connection as the device '{dev}' returned "
                 "nothing after executing a command.\nError: {e}".
                 format(dev=device.hostname, e=str(e)))

        # Attempt device reconnection
        timeout = Timeout(controller_reconnect_max_time,
                          controller_reconnect_check_interval)

        while timeout.iterate():
            timeout.sleep()
            device.destroy()
            try:
                device.connect(learn_hostname=True)
            except Exception:
                log.info("Cannot connect to {dev}".format(
                    dev=device.hostname))
            else:
                break

        # If not connected after timeout, fail
        if not device.connected:
            return False

        # Reconnected, so check firmware upgrade status
        result = device.api.verify_firmware_upgrade_status(
            status='success',
            firmware_group='switch-group {}'.format(switch_group_name),
            max_time=switch_upgrade_max_time,
            check_interval=switch_upgrade_check_interval)

    return result