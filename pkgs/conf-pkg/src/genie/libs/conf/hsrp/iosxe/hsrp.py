'''
IOSXE Genie Conf using CLI for feature Standby.
'''

# Python
from abc import ABC
import warnings

# Genie
from genie.decorator import managedattribute
from genie.conf.base.config import CliConfig
from genie.conf.base.cli import CliConfigBuilder
from genie.conf.base.attributes import UnsupportedAttributeWarning,\
                                       AttributesHelper


class Hsrp(ABC):

    class DeviceAttributes(ABC):

        def build_config(self, devices=None, apply=True, attributes=None,
                         unconfig=False, **kwargs):
            assert not apply
            attributes = AttributesHelper(self, attributes)
            configurations = CliConfigBuilder(unconfig=unconfig)

            # loop over all interfaces
            for sub, attributes2 in attributes.mapping_values(
                    'interface_attr', keys=self.interface_attr.keys()):
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

                # enabled N/A
                # state_change_disable N/A

                # interface <interface_name>
                with configurations.submode_context(attributes.format(
                        'interface {interface_name}', force=True)):

                    # interface <interface_name>
                    #   standby version <version>
                    configurations.append_line(attributes.format(
                        'standby version {version}'))

                    # interface <interface_name>
                    #   standby <bfd> (old)
                    if attributes.value('bfd'):
                        configurations.append_line('standby bfd')

                    # interface <interface_name>
                    #   standby bfd
                    if attributes.value('bfd_enabled'):
                        configurations.append_line('standby bfd')

                    # bfd_interval N/A
                    # bfd_detection_multiplier N/A
                    # bfd_address N/A
                    # bfd_interface_name

                    # interface <interface_name>
                    #   standby delay minimum <minimum_delay> \
                    #   reload <reload_delay>
                    if attributes.value('minimum_delay') and \
                       attributes.value('reload_delay'):
                        configurations.append_line(attributes.format(
                            'standby delay minimum {minimum_delay} '
                            'reload {reload_delay}'))
                    elif attributes.value('minimum_delay'):
                        configurations.append_line(attributes.format(
                            'standby delay minimum {minimum_delay}'))

                    # interface <interface_name>
                    #   standby mac-refresh <mac_refresh>
                    if attributes.value('mac_refresh'):
                        configurations.append_line(attributes.format(
                            'standby mac-refresh {mac_refresh}'))

                    # interface <interface_name>
                    #   standby use-bia scope interface
                    if attributes.value('use_bia'):
                        configurations.append_line(attributes.format(
                            'standby use-bia'))

                    # interface <interface_name>
                    #   standby redirect (old)
                    if attributes.value('redirect'):
                        configurations.append_line(
                            'standby redirect')

                    # interface <interface_name>
                    #   standby redirect
                    if attributes.value('redirects_disable') == False:
                        configurations.append_line(
                            'standby redirect')

                    if attributes.value('authentication_word'):
                        # interface <interface_name>
                        #   standby <group_number> authentication \
                        #   <authentication_word> (old)
                        configurations.append_line(attributes.format(
                            'standby {group_number} '
                            'authentication {authentication_word}'))
                    elif attributes.value('authentication_text'):
                        # interface <interface_name>
                        #   standby <group_number> authentication text \
                        #   <authentication_text> (old)
                        configurations.append_line(attributes.format(
                            'standby {group_number} '
                            'authentication text {authentication_text}'))
                    elif attributes.value('authentication_md5_keychain'):
                        # interface <interface_name>
                        #   standby <group_number> authentication \
                        #   md5 key-chain <authentication_md5_keychain> (old)
                        configurations.append_line(attributes.format(
                            'standby {group_number} authentication '
                            'md5 key-chain {authentication_md5_keychain}'))
                    elif attributes.value('authentication_md5_keystring'):
                        # interface <interface_name>
                        #   standby <group_number> authentication \
                        #   md5 key-string <authentication_md5_keystring> (old)
                        configurations.append_line(attributes.format(
                            'standby {group_number} authentication '
                            'md5 key-string {authentication_md5_keystring}'))

                    # interface <interface_name>
                    #   standby <group_number> authentication \
                    #   <authentication>
                    configurations.append_line(attributes.format(
                        'standby {group_number} '
                        'authentication {authentication}'))

                    # interface <interface_name>
                    #   standby <group_number> follow <follow>
                    configurations.append_line(attributes.format(
                        'standby {group_number} follow {follow}'))

                    # interface <interface_name>
                    #   standby <group_number> ip <ip_address> (old)
                    if attributes.value('address_family').name == 'ipv4':
                        configurations.append_line(attributes.format(
                            'standby {group_number} ip {ip_address}'))

                    # interface <interface_name>
                    #   standby <group_number> ip <primary_ipv4_address>
                    #   standby <group_number> ip <secondary_ipv4_address> secondary
                    if attributes.value('address_family').name == 'ipv4':
                        configurations.append_line(attributes.format(
                            'standby {group_number} ip {primary_ipv4_address}'))
                        configurations.append_line(attributes.format(
                            'standby {group_number} ip {secondary_ipv4_address}'
                            ' secondary'))
                        if attributes.value('virtual_ip_learn'):
                            configurations.append_line(attributes.format(
                                'standby {group_number} ip'))

                    # interface <interface_name>
                    #   standby <group_number> ipv6 <global_ipv6_address>
                    #   standby <group_number> ipv6 <link_local_ipv6_address>
                    if attributes.value('address_family').name == 'ipv6':
                        configurations.append_line(attributes.format(
                            'standby {group_number} ipv6 '
                            '{global_ipv6_address}'))
                        configurations.append_line(attributes.format(
                            'standby {group_number} ipv6 '
                            '{link_local_ipv6_address}'))
                        if attributes.value('hsrp_linklocal'):
                            if attributes.value('hsrp_linklocal').name \
                                == 'auto':
                                configurations.append_line(attributes.format(
                                    'standby {group_number} ipv6 autoconfig'))

                    # interface <interface_name>
                    #   standby <group_number> mac-address <mac_address> (old)
                    configurations.append_line(attributes.format(
                        'standby {group_number} mac-address {mac_address}'))

                    # interface <interface_name>
                    #   standby <group_number> mac-address <virtual_mac_address>
                    configurations.append_line(attributes.format(
                        'standby {group_number} mac-address '
                        '{virtual_mac_address}'))

                    # interface <interface_name>
                    #   standby <group_number> name <group_name> (old)
                    configurations.append_line(attributes.format(
                        'standby {group_number} name {group_name}'))

                    # interface <interface_name>
                    #   standby <group_number> name <session_name>
                    configurations.append_line(attributes.format(
                        'standby {group_number} name {session_name}'))

                    if attributes.value('preempt') and \
                       attributes.value('preempt_minimum_delay') and \
                       attributes.value('preempt_reload_delay') and \
                       attributes.value('preempt_sync_delay'):
                        # interface <interface_name>
                        #   standby <group_number> preempt delay \
                        #   minimum <preempt_minimum_delay> reload \
                        #   <preempt_reload_delay> sync <preempt_sync_delay>
                        configurations.append_line(attributes.format(
                            'standby {group_number} '
                            'preempt delay minimum {preempt_minimum_delay} '
                            'reload {preempt_reload_delay} '
                            'sync {preempt_sync_delay}'))
                    elif attributes.value('preempt') and \
                         attributes.value('preempt_minimum_delay') and \
                         attributes.value('preempt_reload_delay'):
                        # interface <interface_name>
                        #   standby <group_number> preempt delay \
                        #   minimum <preempt_minimum_delay> reload \
                        #   <preempt_reload_delay>
                        configurations.append_line(attributes.format(
                            'standby {group_number} '
                            'preempt delay minimum {preempt_minimum_delay} '
                            'reload {preempt_reload_delay}'))
                    elif attributes.value('preempt') and \
                         attributes.value('preempt_minimum_delay'):
                        # interface <interface_name>
                        #   standby <group_number> preempt delay \
                        #   minimum <preempt_minimum_delay>
                        configurations.append_line(attributes.format(
                            'standby {group_number} '
                            'preempt delay minimum {preempt_minimum_delay}'))
                    elif attributes.value('preempt') and \
                         attributes.value('preempt_reload_delay'):
                        # interface <interface_name>
                        #   standby <group_number> preempt delay \
                        #   reload <preempt_reload_delay>
                        configurations.append_line(attributes.format(
                            'standby {group_number} '
                            'preempt delay reload {preempt_reload_delay}'))
                    elif attributes.value('preempt') and \
                         attributes.value('preempt_sync_delay'):
                        # interface <interface_name>
                        #   standby <group_number> preempt delay \
                        #   sync <preempt_sync_delay>
                        configurations.append_line(attributes.format(
                            'standby {group_number} '
                            'preempt delay sync {preempt_sync_delay}'))
                    elif attributes.value('preempt'):
                        # interface <interface_name>
                        #   standby <group_number> preempt
                        configurations.append_line(attributes.format(
                            'standby {group_number} preempt'))

                    # interface <interface_name>
                    #   standby <group_number> priority <priority>
                    configurations.append_line(attributes.format(
                        'standby {group_number} priority {priority}'))

                    # interface <interface_name>
                    #   standby <group_number> timers \
                    #   <hello_interval_seconds> <holdtime_seconds> (old)
                    configurations.append_line(attributes.format(
                        'standby {group_number} timers '
                        '{hello_interval_seconds} {holdtime_seconds}'))

                    # interface <interface_name>
                    #   standby <group_number> timers msec \
                    #   <hello_interval_msec> msec <holdtime_msec> (old)
                    configurations.append_line(attributes.format(
                        'standby {group_number} timers msec '
                        '{hello_interval_msec} msec {holdtime_msec}'))

                    timers_config =\
                     [attributes.format('standby {group_number} timers ')]
                    if attributes.value('hello_msec_flag') is False and\
                         attributes.value('hold_msec_flag') is False:
                        timers_config.append(\
                         attributes.format('{hello_sec} {hold_sec}'))
                    elif attributes.value('hello_msec_flag') is True and\
                         attributes.value('hold_msec_flag') is False:
                        timers_config.append(\
                         attributes.format('msec {hello_msec} {hold_sec}'))
                    elif attributes.value('hello_msec_flag') is False and\
                         attributes.value('hold_msec_flag') is True:
                        timers_config.append(\
                         attributes.format('{hello_sec} msec {hold_msec}'))
                    elif attributes.value('hello_msec_flag') is True and\
                         attributes.value('hold_msec_flag') is True:
                        timers_config.append(\
                         attributes.format('msec {hello_msec} msec '
                            '{hold_msec}'))
                    if timers_config[1] != '' and None not in timers_config:
                        configurations.append_line(''.join(timers_config))

                    # interface <interface_name>
                    #   standby <group_number> track object <track_object> \
                    #   decrement <priority_decrement>
                    configurations.append_line(attributes.format(
                        'standby {group_number} track {track_object} '
                        'decrement {priority_decrement}'))

                    # interface <interface_name>
                    #   standby <group_number> track object <tracked_object> \
                    #   [decrement <tracked_object_priority_decrement>]
                    if attributes.value('tracked_object') and \
                     attributes.value('tracked_object_priority_decrement'):
                        configurations.append_line(attributes.format(
                            'standby {group_number} track {tracked_object} '
                            'decrement {tracked_object_priority_decrement}'))
                    elif attributes.value('tracked_object'):
                        configurations.append_line(attributes.format(
                            'standby {group_number} track {tracked_object}'))                      

                    # interface <interface_name>
                    #   standby <group_number> track object <track_object> \
                    #   shutdown
                    if attributes.value('track_shutdown'):
                        configurations.append_line(attributes.format(
                            'standby {group_number} track {track_object} '
                            'shutdown'))

                    # tracked_interface N/A
                    # tracked_intf_priority_decrement N/A

                return str(configurations)

            def build_unconfig(self, apply=True, attributes=None, **kwargs):
                return self.build_config(apply=apply, attributes=attributes,
                                         unconfig=True, **kwargs)

