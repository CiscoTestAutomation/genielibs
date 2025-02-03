''' execute functions for wsim'''

# Python
import logging
import re
import time
from genie.utils.timeout import Timeout

# Unicon
from unicon.core.errors import SubCommandFailure

# Logger
log = logging.getLogger(__name__)


def configure_controller_details(device, ctrl_type,ctrl_ip,
                                 ctrl_username,ctrl_password,):
    """Configures the controller details on wsim
            Args:
                device (obj): Device object
                ctrl_type (str): Controller type
                ctrl_ip(str): Controller management IP
                ctrl_username (str): Controller username
                ctrl_password (str): Controller Password
            Returns:
                    None
            Raises:
                    SubCommandFailure
            """

    try:
        device.execute("configure global wlc type {}".format(ctrl_type))
        device.execute("configure global wlc ip {}".format(ctrl_ip))
        device.execute("configure global wlc user {}".format(ctrl_username))
        device.execute("configure global wlc password {}".format(ctrl_password))
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to configure the controller configs on wsim"
            "Error: {e}".format(
                device=device.name,
                e=str(e)
            )
        ) from e

    else:
        log.info("Successfully configured controller configs on wsim {}".format(device.name))


def configure_ap_details(device,ap_name,ap_model,ap_vlan,ap_ip,ap_base_mac,ap_freq):
    try:
        device.execute("configure global setup sit yes")
        device.execute("config global setup ap access yes")
        device.execute("configure global ap model {}".format(ap_model))
        device.execute("configure global ap name {}".format(ap_name))
        device.execute("configure global ap base_mac {}".format(ap_base_mac))
        device.execute("configure global setup ap access vlan {}".format(ap_vlan))
        device.execute("configure global wlc ap-vlan-ip {}".format(ap_ip))
        device.execute("configure global ap freq {}".format(ap_freq))

    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to configure the controller configs on wsim"
            "Error: {e}".format(
                device=device.name,
                e=str(e)
            )
        ) from e

    else:
        log.info("Successfully configured ap configs on wsim {}".format(device.name))

def configure_client_details(device,client_base_mac):
    try:
        device.execute("configure global client base_mac {}".format(client_base_mac))

    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to configure the controller configs on wsim"
            "Error: {e}".format(
                device=device.name,
                e=str(e)
            )
        ) from e

    else:
        log.info("Successfully configured ap configs on wsim {}".format(device.name))


def run_wsim_config(device, timeout=600):
    try:
        device.execute("configure client number total 1 ap 1", timeout=timeout)
        device.execute("run wlc remove certs",timeout=timeout)
        device.execute("run wlc apply certs",timeout=timeout)
        device.execute("run wlc get capwap",timeout=timeout)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to configure the controller configs on wsim"
            "Error: {e}".format(
                device=device.name,
                e=str(e)
            )
        ) from e
    else:
        log.info("Successfully configured certs for controller with wsim {}".format(device.name))

def configure_ap_client_count(device,ap_count,client_count,shell_access=True,timeout=600):
    try:
        if shell_access:
            device.execute("configure client container avahi number total {} ap {}".format(client_count,ap_count),timeout=timeout)

        else:
            device.execute("configure client number total {} ap {}".format(client_count,ap_count),timeout=timeout)

        device.execute("configure hwsim connect mode ALL",timeout=timeout)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to configure the controller configs on wsim"
            "Error: {e}".format(
                device=device.name,
                e=str(e)
            )
        ) from e
    else:
        log.info("Successfully configured ap, client count configs on wsim {}".format(device.name))



def simulate_ap_container(device,ap_count,timeout=600):
    try:
        device.execute("start ap id 1 to {}".format(ap_count),timeout=timeout)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to configure the controller configs on wsim"
            "Error: {e}".format(
                device=device.name,
                e=str(e)
            )
        ) from e
    else:
        log.info("Successfully configured ap, client count configs on wsim {}".format(device.name))


def verify_ap_associate(device,ap_count,max_time=600):
    try:
        check_interval = 30
        timeout = Timeout(max_time, check_interval)
        current_ap_count = 0
        while timeout.iterate():
            try:
                show_data = device.execute("show ap status | grep APs:")
                current_ap_count = re.search(r"\d+\s+APs:.* (\d+)\s+Run", show_data, re.IGNORECASE).group(1)
                log.info("Current ap count on wsim:{}".format(str(current_ap_count)))
                log.info("Expected ap count:{}".format(str(ap_count)))
                if current_ap_count != ap_count:
                    log.info("Waiting for {}s and rechecking the ap status".format(timeout))
                    timeout.sleep()
                    pass
                else:
                    log.info("Successfully all Aps moved to RUN state on wsim {}".format(device.name))
                    break
            except AttributeError:
                log.info("Waiting for {}s and rechecking the ap status".format(timeout))
                timeout.sleep()
                pass
        else:
            raise Exception
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to execute show ap status on wsim"
            "Error: {e}".format(
                device=device.name,
                e=str(e)
            )
        ) from e