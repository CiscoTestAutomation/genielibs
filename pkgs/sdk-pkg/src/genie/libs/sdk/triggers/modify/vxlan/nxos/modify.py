'''Implementation for vxlan modify triggers'''

import socket, struct
import logging
import re

# Genie Libs
from genie.libs.sdk.libs.utils.mapping import Mapping
from genie.libs.sdk.triggers.modify.modify import TriggerModify
from genie.libs.sdk.libs.utils.triggeractions import Configure

from functools import partial
from genie.libs.conf.base import IPv4Address
from pyats import aetest

# Which key to exclude for VXLAN Ops comparison
vxlan_exclude = ['maker', 'uptime','up_time']
interface_exclude = ['maker', 'last_change','in_rate','in_rate_pkts',
                     'out_rate', 'out_rate_pkts', 'in_octets',
                     'in_pkts', 'in_unicast_pkts', 'out_octets',
                     'out_pkts', 'out_unicast_pkts', 'out_multicast_pkts',
                     'in_multicast_pkts', 'last_clear', 'in_broadcast_pkts',
                     'out_broadcast_pkts']

multisite_exclude = ['multisite_bgw_if', 'multisite_bgw_if_admin_state',
                     'multisite_bgw_if_ip', 'multisite_bgw_if_oper_state',
                     'multisite_bgw_if_oper_state_down_reason', 'vip_rmac_ro']

vxlan_base_exclude = ['maker','uptime','up_time']
log = logging.getLogger(__name__)

class TriggerModifyNveMultisiteBgwInterface(TriggerModify):
    """Modify and revert the multisite bgw interface dynamically learned vxlan(s)."""

    __description__ = """Modify and revert the  multisite bgw interface dynamically learned vxlan(s).

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

                nve_name: `str`
                source_if: `str`
                nve_vni: `int`
                multisite_bgw_if: `str`

                (e.g) interface: '(?P<interface>Ethernet1*)' (Regex supported)
                      OR
                      interface: 'Ethernet1/1/1' (Specific value)

    steps:
        1. Learn Vxlan Ops object and store the vni state which is active and has source interface
            and multisite bgw interface. SKIP the trigger if there is no VXLAN(s) found
        2. Save the current device configurations through "method" which user uses
        3. Modify the multisite bgw interface of the learned VXLAN from step 1 with Interface Conf object
        4. Verify the multisite bgw interface of the learned VXLAN group(s) from step 3
           changes to the modified value in step 3.
        5. Recover the device configurations to the one in step 2
        6. Learn VXLAN Ops again and verify it is the same as the Ops in step 1

    """

    # configuration steps callable
    # adding new value for multisite bgw interface
    def configure_multisite_bgw_interface(self, conf_obj, **kwargs):
        ret = ""
        for key in self.keys:
            if  key['intf_name']!= key['source_if'] \
                    and key['intf_name'] != key['multisite_bgw_if']:
                ret = key['intf_name']
        if ret:
            self.keys[0]['multisite_bgw_intf'] = ret
            conf_obj.nve_multisite_bgw_intf = ret
            conf_obj.build_config()
        else:
            self.failed('Failed to find the '
                        'attribute', from_exception=self.keys)

        @aetest.test
        def verify_configuration(self, uut, abstract, steps):
            # modify self.keys to modify the multisite bgw interface value
            for item in self.mapping.keys:
                try:
                    ret = item['multisite_bgw_intf']
                    req = ['nve', '(?P<nve_name>.*)', 'multisite_bgw_if']
                    req.insert(len(req), ret)
                    self.mapping._verify_ops_dict['ops.vxlan.vxlan.Vxlan']['requirements'].append(req)
                    log.info("\n\nVerifying the following requirements: {req}".format(req=req))
                except Exception as e:
                    self.failed('Failed to verify the '
                                'added feature', from_exception=e)

            super().verify_configuration(uut, abstract, steps)

    mapping = Mapping(requirements={'ops.vxlan.vxlan.Vxlan': {
                                        'requirements': [['nve', '(?P<nve_name>.*)', 'source_if', '(?P<source_if>.*)'],
                                                         ['nve', '(?P<nve_name>.*)', 'multisite_bgw_if', '(?P<multisite_bgw_if>.*)'],
                                                         ['nve', '(?P<nve_name>.*)', 'vni', '(?P<nve_vni>.*)', 'vni_state', 'up']],
                                        'all_keys': True,
                                        'kwargs': {'attributes': ['nve[(.*)][vni][(.*)]',
                                                                  'nve[(.*)][source_if]',
                                                                  'nve[(.*)][multisite_bgw_if]','l2route']},
                                        'exclude': vxlan_exclude +['peer_id','tx_id']},
                                    'ops.interface.interface.Interface': {
                                        'requirements': [['info', '(?P<intf_name>(L|l)oopback.*)', 'oper_status', 'up']],
                                        'kwargs': {'attributes': ['info']},
                                        'exclude': interface_exclude + vxlan_base_exclude}},
                    config_info={'conf.interface.Interface': {
                                        'requirements': [[partial(configure_multisite_bgw_interface, \
                                                                  nve_multisite_bgw_intf='(?P<source_if>.*)')]],
                                        'verify_conf': False,
                                        'kwargs': {'mandatory': {'name': '(?P<nve_name>.*)', 'attach': False}}}},
                    verify_ops={'ops.vxlan.vxlan.Vxlan': {
                                        'requirements': [['nve', '(?P<nve_name>.*)', 'vni', '(?P<nve_vni>.*)', 'vni_state', 'down']],
                                        'kwargs': {'attributes': ['nve[(.*)][vni][(.*)]',
                                                                  'nve[(.*)][source_if]',
                                                                  'nve[(.*)][multisite_bgw_if]','l2route']},
                                        'exclude': vxlan_exclude + multisite_exclude +['l2route', 'repl_ip']}},
                    num_values={'nve_name': 'all', 'source_if': 'all', 'intf_name': 'all'})


