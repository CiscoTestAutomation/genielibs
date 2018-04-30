
from enum import Enum
import functools

from genie.decorator import managedattribute
from genie.conf.base.attributes import KeyedSubAttributes


@functools.total_ordering
class AFI(Enum):
    '''IANA Address Family Identifiers.

    value: Printable/readable/Cisco-ized string.
    iana_number: IANA-assigned numerical value.

    See: http://www.iana.org/assignments/address-family-numbers/address-family-numbers.xhtml
    '''

    ipv4 = ('ipv4', 1)
    ipv6 = ('ipv6', 2)
    l2vpn = ('l2vpn', 25)
    link_state = ('link-state', 16388)

    def __new__(cls, value, iana_number):
        e = object.__new__(cls)
        e._value_ = value
        e.iana_number = iana_number
        return e

    def __repr__(self):
        return '%s.%s' % (
            self.__class__.__name__, self._name_)

    def __int__(self):
        return self.iana_number

    def __eq__(self, other):
        if not isinstance(other, AddressFamily):
            return NotImplemented
        return self is other

    def __lt__(self, other):
        if not isinstance(other, AddressFamily):
            return NotImplemented
        # Alphabetical
        return self.value < other.value

    __hash__ = Enum.__hash__


@functools.total_ordering
class SAFI(Enum):
    '''IANA Subsequent Address Family Identifiers.

    value: Printable/readable/Cisco-ized string.
    iana_number: IANA-assigned numerical value.

    See: http://www.iana.org/assignments/safi-namespace/safi-namespace.xhtml
    '''

    unicast = ('unicast', 1)
    multicast = ('multicast', 2)
    bothcast = ('bothcast', 3)
    labeled_unicast = ('labeled-unicast', 4)
    mvpn = ('mvpn', 5)
    l2vpn_mspw = ('l2vpn mspw', 6)
    tunnel = ('tunnel', 64)
    l2vpn_vpls_vpws = ('l2vpn vpls-vpws', 65)
    l2vpn_vpls = ('l2vpn vpls', 65)
    mdt = ('mdt', 66)
    l2vpn_evpn = ('l2vpn evpn', 70)
    link_state = ('link-state', 71)
    vpn_unicast = ('vpn unicast', 128)
    vpn_multicast = ('vpn multicast', 129)
    rt_filter = ('rt-filter', 132)
    flowspec = ('flowspec', 133)
    vpn_flowspec = ('vpn flowspec', 134)

    def __new__(cls, value, iana_number):
        e = object.__new__(cls)
        e._value_ = value
        e.iana_number = iana_number
        return e

    def __repr__(self):
        return '%s.%s' % (
            self.__class__.__name__, self._name_)

    def __int__(self):
        return self.iana_number

    def __eq__(self, other):
        if not isinstance(other, AddressFamily):
            return NotImplemented
        return self is other

    def __lt__(self, other):
        if not isinstance(other, AddressFamily):
            return NotImplemented
        # Alphabetical
        return self.value < other.value

    __hash__ = Enum.__hash__


@functools.total_ordering
class AddressFamily(Enum):

    ipv4 = ('ipv4', AFI.ipv4, None)
    ipv6 = ('ipv6', AFI.ipv6, None)

    ipv4_flowspec = ('ipv4 flowspec', AFI.ipv4, SAFI.flowspec)
    ipv4_labeled_unicast = ('ipv4 labeled-unicast', AFI.ipv4, SAFI.labeled_unicast)
    ipv4_mdt = ('ipv4 mdt', AFI.ipv4, SAFI.mdt)
    ipv4_multicast = ('ipv4 multicast', AFI.ipv4, SAFI.multicast)
    ipv4_mvpn = ('ipv4 mvpn', AFI.ipv4, SAFI.mvpn)
    ipv4_rt_filter = ('ipv4 rt-filter', AFI.ipv4, SAFI.rt_filter)
    ipv4_tunnel = ('ipv4 tunnel', AFI.ipv4, SAFI.tunnel)
    ipv4_unicast = ('ipv4 unicast', AFI.ipv4, SAFI.unicast)
    ipv6_flowspec = ('ipv6 flowspec', AFI.ipv6, SAFI.flowspec)
    ipv6_labeled_unicast = ('ipv6 labeled-unicast', AFI.ipv6, SAFI.labeled_unicast)
    ipv6_multicast = ('ipv6 multicast', AFI.ipv6, SAFI.multicast)
    ipv6_mvpn = ('ipv6 mvpn', AFI.ipv6, SAFI.mvpn)
    ipv6_unicast = ('ipv6 unicast', AFI.ipv6, SAFI.unicast)
    l2vpn_evpn = ('l2vpn evpn', AFI.l2vpn, SAFI.l2vpn_evpn)
    l2vpn_mspw = ('l2vpn mspw', AFI.l2vpn, SAFI.l2vpn_mspw)
    l2vpn_vpls_vpws = ('l2vpn vpls-vpws', AFI.l2vpn, SAFI.l2vpn_vpls_vpws)
    l2vpn_vpls = ('l2vpn vpls', AFI.l2vpn, SAFI.l2vpn_vpls)
    link_state_link_state = ('link-state link-state', AFI.link_state, SAFI.link_state)
    link_state = ('link-state', AFI.link_state, None)
    vpnv4_flowspec = ('vpnv4 flowspec', AFI.ipv4, SAFI.vpn_flowspec)
    vpnv4_multicast = ('vpnv4 multicast', AFI.ipv4, SAFI.vpn_multicast)
    vpnv4_unicast = ('vpnv4 unicast', AFI.ipv4, SAFI.vpn_unicast)
    vpnv6_flowspec = ('vpnv6 flowspec', AFI.ipv6, SAFI.vpn_flowspec)
    vpnv6_multicast = ('vpnv6 multicast', AFI.ipv6, SAFI.vpn_multicast)
    vpnv6_unicast = ('vpnv6 unicast', AFI.ipv6, SAFI.vpn_unicast)

    def __new__(cls, value, afi, safi):
        e = object.__new__(cls)
        e._value_ = value
        e.afi = afi
        e.safi = safi
        return e

    def __repr__(self):
        return '%s.%s' % (
            self.__class__.__name__, self._name_)

    def __eq__(self, other):
        if not isinstance(other, AddressFamily):
            return NotImplemented
        return self is other

    def __lt__(self, other):
        if not isinstance(other, AddressFamily):
            return NotImplemented
        # Alphabetical
        return self.value < other.value

    __hash__ = Enum.__hash__


class AddressFamilySubAttributes(KeyedSubAttributes):

    address_family = managedattribute(
        name='address_family',
        read_only=True)  # key

    def __init__(self, parent, key):
        self._address_family = key
        super().__init__(parent=parent)

    @classmethod
    def _sanitize_key(cls, key):
        if key is None:
            # allow indexing with a address_family=None
            pass
        else:
            key = AddressFamily(key)
        return key

    @classmethod
    def _assert_key_allowed(cls, key):
        if key is None:
            # allow indexing with a address_family=None
            pass
        elif key not in AddressFamily:
            raise KeyError(
                '{cls} only accepts AddressFamily values, not {key!r}'.
                format(cls=cls.__name__, key=key))
        allowed_keys = getattr(cls, 'allowed_keys', None)
        if allowed_keys is not None:
            if key not in allowed_keys:
                raise KeyError(
                    '{cls} only accepts {allowed_keys}, not {key!r}'.\
                    format(cls=cls.__name__,
                           allowed_keys=allowed_keys,
                           key=key))

