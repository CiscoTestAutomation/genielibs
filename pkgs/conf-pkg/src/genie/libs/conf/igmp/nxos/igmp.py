'''
NXOS specific configurations for Igmp feature object.
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
# Igmp
# +-- DeviceAtributes
#       +-- VrfAttributes
#             +-- InterfaceAttributes


class Igmp(ABC):

    class DeviceAttributes(ABC):

        def build_config(self, apply=True, attributes=None, unconfig=False,
                         **kwargs):
            assert not kwargs, kwargs
            attributes = AttributesHelper(self, attributes)
            configurations = CliConfigBuilder(unconfig=unconfig)

            # require_router_alert
            if attributes.value('require_router_alert'):
                configurations.append_line('ip igmp enforce-router-alert')
 
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

                # global_max_groups -- not supported on nxos

                with configurations.submode_context(
                    attributes.format('vrf context {vrf_id}' if 
                            self.vrf_id != 'default' else '', force=True)):
                    if unconfig and attributes.iswildcard and self.vrf_id != 'default':
                        configurations.submode_unconfig()

                    # Ssm Attributes under vrf level config
                    for ssm, attributes2 in attributes.sequence_values('ssm', sort=True):
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
                            configurations.append_line('ip pim sparse-mode')

                        # last_member_query_interval -- not supported on nxos

                        # group_policy
                        if attributes.value('group_policy'):
                            configurations.append_line(
                                attributes.format('ip igmp access-group {group_policy}'))

                        # immediate_leave
                        if attributes.value('immediate_leave'):
                            configurations.append_line('ip igmp immediate-leave')

                        # max_groups
                        if attributes.value('max_groups'):
                            configurations.append_line(
                                attributes.format('ip igmp state-limit {max_groups}'))

                        # query_interval
                        if attributes.value('query_interval'):
                            configurations.append_line(
                                attributes.format('ip igmp query-interval {query_interval}'))

                        # query_max_response_time
                        if attributes.value('query_max_response_time'):
                            configurations.append_line(
                                attributes.format('ip igmp query-max-response-time '
                                                  '{query_max_response_time}'))

                        # robustness_variable
                        if attributes.value('robustness_variable'):
                            configurations.append_line(
                                attributes.format('ip igmp robustness-variable '
                                                  '{robustness_variable}'))

                        # version
                        if attributes.value('version'):
                            configurations.append_line(
                                attributes.format('ip igmp version {version}'))


                        # Mroute Attributes under top level config
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
