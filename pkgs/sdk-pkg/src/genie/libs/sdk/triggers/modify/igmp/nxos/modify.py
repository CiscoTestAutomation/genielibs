'''NXOS Implementation for Igmp modify triggers'''

# python
from copy import deepcopy 

# pyats
from pyats import aetest

# Genie Libs
from genie.libs.sdk.libs.utils.mapping import Mapping
from genie.libs.sdk.triggers.modify.modify import TriggerModify

# pyats
from pyats.utils.objects import Not, NotExists

# Which key to exclude for Igmp Ops comparison
igmp_exclude = ['maker', 'expire', 'up_time']


class TriggerModifyIgmpVersion(TriggerModify):
    """Modify dynamically learned enabled Igmp interface(s) version then restore the
      configuration by reapplying the whole running configuration."""

    __description__ = """Modify dynamically learned enabled Igmp interface(s) version
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
            static:
                The keys below are dynamically learnt by default.
                However, they can also be set to a custom value when provided in the trigger datafile.

                interface: `str`
                vrf: `str`

                (e.g) interface: '(?P<interface>Ethernet1*)' (Regex supported)
                    OR
                    interface: 'Ethernet1/1/1' (Specific value)

    steps:
        1. Learn Igmp Ops object and store the Igmp interface version
           if has any, otherwise, SKIP the trigger
        2. Save the current device configurations through "method" which user uses
        3. Modify the learned Igmp interface version from step 1 
           with Igmp Conf object
        4. Verify the Igmp interface version  from step 3 is reflected in device configuration
        5. Recover the device configurations to the one in step 2
        6. Learn Igmp Ops again and verify it is the same as the Ops in step 1

    """
    # Mapping of Information between Ops and Conf
    # Also permit to dictate which key to verify
    mapping = Mapping(requirements={
                          'ops.igmp.igmp.Igmp':{
                                'requirements':[\
                                    ['info', 'vrfs', '(?P<vrf>.*)', 'interfaces',
                                     '(?P<interface>.*)', 'enable', True],
                                    ['info', 'vrfs', '(?P<vrf>.*)', 'interfaces',
                                     '(?P<interface>.*)', 'version', '(?P<version>2)']],
                                'all_keys': True,
                                'kwargs':{'attributes': [
                                    'info[vrfs][(.*)]']},
                                'exclude': igmp_exclude}},
                      config_info={'conf.igmp.Igmp':{
                                       'requirements':[
                                         ['device_attr', '{uut}', 'vrf_attr', '(?P<vrf>.*)',
                                          'interface_attr', '(?P<interface>.*)', 'version',
                                          3]],
                                       'verify_conf':False,
                                       'kwargs':{}}},
                      verify_ops={
                          'ops.igmp.igmp.Igmp':{
                                'requirements':[\
                                    ['info', 'vrfs', '(?P<vrf>.*)', 'interfaces',
                                     '(?P<interface>.*)', 'version', 3]],
                                'kwargs':{'attributes': [
                                    'info[vrfs][(.*)]']},
                                'exclude': igmp_exclude}},
                      num_values={'vrf': 1, 'interface': 1})
