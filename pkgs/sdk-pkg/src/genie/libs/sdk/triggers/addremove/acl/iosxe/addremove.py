'''IOSXE Implementation for routing addremove triggers'''

# python
from functools import partial

# import genie.libs
from genie.libs.sdk.libs.utils.mapping import Mapping
from genie.libs.sdk.triggers.addremove.addremove import TriggerAddRemove

# ATS
from pyats import aetest
from pyats.utils.objects import NotExists, Not

# Which key to exclude for ACL Ops comparison
acl_exclude = ['maker', 'attributes']

interface_exclude = ['maker', 'last_change','in_rate','in_rate_pkts',
                     'out_rate', 'out_rate_pkts', 'in_octets',
                     'in_pkts', 'in_unicast_pkts', 'out_octets',
                     'out_pkts', 'out_unicast_pkts', 'out_multicast_pkts',
                     'in_multicast_pkts', 'last_clear', 'in_broadcast_pkts',
                     'out_broadcast_pkts', 'in_errors', '(Tunnel.*)', 'status',
                     'accounting']


class TriggerAddRemoveEthernetMacAcl(TriggerAddRemove):
    """Apply the mac acl to ethernet interface, and remove the
    added mac acl
    """

    __description__ = """Apply the mac acl to ethernet interface, and remove the
    added mac acl.

    trigger_datafile:
        Mandatory:
            timeout: 
                max_time (`int`): Maximum wait time for the trigger,
                                in second. Default: 180
                interval (`int`): Wait time between iterations when looping is needed,
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
                interval (`int`): Wait time between iterations when looping is needed,
                                in second. Default: 15
            static:
                The keys below are dynamically learnt by default.
                However, they can also be set to a custom value when provided in the trigger datafile.

                interface: `str`

               (e.g) interface: '(?P<interface>Ethernet1*)' (Regex supported)
                     OR
                     interface: 'Ethernet1/1/1' (Specific value)
    steps:
        1. Learn acl Ops object and store the acls info if has any.
           Learn Interface ops object to select one trunk interface to add mac acl
        2. Save the current device configurations through "method" which user uses
        3. Add the configuration of acl with acl Conf object
        4. Verify the acl from step 3 has configured
        5. Remove the acl configurations.
        6. Recover the device configurations to the one in step 2
        7. Learn acl Ops again and verify it is the same as the Ops in step 1

    """
    ADD_ACL_NAME = 'etherent_mac_acl_add'


    mapping = Mapping(requirements={'ops.acl.acl.Acl':{
                                            'requirements':[['info', 'acls', NotExists(ADD_ACL_NAME)]],
                                            'exclude': acl_exclude},
                                    'ops.interface.interface.Interface':{
                                            'requirements':[['info', '(?P<interface>\w+Ethernet[\d\/]+$)',
                                                             'switchport_mode', 'trunk'],
                                                            ['info', '(?P<interface>\w+Ethernet[\d\/]+$)',
                                                             'oper_status', 'up']],
                                            'exclude': interface_exclude,
                                            'kwargs': {'attributes': ['info[(.*)][switchport_mode]',
                                                                      'info[(.*)][oper_status]']}}},
                      config_info={'conf.acl.Acl':{
                                      'requirements':[['device_attr', '{uut}',
                                                       'acl_attr', ADD_ACL_NAME,
                                                       'acl_type', 'eth-acl-type'],
                                                      ['device_attr', '{uut}',
                                                       'acl_attr', ADD_ACL_NAME,
                                                       'ace_attr', '10',
                                                       'actions_forwarding', 'permit'],
                                                      ['device_attr', '{uut}',
                                                       'acl_attr', ADD_ACL_NAME,
                                                       'ace_attr', '10',
                                                       'src', 'host 0011.2233.1111'],
                                                      ['device_attr', '{uut}',
                                                       'acl_attr', ADD_ACL_NAME,
                                                       'ace_attr', '10',
                                                       'dst', 'host 0011.2233.2222'],
                                                      ['device_attr', '{uut}',
                                                       'acl_attr', ADD_ACL_NAME,
                                                       'interface_attr', '(?P<interface>\w+Ethernet[\d\/]+$)',
                                                       'if_in', True]],
                                      'verify_conf':False,
                                      'kwargs':{}}},
                      verify_ops={'ops.acl.acl.Acl':{
                                      'requirements': [['info', 'acls', ADD_ACL_NAME, 'name', ADD_ACL_NAME],
                                                       ['info', 'acls', ADD_ACL_NAME, 'type', 'eth-acl-type'],
                                                       ['info', 'acls', ADD_ACL_NAME, 'aces', '10', 'name', '10'],
                                                       ['info', 'acls', ADD_ACL_NAME, 'aces', '10', 'matches',
                                                        'l2', 'eth', 'destination_mac_address', 'host 0011.2233.2222'],
                                                       ['info', 'acls', ADD_ACL_NAME, 'aces', '10', 'matches',
                                                        'l2', 'eth', 'source_mac_address', 'host 0011.2233.1111'],
                                                       ['info', 'acls', ADD_ACL_NAME, 'aces', '10', 'actions',
                                                        'logging', 'log-none'],
                                                       ['info', 'acls', ADD_ACL_NAME, 'aces', '10', 'actions',
                                                        'forwarding', 'permit']],
                                      'kwargs':{'attributes':['info']},
                                      'exclude': acl_exclude},
                                  'ops.interface.interface.Interface':{
                                          'requirements':[['info', '(?P<interface>\w+Ethernet[\d\/]+$)',
                                                           'switchport_mode', 'trunk'],
                                                          ['info', '(?P<interface>\w+Ethernet[\d\/]+$)',
                                                           'oper_status', 'up']],
                                            'kwargs': {'attributes': ['info[(.*)][switchport_mode]',
                                                                      'info[(.*)][oper_status]']},
                                          'exclude': interface_exclude}},
                      num_values={'interface':1})


