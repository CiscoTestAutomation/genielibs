'''NXOS Implementation for Interface unconfigconfig triggers'''

# Genie Libs
from genie.libs.sdk.libs.utils.mapping import Mapping
from genie.libs.sdk.triggers.unconfigconfig.unconfigconfig import TriggerUnconfigConfig

# Which key to exclude for NVE Ops comparison
nve_exclude = ['maker',]


class TriggerUnconfigConfigVxlanNveOverlayInterface(TriggerUnconfigConfig):
    """Unconfigure and reapply the dynamically learned Nve onverlay interface(s)."""

    __description__ = """Unconfigure and reapply the dynamically learned Nve onverlay interface(s).

    trigger_datafile:
        Mandatory:
            timeout: 
                max_time (`int`): Maximum wait time for the trigger,
                                in second. Default: 180
                interval (`int`): Wait time between iteration when looping is needed,
                                in second. Default: 15
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
        1. Learn VxLan Ops object and verify if has any "up" Nve interface(s),
           otherwise, SKIP the trigger
        2. Unconfigure the learned Nve interface(s) from step 1 with Interface Conf object
        3. Verify the state of learned Nve interface(s) from step 2 is removed
        4. Reapply the configuration of Nve interface(s) with checkpoint
        5. Learn VxLan Ops again and verify it is the same as the Ops in step 1
        
    """

    # Mapping of Information between Ops and Conf
    # Also permit to dictate which key to verify
    mapping = Mapping(requirements={'ops.vxlan.vxlan.Vxlan': {
                                        'requirements': [['nve', '(?P<name>.*)', 'if_state', 'up']],
                                        'kwargs': {'attributes': [
                                                      'nve[(.*)][if_state]',
                                                      'nve[(.*)][vni][(.*)][vni]']},
                                        'exclude': nve_exclude}},
                      config_info={'conf.interface.Interface':{
                                        'requirements':[],
                                        'verify_conf':False,
                                        'kwargs':{'mandatory':{'name': '(?P<name>.*)',
                                                               'attach': False}}}},
                      verify_ops={'ops.vxlan.vxlan.Vxlan':{
                                        'requirements':[['nve', '(?P<name>.*)']],
                                        'kwargs': {'attributes': [
                                                      'nve[(.*)][if_state]',
                                                      'nve[(.*)][vni][(.*)][vni]']},
                                        'exclude': nve_exclude}},
                      num_values={'name': 1})
