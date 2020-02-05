'''NXOS Implementation for Igmp add-remove triggers'''

# python
from functools import partial

# import pyats
from pyats import aetest
from pyats.utils.objects import Not, NotExists

# Genie Libs
from genie.libs.sdk.libs.utils.mapping import Mapping
from genie.libs.sdk.triggers.addremove.addremove import TriggerAddRemove
from genie.libs.sdk.libs.utils.triggeractions import configure_add_attributes
from genie.libs.conf.igmp.igmp_group import IgmpGroup


# Which key to exclude for Igmp Ops comparison
igmp_exclude = ['maker', 'elapsed_time', 'discontinuity_time',
           'keepalive', 'total', 'up_time', 'expire', 'remote',
           'last_message_received', 'num_of_comparison', 'rpf_failure',
           'total_accept_count', 'total_reject_count', 'notification']

# Which key to exclude for Interface Ops comparison
interface_exclude = ['maker', 'last_change','in_rate','in_rate_pkts',
                     'out_rate', 'out_rate_pkts', 'in_octets',
                     'in_pkts', 'in_unicast_pkts', 'out_octets',
                     'out_pkts', 'out_unicast_pkts', 'out_multicast_pkts',
                     'in_multicast_pkts', 'last_clear', 'in_broadcast_pkts',
                     'out_broadcast_pkts', 'bandwidth', 'load_interval',
                     'port_speed', 'in_crc_errors', 'in_discards',
                     'unnumbered', '(Tunnel.*)', 'accounting']
                     

class TriggerAddRemoveIgmpEnable(TriggerAddRemove):
    """Apply the Igmp interface enable, add remove added Igmp interface enable"""

    __description__ = """Apply the Igmp interface enable, add remove added Igmp interface enable.

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

                vrf: `str`
                interface: `str`

                (e.g) interface: '(?P<interface>Ethernet1*)' (Regex supported)
                      OR
                      interface: 'Ethernet1/1/1' (Specific value)

    steps:
        1. Learn Igmp Ops/Conf object and store the Igmp interface enable, learn Interface ops to 
           get interface with ip address and not same to the existing igmp interface.
        2. Save the current device configurations through "method" which user uses
        3. Add the configuration of interface as igmp originator-id with Igmp Conf object
        4. Verify the igmp interface enable from step 3 has configured
        5. Remove the igmp interface enable configurations.
        6. Recover the device configurations to the one in step 2
        7. Learn Igmp Ops again and verify it is the same as the Ops in step 1
    """

    @aetest.setup
    def verify_prerequisite(self, uut, abstract, steps, timeout):
        # learn existing igmp interfaces
        super().verify_prerequisite(uut, abstract, steps, timeout)
        igmp_keys = self.mapping.keys


        # learn interafce ops to get ipv4 up interfaces
        self.mapping.requirements = {}
        self.mapping.requirements['ops.interface.interface.Interface'] = \
            {'requirements':[['info', '(?P<interface>^(?!mgmt).*)', 'ipv4',
                              '(?P<ip>.*)', 'ip', '(?P<address>.*)'],
                             ['info', '(?P<interface>.*)', 'vrf',
                              '(?P<add_igmp_intf_vrf>.*)']],
            'all_keys': True,
            'kwargs':{'attributes': [
                'info[(.*)][ipv4][(.*)][ip]',
                'info[(.*)][vrf]']},
            'exclude': interface_exclude}
        super().verify_prerequisite(uut, abstract, steps, timeout)
        intf_keys = self.mapping.keys

        # find interface
        with steps.start("Extracting ipv4 interfaces "
          "which are not igmp interfaces") as step:

            add_keys = {}
            for item in intf_keys:
                if all(item['interface'] not in \
                    i['interface'] for i in igmp_keys):
                    # attach the add value to mapping keys
                    add_keys.update({'add_igmp_intf': item['interface'],
                                     'add_igmp_intf_vrf': item['add_igmp_intf_vrf']})
                    break

            if not add_keys:
                step.skipped('Could not find up ipv4 interface which is '
                    'not existed igmp interface')
                self.skipped('Could not find up ipv4 interface which is '
                    'not existed igmp interface', goto=['next_tc'])

        self.mapping.keys = [add_keys]

    # Mapping of Information between Ops and Conf
    # Also permit to dictate which key to verify
    mapping = Mapping(requirements={'ops.igmp.igmp.Igmp':{
                                          'requirements':[\
                                              ['info', 'vrfs', '(?P<vrf>.*)', 'interfaces',
                                               '(?P<interface>.*)']],
                                          'kwargs':{'attributes': [
                                              'info[vrfs][(.*)][interfaces]']},
                                          'exclude': igmp_exclude}},
                      config_info={'conf.igmp.Igmp':{
                                       'requirements':[
                                         ['device_attr', '{uut}', 'vrf_attr', '(?P<add_igmp_intf_vrf>.*)',
                                          'interface_attr', '(?P<add_igmp_intf>.*)', 'enable', True]],
                                       'verify_conf':False,
                                       'kwargs':{}}},
                      verify_ops={'ops.igmp.igmp.Igmp':{
                                          'requirements':[\
                                              ['info', 'vrfs', '(?P<add_igmp_intf_vrf>.*)', 'interfaces',
                                               '(?P<add_igmp_intf>.*)', 'enable', True]],
                                          'kwargs':{'attributes': ['info[vrfs][(.*)][interfaces]']},
                                          'exclude': igmp_exclude}},
                      num_values={'vrf': 'all', 'interface': 'all'})


