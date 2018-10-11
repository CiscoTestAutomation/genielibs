'''NXOS Implementation for Pim modify triggers'''

# Genie Libs
from genie.libs.sdk.libs.utils.mapping import Mapping
from genie.libs.sdk.triggers.modify.modify import TriggerModify

# Which key to exclude for Pim Ops comparison
pim_exclude = ['maker']


class TriggerModifyPimNeighborFilter(TriggerModify):
    """Modify dynamically learned PIM interface(s)'s neighbor-filter then restore the
      configuration by reapplying the whole running configuration."""

    __description__ = """Modify dynamically learned PIM interface(s)'s neighbor-filter
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
        1. Learn Pim Ops object and store the PIM interface(s)'s neighbor-filter
           if has any, otherwise, SKIP the trigger
        2. Save the current device configurations through "method" which user uses
        3. Modify the learned PIM interface(s)'s neighbor-filter from step 1 
           with Pim Conf object
        4. Verify the PIM interface(s)'s neighbor-filter from step 3 is
           reflected in device configuration
        5. Recover the device configurations to the one in step 2
        6. Learn Pim Ops again and verify it is the same as the Ops in step 1

    """
    MODIFY_NAME = 'modified_pim_neighbor_policy'

    # Mapping of Information between Ops and Conf
    # Also permit to dictate which key to verify
    mapping = Mapping(requirements={
                          'ops.pim.pim.Pim':{
                                'requirements':[\
                                    ['info', 'vrf', '(?P<vrf>.*)', 'interfaces',
                                     '(?P<pim_intf>.*)', 'address_family', '(?P<af>.*)',
                                     'neighbor_filter', '(?P<neighbor_filter>.*)'],
                                    ['info', 'vrf', '(?P<vrf>.*)', 'interfaces',
                                     '(?P<pim_intf>.*)', 'address_family', '(?P<af>.*)',
                                     'oper_status', 'up']],
                                'kwargs':{'attributes': [
                                    'info[vrf][(.*)][interfaces][(.*)][address_family][(.*)][oper_status]',
                                    'info[vrf][(.*)][interfaces][(.*)][address_family][(.*)][neighbor_filter]']},
                                'exclude': pim_exclude}},
                      config_info={'conf.pim.Pim':{
                                       'requirements':[
                                         ['device_attr', '{uut}', 'vrf_attr', '(?P<vrf>.*)',
                                          'address_family_attr', '(?P<af>.*)', 'interface_attr',
                                          '(?P<pim_intf>.*)', 'neighbor_filter', MODIFY_NAME]],
                                       'verify_conf':False,
                                       'kwargs':{}}},
                      verify_ops={
                          'ops.pim.pim.Pim':{
                                'requirements':[\
                                    ['info', 'vrf', '(?P<vrf>.*)', 'interfaces',
                                     '(?P<pim_intf>.*)', 'address_family', '(?P<af>.*)',
                                     'neighbor_filter', MODIFY_NAME],
                                    ['info', 'vrf', '(?P<vrf>.*)', 'interfaces',
                                     '(?P<pim_intf>.*)', 'address_family', '(?P<af>.*)',
                                     'oper_status', 'up']],
                                'kwargs':{'attributes': [
                                    'info[vrf][(.*)][interfaces][(.*)][address_family][(.*)][oper_status]',
                                    'info[vrf][(.*)][interfaces][(.*)][address_family][(.*)][neighbor_filter]']},
                                'exclude': pim_exclude}},
                      num_values={'vrf': 1, 'af': 1, 'pim_intf': 1})