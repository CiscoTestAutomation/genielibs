''' 
LISP Genie Conf Object Implementation for IOSXE - CLI.
'''

# Pyhon
from abc import ABC

# Genie
from genie.conf.base.attributes import AttributesHelper
from genie.conf.base.cli import CliConfigBuilder
from genie.conf.base.config import CliConfig

# LISP Heirarchy
# --------------
# Lisp
#  +- DeviceAttributes
#      +- InterfaceAttributes
#      |   +- MobilityDynamicEidAttributes
#      +- RouterInstanceAttributes
#          +- LocatorSetAttributes
#          |   +- InterfaceAttributes
#          |       +- InterfacdTypeAttributes
#          +- ServiceAttributes
#          |   +- ItrMrAttributes
#          |   +- EtrMsAttributes
#          |   +- ProxyItrAttributes
#          +- InstanceAttributes
#          |   +- DynamicEidAttributes
#          |       +- DbMappingAttributes
#          |   +- ServiceAttributes
#          |       +- DbMappingAttributes
#          |       +- UsePetrAttributes
#          |       +- MapCacheAttributes
#          +- SiteAttributes
#          |   +- InstanceIdAttributes
#          |       +- EidRecordAttributes
#          +- ExtranetAttributes
#              +- InstanceIdAttributes
#                  +- EidRecordProviderAttributes
#                  +- EidRecordSubscriberAttributes


