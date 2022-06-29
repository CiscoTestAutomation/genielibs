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


def execute_ap_tx_power_commands(device, ap_name, ap_model, tx_power):
    try:
        execute_string_1 = 'ap name ' + ap_name + ' shut' + '\n' + \
        'ap name ' + ap_name + ' dot11 5ghz shut' + '\n' + \
        'ap name ' + ap_name + ' dot11 5ghz radio role manual client-serving' + '\n' + \
        'ap name ' + ap_name + ' dot11 5ghz txpower {}'.format(tx_power) + '\n' + \
        'ap name ' + ap_name + ' no dot11 5ghz shut' + '\n' + \
        'ap name ' + ap_name + ' dot11 24ghz shut' + '\n' + \
        'ap name ' + ap_name + ' dot11 24ghz radio role manual client-serving' + '\n' + \
        'ap name ' + ap_name + ' dot11 24ghz txpower {}'.format(tx_power) + '\n' + \
        'ap name ' + ap_name + ' no dot11 24ghz shut' + '\n' + \
        'ap name ' + ap_name + ' no shut' + '\n'
        
        execute_string_2 = 'ap name ' + ap_name + ' shut' + '\n' + \
        'ap name ' + ap_name + ' dot11 5ghz shut' + '\n' + \
        'ap name ' + ap_name + ' dot11 5ghz txpower {}'.format(tx_power) + '\n' + \
        'ap name ' + ap_name + ' dot11 5ghz channel auto' + '\n' + \
        'ap name ' + ap_name + ' no dot11 5ghz shut' + '\n' + \
        'ap name ' + ap_name + ' dot11 24ghz shut' + '\n' + \
        'ap name ' + ap_name + ' dot11 24ghz txpower {}'.format(tx_power) + '\n' + \
        'ap name ' + ap_name + ' dot11 24ghz channel auto' + '\n' + \
        'ap name ' + ap_name + ' no dot11 24ghz shut' + '\n' + \
        'ap name ' + ap_name + ' no shut' + '\n'

        if "9130" in ap_model:
            device.execute(execute_string_1)

        else:
            device.execute(execute_string_2)
			
    except SubCommandFailure as e:
        raise SubCommandFailure("Failed in configure ap tx power on device {device} Error: {e}".format(device=device.name,e=str(e))) from e
		
    else:
        log.info("Successfully assigned tx power to AP-{}".format(ap_name))
