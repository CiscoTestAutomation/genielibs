'''
IOSXE Genie Conf using YANG for feature Standby.
'''

# Python
from abc import ABC
import warnings
import string

# Genie
from genie.conf.base import Interface
from genie.conf.base.cli import CliConfigBuilder
from genie.conf.base.config import YangConfig
from genie.conf.base.attributes import UnsupportedAttributeWarning,\
                                       AttributesHelper

# YDK
try:
    from ydk.models.cisco_iosxe_native import Cisco_IOS_XE_native as ned
    from ydk.types import DELETE, Empty
    from ydk.services import CRUDService

    # patch a netconf provider
    from ydk.providers import NetconfServiceProvider as _NetconfServiceProvider
    from ydk.providers._provider_plugin import _ClientSPPlugin
    from ydk.services import CodecService
    from ydk.providers import CodecServiceProvider

    class NetconfServiceProvider(_NetconfServiceProvider):
        def __init__(self, device):
            if 'yang' not in device.mapping:
                # Want it, but dont have a connection? 
                raise Exception("Missing connection of "
                                "type 'yang' in the device "
                                "mapping '{map}'".format(map=device.mapping))
            alias = device.mapping['yang']
            dev = device.connectionmgr.connections[alias]

            super().__init__(address=str(dev.connection_info.ip),
                             port=dev.connection_info.port,
                             username=dev.connection_info.username,
                             password=dev.connection_info.password,
                             protocol = 'ssh')

            self.sp_instance = _ClientSPPlugin(self.timeout,
                                               use_native_client=False)

            self.sp_instance._nc_manager = dev
        def _connect(self, *args, **kwargs): pass
except:
    pass


