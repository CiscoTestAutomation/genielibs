
# Table of contents:
#     class Ldp:
#         class DeviceAttributes:
#             def build_config/build_unconfig:
#             class VrfAttributes:
#                 def build_config/build_unconfig:
#                 (class NeighborAttributes)
#                 class AddressFamilyAttributes:
#                     def build_config/build_unconfig:
#                     (class NeighborAttributes)
#             class InterfaceAttributes:
#                 def build_config/build_unconfig:
#                 class AddressFamilyAttributes:
#                     def build_config/build_unconfig:

from abc import ABC
import warnings
import re

from genie.conf.base.attributes import UnsupportedAttributeWarning, AttributesHelper
from genie.conf.base.cli import CliConfigBuilder
from genie.conf.base.config import CliConfig

from genie.libs.conf.address_family import AddressFamily
from genie.libs.conf.base import PasswordType
from genie.libs.conf.vrf import VrfSubAttributes

class Ldp(ABC):

    class DeviceAttributes(ABC):

        def build_config(self, apply=True, attributes=None, unconfig=False, **kwargs):
            attributes = AttributesHelper(self, attributes)
            configurations = CliConfigBuilder(unconfig=unconfig)

            # iosxr: mpls ldp (config-ldp)
            with configurations.submode_context('mpls ldp'):
                if unconfig and attributes.iswildcard:
                    configurations.submode_unconfig()

                # iosxr: mpls ldp / capabilities cisco ios-xr disable
                if attributes.value('capabilities_cisco_iosxr') is False:
                    configurations.append_line('capabilities cisco ios-xr disable')

                # iosxr: mpls ldp / default-vrf implicit-ipv4 disable
                if attributes.value('default_vrf_impl_ipv4') is False:
                    configurations.append_line('default-vrf implicit-ipv4 disable')

                # iosxr: mpls ldp / discovery (config-ldp-disc)
                with configurations.submode_context('discovery', cancel_empty=True):

                    # iosxr: mpls ldp / discovery / ds-tlv disable
                    if attributes.value('ds_tlv') is False:
                        configurations.append_line('ds-tlv disable')

                    # iosxr: mpls ldp / discovery / hello holdtime 1
                    configurations.append_line(attributes.format('hello holdtime {hello_holdtime}'))

                    # iosxr: mpls ldp / discovery / hello interval 1
                    configurations.append_line(attributes.format('hello interval {hello_interval}'))

                    # iosxr: mpls ldp / discovery / instance-tlv disable
                    if attributes.value('instance_tlv') is False:
                        configurations.append_line('instance-tlv disable')

                    # iosxr: mpls ldp / discovery / quick-start disable
                    if attributes.value('quickstart') is False:
                        configurations.append_line('quick-start disable')

                    # iosxr: mpls ldp / discovery / targeted-hello holdtime 1
                    configurations.append_line(attributes.format('targeted-hello holdtime {targeted_hello_holdtime}'))

                    # iosxr: mpls ldp / discovery / targeted-hello interval 1
                    configurations.append_line(attributes.format('targeted-hello interval {targeted_hello_interval}'))

                # iosxr: mpls ldp / entropy-label
                if attributes.value('entropy_label'):
                    configurations.append_line('entropy-label')

                # iosxr: mpls ldp / graceful-restart
                if attributes.value('gr'):
                    configurations.append_line('graceful-restart')

                # iosxr: mpls ldp / graceful-restart forwarding-state-holdtime 60
                configurations.append_line(attributes.format('graceful-restart forwarding-state-holdtime {gr_fwdstate_holdtime}'))

                # iosxr: mpls ldp / graceful-restart reconnect-timeout 60
                configurations.append_line(attributes.format('graceful-restart reconnect-timeout {gr_reconnect_timeout}'))

                # iosxr: mpls ldp / igp sync delay on-proc-restart 60
                configurations.append_line(attributes.format('igp sync delay on-proc-restart {igp_sync_delay_on_proc_restart}'))

                # iosxr: mpls ldp / igp sync delay on-session-up 5
                if attributes.value('igp_sync_delay_on_session_up') is False:
                    pass
                else:
                    configurations.append_line(attributes.format('igp sync delay on-session-up {igp_sync_delay_on_session_up}'))

                # iosxr: mpls ldp / nsr
                if attributes.value('nsr'):
                    configurations.append_line('nsr')

                # iosxr: mpls ldp / session backoff 100 200
                configurations.append_line(attributes.format('session backoff {session_backoff_init} {session_backoff_max}'))

                # iosxr: mpls ldp / session holdtime 15
                configurations.append_line(attributes.format('session holdtime {session_holdtime}'))

                # iosxr: mpls ldp / session protection
                # iosxr: mpls ldp / session protection duration 30
                # iosxr: mpls ldp / session protection duration infinite
                # iosxr: mpls ldp / session protection for someword
                # iosxr: mpls ldp / session protection for someword duration 30
                # iosxr: mpls ldp / session protection for someword duration infinite
                if attributes.value('session_protection') or attributes.value('session_protection_for_acl'):
                    cfg = 'session protection'
                    cfg += attributes.format(' for {session_protection_for_acl.name}', force=True)
                    if self.session_protection_dur is float('inf'):
                        cfg += ' duration infinite'
                    else:
                        cfg += attributes.format(' duration {session_protection_dur}', force=True)
                    configurations.append_line(cfg)

                # iosxr: mpls ldp / signalling dscp <0-63>
                configurations.append_line(attributes.format('signalling dscp {signalling_dscp}'))

                # iosxr: mpls ldp / log (config-ldp-log)
                with configurations.submode_context('log', cancel_empty=True):

                    # iosxr: mpls ldp / log / graceful-restart
                    if attributes.value('log_gr'):
                        configurations.append_line('graceful-restart')

                    # iosxr: mpls ldp / log / hello-adjacency
                    if attributes.value('log_hello_adj'):
                        configurations.append_line('hello-adjacency')

                    # iosxr: mpls ldp / log / neighbor
                    if attributes.value('log_neighbor'):
                        configurations.append_line('neighbor')

                    # iosxr: mpls ldp / log / nsr
                    if attributes.value('log_nsr'):
                        configurations.append_line('nsr')

                    # iosxr: mpls ldp / log / session-protection
                    if attributes.value('log_sess_prot'):
                        configurations.append_line('session-protection')

                # iosxr: mpls ldp / ltrace-buffer multiplier 1
                configurations.append_line(attributes.format('ltrace-buffer multiplier {ltrace_buffer_multiplier}'))

                for sub, attributes2 in attributes.mapping_values('vrf_attr', keys=self.vrfs, sort=True):
                    configurations.append_block(sub.build_config(apply=False, attributes=attributes2, unconfig=unconfig))

            if apply:
                if configurations:
                    self.device.configure(str(configurations), fail_invalid=True)
            else:
                return CliConfig(device=self.device, unconfig=unconfig,
                                 cli_config=configurations, fail_invalid=True)

        def build_unconfig(self, apply=True, attributes=None, **kwargs):
            return self.build_config(apply=apply, attributes=attributes, unconfig=True, **kwargs)

        class VrfAttributes(ABC):

            def build_config(self, apply=True, attributes=None, unconfig=False, **kwargs):
                assert not apply
                attributes = AttributesHelper(self, attributes)
                configurations = CliConfigBuilder(unconfig=unconfig)

                # iosxr: mpls ldp / vrf someword (config-ldp-vrf)
                with configurations.submode_context(
                        None if self.vrf_name == 'default' else attributes.format('vrf {vrf_name}', force=True)):
                    if self.vrf_name != 'default' and unconfig and attributes.iswildcard:
                        configurations.submode_unconfig()

                    # iosxr: mpls ldp / [vrf someword] / router-id 1.2.3.4
                    configurations.append_line(attributes.format('router-id {router_id}'))

                    # iosxr: mpls ldp / [vrf someword] / session downstream-on-demand with someword
                    configurations.append_line(attributes.format('session downstream-on-demand with {session_dod_acl.name}'))

                    # iosxr: mpls ldp / [vrf someword] / graceful-restart helper-peer maintain-on-local-reset for someword
                    configurations.append_line(attributes.format('graceful-restart helper-peer maintain-on-local-reset for {gr_maintain_acl.name}'))

                    for sub, attributes2 in attributes.mapping_values('address_family_attr', keys=self.address_families, sort=True):
                        configurations.append_block(sub.build_config(apply=False, attributes=attributes2, unconfig=unconfig))

                    for sub, attributes2 in attributes.mapping_values('interface_attr', keys=self.interfaces, sort=True):
                        configurations.append_block(sub.build_config(apply=False, attributes=attributes2, unconfig=unconfig))

                    # iosxr: mpls ldp / neighbor (config-ldp-nbr)
                    # iosxr: mpls ldp / vrf someword / neighbor (config-ldp-vrf-nbr)
                    with configurations.submode_context('neighbor', cancel_empty=True):

                        if self.vrf_name == 'default':
                            # iosxr: mpls ldp / neighbor / dual-stack tlv-compliance
                            if attributes.value('dualstack_tlv_compliance'):
                                configurations.append_line('dual-stack tlv-compliance')

                        if self.vrf_name == 'default':
                            # iosxr: mpls ldp / neighbor / dual-stack transport-connection max-wait <0-60>
                            configurations.append_line(attributes.format('dual-stack transport-connection max-wait {dualstack_transport_max_wait}'))

                        if self.vrf_name == 'default':
                            # iosxr: mpls ldp / neighbor / dual-stack transport-connection prefer ipv4
                            if attributes.value('dualstack_transport_prefer_ipv4'):
                                configurations.append_line('dual-stack transport-connection prefer ipv4')

                        # iosxr: mpls ldp / [vrf someword] / neighbor / password clear some clear password
                        # iosxr: mpls ldp / [vrf someword] / neighbor / password encrypted 060506324F41
                        if self.password_type is PasswordType.clear:
                            configurations.append_line(attributes.format('password clear {password}'))
                        elif self.password_type is PasswordType.encrypted:
                            configurations.append_line(attributes.format('password encrypted {password}'))

                        for neighbor, neighbor_attributes in attributes.mapping_values('neighbor_attr', keys=self.neighbors, sort=True):

                            # iosxr: mpls ldp / [vrf someword] / neighbor / 1.2.3.4:0 password disable
                            if neighbor_attributes.value('disable_password'):
                                configurations.append_line(neighbor_attributes.format('{neighbor} password disable', force_neighbor=True))
                            else:
                                # iosxr: mpls ldp / [vrf someword] / neighbor / 1.2.3.4:0 password clear some clear password
                                # iosxr: mpls ldp / [vrf someword] / neighbor / 1.2.3.4:0 password encrypted 060506324F41
                                if neighbor.password_type is PasswordType.clear:
                                    configurations.append_line(neighbor_attributes.format('{neighbor} password clear {password}', force_neighbor=True, inherited=False))
                                elif neighbor.password_type is PasswordType.encrypted:
                                    configurations.append_line(neighbor_attributes.format('{neighbor} password encrypted {password}', force_neighbor=True, inherited=False))

                return str(configurations)

            def build_unconfig(self, apply=True, attributes=None, **kwargs):
                return self.build_config(apply=apply, attributes=attributes, unconfig=True, **kwargs)

            class AddressFamilyAttributes(ABC):

                def build_config(self, apply=True, attributes=None, unconfig=False, **kwargs):
                    assert not apply
                    attributes = AttributesHelper(self, attributes)
                    configurations = CliConfigBuilder(unconfig=unconfig)

                    # iosxr: mpls ldp / address-family ipv4 (config-ldp-af)
                    # iosxr: mpls ldp / address-family ipv6 (config-ldp-af)
                    # iosxr: mpls ldp / vrf someword / address-family ipv4 (config-ldp-vrf-af)
                    with configurations.submode_context(attributes.format('address-family {address_family.value}', force=True)):
                        if unconfig and attributes.iswildcard:
                            configurations.submode_unconfig()

                        if self.vrf_name == 'default':
                            if self.targeted_hello_accept_from_acl:
                                # iosxr: mpls ldp / address-family ipv4|ipv6 / discovery targeted-hello accept from someword
                                configurations.append_line(attributes.format('discovery targeted-hello accept from {targeted_hello_accept_from_acl.name}'))
                            else:
                                # iosxr: mpls ldp / address-family ipv4|ipv6 / discovery targeted-hello accept
                                if attributes.value('targeted_hello_accept'):
                                    configurations.append_line('discovery targeted-hello accept')

                        if self.address_family is AddressFamily.ipv4 or self.vrf_name == 'default':
                            # iosxr: mpls ldp / [vrf someword] / address-family ipv4 / discovery transport-address 1.2.3.4
                            # iosxr: mpls ldp / address-family ipv6 / discovery transport-address 1:2::3
                            v = attributes.value('transport_address')
                            if v is not None:
                                if v == 'interface':
                                    pass
                                else:
                                    configurations.append_line(attributes.format('discovery transport-address {transport_address}'))

                        if self.address_family is AddressFamily.ipv4 or self.vrf_name == 'default':
                            # iosxr: mpls ldp / address-family ipv4 / label (config-ldp-af-lbl)
                            # iosxr: mpls ldp / vrf someword / address-family ipv4 / label (config-ldp-vrf-af-lbl)
                            # iosxr: mpls ldp / address-family ipv6 / label (config-ldp-af-lbl)
                            with configurations.submode_context('label', cancel_empty=True):

                                # iosxr: mpls ldp / address-family ipv4 / label / local (config-ldp-af-lbl-lcl)
                                # iosxr: mpls ldp / vrf someword / address-family ipv4 / label / local (config-ldp-vrf-af-lbl-lcl)
                                # iosxr: mpls ldp / address-family ipv6 / label / local (config-ldp-af-lbl-lcl)
                                with configurations.submode_context('local', cancel_empty=True):

                                    # iosxr: mpls ldp / address-family ipv4 / label / local / advertise (config-ldp-af-lbl-lcl-advt)
                                    # iosxr: mpls ldp / vrf someword / address-family ipv4 / label / local / advertise (config-ldp-vrf-af-lbl-lcl-advt)
                                    # iosxr: mpls ldp / address-family ipv6 / label / local / advertise (config-ldp-af-lbl-lcl-advt)
                                    with configurations.submode_context('advertise', cancel_empty=True):

                                        # iosxr: mpls ldp / [vrf someword] / address-family ipv4 / label / local / advertise / disable
                                        # iosxr: mpls ldp / address-family ipv6 / label / local / advertise / disable
                                        if attributes.value('advertise') is False:
                                            configurations.append_line('disable')

                                        # iosxr: mpls ldp / [vrf someword] / address-family ipv4 / label / local / advertise / explicit-null
                                        # iosxr: mpls ldp / [vrf someword] / address-family ipv4 / label / local / advertise / explicit-null for someword
                                        # iosxr: mpls ldp / [vrf someword] / address-family ipv4 / label / local / advertise / explicit-null for someword to someword2
                                        # iosxr: mpls ldp / [vrf someword] / address-family ipv4 / label / local / advertise / explicit-null to someword
                                        # iosxr: mpls ldp / address-family ipv6 / label / local / advertise / explicit-null
                                        # iosxr: mpls ldp / address-family ipv6 / label / local / advertise / explicit-null for someword
                                        # iosxr: mpls ldp / address-family ipv6 / label / local / advertise / explicit-null for someword to someword2
                                        # iosxr: mpls ldp / address-family ipv6 / label / local / advertise / explicit-null to someword
                                        if self.advertise_expnull_for_acl and self.advertise_expnull_to_acl:
                                            configurations.append_line(attributes.format('explicit-null for {advertise_expnull_for_acl.name} to {advertise_expnull_to_acl.name}'))
                                        elif self.advertise_expnull_to_acl:
                                            configurations.append_line(attributes.format('explicit-null to {advertise_expnull_to_acl.name}'))
                                        elif self.advertise_expnull_for_acl:
                                            configurations.append_line(attributes.format('explicit-null for {advertise_expnull_for_acl.name}'))
                                        elif attributes.value('advertise_expnull'):
                                            configurations.append_line('explicit-null')

                                        # iosxr: mpls ldp / address-family ipv4|ipv6 / label / local / advertise / for someword
                                        # iosxr: mpls ldp / address-family ipv4|ipv6 / label / local / advertise / for someword to someword2
                                        if self.advertise_for_acl and self.advertise_to_acl:
                                            configurations.append_line(attributes.format('for {advertise_for_acl.name} to {advertise_to_acl.name}'))
                                        else:
                                            configurations.append_line(attributes.format('for {advertise_for_acl.name}'))

                                        # iosxr: mpls ldp / [vrf someword] / address-family ipv4 / label / local / advertise / interface GigabitEthernet0/0/0/0
                                        # iosxr: mpls ldp / address-family ipv6 / label / local / advertise / interface GigabitEthernet0/0/0/0
                                        for v, attributes2 in attributes.sequence_values('advertise_interfaces'):
                                            configurations.append_line('interface {}'.format(v.name))

                                        for neighbor, neighbor_attributes in attributes.mapping_values('neighbor_attr', keys=self.neighbors, sort=True):

                                            # iosxr: mpls ldp / [vrf someword] / address-family ipv4 / label / local / advertise / to 1.2.3.4:0 for someword
                                            # iosxr: mpls ldp / address-family ipv6 / label / local / advertise / to 1.2.3.4:0 for someword
                                            configurations.append_line(neighbor_attributes.format('to {neighbor} for {advertise_for_acl.name}', force_neighbor=True, inherited=False))

                                    # iosxr: mpls ldp / [vrf someword] / address-family ipv4 / label / local / allocate for someword
                                    # iosxr: mpls ldp / address-family ipv6 / label / local / allocate for someword
                                    configurations.append_line(attributes.format('allocate for {allocate_for_acl.name}'))

                                    # iosxr: mpls ldp / [vrf someword] / address-family ipv4 / label / local / allocate for host-routes
                                    # iosxr: mpls ldp / address-family ipv6 / label / local / allocate for host-routes
                                    if attributes.value('allocate_for_host_routes'):
                                        configurations.append_line('allocate for host-routes')

                                    # iosxr: mpls ldp / [vrf someword] / address-family ipv4 / label / local / default-route
                                    # iosxr: mpls ldp / address-family ipv6 / label / local / default-route
                                    if attributes.value('default_route'):
                                        configurations.append_line('default-route')

                                    # iosxr: mpls ldp / [vrf someword] / address-family ipv4 / label / local / implicit-null-override for someword
                                    # iosxr: mpls ldp / address-family ipv6 / label / local / implicit-null-override for someword
                                    configurations.append_line(attributes.format('implicit-null-override for {impnull_override_for_acl.name}'))

                                # iosxr: mpls ldp / address-family ipv4 / label / remote (config-ldp-af-lbl-rmt)
                                # iosxr: mpls ldp / vrf someword / address-family ipv4 / label / remote (config-ldp-vrf-af-lbl-rmt)
                                # iosxr: mpls ldp / address-family ipv6 / label / remote (config-ldp-af-lbl-rmt)
                                with configurations.submode_context('remote', cancel_empty=True):

                                    # iosxr: mpls ldp / address-family ipv4|ipv6 / label / remote / accept (config-ldp-af-lbl-rmt-acpt)
                                    # iosxr: mpls ldp / vrf someword / address-family ipv4 / label / remote / accept (config-ldp-vrf-af-lbl-rmt-acpt)
                                    with configurations.submode_context('accept', cancel_empty=True):

                                        for neighbor, neighbor_attributes in attributes.mapping_values('neighbor_attr', keys=self.neighbors, sort=True):

                                            # iosxr: mpls ldp / [vrf someword] / address-family ipv4 / label / remote / accept / from 1.2.3.4:0 for someword
                                            # iosxr: mpls ldp / address-family ipv6 / label / remote / accept / from 1.2.3.4:0 for someword
                                            configurations.append_line(neighbor_attributes.format('from {neighbor} for {accept_for_acl.name}', force_neighbor=True))

                        for neighbor, neighbor_attributes in attributes.mapping_values('neighbor_attr', keys=self.neighbors, sort=True):

                            if self.vrf_name == 'default':
                                # iosxr: mpls ldp / address-family ipv4 / neighbor 1.2.3.4 targeted
                                # iosxr: mpls ldp / address-family ipv6 / neighbor 1:2::3 targeted
                                if neighbor_attributes.value('targeted'):
                                    configurations.append_line(neighbor_attributes.format('neighbor {neighbor.ip} targeted', force_neighbor=True))

                        if self.vrf_name == 'default':
                            # iosxr: mpls ldp / address-family ipv4|ipv6 / redistribute (config-ldp-af-redist)
                            with configurations.submode_context('redistribute', cancel_empty=True):

                                # iosxr: mpls ldp / address-family ipv4|ipv6 / redistribute / bgp (config-ldp-af-redist-bgp)
                                with configurations.submode_context(
                                        'bgp', cancel_empty=attributes.value('redist_bgp') is not True):

                                    # iosxr: mpls ldp / address-family ipv4|ipv6 / redistribute / bgp / advertise-to someword
                                    configurations.append_line(attributes.format('advertise-to {redist_bgp_advto_acl.name}'))

                                    # iosxr: mpls ldp / address-family ipv4|ipv6 / redistribute / bgp / as 1
                                    # iosxr: mpls ldp / address-family ipv4|ipv6 / redistribute / bgp / as 100.200
                                    # iosxr: mpls ldp / address-family ipv4|ipv6 / redistribute / bgp / as 65536
                                    configurations.append_line(attributes.format('as {redist_bgp_as}'))

                        if self.vrf_name == 'default':
                            # iosxr: mpls ldp / address-family ipv4|ipv6 / traffic-eng (config-ldp-af-te)
                            with configurations.submode_context('traffic-eng', cancel_empty=True):

                                # iosxr: mpls ldp / address-family ipv4|ipv6 / traffic-eng / auto-tunnel mesh (config-ldp-af-te-mesh)
                                with configurations.submode_context('auto-tunnel mesh', cancel_empty=True):

                                    # iosxr: mpls ldp / address-family ipv4|ipv6 / traffic-eng / auto-tunnel mesh / group <0-4294967295>
                                    # iosxr: mpls ldp / address-family ipv4|ipv6 / traffic-eng / auto-tunnel mesh / group all
                                    v = attributes.value('te_autotunnel_mesh_group_id')
                                    if v is not None:
                                        if v == 'all':
                                            configurations.append_line('group all')
                                        else:
                                            configurations.append_line(attributes.format('group {te_autotunnel_mesh_group_id}'))

                    return str(configurations)

                def build_unconfig(self, apply=True, attributes=None, **kwargs):
                    return self.build_config(apply=apply, attributes=attributes, unconfig=True, **kwargs)

        class InterfaceAttributes(ABC):

            def build_config(self, apply=True, attributes=None, unconfig=False, **kwargs):
                assert not apply
                attributes = AttributesHelper(self, attributes)
                configurations = CliConfigBuilder(unconfig=unconfig)

                # iosxr: mpls ldp / interface GigabitEthernet0/0/0/0 (config-ldp-if)
                # iosxr: mpls ldp / vrf someword / interface GigabitEthernet0/0/0/0 (config-ldp-vrf-if)
                with configurations.submode_context(attributes.format('interface {interface_name}', force=True)):
                    if unconfig and attributes.iswildcard:
                        configurations.submode_unconfig()

                    # iosxr: mpls ldp / interface GigabitEthernet0/0/0/0 / discovery hello dual-stack-tlv ipv4
                    # iosxr: mpls ldp / interface GigabitEthernet0/0/0/0 / discovery hello dual-stack-tlv ipv6
                    configurations.append_line(attributes.format('discovery hello dual-stack-tlv {disc_hello_dualstack_tlv.value}'))

                    # iosxr: mpls ldp / interface GigabitEthernet0/0/0/0 / discovery hello holdtime 1
                    configurations.append_line(attributes.format('discovery hello holdtime {hello_holdtime}', inherited=False))

                    # iosxr: mpls ldp / interface GigabitEthernet0/0/0/0 / discovery hello interval 1
                    configurations.append_line(attributes.format('discovery hello interval {hello_interval}', inherited=False))

                    # iosxr: mpls ldp / interface GigabitEthernet0/0/0/0 / discovery quick-start disable
                    if attributes.value('quickstart', inherited=False) is False:
                        configurations.append_line('discovery quick-start disable')

                    # iosxr: mpls ldp / interface GigabitEthernet0/0/0/0 / igp sync delay on-session-up 5
                    # iosxr: mpls ldp / interface GigabitEthernet0/0/0/0 / igp sync delay on-session-up disable
                    if attributes.value('igp_sync_delay_on_session_up') is False:
                        configurations.append_line('igp sync delay on-session-up disable')
                    else:
                        configurations.append_line(attributes.format('igp sync delay on-session-up {igp_sync_delay_on_session_up}', inherited=False))

                    for sub, attributes2 in attributes.mapping_values('address_family_attr', keys=self.address_families, sort=True):
                        configurations.append_block(sub.build_config(apply=False, attributes=attributes2, unconfig=unconfig))

                return str(configurations)

            def build_unconfig(self, apply=True, attributes=None, **kwargs):
                return self.build_config(apply=apply, attributes=attributes, unconfig=True, **kwargs)

            class AddressFamilyAttributes(ABC):

                def build_config(self, apply=True, attributes=None, unconfig=False, **kwargs):
                    assert not apply
                    attributes = AttributesHelper(self, attributes)
                    configurations = CliConfigBuilder(unconfig=unconfig)

                    # iosxr: mpls ldp / [vrf someword] / interface GigabitEthernet0/0/0/0 / address-family ipv4 (config-ldp-vrf-if-af)
                    # iosxr: mpls ldp / interface GigabitEthernet0/0/0/0 / address-family ipv6 (config-ldp-if-af)
                    with configurations.submode_context(attributes.format('address-family {address_family.value}', force=True)):
                        if unconfig and attributes.iswildcard:
                            configurations.submode_unconfig()

                        # iosxr: mpls ldp / [vrf someword] / interface GigabitEthernet0/0/0/0 / address-family ipv4 / discovery transport-address 1.2.3.4
                        # iosxr: mpls ldp / interface GigabitEthernet0/0/0/0 / address-family ipv6 / discovery transport-address 1:2::3
                        # iosxr: mpls ldp / [vrf someword] / interface GigabitEthernet0/0/0/0 / address-family ipv4 / discovery transport-address interface
                        # iosxr: mpls ldp / interface GigabitEthernet0/0/0/0 / address-family ipv6 / discovery transport-address interface
                        v = attributes.value('transport_address')
                        if v is not None:
                            if v == 'interface':
                                configurations.append_line('discovery transport-address interface')
                            else:
                                configurations.append_line(attributes.format('discovery transport-address {transport_address}', inherited=False))

                        # iosxr: mpls ldp / interface GigabitEthernet0/0/0/0 / address-family ipv4|ipv6 / igp auto-config disable
                        if attributes.value('igp_autoconfig') is False:
                            configurations.append_line('igp auto-config disable')

                        # iosxr: mpls ldp / interface GigabitEthernet0/0/0/0 / address-family ipv4|ipv6 / mldp disable

                    return str(configurations)

                def build_unconfig(self, apply=True, attributes=None, **kwargs):
                    return self.build_config(apply=apply, attributes=attributes, unconfig=True, **kwargs)

