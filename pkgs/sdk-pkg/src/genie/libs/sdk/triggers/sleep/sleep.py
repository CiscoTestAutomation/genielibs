'''Common implementation for sleep triggers'''
# python import
import logging
import time

# pyats import
from pyats import aetest

# Genie Libs import
from genie.libs.sdk.triggers.template.sleep import TriggerSleep

log = logging.getLogger(__name__)


class TriggerSleep(TriggerSleep):
    '''Trigger class for Sleep action'''

    @aetest.test
    def sleep(self, uut, sleep_time, message_time):
        ''' Trigger will sleep for 'sleep_time' seconds given by the user
            and will populate a message with the remaining sleep time every 
            'message_time' seconds.
        '''

        log.info('Sleeping for {f} seconds'.format(f=sleep_time))

        for iteration in range(sleep_time, 0, -1):
            time.sleep(1)
            if (iteration % message_time) == 0 and (iteration != sleep_time):
                log.info('{f} seconds remaining'.format(f=iteration))
