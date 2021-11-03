# '''IOSXE Implementation for Interface unconfigconfig triggers'''

# import pyats
from pyats.utils.objects import Not, NotExists

# Genie Libs
from genie.libs.sdk.libs.utils.mapping import Mapping
from genie.libs.sdk.triggers.unconfigconfig.unconfigconfig import TriggerUnconfigConfig

# Which key to exclude for Vxlan Ops comparison
vxlan_vni_exclude = ['num_l3vni_cp', 'num_l2vni_cp', 'num_l2vni_dp']


class TriggerUnconfigConfigNveVni(TriggerUnconfigConfig):
    """Unconfigure NVE L2 or L3 VNI and reapply the whole configurations of dynamically learned Nve(s)."""

    __description__ = """Unconfigure nve L2 or L3 VNI and reapply the whole configurations of dynamically learned Nve(s).

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
                 Buffer recovery timeout when the previous timeout has been exhausted,
                 to make sure the devices are recovered before ending the trigger

                 max_time (`int`): Maximum wait time for the last step of the trigger,
                                 in second. Default: 180
                 interval (`int`): Wait time between iteration when looping is needed,
                                 in second. Default: 15
             static:
                 The keys below are dynamically learnt by default.
                 However, they can also be set to a custom value when provided in the trigger datafile.

                  nve_name: `str`
                  nve_vni: `str`

                  (e.g) interface: '(?P<interface>Ethernet1*)' (Regex supported)
                        OR
                        interface: 'Ethernet1/1/1' (Specific value)
       steps:
         1. Learn Vxlan Ops object and store the nve information under nve if has any,
            otherwise, SKIP the trigger
         2. Save the current device configurations through "method" which user uses
         3. Unconfigure the nve_vni with Interface Conf object
         4. Verify the nve_vni from step 3 no longer exists
         5. Recover the device configurations to the one in step 2
         6. Learn Vxlan Ops again and verify it is the same as the Ops in step 1
       """

    mapping = Mapping(requirements={'ops.vxlan.vxlan.Vxlan': {
                                        'requirements': [['nve', '(?P<nve_name>nve.*)', 'vni', '(?P<nve_vni>.*)', 'vni_state', 'Up'],
                                                         ['nve', '(?P<nve_name>nve.*)', 'admin_state','Up'],
                                                         ['nve', '(?P<nve_name>nve.*)', 'oper_state','Up']],
                                        'kwargs': {'attributes': ['nve[(.*)]']},
                                        'all_keys': True,
                                        'exclude': vxlan_vni_exclude}},
                      config_info={'conf.interface.Interface': {
                                        'requirements': [['nve_vni','(?P<nve_vni>.*)']],
                                        'verify_conf': False,
                                        'kwargs': {'mandatory': {'name': '(?P<nve_name>nve.*)', 'attach': False}}}},
                      verify_ops={'ops.vxlan.vxlan.Vxlan': {
                                        'requirements': [['nve', '(?P<nve_name>nve.*)', 'vni', NotExists('(?P<nve_vni>.*)')]],
                                        'kwargs': {'attributes': ['nve[(.*)]']},
                                        'all_keys': True,
                                        'exclude': vxlan_vni_exclude}},
                      num_values={'nve_name':1 , 'nve_vni':1 })
