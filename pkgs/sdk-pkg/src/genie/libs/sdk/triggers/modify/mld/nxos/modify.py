'''NXOS Implementation for Mld modify triggers'''

# python
from copy import deepcopy 

# pyats
from ats import aetest

# Genie Libs
from genie.libs.sdk.libs.utils.mapping import Mapping
from genie.libs.sdk.triggers.modify.modify import TriggerModify

# pyats
from ats.utils.objects import Not, NotExists

# Which key to exclude for Mld Ops comparison
mld_exclude = ['maker', 'expire', 'up_time']


class TriggerModifyMldVersion(TriggerModify):
    """Modify dynamically learned enabled Mld interface(s) version then restore the
      configuration by reapplying the whole running configuration."""

    __description__ = """Modify dynamically learned enabled Mld interface(s) version
    then restore the configuration by reapplying the whole running configuration.

    trigger_datafile:
        Mandatory:
            timeout: 
                max_time (`int`): Maximum wait time for the trigger,
                                in second. Default: 180
                interval (`int`): Wait time between iteration when looping is needed,
                                in second. Default: 15
                method (`str`): Method to recover the device configuration,
                              Support methods:
                                'checkpoint': Rollback the configuration by
                                              checkpoint (nxos),
                                              archive file (iosxe),
                                              load the saved running-config file on disk (iosxr)
        Optional:
            tgn_timeout (`int`): Maximum wait time for all traffic threads to be
                                 restored to the reference rate,
                                 in second. Default: 60
            tgn_delay (`int`): Wait time between each poll to verify if traffic is resumed,
                               in second. Default: 10
            timeout_recovery: 
                Buffer recovery timeout make sure devices are recovered at the end
                of the trigger execution. Used when previous timeouts have been exhausted.

                max_time (`int`): Maximum wait time for the last step of the trigger,
                                in second. Default: 180
                interval (`int`): Wait time between iteration when looping is needed,
                                in second. Default: 15

    steps:
        1. Learn Mld Ops object and store the Mld interface version
           if has any, otherwise, SKIP the trigger
        2. Save the current device configurations through "method" which user uses
        3. Modify the learned Mld interface version from step 1 
           with Mld Conf object
        4. Verify the Mld interface version  from step 3 is reflected in device configuration
        5. Recover the device configurations to the one in step 2
        6. Learn Mld Ops again and verify it is the same as the Ops in step 1

    """
    # Mapping of Information between Ops and Conf
    # Also permit to dictate which key to verify
    mapping = Mapping(requirements={
                          'ops.mld.mld.Mld':{
                                'requirements':[\
                                    ['info', 'vrfs', '(?P<vrf>.*)', 'interfaces',
                                     '(?P<mld_intf>.*)', 'enable', True],
                                    ['info', 'vrfs', '(?P<vrf>.*)', 'interfaces',
                                     '(?P<mld_intf>.*)', 'version', '(?P<version>2)']],
                                'all_keys': True,
                                'kwargs':{'attributes': [
                                    'info[vrfs][(.*)]']},
                                'exclude': mld_exclude}},
                      config_info={'conf.mld.Mld':{
                                       'requirements':[
                                         ['device_attr', '{uut}', 'vrf_attr', '(?P<vrf>.*)',
                                          'interface_attr', '(?P<mld_intf>.*)', 'version',
                                          1]],
                                       'verify_conf':False,
                                       'kwargs':{}}},
                      verify_ops={
                          'ops.mld.mld.Mld':{
                                'requirements':[\
                                    ['info', 'vrfs', '(?P<vrf>.*)', 'interfaces',
                                     '(?P<mld_intf>.*)', 'version', 1]],
                                'missing': False,
                                'kwargs':{'attributes': [
                                    'info[vrfs][(.*)]']},
                                'exclude': mld_exclude}},
                      num_values={'vrf': 1, 'mld_intf': 1})
