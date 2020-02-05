''' triggerDisableEnable template'''

# import pyats
from pyats import aetest

# import genie infra
from genie.harness.base import Trigger


class TriggerDisableEnable(Trigger):
    ''' Template for all DisableEnable triggers

        triggerDisableEnable will follow the following steps:

          1. Extract the information from ops object.

          2. Store configurations via checkpoint or tftp file.

          3. Disable feature via cli "no feature <feature>".

          4. Verify if the feature disabled by "show feature".

          5. Enable feature via checkpoint or tftp file.

          6. Verify if the feature enabled by "show feature" and
             compare ops to original ops before the action.

    '''

    @aetest.test
    def verify_prerequisite(self):
        raise NotImplementedError

    @aetest.test
    def save_configuration(self):
        raise NotImplementedError

    @aetest.test
    def disable(self):
        raise NotImplementedError

    @aetest.test
    def verify_disable(self):
        raise NotImplementedError

    @aetest.test
    def restore_configuration(self):
        raise NotImplementedError

    @aetest.test
    def verify_initial_state(self):
        raise NotImplementedError


class TriggerDisableEnableReqHandler(Trigger):
    ''' Template for all DisableEnable triggers

        triggerDisableEnable will follow the following steps:

          1. Extract the information from ops object.

          2. Store configurations via checkpoint or tftp file.

          3. Handle the configuration dependencies before disabling 
             the feature if needed. Ex. the portchannel interfaces
             should be removed when disabling lacp feature.

          4. Disable feature via cli "no feature <feature>".

          5. Verify if the feature disabled by "show feature".

          6. Handle the configurations dependencies before enabling
             the feature if needed. Ex. Adding dynamic vlans back.

          7. Enable feature via checkpoint or tftp file.

          8. Verify if the feature enabled by "show feature" and
             compare ops to original ops before the action.

    '''

    @aetest.test
    def verify_prerequisite(self):
        raise NotImplementedError

    @aetest.test
    def save_configuration(self):
        raise NotImplementedError

    @aetest.test
    def pre_handle_dependency(self):
        raise NotImplementedError

    @aetest.test
    def disable(self):
        raise NotImplementedError

    @aetest.test
    def verify_disable(self):
        raise NotImplementedError

    @aetest.test
    def post_handle_dependency(self):
        raise NotImplementedError

    @aetest.test
    def restore_configuration(self):
        raise NotImplementedError

    @aetest.test
    def verify_initial_state(self):
        raise NotImplementedError
