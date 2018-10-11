
# import python
from abc import ABC

# import genie
from genie.conf.base.config import CliConfig
from genie.conf.base.cli import CliConfigBuilder
from genie.conf.base.attributes import UnsupportedAttributeWarning, \
                                       AttributesHelper


class Stp(ABC):

    class DeviceAttributes(ABC):

        def build_config(self, apply=True, attributes=None, unconfig=False,
                         **kwargs):
            assert not kwargs, kwargs
            attributes = AttributesHelper(self, attributes)
            configurations = CliConfigBuilder(unconfig=unconfig)
            
            # spanning-tree bridge assurance
            if attributes.value('bridge_assurance'):
                configurations.append_line(
                    attributes.format('spanning-tree bridge assurance'))
            
            # spanning-tree etherchannel guard misconfig
            if attributes.value('etherchannel_misconfig_guard'):
                configurations.append_line(
                    attributes.format('spanning-tree etherchannel guard misconfig'))
            
            # errdisable recovery interval <bpduguard_timeout_recovery>
            if attributes.value('bpduguard_timeout_recovery'):
                configurations.append_line(
                    attributes.format('errdisable recovery '
                        'interval {bpduguard_timeout_recovery}'))
            
            # spanning-tree loopguard default
            if attributes.value('loop_guard'):
                configurations.append_line(
                    attributes.format('spanning-tree loopguard default'))
            
            # spanning-tree portfast bpduguard default
            if attributes.value('bpdu_guard'):
                configurations.append_line(
                    attributes.format('spanning-tree portfast bpduguard default'))
            
            # spanning-tree portfast bpdufilter default
            if attributes.value('bpdu_filter'):
                configurations.append_line(
                    attributes.format('spanning-tree portfast bpdufilter default'))

            # mpde attributes
            for sub, attributes2 in attributes.mapping_values('mode_attr',
                sort=True, keys=self.mode_attr):
                configurations.append_block(
                    sub.build_config(apply=False,
                                     attributes=attributes2,
                                     unconfig=unconfig))

            if apply:
                if configurations:
                    self.device.configure(configurations)
            else:
                return CliConfig(device=self.device, unconfig=unconfig,
                                 cli_config=configurations)

        def build_unconfig(self, apply=True, attributes=None, **kwargs):
            return self.build_config(apply=apply, attributes=attributes,
                                     unconfig=True, **kwargs)

        class ModeAttributes(ABC):

            def build_config(self, apply=True, attributes=None, unconfig=False,
                             **kwargs):
                assert not apply
                assert not kwargs, kwargs
                attributes = AttributesHelper(self, attributes)
                configurations = CliConfigBuilder(unconfig=unconfig)

                # spanning-tree mode {mode}
                if attributes.value('mode'):
                    mode = 'mst' if 'mstp' in self.mode else self.mode
                    configurations.append_line(
                        attributes.format('spanning-tree mode {}'.format(mode), force=True))

                # spanning-tree transmit hold-count {hold_count}
                configurations.append_line(
                    attributes.format('spanning-tree transmit hold-count {hold_count}'))

                # mst_attr
                for sub, attributes2 in attributes.mapping_values('mst_attr',
                    sort=True, keys=self.mst_attr):
                    configurations.append_block(
                        sub.build_config(apply=False,
                                         attributes=attributes2,
                                         unconfig=unconfig))

                # pvst_attr
                for sub, attributes2 in attributes.mapping_values('pvst_attr',
                    sort=True, keys=self.pvst_attr):
                    configurations.append_block(
                        sub.build_config(apply=False,
                                         attributes=attributes2,
                                         unconfig=unconfig))

                return str(configurations)

            def build_unconfig(self, apply=True, attributes=None, **kwargs):
                return self.build_config(apply=apply, attributes=attributes,
                                         unconfig=True, **kwargs)

            # ---------------
            #    mode MST
            # ---------------
            class MstAttributes(ABC):

                def build_config(self, apply=True, attributes=None,
                                 unconfig=False, **kwargs):
                    assert not apply
                    assert not kwargs, kwargs
                    attributes = AttributesHelper(self, attributes)
                    configurations = CliConfigBuilder(unconfig=unconfig)

                    # spanning-tree mst max-hops <m_max_hop>
                    configurations.append_line(
                        attributes.format('spanning-tree mst max-hops {m_max_hop}'))

                    # spanning-tree mst hello-time <m_hello_time>
                    configurations.append_line(
                        attributes.format('spanning-tree mst hello-time {m_hello_time}'))

                    # spanning-tree mst max-age <m_max_age>
                    configurations.append_line(
                        attributes.format('spanning-tree mst max-age {m_max_age}'))

                    # spanning-tree mst forward-time <m_forwarding_delay>
                    configurations.append_line(
                        attributes.format('spanning-tree mst forward-time {m_forwarding_delay}'))

                    # instance_attr
                    for sub, attributes2 in attributes.mapping_values('instance_attr',
                        sort=True, keys=self.instance_attr):
                        configurations.append_block(
                            sub.build_config(apply=False,
                                             attributes=attributes2,
                                             unconfig=unconfig))
                    # interface_attr
                    for sub, attributes2 in attributes.mapping_values('interface_attr',
                        sort=True, keys=self.interface_attr):
                        configurations.append_block(
                            sub.build_config(apply=False,
                                             attributes=attributes2,
                                             unconfig=unconfig))

                    return str(configurations)

                def build_unconfig(self, apply=True, attributes=None,
                                   **kwargs):
                    return self.build_config(apply=apply,
                                             attributes=attributes,
                                             unconfig=True, **kwargs)

                class InterfaceAttributes(ABC):

                    def build_config(self, apply=True, attributes=None,
                                     unconfig=False, **kwargs):
                        assert not apply
                        assert not kwargs, kwargs
                        attributes = AttributesHelper(self, attributes)
                        configurations = CliConfigBuilder(unconfig=unconfig)

                        # the interface should have vrf(name = vrf_name) attached
                        with configurations.submode_context(
                            attributes.format('interface {interface_name}',
                                              force=True)):
                            # spanning-tree portfast
                            configurations.append_line(attributes.format(
                                'spanning-tree portfast')) if attributes.value('m_if_edge_port') and \
                                    'edge_enable' in attributes.value('m_if_edge_port') else None

                            # spanning-tree link-type point-to-point
                            configurations.append_line(attributes.format(
                                'spanning-tree link-type point-to-point')) if attributes.value('m_if_link_type') and \
                                    'p2p' in attributes.value('m_if_link_type') else None

                            # spanning-tree link-type shared
                            configurations.append_line(attributes.format(
                                'spanning-tree link-type shared')) if attributes.value('m_if_link_type') and \
                                    'shared' in attributes.value('m_if_link_type') else None

                            # spanning-tree guard <m_if_guard>
                            configurations.append_line(attributes.format(
                                'spanning-tree guard {m_if_guard}'))

                            # spanning-tree bpduguard enable
                            configurations.append_line(attributes.format(
                                'spanning-tree bpduguard enable')) if \
                                    attributes.value('m_if_bpdu_guard') else None

                            # spanning-tree bpdufilter enable
                            configurations.append_line(attributes.format(
                                'spanning-tree bpdufilter enable')) if \
                                    attributes.value('m_if_bpdu_filter') else None

                        return str(configurations)

                    def build_unconfig(self, apply=True, attributes=None,
                                       **kwargs):
                        return self.build_config(apply=apply,
                                                 attributes=attributes,
                                                 unconfig=True, **kwargs)

                class InstanceAttributes(ABC):

                    def build_config(self, apply=True, attributes=None,
                                     unconfig=False, **kwargs):
                        assert not apply
                        assert not kwargs, kwargs
                        attributes = AttributesHelper(self, attributes)
                        configurations = CliConfigBuilder(unconfig=unconfig)

                        # only add mst_id in attributes when 
                        # unconfig for specific attributes is enable
                        if unconfig and attributes.attributes:
                            attributes.attributes['mst_id'] = None

                        # the interface should have vrf(name = vrf_name) attached
                        if attributes.value('m_vlans') or \
                           attributes.value('m_name') or \
                           attributes.value('m_revision'):
                            with configurations.submode_context(
                                attributes.format('spanning-tree mst configuration',
                                                  force=True)):

                                # instance <mst_id> vlan <m_vlans>
                                configurations.append_line(
                                    attributes.format(
                                        'instance {mst_id} vlan {m_vlans}'))

                                # name <m_name>
                                configurations.append_line(
                                    attributes.format(
                                        'name {m_name}'))

                                # revision  <m_revision>
                                configurations.append_line(
                                    attributes.format(
                                        'revision {m_revision}'))

                        # spanning-tree mst <mst_id> priority <m_bridge_priority>
                        configurations.append_line(
                            attributes.format(
                                'spanning-tree mst {mst_id} priority {m_bridge_priority}'))

                        # interface_attr
                        for sub, attributes2 in attributes.mapping_values('interface_attr',
                            sort=True, keys=self.interface_attr):
                            configurations.append_block(
                                sub.build_config(apply=False,
                                                 attributes=attributes2,
                                                 unconfig=unconfig,
                                                 mst_id = self.mst_id))

                        return str(configurations)

                    def build_unconfig(self, apply=True, attributes=None,
                                       **kwargs):
                        return self.build_config(apply=apply,
                                                 attributes=attributes,
                                                 unconfig=True, **kwargs)

                    class InterfaceAttributes(ABC):

                        def build_config(self, apply=True, attributes=None,
                                         unconfig=False, **kwargs):
                            assert not apply
                            attributes = AttributesHelper(self, attributes)
                            configurations = CliConfigBuilder(unconfig=unconfig)
                                
                            self.mst_id = kwargs['mst_id']
                        
                            # only add mst_id in attributes when 
                            # unconfig for specific attributes is enable
                            if unconfig and attributes.attributes:
                                attributes.attributes['mst_id'] = None

                            # the interface should have vrf(name = vrf_name) attached
                            with configurations.submode_context(
                                attributes.format('interface {interface_name}',
                                                  force=True)):
                                # spanning-tree mst <mst_id> cost <m_inst_if_cost>
                                configurations.append_line(
                                    attributes.format(
                                        'spanning-tree mst {mst_id} cost {m_inst_if_cost}'))

                                # spanning-tree mst <mst_id> port-priority <m_inst_if_port_priority>
                                configurations.append_line(
                                    attributes.format(
                                        'spanning-tree mst {mst_id} port-priority {m_inst_if_port_priority}'))

                            return str(configurations)

                        def build_unconfig(self, apply=True, attributes=None,
                                           **kwargs):
                            return self.build_config(apply=apply,
                                                     attributes=attributes,
                                                     unconfig=True, **kwargs)

            # ---------------
            #    mode Pvst
            # ---------------
            class PvstAttributes(ABC):

                def build_config(self, apply=True, attributes=None,
                                 unconfig=False, **kwargs):
                    assert not apply
                    assert not kwargs, kwargs
                    attributes = AttributesHelper(self, attributes)
                    configurations = CliConfigBuilder(unconfig=unconfig)

                    # instance_attr
                    for sub, attributes2 in attributes.mapping_values('vlan_attr',
                        sort=True, keys=self.vlan_attr):
                        configurations.append_block(
                            sub.build_config(apply=False,
                                             attributes=attributes2,
                                             unconfig=unconfig))
                    # interface_attr
                    for sub, attributes2 in attributes.mapping_values('interface_attr',
                        sort=True, keys=self.interface_attr):
                        configurations.append_block(
                            sub.build_config(apply=False,
                                             attributes=attributes2,
                                             unconfig=unconfig))
                    return str(configurations)

                def build_unconfig(self, apply=True, attributes=None,
                                   **kwargs):
                    return self.build_config(apply=apply,
                                             attributes=attributes,
                                             unconfig=True, **kwargs)

                class InterfaceAttributes(ABC):

                    def build_config(self, apply=True, attributes=None,
                                     unconfig=False, **kwargs):
                        assert not apply
                        assert not kwargs, kwargs
                        attributes = AttributesHelper(self, attributes)
                        configurations = CliConfigBuilder(unconfig=unconfig)

                        # the interface should have vrf(name = vrf_name) attached
                        with configurations.submode_context(
                            attributes.format('interface {interface_name}',
                                              force=True)):
                            # spanning-tree portfast
                            configurations.append_line(attributes.format(
                                'spanning-tree portfast')) if attributes.value('p_if_edge_port') and \
                                    'edge_enable' in attributes.value('p_if_edge_port') else None

                            # spanning-tree link-type point-to-point
                            configurations.append_line(attributes.format(
                                'spanning-tree link-type point-to-point')) if attributes.value('p_if_link_type') and \
                                    'p2p' in attributes.value('p_if_link_type') else None

                            # spanning-tree link-type shared
                            configurations.append_line(attributes.format(
                                'spanning-tree link-type shared')) if attributes.value('p_if_link_type') and \
                                    'shared' in attributes.value('p_if_link_type') else None

                            # spanning-tree guard <p_if_guard>
                            configurations.append_line(attributes.format(
                                'spanning-tree guard {p_if_guard}'))

                            # spanning-tree bpduguard enable
                            configurations.append_line(attributes.format(
                                'spanning-tree bpduguard enable')) if \
                                    attributes.value('p_if_bpdu_guard') else None

                            # spanning-tree bpdufilter enable
                            configurations.append_line(attributes.format(
                                'spanning-tree bpdufilter enable')) if \
                                    attributes.value('p_if_bpdu_filter') else None

                        return str(configurations)

                    def build_unconfig(self, apply=True, attributes=None,
                                       **kwargs):
                        return self.build_config(apply=apply,
                                                 attributes=attributes,
                                                 unconfig=True, **kwargs)

                class VlanAttributes(ABC):

                    def build_config(self, apply=True, attributes=None,
                                     unconfig=False, **kwargs):
                        assert not apply
                        assert not kwargs, kwargs
                        attributes = AttributesHelper(self, attributes)
                        configurations = CliConfigBuilder(unconfig=unconfig)

                        # only add vlan_id in attributes when 
                        # unconfig for specific attributes is enable
                        if unconfig and attributes.attributes:
                            attributes.attributes['vlan'] = None

                        if attributes.value('vlan_id'):
                            configurations.append_line(attributes.format(
                                'spanning-tree vlan {vlan_id}'))

                        # spanning-tree vlan <vlan_id> hello-time <v_hello_time>
                        configurations.append_line(
                            attributes.format(
                                'spanning-tree vlan {vlan} hello-time {v_hello_time}'))

                        # spanning-tree vlan <vlan_id> max-age <v_max_age>
                        configurations.append_line(
                            attributes.format(
                                'spanning-tree vlan {vlan} max-age {v_max_age}'))

                        # spanning-tree vlan <vlan_id> forward-time <v_forwarding_delay>
                        configurations.append_line(
                            attributes.format(
                                'spanning-tree vlan {vlan} forward-time {v_forwarding_delay}'))

                        # spanning-tree vlan <vlan_id> priority <v_bridge_priority>
                        configurations.append_line(
                            attributes.format(
                                'spanning-tree vlan {vlan} priority {v_bridge_priority}'))

                        # interface_attr
                        for sub, attributes2 in attributes.mapping_values('interface_attr',
                            sort=True, keys=self.interface_attr):
                            configurations.append_block(
                                sub.build_config(apply=False,
                                                 attributes=attributes2,
                                                 unconfig=unconfig,
                                                 vlan_id = self.vlan))

                        return str(configurations)

                    def build_unconfig(self, apply=True, attributes=None,
                                       **kwargs):
                        return self.build_config(apply=apply,
                                                 attributes=attributes,
                                                 unconfig=True, **kwargs)

                    class InterfaceAttributes(ABC):

                        def build_config(self, apply=True, attributes=None,
                                         unconfig=False, **kwargs):
                            assert not apply
                            attributes = AttributesHelper(self, attributes)
                            configurations = CliConfigBuilder(unconfig=unconfig)

                            self.vlan = kwargs['vlan_id']

                            # only add vlan_id in attributes when 
                            # unconfig for specific attributes is enable
                            if unconfig and attributes.attributes:
                                attributes.attributes['vlan'] = None

                            # the interface should have vrf(name = vrf_name) attached
                            with configurations.submode_context(
                                attributes.format('interface {interface_name}',
                                                  force=True)):
                                # spanning-tree mst <mst_id> cost <m_inst_if_cost>
                                configurations.append_line(
                                    attributes.format(
                                        'spanning-tree vlan {vlan} cost {v_if_cost}'))

                                # spanning-tree vlan <vlan_id> port-priority <v_if_port_priority>
                                configurations.append_line(
                                    attributes.format(
                                        'spanning-tree vlan {vlan} port-priority {v_if_port_priority}'))

                            return str(configurations)

                        def build_unconfig(self, apply=True, attributes=None,
                                           **kwargs):
                            return self.build_config(apply=apply,
                                                     attributes=attributes,
                                                     unconfig=True, **kwargs)



