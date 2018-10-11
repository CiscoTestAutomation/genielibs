from enum import Enum

# Genie
from genie.decorator import managedattribute
from genie.conf.base.config import CliConfig
from genie.conf.base.base import DeviceFeature
from genie.conf.base.attributes import DeviceSubAttributes,\
                                       InterfaceSubAttributes,\
                                       SubAttributesDict,\
                                       AttributesHelper

__all__ = (
    'Hsrp',
)


class Hsrp(DeviceFeature):

    def __init__(self, group_number=None, address_family='ipv4', *args, **kwargs):
        if group_number != None:
            self.group_number = int(group_number)
        self.address_family = address_family
        super().__init__(*args, **kwargs)

    class DeviceAttributes(DeviceSubAttributes):

        class InterfaceAttributes(InterfaceSubAttributes):
            pass

        interface_attr = managedattribute(
            name='interface_attr',
            read_only=True,
            doc=InterfaceAttributes.__doc__)

        @interface_attr.initter
        def interface_attr(self):
            return SubAttributesDict(self.InterfaceAttributes, parent=self)

    device_attr = managedattribute(
        name='device_attr',
        read_only=True,
        doc=DeviceAttributes.__doc__)

    @device_attr.initter
    def device_attr(self):
        return SubAttributesDict(self.DeviceAttributes, parent=self)

    # ==================== HSRP attributes ====================

    # enabled
    enabled = managedattribute(
        name='enabled',
        default=None,
        type=(None, managedattribute.test_istype(bool)),
        doc='Enable feature HSRP')

    # state_change_disable (XR only)
    state_change_disable = managedattribute(
        name='state_change_disable',
        default=None,
        type=(None, managedattribute.test_istype(bool)),
        doc='Disable HSRP state change messages')

    # bfd (old)
    bfd = managedattribute(
        name='bfd',
        default=None,
        type=(None, managedattribute.test_istype(bool)),
        doc='Configure hsrp bfd')

    # bfd_enabled
    bfd_enabled = managedattribute(
        name='bfd_enabled',
        default=None,
        type=(None, managedattribute.test_istype(bool)),
        doc='Configure hsrp bfd')

    # minimum_delay
    minimum_delay = managedattribute(
       name='minimum_delay',
       default=None,
       type=(None, managedattribute.test_istype(int)),
       doc='Minimum delay')

    # reload_delay
    reload_delay = managedattribute(
       name='reload_delay',
       default=None,
       type=(None, managedattribute.test_istype(int)),
       doc='Delay after reload')

    # mac_refresh
    mac_refresh = managedattribute(
        name='mac_refresh',
        default=None,
        type=(None, managedattribute.test_istype(int)),
        doc='Refresh MAC cache on switch by periodically '
            'sending packet from virtual mac address')

    # use_bia
    use_bia = managedattribute(
        name='use_bia',
        default=None,
        type=(None, managedattribute.test_istype(bool)),
        doc="HSRP uses interface's burned in address")

    # hsrp/standby version
    version = managedattribute(
       name='version',
       default=None,
       type=(None, managedattribute.test_istype(int)),
       doc='Configure hsrp version')

    # hsrp/standby redirect (old)
    redirect = managedattribute(
       name='redirect',
       default=None,
       type=(None, managedattribute.test_istype(bool)),
       doc='Configure hsrp redirect')

    # redirect_disable
    redirects_disable = managedattribute(
       name='redirects_disable',
       default=None,
       type=(None, managedattribute.test_istype(bool)),
       doc='Disable hsrp redirect')

    # group_number
    group_number = managedattribute(
        name='group_number',
        default=None,
        type=(None, managedattribute.test_istype(int)),
        doc='Configure hsrp group number')

    # ==================== Interface attributes ====================

    # group_name old
    group_name = managedattribute(
        name='group_name',
        default=None,
        doc='Configure hsrp mac refresh time')

    # session_name
    session_name = managedattribute(
        name='session_name',
        default=None,
        doc='Redundancy name string')

    # ipv4 address (old)
    ip_address = managedattribute(
        name='ip_address',
        default=None,
        doc='Enable HSRP IPv4 and set the virtual IP address')

    # primary_ipv4_address
    primary_ipv4_address = managedattribute(
        name='primary_ipv4_address',
        default=None,
        type=(None, managedattribute.test_istype(str)),
        doc='Enable HSRP IPv4 and set the virtual IP address')

    # secondary_ipv4_address
    secondary_ipv4_address = managedattribute(
        name='secondary_ipv4_address',
        default=None,
        type=(None, managedattribute.test_istype(str)),
        doc='Make this IP address a secondary virtual IP address')

    # ipv6 address (old)
    ipv6_address = managedattribute(
        name='ipv6_address',
        default=None,
        doc='Enable HSRP IPv6')

    # global_ipv6_address
    global_ipv6_address = managedattribute(
        name='global_ipv6_address',
        default=None,
        type=(None, managedattribute.test_istype(str)),
        doc='Enable HSRP IPv6')

    # link_local_ipv6_address
    link_local_ipv6_address = managedattribute(
        name='link_local_ipv6_address',
        default=None,
        type=(None, managedattribute.test_istype(str)),
        doc='Enable HSRP IPv6')    

    # hsrp_linklocal
    class HSRP_LINKLOCAL(Enum):
        manual = 'manual'
        auto = 'auto'
        legacy = 'legacy'

    hsrp_linklocal = managedattribute(
        name='hsrp_linklocal',
        default=None,
        type=(None, HSRP_LINKLOCAL),
        doc='Obtain address using autoconfiguration')      

    # priority
    priority = managedattribute(
        name='priority',
        default=None,
        type=(None, managedattribute.test_istype(int)),
        doc='Priority value')

    # preepmt
    preempt = managedattribute(
        name='preempt',
        default=False,
        type=(None, managedattribute.test_istype(bool)),
        doc='Overthrow lower priority Active routers')

    # preempt delay
    preempt_minimum_delay = managedattribute(
        name='preempt_minimum_delay',
        default=False,
        type=(None, managedattribute.test_istype(int)),
        doc='Configure wait before preempting')

    # preempt reload
    preempt_reload_delay = managedattribute(
        name='preempt_reload_delay',
        default=False,
        type=(None, managedattribute.test_istype(int)),
        doc='Configure preempt reload delay')

    # preempt sync
    preempt_sync_delay = managedattribute(
        name='preempt_sync_delay',
        default=False,
        type=(None, managedattribute.test_istype(int)),
        doc='Configure wait for IP redundancy clients')

    # authentication
    authentication = managedattribute(
        name='authentication',
        default=None,
        doc='authentication string')

    # authentication_word (old)
    authentication_word = managedattribute(
        name='authentication_word',
        default=None,
        doc='Configure hsrp authentication')

    # authentication_text (old)
    authentication_text = managedattribute(
        name='authentication_text',
        default=None,
        doc='Configure hsrp authentication text')

    # authentication_md5_keychain (old)
    authentication_md5_keychain = managedattribute(
        name='authentication_md5_keychain',
        default=None,
        doc='Configure hsrp MD5 authentication with keychain')

    # authentication_md5_keystring (old)
    authentication_md5_keystring = managedattribute(
        name='authentication_md5_keystring',
        default=None,
        doc='Configure hsrp MD5 authentication with keystring')

    # track object (old)
    track_object = managedattribute(
        name='track_object',
        default=None,
        type=(None, managedattribute.test_istype(int)),
        doc='Configure hsrp track')

    # tracked_object
    tracked_object = managedattribute(
        name='tracked_object',
        default=None,
        type=(None, managedattribute.test_istype(int)),
        doc='Tracked object number')

    # priority decrement (old)
    priority_decrement = managedattribute(
        name='priority_decrement',
        default=None,
        type=(None, managedattribute.test_istype(int)),
        doc='Configure hsrp track priority decrement')

    # tracked_object_priority_decrement
    tracked_object_priority_decrement = managedattribute(
        name='tracked_object_priority_decrement',
        default=None,
        type=(None, managedattribute.test_istype(int)),
        doc='Priority decrement')

    # tracked_interface
    tracked_interface = managedattribute(
        name='track_interface',
        default=None,
        type=(None, managedattribute.test_istype(str)),
        doc='Configuring tracking interface')

    # tracked_intf_priority_decrement
    tracked_intf_priority_decrement = managedattribute(
        name='tracked_intf_priority_decrement',
        default=None,
        type=(None, managedattribute.test_istype(int)),
        doc='Priority decrement')

    # hello_msec_flag
    hello_msec_flag = managedattribute(
        name='hello_msec_flag',
        default=False,
        type=(None, managedattribute.test_istype(bool)),
        doc='Specify hello interval in milliseconds')

    # hold_msec_flag
    hold_msec_flag = managedattribute(
        name='hold_msec_flag',
        default=False,
        type=(None, managedattribute.test_istype(bool)),
        doc='Specify hold time in milliseconds')

    # timer hello interval in seconds (old)
    hello_interval_seconds = managedattribute(
        name='hello_interval_seconds',
        default=None,
        type=(None, managedattribute.test_istype(int)),
        doc='Configure hsrp timer hello interval in seconds')

    # hello_sec
    hello_sec = managedattribute(
        name='hello_sec',
        default=None,
        type=(None, managedattribute.test_istype(int)),
        doc='Hello interval in seconds')

    # timer hold time in seconds (old)
    holdtime_seconds = managedattribute(
        name='holdtime_seconds',
        default=None,
        type=(None, managedattribute.test_istype(int)),
        doc='Configure hsrp timer holdtime in seconds')

    # hold_sec
    hold_sec = managedattribute(
        name='hold_sec',
        default=None,
        type=(None, managedattribute.test_istype(int)),
        doc='Hold time in seconds')

    # timer hello interval in mseconds (old)
    hello_interval_msec = managedattribute(
        name='hello_interval_msec',
        default=None,
        type=(None, managedattribute.test_istype(int)),
        doc='Configure hsrp timer hello interval in milli-seconds')

    # hello_msec
    hello_msec = managedattribute(
        name='hello_msec',
        default=None,
        type=(None, managedattribute.test_istype(int)),
        doc='Hello interval in milliseconds')

    # timer hold time in seconds (old)
    holdtime_msec = managedattribute(
        name='holdtime_msec',
        default=None,
        type=(None, managedattribute.test_istype(int)),
        doc='Configure hsrp timer holdtime in milli-seconds')

    # hold_msec
    hold_msec = managedattribute(
        name='hold_msec',
        default=None,
        type=(None, managedattribute.test_istype(int)),
        doc='Hold time in milliseconds')

    # virtual_ip_learn
    virtual_ip_learn = managedattribute(
        name='virtual_ip_learn',
        default=None,
        type=(None, managedattribute.test_istype(bool)),
        doc='Enable HSRP IPv4 and learn virtual IP address')

    # follow
    follow = managedattribute(
        name='follow',
        default=None,
        type=(None, managedattribute.test_istype(str)),
        doc='Name of HSRP group to follow')

    # mac_address (old)
    mac_address = managedattribute(
        name='mac_address',
        default=None,
        doc='Configure hsrp mac refresh time')

    # virtual_mac_address
    virtual_mac_address = managedattribute(
        name='virtual_mac_address',
        default=None,
        doc='Virtual MAC address')

    # ==================== IOSXE specific ====================

    # track shutdown
    track_shutdown = managedattribute(
        name='track_shutdown',
        default=None,
        type=(None, managedattribute.test_istype(bool)),
        doc='Configure hsrp track priority decrement')

    # ==================== IOSXR specific ====================

    # bfd_min_interval (old)
    bfd_min_interval = managedattribute(
        name='bfd_min_interval',
        default=None,
        type=(None, managedattribute.test_istype(int)),
        doc='Configure hsrp bfd minimum interval')

    # bfd_interval
    bfd_interval = managedattribute(
        name='bfd_interval',
        default=None,
        type=(None, managedattribute.test_istype(int)),
        doc='Configure hsrp bfd minimum interval')

    # bfd_multiplier (old)
    bfd_multiplier = managedattribute(
        name='bfd_multiplier',
        default=None,
        type=(None, managedattribute.test_istype(int)),
        doc='Configure hsrp bfd multiplier')

    # bfd_detection_multiplier
    bfd_detection_multiplier = managedattribute(
        name='bfd_detection_multiplier',
        default=None,
        type=(None, managedattribute.test_istype(int)),
        doc='Configure hsrp bfd multiplier')

    # bfd_address
    bfd_address = managedattribute(
        name='bfd_address',
        default=None,
        type=(None, managedattribute.test_istype(str)),
        doc='HSRP BFD remote interface IP address')

    # bfd_interface_name
    bfd_interface_name = managedattribute(
        name='bfd_interface_name',
        default=None,
        type=(None, managedattribute.test_istype(str)),
        doc='HSRP BFD outgoing interface')

    # address_family
    class ADDRESS_FAMILY(Enum):
        ipv4='ipv4'
        ipv6='ipv6'

    address_family = managedattribute(
       name='address_family',
       default='ipv4',
       type=(None, ADDRESS_FAMILY),
       doc='Configure hsrp address family')

    # bfd_fast_detect
    bfd_fast_detect = managedattribute(
        name='bfd_fast_detect',
        default=None,
        type=(None, managedattribute.test_istype(bool)),
        doc='Configure hsrp bfd fast detect')

    # ==================== NXOS specific ====================

    # feature hsrp
    enabled = managedattribute(
        name='enabled',
        default=False,
        type=(None, managedattribute.test_istype(bool)),
        doc='Enable or disable feature hsrp')

    # ===========================================================

    def build_config(self, devices=None, apply=True, attributes=None,
                     unconfig=False):
        cfgs = {}
        attributes = AttributesHelper(self, attributes)
        if devices is None:
            devices = self.devices
        devices = set(devices)

        for key, sub, attributes2 in attributes.mapping_items(
                'device_attr', sort=True):
            cfgs[key] = sub.build_config(apply=False, attributes=attributes2)
        if apply:
            for device_name, cfg in sorted(cfgs.items()):
                self.testbed.config_on_devices(cfg, fail_invalid=True)
        else:
            return cfgs

    def build_unconfig(self, devices=None, apply=True, attributes=None):
        cfgs = {}
        attributes = AttributesHelper(self, attributes)
        if devices is None:
            devices = self.devices
        devices = set(devices)

        for key, sub, attributes2 in attributes.mapping_items(
                'device_attr', sort=True):
            cfgs[key] = sub.build_unconfig(apply=False, attributes=attributes2)

        if apply:
            for device_name, cfg in sorted(cfgs.items()):
                self.testbed.config_on_devices(cfg, fail_invalid=True)
        else:
            return cfgs

