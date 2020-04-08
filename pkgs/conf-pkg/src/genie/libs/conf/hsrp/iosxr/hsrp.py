'''
IOSXR Specific Configurations for Hsrp Feature objects.
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

            # iosxr: router hsrp
            configurations.append_line(attributes.format('router hsrp',
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

                # router hsrp
                #   message state disable
                if attributes.value('state_change_disable'):
                    configurations.append_line(
                        'message state disable')

                # interface <interface_name>
                with configurations.submode_context(attributes.format(
                        'interface {interface_name}', force=True)):

                    # interface <interface_name>
                    #   hsrp bfd minimim delay <bfd_min_interval>\
                    configurations.append_line(attributes.format(
                        'hsrp bfd minimum-interval {bfd_min_interval}'))

                    # interface <interface_name>
                    #   hsrp bfd minimim delay <bfd_interval>\
                    configurations.append_line(attributes.format(
                        'hsrp bfd minimum-interval {bfd_interval}'))

                    # interface <interface_name>
                    #   hsrp bfd multiplier <bfd_multiplier>\
                    configurations.append_line(attributes.format(
                        'hsrp bfd multiplier {bfd_multiplier}'))

                    # interface <interface_name>
                    #   hsrp bfd multiplier <bfd_detection_multiplier>\
                    configurations.append_line(attributes.format(
                        'hsrp bfd multiplier {bfd_detection_multiplier}'))

                    # interface <interface_name>
                    #   hsrp delay minimum <minimum_delay> \
                    #   reload <reload_delay>
                    configurations.append_line(attributes.format(
                        'hsrp delay minimum {minimum_delay} '
                        'reload {reload_delay}'))

                    # interface <interface_name>
                    #   hsrp use-bia
                    if attributes.value('use_bia'):
                        configurations.append_line(attributes.format(
                            'hsrp use-bia'))

                    # interface <interface_name>
                    #   hsrp redirect disable
                    if attributes.value('redirect'):
                        configurations.append_line(attributes.format(
                            'hsrp redirect disable'))

                    # interface <interface_name>
                    #   hsrp redirect disable
                    if attributes.value('redirects_disable'):
                        configurations.append_line(attributes.format(
                            'hsrp redirect disable'))

                    # interface <interface_name>
                    #   hsrp mac-refresh <mac_refresh>
                    configurations.append_line(attributes.format(
                        'hsrp mac-refresh {mac_refresh}'))

                    # interface <interface_name>
                    #   address-family <address_family>
                    with configurations.submode_context(attributes.format(
                        'address-family {address_family.name}', force=True)):

                        if unconfig and attributes.iswildcard:
                            configurations.submode_unconfig()

                        # interface <interface_name>
                        #   address-family <address_family>
                        #       hsrp version <version>
                        if attributes.value('version'):
                            configurations.append_line(attributes.format(
                                'hsrp version {version}'))

                        # interface <interface_name>
                        #   address-family <address_family>
                        #       hsrp <bfd_address> [<bfd_interface_name>]
                        if attributes.value('bfd_address') and \
                         attributes.value('bfd_interface_name'):
                            configurations.append_line(attributes.format(
                                'hsrp bfd fast-detect peer {bfd_address} '
                                '{bfd_interface_name}'))
                        elif attributes.value('bfd_address'):
                            configurations.append_line(attributes.format(
                                'hsrp bfd fast-detect peer {bfd_address}'))

                        # interface <interface_name>
                        #   address-family <address_family>
                        #       hsrp <group_number>
                        with configurations.submode_context(attributes.format(
                                'hsrp {group_number}', force=True)):

                            if unconfig and attributes.iswildcard:
                                configurations.submode_unconfig()

                            # interface <interface_name>
                            #   address-family <address_family>
                            #       hsrp <group_number>
                            #           address <ip_address>
                            configurations.append_line(attributes.format(
                                'address {ip_address}'))

                            # interface <interface_name>
                            #   address-family <address_family>
                            #       hsrp <group_number>
                            #           address learn
                            if attributes.value('virtual_ip_learn'):
                                configurations.append_line('address learn')                            

                            if attributes.value('address_family').name \
                             == 'ipv4':
                                # interface <interface_name>
                                #   address-family <address_family>
                                #       hsrp <group_number>
                                #           address <primary_ipv4_address>
                                configurations.append_line(attributes.format(
                                    'address {primary_ipv4_address}'))
    
                                # interface <interface_name>
                                #   address-family <address_family>
                                #     hsrp <group_number>
                                #       address <secondary_ipv4_address> secondary
                                configurations.append_line(attributes.format(
                                    'address {secondary_ipv4_address} '
                                    'secondary'))

                            if attributes.value('address_family').name \
                             == 'ipv6':
                                # interface <interface_name>
                                #   address-family <address_family>
                                #       hsrp <group_number>
                                #           address global <global_ipv6_address>
                                configurations.append_line(attributes.format(
                                    'address global {global_ipv6_address}'))
    
                                # interface <interface_name>
                                #   address-family <address_family>
                                #     hsrp <group_number>
                                #       address linklocal <link_local_ipv6_address>
                                configurations.append_line(attributes.format(
                                    'address linklocal '
                                    '{link_local_ipv6_address}'))

                                # interface <interface_name>
                                #   address-family <address_family>
                                #     hsrp <group_number>
                                #       address linklocal autoconfig
                                if attributes.value('hsrp_linklocal'):
                                    if attributes.value('hsrp_linklocal').name\
                                     == 'auto':
                                        configurations.append_line(\
                                            'address linklocal autoconfig')
    
                            # interface <interface_name>
                            #   address-family <address_family>
                            #       hsrp <group_number>
                            #           authentication <authentication_word>
                            configurations.append_line(attributes.format(
                                'authentication {authentication_word}'))

                            # interface <interface_name>
                            #   address-family <address_family>
                            #       hsrp <group_number>
                            #           authentication <authentication>
                            configurations.append_line(attributes.format(
                                'authentication {authentication}'))

                            # interface <interface_name>
                            #   address-family <address_family>
                            #       hsrp <group_number>
                            #           bfd fast-detect
                            if attributes.value('bfd_fast_detect'):
                                configurations.append_line('bfd fast-detect')

                            # interface <interface_name>
                            #   address-family <address_family>
                            #       hsrp <group_number>
                            #           bfd fast-detect
                            if attributes.value('bfd_enabled'):
                                configurations.append_line('bfd fast-detect')

                            # interface <interface_name>
                            #   address-family <address_family>
                            #       hsrp <group_number>
                            #           mac-address <mac_address>
                            configurations.append_line(attributes.format(
                                'mac-address {mac_address}'))

                            # interface <interface_name>
                            #   address-family <address_family>
                            #       hsrp <group_number>
                            #           mac-address <virtual_mac_address>
                            configurations.append_line(attributes.format(
                                'mac-address {virtual_mac_address}'))

                            # interface <interface_name>
                            #   address-family <address_family>
                            #       hsrp <group_number>
                            #           name <group_name>
                            configurations.append_line(attributes.format(
                                'name {group_name}'))

                            # interface <interface_name>
                            #   address-family <address_family>
                            #       hsrp <group_number>
                            #           name <session_name>
                            configurations.append_line(attributes.format(
                                'name {session_name}'))

                            # interface <interface_name>
                            #   address-family <address_family>
                            #       hsrp <group_number>
                            #           slave follow <follow>
                            configurations.append_line(attributes.format(
                                'slave follow {follow}'))

                            if attributes.value('preempt') and \
                               attributes.value('preempt_minimum_delay'):
                                # interface <interface_name>
                                #   address-family <address_family>
                                #       hsrp <group_number>
                                #           preempt delay <preempt_minimum_delay>
                                configurations.append_line(attributes.format(
                                    'preempt delay {preempt_minimum_delay}'))
                            elif attributes.value('preempt'):
                                # interface <interface_name>
                                #   address-family <address_family>
                                #       hsrp <group_number>
                                #           preempt
                                configurations.append_line(
                                    attributes.format('preempt'))

                            # interface <interface_name>
                            #   address-family <address_family>
                            #       hsrp <group_number>
                            #           priority <priority>
                            configurations.append_line(attributes.format(
                                'priority {priority}'))

                            # interface <interface_name>
                            #   address-family <address_family>
                            #       hsrp <group_number>
                            #           timers <hello_interval_seconds>\
                            #           <holdtime_seconds>
                            configurations.append_line(attributes.format(
                                'timers {hello_interval_seconds}'
                                ' {holdtime_seconds}'))

                            # interface <interface_name>
                            #   address-family <address_family>
                            #       hsrp <group_number>
                            #           timers msec <hello_interval_msec> \
                            #           msec <holdtime_msec>
                            configurations.append_line(attributes.format(
                                'timers msec {hello_interval_msec} '
                                'msec {holdtime_msec}'))

                            timers_config = ['timers ']
                            if (attributes.value('hello_msec_flag') is False)\
                             and (attributes.value('hold_msec_flag') is False):
                                # interface <interface_name>
                                #   address-family <address_family>
                                #       hsrp <group_number>
                                #           timers <hello_sec>\
                                #           <hold_sec>
                                timers_config.append(\
                                 attributes.format('{hello_sec} {hold_sec}'))
                            elif (attributes.value('hello_msec_flag') is True)\
                             and (attributes.value('hold_msec_flag') is False):
                                # interface <interface_name>
                                #   address-family <address_family>
                                #       hsrp <group_number>
                                #           timers msec <hello_msec>\
                                #           <hold_sec>
                                timers_config.append(attributes.format(\
                                    'msec {hello_msec} {hold_sec}'))
                            elif (attributes.value('hello_msec_flag') is False)\
                             and (attributes.value('hold_msec_flag') is True):
                                # interface <interface_name>
                                #   address-family <address_family>
                                #       hsrp <group_number>
                                #           timers <hello_sec>\
                                #           msec <hold_msec>
                                timers_config.append(attributes.format(\
                                    '{hello_sec} msec {hold_msec}'))
                            elif (attributes.value('hello_msec_flag') is True)\
                             and (attributes.value('hold_msec_flag') is True):
                                # interface <interface_name>
                                #   address-family <address_family>
                                #       hsrp <group_number>
                                #           timers msec <hello_msec>\
                                #           msec <hold_msec>
                                timers_config.append(attributes.format(\
                                    'msec {hello_msec} msec {hold_msec}'))
                            if timers_config[1] != '':
                                configurations.append_line(\
                                    ''.join(timers_config))

                            # interface <interface_name>
                            #   address-family <address_family>
                            #       hsrp <group_number>
                            #           track object <track_object> \
                            #           [<priority_decrement>]
                            if attributes.value('track_object') and\
                             attributes.value('priority_decrement'):
                                configurations.append_line(attributes.format(
                                    'track object {track_object}'
                                    ' {priority_decrement}'))
                            elif attributes.value('track_object'):
                                configurations.append_line(attributes.format(
                                    'track object {track_object}'))

                            # interface <interface_name>
                            #   address-family <address_family>
                            #       hsrp <group_number>
                            #           track object <tracked_object> \
                            #           [<tracked_object_priority_decrement>]
                            if attributes.value('tracked_object') and\
                             attributes.value(\
                                'tracked_object_priority_decrement'):
                                configurations.append_line(attributes.format(
                                    'track object {tracked_object}'
                                    ' {tracked_object_priority_decrement}'))
                            elif attributes.value('tracked_object'):
                                configurations.append_line(attributes.format(
                                    'track object {tracked_object}'))

                            # interface <interface_name>
                            #   address-family <address_family>
                            #       hsrp <group_number>
                            #           track <tracked_interface> \
                            #           [<tracked_intf_priority_decrement>]
                            if attributes.value('tracked_interface') and\
                             attributes.value(\
                                'tracked_intf_priority_decrement'):
                                configurations.append_line(attributes.format(
                                    'track {tracked_interface}'
                                    ' {tracked_intf_priority_decrement}'))
                            elif attributes.value('tracked_interface'):
                                configurations.append_line(attributes.format(
                                    'track {tracked_interface}'))

                return str(configurations)

            def build_unconfig(self, apply=True, attributes=None, **kwargs):
                return self.build_config(apply=apply, attributes=attributes,
                                         unconfig=True, **kwargs)