class TriggerModifyNveVniMcastGroup(TriggerModify):
    """Modify and revert the mcast group dynamically learned vxlan(s)."""

    __description__ = """Modify and revert the mcast group dynamically learned vxlan(s).

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

                nve_name: `str`
                nve_vni: `int`
                mcast: `str`

                (e.g) interface: '(?P<interface>Ethernet1*)' (Regex supported)
                      OR
                      interface: 'Ethernet1/1/1' (Specific value)
        steps:
            1. Learn Vxlan Ops object and store the vni state which is active.
                SKIP the trigger if there is no VXLAN(s) found
            2. Save the current device configurations through "method" which user uses
            3. Modify the mcast group of the learned VXLAN from step 1 with Interface Conf object
            4. Verify the mcast group of the learned VXLAN(s) from step 3
               changes to the modified value in step 3.
            5. Recover the device configurations to the one in step 2
            6. Learn VXLAN Ops again and verify it is the same as the Ops in step 1
    """

    # configuration steps callable
    # adding new value for mcast group
    def configure_mcast_group(self, conf_obj, **kwargs):
        for x in self.__dict__['keys']:
            # supporting python 3.6
            try:
                mcast_group = x['mcast']
                mcast_group_value = struct.unpack('>L',socket.inet_aton(mcast_group))[0]+1
            except Exception as e:
                mcast_group = IPv4Address(x['mcast'])
                mcast_group_value = mcast_group.__dict__['_ip']+1
        t = struct.pack("!L", mcast_group_value)
        new_mcast_group = socket.inet_ntoa(t)
        self.keys[0]['mcast'] = new_mcast_group
        conf_obj.nve_vni_mcast_group = new_mcast_group
        conf_obj.build_config()


    @aetest.test
    def verify_modification(self, uut, abstract, steps):
        # modify self.keys to modify the mcast group value
        for item in self.mapping.keys:
            try:
                ret = item['mcast']
                req = ['nve', '(?P<nve_name>.*)', 'vni', '(?P<nve_vni>.*)', 'mcast']
                req.insert(len(req),ret)
                self.mapping._verify_ops_dict['ops.vxlan.vxlan.Vxlan']['requirements'].append(req)
            except Exception as e:
                log.warning('Cannot modify mcast group information.'
                            'Mismatch is expected {}'.format(e))

        super().verify_modification(uut, abstract, steps)

    # Mapping of Information between Ops and Conf
    # Also permit to dictates which key to verify
    mapping = Mapping(requirements={'ops.vxlan.vxlan.Vxlan':{
                                          'requirements':[['nve','(?P<nve_name>.*)','vni','(?P<nve_vni>.*)','mcast','(?P<mcast>[\d+\.\d+\.\d+\.\d+].*)'],
                                                          ['nve','(?P<nve_name>.*)','vni','(?P<nve_vni>.*)','vni_state','up']],
                                          'kwargs':{'attributes':['nve[(.*)][vni][(.*)][mcast]',
                                                                  'nve[(.*)][vni][(.*)][vni_state]']},
                                          'all_keys': True,
                                          'exclude': vxlan_base_exclude}},
                      config_info={'conf.interface.Interface': {
                                     'requirements':[[partial(configure_mcast_group, mcast='(?P<mcast>.*)')]],
                                     'verify_conf':False,
                                     'kwargs': {'mandatory': {'name': '(?P<nve_name>.*)',
                                                              'nve_vni': '(?P<nve_vni>.*)',
                                                              'nve_vni_associate_vrf': False,
                                                              'attach': False}}}},
                      verify_ops={'ops.vxlan.vxlan.Vxlan':{
                                    'requirements':[['nve', '(?P<nve_name>.*)', 'vni', '(?P<nve_vni>.*)', 'vni_state', 'up']],
                                    'kwargs':{'attributes':['nve[(.*)][vni][(.*)][mcast]',
                                                            'nve[(.*)][vni][(.*)][vni_state]']},
                                    'exclude': vxlan_base_exclude}},
                      num_values={'nve_name':1 ,'nve_vni':1})

