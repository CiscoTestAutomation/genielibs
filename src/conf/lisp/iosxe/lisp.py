from abc import ABC
import warnings

from genie.conf.base.attributes import UnsupportedAttributeWarning,\
    AttributesHelper
from genie.conf.base.config import CliConfig
from genie.conf.base.cli import CliConfigBuilder
from genie.conf.base import Interface
from genie.libs.conf.vrf import VrfSubAttributes


class Lisp(ABC):
    class DeviceAttributes(ABC):

        def build_config(self, devices=None, apply=True, attributes=None,
                         unconfig=False, **kwargs):

            attributes = AttributesHelper(self, attributes)
            configurations = CliConfigBuilder(unconfig=unconfig)

            vrf = list(self.vrf_attr.keys())
            with configurations.submode_context(
                attributes.format('router lisp {router_lisp_id}', force=True) if self.router_lisp_id is not None else
                    attributes.format('router lisp', force=True)):

                if unconfig and attributes.iswildcard:
                        configurations.submode_unconfig()

                for sub, attributes2 in attributes.mapping_values('vrf_attr', sort=True):
                    configurations.append_block(sub.build_config(apply=False,
                                                                 attributes=attributes2,
                                                                 unconfig=unconfig,
                                                                 **kwargs))

            if len(self.vrf_attr.keys()) > 1:
                raise Exception('One Vrf must be part of \'device_attr\', '
                                'but it has {vrf}'.format(vrf=vrf))
            if apply:
                if configurations:
                    self.device.configure(str(configurations))
            else:
                return CliConfig(device=self.device, unconfig=unconfig,
                                 cli_config=configurations)

        def build_unconfig(self, apply=True, attributes=None, **kwargs):
            return self.build_config(apply=apply, attributes=attributes, unconfig=True, **kwargs)

        class VrfAttributes(ABC):

            def build_config(self, devices=None, apply=True, attributes=None,
                             unconfig=False, **kwargs):
                attributes = AttributesHelper(self, attributes)
                # List containing configuration for this loop
                # Instantiate configurations
                configurations = CliConfigBuilder(unconfig=unconfig)
                vrf = self.vrf_name
                if attributes.value('security'):
                    configurations.append_line(attributes.format('security {security}'))
                if attributes.value('locator_table'):
                    configurations.append_line(attributes.format('locator-table {locator_table}'))
                if attributes.value('control_packet'):
                    configurations.append_line(attributes.format('control-packet mtu {control_packet}'))
                if attributes.value('ddt'):
                    configurations.append_line(attributes.format('ddt {ddt}'))
                if attributes.value('decapsulation'):
                    configurations.append_line(attributes.format('decapsulation {decapsulation}'))
                if attributes.value('default'):
                    configurations.append_line(attributes.format('default {default}'))
                if attributes.value('disable_ttl_propagate'):
                    configurations.append_line(attributes.format('disable-ttl-propagate'))
                if attributes.value('loc_reach_algorithm'):
                    configurations.append_line(attributes.format('loc-reach-algorithm {loc_reach_algorithm}'))
                if attributes.value('locator'):
                    configurations.append_line(attributes.format('locator default-set {locator}'))
                if attributes.value('locator_down'):
                    configurations.append_line(attributes.format('locator-down {locator_down}'))
                if attributes.value('map_request'):
                    configurations.append_line(attributes.format('map-request itr-rlocs {map_request}'))

                for sub, attributes2 in attributes.mapping_values('locatorset_attr', keys=self.locatorset_attr.keys()):
                    configurations.append_block(sub.build_config(apply=False,
                                                attributes=attributes2,
                                                unconfig=unconfig,
                                                **kwargs))

                for sub, attributes2 in attributes.mapping_values('service_attr', keys=self.service_attr.keys()):
                    configurations.append_block(sub.build_config(apply=False,
                                                attributes=attributes2, vrf=vrf,
                                                unconfig=unconfig,
                                                **kwargs))

                for sub, attributes2 in attributes.mapping_values('instance_attr', keys=self.instance_attr.keys()):
                    configurations.append_block(sub.build_config(apply=False,
                                                attributes=attributes2,
                                                unconfig=unconfig, vrf=vrf,
                                                **kwargs))

                for sub, attributes2 in attributes.mapping_values('site_attr', keys=self.site_attr.keys()):
                    configurations.append_block(sub.build_config(apply=False,
                                                attributes=attributes2,
                                                unconfig=unconfig,
                                                **kwargs))

                for sub, attributes2, in attributes.mapping_values('locator_scope_attr',
                                                                   keys=self.locator_scope_attr.keys()):
                    configurations.append_block(sub.build_config(apply=False,
                                                attributes=attributes2,
                                                unconfig=unconfig,
                                                **kwargs))

                return str(configurations)

            class InstanceAttributes(ABC):

                def build_config(self, devices=None, apply=True, attributes=None,
                                 unconfig=False, **kwargs):
                    attributes = AttributesHelper(self, attributes)
                    configurations = CliConfigBuilder(unconfig=unconfig)
                    with configurations.submode_context(attributes.format('instance-id {instance_id}', force=True)):
                        if unconfig and attributes.iswildcard:
                            configurations.submode_unconfig()
                        for sub, attributes2 in attributes.mapping_values('service_attr',
                                                                          keys=self.service_attr.keys(),
                                                                          inherited=False):
                            configurations.append_block(sub.build_config(apply=False,
                                                                         attributes=attributes2,
                                                                         unconfig=unconfig,
                                                                         **kwargs))
                        for sub, attributes2 in attributes.mapping_values('dynamic_eid_attr',
                                                                          keys=self.dynamic_eid_attr.keys(),
                                                                          inherited=False):
                            configurations.append_block(sub.build_config(apply=False,
                                                                         attributes=attributes2,
                                                                         unconfig=unconfig,
                                                                         **kwargs))

                    return str(configurations)

                def build_unconfig(self, apply=True, attributes=None, **kwargs):
                    return self.build_config(apply=apply, attributes=attributes, unconfig=True, **kwargs)

            class LocatorScopeAttributes(ABC):

                def build_config(self, devices=None, apply=True, attributes=None,
                                 unconfig=False, **kwargs):
                    attributes = AttributesHelper(self, attributes)
                    configurations = CliConfigBuilder(unconfig=unconfig)
                    with configurations.submode_context(attributes.format('locator-scope {locator_scope_name}',
                                                                          force=True)):
                        if unconfig and attributes.iswildcard:
                            configurations.submode_unconfig()

                        if attributes.value('rloc_prefix'):
                            configurations.append_line(attributes.format('rloc-prefix {rloc_prefix}'))
                        if attributes.value('rtr_locator_set'):
                            configurations.append_line(attributes.format('rtr-locator-set {rtr_locator_set}'))
                    return str(configurations)

                def build_unconfig(self, apply=True, attributes=None, **kwargs):
                    return self.build_config(apply=apply, attributes=attributes, unconfig=True, **kwargs)

            class ServiceAttributes(ABC):

                def build_config(self, devices=None, apply=True, attributes=None,
                                 unconfig=False, **kwargs):
                    attributes = AttributesHelper(self, attributes)
                    configurations = CliConfigBuilder(unconfig=unconfig)
                    with configurations.submode_context(attributes.format('service {service_name}', force=True)):
                        if unconfig and attributes.iswildcard:
                            configurations.submode_unconfig()

                        if attributes.value('eid_table'):
                            configurations.append_line(attributes.format('eid-table {eid_table}'))
                        if attributes.value('itr_enabled'):
                            configurations.append_line(attributes.format('itr'))
                        if attributes.value('etr_enabled'):
                            configurations.append_line(attributes.format('etr'))
                        if attributes.value('map_resolver_enabled'):
                            configurations.append_line(attributes.format('map-resolver'))
                        if attributes.value('map_server_enabled'):
                            configurations.append_line(attributes.format('map-server'))
                        if attributes.value('encapsulation'):
                            configurations.append_line(attributes.format('encapsulation {encapsulation.name}'))
                        if attributes.value('itr_values'):
                            for val in self.itr_values:
                                configurations.append_line(attributes.format('itr {}'.format(val)))
                        if attributes.value('etr_values'):
                            for val in self.etr_values:
                                configurations.append_line(attributes.format('etr {}'.format(val)))
                        if attributes.value('database_mapping'):
                            configurations.append_line(attributes.format('database-mapping {database_mapping}'))
                        if attributes.value('map_request_source'):
                            configurations.append_line(attributes.format('map-request-source {map_request_source}'))
                        if attributes.value('use_petr'):
                            configurations.append_line(attributes.format('use-petr {use_petr}'))
                        if attributes.value('site_registrations'):
                            configurations.append_line(attributes.format(
                                'site-registrations limit {site_registrations}'))
                        if attributes.value('map_cache_persistence_interval'):
                            configurations.append_line(attributes.format(
                                'map-cache-persistent interval {map_cache_persistence_interval}'))
                        if self.service_name == 'ethernet':
                            if attributes.value('eth_db_map'):
                                for mapping in self.eth_db_map:
                                    configurations.append_line(attributes.format('database-mapping {}'.format(mapping)))
                        if self.service_name == 'ipv4':
                            if attributes.value('ipv4_db_map'):
                                for mapping in self.ipv4_db_map:
                                    configurations.append_line(attributes.format('database-mapping {}'.format(mapping)))
                        if self.service_name == 'ipv6':
                            if attributes.value('ipv6_db_map'):
                                for mapping in self.ipv6_db_map:
                                    configurations.append_line(attributes.format('database-mapping {}'.format(mapping)))
                        if attributes.value('map_cache_limit'):
                            configurations.append_line(attributes.format('map-cache-limit {map_cache_limit}'))

                    return str(configurations)

                def build_unconfig(self, apply=True, attributes=None, **kwargs):
                    return self.build_config(apply=apply, attributes=attributes, unconfig=True, **kwargs)

            class LocatorSetAttributes(ABC):

                def build_config(self, devices=None, apply=True, attributes=None,
                                 unconfig=False, **kwargs):
                    attributes = AttributesHelper(self, attributes)
                    configurations = CliConfigBuilder(unconfig=unconfig)
                    with configurations.submode_context(attributes.format('locator-set {locator_set_name}',
                                                                          force=True)):
                        if unconfig and attributes.iswildcard:
                            configurations.submode_unconfig()

                        if attributes.value('rloc_value'):
                            configurations.append_line(attributes.format('{rloc_value}'))

                        if attributes.value('auto_discover_rlocs'):
                            configurations.append_line(attributes.format('auto-discover-rlocs'))

                    return str(configurations)

                def build_unconfig(self, apply=True, attributes=None, **kwargs):
                    return self.build_config(apply=apply, attributes=attributes, unconfig=True, **kwargs)

            class SiteAttributes(ABC):

                def build_config(self, devices=None, apply=True, attributes=None,
                                 unconfig=False, **kwargs):
                    attributes = AttributesHelper(self, attributes)
                    configurations = CliConfigBuilder(unconfig=unconfig)
                    with configurations.submode_context(attributes.format('site {site_name}', force=True)):
                        if unconfig and attributes.iswildcard:
                            configurations.submode_unconfig()
                        if attributes.value('authentication_key'):
                            configurations.append_line(attributes.format('authentication-key {authentication_key}'))
                        if attributes.value('eid_records'):
                            for record in self.eid_records:
                                configurations.append_line(attributes.format('eid-record {}'.format(record)))

                    return str(configurations)

                def build_unconfig(self, apply=True, attributes=None, **kwargs):
                    return self.build_config(apply=apply, attributes=attributes, unconfig=True, **kwargs)

            # TODO finish implementing Dynamic EID subattribute
            class DynamicEIDAttributes(ABC):

                def build_config(self, devices=None, apply=True, attributes=None,
                                 unconfig=False, **kwargs):
                    attributes = AttributesHelper(self, attributes)
                    configurations = CliConfigBuilder(unconfig=unconfig)
                    with configurations.submode_context(attributes.format(
                            'dynamic-eid {dynamic_eid_name}', force=True)):
                        if attributes.value('database_mapping'):
                            configurations.append_line(attributes.format('database-mapping {database_mapping}'))
                    return str(configurations)

                def build_unconfig(self, apply=True, attributes=None, **kwargs):
                    return self.build_config(apply=apply, attributes=attributes, unconfig=True, **kwargs)
