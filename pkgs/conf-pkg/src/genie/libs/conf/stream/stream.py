
__all__ = (
    'Stream',
    'StreamStats',
)

import functools
import collections
from collections import abc
import itertools
import enum
import logging
import datetime
import operator
import re
logger = logging.getLogger(__name__)

try:
    from pyats.tcl import tclstr
    item_cast = tclstr
except Exception:
    item_cast = None

from collections import defaultdict
from genie.utils.cisco_collections import Range
from genie.utils.cisco_collections import typedset

from genie.decorator import managedattribute
from genie.conf.base import Device
from genie.conf.base import ConfigurableBase
import genie.conf.base.attributes
from genie.conf.base.attributes import SubAttributes, KeyedSubAttributes, \
    AttributesHelper
from genie.conf.base.sprinkler import IpUtils

from genie.libs.conf.base import \
    IPv4Address, IPv4AddressRange, IPv4InterfaceRange, \
    IPv6Address, IPv6AddressRange, IPv6InterfaceRange, \
    MAC, MACRange
from genie.libs.conf.interface import \
    Interface, EthernetInterface, AtmInterface, PosInterface, TunnelInterface
from genie.libs.conf.mcast import \
    MulticastGroup

from genie.libs.conf.utils import round_nearest


def _IPv4InterfaceRange_to_IPv4AddressRange(value):
    if isinstance(value, IPv4InterfaceRange):
        return IPv4AddressRange(value.start.ip, value.stop.ip, value.step)
    raise TypeError(value)


def _IPv6InterfaceRange_to_IPv6AddressRange(value):
    if isinstance(value, IPv6InterfaceRange):
        return IPv4AddressRange(value.start.ip, value.stop.ip, value.step)
    raise TypeError(value)


def _asdict(self):
    d = {}
    for k in dir(self):
        if k.startswith('_'):
            continue
        try:
            v = getattr(self, k)
        except:
            continue
        if callable(v):
            continue
        if getattr(v, 'asdict', None):
            v = v.asdict()
        elif isinstance(v, abc.Mapping):
            v = {k2: v2.asdict() if getattr(v2, 'asdict', None) else v2
                 for k2, v2 in v.items()}
        d[k] = v
    return d


class _StatsBase(object):

    asdict = _asdict

    def __sub__(self, other):
        d = type(self)()

        for attr in set(dir(self)) | set(dir(other)):
            if attr.startswith('_'):
                # Private... sub-class must handle if important
                continue
            if attr.endswith('_delay') \
                    or attr.endswith('_length') \
                    or attr.endswith('_rate'):
                # Makes no sense substituting these
                continue
            v_self = getattr(self, attr, None)
            if v_self is None:
                v_self = 0
            v_other = getattr(other, attr, None)
            if v_other is None:
                v_other = 0
            try:
                setattr(d, attr, v_self - v_other)
            except TypeError:
                pass

        return d

    def _update_rate_stats(self, elapsed_time):
        pass


class TxStats(_StatsBase):
    '''Generic TX statistics'''
    total_pkts = None
    total_pkt_rate = None
    total_pkt_bits = None
    total_pkt_bit_rate = None
    total_pkt_bytes = None
    total_pkt_byte_rate = None

    def _update_rate_stats(self, elapsed_time):
        super()._update_rate_stats(elapsed_time)

        map_count_rate_stats = {
            'total_pkts': 'total_pkt_rate',
            'total_pkt_bits': 'total_pkt_bit_rate',
            'total_pkt_bytes': 'pkt_byte_rate',
        }

        for count_attr, rate_attr in map_count_rate_stats.items():
            count_value = getattr(self, count_attr, None)
            if count_value is None:
                continue
            try:
                setattr(self, rate_attr, count_value / elapsed_time)
            except (TypeError, ZeroDivisionError):
                pass


class RxStats(_StatsBase):
    '''Generic RX statistics'''
    total_pkts = None
    total_pkt_rate = None
    total_pkt_bits = None
    total_pkt_bit_rate = None
    total_pkt_bytes = None
    total_pkt_byte_rate = None
    min_delay = None
    max_delay = None
    avg_delay = None
    out_of_sequence_pkts = None
    out_of_sequence_pkt_rate = None
    x_adv_seq_in_order_pkts = None
    x_adv_seq_in_order_pkt_rate = None
    x_adv_seq_reordered_pkts = None
    x_adv_seq_reordered_pkt_rate = None
    x_adv_seq_late_pkts = None
    x_adv_seq_late_pkt_rate = None
    x_adv_seq_duplicate_pkts = None
    x_adv_seq_duplicate_pkt_rate = None
    x_adv_seq_dropped_pkts = None
    x_adv_seq_dropped_pkt_rate = None
    x_has_port_stray_pkts = None

    def _update_rate_stats(self, elapsed_time):
        super()._update_rate_stats(elapsed_time)

        map_count_rate_stats = {
            'total_pkts': 'total_pkt_rate',
            'total_pkt_bits': 'total_pkt_bit_rate',
            'total_pkt_bytes': 'pkt_byte_rate',
            'total_pkt_bytes': 'total_pkt_byte_rate',
            'out_of_sequence_pkts': 'out_of_sequence_pkt_rate',
            'x_adv_seq_in_order_pkts': 'x_adv_seq_in_order_pkt_rate',
            'x_adv_seq_reordered_pkts': 'x_adv_seq_reordered_pkt_rate',
            'x_adv_seq_late_pkts': 'x_adv_seq_late_pkt_rate',
            'x_adv_seq_duplicate_pkts': 'x_adv_seq_duplicate_pkt_rate',
            'x_adv_seq_dropped_pkts': 'x_adv_seq_dropped_pkt_rate',
        }

        for count_attr, rate_attr in map_count_rate_stats.items():
            count_value = getattr(self, count_attr, None)
            if count_value is None:
                continue
            try:
                setattr(self, rate_attr, count_value / elapsed_time)
            except (TypeError, ZeroDivisionError):
                pass


class BySubStreamTxStats(TxStats):
    '''Sub-stream TX statistics'''
    pass


class BySubStreamRxStats(RxStats):
    '''Sub-stream RX statistics'''
    pass


class StreamTxStats(TxStats):
    '''Stream TX statistics'''

    # dict of BySubStreamTxStats
    by_sub_stream = managedattribute(
        name='by_sub_stream',
        read_only=True,
        finit=dict)

    def __sub__(self, other):
        d = super().__sub__(other)

        for sub_stream in set(self.by_sub_stream.keys()) | set(other.by_sub_stream.keys()):
            self_by_sub_stream = self.by_sub_stream.get(sub_stream, None) or BySubStreamTxStats()
            other_by_sub_stream = other.by_sub_stream.get(sub_stream, None) or BySubStreamTxStats()
            d.by_sub_stream[sub_stream] = self_by_sub_stream - other_by_sub_stream

        return d

    def _update_rate_stats(self, elapsed_time):
        super()._update_rate_stats(elapsed_time)
        for sub in self.by_sub_stream.values():
            sub._update_rate_stats(elapsed_time)


class StreamRxStats(RxStats):
    '''Stream RX statistics'''

    # dict of BySubStreamRxStats
    by_sub_stream = managedattribute(
        name='by_sub_stream',
        read_only=True,
        finit=dict)

    def __sub__(self, other):
        d = super().__sub__(other)

        for sub_stream in set(self.by_sub_stream.keys()) | set(other.by_sub_stream.keys()):
            self_by_sub_stream = self.by_sub_stream.get(sub_stream, None) or BySubStreamRxStats()
            other_by_sub_stream = other.by_sub_stream.get(sub_stream, None) or BySubStreamRxStats()
            d.by_sub_stream[sub_stream] = self_by_sub_stream - other_by_sub_stream

        return d

    def _update_rate_stats(self, elapsed_time):
        super()._update_rate_stats(elapsed_time)
        for sub in self.by_sub_stream.values():
            sub._update_rate_stats(elapsed_time)


class ByInterfaceStreamStats(object):
    '''Statistics for an interface'''

    tx = managedattribute(
        name='tx',
        read_only=True,
        finit=StreamTxStats,
        doc=StreamTxStats.__doc__)

    rx = managedattribute(
        name='rx',
        read_only=True,
        finit=StreamRxStats,
        doc=StreamRxStats.__doc__)

    asdict = _asdict

    def __sub__(self, other):
        d = ByInterfaceStreamStats()

        d._tx = self.tx - other.tx
        d._rx = self.rx - other.rx

        return d

    def _update_rate_stats(self, elapsed_time):
        self.tx._update_rate_stats(elapsed_time)
        self.rx._update_rate_stats(elapsed_time)


class ByStreamStats(object):
    '''Statistics for a stream'''

    tx = managedattribute(
        name='tx',
        read_only=True,
        finit=StreamTxStats,
        doc=StreamTxStats.__doc__)

    rx = managedattribute(
        name='rx',
        read_only=True,
        finit=StreamRxStats,
        doc=StreamRxStats.__doc__)

    # dict of ByInterfaceStreamStats
    by_interface = managedattribute(
        name='by_interface',
        read_only=True,
        finit=dict)

    elapsed_time = None

    asdict = _asdict

    def __sub__(self, other):
        d = ByStreamStats()

        d._tx = self.tx - other.tx
        d._rx = self.rx - other.rx

        for interface in set(self.by_interface.keys()) | set(other.by_interface.keys()):
            self_by_interface = self.by_interface.get(interface, None) or ByInterfaceStreamStats()
            other_by_interface = other.by_interface.get(interface, None) or ByInterfaceStreamStats()
            d.by_interface[interface] = self_by_interface - other_by_interface

        try:
            self.elapsed_time = self.elapsed_time - other.elapsed_time
        except TypeError:
            pass

        if self.elapsed_time:
            d.tx._update_rate_stats(self.elapsed_time)
            d.rx._update_rate_stats(self.elapsed_time)
            for sub in d.by_interface.values():
                sub._update_rate_stats(self.elapsed_time)

        return d


class StreamStats(object):

    ByStreamStats = ByStreamStats
    BySubStreamTxStats = BySubStreamTxStats
    BySubStreamRxStats = BySubStreamRxStats
    ByInterfaceStreamStats = ByInterfaceStreamStats

    # dict of ByStreamStats
    by_stream = managedattribute(
        name='by_stream',
        read_only=True,
        finit=dict)

    collect_time = None

    def __init__(self):
        self.collect_time = datetime.datetime.now()

    asdict = _asdict

    def __sub__(self, other):

        d = StreamStats()
        d.collect_time = other.collect_time

        for stream in set(self.by_stream.keys()) | set(other.by_stream.keys()):
            self_by_stream = self.by_stream.get(stream, None) or ByStreamStats()
            other_by_stream = other.by_stream.get(stream, None) or ByStreamStats()
            d.by_stream[stream] = self_by_stream - other_by_stream

        return d

