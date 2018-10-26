'''NXOS Implementation for Mld add-remove triggers'''

# python
from functools import partial

# import ats
from ats import aetest
from ats.utils.objects import Not, NotExists

# Genie Libs
from genie.libs.sdk.libs.utils.mapping import Mapping
from genie.libs.sdk.triggers.addremove.addremove import TriggerAddRemove
from genie.libs.sdk.libs.utils.triggeractions import configure_add_attributes
from genie.libs.conf.mld.mld_group import MldGroup


# Which key to exclude for Mld Ops comparison
mld_exclude = ['maker', 'elapsed_time', 'discontinuity_time',
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
                     

class TriggerAddRemoveMldEnable(TriggerAddRemove):
    """Apply the Mld interface enable, add remove added Mld interface enable"""

    __description__ = """Apply the Mld interface enable, add remove added Mld interface enable.

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
        1. Learn Mld Ops/Conf object and store the Mld interface enable, learn Interface ops to 
           get interface with ip address and not same to the existing mld interface.
        2. Save the current device configurations through "method" which user uses
        3. Add the configuration of interface as mld originator-id with Mld Conf object
        4. Verify the mld interface enable from step 3 has configured
        5. Remove the mld interface enable configurations.
        6. Recover the device configurations to the one in step 2
        7. Learn Mld Ops again and verify it is the same as the Ops in step 1
    """

    @aetest.setup
    def verify_prerequisite(self, uut, abstract, steps, timeout):
        # learn existing mld interfaces
        super().verify_prerequisite(uut, abstract, steps, timeout)
        mld_keys = self.mapping.keys


        # learn interafce ops to get ipv6 up interfaces
        self.mapping.requirements = {}
        self.mapping.requirements['ops.interface.interface.Interface'] = \
            {'requirements':[['info', '(?P<mld_intf>^(?!mgmt).*)', 'ipv6',
                              '(?P<ip>.*)', 'ip', '(?P<address>.*)'],
                             ['info', '(?P<mld_intf>.*)', 'vrf',
                              '(?P<add_mld_intf_vrf>.*)']],
            'all_keys': True,
            'kwargs':{'attributes': [
                'info[(.*)][ipv6][(.*)][ip]',
                'info[(.*)][vrf]']},
            'exclude': interface_exclude}
        super().verify_prerequisite(uut, abstract, steps, timeout)
        intf_keys = self.mapping.keys

        # find interface
        with steps.start("Extracting ipv6 interfaces "
          "which are not igmp interfaces") as step:
            add_keys = {}
            for item in intf_keys:
                if all(item['mld_intf'] not in \
                    i['mld_intf'] for i in mld_keys):
                    # attach the add value to mapping keys
                    add_keys.update({'add_mld_intf': item['mld_intf'],
                                     'add_mld_intf_vrf': item['add_mld_intf_vrf']})
                    break

            if not add_keys:
                step.skipped('Could not find up ipv6 interface which is '
                    'not existed igmp interface')
                self.skipped('Could not find up ipv6 interface which is not '
                    'existed mld interface', goto=['next_tc'])

        self.mapping.keys = [add_keys]

    # Mapping of Information between Ops and Conf
    # Also permit to dictate which key to verify
    mapping = Mapping(requirements={'ops.mld.mld.Mld':{
                                          'requirements':[\
                                              ['info', 'vrfs', '(?P<vrf>.*)', 'interfaces',
                                               '(?P<mld_intf>.*)']],
                                          'kwargs':{'attributes': [
                                              'info[vrfs][(.*)][interfaces]']},
                                          'exclude': mld_exclude}},
                      config_info={'conf.mld.Mld':{
                                       'requirements':[
                                         ['device_attr', '{uut}', 'vrf_attr', '(?P<add_mld_intf_vrf>.*)',
                                          'interface_attr', '(?P<add_mld_intf>.*)', 'enable', True]],
                                       'verify_conf':False,
                                       'kwargs':{}}},
                      verify_ops={'ops.mld.mld.Mld':{
                                          'requirements':[\
                                              ['info', 'vrfs', '(?P<add_mld_intf_vrf>.*)', 'interfaces',
                                               '(?P<add_mld_intf>.*)', 'enable', True]],
                                          'kwargs':{'attributes': ['info[vrfs][(.*)][interfaces]']},
                                          'exclude': mld_exclude}},
                      num_values={'vrf': 'all', 'mld_intf': 'all'})


class TriggerAddRemoveMldVersion(TriggerAddRemove):
    """Apply Mld interface version, and remove added Mld interface version"""

    __description__ = """Apply Mld interface version, and remove added Mld interface version.

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
        1. Learn Mld Ops object and store the Mld which interface version is default value.
        2. Save the current device configurations through "method" which user uses
        3. Add the configuration of mld interface version with Mld Conf object
        4. Verify the mld interface version from step 3 has configured
        5. Remove the mld interface version configurations.
        6. Recover the device configurations to the one in step 2
        7. Learn Mld Ops again and verify it is the same as the Ops in step 1

    """
    ADD_VERSION = 1
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
                                          ADD_VERSION]],
                                       'verify_conf':False,
                                       'kwargs':{}}},
                      verify_ops={
                          'ops.mld.mld.Mld':{
                                'requirements':[\
                                    ['info', 'vrfs', '(?P<vrf>.*)', 'interfaces',
                                     '(?P<mld_intf>.*)', 'version', ADD_VERSION]],
                                'missing': False,
                                'kwargs':{'attributes': [
                                    'info[vrfs][(.*)]']},
                                'exclude': mld_exclude}},
                      num_values={'vrf': 1, 'mld_intf': 1})


