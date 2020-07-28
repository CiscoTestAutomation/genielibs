import time
import logging

log = logging.getLogger(__name__)

def execute_reload(device, prompt_recovery, reload_creds, sleep_after_reload=120,
    timeout=800, **kwargs):
    ''' Reload device
        Args:
            device ('obj'): Device object
            prompt_recovery ('bool'): Enable/Disable prompt recovery feature
            reload_creds ('str'): Credential name defined in the testbed yaml file to be used during reload
            sleep_after_reload ('int'): Time to sleep after reload in seconds, default: 120
            timeout ('int'): reload timeout value, defaults 800 seconds.
    '''

    log.info("Reloading device '{d}'".format(d=device.name))

    credentials = ['default']

    if reload_creds:
        credentials.insert(0, reload_creds)

    try:
        device.reload(prompt_recovery=prompt_recovery, reload_creds=credentials,
                      timeout=timeout)
    except Exception as e:
        log.error("Error while reloading device {}".format(device.name))
        raise e

    log.info("Waiting '{}' seconds after reload ...".format(sleep_after_reload))
    time.sleep(sleep_after_reload)

