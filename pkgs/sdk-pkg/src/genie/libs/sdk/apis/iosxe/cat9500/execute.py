'''IOSXE CAT9K specific execute functions'''

# Python
import time
import logging

# Logger
log = logging.getLogger(__name__)


def execute_reload(device, prompt_recovery, reload_creds, reload_file=None, sleep_after_reload=120,
    timeout=800):
    ''' Reload device
        Args:
            device ('obj'): Device object
            prompt_recovery ('bool'): Enable/Disable prompt recovery feature
            reload_creds ('str'): Credential name defined in the testbed yaml file to be used during reload
            reload_file ('str'): File to reload the setup with, defaulted to None
            sleep_after_reload ('int'): Time to sleep after reload in seconds, default: 120
            timeout ('int'): reload timeout value, defaults 800 seconds.
    '''

    log.info("Reloading device '{d}'".format(d=device.name))

    credentials = ['default']

    if reload_creds:
        credentials.insert(0, reload_creds)

    if reload_file:
        try:
            # tftp://223.255.254.254/francois/cat9k_iosxe.2019-06-14_19.31_francois.SSA.bin
            device.execute('install add file {} activate commit prompt-level none'.\
                format(reload_file), prompt_recovery=prompt_recovery,
                reload_creds=credentials, timeout=timeout)
        except Exception as e:
            log.error("Error while copying image to standby and reloading "
                "the whole setup with the new image on device {}".format(device.name))
            raise e
    else:
        try:
            device.reload(prompt_recovery=prompt_recovery, reload_creds=credentials,
                          timeout=timeout)
        except Exception as e:
            log.error("Error while reloading device {}".format(device.name))
            raise e

    log.info("Waiting '{}' seconds after reload ...".format(sleep_after_reload))
    time.sleep(sleep_after_reload)