class TriggerAddRemoveEthernetIpAclPermit(TriggerAddRemove):
    """Apply the IP acls with L2 ports which is Ethernet interfaces to device, and remove the
    added IP acls.
    """

    __description__ = """Apply the IP acls with L2 ports which is Ethernet
    interfaces to device, and remove the added IP acls..

    trigger_datafile:
        Mandatory:
            timeout: 
                max_time (`int`): Maximum wait time for the trigger,
                                in second. Default: 180
                interval (`int`): Wait time between iterations when looping is needed,
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
                interval (`int`): Wait time between iterations when looping is needed,
                                in second. Default: 15
            static:
                The keys below are dynamically learnt by default.
                However, they can also be set to a custom value when provided in the trigger datafile.

                interface: `str`

               (e.g) interface: '(?P<interface>Ethernet1*)' (Regex supported)
                     OR
                     interface: 'Ethernet1/1/1' (Specific value)
    steps:
        1. Learn acl Ops object and store the acls info if has any.
           Learn Interface ops object to select one trunk interface to add mac acl
        2. Save the current device configurations through "method" which user uses
        3. Add the configuration of acl with acl Conf object
        4. Verify the acl from step 3 has configured
        5. Remove the acl configurations.
        6. Recover the device configurations to the one in step 2
        7. Learn acl Ops again and verify it is the same as the Ops in step 1

    """
    ADD_ACL_NAME = 'ethernet_ip_acl_permit_add'
    ACTION = 'permit'

    mapping = Mapping(requirements={'ops.acl.acl.Acl':{
                                            'requirements':[['info', 'acls', NotExists(ADD_ACL_NAME)]],
                                            'exclude': acl_exclude},
                                    'ops.interface.interface.Interface':{
                                            'requirements':[['info', '(?P<interface>\w+Ethernet[\d\/]+$)',
                                                             'switchport_mode', 'trunk'],
                                                            ['info', '(?P<interface>\w+Ethernet[\d\/]+$)',
                                                             'oper_status', 'up']],
                                            'kwargs': {'attributes': ['info[(.*)][switchport_mode]',
                                                                      'info[(.*)][oper_status]']},
                                            'exclude': interface_exclude}},
                      config_info={'conf.acl.Acl':{
                                      'requirements':[['device_attr', '{uut}',
                                                       'acl_attr', ADD_ACL_NAME,
                                                       'acl_type', 'ipv4-acl-type'],
                                                      ['device_attr', '{uut}',
                                                       'acl_attr', ADD_ACL_NAME,
                                                       'ace_attr', '10',
                                                       'actions_forwarding', ACTION],
                                                      ['device_attr', '{uut}',
                                                       'acl_attr', ADD_ACL_NAME,
                                                       'ace_attr', '10',
                                                       'protocol', 'icmp'],
                                                      ['device_attr', '{uut}',
                                                       'acl_attr', ADD_ACL_NAME,
                                                       'ace_attr', '10',
                                                       'src', 'any'],
                                                      ['device_attr', '{uut}',
                                                       'acl_attr', ADD_ACL_NAME,
                                                       'ace_attr', '10',
                                                       'dst', 'any'],
                                                      ['device_attr', '{uut}',
                                                       'acl_attr', ADD_ACL_NAME,
                                                       'interface_attr', '(?P<interface>\w+Ethernet[\d\/]+$)',
                                                       'if_in', True]],
                                      'verify_conf':False,
                                      'kwargs':{}}},
                      verify_ops={'ops.acl.acl.Acl':{
                                      'requirements': [['info', 'acls', ADD_ACL_NAME, 'name', ADD_ACL_NAME],
                                                       ['info', 'acls', ADD_ACL_NAME, 'type', 'ipv4-acl-type'],
                                                       ['info', 'acls', ADD_ACL_NAME, 'aces', '10', 'name', '10'],
                                                       ['info', 'acls', ADD_ACL_NAME, 'aces', '10', 'actions',
                                                        'logging', 'log-none'],
                                                       ['info', 'acls', ADD_ACL_NAME, 'aces', '10', 'actions',
                                                        'forwarding', ACTION]],
                                      'kwargs':{'attributes':['info']},
                                      'exclude': acl_exclude},
                                  'ops.interface.interface.Interface':{
                                          'requirements':[['info', '(?P<interface>\w+Ethernet[\d\/]+$)',
                                                           'switchport_mode', 'trunk'],
                                                          ['info', '(?P<interface>\w+Ethernet[\d\/]+$)',
                                                           'oper_status', 'up']],
                                          'kwargs': {'attributes': ['info[(.*)][switchport_mode]',
                                                                      'info[(.*)][oper_status]']},
                                          'exclude': interface_exclude}},
                      num_values={'interface':1})


