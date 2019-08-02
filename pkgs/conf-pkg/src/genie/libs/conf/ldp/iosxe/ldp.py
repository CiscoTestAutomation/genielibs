#
# DeviceAttributes +---------+ VrfAttributes +--------+ NeighborAttributes
#                  +
#                  +
#                  +---------+ InterfaceAttributes
#
#

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

            if attributes.iswildcard:
                # iosxe : mpls label protocol ldp
                configurations.append_line('mpls label protocol ldp', \
                                            unconfig_cmd = 'default mpls label protocol')

                # iosxe : mpls ip
                configurations.append_line('mpls ip', \
                                            unconfig_cmd = 'default mpls ip')


            # iosxe : no mpls ip
            if attributes.value('shutdown'):
                configurations.append_line('no mpls ip', \
                                            unconfig_cmd = 'mpls ip')

            # iosxe : mpls ip default-route
            if attributes.value('default_route'):
                configurations.append_line('mpls ip default-route')

            # iosxe : mpls ldp nsr
            if attributes.value('nsr'):
                configurations.append_line('mpls ldp nsr')

            # iosxe : mpls ldp graceful-restart
            if attributes.value('gr'):
                configurations.append_line('mpls ldp graceful-restart')

            # iosxe : mpls ldp graceful-restart timers forwarding-holding <30-600>
            configurations.append_line(attributes.format(\
                'mpls ldp graceful-restart timers forwarding-holding {gr_fwdstate_holdtime}'))

            # iosxe : mpls ldp graceful-restart timers max-recovery <15-600>
            configurations.append_line(attributes.format(\
                'mpls ldp graceful-restart timers max-recovery {gr_max_recovery}'))

            # iosxe : mpls ldp graceful-restart timers neighbor-liveness <5-300>
            configurations.append_line(attributes.format(\
                'mpls ldp graceful-restart timers neighbor-liveness {gr_neighbor_liveness}'))

            # iosxe : mpls ldp discovery hello interval <1-65535>
            configurations.append_line(attributes.format(\
                'mpls ldp discovery hello interval {hello_interval}'))

            # iosxe : mpls ldp discovery hello holdtime <1-65535>
            configurations.append_line(attributes.format(\
                'mpls ldp discovery hello holdtime {hello_holdtime}'))


            # iosxe : mpls ldp discovery targeted-hello interval ...
            configurations.append_line(attributes.format(\
                'mpls ldp discovery targeted-hello interval {targetted_hello_interval}'))

            # iosxe : mpls ldp discovery targeted-hello holdtime ...
            configurations.append_line(attributes.format(\
                'mpls ldp discovery targeted-hello holdtime {targetted_hello_holdtime}'))

            # iosxe : mpls ldp discovery targeted-hello accept
            # iosxe : mpls ldp discovery targeted-hello accept from ACL_NAME
            if attributes.value('targeted_hello_accept'):
                if attributes.value('targeted_hello_accept_from_acl') is not None:
                    configurations.append_line(attributes.format(\
                        'mpls ldp discovery targeted-hello accept from {targeted_hello_accept_from_acl.name}'))
                else:
                    configurations.append_line(attributes.format(\
                        'mpls ldp discovery targeted-hello accept'))


            if attributes.value('advertise_expnull'):
                if attributes.value('advertise_expnull_for_acl') and \
                   attributes.value('advertise_expnull_to_acl'):
                   configurations.append_line(attributes.format('mpls ldp explicit-null for {advertise_expnull_for_acl.name}'\
                                              ' to {advertise_expnull_to_acl.name}'))

                elif attributes.value('advertise_expnull_for_acl'):
                    configurations.append_line(attributes.format('mpls ldp explicit-null for {advertise_expnull_for_acl.name}'))

                else:
                    configurations.append_line('mpls ldp explicit-null')

            for sub, attributes2 in attributes.mapping_values('vrf_attr', keys=self.vrfs, sort=True):
                configurations.append_block(sub.build_config(apply=False, attributes=attributes2, unconfig=unconfig))

            for sub, attributes2 in attributes.mapping_values('interface_attr', keys=self.interfaces, sort=True):
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

                # iosxe: mpls ldp router-id {interface.name}
                # iosxe: mpls ldp router-id vrf xxx {interface.name}
                if self.vrf_name == 'default':
                    configurations.append_line(attributes.format('mpls ldp router-id {router_id.name}'))
                else:
                    configurations.append_line(attributes.format('mpls ldp router-id vrf {vrf_name} {router_id.name}',force=True))

                # iosxe : mpls ldp session protection ...
                if self.vrf_name == 'default':
                    if attributes.value('session_protection'):
                        if attributes.value('session_protection_for_acl') and attributes.value('session_protection_dur'):
                            configurations.append_line(attributes.format('mpls ldp session protection for '\
                                                '{session_protection_for_acl.name} {session_protection_dur}'))

                        elif attributes.value('session_protection_for_acl'):
                            configurations.append_line(attributes.format('mpls ldp session protection for '\
                                                '{session_protection_for_acl.name}'))

                        elif attributes.value('session_protection_dur'):
                            configurations.append_line(attributes.format('mpls ldp session protection for {session_protection_dur}'))

                        else:
                            configurations.append_line('mpls ldp session protection')

                else:
                    if attributes.value('session_protection'):
                        if attributes.value('session_protection_for_acl') and attributes.value('session_protection_dur'):
                            configurations.append_line(attributes.format('mpls ldp session protection vrf {vrf_name} for '\
                                                '{session_protection_for_acl.name} {session_protection_dur}',force=True))

                        elif attributes.value('session_protection_for_acl'):
                            configurations.append_line(attributes.format('mpls ldp session protection vrf {vrf_name} for '\
                                                '{session_protection_for_acl.name}',force=True))

                        elif attributes.value('session_protection_dur'):
                            configurations.append_line(attributes.format('mpls ldp session protection vrf {vrf_name} for '\
                                                '{session_protection_dur}',force=True))

                        else:
                            configurations.append_line(attributes.format('mpls ldp session protection vrf {vrf_name}',force=True))

                # TODO : support more password options, currently only supporting 1
                # TODO : supporting encrypted password
                # iosxe : mpls ldp password option 1 for xx yy ...
                if self.vrf_name == 'default':
                    if attributes.value('password_for_acl'):
                        configurations.append_line(attributes.format('mpls ldp password option 1 for {password_for_acl} '\
                                                                'password {password}'))
                else:
                    if attributes.value('password_for_acl'):
                        configurations.append_line(attributes.format('mpls ldp vrf {vrf_name} password option 1 for {password_for_acl} '\
                                                                'password {password}',force=True))

                # TODO : supporting encrypted password
                for neighbor, neighbor_attributes in attributes.mapping_values('neighbor_attr', keys=self.neighbors, sort=True):
                    # iosxe: mpls ldp neighbor a.b.c.d password xxx
                    # iosxe: mpls ldp neighbor vrf xxx a.b.c.d password xxx
                    def _transform(neighbor):
                        return str(neighbor).split(':')[0]
                    if neighbor_attributes.value('password'):
                        if self.vrf_name == 'default':
                            configurations.append_line(neighbor_attributes.format('mpls ldp neighbor {neighbor} password {password}', \
                                transform_neighbor=_transform,force=True))
                        else:
                            configurations.append_line(neighbor_attributes.format('mpls ldp neighbor vrf {vrf_name} '\
                                '{neighbor} password {password}', transform_neighbor=_transform, force=True))

                return str(configurations)

            def build_unconfig(self, apply=True, attributes=None, **kwargs):
                return self.build_config(apply=apply, attributes=attributes, unconfig=True, **kwargs)

        class InterfaceAttributes(ABC):

            def build_config(self, apply=True, attributes=None, unconfig=False, **kwargs):
                assert not apply
                attributes = AttributesHelper(self, attributes)
                configurations = CliConfigBuilder(unconfig=unconfig)

                with configurations.submode_context(attributes.format('interface {interface_name}', force=True, cancel_empty=True)):

                    # iosxe: interface GigabitEthernet0/0/0 / mpls ip
                    if attributes.iswildcard:
                        configurations.append_line('mpls ip')
                    
                    # iosxe: interface GigabitEthernet0/0/0 / mpls ldp igp autoconfig
                    if attributes.value('igp_autoconfig'):
                        configurations.append_line('mpls ldp igp autoconfig')

                    # iosxe: interface GigabitEthernet0/0/0 / mpls ldp igp sync
                    if attributes.value('igp_sync'):
                        configurations.append_line('mpls ldp igp sync')

                    # iosxe: interface GigabitEthernet0/0/0 / mpls ldp igp sync time 5
                    configurations.append_line(attributes.format('mpls ldp igp sync delay {igp_sync_delay_time}'))

                    # iosxe: interface GigabitEthernet0/0/0 / mpls ldp discovery transport-address 10.12.1.1
                    configurations.append_line(attributes.format('mpls ldp discovery transport-address {transport_address}'))

                return str(configurations)

            def build_unconfig(self, apply=True, attributes=None, **kwargs):
                return self.build_config(apply=apply, attributes=attributes, unconfig=True, **kwargs)


