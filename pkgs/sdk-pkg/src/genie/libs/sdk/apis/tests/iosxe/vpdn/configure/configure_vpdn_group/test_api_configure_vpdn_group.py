from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.vpdn.configure import configure_vpdn_group


class TestConfigureVpdnGroup(TestCase):

    def test_configure_request_dialin_group(self):
        device = Mock()
        device.configure.return_value = None

        configure_vpdn_group(
            device,
            vpdn_group_number="scale_n1",
            request_dialin=True,
            domain="cisco.com",
            initiate_to="200.0.0.1",
            local_name="LAC",
            tunnel_hello_interval="0",
            tunnel_password="cisco",
            tunnel_receive_window="8",
        )

        expected_config = [
            "vpdn-group scale_n1",
            "request-dialin",
            "protocol l2tp",
            "domain cisco.com",
            "initiate-to ip 200.0.0.1",
            "local name LAC",
            "l2tp tunnel hello 0",
            "l2tp tunnel password 0 cisco",
            "l2tp tunnel receive-window 8",
        ]

        self.assertTrue(device.configure.called)
        call_args = device.configure.call_args_list[0][0][0]
        self.assertEqual(call_args, expected_config)

    def test_configure_accept_dialin_group_backwards_compatible(self):
        device = Mock()
        device.configure.return_value = None

        configure_vpdn_group(
            device,
            True,
            "11",
            False,
            True,
            "cisco.com",
            "9.9.9.1",
            "0",
            "cisco",
            "1",
            "lns1",
        )

        expected_config = [
            "vpdn enable",
            "vpdn authen-before-forward",
            "vpdn-group 11",
            "accept-dialin",
            "protocol l2tp",
            "virtual-template 1",
            "local name lns1",
            "l2tp tunnel hello 0",
            "l2tp tunnel password 0 cisco",
        ]

        self.assertTrue(device.configure.called)
        call_args = device.configure.call_args_list[0][0][0]
        self.assertEqual(call_args, expected_config)

    def test_configure_request_dialin_group_with_prioritized_initiate_to_entries(
        self,
    ):
        device = Mock()
        device.configure.return_value = None

        configure_vpdn_group(
            device,
            vpdn_group_number="scale_n1",
            request_dialin=True,
            initiate_to_entries=[
                {"ip": "10.1.1.2", "priority": "1"},
                {"ip": "10.1.1.1", "priority": "2"},
            ],
            busy_timeout="30",
        )

        expected_config = [
            "vpdn-group scale_n1",
            "request-dialin",
            "protocol l2tp",
            "initiate-to ip 10.1.1.2 priority 1",
            "initiate-to ip 10.1.1.1 priority 2",
            "l2tp tunnel busy timeout 30",
        ]

        self.assertTrue(device.configure.called)
        call_args = device.configure.call_args_list[0][0][0]
        self.assertEqual(call_args, expected_config)
