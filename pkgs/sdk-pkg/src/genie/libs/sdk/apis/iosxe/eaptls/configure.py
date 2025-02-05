# Python
import logging
import time
import re
from genie.utils.timeout import Timeout

# Unicon
from unicon.eal.dialogs import Statement, Dialog
from unicon.core.errors import SubCommandFailure

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def configure_pki_export_pem(device):
    """ Generates certificate on device

        Args:
            device (`obj`): Device object

        Returns:
            Certificate or None

        Raise:
            SubCommandFailure: Failed to generate certificate on device
    """

    try:
        output = device.configure(["crypto pki export cisco pem terminal"])

    except SubCommandFailure:
        raise SubCommandFailure(
            "Could not generate certificate on device"
        )

    return output


def configure_pki_authenticate_certificate(device, certificate, label_name):
    """ Pastes certificate on device

        Args:
            device (`obj`): Device object
            certificate ('str'): Certificate to be pasted
            label_name ('str'): Label name

        Returns:
            None

        Raise:
            SubCommandFailure: Failed to paste certificate on device
    """
    def cert_key_handler(spawn, data):
        spawn.sendline(data)
        spawn.sendline('quit')
    
    dialog = Dialog(
                [
                    Statement(
                        r"^.*Are you sure you want to do this\? \[yes/no\]\s?.*$",
                        action="sendline(yes)",
                        loop_continue=True,
                    ),
                    Statement(
                        r'^.*End with a blank line or the word "quit" on a line by itself\s?.*',
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
       device.configure("crypto pki authenticate {label_name}"
                        .format(label_name=label_name), reply=dialog, timeout=200)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not Paste certificate on device "
            "Error: {error}".format(error=e)
            )

def configure_pki_enroll_certificate(device, label_name):
    """ Enrolls certificate on device and returns the certificate

        Args:
            device (`obj`): Device object
            label_name ('str'): Label name

        Returns:
            Enrolled certificate

        Raise:
            SubCommandFailure: Failed to enroll certificate on device and return it
    """

    dialog = Dialog(
                [
                    Statement(
                        r"^.*Include the router serial number in the subject name\? \[yes/no\]:.*",
                        action="sendline(yes)",
                        loop_continue=True,
                    ),
                    Statement(
                        r'^.*Include an IP address in the subject name\? \[no\]:.*',
                        action="sendline(no)",
                        loop_continue=True,
                        continue_timer=False
                    ),
                    Statement(
                        r".*Display Certificate Request to terminal\? \[yes/no\]:.*", 
                        action="sendline(yes)", loop_continue=True
                    ),
                   Statement(
                        r".*Redisplay enrollment request\? \[yes/no\]:.*", 
                        action="sendline(no)", loop_continue=True
                    )

                ]
            )

    try:
       output = device.configure("crypto pki enroll {label_name}".
                        format(label_name=label_name), reply=dialog, timeout=200)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not Enroll certificate on device and return it"
            "Error: {error}".format(error=e)
            )

    return output

def unconfigure_crypto_pki_server(device, server_name):
    """ Unconfigures crypto pki server on device

        Args:
            device (`obj`): Device object
            server_name ('str'): Name of the server

        Returns:
            None

        Raise:
            SubCommandFailure: Failed to unconfigure crypto pki server on device
    """

    try:
        device.configure([f"no crypto pki server {server_name}"])

    except SubCommandFailure:
        raise SubCommandFailure(
            "Could not unconfigure crypto pki server on device"
        )


def configure_crypto_pki_server(
    device,
    domain_name=None,
    database_level=None,
    issuer_name=None,
    hash=None,
    modulus_size=None,
    password=None,
    server_name=None,
    **kwargs
):
    """Configures crypto pki server on device

    Args:
        device (`obj`): Device object
        domain_name ('str'): Name of the domain to be configured
        database_level ('str'): Database level to be configured
        issuer_name ('str'): Issuer name to be configured
        hash ('str'): Hash to be configured
        modulus_size ('str'): Modulus size to be configured
        Password ('str'): Password to be configured
        server_name ('str'): Name of the server to be configured

    Returns:
        None

    Raise:
        SubCommandFailure: Failed to configure crypto pki server on device
    """

    if kwargs:
        from genie.libs.sdk.apis.iosxe.pki.configure import configure_crypto_pki_server as pki_configure_crypto_pki_server
        return pki_configure_crypto_pki_server(device=device, server_name=server_name, database_level=database_level, issuer_name=issuer_name, password=password, **kwargs)

    def send_password(spawn, password):
        spawn.sendline(password)
    
    dialog_1=Dialog(
                [
                    Statement(
                        r"^.*Destination filename \[nvram\.pub\]\?.*$",
                        action="sendline(\r)",
                        loop_continue=True,
                    ),
                    Statement(
                        r"^.*Do you really want to overwrite it\? \[yes/no\]:.*$",
                        action="sendline(yes)",
                        loop_continue=True,
                    ),
                    Statement(
                        r"^.*Destination filename \[nvram\.prv\]\?.*$",
                        action="sendline(\r)",
                        loop_continue=True,
                    ),
                    Statement(
                        r"^.*Do you really want to overwrite it\? \[yes/no\]:.*$",
                        action="sendline(yes)",
                        loop_continue=True,
                    ),
                ]
            )
    try:
        device.configure(
            [
                f"ip domain-name {domain_name}",
                f"crypto pki server {server_name}",
                f"database level {database_level}",
                f"issuer-name {issuer_name}",
                f"hash {hash}",
                "shut",
                "exit",
            ]
        )
        
        time.sleep(10)
        
        device.configure(
            [
                f"crypto key generate  rsa modulus {modulus_size} label  cisco exportable",
                f"crypto key export rsa cisco pem url nvram 3des {password}",
            ],
            timeout=5,reply=dialog_1
        )
        
        time.sleep(20)
        
        dialog_2=Dialog(
                [
                    Statement(
                        r"Password:\s?$",
                        action=send_password,
                        args={"password": password},
                        loop_continue=True,
                    ),
                    Statement(
                        r"Re-enter password:\s?$",
                        action=send_password,
                        args={"password": password},
                        loop_continue=True,
                    ),
                ]
            )
        
        device.configure(
            [
                f"crypto pki server {server_name}",
                "no shut",
            ],
            timeout=120, reply=dialog_2
        )

        time.sleep(120)
        
    except SubCommandFailure:
        raise SubCommandFailure("Could not configure crypto pki server on device")


def unconfigure_trustpoint_switch(device, label_name):
    """ Unconfigures Trustpoint related config on device
        Args:
            device ('obj'): device to use
            label_name ('str'): Label name

        Returns:
            None

        Raises:
            SubCommandFailure
    """
    logger.debug("Unconfigure Trustpoint on device")

    dialog = Dialog([
    Statement(pattern=r'.*\% Removing an enrolled trustpoint will destroy all certificates\n'
    r'received from the related Certificate Authority\.\n'

    r'Are you sure you want to do this\? \[yes\/no\]\:',
                        action='sendline(y)',
                        loop_continue=True,
                        continue_timer=False)
    ])

    try:
       device.configure("no crypto pki trustpoint {label_name}".format(label_name=label_name), reply=dialog)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not unconfigure Trustpoint related config from device "
            "Error: {error}".format(error=e)
            )