class TriggerAddRemoveIgmpVersion(TriggerAddRemove):
    """Apply Igmp interface version, and remove added Igmp interface version"""

    __description__ = """Apply Igmp interface version, and remove added Igmp interface version.

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

                vrf: `str`
                interface: `str`

                (e.g) interface: '(?P<interface>Ethernet1*)' (Regex supported)
                      OR
                      interface: 'Ethernet1/1/1' (Specific value)
    steps:
        1. Learn Igmp Ops object and store the Igmp which interface version is default value.
        2. Save the current device configurations through "method" which user uses
        3. Add the configuration of igmp interface version with Igmp Conf object
        4. Verify the igmp interface version from step 3 has configured
        5. Remove the igmp interface version configurations.
        6. Recover the device configurations to the one in step 2
        7. Learn Igmp Ops again and verify it is the same as the Ops in step 1

    """
    ADD_VERSION = 3
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
                                          ADD_VERSION]],
                                       'verify_conf':False,
                                       'kwargs':{}}},
                      verify_ops={
                          'ops.igmp.igmp.Igmp':{
                                'requirements':[\
                                    ['info', 'vrfs', '(?P<vrf>.*)', 'interfaces',
                                     '(?P<interface>.*)', 'version', ADD_VERSION]],
                                'kwargs':{'attributes': [
                                    'info[vrfs][(.*)]']},
                                'exclude': igmp_exclude}},
                      num_values={'vrf': 1, 'interface': 1})