class TriggerAddRemoveEthernetIpAclDeny(TriggerAddRemove):
    """Apply the IP acls with L2 ports which is Ethernet interfaces to device, and remove the
    added IP acls.
    """

    __description__ = """Apply the IP acls with L2 ports which is Ethernet
    interfaces to device, and remove the added IP acls..

    trigger_datafile:
        Mandatory:
            timeout: 
                max_time (`int`): Maximum wait time for the trigger,
                                in second. Default: 180
                interval (`int`): Wait time between iterations when looping is needed,
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
                interval (`int`): Wait time between iterations when looping is needed,
                                in second. Default: 15
            static:
                The keys below are dynamically learnt by default.
                However, they can also be set to a custom value when provided in the trigger datafile.

                interface: `str`

               (e.g) interface: '(?P<interface>Ethernet1*)' (Regex supported)
                     OR
                     interface: 'Ethernet1/1/1' (Specific value)
    steps:
        1. Learn acl Ops object and store the acls info if has any.
           Learn Interface ops object to select one trunk interface to add mac acl
        2. Save the current device configurations through "method" which user uses
        3. Add the configuration of acl with acl Conf object
        4. Verify the acl from step 3 has configured
        5. Remove the acl configurations.
        6. Recover the device configurations to the one in step 2
        7. Learn acl Ops again and verify it is the same as the Ops in step 1

    """
    ADD_ACL_NAME = 'ethernet_ip_acl_deny_add'
    ACTION = 'deny'

    mapping = Mapping(requirements={'ops.acl.acl.Acl':{
                                            'requirements':[['info', 'acls', NotExists(ADD_ACL_NAME)]],
                                            'exclude': acl_exclude},
                                    'ops.interface.interface.Interface':{
                                            'requirements':[['info', '(?P<interface>\w+Ethernet[\d\/]+$)',
                                                             'switchport_mode', 'trunk'],
                                                            ['info', '(?P<interface>\w+Ethernet[\d\/]+$)',
                                                             'oper_status', 'up']],
                                            'kwargs': {'attributes': ['info[(.*)][switchport_mode]',
                                                                      'info[(.*)][oper_status]']},
                                            'exclude': interface_exclude}},
                      config_info={'conf.acl.Acl':{
                                      'requirements':[['device_attr', '{uut}',
                                                       'acl_attr', ADD_ACL_NAME,
                                                       'acl_type', 'ipv4-acl-type'],
                                                      ['device_attr', '{uut}',
                                                       'acl_attr', ADD_ACL_NAME,
                                                       'ace_attr', '10',
                                                       'actions_forwarding', ACTION],
                                                      ['device_attr', '{uut}',
                                                       'acl_attr', ADD_ACL_NAME,
                                                       'ace_attr', '10',
                                                       'protocol', 'icmp'],
                                                      ['device_attr', '{uut}',
                                                       'acl_attr', ADD_ACL_NAME,
                                                       'ace_attr', '10',
                                                       'src', 'any'],
                                                      ['device_attr', '{uut}',
                                                       'acl_attr', ADD_ACL_NAME,
                                                       'ace_attr', '10',
                                                       'dst', 'any'],
                                                      ['device_attr', '{uut}',
                                                       'acl_attr', ADD_ACL_NAME,
                                                       'interface_attr', '(?P<interface>\w+Ethernet[\d\/]+$)',
                                                       'if_in', True]],
                                      'verify_conf':False,
                                      'kwargs':{}}},
                      verify_ops={'ops.acl.acl.Acl':{
                                      'requirements': [['info', 'acls', ADD_ACL_NAME, 'name', ADD_ACL_NAME],
                                                       ['info', 'acls', ADD_ACL_NAME, 'type', 'ipv4-acl-type'],
                                                       ['info', 'acls', ADD_ACL_NAME, 'aces', '10', 'name', '10'],
                                                       ['info', 'acls', ADD_ACL_NAME, 'aces', '10', 'actions',
                                                        'logging', 'log-none'],
                                                       ['info', 'acls', ADD_ACL_NAME, 'aces', '10', 'actions',
                                                        'forwarding', ACTION]],
                                      'kwargs':{'attributes':['info']},
                                      'exclude': acl_exclude},
                                  'ops.interface.interface.Interface':{
                                          'requirements':[['info', '(?P<interface>\w+Ethernet[\d\/]+$)',
                                                           'switchport_mode', 'trunk'],
                                                          ['info', '(?P<interface>\w+Ethernet[\d\/]+$)',
                                                           'oper_status', 'up']],
                                          'kwargs': {'attributes': ['info[(.*)][switchport_mode]',
                                                                      'info[(.*)][oper_status]']},
                                          'exclude': interface_exclude}},
                      num_values={'interface':1})