def unconfigure_crypto_key(device, label_name):
    """ Unconfigures Crypto Key on device
        Args:
            device ('obj'): device to use
            label_name ('str'): Label name
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    dialog = Dialog([
    Statement(pattern=r'.*Do you really want to remove these keys\? \[yes\/no\]\:.*',
                        action='sendline(y)',
                        loop_continue=False,
                        continue_timer=False)
    ])
    try:
        device.configure(f"crypto key zeroize rsa {label_name}", reply=dialog, timeout=200)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Could not unconfigure Crypto Key from device. Error:\n{e}")

def crypto_pki_server_request(device, server_name, retrive_method, certificate_format, certificate):
    """ Gets grant ID from device
        Args:
            device (`obj`): Device object
            server_name ('str'): Name of the server
            retrive_method ('str'): Certificate Retrieve method
            certificate_format ('str'): Format in which certificate needs to be retrieved
            certificate ('str'): Certificate to be pasted

        Returns:
            Grant ID full output or None

        Raise:
            SubCommandFailure: Failed to get Grant ID full output from device
    """

    def cert_key_handler(spawn, data):
        spawn.sendline(data)
        spawn.sendline('')

    dialog = Dialog(
                [
                    Statement(
                        r'^.*% End with a blank line or "quit" on a line by itself\.\s?.*',
                        action=cert_key_handler,
                        args={"data": certificate},
                        loop_continue=True,
                        continue_timer=False
                    ),
                ]
            )

    try:
       output = device.execute(f"crypto pki server {server_name} request pkcs10 {retrive_method} {certificate_format}",
                         reply=dialog, timeout=200)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not get the grant ID full output from device "
            "Error: {error}".format(error=e)
            )

    return output

def get_grant_id_pki_server(grant_output):
    """ Gets grant ID from Grant ID output
        Args:
            device (`obj`): Device object
            grant_output ('str'): Grant ID output

        Returns:
            Grant ID or None

        Raise:
            SubCommandFailure: Failed to retrieve Grant ID from Grant ID full output
    """
    p = re.compile(r'\% Enrollment request pending\, reqId\=(?P<grant_id>\d+)')
    m = p.search(grant_output)
    grant = m.group('grant_id')

    return grant


def get_grant_certificate(device, grant_id):
    """ Generates grant certificate on device

        Args:
            device (`obj`): Device object
            grant_id ('str'): Grant ID to generate the grant

        Returns:
            Grant Certificate or None

        Raise:
            SubCommandFailure: Failed to generate grant certificate on device
    """

    try:
        output = device.execute([f"crypto pki server cisco grant {grant_id}"])
    except SubCommandFailure:
        raise SubCommandFailure(
            "Could not generate certificate on device"
        )

    return output

def crypto_pki_import(device, certificate, label_name):
    """ Imports the certificate on the device
        Args:
            device (`obj`): Device object
            certificate ('str'): Certificate to import
			label_name ('str') : Label name

        Returns:
            None

        Raise:
            SubCommandFailure: Failed to import certificate on device
    """
	
    def cert_key_handler(spawn, data):
        spawn.sendline(data)
        spawn.sendline('\r')
        spawn.sendline('\r')

    dialog = Dialog(
                [
                    Statement(
                        r"^.*Are you sure you want to do this\? \[yes/no\]\s?.*$",
                        action="sendline(yes)",
                        loop_continue=True,
                    ),
                    Statement(
                        r'^.*End with a blank line or the word "quit" on a line by itself\s?.*',
                        action=cert_key_handler,
                        args={"data": certificate},
                        loop_continue=True,
                        continue_timer=False
                    ),
                ]
            )

    try:
       device.configure(f"crypto pki import {label_name} certificate", reply=dialog, timeout=200)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not import certificate on device "
            "Error: {error}".format(error=e)
            )
