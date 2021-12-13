__all__ = (
    'Vpc',
)

# genie
from genie.decorator import managedattribute
from genie.conf.base.base import DeviceFeature, InterfaceFeature

# genie.libs
from genie.conf.base.attributes import DeviceSubAttributes, \
    SubAttributesDict,\
    AttributesHelper, \
    KeyedSubAttributes

# Structure Hierarchy:
# Vpc
# +-- DeviceAttribute
#     +--DomainAttribute


class Vpc(DeviceFeature):

    # enabled
    enabled = managedattribute(
        name='enabled',
        default=None,
        type=(None, managedattribute.test_istype(bool)),
        doc="Enable Vpc feature.")

    # domain_id
    domain_id = managedattribute(
        name='domain_id',
        default=None,
        type=(None, managedattribute.test_istype(int)),
        doc="Vpc Domain id.")

    # auto_recovery_enabled
    auto_recovery_enabled = managedattribute(
        name='auto_recovery_enabled',
        default=None,
        type=(None, managedattribute.test_istype(bool)),
        doc="VPC settings to enable auto recovery if peer is presumed non-operational.")

    # auto_recovery_intvl [60-3600]
    auto_recovery_interval = managedattribute(
        name='auto_recovery_interval',
        default=None,
        type=(None, managedattribute.test_istype(int)),
        doc="Duration to wait before assuming peer dead and restoring vpcs.")

    # delay_restore_vpc [1-3600]
    delay_restore_vpc = managedattribute(
        name='delay_restore_vpc',
        default=None,
        type=(None, managedattribute.test_istype(int)),
        doc="Delay time in bringing up the vPC links.")

    # delay_restore_svi [1-3600]
    delay_restore_svi = managedattribute(
        name='delay_restore_svi',
        default=None,
        type=(None, managedattribute.test_istype(int)),
        doc="Delay time in bringing up interface-vlan.")

    # delay_restore_orphan [0-300]
    delay_restore_orphan = managedattribute(
        name='delay_restore_orphan',
        default=None,
        type=(None, managedattribute.test_istype(int)),
        doc="Delay time in bringing up orphan port.")

    # exclude_svi
    dual_active_exclude_svi = managedattribute(
        name='dual_active_exclude_svi',
        default=None,
        type=(None, managedattribute.test_istype(int)),
        doc="Svis to be exclude from suspension when dual-active.")

    # fast_convergence_enabled
    fast_convergence_enabled = managedattribute(
        name='fast_convergence_enabled',
        default=None,
        type=(None, managedattribute.test_istype(bool)),
        doc="Enable vPC fast-convergence.")

    # graceful_cc_enabled
    graceful_cc_enabled = managedattribute(
        name='graceful_cc_enabled',
        default=None,
        type=(None, managedattribute.test_istype(bool)),
        doc="Enable graceful type-1 consistency check.")

    # ip_arp_sync_enabled
    ip_arp_sync_enabled = managedattribute(
        name='ip_arp_sync_enabled',
        default=None,
        type=(None, managedattribute.test_istype(bool)),
        doc="Enable CFS ip arp synchronization.")

    # ipv6_nd_sync_enabled
    ipv6_nd_sync_enabled = managedattribute(
        name='ipv6_nd_sync_enabled',
        default=None,
        type=(None, managedattribute.test_istype(bool)),
        doc="Enable CFS ipv6 nd synchronization.")

    # l3_peer_router_enabled
    l3_peer_router_enabled = managedattribute(
        name='l3_peer_router_enabled',
        default=None,
        type=(None, managedattribute.test_istype(bool)),
        doc="Layer 3 peer router enabled.")

    # l3_peer_router_syslog_enabled
    l3_peer_router_syslog_enabled = managedattribute(
        name='l3_peer_router_syslog_enabled',
        default=None,
        type=(None, managedattribute.test_istype(bool)),
        doc="Layer 3 peer router syslog messages enabled.")

    # l3_peer_router_syslog_intvl [1-3600]
    l3_peer_router_syslog_intvl = managedattribute(
        name='l3_peer_router_syslog_intvl',
        default=None,
        type=(None, managedattribute.test_istype(int)),
        doc="Layer 3 peer router, How many seconds to print a syslog.")

    # mac_bpdu_src_ver
    mac_bpdu_src_ver = managedattribute(
        name='mac_bpdu_src_ver',
        default=None,
        type=(None, managedattribute.test_istype(int)),
        doc="Use version 2 bpdu source mac-address.")

    # peer_gw_exlude_enabled
    peer_gw_enabled = managedattribute(
        name='peer_gw_enabled',
        default=None,
        type=(None, managedattribute.test_istype(bool)),
        doc="Enable L3 forwarding for packets destined to peer's gateway mac-address.")

    # peer_gw_exlude_vlan
    peer_gw_exlude_vlan = managedattribute(
        name='peer_gw_exlude_vlan',
        default=None,
        type=(None, managedattribute.test_istype(int)),
        doc="VLANs to be excluded from peer-gateway functionality.")

    # peer_switch_enabled
    peer_switch_enabled = managedattribute(
        name='peer_switch_enabled',
        default=None,
        type=(None, managedattribute.test_istype(bool)),
        doc="Enable peer switch on vPC pair switches.")

    # role_priority [1-65535]
    role_priority = managedattribute(
        name='role_priority',
        default=None,
        type=(None, managedattribute.test_istype(int)),
        doc="Vpc role priority value.")

    # shutdown
    shutdown = managedattribute(
        name='shutdown',
        default=None,
        type=(None, managedattribute.test_istype(bool)),
        doc="Suspend vPC locally.")

    # system_mac
    system_mac = managedattribute(
        name='system_mac',
        default=None,
        type=(None, managedattribute.test_istype(str)),
        doc="System mac address.")

    # system_priority [1-65535]
    system_priority = managedattribute(
        name='system_priority',
        default=None,
        type=(None, managedattribute.test_istype(int)),
        doc="System priority value.")

    # track [1-65535]
    track = managedattribute(
        name='track',
        default=None,
        type=(None, managedattribute.test_istype(int)),
        doc="Tracked object value.")

    # virtual_peer_link_ip
    virtual_peer_link_ip = managedattribute(
        name='virtual_peer_link_ip',
        default=None,
        type=(None, managedattribute.test_istype(str)),
        doc="Virtual peer-link destination ip.")

    # keepalive_dst_ip
    keepalive_dst_ip = managedattribute(
        name='keepalive_dst_ip',
        default=None,
        type=(None, managedattribute.test_istype(str)),
        doc="Destination ip address of peer switch for keepalive messages.")

    # keepalive_src_ip
    keepalive_src_ip = managedattribute(
        name='keepalive_src_ip',
        default=None,
        type=(None, managedattribute.test_istype(str)),
        doc="Source ip address for keepalive messages.")

    # keepalive_vrf
    keepalive_vrf = managedattribute(
        name='keepalive_vrf',
        default=None,
        type=(None, managedattribute.test_istype(str)),
        doc="Vrf to be used for hello messages.")

    # keepalive_udp_port
    keepalive_udp_port = managedattribute(
        name='keepalive_udp_port',
        default=None,
        type=(None, managedattribute.test_istype(int)),
        doc="UDP port number used for hello.")

    # keepalive_interval
    keepalive_interval = managedattribute(
        name='keepalive_interval',
        default=None,
        type=(None, managedattribute.test_istype(int)),
        doc="Hello time interval in milliseconds.")

    # keepalive_timeout
    keepalive_timeout = managedattribute(
        name='keepalive_timeout',
        default=None,
        type=(None, managedattribute.test_istype(int)),
        doc="Hold timeout to ignore stale peer alive messages.")

    # keepalive_tos
    keepalive_tos = managedattribute(
        name='keepalive_tos',
        default=None,
        type=(None, managedattribute.test_istype(str)),
        doc="Type of Service(IPV4)/Traffic Class(IPV6).")

    # keepalive_tos_byte
    keepalive_tos_byte = managedattribute(
        name='keepalive_tos_byte',
        default=None,
        type=(None, managedattribute.test_istype(int)),
        doc="Type of Service Byte (IPv4)/Traffic Class Octet(IPv6).")

    # keepalive_precedence
    keepalive_precedence = managedattribute(
        name='keepalive_precedence',
        default=None,
        type=(None, managedattribute.test_istype(str)),
        doc="Precedence Value.")

    class DeviceAttributes(DeviceSubAttributes):

        class DomainAttributes(KeyedSubAttributes):
            def __init__(self, parent, key):
                self.domain_id = key
                super().__init__(parent=parent)

        domain_attr = managedattribute(
            name='domain_attr',
            read_only=True,
            doc=DomainAttributes.__doc__)

        @domain_attr.initter
        def domain_attr(self):
            return SubAttributesDict(
                self.DomainAttributes, parent=self)

    device_attr = managedattribute(
        name='device_attr',
        read_only=True,
        doc=DeviceAttributes.__doc__)

    @device_attr.initter
    def device_attr(self):
        return SubAttributesDict(self.DeviceAttributes, parent=self)

    def build_config(self, devices=None, apply=True, attributes=None):
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
