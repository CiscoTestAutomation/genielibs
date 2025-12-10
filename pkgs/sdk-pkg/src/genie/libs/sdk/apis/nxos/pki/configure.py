from unicon.eal.dialogs import Statement, Dialog
import logging 

logger = logging.getLogger(__name__)

# Unicon
from unicon.core.errors import SubCommandFailure

# Genie
from genie.metaparser.util.exceptions import SchemaEmptyParserError

def configure_trustpoint(device, tp_name, **kwargs):
    """ Configure a trustpoint on the device

        Args:
            device (obj): Device object
            tp_name (str): Name of the trustpoint to configure

        Returns:
            None
    """
    commands = [
        f"crypto ca trustpoint {tp_name}",
        "enrollment terminal"
    ]

    try:
        device.configure(commands)
    except SubCommandFailure as e:
        logger.error(f"Failed to configure trustpoint {tp_name}: {e}")
        raise

def unconfigure_trustpoint(device, tp_name):
    """ Unconfigure a trustpoint on the device

        Args:
            device (obj): Device object
            tp_name (str): Name of the trustpoint to unconfigure

        Returns:
            None
    """
    command = f"no crypto ca trustpoint {tp_name}"

    try:
        device.configure(command)
    except SubCommandFailure as e:
        logger.error(f"Failed to unconfigure trustpoint {tp_name}: {e}")
        raise

def configure_pki_authenticate_certificate(device, certificate, tp_name):
    """ Configure PKI authenticate certificate on the device

        Args:
            device (obj): Device object
            certificate (str): PEM formatted certificate string
            tp_name (str): Name of the trustpoint to associate with the certificate

        Returns:
            None
    """
    def cert_key_handler(spawn, data):
        spawn.sendline(data)
        spawn.sendline('END OF INPUT')

    dialog = Dialog(
            [
                Statement(
                    r"^.*Are you sure you want to do this\? \[yes/no\]\s?.*$",
                    action="sendline(yes)",
                    loop_continue=True,
                ),
                Statement(
                    r'^.*end the input with a line containing only END OF INPUT :.*',
                    action=cert_key_handler,
                    args={"data": certificate},
                    loop_continue=True,
                    continue_timer=False
                ),
                Statement(
                    r".*Do you accept this certificate\? \[yes/no\]:.*", 
                    action="sendline(yes)", loop_continue=True
                ),
            ]
        )
    
    try:
       device.configure("crypto ca authenticate {tp_name}"
                        .format(tp_name=tp_name), reply=dialog, timeout=200)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not Paste certificate on device "
            "Error: {error}".format(error=e)
            )