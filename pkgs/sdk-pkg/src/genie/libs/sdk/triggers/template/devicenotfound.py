''' triggerNoDevice template '''

# import ats
from ats import aetest

# import genie infra
from genie.harness.base import Trigger

@aetest.skip(reason='The device provided does not exist in the testbed yaml')
class TriggerDeviceNotFound(Trigger):
    ''' Trigger that is used when a device is not found '''
    pass
