import logging

log = logging.getLogger(__name__)

def verify_rollback_label(device, rollback_id, rollback_label):
    """
    Verifies rollback label for rollback id
    Args:
        device ('obj'): Device object
        rollback_id ('int'): rollback id for which label has to be verified
        rollback_label ('str'): rollback label
    Returns:
        True if rollback label matches
        False if rollback label not matches
    Raises:
        error
    """
    try:
        output = device.parse("show install rollback id {id}".format(id=rollback_id))
    except Exception as e:
        log.error(f"Error occured while verifying rollback label: {e}")

    return output['id'][int(rollback_id)]['label'] == rollback_label


def verify_install_state(device, install_type='IMG', install_state='C'):
    """
    Verifies install state
    Args:
        device ('obj'): Device object
        install_type ('str, optional'): install type to verify
        install_state ('str, optional'): install state to verify
    Returns:
        True if rollback label matches
        False if rollback label not matches
    """
    output = device.parse("show install summary")
    location = list(output.get('location').keys())[0]

    for p in output.get('location').get(location).get('pkg_state'):
        file_state = output['location'][location]['pkg_state'][p]['state']
        file_type = output['location'][location]['pkg_state'][p]['type']

        if file_state == install_state and file_type == install_type:
            return True
    return False


def verify_install_auto_abort_timer_state(device, timer_state='inactive'):
    """
    Verifies install auto abort timer state
    Args:
        device ('obj'): Device object
        timer_state ('str, optional'): install type to verify
    Returns:
        True if install auto abort timer state matches
        False if install auto abort timer state not matches
    """
    output = device.parse("show install summary")
    location = list(output.get('location').keys())[0]
    get_timer_state = output.get('location').get(location).get('auto_abort_timer')

    return get_timer_state == timer_state


def verify_active_standby(device):
    """
    Verify active and standby dut
    Args:
        device ('obj'): Device object
    Returns:
        True if device is active
        False if device is standby
    Raises:
        Raises exception
    """
    try:
        output = device.parse('show redundancy states')
    except Exception as e:
        log.error("Failed to parse : {e}".format(e=e))
    
    return output['my_state'] == "ACTIVE"


def verify_rollback_description(device, rollback_id, rollback_description):
    """
    Verifies rollback label for rollback id
    Args:
        device ('obj'): Device object
        rollback_id ('int'): rollback id for which label has to be verified
        rollback_description ('str'): rollback label
    Returns:
        True if rollback label matches
        False if rollback label not matches
    Raises:
        error
    """
    try:
        output = device.parse("show install rollback id {id}".format(id=rollback_id))
    except Exception as e:
        log.error(f"Error occured while verifying rollback label: {e}")

    return output['id'][int(rollback_id)]['description'] == rollback_description