class TriggerAddRemoveIgmpJoinGroup(TriggerAddRemove):
    """Apply the Igmp interface join-group, and remove added Igmp interface join-group"""

    __description__ = """Apply the Igmp peer(s) sa-filter out, and
    remove added Igmp peer(s) sa-filter out.

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
            add_igmp_group: Trigger yaml file customized add imgp join-group.               
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

                vrf: `str`
                join_group: `str`
                group: `str`
                interface: `str`

                (e.g) interface: '(?P<interface>Ethernet1*)' (Regex supported)
                      OR
                      interface: 'Ethernet1/1/1' (Specific value)
    steps:
        1. Learn Igmp Ops object and store the Igmp interface(s) which does not have added join-group.
        2. Save the current device configurations through "method" which user uses
        3. Add the configuration of igmp interface join-group with Igmp Conf object
        4. Verify the igmp interface join-group from step 3 has configured
        5. Remove the igmp interface join-group configurations.
        6. Recover the device configurations to the one in step 2
        7. Learn Igmp Ops again and verify it is the same as the Ops in step 1

    """
    ADD_JOIN_GROUP = '234.1.1.2 *'

    @aetest.setup
    def verify_prerequisite(self, uut, abstract, steps, timeout, add_igmp_group=None):

        self.timeout = timeout

        try:
            self.pre_snap = self.mapping.learn_ops(device=uut,
                                                   abstract=abstract,
                                                   steps=steps,
                                                   timeout=timeout)
        except Exception as e:
            self.errored("Section failed due to: '{e}'".format(e=e))

        # nothing in the static groups,
        # then learn if any groups to have some vrf interface value
        if any(not item for item in self.mapping.keys):
            self.mapping.requirements['ops.igmp.igmp.Igmp']['requirements'] = \
              [['info', 'vrfs', '(?P<vrf>.*)', 'interfaces',
               '(?P<interface>.*)', 'group', '(?P<group>.*)', '(?P<dummy>.*)']] # incase there is nothing learned

            try:
                self.pre_snap = self.mapping.learn_ops(device=uut,
                                                       abstract=abstract,
                                                       steps=steps,
                                                       timeout=timeout)
            except Exception as e:
                self.errored("Section failed due to: '{e}'".format(e=e))

            if any(not item for item in self.mapping.keys):
                self.skipped('Cannot learn the feature', goto=['next_tc'])

        with steps.start("Check if added group %s not in the "
          "existing groups" % self.ADD_JOIN_GROUP) as step:

            # learn igmp ops to have existing igmp interfaces
            if any(self.ADD_JOIN_GROUP in \
                item.get('join_group', '') for item in self.mapping.keys):
                if add_igmp_group:
                    self.ADD_JOIN_GROUP = add_igmp_group
                else:
                    self.skipped('Could not find join_group does not '
                      'include the added group %s' % self.ADD_JOIN_GROUP, goto=['next_tc'])

            # attach the add value to mapping keys
            [item.update({'add_igmp_group': self.ADD_JOIN_GROUP.split()[0],
                          'add_igmp_source': self.ADD_JOIN_GROUP.split()[1],
                          'add_igmp_group_key': self.ADD_JOIN_GROUP}) for item in self.mapping.keys]

            step.passed('Will add group %s' % self.ADD_JOIN_GROUP)

    # Mapping of Information between Ops and Conf
    # Also permit to dictate which key to verify
    mapping = Mapping(requirements={
                          'ops.igmp.igmp.Igmp':{
                                'requirements':[\
                                    ['info', 'vrfs', '(?P<vrf>.*)', 'interfaces',
                                     '(?P<interface>.*)', 'join_group', '(?P<join_group>.*)',
                                     'group', '(?P<group>.*)']],
                                'all_keys': True,
                                'kwargs':{'attributes': [
                                    'info[vrfs][(.*)][interfaces][(.*)][join_group][(.*)]',
                                    'info[vrfs][(.*)][interfaces][(.*)][static_group][(.*)]',
                                    'info[vrfs][(.*)][interfaces][(.*)][group][(.*)]']},
                                'exclude': igmp_exclude}},
                      config_info={'conf.igmp.Igmp':{
                                       'requirements':[
                                         [partial(configure_add_attributes,  # callable configuration
                                            add_obj=IgmpGroup,
                                            base=[['device_attr', '{uut}', 'vrf_attr', '(?P<vrf>.*)',
                                                  'interface_attr', '(?P<interface>.*)']],
                                            add_attribute=[['join_group', '(?P<add_igmp_group>.*)'],
                                                           ['join_group_source_addr', '(?P<add_igmp_source>.*)'],],
                                            add_method='add_groups',
                                        )]],
                                       'verify_conf':False,
                                       'kwargs':{}}},
                      verify_ops={
                          'ops.igmp.igmp.Igmp':{
                                'requirements':[\
                                    ['info', 'vrfs', '(?P<vrf>.*)', 'interfaces',
                                     '(?P<interface>.*)', 'join_group', '(?P<add_igmp_group_key>.*)',
                                     'group', '(?P<add_igmp_group>.*)'],
                                    ['info', 'vrfs', '(?P<vrf>.*)', 'interfaces',
                                     '(?P<interface>.*)', 'join_group', '(?P<add_igmp_group_key>.*)',
                                     'source', '(?P<add_igmp_source>.*)'],
                                    ['info', 'vrfs', '(?P<vrf>.*)', 'interfaces',
                                     '(?P<interface>.*)', 'group', '(?P<add_igmp_group>.*)',
                                     'last_reporter', '([\w\.]+)']],
                                'kwargs':{'attributes': [
                                    'info[vrfs][(.*)][interfaces][(.*)][join_group][(.*)]',
                                    'info[vrfs][(.*)][interfaces][(.*)][static_group][(.*)]',
                                    'info[vrfs][(.*)][interfaces][(.*)][group][(.*)]']},
                                'exclude': igmp_exclude}},
                      num_values={'vrf': 1, 'interface': 1, 'join_group': 1, 'group': 1, 'source': 1})


