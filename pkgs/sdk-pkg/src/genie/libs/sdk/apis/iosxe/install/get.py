# Python
import logging

log = logging.getLogger(__name__)


def get_install_version(device, install_type='IMG', install_state=None):
    """
    returns version of img/smu
    Args:
        device ('obj'): Device object
        install_type ('str, optional'): install type
        install_state ('str, optional'): install state
    Returns:
        Install version if match criteria is satisfied
        False if Install version if match criteria is not satisfied
    Raises:
        SubCommandFailure
    """
    output = device.parse("show install summary")
    location = list(output.get('location').keys())[0]

    for pkg in output.get('location').get(location).get('pkg_state'):
        file_state = output['location'][location]['pkg_state'][pkg]['state']
        file_type = output['location'][location]['pkg_state'][pkg]['type']

        if install_state :
            if file_state == install_state and file_type == install_type:
                return output['location'][location]['pkg_state'][pkg]['filename_version']
        else:
            if file_type == install_type:
                return output['location'][location]['pkg_state'][pkg]['filename_version']

    return False