class Lisp(ABC):

    class DeviceAttributes(ABC):

        def build_config(self, apply=True, attributes=None, unconfig=False,
                         **kwargs):
            assert not kwargs, kwargs
            attributes = AttributesHelper(self, attributes)
            configurations = CliConfigBuilder(unconfig=unconfig)

            # +- DeviceAttributes
            #   +- InterfaceAttributes
            # ------------------------
            # Add InterfaceAttributes configurations under DeviceAttributes
            for sub, attributes2 in attributes.mapping_values('intf_attr', 
                                                              sort=True, 
                                                              keys=self.intf_attr):
                configurations.append_block(
                    sub.build_config(apply=False,
                                     attributes=attributes2,
                                     unconfig=unconfig))

            # +- DeviceAttributes
            #   +- RouterInstanceAttributes
            # -----------------------------
            # Add RouterInstanceAttributes configurations under DeviceAttributes
            for sub, attributes2 in attributes.mapping_values('router_instance_attr', 
                                                              sort=True, 
                                                              keys=self.router_instance_attr):
                configurations.append_block(
                    sub.build_config(apply=False,
                                     attributes=attributes2,
                                     unconfig=unconfig))

            return str(configurations)

        def build_unconfig(self, apply=True, attributes=None, **kwargs):
            return self.build_config(apply=apply, attributes=attributes,
                                     unconfig=True, **kwargs)

        # +- DeviceAttributes
        #   +- InterfaceAttributes
        class InterfaceAttributes(ABC):

            def build_config(self, apply=True, attributes=None, unconfig=False, **kwargs):
                assert not apply
                attributes = AttributesHelper(self, attributes)
                configurations = CliConfigBuilder(unconfig=unconfig)

                # interface GigabitEthernet1
                with configurations.submode_context(
                    attributes.format('interface {interface.name}', force=True)):

                    # interface GigabitEthernet1
                    #   no lisp mobility liveness test
                    if attributes.value('if_mobility_liveness_test_disabled') is True:
                        config_cmd = 'no lisp mobility liveness test'
                        unconfig_cmd = 'lisp mobility liveness test'
                        configurations.append_line(attributes.format(config_cmd),
                                                    unconfig_cmd=unconfig_cmd)

                    # +- DeviceAttributes
                    #   +- InterfaceAttributes
                    #     +- MobilityDynamicEidAttributes
                    # -----------------------------------
                    # Add MobilityDynamicEidAttributes configurations under InterfaceAttributes
                    for sub, attributes2 in attributes.mapping_values('mobility_dynamic_eid_attr', 
                                                                      sort=True, 
                                                                      keys=self.mobility_dynamic_eid_attr):
                        configurations.append_block(
                            sub.build_config(apply=False,
                                             attributes=attributes2,
                                             unconfig=unconfig))

                return str(configurations)

            def build_unconfig(self, apply=True, attributes=None, **kwargs):
                return self.build_config(apply=apply, attributes=attributes,
                                         unconfig=True, **kwargs)

            # +- DeviceAttributes
            #   +- RouterInstanceAttributes
            #     +- LocatorSetAttributes
            class MobilityDynamicEidAttributes(ABC):

                def build_config(self, apply=True, attributes=None, unconfig=False, **kwargs):
                    assert not apply
                    attributes = AttributesHelper(self, attributes)
                    configurations = CliConfigBuilder(unconfig=unconfig)

                    configurations.append_line(
                        attributes.format('lisp mobility {if_mobility_dynamic_eid_name}'))

                    return str(configurations)

                def build_unconfig(self, apply=True, attributes=None, **kwargs):
                    return self.build_config(apply=apply, attributes=attributes,
                                             unconfig=True, **kwargs)

        # +- DeviceAttributes
        #   +- RouterInstanceAttributes
        class RouterInstanceAttributes(ABC):

            def build_config(self, apply=True, attributes=None, unconfig=False, **kwargs):
                assert not apply
                attributes = AttributesHelper(self, attributes)
                configurations = CliConfigBuilder(unconfig=unconfig)

                # router lisp 101
                with configurations.submode_context(
                    attributes.format('router lisp {lisp_router_instance_id}', force=True)):

                    if unconfig and attributes.iswildcard:
                        configurations.submode_unconfig()

                    # +- DeviceAttributes
                    #   +- RouterInstanceAttributes
                    #     +- LocatorSetAttributes
                    # -----------------------------------
                    # Add LocatorSetAttributes configurations under RouterInstanceAttributes
                    for sub, attributes2 in attributes.mapping_values('locator_set_attr', 
                                                                      sort=True, 
                                                                      keys=self.locator_set_attr):
                        configurations.append_block(
                            sub.build_config(apply=False,
                                             attributes=attributes2,
                                             unconfig=unconfig))

                    # +- DeviceAttributes
                    #   +- RouterInstanceAttributes
                    #     +- ServiceAttributes
                    # -----------------------------------
                    # Add ServiceAttributes configurations under RouterInstanceAttributes
                    for sub, attributes2 in attributes.mapping_values('service_attr', 
                                                                      sort=True, 
                                                                      keys=self.service_attr):
                        configurations.append_block(
                            sub.build_config(apply=False,
                                             attributes=attributes2,
                                             unconfig=unconfig))

                    # +- DeviceAttributes
                    #   +- RouterInstanceAttributes
                    #     +- InstanceAttributes
                    # -----------------------------------
                    # Add InstanceAttributes configurations under RouterInstanceAttributes
                    for sub, attributes2 in attributes.mapping_values('instance_id_attr', 
                                                                      sort=True, 
                                                                      keys=self.instance_id_attr):
                        configurations.append_block(
                            sub.build_config(apply=False,
                                             attributes=attributes2,
                                             unconfig=unconfig))

                    # +- DeviceAttributes
                    #   +- RouterInstanceAttributes
                    #     +- SiteAttributes
                    # -----------------------------------
                    # Add SiteAttributes configurations under RouterInstanceAttributes
                    for sub, attributes2 in attributes.mapping_values('site_attr', 
                                                                      sort=True, 
                                                                      keys=self.site_attr):
                        configurations.append_block(
                            sub.build_config(apply=False,
                                             attributes=attributes2,
                                             unconfig=unconfig))

                    # +- DeviceAttributes
                    #   +- RouterInstanceAttributes
                    #     +- ExtranetAttributes
                    # -----------------------------------
                    # Add ExtranetAttributes configurations under RouterInstanceAttributes
                    for sub, attributes2 in attributes.mapping_values('extranet_attr', 
                                                                      sort=True, 
                                                                      keys=self.extranet_attr):
                        configurations.append_block(
                            sub.build_config(apply=False,
                                             attributes=attributes2,
                                             unconfig=unconfig))

                return str(configurations)

            def build_unconfig(self, apply=True, attributes=None, **kwargs):
                return self.build_config(apply=apply, attributes=attributes,
                                         unconfig=True, **kwargs)

            # +- DeviceAttributes
            #   +- RouterInstanceAttributes
            #     +- LocatorSetAttributes
            class LocatorSetAttributes(ABC):

                def build_config(self, apply=True, attributes=None, unconfig=False, **kwargs):
                    assert not apply
                    attributes = AttributesHelper(self, attributes)
                    configurations = CliConfigBuilder(unconfig=unconfig)

                    # locator-set RLOC
                    with configurations.submode_context(
                        attributes.format('locator-set {locator_set_name}', force=True)):

                        if unconfig and attributes.iswildcard:
                            configurations.submode_unconfig()

                        # +- DeviceAttributes
                        #   +- RouterInstanceAttributes
                        #     +- LocatorSetAttributes
                        #       +- InterfaceAttributes
                        # -----------------------------------
                        # Add InterfaceAttributes configurations under LocatorSetAttributes
                        for sub, attributes2 in attributes.mapping_values('locator_set_intf_attr', 
                                                                          sort=True, 
                                                                          keys=self.locator_set_intf_attr):
                            configurations.append_block(
                                sub.build_config(apply=False,
                                                 attributes=attributes2,
                                                 unconfig=unconfig))

                    return str(configurations)

                def build_unconfig(self, apply=True, attributes=None, **kwargs):
                    return self.build_config(apply=apply, attributes=attributes,
                                             unconfig=True, **kwargs)

                # +- DeviceAttributes
                #   +- RouterInstanceAttributes
                #     +- LocatorSetAttributes
                #       +- InterfaceAttributes
                class InterfaceAttributes(ABC):

                    def build_config(self, apply=True, attributes=None, unconfig=False, **kwargs):
                        assert not apply
                        attributes = AttributesHelper(self, attributes)
                        configurations = CliConfigBuilder(unconfig=unconfig)

                        # +- DeviceAttributes
                        #   +- RouterInstanceAttributes
                        #     +- LocatorSetAttributes
                        #       +- InterfaceAttributes
                        #         +- InterfaceTypeAttributes
                        # -----------------------------------
                        # Add InterfaceTypeAttributes configurations under InterfaceAttributes
                        for sub, attributes2 in attributes.mapping_values('locator_set_intf_type_attr', 
                                                                          sort=True, 
                                                                          keys=self.locator_set_intf_type_attr):
                            configurations.append_block(
                                sub.build_config(apply=False,
                                                 attributes=attributes2,
                                                 unconfig=unconfig,
                                                 ls_interface=self.ls_interface))

                        return str(configurations)

                    def build_unconfig(self, apply=True, attributes=None, **kwargs):
                        return self.build_config(apply=apply, attributes=attributes,
                                                 unconfig=True, **kwargs)
                    # +- DeviceAttributes
                    #   +- RouterInstanceAttributes
                    #     +- LocatorSetAttributes
                    #       +- InterfaceAttributes
                    #         +- InterfaceTypeAttributes
                    class InterfaceTypeAttributes(ABC):

                        def build_config(self, apply=True, attributes=None, unconfig=False, **kwargs):
                            assert not apply
                            attributes = AttributesHelper(self, attributes)
                            configurations = CliConfigBuilder(unconfig=unconfig)

                            if self.ls_interface_type == 'ipv4':
                                intf_type = 'IPv4-interface'
                            elif self.ls_interface_type == 'ipv6':
                                intf_type = 'IPv6-interface'

                            cfg_str = '{type} {interface}'.format(type=intf_type, interface=kwargs['ls_interface'])

                            if attributes.value('ls_priority'):
                                cfg_str += ' priority {ls_priority}'

                            if attributes.value('ls_weight'):
                                cfg_str += ' weight {ls_weight}'

                            configurations.append_line(attributes.format(cfg_str))

                            return str(configurations)

                        def build_unconfig(self, apply=True, attributes=None, **kwargs):
                            return self.build_config(apply=apply, attributes=attributes,
                                                     unconfig=True, **kwargs)

            # +- DeviceAttributes
            #   +- RouterInstanceAttributes
            #     +- ServiceAttributes
            class ServiceAttributes(ABC):

                def build_config(self, apply=True, attributes=None, unconfig=False, **kwargs):
                    assert not apply
                    attributes = AttributesHelper(self, attributes)
                    configurations = CliConfigBuilder(unconfig=unconfig)

                    # service ipv4
                    with configurations.submode_context(
                        attributes.format('service {service}', force=True)):

                        if unconfig and attributes.iswildcard:
                            configurations.submode_unconfig()

                        # service ipv4
                        #   itr
                        if attributes.value('itr_enabled') is True:
                            configurations.append_line('itr')

                        # service ipv4
                        #   etr
                        if attributes.value('etr_enabled') is True:
                            configurations.append_line('etr')

                        # service ipv4
                        #   map-server
                        if attributes.value('ms_enabled') is True:
                            configurations.append_line('map-server')

                        # service ipv4
                        #   map-resolver
                        if attributes.value('mr_enabled') is True:
                            configurations.append_line('map-resolver')

                        # service ipv4
                        #   proxy-etr
                        if attributes.value('proxy_etr_enabled') is True:
                            configurations.append_line('proxy-etr')

                        # service ipv4
                        #   encapsulation vxlan
                        if attributes.value('encapsulation'):
                            configurations.append_line('encapsulation {}'.\
                                    format(attributes.value('encapsulation').value))

                        # +- DeviceAttributes
                        #   +- RouterInstanceAttributes
                        #     +- ServiceAttributes
                        #       +- ItrMrAttributes
                        # -----------------------------------
                        # Add ItrMrAttributes configurations under ServiceAttributes
                        for sub, attributes2 in attributes.mapping_values('itr_mr_attr', 
                                                                          sort=True, 
                                                                          keys=self.itr_mr_attr):
                            configurations.append_block(
                                sub.build_config(apply=False,
                                                 attributes=attributes2,
                                                 unconfig=unconfig))

                        # +- DeviceAttributes
                        #   +- RouterInstanceAttributes
                        #     +- ServiceAttributes
                        #       +- EtrMsAttributes
                        # -----------------------------------
                        # Add EtrMsAttributes configurations under ServiceAttributes
                        for sub, attributes2 in attributes.mapping_values('etr_ms_attr', 
                                                                          sort=True, 
                                                                          keys=self.etr_ms_attr):
                            configurations.append_block(
                                sub.build_config(apply=False,
                                                 attributes=attributes2,
                                                 unconfig=unconfig))

                        # +- DeviceAttributes
                        #   +- RouterInstanceAttributes
                        #     +- ServiceAttributes
                        #       +- ProxyItrAttributes
                        # -----------------------------------
                        # Add ProxyItrAttributes configurations under ServiceAttributes
                        for sub, attributes2 in attributes.mapping_values('proxy_attr', 
                                                                          sort=True, 
                                                                          keys=self.proxy_attr):
                            configurations.append_block(
                                sub.build_config(apply=False,
                                                 attributes=attributes2,
                                                 unconfig=unconfig))

                    return str(configurations)

                def build_unconfig(self, apply=True, attributes=None, **kwargs):
                    return self.build_config(apply=apply, attributes=attributes,
                                             unconfig=True, **kwargs)

                # +- DeviceAttributes
                #   +- RouterInstanceAttributes
                #     +- ServiceAttributes
                #       +- ItrMrAttributes
                class ItrMrAttributes(ABC):

                    def build_config(self, apply=True, attributes=None, unconfig=False, **kwargs):
                        assert not apply
                        attributes = AttributesHelper(self, attributes)
                        configurations = CliConfigBuilder(unconfig=unconfig)

                        # service ipv4
                        #   itr map-resolver 6.6.6.6
                        configurations.append_line(attributes.format('itr map-resolver {itr_map_resolver}'))

                        return str(configurations)

                    def build_unconfig(self, apply=True, attributes=None, **kwargs):
                        return self.build_config(apply=apply, attributes=attributes,
                                                 unconfig=True, **kwargs)

                # +- DeviceAttributes
                #   +- RouterInstanceAttributes
                #     +- ServiceAttributes
                #       +- EtrMsAttributes
                class EtrMsAttributes(ABC):

                    def build_config(self, apply=True, attributes=None, unconfig=False, **kwargs):
                        assert not apply
                        attributes = AttributesHelper(self, attributes)
                        configurations = CliConfigBuilder(unconfig=unconfig)

                        # service ipv4
                        #   etr map-server 5.5.5.5 key cisco123
                        if attributes.value('etr_auth_key'):
                            cfg_str = 'etr map-resolver {etr_map_server} key {etr_auth_key}'
                            if attributes.value('etr_auth_key_type').value is not None:
                                cfg_str += ' hash-function {}'.format(attributes.value('etr_auth_key_type').name)
                            configurations.append_line(attributes.format(cfg_str))

                        # service ipv4
                        #   etr map-server 5.5.5.5 proxy-reply
                        if attributes.value('etr_proxy_reply') is True:
                            configurations.append_line(attributes.format('etr map-resolver {etr_map_server} proxy-reply'))

                        return str(configurations)

                    def build_unconfig(self, apply=True, attributes=None, **kwargs):
                        return self.build_config(apply=apply, attributes=attributes,
                                                 unconfig=True, **kwargs)

                # +- DeviceAttributes
                #   +- RouterInstanceAttributes
                #     +- ServiceAttributes
                #       +- ProxyItrAttributes
                class ProxyItrAttributes(ABC):

                    def build_config(self, apply=True, attributes=None, unconfig=False, **kwargs):
                        assert not apply
                        attributes = AttributesHelper(self, attributes)
                        configurations = CliConfigBuilder(unconfig=unconfig)

                        # service ipv4
                        #   proxy-itr 10.10.10.10
                        if attributes.value('proxy_itr'):
                            configurations.append_line(attributes.format('proxy-itr {proxy_itr}'))

                        return str(configurations)

                    def build_unconfig(self, apply=True, attributes=None, **kwargs):
                        return self.build_config(apply=apply, attributes=attributes,
                                                 unconfig=True, **kwargs)

            # +- DeviceAttributes
            #   +- RouterInstanceAttributes
            #     +- InstanceAttributes
            class InstanceAttributes(ABC):

                def build_config(self, apply=True, attributes=None, unconfig=False, **kwargs):
                    assert not apply
                    attributes = AttributesHelper(self, attributes)
                    configurations = CliConfigBuilder(unconfig=unconfig)

                    # instance-id 101
                    with configurations.submode_context(
                        attributes.format('instance-id {instance_id}', force=True)):

                        if unconfig and attributes.iswildcard:
                            configurations.submode_unconfig()

                        # +- DeviceAttributes
                        #   +- RouterInstanceAttributes
                        #     +- InstanceAttributes
                        #       +- DynamicEidAttributes
                        # -----------------------------------
                        # Add DynamicEidAttributes configurations under InstanceAttributes
                        for sub, attributes2 in attributes.mapping_values('dynamic_eid_attr', 
                                                                          sort=True, 
                                                                          keys=self.dynamic_eid_attr):
                            configurations.append_block(
                                sub.build_config(apply=False,
                                                 attributes=attributes2,
                                                 unconfig=unconfig))

                        # +- DeviceAttributes
                        #   +- RouterInstanceAttributes
                        #     +- InstanceAttributes
                        #       +- ServiceAttributes
                        # -----------------------------------
                        # Add ServiceAttributes configurations under InstanceAttributes
                        for sub, attributes2 in attributes.mapping_values('inst_service_attr', 
                                                                          sort=True, 
                                                                          keys=self.inst_service_attr):
                            configurations.append_block(
                                sub.build_config(apply=False,
                                                 attributes=attributes2,
                                                 unconfig=unconfig,
                                                 instance_id=self.instance_id))

                    return str(configurations)

                def build_unconfig(self, apply=True, attributes=None, **kwargs):
                    return self.build_config(apply=apply, attributes=attributes,
                                             unconfig=True, **kwargs)

                # +- DeviceAttributes
                #   +- RouterInstanceAttributes
                #     +- InstanceAttributes
                #       +- DynamicEidAttributes
                class DynamicEidAttributes(ABC):

                    def build_config(self, apply=True, attributes=None, unconfig=False, **kwargs):
                        assert not apply
                        attributes = AttributesHelper(self, attributes)
                        configurations = CliConfigBuilder(unconfig=unconfig)

                        # instance-id 101
                        #   dynamic-eid 192
                        with configurations.submode_context(
                            attributes.format('dynamic-eid {inst_dyn_eid}', force=True)):

                            if unconfig and attributes.iswildcard:
                                configurations.submode_unconfig()

                            # +- DeviceAttributes
                            #   +- RouterInstanceAttributes
                            #     +- InstanceAttributes
                            #       +- DynamicEidAttributes
                            #         +- DbMappingAttributes
                            # -----------------------------------
                            # Add DbMappingAttributes configurations under DynamicEidAttributes
                            for sub, attributes2 in attributes.mapping_values('db_mapping_attr', 
                                                                              sort=True, 
                                                                              keys=self.db_mapping_attr):
                                configurations.append_block(
                                    sub.build_config(apply=False,
                                                     attributes=attributes2,
                                                     unconfig=unconfig))

                        return str(configurations)

                    def build_unconfig(self, apply=True, attributes=None, **kwargs):
                        return self.build_config(apply=apply, attributes=attributes,
                                                 unconfig=True, **kwargs)

                    # +- DeviceAttributes
                    #   +- RouterInstanceAttributes
                    #     +- InstanceAttributes
                    #       +- DynamicEidAttributes
                    #         +- DbMappingAttributes
                    class DbMappingAttributes(ABC):

                        def build_config(self, apply=True, attributes=None, unconfig=False, **kwargs):
                            assert not apply
                            attributes = AttributesHelper(self, attributes)
                            configurations = CliConfigBuilder(unconfig=unconfig)

                            # instance-id 101
                            #   dynamic-eid 192
                            #     database-mapping 192.168.0.0/24
                            cfg_str = 'datbase-mapping {etr_dyn_eid_id}'

                            # instance-id 101
                            #   dynamic-eid 192
                            #     database-mapping 192.168.0.0/24 locator-set RLOC1
                            if attributes.value('etr_dyn_eid_rlocs'):
                                cfg_str += ' locator-set {etr_dyn_eid_rlocs}'

                            configurations.append_line(attributes.format(cfg_str))

                            return str(configurations)

                        def build_unconfig(self, apply=True, attributes=None, **kwargs):
                            return self.build_config(apply=apply, attributes=attributes,
                                                     unconfig=True, **kwargs)

                # +- DeviceAttributes
                #   +- RouterInstanceAttributes
                #     +- InstanceAttributes
                #       +- ServiceAttributes
                class ServiceAttributes(ABC):

                    def build_config(self, apply=True, attributes=None, unconfig=False, **kwargs):
                        assert not apply
                        attributes = AttributesHelper(self, attributes)
                        configurations = CliConfigBuilder(unconfig=unconfig)

                        # instance-id 101
                        #   service ipv4
                        with configurations.submode_context(
                            attributes.format('service {inst_service}', force=True)):

                            if unconfig and attributes.iswildcard:
                                configurations.submode_unconfig()

                            if attributes.value('etr_eid_vrf'):
                                configurations.append_line(attributes.format('eid-table vrf {etr_eid_vrf}'))
                            else:
                                configurations.append_line(attributes.format('eid-table default'))

                            # +- DeviceAttributes
                            #   +- RouterInstanceAttributes
                            #     +- InstanceAttributes
                            #       +- ServiceAttributes
                            #         +- DbMappingAttributes
                            # -----------------------------------
                            # Add DbMappingAttributes configurations under ServiceAttributes
                            for sub, attributes2 in attributes.mapping_values('service_db_mapping_attr', 
                                                                              sort=True, 
                                                                              keys=self.service_db_mapping_attr):
                                configurations.append_block(
                                    sub.build_config(apply=False,
                                                     attributes=attributes2,
                                                     unconfig=unconfig))

                            # +- DeviceAttributes
                            #   +- RouterInstanceAttributes
                            #     +- InstanceAttributes
                            #       +- ServiceAttributes
                            #         +- UsePetrAttributes
                            # -----------------------------------
                            # Add UsePetrAttributes configurations under ServiceAttributes
                            for sub, attributes2 in attributes.mapping_values('use_petr_attr', 
                                                                              sort=True, 
                                                                              keys=self.use_petr_attr):
                                configurations.append_block(
                                    sub.build_config(apply=False,
                                                     attributes=attributes2,
                                                     unconfig=unconfig,
                                                     instance_id=kwargs['instance_id']))

                            # +- DeviceAttributes
                            #   +- RouterInstanceAttributes
                            #     +- InstanceAttributes
                            #       +- ServiceAttributes
                            #         +- MapCacheAttributes
                            # -----------------------------------
                            # Add MapCacheAttributes configurations under ServiceAttributes
                            for sub, attributes2 in attributes.mapping_values('map_cache_attr', 
                                                                              sort=True, 
                                                                              keys=self.map_cache_attr):
                                configurations.append_block(
                                    sub.build_config(apply=False,
                                                     attributes=attributes2,
                                                     unconfig=unconfig))

                        return str(configurations)

                    def build_unconfig(self, apply=True, attributes=None, **kwargs):
                        return self.build_config(apply=apply, attributes=attributes,
                                                 unconfig=True, **kwargs)

                    # +- DeviceAttributes
                    #   +- RouterInstanceAttributes
                    #     +- InstanceAttributes
                    #       +- ServiceAttributes
                    #         +- DbMappingAttributes
                    class DbMappingAttributes(ABC):

                        def build_config(self, apply=True, attributes=None, unconfig=False, **kwargs):
                            assert not apply
                            attributes = AttributesHelper(self, attributes)
                            configurations = CliConfigBuilder(unconfig=unconfig)

                            # instance-id 101
                            #   service ipv4
                            #     database-mapping 192.168.0.0/24
                            cfg_str = 'datbase-mapping {etr_eid_id}'

                            # instance-id 101
                            #   service ipv4
                            #     database-mapping 192.168.0.0/24 locator-set RLOC1
                            if attributes.value('etr_eid_rlocs'):
                                cfg_str += ' locator-set {etr_eid_rlocs}'

                            configurations.append_line(attributes.format(cfg_str))

                            return str(configurations)

                        def build_unconfig(self, apply=True, attributes=None, **kwargs):
                            return self.build_config(apply=apply, attributes=attributes,
                                                     unconfig=True, **kwargs)

                    # +- DeviceAttributes
                    #   +- RouterInstanceAttributes
                    #     +- InstanceAttributes
                    #       +- ServiceAttributes
                    #         +- UsePetrAttributes
                    class UsePetrAttributes(ABC):

                        def build_config(self, apply=True, attributes=None, unconfig=False, **kwargs):
                            assert not apply
                            attributes = AttributesHelper(self, attributes)
                            configurations = CliConfigBuilder(unconfig=unconfig)

                            # instance-id 101
                            #   service ipv4
                            #     use-petr 10.10.10.10
                            cfg_str = 'use-petr {petr} instance-id {iid}'.\
                                        format(petr=self.etr_use_petr, iid=kwargs['instance_id'])

                            # instance-id 101
                            #   service ipv4
                            #     use-petr 10.10.10.10 priority 10
                            if attributes.value('etr_use_petr_priority'):
                                cfg_str += ' priority {etr_use_petr_priority}'

                            # instance-id 101
                            #   service ipv4
                            #     use-petr 10.10.10.10 priority 10 weight 30
                            if attributes.value('etr_use_petr_weight'):
                                cfg_str += ' weight {etr_use_petr_weight}'

                            configurations.append_line(attributes.format(cfg_str))

                            return str(configurations)

                        def build_unconfig(self, apply=True, attributes=None, **kwargs):
                            return self.build_config(apply=apply, attributes=attributes,
                                                     unconfig=True, **kwargs)

                    # +- DeviceAttributes
                    #   +- RouterInstanceAttributes
                    #     +- InstanceAttributes
                    #       +- ServiceAttributes
                    #         +- MapCacheAttributes
                    class MapCacheAttributes(ABC):

                        def build_config(self, apply=True, attributes=None, unconfig=False, **kwargs):
                            assert not apply
                            attributes = AttributesHelper(self, attributes)
                            configurations = CliConfigBuilder(unconfig=unconfig)

                            # instance-id 101
                            #   service ipv4
                            #     map-cache 10.1.1.0/24
                            cfg_str = 'map-cache {itr_mc_id}'

                            # instance-id 101
                            #   service ipv4
                            #     map-cache 10.1.1.0/24 map-request
                            if attributes.value('itr_mc_map_request') is True:
                                cfg_str += ' map-request'

                            configurations.append_line(attributes.format(cfg_str))

                            return str(configurations)

                        def build_unconfig(self, apply=True, attributes=None, **kwargs):
                            return self.build_config(apply=apply, attributes=attributes,
                                                     unconfig=True, **kwargs)

            # +- DeviceAttributes
            #   +- RouterInstanceAttributes
            #     +- SiteAttributes
            class SiteAttributes(ABC):

                def build_config(self, apply=True, attributes=None, unconfig=False, **kwargs):
                    assert not apply
                    attributes = AttributesHelper(self, attributes)
                    configurations = CliConfigBuilder(unconfig=unconfig)

                    # site xtr1_1
                    with configurations.submode_context(
                        attributes.format('site {ms_site_id}', force=True)):

                        if unconfig and attributes.iswildcard:
                            configurations.submode_unconfig()

                        if attributes.value('ms_site_auth_key'):
                            configurations.append_line(attributes.format('authentication-key {ms_site_auth_key}'))

                        # +- DeviceAttributes
                        #   +- RouterInstanceAttributes
                        #     +- SiteAttributes
                        #       +- InstanceIdAttributes
                        # -----------------------------------
                        # Add SiteAttributes configurations under RouterInstanceAttributes
                        for sub, attributes2 in attributes.mapping_values('site_inst_id_attr', 
                                                                          sort=True, 
                                                                          keys=self.site_inst_id_attr):
                            configurations.append_block(
                                sub.build_config(apply=False,
                                                 attributes=attributes2,
                                                 unconfig=unconfig,
                                                 ms_site_id=self.ms_site_id))

                    return str(configurations)

                def build_unconfig(self, apply=True, attributes=None, **kwargs):
                    return self.build_config(apply=apply, attributes=attributes,
                                             unconfig=True, **kwargs)

                # +- DeviceAttributes
                #   +- RouterInstanceAttributes
                #     +- SiteAttributes
                #       +- InstanceIdAttributes
                class InstanceIdAttributes(ABC):

                    def build_config(self, apply=True, attributes=None, unconfig=False, **kwargs):
                        assert not apply
                        attributes = AttributesHelper(self, attributes)
                        configurations = CliConfigBuilder(unconfig=unconfig)

                        # +- DeviceAttributes
                        #   +- RouterInstanceAttributes
                        #     +- SiteAttributes
                        #       +- InstanceIdAttributes
                        #         +- EidRecordAttributes
                        # -----------------------------------
                        # Add SiteAttributes configurations under RouterInstanceAttributes
                        for sub, attributes2 in attributes.mapping_values('eid_record_attr', 
                                                                          sort=True, 
                                                                          keys=self.eid_record_attr):
                            configurations.append_block(
                                sub.build_config(apply=False,
                                                 attributes=attributes2,
                                                 unconfig=unconfig,
                                                 instance_id=self.site_inst_id))

                        return str(configurations)

                    def build_unconfig(self, apply=True, attributes=None, **kwargs):
                        return self.build_config(apply=apply, attributes=attributes,
                                                 unconfig=True, **kwargs)

                    # +- DeviceAttributes
                    #   +- RouterInstanceAttributes
                    #     +- SiteAttributes
                    #       +- InstanceIdAttributes
                    #         +- EidRecordAttributes
                    class EidRecordAttributes(ABC):

                        def build_config(self, apply=True, attributes=None, unconfig=False, **kwargs):
                            assert not apply
                            attributes = AttributesHelper(self, attributes)
                            configurations = CliConfigBuilder(unconfig=unconfig)

                            # eid-record instance-id 101 88.88.88.0/24
                            cfg_str = 'eid-record instance-id {iid} {eid}'.\
                                        format(iid=kwargs['instance_id'], eid=self.ms_eid_id)

                            if attributes.value('ms_eid_accept_more_specifics') is True:
                                cfg_str += ' accept-more-specifics'

                            configurations.append_line(attributes.format(cfg_str))

                            return str(configurations)

                    def build_unconfig(self, apply=True, attributes=None, **kwargs):
                        return self.build_config(apply=apply, attributes=attributes,
                                                 unconfig=True, **kwargs)

            # +- DeviceAttributes
            #   +- RouterInstanceAttributes
            #     +- ExtranetAttributes
            class ExtranetAttributes(ABC):

                def build_config(self, apply=True, attributes=None, unconfig=False, **kwargs):
                    assert not apply
                    attributes = AttributesHelper(self, attributes)
                    configurations = CliConfigBuilder(unconfig=unconfig)

                    # extranet ext1
                    with configurations.submode_context(
                        attributes.format('extranet {ms_extranet}', force=True)):

                        if unconfig and attributes.iswildcard:
                            configurations.submode_unconfig()

                        # +- DeviceAttributes
                        #   +- RouterInstanceAttributes
                        #     +- ExtranetAttributes
                        #       +- InstanceIdAttributes
                        # -----------------------------------
                        # Add InstanceIdAttributes configurations under ExtranetAttributes
                        for sub, attributes2 in attributes.mapping_values('extranet_inst_id_attr', 
                                                                          sort=True, 
                                                                          keys=self.extranet_inst_id_attr):
                            configurations.append_block(
                                sub.build_config(apply=False,
                                                 attributes=attributes2,
                                                 unconfig=unconfig))

                    return str(configurations)

                def build_unconfig(self, apply=True, attributes=None, **kwargs):
                    return self.build_config(apply=apply, attributes=attributes,
                                             unconfig=True, **kwargs)

                # +- DeviceAttributes
                #   +- RouterInstanceAttributes
                #     +- ExtranetAttributes
                #       +- InstanceIdAttributes
                class InstanceIdAttributes(ABC):

                    def build_config(self, apply=True, attributes=None, unconfig=False, **kwargs):
                        assert not apply
                        attributes = AttributesHelper(self, attributes)
                        configurations = CliConfigBuilder(unconfig=unconfig)

                        # +- DeviceAttributes
                        #   +- RouterInstanceAttributes
                        #     +- ExtranetAttributes
                        #       +- InstanceIdAttributes
                        #         +- EidRecordProviderAttributes
                        # --------------------------------------
                        # Add EidRecordProviderAttributes configurations under InstanceIdAttributes
                        for sub, attributes2 in attributes.mapping_values('eid_record_provider_attr', 
                                                                          sort=True, 
                                                                          keys=self.eid_record_provider_attr):
                            configurations.append_block(
                                sub.build_config(apply=False,
                                                 attributes=attributes2,
                                                 unconfig=unconfig,
                                                 instance_id=self.extranet_inst_id))

                        # +- DeviceAttributes
                        #   +- RouterInstanceAttributes
                        #     +- ExtranetAttributes
                        #       +- InstanceIdAttributes
                        #         +- EidRecordSubscriberAttributes
                        # ----------------------------------------
                        # Add EidRecordSubscriberAttributes configurations under InstanceIdAttributes
                        for sub, attributes2 in attributes.mapping_values('eid_record_subscriber_attr', 
                                                                          sort=True, 
                                                                          keys=self.eid_record_subscriber_attr):
                            configurations.append_block(
                                sub.build_config(apply=False,
                                                 attributes=attributes2,
                                                 unconfig=unconfig,
                                                 instance_id=self.extranet_inst_id))

                        return str(configurations)

                    def build_unconfig(self, apply=True, attributes=None, **kwargs):
                        return self.build_config(apply=apply, attributes=attributes,
                                                 unconfig=True, **kwargs)

                    # +- DeviceAttributes
                    #   +- RouterInstanceAttributes
                    #     +- ExtranetAttributes
                    #       +- InstanceIdAttributes
                    #         +- EidRecordProviderAttributes
                    class EidRecordProviderAttributes(ABC):

                        def build_config(self, apply=True, attributes=None, unconfig=False, **kwargs):
                            assert not apply
                            attributes = AttributesHelper(self, attributes)
                            configurations = CliConfigBuilder(unconfig=unconfig)

                            # extranet ext1
                            #   eid-record-provider instance-id 101 88.88.88.0/24
                            cfg_str = 'eid-record-provider instance-id {iid} {provider}'.\
                                        format(iid=kwargs['instance_id'], provider=self.ms_extranet_provider_eid)

                            # extranet ext1
                            #   eid-record-provider instance-id 101 88.88.88.0/24 bidirectional
                            if attributes.value('ms_extranet_provider_bidir') is True:
                                cfg_str += ' bidirectional'

                            configurations.append_line(attributes.format(cfg_str))

                            return str(configurations)

                        def build_unconfig(self, apply=True, attributes=None, **kwargs):
                            return self.build_config(apply=apply, attributes=attributes,
                                                     unconfig=True, **kwargs)

                    # +- DeviceAttributes
                    #   +- RouterInstanceAttributes
                    #     +- ExtranetAttributes
                    #       +- InstanceIdAttributes
                    #         +- EidRecordSubscriberAttributes
                    class EidRecordSubscriberAttributes(ABC):

                        def build_config(self, apply=True, attributes=None, unconfig=False, **kwargs):
                            assert not apply
                            attributes = AttributesHelper(self, attributes)
                            configurations = CliConfigBuilder(unconfig=unconfig)

                            # extranet ext1
                            #   eid-record-provider instance-id 101 88.88.88.0/24
                            cfg_str = 'eid-record-subscriber instance-id {iid} {subscriber}'.\
                                        format(iid=kwargs['instance_id'], subscriber=self.ms_extranet_subscriber_eid)

                            # extranet ext1
                            #   eid-record-provider instance-id 101 88.88.88.0/24 bidirectional
                            if attributes.value('ms_extranet_subscriber_bidir') is True:
                                cfg_str += ' bidirectional'

                            configurations.append_line(attributes.format(cfg_str))

                            return str(configurations)

                        def build_unconfig(self, apply=True, attributes=None, **kwargs):
                            return self.build_config(apply=apply, attributes=attributes,
                                                     unconfig=True, **kwargs)
