"""Common configure functions for crypto key"""

# Python
import logging
import re
from typing import Any

# Unicon
from unicon.core.errors import SubCommandFailure
from unicon.eal.dialogs import Statement, Dialog

# Genie
from genie.metaparser.util.exceptions import SchemaEmptyParserError

logger = logging.getLogger(__name__)

def generate_crypto_key(device, 
                        key_type, 
                        key_label=None,
                        modulus=None,
                        key_size=None,
                        exportable=False,
                        timeout=30):
    """ Generate Crypto keys
        Args:
            device ('obj')    : device to use
            key_type ('str', optional)  : iosxe routers support rsa and ec keys
            key_label ('str', optional) : Name of the keypair
            modulus ('int', optional) : Size of the key that will be generated. <512-4096> 
            keysize ('int', optional) : Size of the EC keys. <256,384,521>
            exportable ('boolean', optional) : Allows the key to be exported. Default value is False
            timeout('int', optional): timeout for exec command execution, default is 30
        Returns:
            None
        Raises:
            SubCommandFailure
    """

    dialog = Dialog([
                Statement(pattern=r'.*How many bits in the modulus.*',
                    action=f'sendline(2048)',
                    loop_continue=True,
                    continue_timer=False),
                Statement(pattern=r'.*% Do you really want to replace them.*',
                    action=f'sendline(yes)',
                    loop_continue=True,
                    continue_timer=False)
    ])

    #initialize list variable
    configs = []

    if key_type == 'rsa':
        if key_label is None:
            if modulus is not None:
                if exportable is True:
                    configs = (f"crypto key generate {key_type} modulus {modulus} exportable")
                elif exportable is False:
                    configs = (f"crypto key generate {key_type} modulus {modulus}")
            elif modulus is None:
                if exportable is True:
                    configs = (f"crypto key generate {key_type} exportable")
                elif exportable is False:
                    configs = (f"crypto key generate {key_type}")

                    
        elif key_label is not None:
            if modulus is not None:
                if exportable is True:
                    configs = (f"crypto key generate {key_type} label {key_label} modulus {modulus} exportable")
                elif exportable is False:
                    configs = (f"crypto key generate {key_type} label {key_label} modulus {modulus}")
            elif modulus is None:
                if exportable is True:
                    configs = (f"crypto key generate {key_type} label {key_label} exportable")
                elif exportable is False:
                    configs = (f"crypto key generate {key_type} label {key_label}")


    elif key_type == 'ec':
        if key_label is None:
            if exportable is False:
                configs = (f"crypto key generate {key_type} keysize {key_size}")
            elif exportable is True:
                configs = (f"crypto key generate {key_type} keysize {key_size} exportable")
        elif key_label is not None:
            if exportable is False:
                configs = (f"crypto key generate {key_type} keysize {key_size} label {key_label}")
            elif exportable is True:
                configs = (f"crypto key generate {key_type} keysize {key_size} exportable label {key_label}")


    error_patterns = ['% Please define a domain-name first.']

    try:
        device.configure(configs, reply=dialog, error_pattern=error_patterns, timeout=timeout)
    except SubCommandFailure as e:
        logger.error(e)
        raise SubCommandFailure("Could not generate keys")


def crypto_key_export (device, 
                        key_type, 
                        key_label, 
                        export_via,
                        encryption, 
                        passphrase,
                        timeout=30
                        ):
    """ Crypto key export
        Args:
            device ('obj')    : device to use
            key_type ('str', optional)  : iosxe routers support rsa or ec keys
            key_label ('str', optional) : Name of the keypair
            export_via ('str', optional) : Export keys via terminal or file system. Format to be used {"terminal" | "url bootflash:"}
            encryption ('str', optional) : Generates a general purpose RSA key pair for signing and encryption
            passphrase ('str', optional) : Passphrase used to protect the private key
            timeout('int', optional): timeout for exec command execution, default is 30
        Returns:
            export_key
        Raises:
            SubCommandFailure

    """

    #initialize list variable
    configs = []
    configs.append(f"crypto key export {key_type} {key_label} pem {export_via} {encryption} {passphrase}")

    error_patterns = [f'% RSA keypair {key_label} is not exportable.']

    try:
        export_key=device.configure(configs, error_pattern=error_patterns, timeout=30)
        logger.info("The keys are saved in a variable called export_key")
        return export_key
    except SubCommandFailure as e:
        logger.error("Failed to export keys"
             "Error:\n{error}".format(error=e)
        )
        raise

def generate_crypto_key_execute(device, key_type, modulus=''):
    """ Generate Crypto keys in execute mode
        Args:
            device ('obj')    : device to use
            key_type ('str')  : iosxe routers support rsa and ec keys
            modulus ('int', optional) : Size of the key that will be generated. <512-4096> 
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    if modulus:
        cmd = f"crypto key generate {key_type} modulus {modulus}"
    else:
        cmd = f"crypto key generate {key_type}"
    try:
        device.execute(cmd)
    except SubCommandFailure as e:
        logger.error(e)
        raise SubCommandFailure("Could not generate keys")
