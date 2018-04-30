'''
NXOS Specific Configurations for Hsrp Feature objects.
'''

# Python
from abc import ABC
import warnings

# Genie
from genie.decorator import managedattribute
from genie.conf.base.config import CliConfig
from genie.conf.base.cli import CliConfigBuilder
from genie.conf.base.attributes import UnsupportedAttributeWarning, \
                                       AttributesHelper


class Hsrp(ABC):

    class DeviceAttributes(ABC):

        def build_config(self, devices=None, apply=True, attributes=None,
                         unconfig=False, **kwargs):
            assert not apply
            attributes = AttributesHelper(self, attributes)
            configurations = CliConfigBuilder(unconfig=unconfig)

            # feature hsrp
            if attributes.value('enabled'):
                configurations.append_line(attributes.format('feature hsrp',
                                           force=True))

            # loop over all interfaces
            for sub, attributes2 in attributes.mapping_values('interface_attr',
                    keys=self.interface_attr.keys()):
                configurations.append_block(sub.build_config(apply=False,
                    attributes=attributes2, unconfig=unconfig, **kwargs))

            return CliConfig(device=self.device, unconfig=unconfig,
                             cli_config=configurations)

        def build_unconfig(self, apply=True, attributes=None, **kwargs):
            return self.build_config(apply=apply, attributes=attributes,
                                     unconfig=True, **kwargs)

        class InterfaceAttributes(ABC):

            def build_config(self, apply=True, attributes=None,
                             unconfig=False, **kwargs):
                assert not apply
                attributes = AttributesHelper(self, attributes)
                configurations = CliConfigBuilder(unconfig=unconfig)

                # state_change_disable N/A

                # interface <interface_name>
                with configurations.submode_context(attributes.format(
                        'interface {interface_name}', force=True)):

                    # interface <interface_name>
                    #   hsrp bfd
                    if attributes.value('bfd'):
                        configurations.append_line(
                            attributes.format('hsrp bfd'))

                    # interface <interface_name>
                    #   hsrp bfd
                    if attributes.value('bfd_enabled'):
                        configurations.append_line(
                            attributes.format('hsrp bfd'))

                    # bfd_interval N/A
                    # bfd_detection_multiplier N/A
                    # bfd_address N/A
                    # bfd_interface_name N/A

                    # interface <interface_name>
                    #   hsrp version <version>
                    if attributes.value('version') == 2:
                        configurations.append_line(
                            attributes.format('hsrp version {version}'))

                    if attributes.value('minimum_delay') and \
                       attributes.value('reload_delay'):
                        # interface <interface_name>
                        #   hsrp delay minimum <minimum_delay> \
                        #   reload <reload_delay>
                        configurations.append_line(attributes.format(
                            'hsrp delay minimum {minimum_delay} '
                            'reload {reload_delay}'))
                    elif attributes.value('minimum_delay'):
                        # interface <interface_name>
                        #   hsrp delay minimum <delay>
                        configurations.append_line(attributes.format(
                            'hsrp delay minimum {minimum_delay}'))

                    # interface <interface_name>
                    #   hsrp mac-refresh <mac_refresh>
                    configurations.append_line(
                        attributes.format('hsrp mac-refresh {mac_refresh}'))

                    # interface <interface_name>
                    #   hsrp use-bia scope interface
                    if attributes.value('use_bia'):
                        configurations.append_line('hsrp use-bia')

                    # redirects_disable N/A

                    # interface <interface_name>
                    #   hsrp <group_number>
                    line = 'hsrp {group_number}'
                    if self.address_family.name == 'ipv6':
                        line += ' ipv6'
                    with configurations.submode_context(attributes.format(
                            line, force=True)):

                        if unconfig and attributes.iswildcard:
                            configurations.submode_unconfig()

                        if attributes.value('authentication_word'):
                            # interface <interface_name>
                            #   hsrp <group_number>
                            #     authentication <authentication_word>
                            configurations.append_line(attributes.format(
                                'authentication {authentication_word}'))
                        elif attributes.value('authentication_text'):
                            # interface <interface_name>
                            #   hsrp <group_number>
                            #     authentication text <authentication_text>
                            configurations.append_line(attributes.format(
                                'authentication text {authentication_text}'))
                        elif attributes.value('authentication_md5_keychain'):
                            # interface <interface_name>
                            #   hsrp <group_number>
                            #     authentication md5 key-chain \
                            #     <authentication_md5_keychain>
                            configurations.append_line(attributes.format(
                                'authentication md5 key-chain '
                                '{authentication_md5_keychain}'))
                        elif attributes.value('authentication_md5_keystring'):
                            # interface <interface_name>
                            #   hsrp <group_number>
                            #     authentication md5 key-string \
                            #     <authentication_md5_keystring>
                            configurations.append_line(attributes.format(
                                'authentication md5 key-string '
                                '{authentication_md5_keystring}'))

                        if attributes.value('authentication'):
                            # interface <interface_name>
                            #   hsrp <group_number>
                            #     authentication <authentication>
                            configurations.append_line(attributes.format(
                                'authentication {authentication}'))
                        
                        # interface <interface_name>
                        #   hsrp <group_number>
                        #     ip <ip_address>
                        if self.address_family.name == 'ipv4':
                            configurations.append_line(
                                attributes.format('ip {ip_address}'))
                        elif self.address_family.name == 'ipv6':
                            configurations.append_line(
                                attributes.format('ipv6 {ip_address}'))

                        # interface <interface_name>
                        #   hsrp <group_number>
                        #     ip <primary_ipv4_address>|<secondary_ipv4_address> [secondary]
                        #     ip <global_ipv6_address>|<link_local_ipv6_address>
                        #     ip autoconfig
                        if self.address_family.name == 'ipv4':
                            if attributes.value('primary_ipv4_address'):
                                configurations.append_line(
                                    attributes.format('ip '
                                        '{primary_ipv4_address}'))
                            if attributes.value('secondary_ipv4_address'):
                                configurations.append_line(
                                    attributes.format('ip '
                                        '{secondary_ipv4_address} secondary'))
                        elif self.address_family.name == 'ipv6':
                            if attributes.value('global_ipv6_address'):
                                configurations.append_line(
                                    attributes.format('ip '
                                        '{global_ipv6_address}'))
                            if attributes.value('link_local_ipv6_address'):
                                configurations.append_line(
                                    attributes.format('ip '
                                        '{link_local_ipv6_address}'))
                            if attributes.value('hsrp_linklocal'):
                                if attributes.value('hsrp_linklocal').name ==\
                                 'auto':
                                    configurations.append_line('ip autoconfig')

                        # interface <interface_name>
                        #   hsrp <group_number>
                        if attributes.value('virtual_ip_learn'):
                            configurations.append_line('ip')

                        # interface <interface_name>
                        #   hsrp <group_number>
                        #     mac-address <mac_address>
                        configurations.append_line(
                            attributes.format('mac-address {mac_address}'))

                        # interface <interface_name>
                        #   hsrp <group_number>
                        #     mac-address <virtual_mac_address>
                        configurations.append_line(
                            attributes.format('mac-address '
                                '{virtual_mac_address}'))

                        # interface <interface_name>
                        #   hsrp <group_number>
                        #     name <group_name>
                        configurations.append_line(
                            attributes.format('name {group_name}'))

                        # interface <interface_name>
                        #   hsrp <group_number>
                        #     name <session_name>
                        configurations.append_line(
                            attributes.format('name {session_name}'))

                        # interface <interface_name>
                        #   hsrp <group_number>
                        #     follow <follow>
                        configurations.append_line(
                            attributes.format('follow {follow}'))
                        
                        if attributes.value('preempt') and \
                           attributes.value('preempt_minimum_delay') and \
                           attributes.value('preempt_reload_delay') and \
                           attributes.value('preempt_sync_delay'):
                            # interface <interface_name>
                            #   hsrp <group_number>
                            #     preempt delay \
                            #     minimum <preempt_minimum_delay> \
                            #     reload <preempt_reload_delay> \
                            #     sync <preempt_sync_delay>
                            configurations.append_line(attributes.format(
                                'preempt delay minimum {preempt_minimum_delay} '
                                'reload {preempt_reload_delay} '
                                'sync {preempt_sync_delay}'))
                        elif attributes.value('preempt') and \
                             attributes.value('preempt_minimum_delay') and \
                             attributes.value('preempt_reload_delay'):
                            # interface <interface_name>
                            #   hsrp <group_number>
                            #     preempt delay minimum <preempt_minimum_delay>\
                            #     reload <preempt_reload_delay>
                            configurations.append_line(attributes.format(
                                'preempt delay minimum {preempt_minimum_delay} '
                                'reload {preempt_reload_delay}'))
                        elif attributes.value('preempt') and \
                             attributes.value('preempt_minimum_delay'):
                            # interface <interface_name>
                            #   hsrp <group_number>
                            #     preempt delay minimum <preempt_minimum_delay>
                            configurations.append_line(attributes.format(
                                'preempt delay minimum '
                                '{preempt_minimum_delay}'))
                        elif attributes.value('preempt') and \
                             attributes.value('preempt_reload_delay'):
                            # interface <interface_name>
                            #   hsrp <group_number>
                            #     preempt delay reload <preempt_reload_delay>
                            configurations.append_line(attributes.format(
                                'preempt delay reload '
                                '{preempt_reload_delay}'))
                        elif attributes.value('preempt') and \
                             attributes.value('preempt_sync_delay'):
                            # interface <interface_name>
                            #   hsrp <group_number>
                            #     preempt delay sync <preempt_sync_delay>
                            configurations.append_line(attributes.format(
                                'preempt delay sync '
                                '{preempt_sync_delay}'))
                        elif attributes.value('preempt'):
                            # interface <interface_name>
                            #   hsrp <group_number>
                            #     preempt
                            configurations.append_line('preempt')

                        # interface <interface_name>
                        #   hsrp <group_number>
                        #     priority <priority>
                        configurations.append_line(
                            attributes.format('priority {priority}'))

                        # interface <interface_name>
                        #   hsrp <group_number>
                        #     timers <hello_interval_seconds> <holdtime_seconds>
                        configurations.append_line(attributes.format(
                            'timers {hello_interval_seconds} '
                            '{holdtime_seconds}'))

                        # interface <interface_name>
                        #   hsrp <group_number>
                        #     timers msec <hello_interval_msec> \
                        #     msec <holdtime_msec>
                        configurations.append_line(attributes.format(
                            'timers msec {hello_interval_msec} '
                            'msec {holdtime_msec}'))

                        # interface <interface_name>
                        #   hsrp <group_number>
                        #     timers <hello_sec> <hold_sec>
                        #     timers msec <hello_msec> <hold_sec>
                        #     timers <hello_sec> msec <hold_msec>
                        #     timers msec <hello_msec> msec <hold_msec>
                        timers_config = ['timers ']
                        if (attributes.value('hello_msec_flag') is False) and\
                         (attributes.value('hold_msec_flag') is False):
                            timers_config.append(\
                             attributes.format('{hello_sec} {hold_sec}'))
                        elif (attributes.value('hello_msec_flag') is True) and\
                         (attributes.value('hold_msec_flag') is False):
                            timers_config.append(\
                             attributes.format('msec {hello_msec} {hold_sec}'))
                        elif (attributes.value('hello_msec_flag') is False) and\
                         (attributes.value('hold_msec_flag') is True):
                            timers_config.append(\
                             attributes.format('{hello_sec} msec {hold_msec}'))
                        elif (attributes.value('hello_msec_flag') is True) and\
                         (attributes.value('hold_msec_flag') is True):
                            timers_config.append(\
                             attributes.format('msec {hello_msec} '
                                'msec {hold_msec}'))
                        if timers_config[1] != '':
                            configurations.append_line(''.join(timers_config)) 

                        # interface <interface_name>
                        #   hsrp <group_number>
                        #     track <track> decrement <priority_decrement>
                        if attributes.value('track_object') and\
                           attributes.value('priority_decrement'):
                            configurations.append_line(attributes.format(
                                'track {track_object} '
                                'decrement {priority_decrement}'))
                        elif attributes.value('track_object'):
                            configurations.append_line(attributes.format(
                                'track {track_object}'))

                        # interface <interface_name>
                        #   hsrp <group_number>
                        #     track <tracked_object> decrement <priority_decrement>
                        if attributes.value('tracked_object') and\
                           attributes.value(\
                            'tracked_object_priority_decrement'):
                            configurations.append_line(attributes.format(
                                'track {tracked_object} '
                                'decrement '
                                '{tracked_object_priority_decrement}'))
                        elif attributes.value('tracked_object'):
                            configurations.append_line(attributes.format(
                                'track {tracked_object}'))

                        # tracked_interface N/A
                        # tracked_intf_priority_decrement N/A

                return str(configurations)

            def build_unconfig(self, apply=True, attributes=None, **kwargs):
                return self.build_config(apply=apply, attributes=attributes,
                                         unconfig=True, **kwargs)