class TriggerModifyEvpnMsiteBgwDelayRestoreTime(TriggerModify):
    """Modify and revert the msite bgw delay restore time dynamically learned vxlan(s)."""

    __description__ = """Modify and revert the multisite bgw delay restore time dynamically learned vxlan(s).

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

                    nve_name: `str`
                    evpn_multisite_border_gateway: `int`
                    multisite_convergence_time: `int`

                    (e.g) interface: '(?P<interface>Ethernet1*)' (Regex supported)
                          OR
                          interface: 'Ethernet1/1/1' (Specific value)
        steps:
            1. Learn Vxlan Ops object and store the the multisite bgw delay restore time.
                SKIP the trigger if there is no VXLAN(s) found
            2. Save the current device configurations through "method" which user uses
            3. Modify the multisite bgw delay restore time of the learned VXLAN from step 1
                 with Vxlan Conf object
            4. Verify the multisite bgw delay restore time of the learned VXLAN(s) from step 3
                changes to the modified value in step 3.
            5. Recover the device configurations to the one in step 2
            6. Learn VXLAN Ops again and verify it is the same as the Ops in step 1
    """
    mapping = Mapping(requirements={'ops.vxlan.vxlan.Vxlan': {
                                        'requirements': [[['nve', 'evpn_multisite_border_gateway', '(?P<evpn_multisite_border_gateway>.*)']],
                                                         [['nve','(?P<nve_name>.*)', 'multisite_convergence_time',
                                                          '(?P<multisite_convergence_time>.*)']]],
                                        'kwargs': {'attributes': ['nve[(.*)][multisite_convergence_time]',
                                                                  'nve[(.*)][vni][(.*)]',
                                                                  'nve[evpn_multisite_border_gateway]']},
                                        'exclude': vxlan_base_exclude}},
                    config_info={'conf.vxlan.Vxlan': {
                                        'requirements': [['device_attr', '{uut}', 'evpn_msite_attr', '(?P<evpn_multisite_border_gateway>.*)',\
                                                          'evpn_msite_bgw_delay_restore_time', 101]],
                                        'verify_conf': False,
                                        'kwargs': {}}},
                    verify_ops={'ops.vxlan.vxlan.Vxlan': {
                                        'requirements': [['nve', 'evpn_multisite_border_gateway', '(?P<evpn_multisite_border_gateway>.*)'],
                                                         ['nve', '(?P<nve_name>.*)', 'multisite_convergence_time', 101]],
                                        'kwargs': {'attributes': ['nve[(.*)][multisite_convergence_time]',
                                                                  'nve[(.*)][vni][(.*)]',
                                                                  'nve[evpn_multisite_border_gateway]']},
                                        'exclude': vxlan_base_exclude}},
                    num_values={'nve_name': 'all' , 'evpn_multisite_border_gateway':'all', 'delay_time':'all' })

