'''
IOSXE specific configurations for MLD feature object.
'''

# Python
from abc import ABC

# Genie
from genie.decorator import managedattribute
from genie.conf.base.config import CliConfig
from genie.conf.base.cli import CliConfigBuilder
from genie.conf.base.attributes import UnsupportedAttributeWarning, \
                                       AttributesHelper

# Structure Hierarchy:
# Mld
# +-- DeviceAtributes
#       +-- VrfAttributes
#             +-- InterfaceAttributes


class Mld(ABC):

    class DeviceAttributes(ABC):

        def build_config(self, apply=True, attributes=None, unconfig=False,
                         **kwargs):
            assert not kwargs, kwargs
            attributes = AttributesHelper(self, attributes)
            configurations = CliConfigBuilder(unconfig=unconfig)
 
            # VrfAttributes
            for sub, attributes2 in attributes.mapping_values('vrf_attr',
                    sort=True, keys=self.vrf_attr):
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

            
        class VrfAttributes(ABC):

            def build_config(self, apply=True, attributes=None, unconfig=False,
                             **kwargs):
                assert not kwargs, kwargs
                attributes = AttributesHelper(self, attributes)
                configurations = CliConfigBuilder(unconfig=unconfig)

                # global_max_groups
                if attributes.value('global_max_groups'):
                    cfg_str = 'ipv6 mld state-limit {global_max_groups}' \
                        if self.vrf_id == 'default' else \
                            'ipv6 mld vrf {vrf_id} state-limit {global_max_groups}'

                    configurations.append_line(attributes.format(cfg_str, force=True))

                # ipv6 mld [vrf <vrf>] ssm-map enable
                if hasattr(attributes.value('ssm'), 'data'):
                    if attributes.value('ssm').data:
                        cfg_str = 'ipv6 mld ssm-map enable' \
                            if self.vrf_id == 'default' else \
                                'ipv6 mld vrf {} ssm-map enable'.format(self.vrf_id)

                        configurations.append_line(attributes.format(cfg_str))

                # Ssm Attributes under vrf level config
                for ssm, attributes2 in attributes.sequence_values('ssm', sort=True):
                    kwargs = {'vrf':self.vrf_id}
                    if unconfig:
                        configurations.append_block(ssm.build_unconfig(
                            apply=False, attributes=attributes2, **kwargs))
                    else:
                        configurations.append_block(ssm.build_config(
                            apply=False, attributes=attributes2, **kwargs))

                # InterfaceAttributes
                for sub, attributes2 in attributes.mapping_values('interface_attr',
                        sort=True, keys=self.interface_attr):
                            configurations.append_block(
                                sub.build_config(apply=False,
                                                 attributes=attributes2,
                                                 unconfig=unconfig))

                return str(configurations)

            def build_unconfig(self, apply=True, attributes=None, **kwargs):
                return self.build_config(apply=apply, attributes=attributes,
                                         unconfig=True, **kwargs)

            
            class InterfaceAttributes(ABC):

                def build_config(self, apply=True, attributes=None, unconfig=False,
                                 **kwargs):
                    assert not kwargs, kwargs
                    attributes = AttributesHelper(self, attributes)
                    configurations = CliConfigBuilder(unconfig=unconfig)

                    with configurations.submode_context(
                        attributes.format('interface {intf}', force=True)):

                        # enable
                        if attributes.value('enable'):
                            configurations.append_line('ipv6 mld router')

                        # group_policy
                        if attributes.value('group_policy'):
                            configurations.append_line(
                                attributes.format('ipv6 mld access-group {group_policy}'))

                        # immediate_leave  -- not supported on iosxe

                        # max_groups
                        if attributes.value('max_groups'):
                            configurations.append_line(
                                attributes.format('ipv6 mld limit {max_groups}'))

                        # query_interval
                        if attributes.value('query_interval'):
                            configurations.append_line(
                                attributes.format('ipv6 mld query-interval {query_interval}'))

                        # query_max_response_time
                        if attributes.value('query_max_response_time'):
                            configurations.append_line(
                                attributes.format('ipv6 mld query-max-response-time '
                                                  '{query_max_response_time}'))

                        # version  --  not supported on iosxe

                        # robustness_variable  --  not supported on iosxe

                        # Groups Attributes under top level config
                        for groups, attributes2 in attributes.sequence_values(
                                'groups', sort=True):
                            if unconfig:
                                configurations.append_block(groups.build_unconfig(
                                    apply=False, attributes=attributes2, **kwargs))
                            else:
                                configurations.append_block(groups.build_config(
                                    apply=False, attributes=attributes2, **kwargs))

                    return str(configurations)

                def build_unconfig(self, apply=True, attributes=None, **kwargs):
                    return self.build_config(apply=apply, attributes=attributes,
                                             unconfig=True, **kwargs)