class TriggerAddRemoveVlanIpAclPermit(TriggerAddRemove):
    """Apply the IP acls with L2 ports which is Vlan interfaces to device, and remove the
    added IP acls.
    """

    __description__ = """Apply the IP acls with L2 ports which is Vlan
    interfaces to device, and remove the added IP acls..

    trigger_datafile:
        Mandatory:
            timeout: 
                max_time (`int`): Maximum wait time for the trigger,
                                in second. Default: 180
                interval (`int`): Wait time between iterations when looping is needed,
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
                interval (`int`): Wait time between iterations when looping is needed,
                                in second. Default: 15

    steps:
        1. Learn acl Ops object and store the acls info if has any.
           Learn Interface ops object to select one Vlan interface to add ipv4 icmp acl
        2. Save the current device configurations through "method" which user uses
        3. Add the configuration of acl with acl Conf object
        4. Verify the acl from step 3 has configured
        5. Remove the acl configurations.
        6. Recover the device configurations to the one in step 2
        7. Learn acl Ops again and verify it is the same as the Ops in step 1

    """
    ADD_ACL_NAME = 'vlan_ip_acl_permit_add'
    ACTION = 'permit'

    mapping = Mapping(requirements={'ops.acl.acl.Acl':{
                                            'requirements':[['info', 'acls', NotExists(ADD_ACL_NAME)]],
                                            'exclude': acl_exclude},
                                    'ops.interface.interface.Interface':{
                                            'requirements':[['info', '(?P<intf>Vlan[\d]+$)',
                                                             'ipv4', '(?P<ip>.*)', 'ip', '(?P<ip_addr>.*)'],
                                                            ['info', '(?P<intf>Vlan[\d]+$)',
                                                             'oper_status', 'up']],
                                            'kwargs': {'attributes': ['info[(.*)][oper_status]',
                                                                      'info[(.*)][ipv4]']},
                                            'all_keys': True,
                                            'exclude': interface_exclude}},
                      config_info={'conf.acl.Acl':{
                                      'requirements':[['device_attr', '{uut}',
                                                       'acl_attr', ADD_ACL_NAME,
                                                       'acl_type', 'ipv4-acl-type'],
                                                      ['device_attr', '{uut}',
                                                       'acl_attr', ADD_ACL_NAME,
                                                       'ace_attr', '10',
                                                       'actions_forwarding', ACTION],
                                                      ['device_attr', '{uut}',
                                                       'acl_attr', ADD_ACL_NAME,
                                                       'ace_attr', '10',
                                                       'protocol', 'icmp'],
                                                      ['device_attr', '{uut}',
                                                       'acl_attr', ADD_ACL_NAME,
                                                       'ace_attr', '10',
                                                       'src', 'any'],
                                                      ['device_attr', '{uut}',
                                                       'acl_attr', ADD_ACL_NAME,
                                                       'ace_attr', '10',
                                                       'dst', 'any'],
                                                      ['device_attr', '{uut}',
                                                       'acl_attr', ADD_ACL_NAME,
                                                       'interface_attr', '(?P<intf>.*)',
                                                       'if_in', True]],
                                      'verify_conf':False,
                                      'kwargs':{}}},
                      verify_ops={'ops.acl.acl.Acl':{
                                      'requirements': [['info', 'acls', ADD_ACL_NAME, 'name', ADD_ACL_NAME],
                                                       ['info', 'acls', ADD_ACL_NAME, 'type', 'ipv4-acl-type'],
                                                       ['info', 'acls', ADD_ACL_NAME, 'aces', '10', 'name', '10'],
                                                       ['info', 'acls', ADD_ACL_NAME, 'aces', '10', 'actions',
                                                        'logging', 'log-none'],
                                                       ['info', 'acls', ADD_ACL_NAME, 'aces', '10', 'actions',
                                                        'forwarding', ACTION]],
                                      'kwargs':{'attributes':['info']},
                                      'exclude': acl_exclude},
                                  'ops.interface.interface.Interface':{
                                          'requirements':[['info', '(?P<intf>.*)',
                                                           'oper_status', 'up']],
                                          'kwargs': {'attributes': ['info[(.*)][oper_status]',
                                                                    'info[(.*)][ipv4]']},
                                          'exclude': interface_exclude}},
                      num_values={'intf':1})

