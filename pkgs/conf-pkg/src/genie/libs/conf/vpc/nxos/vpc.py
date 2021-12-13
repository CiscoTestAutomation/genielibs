'''
NXOS specific configurations for Vpc feature object.
'''

# Python
from abc import ABC

# Genie
from genie.conf.base.config import CliConfig
from genie.conf.base.cli import CliConfigBuilder
from genie.conf.base.attributes import AttributesHelper


# Structure Hierarchy:
# Vpc
# +-- DeviceAttributes
#     +-- DomainAttribute


class Vpc(ABC):

    class DeviceAttributes(ABC):

        def build_config(self, apply=True, attributes=None, unconfig=False,
                         **kwargs):
            assert not kwargs, kwargs
            attributes = AttributesHelper(self, attributes)
            configurations = CliConfigBuilder(unconfig=unconfig)

            # feature vpc
            if attributes.value('enabled'):
                if unconfig is False:
                    configurations.append_line(
                        attributes.format('feature vpc'))

            # Make sure that only enabled was provided in attributes
                # If wildcard,  then delete everything
                elif unconfig and\
                    attributes.attributes == {'enabled': {True: None}} or \
                        attributes.iswildcard:
                    configurations.append_line('no feature vpc', raw=True)
                    if apply:
                        if configurations:
                            self.device.configure(configurations)
                    else:
                        return CliConfig(device=self.device, unconfig=unconfig,
                                         cli_config=configurations)

            # DomainAttribute
            for sub, attributes2 in attributes.mapping_values('domain_attr',
                                                              sort=True, keys=self.domain_attr):
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
            return self.build_config(apply=apply, attributes=attributes, unconfig=True, **kwargs)

        class DomainAttributes(ABC):

            def build_config(self, apply=True, attributes=None, unconfig=False,
                             **kwargs):
                assert not kwargs, kwargs
                attributes = AttributesHelper(self, attributes)
                configurations = CliConfigBuilder(unconfig=unconfig)
                with configurations.submode_context(attributes.format(
                        'vpc domain {domain_id}', force=True)):
                    if unconfig and attributes.iswildcard:
                        configurations.submode_unconfig()

                   # nxos: auto-recovery
                    if attributes.value('auto_recovery_enabled'):
                        configurations.append_line(
                            attributes.format('auto-recovery'))

                    # nxos: auto-recovery reload-delay <value>
                    if attributes.value('auto_recovery_interval'):
                        configurations.append_line(
                            attributes.format('auto-recovery reload-delay {auto_recovery_interval}'))

                    # nxos: delay restore <value>
                    if attributes.value('delay_restore_vpc'):
                        configurations.append_line(
                            attributes.format('delay restore {delay_restore_vpc}'))

                    # nxos: delay restore interface-vlan  <value>
                    if attributes.value('delay_restore_svi'):
                        configurations.append_line(
                            attributes.format('delay restore interface-vlan {delay_restore_svi}'))

                    # nxos: delay restore orphan-port  <value>
                    if attributes.value('delay_restore_orphan'):
                        configurations.append_line(
                            attributes.format('delay restore orphan-port {delay_restore_orphan}'))

                    # nxos: dual-active exclude interface-vlan <value>
                    if attributes.value('dual_active_exclude_svi'):
                        configurations.append_line(
                            attributes.format('dual-active exclude interface-vlan {dual_active_exclude_svi}'))

                    # nxos: fast-convergence
                    if attributes.value('fast_convergence_enabled'):
                        configurations.append_line(
                            attributes.format('fast-convergence'))

                    # nxos: graceful consistency-check
                    if attributes.value('graceful_cc_enabled'):
                        configurations.append_line(
                            attributes.format('graceful consistency-check'))

                    # nxos: ip arp synchronize
                    if attributes.value('ip_arp_sync_enabled'):
                        configurations.append_line(
                            attributes.format('ip arp synchronize'))

                    # nxos: ipv6 nd synchronize
                    if attributes.value('ipv6_nd_sync_enabled'):
                        configurations.append_line(
                            attributes.format('ipv6 nd synchronize'))

                    # nxos: layer3 peer-router
                    if attributes.value('l3_peer_router_enabled'):
                        configurations.append_line(
                            attributes.format('layer3 peer-router'))

                    # nxos: layer3 peer-router syslog
                    if attributes.value('l3_peer_router_syslog_enabled'):
                        configurations.append_line(
                            attributes.format('layer3 peer-router syslog'))

                    # nxos: layer3 peer-router syslog interval <value>
                    if attributes.value('l3_peer_router_syslog_intvl'):
                        configurations.append_line(
                            attributes.format('layer3 peer-router syslog interval {l3_peer_router_syslog_intvl}'))

                    # nxos: mac-address bpdu source version <value>
                    if attributes.value('mac_bpdu_src_ver'):
                        configurations.append_line(
                            attributes.format('mac-address bpdu source version {mac_bpdu_src_ver}'))

                    # nxos: peer-gateway
                    if attributes.value('peer_gw_enabled'):
                        configurations.append_line(
                            attributes.format('peer-gateway'))

                    # nxos: peer-gateway exclude-vlan <value>
                    if attributes.value('peer_gw_exlude_vlan'):
                        configurations.append_line(
                            attributes.format('peer-gateway exclude-vlan {peer_gw_exlude_vlan}'))

                    # nxos: peer-switch
                    if attributes.value('peer_switch_enabled'):
                        configurations.append_line(
                            attributes.format('peer-switch'))

                    # nxos: role priority <value>
                    if attributes.value('role_priority'):
                        configurations.append_line(
                            attributes.format('role priority {role_priority}'))

                    # nxos: shutdown
                    if attributes.value('shutdown'):
                        configurations.append_line(
                            attributes.format('shutdown'))

                    # nxos: system-mac <value>
                    if attributes.value('system_mac'):
                        configurations.append_line(
                            attributes.format('system-mac {system_mac}'))

                    # nxos: system-priority <value>
                    if attributes.value('system_priority'):
                        configurations.append_line(
                            attributes.format('system-priority {system_priority}'))

                    # nxos: track <value>
                    if attributes.value('track'):
                        configurations.append_line(
                            attributes.format('track {track}'))

                    # nxos: virtual peer-link destination <value>
                    if attributes.value('virtual_peer_link_ip'):
                        configurations.append_line(
                            attributes.format('virtual peer-link destination {virtual_peer_link_ip}'))

                    # nxos: keepalive attributes
                    if attributes.value('keepalive_dst_ip'):
                        keepalive_cfg = 'peer-keepalive destination {keepalive_dst_ip} '

                        if attributes.value('keepalive_src_ip'):
                            keepalive_cfg += 'source {keepalive_src_ip} '

                        if attributes.value('keepalive_vrf'):
                            keepalive_cfg += 'vrf {keepalive_vrf} '

                        if attributes.value('keepalive_udp_port'):
                            keepalive_cfg += 'udp-port {keepalive_udp_port} '

                        if attributes.value('keepalive_interval'):
                            keepalive_cfg += 'interval {keepalive_interval} '

                        if attributes.value('keepalive_timeout'):
                            keepalive_cfg += 'timeout {keepalive_timeout} '

                        if attributes.value('keepalive_tos'):
                            keepalive_cfg += 'tos {keepalive_tos} '

                        if attributes.value('keepalive_tos_byte'):
                            keepalive_cfg += 'tos-byte {keepalive_tos_byte} '

                        if attributes.value('keepalive_precedence'):
                            keepalive_cfg += 'precedence {keepalive_precedence}'

                        configurations.append_line(
                            attributes.format(keepalive_cfg))

                return str(configurations)

            def build_unconfig(self, apply=True, attributes=None, **kwargs):
                return self.build_config(apply=apply, attributes=attributes, unconfig=True, **kwargs)