class TriggerModifyNveSourceInterfaceLoopback(TriggerModify):
    """Modify and revert nve source interface dynamically learned Vxlan(s)."""

    __description__ = """Unconfigure nve source interface and reapply the whole configurations of dynamically learned Vxlan(s).

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
                 source_if: `str`
                 multisite_bgw_if: `str`

                (e.g) interface: '(?P<interface>Ethernet1*)' (Regex supported)
                      OR
                      interface: 'Ethernet1/1/1' (Specific value)
       steps:
         1. Learn Vxlan Ops object and store the nve source interface under nve
            if has any, otherwise, SKIP the trigger
         2. Save the current device configurations through "method" which user uses
         3. Unconfigure the nve source interface with Interface Conf object
         4. Verify the nve source interface from step 3 are no longer existed
         5. Recover the device configurations to the one in step 2
         6. Learn Vxlan Ops again and verify it is the same as the Ops in step 1
       """


    @aetest.test
    def modify_configuration(self, uut, abstract, steps):
        new_source_if = ""
        values = "(?P<intf_name>.*)\n"\
                 "(?P<source_if>.*)\n"\
                 "(?P<multisite_bgw_if>.*)"

        found_values = re.findall(r'\S+|\n', values)

        req_values = self.mapping._path_population([found_values], uut)
        for key in req_values:
            # new source interface must be different with multisite bgw_if
            if key[0] != key[2] and key[0] != key[4]:
                new_source_if = key[0]
                self.__dict__['new_source_if'] = new_source_if
                break
        if new_source_if:
            cmd = "interface (?P<nve_name>.*)\n" \
                  " shutdown\n" \
                  " source-interface %s\n" \
                  " no shutdown" %new_source_if
            x = re.findall(r'\S+|\n', cmd)
            req = self.mapping._path_population([x], uut)
            req_str = []
            for item in req[0]:
                req_str.append(str(item))

            cmd = ' '.join(req_str)
            try:
                uut.configure(cmd)
            except Exception as e:
                self.failed("Unable to configure: '{c}'".format(c=cmd),
                            from_exception=e)
        else:
            # new source interface must be different with multisite bgw_if
            self.failed("Not found any 'up' loopback and different with multisite bgw_if")

    @aetest.test
    def verify_modification(self, uut, abstract, steps):
        try:
            ret = self.__dict__['new_source_if']
            req = ['nve', '(?P<nve_name>.*)', 'source_if']
            req.insert(len(req), ret)
            self.mapping._verify_ops_dict['ops.vxlan.vxlan.Vxlan']['requirements'].append(req)
            log.info("\n\nVerifying the following requirements: {req}".format(req=req))
        except Exception as e:
            log.warning('Cannot verify source_if information.'
                        'Mismatch is expected {}'.format(e))

        super().verify_modification(uut, abstract, steps)


    @aetest.test
    def restore_configuration(self, uut, method, abstract):
        """exceptional rollback"""
        try:
            cmd = "interface (?P<nve_name>.*)\n" \
                  " shutdown\n" \
                  " source-interface (?P<source_if>.*)\n" \
                  " no shutdown"
            x = re.findall(r'\S+|\n', cmd)
            req = self.mapping._path_population([x], uut)
            req_str = []
            for item in req[0]:
                req_str.append(str(item))

            cmd = ' '.join(req_str)
            try:
                uut.configure(cmd)
            except Exception as e:
                self.failed("Unable to configure: '{c}'".format(c=cmd),
                            from_exception=e)
        except Exception as e:
            self.failed('Failed to restore the configuration', from_exception=e)

    mapping = Mapping(requirements={'ops.vxlan.vxlan.Vxlan':{
                                            'requirements': [['nve', '(?P<nve_name>.*)', 'source_if', '(?P<source_if>.*)'],
                                                             ['nve', '(?P<nve_name>.*)', 'src_if_state', 'up'],
                                                             ['nve', '(?P<nve_name>.*)', 'multisite_bgw_if', '(?P<multisite_bgw_if>.*)']],
                                            'all_keys': True,
                                            'kwargs': {'attributes': ['nve']},
                                            'exclude': vxlan_exclude},
                                    'ops.interface.interface.Interface':{
                                            'requirements': [['info', '(?P<intf_name>(L|l)oopback.*)', 'oper_status', 'up']],
                                            'kwargs': {'attributes': ['info']},
                                            'all_keys': True,
                                            'exclude': interface_exclude + vxlan_base_exclude}},
                        config_info={'conf.interface.Interface': {
                                            'requirements': [],
                                            'verify_conf': False,
                                            'kwargs': {'mandatory': {'name': '(?P<nve_name>.*)', 'attach': False}}}},
                        verify_ops={'ops.vxlan.vxlan.Vxlan': {
                                            'requirements': [['nve', '(?P<nve_name>.*)', 'vni', '(?P<vni>.*)', 'vni_state', 'down'],
                                                             ['nve', '(?P<nve_name>.*)', 'if_state', 'down'],
                                                             ['nve', '(?P<nve_name>.*)', 'multisite_bgw_if_oper_state', 'down'],
                                                             ['nve', '(?P<nve_name>.*)', 'multisite_bgw_if_oper_state_down_reason', 'NVE not up.'],
                                                             ['nve', 'vni', 'summary', 'cp_vni_up', 0]],
                                            'kwargs': {'attributes': ['nve']},
                                            'exclude': vxlan_exclude + ['primary_ip','scondary_ip','vip_rmac',\
                                                                        'ethernet_segment','cp_vni_down','sm_state']}},
                        num_values={'nve_name':1, 'source_if': 1, 'intf_name':'all', 'multisite_bgw_if':1 })