# iosxr: mpls ldp / mldp (config-ldp-mldp)
# iosxr: mpls ldp / mldp / logging internal
# iosxr: mpls ldp / mldp / logging notifications
# iosxr: mpls ldp / mldp / vrf someword (config-ldp-mldp-vrf)
# iosxr: mpls ldp / mldp / address-family ipv4 (config-ldp-mldp-af)
# iosxr: mpls ldp / mldp / vrf someword / address-family ipv4 (config-ldp-mldp-vrf-af)
# iosxr: mpls ldp / mldp / [vrf someword] / address-family ipv4 / carrier-supporting-carrier
# iosxr: mpls ldp / mldp / [vrf someword] / address-family ipv4 / forwarding recursive
# iosxr: mpls ldp / mldp / [vrf someword] / address-family ipv4 / forwarding recursive route-policy someword
# iosxr: mpls ldp / mldp / [vrf someword] / address-family ipv4 / make-before-break
# iosxr: mpls ldp / mldp / [vrf someword] / address-family ipv4 / make-before-break delay <0-600>
# iosxr: mpls ldp / mldp / [vrf someword] / address-family ipv4 / make-before-break delay <0-600> <0-60>
# iosxr: mpls ldp / mldp / [vrf someword] / address-family ipv4 / make-before-break route-policy someword
# iosxr: mpls ldp / mldp / [vrf someword] / address-family ipv4 / mofrr
# iosxr: mpls ldp / mldp / [vrf someword] / address-family ipv4 / mofrr route-policy someword
# iosxr: mpls ldp / mldp / [vrf someword] / address-family ipv4 / neighbor 1.2.3.4 route-policy someword in
# iosxr: mpls ldp / mldp / [vrf someword] / address-family ipv4 / neighbor route-policy someword in
# iosxr: mpls ldp / mldp / [vrf someword] / address-family ipv4 / recursive-fec
# iosxr: mpls ldp / mldp / [vrf someword] / address-family ipv4 / recursive-fec route-policy someword
# iosxr: mpls ldp / mldp / [vrf someword] / address-family ipv4 / rib unicast-always
# iosxr: mpls ldp / mldp / [vrf someword] / address-family ipv4 / static mp2mp 1.2.3.4 1
# iosxr: mpls ldp / mldp / [vrf someword] / address-family ipv4 / static p2mp 1.2.3.4 1
# iosxr: mpls ldp / interface GigabitEthernet0/0/0/0 / address-family ipv4|ipv6 / mldp disable