class TriggerAddRemoveMldJoinGroup(TriggerAddRemove):
    """Apply the Mld interface join-group, and remove added Mld interface join-group"""

    __description__ = """Apply the Mld peer(s) sa-filter out, and
    remove added Mld peer(s) sa-filter out.

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
            add_mld_group: Trigger yaml file customized add imgp join-group.               
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
        1. Learn Mld Ops object and store the Mld interface(s) which does not have added join-group.
        2. Save the current device configurations through "method" which user uses
        3. Add the configuration of mld interface join-group with Mld Conf object
        4. Verify the mld interface join-group from step 3 has configured
        5. Remove the mld interface join-group configurations.
        6. Recover the device configurations to the one in step 2
        7. Learn Mld Ops again and verify it is the same as the Ops in step 1

    """
    ADD_JOIN_GROUP = 'fffe::9 *'

    @aetest.setup
    def verify_prerequisite(self, uut, abstract, steps, timeout, add_mld_group=None):

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
            self.mapping.requirements['ops.mld.mld.Mld']['requirements'] = \
              [['info', 'vrfs', '(?P<vrf>.*)', 'interfaces',
               '(?P<mld_intf>.*)', 'group', '(?P<group>.*)', '(?P<dummy>.*)']] # incase there is nothing learned

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

            # learn mld ops to have existing mld interfaces
            if any(self.ADD_JOIN_GROUP in \
                item.get('join_group', '') for item in self.mapping.keys):
                if add_mld_group:
                    self.ADD_JOIN_GROUP = add_mld_group
                else:
                    self.skipped('Could not find join_group does not '
                      'include the added group %s' % self.ADD_JOIN_GROUP, goto=['next_tc'])

            # attach the add value to mapping keys
            [item.update({'add_mld_group': self.ADD_JOIN_GROUP.split()[0],
                          'add_mld_source': self.ADD_JOIN_GROUP.split()[1],
                          'add_mld_group_key': self.ADD_JOIN_GROUP}) for item in self.mapping.keys]

            step.passed('Will add group %s' % self.ADD_JOIN_GROUP)

    # Mapping of Information between Ops and Conf
    # Also permit to dictate which key to verify
    mapping = Mapping(requirements={
                          'ops.mld.mld.Mld':{
                                'requirements':[\
                                    ['info', 'vrfs', '(?P<vrf>.*)', 'interfaces',
                                     '(?P<mld_intf>.*)', 'join_group', '(?P<join_group>.*)',
                                     'group', '(?P<group>.*)'],
                                    ['info', 'vrfs', '(?P<vrf>.*)', 'interfaces',
                                     '(?P<mld_intf>.*)', 'join_group', '(?P<join_group>.*)',
                                     'source', '(?P<source>\*)'],
                                    ['info', 'vrfs', '(?P<vrf>.*)', 'interfaces',
                                     '(?P<mld_intf>.*)', 'group', '(?P<group>.*)', '(?P<dummy>.*)'], # incase there is nothing learned
                                    ],
                                'all_keys': True,
                                'kwargs':{'attributes': [
                                    'info[vrfs][(.*)][interfaces][(.*)][join_group][(.*)]',
                                    'info[vrfs][(.*)][interfaces][(.*)][static_group][(.*)]',
                                    'info[vrfs][(.*)][interfaces][(.*)][group][(.*)]']},
                                'exclude': mld_exclude}},
                      config_info={'conf.mld.Mld':{
                                       'requirements':[
                                         [partial(configure_add_attributes,  # callable configuration
                                            add_obj=MldGroup,
                                            base=[['device_attr', '{uut}', 'vrf_attr', '(?P<vrf>.*)',
                                                  'interface_attr', '(?P<mld_intf>.*)']],
                                            add_attribute=[['join_group', '(?P<add_mld_group>.*)'],
                                                           ['join_group_source_addr', '(?P<add_mld_source>.*)'],],
                                            add_method='add_groups',
                                        )]],
                                       'verify_conf':False,
                                       'kwargs':{}}},
                      verify_ops={
                          'ops.mld.mld.Mld':{
                                'requirements':[\
                                    ['info', 'vrfs', '(?P<vrf>.*)', 'interfaces',
                                     '(?P<mld_intf>.*)', 'join_group', '(?P<add_mld_group_key>.*)',
                                     'group', '(?P<add_mld_group>.*)'],
                                    ['info', 'vrfs', '(?P<vrf>.*)', 'interfaces',
                                     '(?P<mld_intf>.*)', 'join_group', '(?P<add_mld_group_key>.*)',
                                     'source', '(?P<add_mld_source>.*)'],
                                    ['info', 'vrfs', '(?P<vrf>.*)', 'interfaces',
                                     '(?P<mld_intf>.*)', 'group', '(?P<add_mld_group>.*)', '(.*)']],
                                'kwargs':{'attributes': [
                                    'info[vrfs][(.*)][interfaces][(.*)][join_group][(.*)]',
                                    'info[vrfs][(.*)][interfaces][(.*)][static_group][(.*)]',
                                    'info[vrfs][(.*)][interfaces][(.*)][group][(.*)]']},
                                'exclude': mld_exclude}},
                      num_values={'vrf': 1, 'mld_intf': 1, 'join_group': 1, 'group': 1, 'source': 1})


