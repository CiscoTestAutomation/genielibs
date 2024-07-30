#!/usr/bin/env python

# Python
import unittest
from unittest.mock import Mock

# Genie package
from genie.tests.conf import TestCase
from genie.conf import Genie
from genie.conf.base import Testbed, Device, Link, Interface

# Genie Conf
from genie.libs.conf.urpf import Urpf
from genie.libs.conf.urpf.ipverify import IpVerify
from genie.libs.conf.urpf.ipv6verify import Ipv6Verify


class test_urpf(TestCase):

    def test_urpf_strict_config(self):

        # For failures
        self.maxDiff = None

        # Set testbed
        Genie.testbed = testbed = Testbed()
        dev1 = Device(testbed=testbed, name="PE1", os="nxos")
        # Create Interface object
        intf1 = Interface(name="Ethernet1/1", device=dev1)

        # Create urpf object
        urpf = Urpf()
        urpf.device_attr[dev1].enabled = True

        # add interface configuration to urpf
        ip_verify1 = IpVerify(device=dev1)
        ip_verify1.ip_verify_strict = True
        urpf.device_attr[dev1].interface_attr[intf1].add_ip_urpf_key(ip_verify1)

        # add interface configuration to urpf
        ipv6_verify1 = Ipv6Verify(device=dev1)
        ipv6_verify1.ipv6_verify_strict = True
        ipv6_verify1.ipv6_strict_allow_vnihosts = True
        urpf.device_attr[dev1].interface_attr[intf1].add_ipv6_urpf_key(ipv6_verify1)
        dev1.add_feature(urpf)

        # Build config
        cfgs = urpf.build_config(apply=False)
        # Check config strings built correctly
        self.assertMultiLineEqual(
            str(cfgs[dev1.name]),
            "\n".join(
                [
                    "no system urpf disable",
                    "interface Ethernet1/1",
                    " ip verify unicast source reachable-via rx",
                    " ipv6 verify unicast source reachable-via rx allow vni-hosts",
                    " exit",
                ]
            ),
        )

        # Unconfig
        urpf = urpf.build_unconfig(apply=False)

        # Check unconfig strings built correctly
        self.assertMultiLineEqual(
            str(urpf[dev1.name]),
            "\n".join(
                [
                    "system urpf disable",
                ]
            ),
        )

    def test_urpf_loose_config(self):

        # For failures
        self.maxDiff = None

        # Set testbed
        Genie.testbed = testbed = Testbed()
        dev1 = Device(testbed=testbed, name="PE1", os="nxos")
        # Create Interface object
        intf1 = Interface(name="Ethernet1/1", device=dev1)

        # Create urpf object
        urpf = Urpf()
        urpf.device_attr[dev1].enabled = True

        # add interface configuration to urpf
        ip_verify1 = IpVerify(device=dev1)
        ip_verify1.ip_verify_loose = True
        urpf.device_attr[dev1].interface_attr[intf1].add_ip_urpf_key(ip_verify1)

        # add interface configuration to urpf
        ipv6_verify1 = Ipv6Verify(device=dev1)
        ipv6_verify1.ipv6_verify_loose = True
        ipv6_verify1.ipv6_loose_allow_default = True
        urpf.device_attr[dev1].interface_attr[intf1].add_ipv6_urpf_key(ipv6_verify1)
        dev1.add_feature(urpf)

        # Build config
        cfgs = urpf.build_config(apply=False)
        # Check config strings built correctly
        self.assertMultiLineEqual(
            str(cfgs[dev1.name]),
            "\n".join(
                [
                    "no system urpf disable",
                    "interface Ethernet1/1",
                    " ip verify unicast source reachable-via any",
                    " ipv6 verify unicast source reachable-via any allow-default",
                    " exit",
                ]
            ),
        )
        partial_uncfg1 = urpf.build_unconfig(
            apply=False, attributes={"device_attr": {"*": {"interface_attr": "*"}}}
        )

        self.assertMultiLineEqual(
            str(partial_uncfg1[dev1.name]),
            "\n".join(
                [
                    "interface Ethernet1/1",
                    " no ip verify unicast source reachable-via any",
                    " no ipv6 verify unicast source reachable-via any allow-default",
                    " exit",
                ]
            ),
        )


if __name__ == "__main__":
    unittest.main()
