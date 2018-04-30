import time
import logging


log = logging.getLogger(__name__)

def sleep_processor(section):
    '''Sleep prepostprocessor

    Can be controlled via sections parameters which is provided by the
    triggers/verification datafile
    '''

    if section and getattr(section, 'parameters', {}):
        sleep_time = section.parameters.get('sleep', None)
        if sleep_time:
            log.info("Sleeping for '{t}' seconds before "
                     "executing the testcase".format(t=sleep_time))
            time.sleep(sleep_time)
