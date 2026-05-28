import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform.configure import configure_virtual_service_vnic_gateway_guest_ip_address


class TestConfigureVirtualServiceVnicGatewayGuestIpAddress(unittest.TestCase):

    def test_configure_virtual_service_vnic_gateway_guest_ip_address(self):
        device = Mock()

        result = configure_virtual_service_vnic_gateway_guest_ip_address(
            device,
            'VirtualPortGroup1',
            '16.18.27.2',
            '255.255.255.0',
            'enable',
            '228.10.10.2'
        )

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ([
                'interface VirtualPortGroup1',
                'ip address 16.18.27.2 255.255.255.0',
                'no shut',
                'virtual-service enable',
                'vnic gateway VirtualPortGroup1',
                'guest ip address 228.10.10.2',
                'exit',
                'activate'
            ],)
        )