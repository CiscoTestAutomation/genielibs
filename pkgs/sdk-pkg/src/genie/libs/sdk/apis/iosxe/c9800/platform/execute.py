'''c9800 execute functions for platform'''

# Python
import logging

# Unicon
from unicon.core.errors import SubCommandFailure

# Logger
log = logging.getLogger(__name__)


def execute_self_signed_certificate_command(device, password, key_size=2048, signature_algorithm="sha256",
                                            encryption_type=0, timeout=300):
    """Execute command that installs self signed certificate
        Args:
            device (obj): Device object
            password (str): Password to be configured for the trustpoint.
            key_size (int, optional): Key size to be configured. Default is 2048
                Options: 1024/2048/3072

            signature_algorithm (str, optional): Algorithm to be applied. Default is sha256
                    Options: sha1/sha256/sha384

            encryption_type (int, optional): Encryption type to be configured. Default is 0
                    Options: 0/7
            timeout (int, optional): Execute timeout in seconds. Defaults to 300.
        Returns:
                None
        Raises:
                SubCommandFailure
        """

    try:
        device.execute("wireless config vwlc-ssc key-size {} signature-algo {} password {} {}"\
                .format(key_size, signature_algorithm, encryption_type, password, timeout=timeout))

    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed in install self signed certificate "
            "on device {device} "
            "Error: {e}".format(
                device=device.name,
                e=str(e)
            )
        ) from e

    else:
        log.info("Successfully configured self signed certificate for {}".format(device.name))
