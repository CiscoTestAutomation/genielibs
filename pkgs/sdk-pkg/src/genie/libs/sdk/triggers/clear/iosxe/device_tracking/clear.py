import logging
from ats import aetest
from genie.harness.base import Trigger

log = logging.getLogger(__name__)


class TriggerClearDeviceTrackingDatabase(Trigger):
    '''Clear device tracking database using the existing API'''

    @aetest.test
    def clear_device_tracking_databse(self, uut, options=None):
        uut.api.clear_device_tracking_database(options)
