#!/usr/bin/env python

# Python
import unittest
from unittest.mock import Mock

# Genie package
from genie.tests.conf import TestCase
from genie.conf import Genie
from genie.conf.base import Testbed, Device

# Genie Conf
from genie.libs.conf.service_acceleration import ServiceAcceleration
from genie.libs.conf.service_acceleration.service_vrf import ServiceVrf


class test_service_acceleration(TestCase):

    def test_service_acceleration_feature(self):

        # For failures
        self.maxDiff = None

        # Set testbed
        Genie.testbed = testbed = Testbed()
        dev1 = Device(testbed=testbed, name="PE1", os="nxos")

        # Create service acceleration object
        serv_acc= ServiceAcceleration()
        serv_acc.device_attr[dev1].enabled = True

        # add feature to device
        dev1.add_feature(serv_acc)

        # Build config
        cfgs = serv_acc.build_config(apply=False)
        # Check config strings built correctly
        self.assertMultiLineEqual(
            str(cfgs[dev1.name]),
            "\n".join(
                [
                    "feature service-acceleration",
                ]
            ),
        )

        # Unconfig
        serv_acc = serv_acc.build_unconfig(apply=False)

        # Check unconfig strings built correctly
        self.assertMultiLineEqual(
            str(serv_acc[dev1.name]),
            "\n".join(
                [
                    "no feature service-acceleration",
                ]
            ),
        )

    def test_service_acceleration_service_system_attributes(self):

        # For failures
        self.maxDiff = None

        # Set testbed
        Genie.testbed = testbed = Testbed()
        dev1 = Device(testbed=testbed, name="PE1", os="nxos")

        # Create service acceleration object
        serv_acc= ServiceAcceleration(service_vendor='hypershield')
        serv_acc.device_attr[dev1].source_interface = 'loopback1'
        serv_acc.device_attr[dev1].peer_ip = '1.2.3.4'
        serv_acc.device_attr[dev1].peer_interface = 'Eth1/2'
        serv_acc.device_attr[dev1].controller_token = '{"some dynamically generated token"}'
        serv_acc.device_attr[dev1].https_proxy_username = 'admin'
        serv_acc.device_attr[dev1].https_proxy_password = 'password'

        # add feature to device
        dev1.add_feature(serv_acc)

        # Build config
        cfgs = serv_acc.build_config(apply=False)
        # Check config strings built correctly
        self.assertMultiLineEqual(
            str(cfgs[dev1.name]),
            "\n".join(
                [
                    "service system hypershield\n"
                    " source-interface loopback1\n"
                    " service peer ip address 1.2.3.4 interface Eth1/2\n"
                    ' controller connection-token {"some dynamically generated token"}\n'
                    " https-proxy username admin password password\n"
                    " exit"
                ]
            ),
        )

        partial_uncfg1 = serv_acc.build_unconfig(
            apply=False, attributes={"device_attr": {"*":{"source_interface": None}}}
        )

        self.assertMultiLineEqual(
            str(partial_uncfg1[dev1.name]),
            "\n".join(
                [
                'service system hypershield\n'
                ' no source-interface loopback1\n'
                ' exit'
                ]
            ),
        )

        serv_acc.device_attr[dev1].enabled = False
        uncfgs = serv_acc.build_unconfig(apply=False)
        self.assertMultiLineEqual(
            str(uncfgs[dev1.name]),
            "\n".join(
                [
                'no service system hypershield'
                ]
            ),
        )

    def test_service_acceleration_service_attributes(self):

        # For failures
        self.maxDiff = None

        # Set testbed
        Genie.testbed = testbed = Testbed()
        dev1 = Device(testbed=testbed, name="PE1", os="nxos")

        # Create service acceleration object
        serv_acc= ServiceAcceleration(service_vendor='hypershield')
        serv_acc.device_attr[dev1].source_interface = 'loopback1'
        serv_acc.device_attr[dev1].service_attr['firewall'].in_service = True

        # Add service vrf1 configuration to firewall
        vrf1 = ServiceVrf(device=dev1)
        vrf1.service_vrf_name = 'vrfoci'
        serv_acc.device_attr[dev1].service_attr['firewall'].add_servicevrf_key(vrf1)
        # Add service vrf2 configuration to firewall
        vrf2 = ServiceVrf(device=dev1)
        vrf2.service_vrf_name = 'vrfazure'
        vrf2.module_affinity = 1
        serv_acc.device_attr[dev1].service_attr['firewall'].add_servicevrf_key(vrf2)


        # add feature to device
        dev1.add_feature(serv_acc)

        # Build config
        cfgs = serv_acc.build_config(apply=False)
        # Check config strings built correctly
        self.assertMultiLineEqual(
            str(cfgs[dev1.name]),
            "\n".join(
                [
                'service system hypershield\n'
                ' source-interface loopback1\n'
                ' service firewall\n'
                '  in-service\n'
                '  vrf vrfazure module-affinity 1\n'
                '  vrf vrfoci module-affinity dynamic\n'
                '  exit\n'
                ' exit'
                ]
            ),
        )

        partial_uncfg3 = serv_acc.build_unconfig(
                            apply=False,
                            attributes={'device_attr': {'*': {'service_attr':
                                {'*': 'servicevrf_keys'}}}})

        self.assertMultiLineEqual(
            str(partial_uncfg3[dev1.name]),
            "\n".join(
                [
                'service system hypershield\n'
                ' service firewall\n'
                '  no vrf vrfazure module-affinity 1\n'
                '  no vrf vrfoci module-affinity dynamic\n'
                '  exit\n'
                ' exit'
                ]
            ),
        )

        firewall_uncfg = serv_acc.build_unconfig(
                            apply=False,
                            attributes={'device_attr': {'*': {'service_attr':'*'}}})

        self.assertMultiLineEqual(
            str(firewall_uncfg[dev1.name]),
            "\n".join(
                [
                'service system hypershield\n'
                ' no service firewall\n'
                ' exit'
                ]
            ),
        )

    def test_service_acceleration_all_attributes(self):

        # For failures
        self.maxDiff = None

        # Set testbed
        Genie.testbed = testbed = Testbed()
        dev1 = Device(testbed=testbed, name="PE1", os="nxos")

        # Create service acceleration object
        serv_acc= ServiceAcceleration(service_vendor='hypershield')
        serv_acc.device_attr[dev1].enabled = True
        serv_acc.device_attr[dev1].source_interface = 'loopback1'
        serv_acc.device_attr[dev1].peer_ip = '1.2.3.4'
        serv_acc.device_attr[dev1].peer_interface = 'Eth1/2'
        serv_acc.device_attr[dev1].controller_token = '{"some dynamically generated token"}'
        serv_acc.device_attr[dev1].https_proxy_username = 'admin'
        serv_acc.device_attr[dev1].https_proxy_password = 'password'
        serv_acc.device_attr[dev1].https_proxy = 'proxy.esl.cisco.com'
        serv_acc.device_attr[dev1].https_proxy_port = 8080
        serv_acc.device_attr[dev1].service_attr['firewall'].in_service = True

        # Add service vrf1 configuration to firewall
        vrf1 = ServiceVrf(device=dev1)
        vrf1.service_vrf_name = 'vrfaws'
        serv_acc.device_attr[dev1].service_attr['firewall'].add_servicevrf_key(vrf1)
        # Add service vrf2 configuration to firewall
        vrf2 = ServiceVrf(device=dev1)
        vrf2.service_vrf_name = 'vrfazure'
        vrf2.module_affinity = 1
        serv_acc.device_attr[dev1].service_attr['firewall'].add_servicevrf_key(vrf2)

        # add feature to device
        dev1.add_feature(serv_acc)

        # Build config
        cfgs = serv_acc.build_config(apply=False)
        # Check config strings built correctly
        self.assertMultiLineEqual(
            str(cfgs[dev1.name]),
            "\n".join(
                [
                    "feature service-acceleration\n"
                    "service system hypershield\n"
                    " source-interface loopback1\n"
                    " service peer ip address 1.2.3.4 interface Eth1/2\n"
                    ' controller connection-token {"some dynamically generated token"}\n'
                    " https-proxy username admin password password\n"
                    " https-proxy proxy.esl.cisco.com port 8080\n"
                    " service firewall\n"
                    "  in-service\n"
                    "  vrf vrfaws module-affinity dynamic\n"
                    "  vrf vrfazure module-affinity 1\n"
                    "  exit\n"
                    " exit"
                ]
            ),
        )

        # remove in service under firewall attribute
        remove_in_service = serv_acc.build_unconfig(
                            apply=False,
                            attributes={'device_attr': {'*': {'service_attr':{'*': {'in_service': None}}}}})

        self.assertMultiLineEqual(
            str(remove_in_service[dev1.name]),
            "\n".join(
                [
                'service system hypershield\n'
                ' service firewall\n'
                '  no in-service\n'
                '  exit\n'
                ' exit'
                ]
            ),
        )
        # remove 1 vrf under firewall
        partial_uncfg3 = serv_acc.build_unconfig(
                            apply=False,
                            attributes={'device_attr': {'*': {'service_attr':{'*': {'servicevrf_keys': vrf2}}}}})

        self.assertMultiLineEqual(
            str(partial_uncfg3[dev1.name]),
            "\n".join(
                [
                'service system hypershield\n'
                ' service firewall\n'
                '  no vrf vrfazure module-affinity 1\n'
                '  exit\n'
                ' exit'
                ]
            ),
        )

        serv_acc.device_attr[dev1].enabled = False
        uncfgs = serv_acc.build_unconfig(apply=False)
        self.assertMultiLineEqual(
            str(uncfgs[dev1.name]),
            "\n".join(
                [
                'no service system hypershield'
                ]
            ),
        )

if __name__ == "__main__":
    unittest.main()