@functools.total_ordering
class Stream(ConfigurableBase):

    @property
    def device(self):
        return self.source_tgen_interface.device

    @property
    def testbed(self):
        return self.device.testbed

    @testbed.setter
    def testbed(self, value):
        raise AttributeError(
            'can\'t set attribute; Testbed must be derived from either the'
            ' source or source_tgen_interface parameters')

    name = managedattribute(
        name='name',
        default=None)

    tgen_handle = managedattribute(
        name='tgen_handle',
        default=None,
        type=(None,
              managedattribute.test_tuple_of(str)),
        doc='''The stream handle, as understood by HLTAPI/low-level vendor APIs.

            Note that this can be string representation of multiple sub-stream handles.
        ''')

    bandwidth = managedattribute(
        name='bandwidth',
        default=10,
        type=managedattribute.test_istype((int, float)),
        doc='Bandwidth of the stream -- See also bandwidth_units')

    class BandwidthUnits(enum.Enum):
        mbps = 'mbps'
        kbps = 'kbps'
        bps = 'bps'
        pps = 'pps'
        percent = 'percent'

    bandwidth_units = managedattribute(
        name='bandwidth_units',
        default=BandwidthUnits.kbps,
        type=BandwidthUnits,
        doc='Units used to represent the bandwidth -- See Stream.BandwidthUnits')

    frame_length = managedattribute(
        name='frame_length',
        type=(None, managedattribute.test_istype(int)))

    @frame_length.defaulter
    def frame_length(self):
        layer3_protocol = self.layer3_protocol
        if layer3_protocol in (
                None,
                Stream.Layer3Protocol.ipv4,
                Stream.Layer3Protocol.ipv6,
                Stream.Layer3Protocol.ipx,
                Stream.Layer3Protocol.raw_ipv4_socket,
        ):
            return 512
        else:
            return None

    class FrameLengthMode(enum.Enum):
        l2 = 'l2',
        l3 = 'l3',

    frame_length_mode = managedattribute(
        name='frame_length_mode',
        default=FrameLengthMode.l2,
        type=FrameLengthMode)

    class TransmitMode(enum.Enum):
        continuous = 'continuous'
        random_spaced = 'random_spaced'
        single_pkt = 'single_pkt'
        single_burst = 'single_burst'
        multi_burst = 'multi_burst'
        continuous_burst = 'continuous_burst'
        fixed = 'fixed'

    transmit_mode = managedattribute(
        name='transmit_mode',
        default=TransmitMode.continuous,
        type=TransmitMode)

    packets_per_burst = managedattribute(
        name='packets_per_burst',
        default=None,
        type=(None, managedattribute.test_istype(int)))

    bidirectional = managedattribute(
        name='bidirectional',
        default=False,
        type=managedattribute.test_in((
            False,
        )))  # TODO Support bidirectional traffic

    source_tgen_interface = managedattribute(
        name='source_tgen_interface',
        type=(None, managedattribute.test_isinstance(Interface)))

    @source_tgen_interface.defaulter
    def source_tgen_interface(self):
        source = self.source
        if isinstance(source, Interface):
            return source.tgen_interface
        raise AttributeError

    destination_tgen_interfaces = managedattribute(
        name='destination_tgen_interfaces',
        type=typedset(managedattribute.test_isinstance(Interface))._from_iterable)

    @destination_tgen_interfaces.defaulter
    def destination_tgen_interfaces(self):
        destination = self.destination
        if isinstance(destination, Interface) \
                and destination.device is self.device:
            # TODO
            return frozenset({destination})
        if isinstance(destination, Interface) \
                and getattr(destination, 'tgen_device', None) is self.device:
            # TODO
            return frozenset({destination.tgen_interface})
        # TODO
        return frozenset()

    source = managedattribute(
        name='source',
        type=(
            IPv4Address,
            IPv6Address,
            MAC,
            managedattribute.test_isinstance((
                Interface,
                IPv4AddressRange,
                IPv6AddressRange,
                MACRange,
            )),
            _IPv4InterfaceRange_to_IPv4AddressRange,
            _IPv6InterfaceRange_to_IPv6AddressRange,
        ))

    source_instance = managedattribute(
        name='source_instance',
        default=None,
        type=(None, managedattribute.test_istype(int)))

    source_count = managedattribute(
        name='source_count',
        type=managedattribute.test_istype(int))

    @source_count.defaulter
    def source_count(self):
        source_instance = self.source_instance
        if source_instance is not None:
            return 1
        source = self.source
        if isinstance(source, Interface):
            return 1  # TODO source.count
        elif isinstance(source, Range):
            return len(source)
        else:
            return 1

    destination = managedattribute(
        name='destination',
        type=(
            IPv4Address,
            IPv6Address,
            MAC,
            managedattribute.test_isinstance((
                Interface,
                IPv4AddressRange,
                IPv6AddressRange,
                MACRange,
                MulticastGroup,
            )),
            _IPv4InterfaceRange_to_IPv4AddressRange,
            _IPv6InterfaceRange_to_IPv6AddressRange,
        ))

    @destination.defaulter
    def destination(self):
        source = self.source
        if isinstance(source, TunnelInterface):
            # TODO source_instance
            return source.destination
        raise AttributeError

    destination_instance = managedattribute(
        name='destination_instance',
        default=None,
        type=(None, managedattribute.test_istype(int)))

    destination_count = managedattribute(
        name='destination_count',
        type=managedattribute.test_istype(int))

    @destination_count.defaulter
    def destination_count(self):
        destination_instance = self.destination_instance
        if destination_instance is not None:
            return 1
        destination = self.destination
        if isinstance(destination, Interface):
            return 1  # TODO destination.count
        elif isinstance(destination, Range):
            return len(destination)
        elif isinstance(destination, MulticastGroup):
            return destination.count  # TODO
        else:
            return 1

    # Layer 2

    class Layer2Protocol(enum.Enum):
        ethernet_ii = 'ethernet_ii'
        atm = 'atm'
        hdlc = 'hdlc'
        ppp = 'ppp'
        fr = 'fr'

    layer2_protocol = managedattribute(
        name='layer2_protocol',
        read_only=True)

    @layer2_protocol.getter
    def layer2_protocol(self):
        source_tgen_interface = self.source_tgen_interface
        for interface in itertools.chain([source_tgen_interface], source_tgen_interface.layer2_peer_interfaces):
            if isinstance(interface, EthernetInterface):
                return Stream.Layer2Protocol.ethernet_ii
            elif isinstance(interface, AtmInterface):
                return Stream.Layer2Protocol.atm
            elif isinstance(interface, PosInterface):
                if interface.encap == 'hdlc':
                    return Stream.Layer2Protocol.hdlc
                elif interface.encap == 'ppp':
                    return Stream.Layer2Protocol.ppp
                # TODO Stream.Layer2Protocol.fr
        raise AttributeError

    source_mac_address = managedattribute(
        name='source_mac_address',
        type=(
            MAC,
            managedattribute.test_isinstance((
                MACRange))))

    @source_mac_address.defaulter
    def source_mac_address(self):
        source = self.source
        source_instance = self.source_instance
        if isinstance(source, Interface):
            source_mac_address = getattr(source, 'effective_mac_address', None)
            if source_mac_address is not None:
                return source_mac_address
        source_mac_address = getattr(self.source_tgen_interface, 'effective_mac_address', None)
        if source_mac_address is not None:
            return source_mac_address
        return None

    source_mac_address_count = managedattribute(
        name='source_mac_address_count',
        type=managedattribute.test_istype(int))

    @source_mac_address_count.defaulter
    def source_mac_address_count(self):
        source_mac_address = self.source_mac_address
        if source_mac_address is None:
            return 0
        elif isinstance(source_mac_address, Range):
            # TODO source_instance
            return len(source_mac_address)
        else:
            return self.source_count

    source_mac_address_step = managedattribute(
        name='source_mac_address_step',
        read_only=True)

    @source_mac_address_step.getter
    def source_mac_address_step(self):
        if self.source_mac_address_count >= 1:
            source_mac_address = self.source_mac_address
            if isinstance(source_mac_address, Range):
                return source_mac_address.step
            else:
                return 1
        else:
            return None

    @property
    def source_mac_address_range(self):
        '''Representation of source_mac_address/count/step as a MACRange object.'''
        start = self.source_mac_address
        if start is None:
            return MACRange(0)
        elif isinstance(start, Range):
            start = start.start
        start = int(start)
        step = self.source_mac_address_step
        count = self.source_mac_address_count
        return MACRange(start, start + step * count, step)

    destination_mac_address = managedattribute(
        name='destination_mac_address',
        type=(
            managedattribute.test_in((
                'discovery',
            )),
            MAC,
            managedattribute.test_isinstance((
                MACRange))))

    @destination_mac_address.defaulter
    def destination_mac_address(self):
        layer2_protocol = self.layer2_protocol
        if layer2_protocol is Stream.Layer2Protocol.ethernet_ii:
            destination = self.destination
            destination_instance = self.destination_instance
            if isinstance(destination, (MAC, MACRange)):
                # TODO destination_instance
                return destination
            elif isinstance(destination, MulticastGroup):
                IpUtils.ip_to_mac(self.destination_ip)
            else:
                source_tgen_interface = self.source_tgen_interface
                layer2_peer_interfaces = source_tgen_interface.layer2_peer_interfaces
                if layer2_peer_interfaces:
                    if destination in layer2_peer_interfaces:
                        if getattr(destination, 'effective_mac_address', None):
                            return destination.effective_mac_address
                else:
                    # TODO use self.mac_discovery_gateway?
                    gateway_interface = source_tgen_interface.gateway_interface
                    if getattr(gateway_interface, 'effective_mac_address', None):
                        return gateway_interface.effective_mac_address
                if self.mpls_labels:
                    return 'discovery'
                else:
                    return MAC('ffff.ffff.ffff')  # Broadcast
        else:
            return None

    destination_mac_address_count = managedattribute(
        name='destination_mac_address_count',
        type=managedattribute.test_istype(int))

    @destination_mac_address_count.defaulter
    def destination_mac_address_count(self):
        destination_mac_address = self.destination_mac_address
        if destination_mac_address is None:
            return 0
        elif isinstance(destination_mac_address, Range):
            # TODO destination_instance
            return len(destination_mac_address)
        else:
            destination = self.destination
            if isinstance(destination, MulticastGroup):
                return destination.count
            else:
                return self.destination_count

    destination_mac_address_step = managedattribute(
        name='destination_mac_address_step',
        read_only=True)

    @destination_mac_address_step.getter
    def destination_mac_address_step(self):
        if self.destination_mac_address_count >= 1:
            destination_mac_address = self.destination_mac_address
            if isinstance(destination_mac_address, Range):
                return destination_mac_address.step
            else:
                return 1
        else:
            return None

    @property
    def destination_mac_address_range(self):
        '''Representation of destination_mac_address/count/step as a MACRange object.'''
        start = self.destination_mac_address
        if start == 'discovery':
            return 'discovery'
        elif start is None:
            return MACRange(0)
        elif isinstance(start, Range):
            start = start.start
        start = int(start)
        step = self.destination_mac_address_step
        count = self.destination_mac_address_count
        return MACRange(start, start + step * count, step)

    @property
    def resolved_mac_addresses(self):
        return self.device.get_stream_resolved_mac_addresses(self)

    mac_discovery_gateway = managedattribute(
        name='mac_discovery_gateway',
        type=(
            None,
            IPv4Address,
            IPv6Address,
            managedattribute.test_isinstance((
                IPv4AddressRange,
                IPv6AddressRange,
            )),
            _IPv4InterfaceRange_to_IPv4AddressRange,
            _IPv6InterfaceRange_to_IPv6AddressRange,
        ))

    @mac_discovery_gateway.defaulter
    def mac_discovery_gateway(self):
        destination_mac_address = self.destination_mac_address
        if destination_mac_address != 'discovery':
            return None
        layer2_protocol = self.layer2_protocol
        if layer2_protocol is not Stream.Layer2Protocol.ethernet_ii:
            return None
        layer3_protocol = self.layer3_protocol
        if layer3_protocol is Stream.Layer3Protocol.ipv4:
            ip_attr = 'ipv4'
        elif layer3_protocol is Stream.Layer3Protocol.ipv6:
            ip_attr = 'ipv6'
        else:
            raise ValueError('mac_discovery_gateway: Unexpected layer3_protocol {}'.format(layer3_protocol))
        gateway_interface = self.source_tgen_interface.gateway_interface
        if gateway_interface:  # TODO support multiple gateway_interface(s)
            try:
                return getattr(gateway_interface, ip_attr).ip
            except AttributeError:
                pass
        source = self.source
        if isinstance(source, Interface):
            peer_interfaces = set([
                interface
                for link in source.links
                for interface in link.interfaces
                if interface is not source and
                interface.obj_state == 'active'])
            if len(peer_interfaces) == 1:
                try:
                    return getattr(tuple(peer_interfaces)[0], ip_attr).ip
                except AttributeError:
                    pass
        if isinstance(source, Interface):
            ip_value = getattr(source, ip_attr)
            if ip_value:
                return ip_value.network.broadcast_address
        return None

    mac_discovery_gateway_count = managedattribute(
        name='mac_discovery_gateway_count',
        type=managedattribute.test_istype(int))

    @mac_discovery_gateway_count.defaulter
    def mac_discovery_gateway_count(self):
        mac_discovery_gateway = self.mac_discovery_gateway
        if mac_discovery_gateway is None:
            return 0
        elif isinstance(mac_discovery_gateway, Range):
            # TODO source_instance/destination_instance
            return len(mac_discovery_gateway)
        else:
            return 1

    mac_discovery_gateway_step = managedattribute(
        name='mac_discovery_gateway_step',
        read_only=True)

    @mac_discovery_gateway_step.getter
    def mac_discovery_gateway_step(self):
        if self.mac_discovery_gateway_count >= 1:
            mac_discovery_gateway = self.mac_discovery_gateway
            if isinstance(mac_discovery_gateway, Range):
                return mac_discovery_gateway.step
            else:
                return 1
        else:
            return None

    @property
    def mac_discovery_gateway_range(self):
        '''Representation of mac_discovery_gateway/count/step as a IPv4AddressRange/IPv6AddressRange object.'''
        ip_version = self.ip_version
        if ip_version is None:
            return IPv4AddressRange(0)
        elif ip_version == 4:
            range_type = IPv4AddressRange
            addr_type = IPv4Address
        elif ip_version == 6:
            range_type = IPv6AddressRange
            addr_type = IPv6Address
        else:
            raise ValueError('mac_discovery_gateway_range: Unexpected ip_version {}'.format(ip_version))
        start = self.mac_discovery_gateway
        if start is None:
            return range_type(0)
        elif isinstance(start, addr_type):
            pass
        elif isinstance(start, range_type):
            start = start.start
        else:
            raise ValueError('mac_discovery_gateway_range: Unexpected mac_discovery_gateway {!r}'.format(self.mac_discovery_gateway))
        start = int(start)
        step = self.mac_discovery_gateway_step
        count = self.mac_discovery_gateway_count
        return range_type(start, start + step * count, step)

    eth_encap_val1 = managedattribute(
        name='eth_encap_val1',
        type=(None, managedattribute.test_istype(int)))

    @eth_encap_val1.defaulter
    def eth_encap_val1(self):
        source = self.source
        if isinstance(source, Interface):
            source_instance = self.source_instance
            # TODO source_instance
            return getattr(source, 'eth_encap_val1', None)
        else:
            return None

    eth_encap_count1 = managedattribute(
        name='eth_encap_count1',
        type=managedattribute.test_istype(int))

    @eth_encap_count1.defaulter
    def eth_encap_count1(self):
        if self.eth_encap_val1 is None:
            return 0
        else:
            # int
            return self.source_count

    eth_encap_step1 = managedattribute(
        name='eth_encap_step1',
        type=managedattribute.test_istype(int))

    @eth_encap_step1.defaulter
    def eth_encap_step1(self):
        # TODO
        if self.eth_encap_val1 is None \
                or self.eth_encap_count1 < 1:
            return None
        return 1

    @property
    def eth_encap_range1(self):
        '''Representation of eth_encap_val1/count1/step1 as a range object.'''
        start = self.eth_encap_val1
        if start is None:
            return range(0)
        step = self.eth_encap_step1
        count = self.eth_encap_count1
        return range(start, start + step * count, step)

    @eth_encap_range1.setter
    def eth_encap_range1(self, value):
        if value is None:
            value = range(0)
        if type(value) is range:
            if value:
                self.eth_encap_val1 = value.start
                self.eth_encap_count1 = len(value)
                self.eth_encap_step1 = value.step
            else:
                self.eth_encap_val1 = None
                try:
                    del self.eth_encap_count1
                except AttributeError:
                    pass
                try:
                    del self.eth_encap_step1
                except AttributeError:
                    pass
        else:
            raise TypeError(value)

    @eth_encap_range1.deleter
    def eth_encap_range1(self):
        try:
            del self.eth_encap_val1
        except AttributeError:
            pass
        try:
            del self.eth_encap_count1
        except AttributeError:
            pass
        try:
            del self.eth_encap_step1
        except AttributeError:
            pass

    eth_encap_val2 = managedattribute(
        name='eth_encap_val2',
        type=(None, managedattribute.test_istype(int)))

    @eth_encap_val2.defaulter
    def eth_encap_val2(self):
        source = self.source
        if isinstance(source, Interface):
            source_instance = self.source_instance
            # TODO source_instance
            return getattr(source, 'eth_encap_val2', None)
        else:
            return None

    eth_encap_count2 = managedattribute(
        name='eth_encap_count2',
        type=managedattribute.test_istype(int))

    @eth_encap_count2.defaulter
    def eth_encap_count2(self):
        if self.eth_encap_val2 is None:
            return 0
        else:
            # int
            return self.source_count

    eth_encap_step2 = managedattribute(
        name='eth_encap_step2',
        type=managedattribute.test_istype(int))

    @eth_encap_step2.defaulter
    def eth_encap_step2(self):
        # TODO
        if self.eth_encap_val2 is None \
                or self.eth_encap_count2 < 1:
            return None
        return 1

    @property
    def eth_encap_range2(self):
        '''Representation of eth_encap_val2/count2/step2 as a range object.'''
        start = self.eth_encap_val2
        if start is None:
            return range(0)
        step = self.eth_encap_step2
        count = self.eth_encap_count2
        return range(start, start + step * count, step)

    @eth_encap_range2.setter
    def eth_encap_range2(self, value):
        if value is None:
            value = range(0)
        if type(value) is range:
            if value:
                self.eth_encap_val2 = value.start
                self.eth_encap_count2 = len(value)
                self.eth_encap_step2 = value.step
            else:
                self.eth_encap_val2 = None
                try:
                    del self.eth_encap_count2
                except AttributeError:
                    pass
                try:
                    del self.eth_encap_step2
                except AttributeError:
                    pass
        else:
            raise TypeError(value)

    @eth_encap_range2.deleter
    def eth_encap_range2(self):
        try:
            del self.eth_encap_val2
        except AttributeError:
            pass
        try:
            del self.eth_encap_count2
        except AttributeError:
            pass
        try:
            del self.eth_encap_step2
        except AttributeError:
            pass

    # MPLS

    mpls_labels = managedattribute(
        name='mpls_labels',
        default=(),
        type=managedattribute.test_tuple_of(
            managedattribute.test_istype(int)))

    # Layer 3

    class Layer3Protocol(enum.Enum):
        ipv4 = 'ipv4'
        ipv6 = 'ipv6'
        arp = 'arp'
        pause_control = 'pause_control'
        ipx = 'ipx'
        raw_ipv4_socket = 'raw_ipv4_socket'

    layer3_protocol = managedattribute(
        name='layer3_protocol',
        type=(None, Layer3Protocol))

    @layer3_protocol.defaulter
    def layer3_protocol(self):
        ip_version = self.ip_version
        if ip_version is None:
            return None
        elif ip_version == 4:
            return Stream.Layer3Protocol.ipv4
        elif ip_version == 6:
            return Stream.Layer3Protocol.ipv6
        else:
            raise ValueError('layer3_protocol: Unexpected ip_version {}'.format(ip_version))

    # ARP

    class ArpOperation(enum.Enum):
        arpRequest = 'arpRequest'
        arpReply = 'arpReply'
        rarpRequest = 'rarpRequest'
        rarpReply = 'rarpReply'

    arp_operation = managedattribute(
        name='arp_operation',
        type=(None, ArpOperation))

    @arp_operation.defaulter
    def arp_operation(self):
        layer3_protocol = self.layer3_protocol
        if layer3_protocol is Stream.Layer3Protocol.arp:
            return Stream.ArpOperation.arpRequest
        return None

    arp_source_mac_address = managedattribute(
        name='arp_source_mac_address',
        type=(
            MAC,
            managedattribute.test_isinstance((
                MACRange))))

    @arp_source_mac_address.defaulter
    def arp_source_mac_address(self):
        layer3_protocol = self.layer3_protocol
        if layer3_protocol is Stream.Layer3Protocol.arp:
            return self.source_mac_address
        return None

    arp_source_mac_address_count = managedattribute(
        name='arp_source_mac_address_count',
        type=managedattribute.test_istype(int))

    @arp_source_mac_address_count.defaulter
    def arp_source_mac_address_count(self):
        arp_source_mac_address = self.arp_source_mac_address
        if arp_source_mac_address is None:
            return 0
        elif isinstance(arp_source_mac_address, Range):
            return len(arp_source_mac_address)
        else:
            return 1

    arp_source_mac_address_step = managedattribute(
        name='arp_source_mac_address_step',
        read_only=True)

    @arp_source_mac_address_step.getter
    def arp_source_mac_address_step(self):
        if self.arp_source_mac_address_count >= 1:
            arp_source_mac_address = self.arp_source_mac_address
            if isinstance(arp_source_mac_address, Range):
                return arp_source_mac_address.step
            else:
                return 1
        else:
            return None

    @property
    def arp_source_mac_address_range(self):
        '''Representation of arp_source_mac_address/count/step as a MACRange object.'''
        start = self.arp_source_mac_address
        if start is None:
            return MACRange(0)
        elif isinstance(start, Range):
            start = start.start
        start = int(start)
        step = self.arp_source_mac_address_step
        count = self.arp_source_mac_address_count
        return MACRange(start, start + step * count, step)

    arp_destination_mac_address = managedattribute(
        name='arp_destination_mac_address',
        type=(
            MAC,
            managedattribute.test_isinstance((
                MACRange))))

    @arp_destination_mac_address.defaulter
    def arp_destination_mac_address(self):
        layer3_protocol = self.layer3_protocol
        if layer3_protocol is Stream.Layer3Protocol.arp:
            arp_operation = self.arp_operation
            if arp_operation is Stream.ArpOperation.arpRequest:
                return MAC(0)
            elif arp_operation is Stream.ArpOperation.arpReply:
                return self.destination_mac_address
            else:
                return NotImplementedError(arp_operation)
        return None

    arp_destination_mac_address_count = managedattribute(
        name='arp_destination_mac_address_count',
        type=managedattribute.test_istype(int))

    @arp_destination_mac_address_count.defaulter
    def arp_destination_mac_address_count(self):
        arp_destination_mac_address = self.arp_destination_mac_address
        if arp_destination_mac_address is None:
            return 0
        elif isinstance(arp_destination_mac_address, Range):
            return len(arp_destination_mac_address)
        else:
            return 1

    arp_destination_mac_address_step = managedattribute(
        name='arp_destination_mac_address_step',
        read_only=True)

    @arp_destination_mac_address_step.getter
    def arp_destination_mac_address_step(self):
        if self.arp_destination_mac_address_count >= 1:
            arp_destination_mac_address = self.arp_destination_mac_address
            if isinstance(arp_destination_mac_address, Range):
                return arp_destination_mac_address.step
            else:
                return 1
        else:
            return None

    @property
    def arp_destination_mac_address_range(self):
        '''Representation of arp_destination_mac_address/count/step as a MACRange object.'''
        start = self.arp_destination_mac_address
        if start is None:
            return MACRange(0)
        elif isinstance(start, Range):
            start = start.start
        start = int(start)
        step = self.arp_destination_mac_address_step
        count = self.arp_destination_mac_address_count
        return MACRange(start, start + step * count, step)

    # IP

    ip_version = managedattribute(
        name='ip_version',
        type=(None, managedattribute.test_in((
            4,
            6,
        ))))

    @ip_version.defaulter
    def ip_version(self):
        try:
            layer3_protocol = self._layer3_protocol  # Avoid recursion
        except AttributeError:
            pass
        else:
            if layer3_protocol in (Stream.Layer3Protocol.ipv4, Stream.Layer3Protocol.arp):
                return 4
            elif layer3_protocol is Stream.Layer3Protocol.ipv6:
                return 6
            else:
                return None
        try:
            source_ip = self._source_ip  # Avoid recursion
        except AttributeError:
            pass
        else:
            if source_ip is None:
                return None
            elif isinstance(source_ip, (IPv4Address, IPv4AddressRange)):
                return 4
            elif isinstance(source_ip, (IPv6Address, IPv6AddressRange)):
                return 6
            else:
                raise ValueError('ip_version: Unexpected source_ip {}'.format(source_ip))
        source = self.source
        if isinstance(source, Interface):
            try:
                destination_ip = self._destination_ip  # Avoid recursion
            except AttributeError:
                pass
            else:
                if isinstance(destination_ip, (IPv4Address, IPv4AddressRange)):
                    return 4
                elif isinstance(destination_ip, (IPv6Address, IPv6AddressRange)):
                    return 6
                else:
                    raise ValueError('ip_version: Unexpected destination_ip {}'.format(destination_ip))
            destination = self.destination
            if isinstance(destination, Interface):
                # interface -> interface ... default based on available source IPs
                if source.ipv4 and destination.ipv4:
                    return 4
                elif destination.ipv4 and destination.ipv6:
                    return 6
                else:
                    return None  # TODO
            elif isinstance(destination, (IPv4Address, IPv4AddressRange)):
                return 4
            elif isinstance(destination, (IPv6Address, IPv6AddressRange)):
                return 6
            elif isinstance(destination, MulticastGroup):
                mcast_group_id = destination.group_id
                if isinstance(mcast_group_id, IPv4Address):
                    return 4
                elif isinstance(mcast_group_id, IPv6Address):
                    return 6
                else:
                    raise ValueError('ip_version: Unexpected mcast_group_id {}'.format(mcast_group_id))
            else:
                # TODO -- default based on available source IPs
                raise ValueError('ip_version: Unexpected destination {}'.format(destination))
        elif isinstance(source, (IPv4Address, IPv4AddressRange)):
            return 4
        elif isinstance(source, (IPv6Address, IPv6AddressRange)):
            return 6
        else:
            raise ValueError('ip_version: Unexpected source {}'.format(source))

    source_ip = managedattribute(
        name='source_ip',
        type=(
            None,
            IPv4Address,
            IPv6Address,
            managedattribute.test_isinstance((
                IPv4AddressRange,
                IPv6AddressRange,
            )),
            _IPv4InterfaceRange_to_IPv4AddressRange,
            _IPv6InterfaceRange_to_IPv6AddressRange,
        ))

    @source_ip.defaulter
    def source_ip(self):
        source = self.source
        if isinstance(source, (
                IPv4Address,
                IPv6Address,
                IPv4AddressRange,
                IPv6AddressRange,
        )):
            return source
        elif isinstance(source, (
            MAC,
            MACRange,
        )):
            return None
        elif isinstance(source, Interface):
            source_instance = self.source_instance
            ip_version = self.ip_version
            if ip_version is None:
                return None
            elif ip_version == 4:
                # TODO source_instance
                return source.ipv4.ip
            elif ip_version == 6:
                # TODO source_instance
                return source.ipv6.ip
            else:
                raise ValueError('source_ip: Unexpected ip_version {}'.format(ip_version))
        else:
            # TODO
            raise ValueError('source_ip: Unexpected source {}'.format(source))

    source_ip_count = managedattribute(
        name='source_ip_count',
        type=managedattribute.test_istype(int))

    @source_ip_count.defaulter
    def source_ip_count(self):
        source_ip = self.source_ip
        if source_ip is None:
            return 0
        elif isinstance(source_ip, Range):
            # TODO source_instance
            return len(source_ip)
        else:
            return self.source_count

    source_ip_step = managedattribute(
        name='source_ip_step',
        read_only=True)

    @source_ip_step.getter
    def source_ip_step(self):
        if self.source_ip_count >= 1:
            source_ip = self.source_ip
            if isinstance(source_ip, Range):
                return source_ip.step
            else:
                return 1
        else:
            return None

    @property
    def source_ip_range(self):
        '''Representation of source_ip/count/step as a IPv4AddressRange/IPv6AddressRange object.'''
        ip_version = self.ip_version
        if ip_version is None:
            return IPv4AddressRange(0)
        elif ip_version == 4:
            range_type = IPv4AddressRange
            addr_type = IPv4Address
        elif ip_version == 6:
            range_type = IPv6AddressRange
            addr_type = IPv6Address
        else:
            raise ValueError('source_ip_range: Unexpected ip_version {}'.format(ip_version))
        start = self.source_ip
        if start is None:
            return range_type(0)
        elif isinstance(start, addr_type):
            pass
        elif isinstance(start, range_type):
            start = start.start
        else:
            raise ValueError('source_ip_range: Unexpected source_ip {!r}'.format(self.source_ip))
        start = int(start)
        step = self.source_ip_step
        count = self.source_ip_count
        return range_type(start, start + step * count, step)

    destination_ip = managedattribute(
        name='destination_ip',
        type=(
            None,
            IPv4Address,
            IPv6Address,
            managedattribute.test_isinstance((
                IPv4AddressRange,
                IPv6AddressRange,
            )),
            _IPv4InterfaceRange_to_IPv4AddressRange,
            _IPv6InterfaceRange_to_IPv6AddressRange,
        ))

    @destination_ip.defaulter
    def destination_ip(self):
        destination = self.destination
        if isinstance(destination, (
            IPv4Address,
            IPv6Address,
            IPv4AddressRange,
            IPv6AddressRange,
        )):
            return destination
        elif isinstance(destination, (
            MAC,
            MACRange,
        )):
            return None
        elif isinstance(destination, Interface):
            ip_version = self.ip_version
            if ip_version is None:
                return None
            elif ip_version == 4:
                return destination.ipv4.ip
            elif ip_version == 6:
                return destination.ipv6.ip
            else:
                raise ValueError('destination_ip: Unexpected ip_version {}'.format(ip_version))
        elif isinstance(destination, MulticastGroup):
            return destination.group_id
        else:
            # TODO
            raise ValueError('destination_ip: Unexpected destination {}'.format(destination))

    destination_ip_count = managedattribute(
        name='destination_ip_count',
        type=managedattribute.test_istype(int))

    @destination_ip_count.defaulter
    def destination_ip_count(self):
        destination_ip = self.destination_ip
        if destination_ip is None:
            return 0
        elif isinstance(destination_ip, Range):
            # TODO source_instance/destination_instance
            return len(destination_ip)
        else:
            return 1

    destination_ip_step = managedattribute(
        name='destination_ip_step',
        read_only=True)

    @destination_ip_step.getter
    def destination_ip_step(self):
        if self.destination_ip_count >= 1:
            destination_ip = self.destination_ip
            if isinstance(destination_ip, Range):
                return destination_ip.step
            else:
                return 1
        else:
            return None

    @property
    def destination_ip_range(self):
        '''Representation of destination_ip/count/step as a IPv4AddressRange/IPv6AddressRange object.'''
        ip_version = self.ip_version
        if ip_version is None:
            return IPv4AddressRange(0)
        elif ip_version == 4:
            range_type = IPv4AddressRange
            addr_type = IPv4Address
        elif ip_version == 6:
            range_type = IPv6AddressRange
            addr_type = IPv6Address
        else:
            raise ValueError('destination_ip_range: Unexpected ip_version {}'.format(ip_version))
        start = self.destination_ip
        if start is None:
            return range_type(0)
        elif isinstance(start, addr_type):
            pass
        elif isinstance(start, range_type):
            start = start.start
        else:
            raise ValueError('destination_ip_range: Unexpected destination_ip {!r}'.format(self.destination_ip))
        start = int(start)
        step = self.destination_ip_step
        count = self.destination_ip_count
        return range_type(start, start + step * count, step)

    # Layer 4

    class Layer4Protocol(enum.Enum):
        # HLTAPI:  icmp igmp tcp udp rip dhcp ospf rtp
        # Agilent: igmp icmp tcp tcp_v6 udp udp_v6 rip dhcp ospf rsvp rtp isis icmp_v6 pim ldp gre none
        # Spirent: tcp udp icmp icmpv6 igmp rtp isis ospf
        # Ixia:    icmp igmp ggp gre ip st tcp ucl egp igp bbn_rcc_mon nvp_ii pup argus emcon xnet chaos udp mux dcn_meas hmp prm xns_idp trunk_1 trunk_2 leaf_1 leaf_2 rdp irtp iso_tp4 netblt mfe_nsp merit_inp sep cftp sat_expak mit_subnet rvd ippc sat_mon ipcv br_sat_mon wb_mon wb_expak rip ospf [0-255]
        tcp = 'tcp'
        udp = 'udp'
        icmp = 'icmp'

    layer4_protocol = managedattribute(
        name='layer4_protocol',
        default=None,
        type=(None, Layer4Protocol))

    # Other

    class SubStreamIncrement(enum.Enum):
        any = 'any'
        source_mac_address = 'source_mac_address'
        destination_mac_address = 'destination_mac_address'
        eth_encap_val1 = 'eth_encap_val1'

    sub_stream_increments = managedattribute(
        name='sub_stream_increments',
        finit=typedset(SubStreamIncrement).copy,
        type=typedset(SubStreamIncrement)._from_iterable)

    # TODO expected_path = None  # list(Lsp)

    # TODO track_by = None

    obj_state = managedattribute(
        name='obj_state',
        default='active',
        type=managedattribute.test_in((
            'active',
            'inactive',
        )))

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.device.streams.add(self)

    def __eq__(self, other):
        if not isinstance(other, Stream):
            return NotImplemented
        # Multiple streams with all the same attributes are still not equal!
        return self is other

    def __lt__(self, other):
        if not isinstance(other, Stream):
            return NotImplemented
        for attr in (
                'source_tgen_interface',
                'name',
                'source_mac_address_range.start',
                'eth_encap_range1.start',
                'eth_encap_range2.start',
                #'layer3_protocol',
                'source_ip_range.start.version',
                'source_ip_range.start',
                'destination_mac_address_range.start',
                'destination_ip_range.start.version',
                'destination_ip_range.start',
                #'layer4_protocol',
        ):
            getter = operator.attrgetter(attr)
            v1 = getter(self)
            v2 = getter(other)
            if v1 < v2:
                return True
            if v1 != v2:
                return False
        return False

    def __hash__(self):
        return hash(id(self))

    def build_config(self, apply=True, attributes=None, unconfig=False, **kwargs):
        assert not kwargs, kwargs
        attributes = AttributesHelper(self, attributes)

        source_tgen_interface = self.source_tgen_interface
        device = self.device
        hltapi = device.hltapi
        tcl = hltapi.tcl

        from genie.libs.conf.device.spirent import Device as SpirentDevice
        from genie.libs.conf.device.ixia import Device as IxiaDevice
        #from genie.libs.conf.device.agilent import Device as AgilentDevice
        from genie.libs.conf.device.pagent import Device as PagentDevice

        bNeedStcApply = False
        try:

            if unconfig:
                stream_ids = self.tgen_handle
                if not stream_ids:
                    logger.info('Nothing to do for %r (no tgen-handle)', self)
                else:
                    stc_streamblocks = []
                    hlt_stream_ids = []
                    for stream_id in stream_ids:
                        if stream_id.startswith('streamblock'):
                            stc_streamblocks.append(stream_id)
                        else:
                            hlt_stream_ids.append(stream_id)
                        for streamblock in stc_streamblocks:
                            # Delete Spirent internal streamblock object
                            hltapi.stc_delete(streamblock)
                            bNeedStcApply = True
                        for stream_id in hlt_stream_ids:
                            hltkwargs = {}
                            hltkwargs['mode'] = 'remove'
                            hltkwargs['stream_id'] = stream_id
                            hltkwargs['port_handle'] = source_tgen_interface.tgen_port_handle
                            hltkl = hltapi.traffic_config(**hltkwargs)
                    self.tgen_handle = None

                    # Fix bug in Pagent HLTAPI which removes signature filters on
                    # ports. These will be recreated on next interface_config.
                    if isinstance(device, PagentDevice):
                        tcl.eval(
                            'unset -nocomplain' \
                            ' ::Pagent::_Tgn_Info({},filters)' \
                            .format(source_tgen_interface.tgen_port_handle))

            else:

                #set vRtrIntf [enaTbGetInterfacePeer $vTgnIntf -all]
                source = self.source

                # TODO
                ## One-time Vendor-specific setup {{{
                #switch -exact -- $tgen_platform {
                #    "spirent" {
                #        set tgen [enaTbGetInterfaceParam $vTgnIntf -router]
                #        variable data
                #        # Subscribe to GeneratorPortResults {{{
                #        if { ![info exists data(persist,rtr,$tgen,stc_GeneratorPortResults_resultdataset)] } {
                #            set project [stc::get system1 -children-Project]
                #            set data(persist,rtr,$tgen,stc_GeneratorPortResults_resultdataset) \
                #                [set resultdataset [stc::subscribe -Parent $project -ConfigType Generator -ResultType GeneratorPortResults]]
                #            stc::config $resultdataset -Name "enaTbTopoUtils GeneratorPortResults" -DisablePaging true
                #        }
                #        # }}}
                #        if { $data(persist,use_stc_streamblock_stats) } {
                #            # Subscribe to TxStreamBlockResults {{{
                #            if { ![info exists data(persist,rtr,$tgen,stc_TxStreamBlockResults_resultdataset)] } {
                #                set project [stc::get system1 -children-Project]
                #                set data(persist,rtr,$tgen,stc_TxStreamBlockResults_resultdataset) \
                #                    [set resultdataset [stc::subscribe -Parent $project -ConfigType StreamBlock -ResultType TxStreamBlockResults]]
                #                stc::config $resultdataset -Name "enaTbTopoUtils TxStreamBlockResults" -DisablePaging false -RecordsPerPage 256
                #            }
                #            # }}}
                #            # Subscribe to RxStreamBlockResults {{{
                #            if { ![info exists data(persist,rtr,$tgen,stc_RxStreamBlockResults_resultdataset)] } {
                #                set project [stc::get system1 -children-Project]
                #                set data(persist,rtr,$tgen,stc_RxStreamBlockResults_resultdataset) \
                #                    [set resultdataset [stc::subscribe -Parent $project -ConfigType StreamBlock -ResultType RxStreamBlockResults]]
                #                stc::config $resultdataset -Name "enaTbTopoUtils RxStreamBlockResults" -DisablePaging false -RecordsPerPage 256
                #            }
                #            # }}}
                #        } else {
                #        }
                #    }
                #}
                ## }}}

                if isinstance(source, TunnelInterface):
                    raise NotImplementedError(source)
                    ## Tunnel Stream (Vendor-specific) {{{
                    ## HLTAPI does not support creating dynamic streams for tunnels... use low-level calls
                    #switch -exact -- $tgen_platform {
                    #    "spirent" {
                    #        if { [llength [enaTbGetStreamParam $vStream -sub-stream-increments]] } {
                    #            error TODO-sub-stream-increments
                    #        }
                    #        # Create Stream {{{
                    #        if { [set streamblock [enaTbGetStreamParam $vStream -tgen-handle]] eq "" } {
                    #            set stccmd [list ::stc::create StreamBlock]
                    #            if { [enaObjIsObject $vSrc] } {
                    #                lappend stccmd -under [enaTbGetInterfaceParam $vSrc -tgen-port-handle]
                    #            } else {
                    #                lappend stccmd -under [::stc::get system1 -children-Project]
                    #            }
                    #            aetest::log -debug "stccmd: [list $stccmd]"
                    #            enaVerify "STC stream block creation" {set streamblock [eval $stccmd] ; OK} [OK] -format ena_return_code -eval true -ret-code continue
                    #            aetest::log -debug "streamblock: $streamblock"
                    #            set bNeedStcApply true
                    #            enaTbSetStream $vStream -tgen-handle $streamblock
                    #        }
                    #        # }}}
                    #        # Configure Stream {{{
                    #        set post_stream_config_bodies {}
                    #        set stccmd [list ::stc::config $streamblock]
                    #        lappend stccmd -Name [enaTbFormatStream $vStream]
                    #        lappend stccmd -InsertSig true
                    #        lappend stccmd -FrameConfig {}
                    #        lappend stccmd -EnableStreamOnlyGeneration false
                    #        set l2_encap ""
                    #        if { [set vlan [enaTbGetStreamParam $vStream -eth-encap-val1]] ne "" } {
                    #            error TODO-eth-encap-val1
                    #        }
                    #        lappend stccmd -FrameLengthMode FIXED
                    #        switch -exact -- [enaTbGetStreamParam $vStream -frame-length-mode] {
                    #            l2 {
                    #                # Spirent HLTAPI does not support l2_length
                    #                switch -exact -- $l2_encap {
                    #                    "ethernet_ii_vlan" {
                    #                        # L2 = ETH(14) VLAN(4) MPLS(4) L3 [includes FCS(4)]
                    #                        lappend stccmd -FixedFrameLength [expr { [enaTbGetStreamParam $vStream -frame-length] - 14 - 4 - 4 }]
                    #                    }
                    #                    "ethernet_ii" -
                    #                    default {
                    #                        # TODO
                    #                        # L2 = ETH(14) MPLS(4) L3 [includes FCS(4)]
                    #                        lappend stccmd -FixedFrameLength [expr { [enaTbGetStreamParam $vStream -frame-length] - 14 - 4 }]
                    #                    }
                    #                }
                    #            }
                    #            l3 {
                    #                lappend stccmd -FixedFrameLength [enaTbGetStreamParam $vStream -frame-length]
                    #            }
                    #            default {
                    #                error TODO-frame-length-mode-[enaTbGetStreamParam $vStream -frame-length-mode]
                    #            }
                    #        }
                    #        lappend stccmd -TrafficPattern PAIR
                    #        set lsrcbindings {}
                    #        if { [enaObjIsObject $vSrc] } {
                    #            if { [enaTbGetInterfaceParam $vSrc -iftype] eq "tunnel" } {
                    #                foreach tunnel_handle [enaTbGetInterfaceParam $vSrc -tgen-handle] {
                    #                    set ipv4networkblock [stc::get $tunnel_handle -children-Ipv4NetworkBlock]
                    #                    lappend lsrcbindings $ipv4networkblock
                    #                }
                    #            } else {
                    #                error TODO-src-INTF-IP
                    #            }
                    #        } else {
                    #            error TODO-src-IP
                    #        }
                    #        set ldstbindings {}
                    #        if {
                    #            [enaTbGetInterfaceParam $vSrc -iftype] eq "tunnel" &&
                    #            ![enaTbGetStreamParam $vStream -destination?] &&
                    #            [llength [enaTbGetInterfaceParam $vSrc -tgen-tail-handle]]
                    #        } {
                    #            foreach tunnel_handle [enaTbGetInterfaceParam $vSrc -tgen-tail-handle] {
                    #                set ipv4networkblock [stc::get $tunnel_handle -children-Ipv4NetworkBlock]
                    #                lappend ldstbindings $ipv4networkblock
                    #            }
                    #        } elseif { [enaObjIsObject $vDest interface] } {
                    #            if { [enaTbGetInterfaceParam $vDest -router -type] eq "tgen" } {
                    #                error TODO-dest-TGEN
                    #            } elseif { [enaTbGetInterfaceParam $vDest -router -type] eq "emulated" } {
                    #                if { [enaTbGetInterfaceParam $vDest -iftype] eq "loopback" } {
                    #                    set vDestEmulIntf [enaTbFindInterface -router [enaTbGetInterfaceParam $vDest -router] -iftype physical]
                    #                    set vDestLink [enaTbFindLink -from $vDestEmulIntf -linktype emulated]
                    #                    set vDestRtng [enaTbGetLinkParam $vDestLink -routing]
                    #                    set loroutehandle [enaRtngGetRoutingParam $vDestRtng -router [enaTbGetInterfaceParam $vDest -router] -tgen-loopback-route-handle]
                    #                    if { [regexp {^isisRouteHandle\d+$} $loroutehandle] } {
                    #                        # IS-IS
                    #                        lassign $::sth::IsIs::ISISROUTEHNDLIST($loroutehandle) \
                    #                            isisLspHandle ipVersion isisIpv4RouteHandle isisIpv6RouteHandle
                    #                        set ipv4networkblock [stc::get $isisIpv4RouteHandle -children-Ipv4NetworkBlock]
                    #                    } elseif { [regexp {^routerlsa\d+$} $loroutehandle] } {
                    #                        # ??? regexp {^ospfRouteHandle\d+$} $loroutehandle
                    #                        # OSPF
                    #                        set routerlsa $loroutehandle
                    #                        set routerlsalink [stc::get $routerlsa -children-RouterLsaLink]
                    #                        set ipv4networkblock [stc::get $routerlsalink -children-Ipv4NetworkBlock]
                    #                    } else {
                    #                        error TODO-dest-INTF-LO-UNKRTNG
                    #                    }
                    #                    lappend ldstbindings $ipv4networkblock
                    #                } else {
                    #                    error TODO-dest-INTF-NONLO
                    #                }
                    #            } else {
                    #                error TODO-dest-INTF-IP
                    #            }
                    #        } elseif { [enaObjIsObject $vDest mcastGroup] } {
                    #            error TODO-dest-MCAST-IP
                    #        } elseif { [enaObjIsObject $vDest addrRange] } {
                    #            set vTunDest [enaTbGetInterfaceParam $vSrc -destination] ;# XXXJST TODO Only 1 destination supported
                    #            set vDestEmulIntf [enaTbFindInterface -router [enaTbGetInterfaceParam $vTunDest -router] -iftype physical]
                    #            set vDestLink [enaTbFindLink -from $vDestEmulIntf -linktype emulated]
                    #            set vDestRtng [enaTbGetLinkParam $vDestLink -routing]
                    #            set loroutehandle [enaRtngGetRoutingParam $vDestRtng -router [enaTbGetInterfaceParam $vTunDest -router] -tgen-loopback-route-handle]
                    #            set loroutertrid [enaRtngGetRoutingParam $vDestRtng -router [enaTbGetInterfaceParam $vTunDest -router] -effective-router-id]
                    #            if { [regexp {^isisRouteHandle\d+$} $loroutehandle] } {
                    #                # IS-IS
                    #                lassign $::sth::IsIs::ISISROUTEHNDLIST($loroutehandle) \
                    #                    isisLspHandle ipVersion isisIpv4RouteHandle isisIpv6RouteHandle
                    #                set ipv4networkblock [stc::get $isisIpv4RouteHandle -children-Ipv4NetworkBlock]
                    #            } elseif { [regexp {^routerlsa\d+$} $loroutehandle] } {
                    #                # ??? regexp {^ospfRouteHandle\d+$} $loroutehandle
                    #                # OSPF
                    #                set routerlsa $loroutehandle
                    #                set routerlsalink [stc::get $routerlsa -children-RouterLsaLink]
                    #                set ipv4networkblock [stc::get $routerlsalink -children-Ipv4NetworkBlock]
                    #            } else {
                    #                error TODO-dest-INTF-LO-UNKRTNG
                    #            }
                    #            lappend ldstbindings $ipv4networkblock
                    #            lappend post_stream_config_bodies {
                    #                if { $bNeedStcApply } {
                    #                    enaVerify "STC apply" {::sth::sthCore::doStcApply ; OK} [OK] -eval true -format ena_return_code -log terse
                    #                    set bNeedStcApply false
                    #                }
                    #                package require AtsCli2Xml
                    #                set root_node [cli2xml::parseXml [stc::get $streamblock -FrameConfig]]
                    #                enaDestructor [list cli2xml::destroyXml $root_node]
                    #                if { [OK] == [enaVerify "number of IPv4 PDU nodes found" {llength [set pdu_node [$root_node selectNodes "/frame/config/pdus/pdu\[@pdu='ipv4:IPv4'\]"]]} 1 -eval true -log false] } {
                    #                    set ipv4_pdu [$pdu_node getAttribute name]
                    #                    set ip_offset [expr {
                    #                            [enaIpAddressToInteger [enaTbGetAddressRangeParam $vDest -first]] -
                    #                            [enaIpAddressToInteger $loroutertrid]
                    #                    }]
                    #                    if { $ip_offset < 0 } { set ip_offset [expr { $ip_offset + 0xFFFFFFFF }] }
                    #                    set stcrngcmd [list stc::create RangeModifier \
                    #                            -under $streamblock \
                    #                            -Mask 255.255.255.255 \
                    #                            -StepValue [enaTbGetAddressRangeParam $vDest -formatted-step] \
                    #                            -RecycleCount [enaTbGetAddressRangeParam $vDest -count] \
                    #                            -Data [enaIntegerToIpAddress $ip_offset] \
                    #                            -OffsetReference $ipv4_pdu.destAddr]
                    #                    # -EnableStream true
                    #                    aetest::log -debug "stcrngcmd: [list $stcrngcmd]"
                    #                    enaVerify "STC destination address range modifier creation" {eval $stcrngcmd ; OK} [OK] -format ena_return_code -eval true
                    #                    set bNeedStcApply true
                    #                }
                    #            }
                    #        } else {
                    #            error TODO-dest-IP
                    #        }
                    #        set lmeshedsrcbindings {}
                    #        set lmesheddstbindings {}
                    #        foreach srcbinding $lsrcbindings {
                    #            foreach dstbinding $ldstbindings {
                    #                lappend lmeshedsrcbindings $srcbinding
                    #                lappend lmesheddstbindings $dstbinding
                    #            }
                    #        }
                    #        lappend stccmd -EndpointMapping ONE_TO_ONE
                    #        lappend stccmd -SrcBinding $lmeshedsrcbindings
                    #        lappend stccmd -DstBinding $lmesheddstbindings
                    #        aetest::log -debug "stccmd: [list $stccmd]"
                    #        enaVerify "STC stream block configuration" {eval $stccmd ; OK} [OK] -format ena_return_code -eval true
                    #        set bNeedStcApply true
                    #        foreach body $post_stream_config_bodies { eval $body }
                    #        # }}}
                    #        # Configure Load Profile {{{
                    #        set loadprofile [stc::get $streamblock -AffiliationStreamBlockLoadProfile]
                    #        set stccmd [list stc::config $loadprofile]
                    #        switch -exact -- [enaTbGetStreamParam $vStream -bandwidth-units] {
                    #            mbps {
                    #                lappend stccmd -Load [enaTbGetStreamParam $vStream -bandwidth] -LoadUnit MEGABITS_PER_SECOND
                    #            }
                    #            kbps {
                    #                lappend stccmd -Load [enaTbGetStreamParam $vStream -bandwidth] -LoadUnit KILOBITS_PER_SECOND
                    #            }
                    #            bps {
                    #                lappend stccmd -Load [enaTbGetStreamParam $vStream -bandwidth] -LoadUnit BITS_PER_SECOND
                    #            }
                    #            pps {
                    #                lappend stccmd -Load [enaTbGetStreamParam $vStream -bandwidth] -LoadUnit FRAMES_PER_SECOND
                    #            }
                    #            percent {
                    #                lappend stccmd -Load [enaTbGetStreamParam $vStream -bandwidth] -LoadUnit PERCENT_LINE_RATE
                    #            }
                    #            default {
                    #                error TODO-bandwidth-units-[enaTbGetStreamParam $vStream -bandwidth-units]
                    #            }
                    #        }
                    #        aetest::log -debug "stccmd: [list $stccmd]"
                    #        enaVerify "STC load profile configuration" {eval $stccmd ; OK} [OK] -format ena_return_code -eval true
                    #        set bNeedStcApply true
                    #        # }}}
                    #    }
                    #    default {
                    #        error "Creating tunnel streams is not implemented for $tgen_platform"
                    #    }
                    #}
                    ## }}}

                else:
                    # HLTAPI
                    hltkwargs = {}

                    if self.tgen_handle:
                        hltkwargs['mode'] = 'modify'
                        hltkwargs['stream_id'] = self.tgen_handle
                    else:
                        hltkwargs['mode'] = 'create'
                    hltkwargs['name'] = self.name  # Not in HLTAPI spec v5.4.1
                    hltkwargs['port_handle'] = source_tgen_interface.tgen_port_handle

                    # Sub-stream Increments
                    sub_stream_increments = self.sub_stream_increments
                    if isinstance(device, SpirentDevice):
                        if Stream.SubStreamIncrement.any in sub_stream_increments:
                            # Use VFDs instead of streams for some modifiers.
                            # This enables a higher level of scaling by reducing
                            # memory consumption and the amount of stream
                            # statistics results required.
                            hltkwargs['enable_stream'] = True
                            hltkwargs['enable_stream_only_gen'] = True
                        else:
                            # Use VFDs instead of streams for some modifiers.
                            # This enables a higher level of scaling by reducing
                            # memory consumption and the amount of stream
                            # statistics results required.
                            hltkwargs['enable_stream'] = False
                            hltkwargs['enable_stream_only_gen'] = False
                    else:
                        if sub_stream_increments and Stream.SubStreamIncrement.any not in sub_stream_increments:
                            raise NotImplementedError(sub_stream_increments)

                    # Specify destination ports
                    if not self.bidirectional:
                        destination_tgen_interfaces = list(self.destination_tgen_interfaces)
                        if destination_tgen_interfaces:
                            hltkwargs['dest_port_list'] = [v.tgen_port_handle for v in destination_tgen_interfaces]

                    # Layer 2 protocol
                    # Setup list of possible L2 encaps based on L2 protocol
                    # Ordered by "priority", stream features will be used to
                    # limit the possibilities and the first one from the list
                    # that is left will be used.

                    l2_encaps = []
                    layer2_protocol = self.layer2_protocol
                    if layer2_protocol is Stream.Layer2Protocol.ethernet_ii:
                        l2_encaps += ['ethernet_ii']  # HLTAPI, Agilent, Ixia, Pagent, Spirent
                        l2_encaps += ['ethernet_ii_pppoe']  # Agilent, Ixia, Spirent
                        l2_encaps += ['ethernet_ii_vlan']  # HLTAPI, Agilent, Ixia, Pagent, Spirent
                        l2_encaps += ['ethernet_ii_vlan_pppoe']  # Agilent, Ixia, Spirent
                        l2_encaps += ['ethernet_ii_qinq_pppoe']  # Spirent
                        l2_encaps += ['ethernet_mac_in_mac']  # Agilent
                        l2_encaps += ['ethernet_ii_unicast_mpls']  # HLTAPI, Agilent, Ixia, Pagent, Spirent
                        l2_encaps += ['ethernet_ii_multicast_mpls']  # Agilent, Ixia, Pagent
                        l2_encaps += ['ethernet_ii_vlan_unicast_mpls']  # Agilent, Ixia
                        l2_encaps += ['ethernet_ii_vlan_multicast_mpls']  # Agilent, Ixia

                        # VLAN
                        eth_encap_range1 = self.eth_encap_range1
                        if eth_encap_range1:
                            eth_encap_range2 = self.eth_encap_range2
                            if eth_encap_range2:
                                l2_encaps = [l2_encap for l2_encap in l2_encaps
                                             if 'vlan' in l2_encap or 'qinq' in l2_encap]
                                if isinstance(device, SpirentDevice):
                                    # For Spirent, prefer ethernet_ii_qinq_pppoe to ethernet_ii_vlan_pppoe
                                    l2_encaps = [l2_encap for l2_encap in l2_encaps
                                                 if l2_encap != 'ethernet_ii_vlan_pppoe']

                                # eth_encap_range1 is outer tag
                                hltkwargs['vlan_id_outer'] = eth_encap_range1.start
                                hltkwargs['vlan_outer_cfi'] = 0  # Ethernet
                                if len(eth_encap_range1) > 1:
                                    hltkwargs['vlan_id_outer_mode'] = 'increment'
                                    hltkwargs['vlan_id_outer_count'] = len(eth_encap_range1)
                                    hltkwargs['vlan_id_outer_step'] = eth_encap_range1.step
                                else:
                                    hltkwargs['vlan_id_outer_mode'] = 'fixed'
                                # hltkwargs['vlan_outer_user_priority'] = TODO
                                # hltkwargs['vlan_outer_tpid'] = 0x8100

                                # eth_encap_range2 is inner tag
                                hltkwargs['vlan_cfi'] = 0  # Ethernet
                                hltkwargs['vlan_id'] = eth_encap_range2.start
                                if len(eth_encap_range2) > 1:
                                    hltkwargs['vlan_id_mode'] = 'increment'
                                    hltkwargs['vlan_id_count'] = len(eth_encap_range2)
                                    hltkwargs['vlan_id_step'] = eth_encap_range2.step
                                else:
                                    hltkwargs['vlan_id_mode'] = 'fixed'
                                # hltkwargs['vlan_user_priority'] = TODO

                            else:
                                l2_encaps = [l2_encap for l2_encap in l2_encaps
                                             if 'vlan' in l2_encap]

                                # eth_encap_range1 is outer tag (single)
                                hltkwargs['vlan_cfi'] = 0  # Ethernet
                                hltkwargs['vlan_id'] = eth_encap_range1.start
                                if len(eth_encap_range1) > 1:
                                    hltkwargs['vlan_id_mode'] = 'increment'
                                    hltkwargs['vlan_id_count'] = len(eth_encap_range1)
                                    hltkwargs['vlan_id_step'] = eth_encap_range1.step
                                else:
                                    hltkwargs['vlan_id_mode'] = 'fixed'
                                # hltkwargs['vlan_user_priority'] = TODO

                        else:
                            l2_encaps = [l2_encap for l2_encap in l2_encaps
                                         if 'vlan' not in l2_encap and 'qinq' not in l2_encap]

                        # MAC

                        source_mac_address_range = self.source_mac_address_range
                        if source_mac_address_range:
                            hltkwargs['mac_src'] = source_mac_address_range.start
                            if len(source_mac_address_range) > 1:
                                hltkwargs['mac_src_mode'] = 'increment'
                                hltkwargs['mac_src_count'] = len(source_mac_address_range)
                                hltkwargs['mac_src_step'] = MAC(source_mac_address_range.step)
                            else:
                                hltkwargs['mac_src_mode'] = 'fixed'

                        destination_mac_address_range = self.destination_mac_address_range
                        if destination_mac_address_range:
                            if destination_mac_address_range == 'discovery':
                                hltkwargs['mac_dst_mode'] = 'discovery'
                            else:
                                hltkwargs['mac_dst'] = destination_mac_address_range.start
                                if len(destination_mac_address_range) > 1:
                                    hltkwargs['mac_dst_mode'] = 'increment'
                                    hltkwargs['mac_dst_count'] = len(destination_mac_address_range)
                                    hltkwargs['mac_dst_step'] = MAC(destination_mac_address_range.step)
                                else:
                                    hltkwargs['mac_dst_mode'] = 'fixed'

                        mac_discovery_gateway_range = self.mac_discovery_gateway_range
                        if mac_discovery_gateway_range:
                            hltkwargs['mac_discovery_gw'] = mac_discovery_gateway_range.start
                            if len(mac_discovery_gateway_range) > 1:
                                # Not in spec: hltkwargs['mac_discovery_gw_mode'] = 'increment'
                                hltkwargs['mac_discovery_gw_count'] = len(mac_discovery_gateway_range)
                                hltkwargs['mac_discovery_gw_step'] = MAC(mac_discovery_gateway_range.step)
                            else:
                                # Not in spec: hltkwargs['mac_discovery_gw_mode'] = 'fixed'
                                pass

                    elif layer2_protocol is Stream.Layer2Protocol.atm:
                        l2_encaps += ['atm_snap']  # HLTAPI, Agilent, Ixia, Pagent
                        l2_encaps += ['atm_snap_802.3snap']  # HLTAPI, Agilent, Ixia
                        l2_encaps += ['atm_snap_802.3snap_nofcs']  # Ixia
                        l2_encaps += ['atm_snap_ethernet_ii']  # HLTAPI, Agilent, Ixia
                        l2_encaps += ['atm_snap_ppp']  # Agilent, Ixia
                        l2_encaps += ['atm_snap_pppoe']  # Agilent, Ixia
                        l2_encaps += ['atm_llcsnap']  # Spirent
                        l2_encaps += ['atm_vc_mux']  # HLTAPI, Agilent, Ixia, Spirent
                        l2_encaps += ['atm_vc_mux_802.3snap']  # HLTAPI, Agilent, Ixia
                        l2_encaps += ['atm_vc_mux_802.3snap_nofcs']  # Ixia
                        l2_encaps += ['atm_vc_mux_ethernet_ii']  # HLTAPI, Agilent, Ixia
                        l2_encaps += ['atm_vc_mux_ppp']  # Agilent, Ixia
                        l2_encaps += ['atm_vc_mux_pppoe']  # Agilent, Ixia
                        l2_encaps += ['atm_mpls']  # Pagent
                        raise NotImplementedError(layer2_protocol)

                        # VCI/VPI
                        # hltkwargs['vci'] = TODO
                        # hltkwargs['vci_count'] = TODO
                        # hltkwargs['vci_step'] = TODO
                        # hltkwargs['vpi'] = TODO
                        # hltkwargs['vpi_count'] = TODO
                        # hltkwargs['vpi_step'] = TODO

                    elif layer2_protocol is Stream.Layer2Protocol.hdlc:
                        l2_encaps += ['hdlc_unicast']  # HLTAPI, Agilent, Ixia, Pagent
                        l2_encaps += ['hdlc_broadcast']  # HLTAPI, Agilent, Ixia, Pagent
                        l2_encaps += ['hdlc_unicast_mpls']  # HLTAPI, Agilent, Ixia, Pagent
                        l2_encaps += ['hdlc_multicast_mpls']  # HLTAPI, Agilent, Ixia, Pagent

                    elif layer2_protocol is Stream.Layer2Protocol.ppp:
                        l2_encaps += ['ppp_link']  # Agilent, Ixia

                    elif layer2_protocol is Stream.Layer2Protocol.fr:
                        l2_encaps += ['cisco_framerelay']  # Ixia
                        l2_encaps += ['ietf_framerelay']  # Ixia

                    else:
                        l2_encaps += ['eth']  # HLTAPI
                        l2_encaps += ['raw_l2']  # Agilent
                        raise ValueError(layer2_protocol)

                    # PPPoE
                    if False:
                        l2_encaps = [l2_encap for l2_encap in l2_encaps
                                     if 'pppoe' in l2_encap]
                        # hltkwargs['ppp_session_id'] = TODO
                    else:
                        l2_encaps = [l2_encap for l2_encap in l2_encaps
                                     if 'pppoe' not in l2_encap]

                    # MPLS
                    mpls_labels = self.mpls_labels
                    if mpls_labels:
                        l2_encaps = [l2_encap for l2_encap in l2_encaps
                                     if 'mpls' in l2_encap]
                        hltkwargs['mpls_labels_mode'] = 'fixed'
                        hltkwargs['mpls_labels'] = mpls_labels
                    else:
                        l2_encaps = [l2_encap for l2_encap in l2_encaps
                                     if 'mpls' not in l2_encap]

                    if not l2_encaps:
                        raise ValueError('No possible L2 encapsulation!')
                    hltkwargs['l2_encap'] = l2_encap = l2_encaps[0]

                    hltkwargs['transmit_mode'] = self.transmit_mode.value
                    if self.transmit_mode in (
                            Stream.TransmitMode.single_burst,
                            Stream.TransmitMode.multi_burst,
                            Stream.TransmitMode.continuous_burst,
                    ):
                        hltkwargs['pkts_per_burst'] = self.packets_per_burst

                    # Bandwidth
                    bandwidth_units = self.bandwidth_units
                    if bandwidth_units is Stream.BandwidthUnits.mbps:
                        hltkwargs['rate_bps'] = self.bandwidth * 1000000  # TODO round_nearest
                    elif bandwidth_units is Stream.BandwidthUnits.kbps:
                        hltkwargs['rate_bps'] = self.bandwidth * 1000  # TODO round_nearest
                    elif bandwidth_units is Stream.BandwidthUnits.bps:
                        hltkwargs['rate_bps'] = self.bandwidth  # TODO round_nearest
                    elif bandwidth_units is Stream.BandwidthUnits.pps:
                        hltkwargs['rate_pps'] = self.bandwidth  # TODO round_nearest
                    elif bandwidth_units is Stream.BandwidthUnits.percent:
                        hltkwargs['rate_percent'] = self.bandwidth  # TODO round_nearest
                    else:
                        raise ValueError(bandwidth_units)

                    # Frame length
                    frame_length = self.frame_length
                    if frame_length is not None:
                        frame_length_mode = self.frame_length_mode
                        hltkwargs['length_mode'] = 'fixed'  # fixed | increment | random | auto | imix | gaussian | quad
                        if frame_length_mode is Stream.FrameLengthMode.l2:
                            hltkwargs['packet_len'] = frame_length
                        elif frame_length_mode is Stream.FrameLengthMode.l3:
                            hltkwargs['l3_length'] = frame_length
                        else:
                            raise ValueError(frame_length_mode)

                    # hltkwargs['frame_size'] = TODO
                    # hltkwargs['l3_length_max'] = TODO
                    # hltkwargs['l3_length_min'] = TODO
                    # hltkwargs['l3_gaus1_avg'] = TODO
                    # hltkwargs['l3_gaus2_avg'] = TODO
                    # hltkwargs['l3_gaus3_avg'] = TODO
                    # hltkwargs['l3_gaus4_avg'] = TODO
                    # hltkwargs['l3_guas1_halfbw'] = TODO
                    # hltkwargs['l3_guas1_weight'] = TODO
                    # hltkwargs['l3_guas2_halfbw'] = TODO
                    # hltkwargs['l3_guas2_weight'] = TODO
                    # hltkwargs['l3_guas3_halfbw'] = TODO
                    # hltkwargs['l3_guas3_weight'] = TODO
                    # hltkwargs['l3_guas4_halfbw'] = TODO
                    # hltkwargs['l3_guas4_weight'] = TODO
                    # hltkwargs['l3_imix1_ratio'] = TODO
                    # hltkwargs['l3_imix1_size'] = TODO
                    # hltkwargs['l3_imix2_ratio'] = TODO
                    # hltkwargs['l3_imix2_size'] = TODO
                    # hltkwargs['l3_imix3_ratio'] = TODO
                    # hltkwargs['l3_imix3_size'] = TODO
                    # hltkwargs['l3_imix4_ratio'] = TODO
                    # hltkwargs['l3_imix4_size'] = TODO

                    # Layer 3 protocol
                    # HLTAPI:  ipv4 ipv6 arp pause_control ipx
                    # Agilent: ipv4 ipv6 arp raw_ipv4_socket none
                    # Spirent: ipv4 ipv6 arp
                    # Ixia:    ipv4 ipv6 arp pause_control ipx
                    # Pagent:  ipv4 ipv6
                    layer3_protocol = self.layer3_protocol
                    if layer3_protocol is None:
                        # Only Agilent actually supports l3_protocol=none;
                        # Device-specific Hltapi override will fixup l3_protocol
                        hltkwargs['l3_protocol'] = 'none'
                    else:
                        # Assume OK
                        hltkwargs['l3_protocol'] = layer3_protocol.value

                    if layer3_protocol is None:
                        pass

                    elif layer3_protocol is Stream.Layer3Protocol.ipv4:
                        # IPv4

                        # Source
                        source_ip_range = self.source_ip_range
                        assert source_ip_range
                        hltkwargs['ip_src_addr'] = source_ip_range.start
                        if len(source_ip_range) > 1:
                            hltkwargs['ip_src_mode'] = 'increment'
                            hltkwargs['ip_src_count'] = len(source_ip_range)
                            hltkwargs['ip_src_step'] = IPv4Address(source_ip_range.step)
                        else:
                            hltkwargs['ip_src_mode'] = 'fixed'
                        # hltkwargs['ip_src_skip_broadcast'] = TODO
                        # hltkwargs['ip_src_skip_multicast'] = TODO

                        # Destination
                        destination_ip_range = self.destination_ip_range
                        assert destination_ip_range
                        hltkwargs['ip_dst_addr'] = destination_ip_range.start
                        if len(destination_ip_range) > 1:
                            hltkwargs['ip_dst_mode'] = 'increment'
                            hltkwargs['ip_dst_count'] = len(destination_ip_range)
                            hltkwargs['ip_dst_step'] = IPv4Address(destination_ip_range.step)
                        else:
                            hltkwargs['ip_dst_mode'] = 'fixed'
                        # hltkwargs['ip_dst_skip_broadcast'] = TODO
                        # hltkwargs['ip_dst_skip_multicast'] = TODO

                        # hltkwargs['ip_bit_flags'] = TODO
                        # hltkwargs['ip_checksum'] = TODO
                        # hltkwargs['ip_cu'] = TODO
                        # hltkwargs['ip_dscp'] = TODO
                        # hltkwargs['ip_dscp_count'] = TODO
                        # hltkwargs['ip_dscp_step'] = TODO
                        # hltkwargs['ip_fragment'] = TODO
                        # hltkwargs['ip_fragment_last'] = TODO
                        # hltkwargs['ip_fragment_offset'] = TODO
                        # hltkwargs['ip_hdr_length'] = TODO
                        # hltkwargs['ip_id'] = TODO
                        # hltkwargs['ip_mbz'] = TODO
                        # hltkwargs['ip_precedence'] = TODO
                        # hltkwargs['ip_precedence_count'] = TODO
                        # hltkwargs['ip_precedence_step'] = TODO
                        # hltkwargs['ip_protocol'] = TODO
                        # hltkwargs['ip_tos_count'] = TODO
                        # hltkwargs['ip_tos_field'] = TODO
                        # hltkwargs['ip_tos_step'] = TODO
                        # hltkwargs['ip_ttl'] = TODO

                    elif layer3_protocol is Stream.Layer3Protocol.ipv6:
                        # IPv6

                        # Source
                        source_ip_range = self.source_ip_range
                        assert source_ip_range
                        hltkwargs['ipv6_src_addr'] = source_ip_range.start
                        if len(source_ip_range) > 1:
                            hltkwargs['ipv6_src_mode'] = 'increment'
                            hltkwargs['ipv6_src_count'] = len(source_ip_range)
                            hltkwargs['ipv6_src_step'] = IPv6Address(source_ip_range.step)
                        else:
                            hltkwargs['ipv6_src_mode'] = 'fixed'

                        # Destination {{{
                        destination_ip_range = self.destination_ip_range
                        assert destination_ip_range
                        hltkwargs['ipv6_src_addr'] = destination_ip_range.start
                        if len(destination_ip_range) > 1:
                            hltkwargs['ipv6_src_mode'] = 'increment'
                            hltkwargs['ipv6_src_count'] = len(destination_ip_range)
                            hltkwargs['ipv6_src_step'] = IPv6Address(destination_ip_range.step)
                        else:
                            hltkwargs['ipv6_src_mode'] = 'fixed'

                        # hltkwargs['ipv6_checksum'] = TODO
                        # hltkwargs['ipv6_flow_label'] = TODO
                        # hltkwargs['ipv6_frag_id'] = TODO
                        # hltkwargs['ipv6_frag_more_flag'] = TODO
                        # hltkwargs['ipv6_frag_next_header'] = TODO
                        # hltkwargs['ipv6_frag_offset'] = TODO
                        # hltkwargs['ipv6_hop_limit'] = TODO
                        # hltkwargs['ipv6_length'] = TODO
                        # hltkwargs['ipv6_next_header'] = TODO
                        # hltkwargs['ipv6_src_addr'] = TODO
                        # hltkwargs['ipv6_src_count'] = TODO
                        # hltkwargs['ipv6_src_mode'] = TODO
                        # hltkwargs['ipv6_src_step'] = TODO
                        # hltkwargs['ipv6_traffic_class'] = TODO

                    elif layer3_protocol is Stream.Layer3Protocol.arp:
                        # ARP

                        hltkwargs['arp_operation'] = self.arp_operation.value
                        arp_source_mac_address_range = self.arp_source_mac_address_range
                        assert arp_source_mac_address_range
                        hltkwargs['arp_src_hw_addr'] = arp_source_mac_address_range.start
                        if len(arp_source_mac_address_range) > 1:
                            hltkwargs['arp_src_hw_mode'] = 'increment'
                            hltkwargs['arp_src_hw_count'] = len(arp_source_mac_address_range)
                            hltkwargs['arp_src_hw_step'] = MAC(arp_source_mac_address_range.step)
                        else:
                            hltkwargs['arp_src_hw_mode'] = 'fixed'

                        arp_destination_mac_address_range = self.arp_destination_mac_address_range
                        assert arp_destination_mac_address_range
                        hltkwargs['arp_dst_hw_addr'] = arp_destination_mac_address_range.start
                        if len(arp_destination_mac_address_range) > 1:
                            hltkwargs['arp_dst_hw_mode'] = 'increment'
                            hltkwargs['arp_dst_hw_count'] = len(arp_destination_mac_address_range)
                            hltkwargs['arp_dst_hw_step'] = MAC(arp_destination_mac_address_range.step)
                        else:
                            hltkwargs['arp_dst_hw_mode'] = 'fixed'

                        # Source protocol address (IP)
                        source_ip_range = self.source_ip_range
                        assert source_ip_range
                        hltkwargs['ip_src_addr'] = source_ip_range.start
                        if len(source_ip_range) > 1:
                            hltkwargs['ip_src_mode'] = 'increment'
                            hltkwargs['ip_src_count'] = len(source_ip_range)
                            hltkwargs['ip_src_step'] = IPv4Address(source_ip_range.step)
                        else:
                            hltkwargs['ip_src_mode'] = 'fixed'

                        # Destination protocol address (IP)
                        destination_ip_range = self.destination_ip_range
                        assert destination_ip_range
                        hltkwargs['ip_dst_addr'] = destination_ip_range.start
                        if len(destination_ip_range) > 1:
                            hltkwargs['ip_dst_mode'] = 'increment'
                            hltkwargs['ip_dst_count'] = len(destination_ip_range)
                            hltkwargs['ip_dst_step'] = IPv4Address(destination_ip_range.step)
                        else:
                            hltkwargs['ip_dst_mode'] = 'fixed'

                    elif layer3_protocol is Stream.Layer3Protocol.pause_control:
                        pass
                    elif layer3_protocol is Stream.Layer3Protocol.ipx:
                        pass
                    elif layer3_protocol is Stream.Layer3Protocol.raw_ipv4_socket:
                        pass
                    else:
                        raise ValueError(layer3_protocol)

                    layer4_protocol = self.layer4_protocol
                    if layer4_protocol is None:
                        hltkwargs['l4_protocol'] = 'none'
                    else:
                        # Assume OK
                        hltkwargs['l4_protocol'] = layer4_protocol.value

                    if layer4_protocol is None:
                        pass

                    elif layer4_protocol is Stream.Layer4Protocol.icmp:
                        # ICMP
                        raise NotImplementedError(layer4_protocol)
                        # hltkwargs['icmp_checksum'] = TODO
                        # hltkwargs['icmp_code'] = TODO
                        # hltkwargs['icmp_id'] = TODO
                        # hltkwargs['icmp_seq'] = TODO
                        # hltkwargs['icmp_type'] = TODO

                    elif layer4_protocol is Stream.Layer4Protocol.igmp:
                        # IGMP
                        raise NotImplementedError(layer4_protocol)
                        # hltkwargs['igmp_group_addr'] = TODO
                        # hltkwargs['igmp_group_count'] = TODO
                        # hltkwargs['igmp_group_mode'] = TODO
                        # hltkwargs['igmp_group_step'] = TODO
                        # hltkwargs['igmp_max_response_time'] = TODO
                        # hltkwargs['igmp_msg_type'] = TODO
                        # hltkwargs['igmp_multicast_src'] = TODO
                        # hltkwargs['igmp_qqic'] = TODO
                        # hltkwargs['igmp_qrv'] = TODO
                        # hltkwargs['igmp_record_type'] = TODO
                        # hltkwargs['igmp_s_flag'] = TODO
                        # hltkwargs['igmp_type'] = TODO
                        # hltkwargs['igmp_version'] = TODO

                    elif layer4_protocol is Stream.Layer4Protocol.tcp:
                        # TCP
                        raise NotImplementedError(layer4_protocol)
                        # hltkwargs['tcp_ack_flag'] = TODO
                        # hltkwargs['tcp_ack_num'] = TODO
                        # hltkwargs['tcp_dst_port'] = TODO
                        # hltkwargs['tcp_dst_port_increment'] = TODO
                        # hltkwargs['tcp_fin_flag'] = TODO
                        # hltkwargs['tcp_psh_flag'] = TODO
                        # hltkwargs['tcp_reserved'] = TODO
                        # hltkwargs['tcp_rst_flag'] = TODO
                        # hltkwargs['tcp_seq_num'] = TODO
                        # hltkwargs['tcp_src_port'] = TODO
                        # hltkwargs['tcp_src_port_increment'] = TODO
                        # hltkwargs['tcp_syn_flag'] = TODO
                        # hltkwargs['tcp_urg_flag'] = TODO
                        # hltkwargs['tcp_urgent_ptr'] = TODO
                        # hltkwargs['tcp_window'] = TODO
                        # hltkwargs['tcp_checksum'] = TODO
                        # hltkwargs['tcp_header_length'] = TODO
                        # hltkwargs['tcp_option_length'] = TODO

                    elif layer4_protocol is Stream.Layer4Protocol.udp:
                        # UDP
                        raise NotImplementedError(layer4_protocol)
                        # hltkwargs['udp_checksum'] = TODO
                        # hltkwargs['udp_dst_port'] = TODO
                        # hltkwargs['udp_dst_port_increment'] = TODO
                        # hltkwargs['udp_src_port'] = TODO
                        # hltkwargs['udp_src_port_increment'] = TODO
                        # hltkwargs['udp_length'] = TODO

                    elif layer4_protocol is Stream.Layer4Protocol.rip:
                        # RIP
                        raise NotImplementedError(layer4_protocol)

                    elif layer4_protocol is Stream.Layer4Protocol.dhcp:
                        # DHCP
                        raise NotImplementedError(layer4_protocol)
                        # hltkwargs['dhcp_option'] = TODO
                        # hltkwargs['circuit_id'] = TODO
                        # hltkwargs['remote_id'] = TODO

                    elif layer4_protocol is Stream.Layer4Protocol.ospf:
                        # OSPF
                        raise NotImplementedError(layer4_protocol)

                    elif layer4_protocol is Stream.Layer4Protocol.rtp:
                        # RTP
                        raise NotImplementedError(layer4_protocol)
                        # hltkwargs['ssrc'] = TODO
                        # hltkwargs['csrc_list'] = TODO
                        # hltkwargs['rtp_csrc_count'] = TODO
                        # hltkwargs['rtp_payload_type'] = TODO

                    else:
                        raise ValueError(layer4_protocol)

                    if self.bidirectional:
                        raise NotImplementedError('bidirectional')
                        # hltkwargs['bidirectional'] = TODO
                        # hltkwargs['mac_dst2'] = TODO
                        # hltkwargs['mac_dst2_count'] = TODO
                        # hltkwargs['mac_dst2_mode'] = TODO
                        # hltkwargs['mac_dst2_step'] = TODO
                        # hltkwargs['mac_src2'] = TODO
                        # hltkwargs['mac_src2_count'] = TODO
                        # hltkwargs['mac_src2_mode'] = TODO
                        # hltkwargs['mac_src2_step'] = TODO

                    # Not-implemented -- VPLS
                    # hltkwargs['vpls_source_handle'] = TODO
                    # hltkwargs['vpls_destination_handle'] = TODO
                    # hltkwargs['traffic_flooding_flag'] = TODO

                    # Not-implemented
                    # hltkwargs['mesh_traffic_type'] = TODO
                    # switch -exact -- $mesh_traffic_type {
                    #     "l2_mpls" {
                    #         # hltkwargs['l2mpls_stream'] = TODO
                    #     }
                    # }
                    # hltkwargs['burst_loop_count'] = TODO
                    # hltkwargs['data_length'] = TODO
                    # hltkwargs['data_offset_pattern'] = TODO
                    # hltkwargs['data_offset_start'] = TODO
                    # hltkwargs['data_pattern'] = TODO
                    # hltkwargs['disable_signature'] = TODO
                    # hltkwargs['emulation_dst_handle'] = TODO
                    # hltkwargs['emulation_src_handle'] = TODO
                    # hltkwargs['inter_burst_gap'] = TODO
                    # hltkwargs['inter_stream_gap'] = TODO
                    # hltkwargs['number_packets'] = TODO
                    # hltkwargs['pdu_fill_type'] = TODO
                    # hltkwargs['pdu_payload_bytes'] = TODO
                    # hltkwargs['pdu_payload_data'] = TODO
                    # hltkwargs['protocol'] = TODO
                    # hltkwargs['timestamp_increment'] = TODO
                    # hltkwargs['timestamp_initial_value'] = TODO
                    # hltkwargs['traffic_state'] = TODO

                    hltkl = hltapi.traffic_config(**hltkwargs)
                    if hltkwargs['mode'] == 'create' or 'stream_id' in hltkl:
                        self.tgen_handle = tcl.cast_list(hltkl.stream_id,
                                                         item_cast=item_cast)

                    # Sub-stream Increments
                    sub_stream_increments = self.sub_stream_increments
                    if isinstance(device, SpirentDevice):
                        if sub_stream_increments and Stream.SubStreamIncrement.any not in sub_stream_increments:
                            offsetreference_infos = defaultdict(list)
                            for streamblock in self.tgen_handle:
                                rangemodifiers = hltapi.stc_get(streamblock, '-children-rangemodifier',
                                                                         cast_=functools.partial(tcl.cast_list,
                                                                                                 item_cast=item_cast))
                                for rangemodifier in rangemodifiers:
                                    offsetreference = hltapi.stc_get(rangemodifier, '-OffsetReference',
                                                                     cast_=item_cast)
                                    offsetreference_infos[offsetreference].append((streamblock, rangemodifier))
                            selected_offsetreferences = []
                            for sub_stream_increment in sub_stream_increments:
                                if sub_stream_increment is Stream.SubStreamIncrement.any:
                                    pass  # Not reached
                                elif sub_stream_increment is Stream.SubStreamIncrement.source_mac_address:
                                    selected_offsetreferences += [
                                        e for e in offsetreference_infos
                                        if re.match(r'^ethernet_.*\.srcMac$', e)]
                                elif sub_stream_increment is Stream.SubStreamIncrement.destination_mac_address:
                                    selected_offsetreferences += [
                                        e for e in offsetreference_infos
                                        if re.match(r'^ethernet_.*\.dstMac$', e)]
                                elif sub_stream_increment is Stream.SubStreamIncrement.eth_encap_val1:
                                    selected_offsetreferences += [
                                        e for e in offsetreference_infos
                                        if re.match(r'^ethernet_.*\.vlans.*\.id$', e)]
                                else:
                                    raise ValueError(sub_stream_increment)
                            selected_offsetreferences = set(selected_offsetreferences)
                            for offsetreference in selected_offsetreferences:
                                for streamblock, rangemodifier in offsetreference_infos[offsetreference]:
                                    logger.debug('Enabling (sub-)stream on %r %r for %r' % (streamblock, rangemodifier, offsetreference))
                                    hltapi.stc_config(rangemodifier, '-EnableStream', 'true')
                                    bNeedStcApply = True
                    else:
                        if sub_stream_increments:
                            raise NotImplementedError(sub_stream_increments)

        finally:
            if bNeedStcApply:
                hltapi.stc_apply()
                bNeedStcApply = False

        return ''  # No CLI lines

    def build_unconfig(self, apply=True, attributes=None, **kwargs):
        return self.build_config(apply=apply, attributes=attributes, unconfig=True, **kwargs)

    def get_stats(self):
        '''Get stream stats'''
        return self.device.get_stream_stats([self]).by_stream[self]

    def get_resolved_mac_addresses(self):
        '''Get stream resolved MAC addresses'''
        return self.device.get_stream_resolved_mac_addresses([self]).by_stream[self]

    def discard(self):
        try:
            self.device.streams.discard(self)
        except AttributeError:
            pass

    def count_unique_packets(self):
        num_unique_packets = 0

        from genie.libs.conf.utils import gcd, lcm

        sub_stream_increments = self.sub_stream_increments
        if sub_stream_increments:
            raise NotImplementedError(sub_stream_increments)

        range_attributes = collections.OrderedDict()
        if self.layer2_protocol in (
                Stream.Layer2Protocol.ethernet_ii,
        ):
            range_attributes['source_mac_address'] = self.source_mac_address_range
            range_attributes['destination_mac_address'] = self.destination_mac_address_range
            range_attributes['mac_discovery_gateway'] = self.mac_discovery_gateway_range  # Hopefully aligned with the rest
            range_attributes['eth_encap_val1'] = self.eth_encap_range1
            range_attributes['eth_encap_val2'] = self.eth_encap_range2
        if self.layer3_protocol in (
                Stream.Layer3Protocol.arp,
        ):
            range_attributes['arp_source_mac_address'] = self.arp_source_mac_address_range
            range_attributes['arp_destination_mac_address'] = self.arp_destination_mac_address_range
        if self.layer3_protocol in (
                Stream.Layer3Protocol.ipv4,
                Stream.Layer3Protocol.ipv6,
                Stream.Layer3Protocol.arp,
        ):
            range_attributes['source_ip'] = self.source_ip_range
            range_attributes['destination_ip'] = self.destination_ip_range

        if range_attributes.get('destination_mac_address', None) == 'discovery':
            del range_attributes['destination_mac_address']

        num_unique_packets = functools.reduce(
            lcm, [len(v) or 1 for v in range_attributes.values()], 1)

        return num_unique_packets

    def iterate_packets(self):
        num_unique_packets = 0

        from genie.libs.conf.utils import gcd, lcm

        sub_stream_increments = self.sub_stream_increments
        if sub_stream_increments:
            raise NotImplementedError(sub_stream_increments)

        range_attributes = collections.OrderedDict()
        if self.layer2_protocol in (
                Stream.Layer2Protocol.ethernet_ii,
        ):
            range_attributes['source_mac_address'] = self.source_mac_address_range
            range_attributes['destination_mac_address'] = self.destination_mac_address_range
            range_attributes['mac_discovery_gateway'] = self.mac_discovery_gateway_range  # Hopefully aligned with the rest
            range_attributes['eth_encap_val1'] = self.eth_encap_range1
            range_attributes['eth_encap_val2'] = self.eth_encap_range2
        if self.layer3_protocol in (
                Stream.Layer3Protocol.arp,
        ):
            range_attributes['arp_source_mac_address'] = self.arp_source_mac_address_range
            range_attributes['arp_destination_mac_address'] = self.arp_destination_mac_address_range
        if self.layer3_protocol in (
                Stream.Layer3Protocol.ipv4,
                Stream.Layer3Protocol.ipv6,
                Stream.Layer3Protocol.arp,
        ):
            range_attributes['source_ip'] = self.source_ip_range
            range_attributes['destination_ip'] = self.destination_ip_range

        static_attributes = collections.OrderedDict()
        if range_attributes.get('destination_mac_address', None) == 'discovery':
            static_attributes['destination_mac_address'] = range_attributes.pop('destination_mac_address')
        static_attributes['stream'] = self
        static_attributes['mpls_labels'] = self.mpls_labels
        static_attributes['layer2_protocol'] = self.layer2_protocol
        static_attributes['layer3_protocol'] = self.layer3_protocol
        if self.layer3_protocol in (
                Stream.Layer3Protocol.arp,
        ):
            static_attributes['arp_operation'] = self.arp_operation
        static_attributes['layer4_protocol'] = self.layer4_protocol
        #static_attributes['frame_length'] = self.frame_length
        #static_attributes['frame_length_mode'] = self.frame_length_mode.value
        #static_attributes['bandwidth'] = self.bandwidth
        #static_attributes['bandwidth_units'] = self.bandwidth_units.value

        num_unique_packets = functools.reduce(
            lcm, [len(v) or 1 for v in range_attributes.values()], 1)

        def my_rng_cycle(rng):
            if rng:
                # Better implementation than itertools.cycle since it needs no
                # extra memory.
                while True:
                    yield from rng
            else:
                yield from itertools.repeat(None)

        iterators = collections.OrderedDict()
        iterators['idx'] = range(num_unique_packets)
        for attr, rng in range_attributes.items():
            iterators[attr] = my_rng_cycle(rng)
        for attr, value in static_attributes.items():
            iterators[attr] = itertools.repeat(value)

        attrs = list(iterators.keys())
        Packet = collections.namedtuple('Packet', attrs)
        for values in zip(*iterators.values()):
            yield Packet(*values)