class TriggerAddRemoveIgmpStaticGroup(TriggerAddRemove):
    """Apply the Igmp interface static-group, and remove added Igmp interface static-group"""

    __description__ = """Apply the Igmp interface static-group,
    and remove added Igmp interface static-group.

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

                vrf: `str`
                static_group: `str`
                group: `str`
                interface: `str`

                (e.g) interface: '(?P<interface>Ethernet1*)' (Regex supported)
                      OR
                      interface: 'Ethernet1/1/1' (Specific value)

    steps:
        1. Learn Igmp Ops object and store the Igmp interface(s) which does not have added static-group.
        2. Save the current device configurations through "method" which user uses
        3. Add the configuration of igmp interface static-group with Igmp Conf object
        4. Verify the igmp interface static-group from step 3 has configured
        5. Remove the igmp interface static-group configurations.
        6. Recover the device configurations to the one in step 2
        7. Learn Igmp Ops again and verify it is the same as the Ops in step 1

    """
    ADD_STATIC_GROUP = '234.1.1.2 *'

    @aetest.setup
    def verify_prerequisite(self, uut, abstract, steps, timeout, add_igmp_group=None):

        self.timeout = timeout

        try:
            self.pre_snap = self.mapping.learn_ops(device=uut,
                                                   abstract=abstract,
                                                   steps=steps,
                                                   timeout=timeout)
        except Exception as e:
            self.errored("Section failed due to: '{e}'".format(e=e))

        # nothing in the static groups,
        # then learn if any groups to have some vrf interface value
        if any(not item for item in self.mapping.keys):
            self.mapping.requirements['ops.igmp.igmp.Igmp']['requirements'] = \
              [['info', 'vrfs', '(?P<vrf>.*)', 'interfaces',
               '(?P<interface>.*)', 'group', '(?P<group>.*)', '(?P<dummy>.*)']] # incase there is nothing learned

            try:
                self.pre_snap = self.mapping.learn_ops(device=uut,
                                                       abstract=abstract,
                                                       steps=steps,
                                                       timeout=timeout)
            except Exception as e:
                self.errored("Section failed due to: '{e}'".format(e=e))

            if any(not item for item in self.mapping.keys):
                self.skipped('Cannot learn the feature', goto=['next_tc'])

        with steps.start("Check if added group %s not in the "
          "existing groups" % self.ADD_STATIC_GROUP) as step:
        
            # learn igmp ops to have existing igmp interfaces
            if any(self.ADD_STATIC_GROUP in \
                item.get('static_group', '') for item in self.mapping.keys):
                if add_igmp_group:
                    self.ADD_STATIC_GROUP = add_igmp_group
                else:
                    self.skipped('Could not find static_group does not '
                      'include the added group %s' % self.ADD_STATIC_GROUP, goto=['next_tc'])

            # attach the add value to mapping keys
            [item.update({'add_igmp_group': self.ADD_STATIC_GROUP.split()[0],
                          'add_igmp_source': self.ADD_STATIC_GROUP.split()[1],
                          'add_igmp_group_key': self.ADD_STATIC_GROUP}) for item in self.mapping.keys]

            step.passed('Will add group %s' % self.ADD_STATIC_GROUP)

    # Mapping of Information between Ops and Conf
    # Also permit to dictate which key to verify
    mapping = Mapping(requirements={
                          'ops.igmp.igmp.Igmp':{
                                'requirements':[\
                                    ['info', 'vrfs', '(?P<vrf>.*)', 'interfaces',
                                     '(?P<interface>.*)', 'static_group', '(?P<static_group>.*)',
                                     'group', '(?P<group>.*)']],
                                'all_keys': True,
                                'kwargs':{'attributes': [
                                    'info[vrfs][(.*)][interfaces][(.*)][join_group][(.*)]',
                                    'info[vrfs][(.*)][interfaces][(.*)][static_group][(.*)]',
                                    'info[vrfs][(.*)][interfaces][(.*)][group][(.*)]']},
                                'exclude': igmp_exclude}},
                      config_info={'conf.igmp.Igmp':{
                                       'requirements':[
                                         [partial(configure_add_attributes,  # callable configuration
                                            add_obj=IgmpGroup,
                                            base=[['device_attr', '{uut}', 'vrf_attr', '(?P<vrf>.*)',
                                                  'interface_attr', '(?P<interface>.*)']],
                                            add_attribute=[['static_group', '(?P<add_igmp_group>.*)'],
                                                           ['static_group_source_addr', '(?P<add_igmp_source>.*)'],],
                                            add_method='add_groups',
                                        )]],
                                       'verify_conf':False,
                                       'kwargs':{}}},
                      verify_ops={
                          'ops.igmp.igmp.Igmp':{
                                'requirements':[\
                                    ['info', 'vrfs', '(?P<vrf>.*)', 'interfaces',
                                     '(?P<interface>.*)', 'static_group', '(?P<add_igmp_group_key>.*)',
                                     'group', '(?P<add_igmp_group>.*)'],
                                    ['info', 'vrfs', '(?P<vrf>.*)', 'interfaces',
                                     '(?P<interface>.*)', 'static_group', '(?P<add_igmp_group_key>.*)',
                                     'source', '(?P<add_igmp_source>.*)'],
                                    ['info', 'vrfs', '(?P<vrf>.*)', 'interfaces',
                                     '(?P<interface>.*)', 'group', '(?P<add_igmp_group>.*)', 'last_reporter', '([\w\.]+)']],
                                'kwargs':{'attributes': [
                                    'info[vrfs][(.*)][interfaces][(.*)][join_group][(.*)]',
                                    'info[vrfs][(.*)][interfaces][(.*)][static_group][(.*)]',
                                    'info[vrfs][(.*)][interfaces][(.*)][group][(.*)]']},
                                'exclude': igmp_exclude}},
                      num_values={'vrf': 1, 'interface': 1, 'static_group': 1, 'group': 1, 'source': 1})
