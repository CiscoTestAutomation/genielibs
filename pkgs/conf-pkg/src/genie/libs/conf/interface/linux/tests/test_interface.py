#!/usr/bin/env python

# python
import unittest

# Genie package
from genie.tests.conf import TestCase
from genie.conf import Genie
from genie.conf.base import Testbed, Device

# Linux interface classes under test
from genie.libs.conf.interface.linux.interface import (
    Interface,
    ParsedInterfaceName,
    PhysicalInterface,
    EthernetInterface,
    WlanInterface,
    WwanInterface,
    VirtualInterface,
    LoopbackInterface,
    BridgeInterface,
    BondInterface,
    VlanInterface,
    TunnelInterface,
    SubInterface,
    AliasInterface,
)


class test_linux_interface(TestCase):

    maxDiff = None

    def test_PhysicalInterface_factory(self):
        """Test that physical interface names resolve to the right subclass."""
        Genie.testbed = Testbed()
        dev1 = Device(name='linux-host', os='linux')

        # Classical + predictable Ethernet
        for name in ('eth0', 'ens34', 'eno1', 'enp0s3', 'enp2s0f1'):
            intf = Interface(device=dev1, name=name)
            self.assertIsInstance(intf, EthernetInterface,
                                  f'{name} should be EthernetInterface')
            self.assertIsInstance(intf, PhysicalInterface,
                                  f'{name} should be PhysicalInterface')

        # Wireless
        for name in ('wlan0', 'wlp2s0'):
            intf = Interface(device=dev1, name=name)
            self.assertIsInstance(intf, WlanInterface,
                                  f'{name} should be WlanInterface')

    def test_VirtualInterface_factory(self):
        """Test that virtual interface names resolve to the right subclass."""
        Genie.testbed = Testbed()
        dev1 = Device(name='linux-host', os='linux')

        for name, expected_cls in (
            ('lo',       LoopbackInterface),
            ('br0',      BridgeInterface),
            ('docker0',  BridgeInterface),
            ('virbr0',   BridgeInterface),
            ('bond0',    BondInterface),
            ('vlan10',   VlanInterface),
            ('tun0',     TunnelInterface),
            ('tap0',     TunnelInterface),
            ('dummy0',   TunnelInterface),
            ('veth0',    TunnelInterface),
        ):
            intf = Interface(device=dev1, name=name)
            self.assertIsInstance(intf, expected_cls,
                                  f'{name} should be {expected_cls.__name__}')
            self.assertIsInstance(intf, VirtualInterface,
                                  f'{name} should be VirtualInterface')

    def test_SubInterface_factory(self):
        """Test that dot-notation names resolve to SubInterface."""
        Genie.testbed = Testbed()
        dev1 = Device(name='linux-host', os='linux')

        for name in ('eth0.100', 'enp0s3.200', 'bond0.10', 'ens34.4094'):
            intf = Interface(device=dev1, name=name)
            self.assertIsInstance(intf, SubInterface,
                                  f'{name} should be SubInterface')
            self.assertIsInstance(intf, VirtualInterface,
                                  f'{name} should be VirtualInterface')

    def test_PhysicalInterface_enable_disable(self):
        """Test ip link set up/down config and unconfig."""
        Genie.testbed = Testbed()
        dev1 = Device(name='linux-host', os='linux')
        intf1 = Interface(device=dev1, name='eth0')

        # Enable interface
        intf1.enabled = True
        cfg = intf1.build_config(apply=False)
        self.assertMultiLineEqual(str(cfg), '\n'.join([
            'ip link set eth0 up',
        ]))

        # Unconfig enabled — should bring down
        uncfg = intf1.build_unconfig(apply=False, attributes='enabled')
        self.assertMultiLineEqual(str(uncfg), '\n'.join([
            'ip link set eth0 down',
        ]))

        # Disable interface
        intf1.enabled = False
        cfg = intf1.build_config(apply=False)
        self.assertMultiLineEqual(str(cfg), '\n'.join([
            'ip link set eth0 down',
        ]))

    def test_PhysicalInterface_mtu(self):
        """Test MTU config and unconfig (reset to 1500)."""
        Genie.testbed = Testbed()
        dev1 = Device(name='linux-host', os='linux')
        intf1 = Interface(device=dev1, name='eth0')

        intf1.mtu = 9000
        cfg = intf1.build_config(apply=False)
        self.assertMultiLineEqual(str(cfg), '\n'.join([
            'ip link set eth0 mtu 9000',
        ]))

        uncfg = intf1.build_unconfig(apply=False, attributes='mtu')
        self.assertMultiLineEqual(str(uncfg), '\n'.join([
            'ip link set eth0 mtu 1500',
        ]))

    def test_PhysicalInterface_ipv4(self):
        """Test IPv4 address config and unconfig."""
        Genie.testbed = Testbed()
        dev1 = Device(name='linux-host', os='linux')
        intf1 = Interface(device=dev1, name='eth0')

        intf1.ipv4 = '192.168.1.10/24'
        cfg = intf1.build_config(apply=False)
        self.assertMultiLineEqual(str(cfg), '\n'.join([
            'ip addr add 192.168.1.10/24 dev eth0',
        ]))

        uncfg = intf1.build_unconfig(apply=False, attributes='ipv4')
        self.assertMultiLineEqual(str(uncfg), '\n'.join([
            'ip addr del 192.168.1.10/24 dev eth0',
        ]))

    def test_PhysicalInterface_ipv6(self):
        """Test IPv6 address config and unconfig."""
        Genie.testbed = Testbed()
        dev1 = Device(name='linux-host', os='linux')
        intf1 = Interface(device=dev1, name='eth0')

        intf1.ipv6 = '2001:db8::1/64'
        cfg = intf1.build_config(apply=False)
        self.assertMultiLineEqual(str(cfg), '\n'.join([
            'ip -6 addr add 2001:db8::1/64 dev eth0',
        ]))

        uncfg = intf1.build_unconfig(apply=False, attributes='ipv6')
        self.assertMultiLineEqual(str(uncfg), '\n'.join([
            'ip -6 addr del 2001:db8::1/64 dev eth0',
        ]))

    def test_PhysicalInterface_all_attributes(self):
        """Test full config and unconfig with all supported attributes."""
        Genie.testbed = Testbed()
        dev1 = Device(name='linux-host', os='linux')
        intf1 = Interface(device=dev1, name='eth0')

        intf1.enabled = True
        intf1.mtu = 1400
        intf1.ipv4 = '10.0.0.1/8'
        intf1.ipv6 = '2001:db8::1/64'

        cfg = intf1.build_config(apply=False)
        self.assertMultiLineEqual(str(cfg), '\n'.join([
            'ip link set eth0 up',
            'ip link set eth0 mtu 1400',
            'ip addr add 10.0.0.1/8 dev eth0',
            'ip -6 addr add 2001:db8::1/64 dev eth0',
        ]))

        # Full unconfig resets each attribute
        uncfg = intf1.build_unconfig(apply=False, attributes={
            'enabled': None,
            'mtu': None,
            'ipv4': None,
            'ipv6': None,
        })
        self.assertMultiLineEqual(str(uncfg), '\n'.join([
            'ip link set eth0 down',
            'ip link set eth0 mtu 1500',
            'ip addr del 10.0.0.1/8 dev eth0',
            'ip -6 addr del 2001:db8::1/64 dev eth0',
        ]))

    def test_VirtualInterface_loopback(self):
        """Test loopback (virtual) interface config."""
        Genie.testbed = Testbed()
        dev1 = Device(name='linux-host', os='linux')
        lo = Interface(device=dev1, name='lo')

        self.assertIsInstance(lo, VirtualInterface)

        lo.enabled = True
        lo.ipv4 = '127.0.0.1/8'

        cfg = lo.build_config(apply=False)
        self.assertMultiLineEqual(str(cfg), '\n'.join([
            'ip link set lo up',
            'ip addr add 127.0.0.1/8 dev lo',
        ]))

        uncfg = lo.build_unconfig(apply=False, attributes={
            'enabled': None,
            'ipv4': None,
        })
        self.assertMultiLineEqual(str(uncfg), '\n'.join([
            'ip link set lo down',
            'ip addr del 127.0.0.1/8 dev lo',
        ]))

    def test_VirtualInterface_bond(self):
        """Test bond interface config."""
        Genie.testbed = Testbed()
        dev1 = Device(name='linux-host', os='linux')
        bond0 = Interface(device=dev1, name='bond0')

        self.assertIsInstance(bond0, VirtualInterface)

        bond0.enabled = True
        bond0.mtu = 9000
        bond0.ipv4 = '172.16.0.1/16'

        cfg = bond0.build_config(apply=False)
        self.assertMultiLineEqual(str(cfg), '\n'.join([
            'ip link set bond0 up',
            'ip link set bond0 mtu 9000',
            'ip addr add 172.16.0.1/16 dev bond0',
        ]))

    def test_partial_unconfig_ipv4_only(self):
        """Test partial unconfig targeting only IPv4."""
        Genie.testbed = Testbed()
        dev1 = Device(name='linux-host', os='linux')
        intf1 = Interface(device=dev1, name='ens34')

        intf1.enabled = True
        intf1.mtu = 1500
        intf1.ipv4 = '192.168.100.1/24'
        intf1.ipv6 = 'fe80::1/64'

        uncfg = intf1.build_unconfig(apply=False, attributes='ipv4')
        self.assertMultiLineEqual(str(uncfg), '\n'.join([
            'ip addr del 192.168.100.1/24 dev ens34',
        ]))

    def test_partial_unconfig_ipv6_only(self):
        """Test partial unconfig targeting only IPv6."""
        Genie.testbed = Testbed()
        dev1 = Device(name='linux-host', os='linux')
        intf1 = Interface(device=dev1, name='ens34')

        intf1.ipv4 = '10.1.1.1/24'
        intf1.ipv6 = '2001:db8:1::1/64'

        uncfg = intf1.build_unconfig(apply=False, attributes='ipv6')
        self.assertMultiLineEqual(str(uncfg), '\n'.join([
            'ip -6 addr del 2001:db8:1::1/64 dev ens34',
        ]))

    def test_no_attributes_no_output(self):
        """Test that interface with no attributes produces empty config."""
        Genie.testbed = Testbed()
        dev1 = Device(name='linux-host', os='linux')
        intf1 = Interface(device=dev1, name='eth0')

        cfg = intf1.build_config(apply=False)
        self.assertMultiLineEqual(str(cfg), '')

    # ------------------------------------------------------------------
    # ParsedInterfaceName tests
    # ------------------------------------------------------------------

    def test_parsed_simple_no_subintf(self):
        """Simple names like eth0 parse into type + number with no subintf."""
        p = ParsedInterfaceName('eth0')
        self.assertEqual(p.type, 'eth')
        self.assertEqual(p.number, '0')
        self.assertIsNone(p.subintf_sep)
        self.assertIsNone(p.subintf)

    def test_parsed_eth_subintf(self):
        """eth0.100 must split into number='0', subintf_sep='.', subintf='100'."""
        p = ParsedInterfaceName('eth0.100')
        self.assertEqual(p.type, 'eth')
        self.assertEqual(p.number, '0')
        self.assertEqual(p.subintf_sep, '.')
        self.assertEqual(p.subintf, '100')

    def test_parsed_bond_subintf(self):
        """bond0.200 must split correctly."""
        p = ParsedInterfaceName('bond0.200')
        self.assertEqual(p.type, 'bond')
        self.assertEqual(p.number, '0')
        self.assertEqual(p.subintf_sep, '.')
        self.assertEqual(p.subintf, '200')

    def test_parsed_predictable_name_no_subintf(self):
        """Predictable name enp0s3: type=ethernet, sub_type=pci, bus=0, slot=3."""
        p = ParsedInterfaceName('enp0s3')
        self.assertEqual(p.type, 'ethernet')
        self.assertEqual(p.type_prefix, 'en')
        self.assertEqual(p.sub_type, 'pci')
        self.assertEqual(p.bus, 0)
        self.assertEqual(p.slot, 3)
        self.assertIsNone(p.number)
        self.assertIsNone(p.domain)
        self.assertIsNone(p.function)
        self.assertIsNone(p.subintf_sep)
        self.assertIsNone(p.subintf)

    def test_parsed_predictable_name_with_subintf(self):
        """enp0s3.100 — PCI parsed + subinterface suffix."""
        p = ParsedInterfaceName('enp0s3.100')
        self.assertEqual(p.type, 'ethernet')
        self.assertEqual(p.type_prefix, 'en')
        self.assertEqual(p.sub_type, 'pci')
        self.assertEqual(p.bus, 0)
        self.assertEqual(p.slot, 3)
        self.assertEqual(p.subintf_sep, '.')
        self.assertEqual(p.subintf, '100')

    def test_sub_interface_number(self):
        """Interface.sub_interface_number returns the subintf as int."""
        Genie.testbed = Testbed()
        dev1 = Device(name='linux-host', os='linux')
        sub = Interface(device=dev1, name='eth0.100')
        self.assertEqual(sub.sub_interface_number, 100)

    def test_parent_interface_resolution(self):
        """Sub-interface eth0.100 resolves parent to eth0."""
        Genie.testbed = Testbed()
        dev1 = Device(name='linux-host', os='linux')
        parent = Interface(device=dev1, name='eth0')
        sub = Interface(device=dev1, name='eth0.100')
        self.assertEqual(sub.parent_interface, parent)

    def test_predictable_subintf_sub_interface_number(self):
        """enp0s3.100 sub_interface_number returns 100."""
        Genie.testbed = Testbed()
        dev1 = Device(name='linux-host', os='linux')
        sub = Interface(device=dev1, name='enp0s3.100')
        self.assertEqual(sub.sub_interface_number, 100)

    # ------------------------------------------------------------------
    # Predictable name attribute tests
    # ------------------------------------------------------------------

    def test_predictable_onboard(self):
        """eno1 — onboard type: type=ethernet, sub_type=onboard, number='1'."""
        p = ParsedInterfaceName('eno1')
        self.assertEqual(p.type, 'ethernet')
        self.assertEqual(p.type_prefix, 'en')
        self.assertEqual(p.sub_type, 'onboard')
        self.assertEqual(p.number, '1')
        self.assertIsNone(p.bus)
        self.assertIsNone(p.slot)

    def test_predictable_pcie_hotplug(self):
        """ens34 — PCIe hotplug slot: type=ethernet, sub_type=pcie, slot=34."""
        p = ParsedInterfaceName('ens34')
        self.assertEqual(p.type, 'ethernet')
        self.assertEqual(p.type_prefix, 'en')
        self.assertEqual(p.sub_type, 'pcie')
        self.assertEqual(p.slot, 34)
        self.assertIsNone(p.bus)
        self.assertIsNone(p.number)

    def test_predictable_pci_with_function(self):
        """enp2s0f1 — PCI with function number."""
        p = ParsedInterfaceName('enp2s0f1')
        self.assertEqual(p.type, 'ethernet')
        self.assertEqual(p.sub_type, 'pci')
        self.assertEqual(p.bus, 2)
        self.assertEqual(p.slot, 0)
        self.assertEqual(p.function, 1)
        self.assertIsNone(p.dev_id)

    def test_predictable_pci_with_domain(self):
        """enP1p0s3 — PCI with explicit domain."""
        p = ParsedInterfaceName('enP1p0s3')
        self.assertEqual(p.type, 'ethernet')
        self.assertEqual(p.sub_type, 'pci')
        self.assertEqual(p.domain, 1)
        self.assertEqual(p.bus, 0)
        self.assertEqual(p.slot, 3)

    def test_predictable_pci_all_fields(self):
        """enP0p1s2f3d4u5c6i7 — all PCI/USB fields present."""
        p = ParsedInterfaceName('enP0p1s2f3d4u5c6i7')
        self.assertEqual(p.type, 'ethernet')
        self.assertEqual(p.sub_type, 'pci')
        self.assertEqual(p.domain, 0)
        self.assertEqual(p.bus, 1)
        self.assertEqual(p.slot, 2)
        self.assertEqual(p.function, 3)
        self.assertEqual(p.dev_id, 4)
        self.assertEqual(p.port, 5)
        self.assertEqual(p.config, 6)
        self.assertEqual(p.interface_id, 7)

    def test_predictable_wlan_pci(self):
        """wlp2s0 — WiFi PCI: type=wlan, sub_type=pci, bus=2, slot=0."""
        p = ParsedInterfaceName('wlp2s0')
        self.assertEqual(p.type, 'wlan')
        self.assertEqual(p.type_prefix, 'wl')
        self.assertEqual(p.sub_type, 'pci')
        self.assertEqual(p.bus, 2)
        self.assertEqual(p.slot, 0)

    def test_classical_wlan_not_predictable(self):
        """wlan0 is a classical name, not a predictable one."""
        p = ParsedInterfaceName('wlan0')
        self.assertEqual(p.type, 'wlan')
        self.assertEqual(p.number, '0')
        self.assertIsNone(p.type_prefix)
        self.assertIsNone(p.sub_type)

    def test_predictable_reconstruct_pci(self):
        """reconstruct() rebuilds the original predictable name for PCI."""
        for name in ('enp0s3', 'enp2s0f1', 'enP1p0s3', 'enP0p1s2f3d4u5c6i7',
                     'wlp2s0'):
            p = ParsedInterfaceName(name)
            self.assertEqual(p.reconstruct(), name,
                             f'reconstruct() failed for {name!r}')

    def test_predictable_reconstruct_onboard_pcie(self):
        """reconstruct() rebuilds onboard and PCIe hotplug names."""
        for name in ('eno1', 'ens34'):
            p = ParsedInterfaceName(name)
            self.assertEqual(p.reconstruct(), name,
                             f'reconstruct() failed for {name!r}')

    # ------------------------------------------------------------------
    # DeviceTree / ACPI onboard names (end0, end1 …)
    # ------------------------------------------------------------------

    def test_predictable_devicetree_onboard(self):
        """end0 parses as ethernet / devicetree sub_type, not a classical name."""
        p = ParsedInterfaceName('end0')
        self.assertEqual(p.type, 'ethernet')
        self.assertEqual(p.type_prefix, 'en')
        self.assertEqual(p.sub_type, 'devicetree')
        self.assertEqual(p.number, '0')
        self.assertIsNone(p.bus)
        self.assertIsNone(p.slot)

    def test_predictable_devicetree_reconstruct(self):
        """reconstruct() round-trips DeviceTree names."""
        for name in ('end0', 'end1'):
            p = ParsedInterfaceName(name)
            self.assertEqual(p.reconstruct(), name,
                             f'reconstruct() failed for {name!r}')

    def test_predictable_devicetree_factory(self):
        """end0 resolves to EthernetInterface via factory."""
        Genie.testbed = Testbed()
        dev1 = Device(name='linux-host', os='linux')
        intf = Interface(device=dev1, name='end0')
        self.assertIsInstance(intf, EthernetInterface)

    def test_predictable_devicetree_with_subintf(self):
        """end0.100 correctly parses DeviceTree base + sub-interface suffix."""
        p = ParsedInterfaceName('end0.100')
        self.assertEqual(p.sub_type, 'devicetree')
        self.assertEqual(p.number, '0')
        self.assertEqual(p.subintf, '100')

    # ------------------------------------------------------------------
    # PCIe slot extra suffixes (dev_port, port_name)
    # ------------------------------------------------------------------

    def test_predictable_pcie_with_dev_port(self):
        """ens34d1 — PCIe slot with dev_port suffix."""
        p = ParsedInterfaceName('ens34d1')
        self.assertEqual(p.sub_type, 'pcie')
        self.assertEqual(p.slot, 34)
        self.assertEqual(p.dev_port, 1)
        self.assertIsNone(p.function)
        self.assertIsNone(p.port_name)

    def test_predictable_pcie_with_function_and_dev_port(self):
        """ens34f0d1 — PCIe slot with function + dev_port."""
        p = ParsedInterfaceName('ens34f0d1')
        self.assertEqual(p.sub_type, 'pcie')
        self.assertEqual(p.slot, 34)
        self.assertEqual(p.function, 0)
        self.assertEqual(p.dev_port, 1)

    def test_predictable_pcie_with_port_name(self):
        """ens34neth0 — PCIe slot with firmware port_name."""
        p = ParsedInterfaceName('ens34neth0')
        self.assertEqual(p.sub_type, 'pcie')
        self.assertEqual(p.slot, 34)
        self.assertEqual(p.port_name, 'eth0')
        self.assertIsNone(p.dev_port)

    def test_predictable_pcie_all_suffixes(self):
        """ens34f1d2nport0 — PCIe slot with all optional suffixes."""
        p = ParsedInterfaceName('ens34f1d2nport0')
        self.assertEqual(p.sub_type, 'pcie')
        self.assertEqual(p.slot, 34)
        self.assertEqual(p.function, 1)
        self.assertEqual(p.dev_port, 2)
        self.assertEqual(p.port_name, 'port0')

    def test_predictable_pcie_reconstruct_extra_suffixes(self):
        """reconstruct() round-trips PCIe names with dev_port and port_name."""
        for name in ('ens34d1', 'ens34f0d1', 'ens34f1d2nport0'):
            p = ParsedInterfaceName(name)
            self.assertEqual(p.reconstruct(), name,
                             f'reconstruct() failed for {name!r}')

    def test_predictable_onboard_with_dev_port(self):
        """eno1d1 — onboard with dev_port suffix."""
        p = ParsedInterfaceName('eno1d1')
        self.assertEqual(p.sub_type, 'onboard')
        self.assertEqual(p.number, '1')
        self.assertEqual(p.dev_port, 1)
        self.assertIsNone(p.port_name)

    def test_predictable_onboard_with_port_name(self):
        """eno1nsfp0 — onboard with firmware port_name."""
        p = ParsedInterfaceName('eno1nsfp0')
        self.assertEqual(p.sub_type, 'onboard')
        self.assertEqual(p.number, '1')
        self.assertEqual(p.port_name, 'sfp0')
        self.assertIsNone(p.dev_port)

    def test_predictable_onboard_reconstruct_extra_suffixes(self):
        """reconstruct() round-trips onboard names with dev_port and port_name."""
        for name in ('eno1d1', 'eno1nsfp0', 'eno1d1nsfp0'):
            p = ParsedInterfaceName(name)
            self.assertEqual(p.reconstruct(), name,
                             f'reconstruct() failed for {name!r}')

    def test_predictable_reconstruct_with_subintf(self):
        """reconstruct() with subintf=None drops the suffix (parent resolution)."""
        p = ParsedInterfaceName('enp0s3.100')
        p.subintf = None
        p.subintf_sep = None
        self.assertEqual(p.reconstruct(), 'enp0s3')

    def test_predictable_factory_still_physical(self):
        """Predictable names (ens34, enp0s3, eno1) resolve to EthernetInterface."""
        Genie.testbed = Testbed()
        dev1 = Device(name='linux-host', os='linux')
        for name in ('ens34', 'enp0s3', 'eno1', 'enp2s0f1'):
            intf = Interface(device=dev1, name=name)
            self.assertIsInstance(intf, EthernetInterface,
                                  f'{name} should be EthernetInterface')
            self.assertIsInstance(intf, PhysicalInterface,
                                  f'{name} should be PhysicalInterface')

    def test_predictable_parent_interface(self):
        """enp0s3.100 resolves parent to enp0s3 via reconstruct()."""
        Genie.testbed = Testbed()
        dev1 = Device(name='linux-host', os='linux')
        parent = Interface(device=dev1, name='enp0s3')
        sub = Interface(device=dev1, name='enp0s3.100')
        self.assertEqual(sub.parent_interface, parent)

    # ------------------------------------------------------------------
    # IP alias (eth0:N) tests
    # ------------------------------------------------------------------

    def test_alias_factory(self):
        """Colon-notation names resolve to AliasInterface."""
        Genie.testbed = Testbed()
        dev1 = Device(name='linux-host', os='linux')
        for name in ('eth0:1', 'ens34:0', 'enp0s3:2', 'bond0:1'):
            intf = Interface(device=dev1, name=name)
            self.assertIsInstance(intf, AliasInterface,
                                  f'{name} should be AliasInterface')
            self.assertIsInstance(intf, VirtualInterface,
                                  f'{name} should be VirtualInterface')

    def test_alias_subintf_alias_factory(self):
        """Sub-interface alias eth0.100:1 resolves to AliasInterface (alias wins)."""
        Genie.testbed = Testbed()
        dev1 = Device(name='linux-host', os='linux')
        intf = Interface(device=dev1, name='eth0.100:1')
        self.assertIsInstance(intf, AliasInterface)

    def test_parsed_alias_simple(self):
        """eth0:1 parses into type/number/alias attributes."""
        p = ParsedInterfaceName('eth0:1')
        self.assertEqual(p.type, 'eth')
        self.assertEqual(p.number, '0')
        self.assertEqual(p.alias_sep, ':')
        self.assertEqual(p.alias, '1')
        self.assertIsNone(p.subintf)

    def test_parsed_alias_with_subintf(self):
        """eth0.100:1 parses subintf AND alias correctly."""
        p = ParsedInterfaceName('eth0.100:1')
        self.assertEqual(p.type, 'eth')
        self.assertEqual(p.number, '0')
        self.assertEqual(p.subintf_sep, '.')
        self.assertEqual(p.subintf, '100')
        self.assertEqual(p.alias_sep, ':')
        self.assertEqual(p.alias, '1')

    def test_parsed_predictable_alias(self):
        """Predictable name with alias: enp0s3:2 parses PCI fields + alias."""
        p = ParsedInterfaceName('enp0s3:2')
        self.assertEqual(p.type, 'ethernet')
        self.assertEqual(p.sub_type, 'pci')
        self.assertEqual(p.bus, 0)
        self.assertEqual(p.slot, 3)
        self.assertEqual(p.alias, '2')
        self.assertIsNone(p.subintf)

    def test_alias_number(self):
        """alias_number returns the alias index as int."""
        Genie.testbed = Testbed()
        dev1 = Device(name='linux-host', os='linux')
        intf = Interface(device=dev1, name='eth0:1')
        self.assertEqual(intf.alias_number, 1)

    def test_alias_parent_interface(self):
        """eth0:1 parent_interface resolves to eth0."""
        Genie.testbed = Testbed()
        dev1 = Device(name='linux-host', os='linux')
        parent = Interface(device=dev1, name='eth0')
        alias = Interface(device=dev1, name='eth0:1')
        self.assertEqual(alias.parent_interface, parent)

    def test_alias_subintf_parent_interface(self):
        """eth0.100:1 parent_interface resolves to eth0.100, not eth0."""
        Genie.testbed = Testbed()
        dev1 = Device(name='linux-host', os='linux')
        subintf = Interface(device=dev1, name='eth0.100')
        alias = Interface(device=dev1, name='eth0.100:1')
        self.assertEqual(alias.parent_interface, subintf)

    def test_alias_config_ipv4(self):
        """IPv4 on alias generates ip addr add ... dev <parent> label <alias>."""
        Genie.testbed = Testbed()
        dev1 = Device(name='linux-host', os='linux')
        intf = Interface(device=dev1, name='eth0:1')
        intf.ipv4 = '192.168.1.10/24'
        cfg = intf.build_config(apply=False)
        self.assertMultiLineEqual(str(cfg),
            'ip addr add 192.168.1.10/24 dev eth0 label eth0:1')

    def test_alias_unconfig_ipv4(self):
        """Unconfig of IPv4 alias generates ip addr del with label."""
        Genie.testbed = Testbed()
        dev1 = Device(name='linux-host', os='linux')
        intf = Interface(device=dev1, name='eth0:1')
        intf.ipv4 = '192.168.1.10/24'
        uncfg = intf.build_unconfig(apply=False, attributes='ipv4')
        self.assertMultiLineEqual(str(uncfg),
            'ip addr del 192.168.1.10/24 dev eth0 label eth0:1')

    def test_alias_no_mtu_or_enabled(self):
        """enabled and mtu on an alias produce no output."""
        Genie.testbed = Testbed()
        dev1 = Device(name='linux-host', os='linux')
        intf = Interface(device=dev1, name='eth0:1')
        intf.enabled = True
        intf.mtu = 9000
        cfg = intf.build_config(apply=False)
        self.assertMultiLineEqual(str(cfg), '')

    def test_alias_reconstruct(self):
        """reconstruct() round-trips alias names exactly."""
        for name in ('eth0:1', 'eth0.100:1', 'enp0s3:2', 'bond0:0'):
            p = ParsedInterfaceName(name)
            self.assertEqual(p.reconstruct(), name,
                             f'reconstruct() failed for {name!r}')

    def test_alias_predictable_parent_interface(self):
        """enp0s3:2 parent_interface resolves to enp0s3."""
        Genie.testbed = Testbed()
        dev1 = Device(name='linux-host', os='linux')
        parent = Interface(device=dev1, name='enp0s3')
        alias = Interface(device=dev1, name='enp0s3:2')
        self.assertEqual(alias.parent_interface, parent)


if __name__ == '__main__':
    unittest.main()