class TriggerModifyEvpnRd(TriggerModify):
    """Modify and revert the rd under evpn vni that dynamically learned vxlan(s)."""

    __description__ = """Modify and revert the rd under evpn vni dynamically learned vxlan(s).

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

                     instance: `str`
                     vrf: `str`
                     address_family: `str`
                     rd: `str`
                     rd_vniid: `str`

                    (e.g) interface: '(?P<interface>Ethernet1*)' (Regex supported)
                          OR
                          interface: 'Ethernet1/1/1' (Specific value)
        steps:
            1. Learn Vxlan Ops object and store the rd and it's vni  .
                SKIP the trigger if there is no VXLAN(s) found
            2. Save the current device configurations through "method" which user uses
            3. Modify the rd of the learned VXLAN from step 1 with Vxlan Conf object
            4. Verify the rd of the learned VXLAN(s) from step 3
               changes to the modified value in step 3.
            5. Recover the device configurations to the one in step 2
            6. Learn VXLAN Ops again and verify it is the same as the Ops in step 1
    """

    # configuration steps callable
    # adding new value for rd
    def configure_rd(self, conf_obj, path, **kwargs):
        paths = self._path_population([path], kwargs['device'])

        for path in paths:
            rd_index = int(path.index('evpn_vni_rd'))
            rd_attr_val = path[rd_index+1]

            new_rd_scond_portion = int(rd_attr_val.split(':')[1]) + 1
            new_rd = "{}:{}".format(rd_attr_val.split(':')[0], new_rd_scond_portion)
            self.keys[0]['new_rd'] = new_rd
            path[-1] = new_rd

        log.info('With following configuration:\n{c}'
                 .format(c=paths))
        Configure.conf_configure(device=kwargs['device'],
                                 conf=conf_obj,
                                 conf_structure=paths,
                                 unconfig=False)

    @aetest.test
    def verify_modification(self, uut, abstract, steps):
        for item in self.mapping.keys:
            try:
                ret = item['new_rd']
                req = ['bgp_l2vpn_evpn', 'instance', '(?P<instance>.*)',
                               'vrf', '(?P<vrf>.*)', 'address_family',
                               '(?P<address_family>.*)', 'rd', ret,'rd']
                req.insert(len(req),ret)
                req_2 = ['bgp_l2vpn_evpn', 'instance', '(?P<instance>.*)',
                                                           'vrf', '(?P<vrf>.*)', 'address_family',
                                                           '(?P<address_family>.*)', 'rd', ret, 'rd_vniid', '(?P<rd_vniid>.*)']
                self.mapping._verify_ops_dict['ops.vxlan.vxlan.Vxlan']['requirements'].append(req)
                self.mapping._verify_ops_dict['ops.vxlan.vxlan.Vxlan']['requirements'].append(req_2)
            except Exception as e:
                log.warning('Cannot verify rd information.'
                            'Mismatch is expected {}'.format(e))

        super().verify_modification(uut, abstract, steps)

    # Mapping of Information between Ops and Conf
    # Also permit to dictates which key to verify
    mapping = Mapping(requirements={'ops.vxlan.vxlan.Vxlan':{
                                          'requirements':[['bgp_l2vpn_evpn', 'instance', '(?P<instance>.*)',
                                                           'vrf', '(?P<vrf>.*)', 'address_family',
                                                           '(?P<address_family>.*)', 'rd', '(?P<rd>.*)','rd','(?P<rd>.*)'],
                                                          ['bgp_l2vpn_evpn', 'instance', '(?P<instance>.*)',
                                                           'vrf', '(?P<vrf>.*)', 'address_family',
                                                           '(?P<address_family>.*)', 'rd', '(?P<rd>.*)', 'rd_vniid', '(?P<rd_vniid>.*)'],
                                                          ['bgp_l2vpn_evpn', 'instance', '(?P<instance>.*)',
                                                            'vrf', '(?P<vrf>.*)', 'address_family',
                                                            '(?P<address_family>.*)', 'rd', '(?P<rd>.*)', 'rd_vrf', 'l2']],
                                          'kwargs':{'attributes':['bgp_l2vpn_evpn[instance][(.*)][vrf][(.*)][address_family][(.*)][rd][(.*)][rd]',
                                                                  'bgp_l2vpn_evpn[instance][(.*)][vrf][(.*)][address_family][(.*)][rd][(.*)][rd_vniid]',
                                                                  'bgp_l2vpn_evpn[instance][(.*)][vrf][(.*)][address_family][(.*)][rd][(.*)][rd_vrf]',
                                                                  ]},
                                          'all_keys':True,
                                          'exclude': vxlan_exclude}},
                      config_info={'conf.vxlan.Vxlan': {
                                         'requirements':[[partial(configure_rd, path=['device_attr', '{uut}', 'evpn_attr',
                                                          '*', 'vni_attr', '(?P<rd_vniid>.*)',
                                                          'evpn_vni_rd', '(?P<rd>.*)'])]],
                                         'verify_conf':False,
                                         'kwargs': {}}},
                      verify_ops={'ops.vxlan.vxlan.Vxlan':{
                                        'requirements':[],
                                        'kwargs':{'attributes':['bgp_l2vpn_evpn[instance][(.*)][vrf][(.*)][address_family][(.*)][rd][(.*)][rd]',
                                                                'bgp_l2vpn_evpn[instance][(.*)][vrf][(.*)][address_family][(.*)][rd][(.*)][rd_vniid]',
                                                                'bgp_l2vpn_evpn[instance][(.*)][vrf][(.*)][address_family][(.*)][rd][(.*)][rd_vrf]']},
                                        'exclude': vxlan_exclude}},
                      num_values={'rd': 1, 'instance':1, 'vrf':1, 'address_family':1, 'rd_vniid':1})