class TriggerAddRemoveMldStaticGroup(TriggerAddRemove):
    """Apply the Mld interface static-group, and remove added Mld interface static-group"""

    __description__ = """Apply the Mld interface static-group,
    and remove added Mld interface static-group.

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
        1. Learn Mld Ops object and store the Mld interface(s) which does not have added static-group.
        2. Save the current device configurations through "method" which user uses
        3. Add the configuration of mld interface static-group with Mld Conf object
        4. Verify the mld interface static-group from step 3 has configured
        5. Remove the mld interface static-group configurations.
        6. Recover the device configurations to the one in step 2
        7. Learn Mld Ops again and verify it is the same as the Ops in step 1

    """
    ADD_STATIC_GROUP = 'fffe::9 *'

    @aetest.setup
    def verify_prerequisite(self, uut, abstract, steps, timeout, add_mld_group=None):

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
            self.mapping.requirements['ops.mld.mld.Mld']['requirements'] = \
              [['info', 'vrfs', '(?P<vrf>.*)', 'interfaces',
               '(?P<mld_intf>.*)', 'group', '(?P<group>.*)', '(?P<dummy>.*)']] # incase there is nothing learned

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

            # learn mld ops to have existing mld interfaces
            if any(self.ADD_STATIC_GROUP in \
                item.get('static_group', '') for item in self.mapping.keys):
                if add_mld_group:
                    self.ADD_STATIC_GROUP = add_mld_group
                else:
                    self.skipped('Could not find static_group does not '
                      'include the added group %s' % self.ADD_STATIC_GROUP, goto=['next_tc'])

            # attach the add value to mapping keys
            [item.update({'add_mld_group': self.ADD_STATIC_GROUP.split()[0],
                          'add_mld_source': self.ADD_STATIC_GROUP.split()[1],
                          'add_mld_group_key': self.ADD_STATIC_GROUP}) for item in self.mapping.keys]

            step.passed('Will add group %s' % self.ADD_STATIC_GROUP)

    # Mapping of Information between Ops and Conf
    # Also permit to dictate which key to verify
    mapping = Mapping(requirements={
                          'ops.mld.mld.Mld':{
                                'requirements':[\
                                    ['info', 'vrfs', '(?P<vrf>.*)', 'interfaces',
                                     '(?P<mld_intf>.*)', 'static_group', '(?P<static_group>.*)',
                                     'group', '(?P<group>.*)']],
                                'kwargs':{'attributes': [
                                    'info[vrfs][(.*)][interfaces][(.*)][join_group][(.*)]',
                                    'info[vrfs][(.*)][interfaces][(.*)][static_group][(.*)]',
                                    'info[vrfs][(.*)][interfaces][(.*)][group][(.*)]']},
                                'exclude': mld_exclude}},
                      config_info={'conf.mld.Mld':{
                                       'requirements':[
                                         [partial(configure_add_attributes,  # callable configuration
                                            add_obj=MldGroup,
                                            base=[['device_attr', '{uut}', 'vrf_attr', '(?P<vrf>.*)',
                                                  'interface_attr', '(?P<mld_intf>.*)']],
                                            add_attribute=[['static_group', '(?P<add_mld_group>.*)'],
                                                           ['static_group_source_addr', '(?P<add_mld_source>.*)'],],
                                            add_method='add_groups',
                                        )]],
                                       'verify_conf':False,
                                       'kwargs':{}}},
                      verify_ops={
                          'ops.mld.mld.Mld':{
                                'requirements':[\
                                    ['info', 'vrfs', '(?P<vrf>.*)', 'interfaces',
                                     '(?P<mld_intf>.*)', 'static_group', '(?P<add_mld_group_key>.*)',
                                     'group', '(?P<add_mld_group>.*)'],
                                    ['info', 'vrfs', '(?P<vrf>.*)', 'interfaces',
                                     '(?P<mld_intf>.*)', 'static_group', '(?P<add_mld_group_key>.*)',
                                     'source', '(?P<add_mld_source>.*)'],
                                    ['info', 'vrfs', '(?P<vrf>.*)', 'interfaces',
                                     '(?P<mld_intf>.*)', 'group', '(?P<add_mld_group>.*)', '(.*)']],
                                'kwargs':{'attributes': [
                                    'info[vrfs][(.*)][interfaces][(.*)][join_group][(.*)]',
                                    'info[vrfs][(.*)][interfaces][(.*)][static_group][(.*)]',
                                    'info[vrfs][(.*)][interfaces][(.*)][group][(.*)]']},
                                'exclude': mld_exclude}},
                      num_values={'vrf': 1, 'mld_intf': 1, 'static_group': 1, 'group': 1, 'source': 1})