class Hsrp(ABC):

    class DeviceAttributes(ABC):

        def build_config(self, devices=None, apply=True, attributes=None,
                         unconfig=False, **kwargs):

            assert not apply
            attributes = AttributesHelper(self, attributes)
            configurations = CliConfigBuilder(unconfig=unconfig)
            hsrp_config = []

            # loop over all interfaces
            for sub, attributes2 in attributes.mapping_values(
                    'interface_attr', keys=self.interface_attr.keys()):

                hsrp_config.append(sub.build_config(apply=False,
                     attributes=attributes2, unconfig=unconfig, **kwargs))

            # instantiate crud service
            crud_service = CRUDService()

            if apply:
                for interface in hsrp_config:
                    interface.apply()
            
            else:
                ydks = []
                if unconfig:
                    for interface in hsrp_config:
                        ydks.append(interface)
                else:
                    for interface in hsrp_config:
                        ydks.append(interface)

                return ydks

        def build_unconfig(self, apply=True, attributes=None, **kwargs):
            return self.build_config(apply=apply, attributes=attributes,
                                     unconfig=True, **kwargs)

        class InterfaceAttributes(ABC):

            def build_config(self, apply=True, attributes=None, unconfig=False,
                             **kwargs):
                
                assert not apply
                crud_service = CRUDService()
                attributes = AttributesHelper(self, attributes)
                configurations = CliConfigBuilder(unconfig=unconfig)
                intf_name = attributes.value('interface_name')

                if intf_name.startswith('Gig'):
                    ydk_obj = ned.Native.Interface.Gigabitethernet()
                elif intf_name.startswith('Ten'):
                    ydk_obj = ned.Native.Interface.Tengigabitethernet()

                # Set the interface name
                keep = {string.digits + '//'}
                ydk_obj.name = ''.join(i for i in attributes.value(
                               'interface_name') if i in keep)

                # Standby Object
                standby_obj = ydk_obj.Standby()
                ydk_obj.standby = standby_obj

                # =============
                # leaf: version
                # =============
                # interface <interface_name>
                #   standby version <version>
                if attributes.value('version') == 2:
                    version_obj = ydk_obj.standby.VersionEnum.Y_2
                    standby_obj.version = version_obj
                elif attributes.value('version') == 1:
                    version_obj = ydk_obj.standby.VersionEnum.Y_1
                    standby_obj.version = version_obj

                # =========
                # leaf: bfd
                # =========
                # interface <interface_name>
                #   standby <bfd>
                if attributes.value('bfd'):
                    standby_obj.bfd = Empty()

                # ===========
                # leaf: delay
                # ===========
                # interface <interface_name>
                #   standby delay minimum <minimum_delay>\
                #   reload <reload_delay>
                if attributes.value('minimum_delay') and \
                   attributes.value('reload_delay'):
                    delay_obj = standby_obj.Delay()
                    delay_obj.minimum = int(attributes.value('minimum_delay'))
                    delay_obj.reload = int(attributes.value('reload_delay'))
                    standby_obj.delay = delay_obj
                elif attributes.value('minimum_delay'):
                    delay_obj = standby_obj.Delay()
                    delay_obj.minimum = int(attributes.value('minimum_delay'))
                    standby_obj.delay = delay_obj
                
                # =================
                # leaf: mac-refresh
                # =================
                # interface <interface_name>
                #   standby mac-refresh <mac_refresh>
                if attributes.value('mac_refresh'):
                    standby_obj.mac_refresh = \
                        int(attributes.value('mac_refresh'))

                # =============
                # leaf: use-bia
                # =============
                # interface <interface_name>
                #   standby use-bia scope interface
                if attributes.value('use_bia'):
                    use_bia_obj = ydk_obj.standby.UseBia()
                    scope_obj = ydk_obj.standby.UseBia.Scope()
                    scope_obj.interface = Empty()
                    use_bia_obj.scope = scope_obj
                    standby_obj.use_bia = use_bia_obj

                # ==================
                # leaf: standby-list
                # ==================
                if attributes.value('group_number') is not None:

                    # ==================
                    # leaf: group_number
                    # ==================
                    standby_list_obj = ydk_obj.standby.StandbyList()
                    standby_list_obj.group_number = \
                        int(attributes.value('group_number'))

                    # ====================
                    # leaf: authentication
                    # ====================
                    if attributes.value('authentication_word'):
                        # interface <interface_name>
                        #   standby <group_number> authentication \
                        #   <authentication_word>
                        authentication_obj = standby_list_obj.Authentication()
                        authentication_obj.word = \
                            attributes.value('authentication_word')
                        standby_list_obj.authentication = authentication_obj
                    
                    elif attributes.value('authentication_text'):
                        # interface <interface_name>
                        #   standby <group_number> authentication text \
                        #   <authentication_text>
                        authentication_obj = standby_list_obj.Authentication()
                        authentication_obj.word = \
                            attributes.value('authentication_text')
                        standby_list_obj.authentication = authentication_obj

                    elif attributes.value('authentication_md5_keychain'):
                        # interface <interface_name>
                        #   standby <group_number> authentication \
                        #   md5 key-chain <authentication_md5_keychain>
                        authentication_obj = standby_list_obj.Authentication()
                        md5_obj = authentication_obj.Md5()
                        md5_obj.key_chain = \
                            attributes.value('authentication_md5_keychain')
                        authentication_obj.md5 = md5_obj
                        standby_list_obj.authentication = authentication_obj

                    elif attributes.value('authentication_md5_keystring'):
                        # interface <interface_name>
                        #   standby <group_number> authentication \
                        #   md5 key-string <authentication_md5_keystring>
                        authentication_obj = standby_list_obj.Authentication()
                        md5_obj = authentication_obj.Md5()
                        key_string_obj = md5_obj.KeyString()
                        key_string_obj.string = \
                            attributes.value('authentication_md5_keystring')
                        md5_obj.key_string = key_string_obj
                        authentication_obj.md5 = md5_obj
                        standby_list_obj.authentication = authentication_obj

                    # ============
                    # leaf: follow
                    # ============
                    # interface <interface_name>
                    #   standby <group_number> follow <follow>
                    if attributes.value('follow'):
                        standby_list_obj.follow = attributes.value('follow')

                    # ========
                    # leaf: ip
                    # ========
                    # interface <interface_name>
                    #   standby <group_number> ip <ip_address>
                    if attributes.value('ip_address'):
                        ip_obj = standby_list_obj.Ip()
                        ip_obj.address = attributes.value('ip_address')
                        standby_list_obj.ip = ip_obj

                    # ==========
                    # leaf: ipv6
                    # ==========
                    # interface <interface_name>
                    #   standby <group_number> ip <ip_address>
                    if attributes.value('ipv6_address') == 'autoconfig':
                        ipv6_obj = standby_list_obj.Ipv6Enum.autoconfig
                        standby_list_obj.ipv6 = ipv6_obj
                    else:
                        standby_list_obj.ipv6 = \
                            attributes.value('ipv6_address')

                    # =================
                    # leaf: mac-address
                    # =================
                    # interface <interface_name>
                    #   standby <group_number> mac-address <mac_address>
                    if attributes.value('mac_address'):
                        standby_list_obj.mac_address = \
                            attributes.value('mac_address')

                    # ==========
                    # leaf: name
                    # ==========
                    # interface <interface_name>
                    #   standby <group_number> name <group_name>
                    if attributes.value('group_name'):
                        standby_list_obj.name =  attributes.value('group_name')

                    # =============
                    # leaf: preempt
                    # =============
                    if attributes.value('preempt') and \
                       attributes.value('preempt_minimum_delay') and \
                       attributes.value('preempt_reload_delay') and \
                       attributes.value('preempt_sync_delay'):
                        # interface <interface_name>
                        #   standby <group_number> preempt delay \
                        #   minimum <preempt_minimum_delay> reload \
                        #   <preempt_reload> sync <preempt_sync>
                        preempt_obj = standby_list_obj.Preempt()
                        preempt_obj_delay = preempt_obj.Delay()
                        preempt_obj_delay.minimum = \
                            int(attributes.value('preempt_minimum_delay'))
                        preempt_obj_delay.reload = \
                            int(attributes.value('preempt_reload_delay'))
                        preempt_obj_delay.sync = \
                            int(attributes.value('preempt_sync_delay'))
                        preempt_obj.delay = preempt_obj_delay
                        standby_list_obj.preempt = preempt_obj
                    elif attributes.value('preempt') and \
                         attributes.value('preempt_minimum_delay') and \
                         attributes.value('preempt_reload_delay'):
                        # interface <interface_name>
                        #   standby <group_number> preempt delay \
                        #   minimum <preempt_minimum_delay> \
                        #   reload <preempt_reload>
                        preempt_obj = standby_list_obj.Preempt()
                        preempt_obj_delay = preempt_obj.Delay()
                        preempt_obj_delay.minimum = \
                            int(attributes.value('preempt_minimum_delay'))
                        preempt_obj_delay.reload = \
                            int(attributes.value('preempt_reload_delay'))
                        preempt_obj.delay = preempt_obj_delay
                        standby_list_obj.preempt = preempt_obj
                    elif attributes.value('preempt') and \
                         attributes.value('preempt_minimum_delay'):
                        # interface <interface_name>
                        #   standby <group_number> preempt delay \
                        #   minimum <preempt_minimum_delay>
                        preempt_obj = standby_list_obj.Preempt()
                        preempt_obj_delay = preempt_obj.Delay()
                        preempt_obj_delay.minimum = \
                            int(attributes.value('preempt_minimum_delay'))
                        preempt_obj.delay = preempt_obj_delay
                        standby_list_obj.preempt = preempt_obj
                    elif attributes.value('preempt'):
                        # interface <interface_name>
                        #   standby <group_number> preempt delay
                        preempt_obj = standby_list_obj.Preempt()
                        preempt_obj_delay = preempt_obj.Delay()
                        preempt_obj.delay = preempt_obj_delay
                        standby_list_obj.preempt = preempt_obj

                    # ==============
                    # leaf: priority
                    # ==============
                    # interface <interface_name>
                    #   standby <group_number> priority <priority>
                    if attributes.value('priority'):
                        standby_list_obj.priority = \
                            int(attributes.value('priority'))

                    # ==============
                    # leaf: redirect
                    # ==============
                    # TODO: this is a bug

                    # ============
                    # leaf: timers
                    # ============
                    if attributes.value('hello_interval_seconds') and \
                       attributes.value('holdtime_seconds'):
                        # interface <interface_name>
                        #   standby <group_number> timers \
                        #   <hello_interval_seconds> <holdtime_seconds>
                        timers_obj = standby_list_obj.Timers()
                        hello_interval_obj = timers_obj.HelloInterval()
                        hello_interval_obj.seconds = \
                            int(attributes.value('hello_interval_seconds'))
                        timers_obj.hello_interval =  hello_interval_obj
                        hold_time_obj = timers_obj.HoldTime()
                        hold_time_obj.seconds = \
                            attributes.value('holdtime_seconds')
                        timers_obj.hold_time = hold_time_obj
                        standby_list_obj.timers = timers_obj
                    elif attributes.value('hello_interval_msec') and \
                         attributes.value('holdtime_msec'):
                        # interface <interface_name>
                        #   standby <group_number> timers msec \
                        #   <hello_interval_msec> msec <holdtime_msec>
                        timers_obj = standby_list_obj.Timers()
                        hello_interval_obj = timers_obj.HelloInterval()
                        hello_interval_obj.msec = \
                            int(attributes.value('hello_interval_msec'))
                        timers_obj.hello_interval =  hello_interval_obj
                        hold_time_obj = timers_obj.HoldTime()
                        hold_time_obj.msec = attributes.value('holdtime_msec')
                        timers_obj.hold_time = hold_time_obj
                        standby_list_obj.timers = timers_obj

                    # ===========
                    # leaf: track
                    # ===========
                    if attributes.value('track_object') and \
                       attributes.value('priority_decrement'):
                        # interface <interface_name>
                        #   standby <group_number> track object <track_object> \
                        #   decrement <priority_decrement>
                        track_obj = standby_list_obj.Track()
                        track_obj.number = attributes.value('track_object')
                        track_obj.decrement = \
                            int(attributes.value('priority_decrement'))
                        standby_list_obj.track.append(track_obj)
                    elif attributes.value('track_object') and \
                         attributes.value('track_shutdown'):
                        # interface <interface_name>
                        #   standby <group_number> track object <track_object> \
                        #   shutdown
                        track_obj = standby_list_obj.Track()
                        track_obj.number = attributes.value('track_object')
                        track_obj.shutdown = Empty()
                        standby_list_obj.track.append(track_obj)

                    # Add standby_list_obj to standby_obj
                    standby_obj.standby_list.append(standby_list_obj)

                if unconfig:
                    return YangConfig(device=self.device,
                                      ydk_obj=ydk_obj,
                                      ncp=NetconfServiceProvider,
                                      crud_service=crud_service.delete)
                else:
                    return YangConfig(device=self.device,
                                      ydk_obj=ydk_obj,
                                      ncp=NetconfServiceProvider,
                                      crud_service=crud_service.create)

            def build_unconfig(self, apply=True, attributes=None, **kwargs):
                return self.build_config(apply=apply, attributes=attributes, 
                                         unconfig=True, **kwargs)

