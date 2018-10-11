'''NXOS Implementation for Pim add-remove triggers'''

# Genie Libs
from genie.libs.sdk.libs.utils.mapping import Mapping
from genie.libs.sdk.triggers.addremove.addremove import TriggerAddRemove

# pyats
from ats.utils.objects import NotExists

# Which key to exclude for Pim Ops comparison
pim_exclude = ['maker',]
                     

class TriggerAddRemovePimNeighborFilter(TriggerAddRemove):
    """Apply the Pim interface(s)'s neighbor-filter, add remove added Pim interface(s)'s neighbor-filter"""

    __description__ = """Apply the Pim interface(s)'s neighbor-filter,
    add remove added Pim interface(s)'s neighbor-filter.

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
        1. Learn Pim Ops/Conf object and store the Pim interface(s)'s neighbor-filter.
        2. Save the current device configurations through "method" which user uses
        3. Add the configuration of Pim interface(s)'s neighbor-filter with Pim Conf object
        4. Verify the Pim interface(s)'s neighbor-filter from step 3 has configured
        5. Remove the Pim interface(s)'s neighbor-filter configurations.
        6. Recover the device configurations to the one in step 2
        7. Learn Pim Ops again and verify it is the same as the Ops in step 1

    """
    ADD_NAME = 'added_pim_neighbor_policy'

    # Mapping of Information between Ops and Conf
    # Also permit to dictate which key to verify
    mapping = Mapping(requirements={
                          'ops.pim.pim.Pim':{
                                'requirements':[\
                                    ['info', 'vrf', '(?P<vrf>.*)', 'interfaces',
                                     '(?P<pim_intf>.*)', 'address_family', '(?P<af>.*)',
                                     NotExists('neighbor_filter')],
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
                                          '(?P<pim_intf>.*)', 'neighbor_filter', ADD_NAME]],
                                       'verify_conf':False,
                                       'kwargs':{}}},
                      verify_ops={
                          'ops.pim.pim.Pim':{
                                'requirements':[\
                                    ['info', 'vrf', '(?P<vrf>.*)', 'interfaces',
                                     '(?P<pim_intf>.*)', 'address_family', '(?P<af>.*)',
                                     'neighbor_filter', ADD_NAME],
                                    ['info', 'vrf', '(?P<vrf>.*)', 'interfaces',
                                     '(?P<pim_intf>.*)', 'address_family', '(?P<af>.*)',
                                     'oper_status', 'up']],
                                'kwargs':{'attributes': [
                                    'info[vrf][(.*)][interfaces][(.*)][address_family][(.*)][oper_status]',
                                    'info[vrf][(.*)][interfaces][(.*)][address_family][(.*)][neighbor_filter]']},
                                'exclude': pim_exclude}},
                      num_values={'vrf': 1, 'af': 1, 'pim_intf': 1})

