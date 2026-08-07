from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.interface.configure import configure_virtual_template


class TestConfigureVirtualTemplate(TestCase):

    def setUp(self):
        self.device = Mock()
        self.device.is_connected.return_value = True
        self.device.configure.return_value = None

    def assert_configured(self, expected_config):
        self.device.configure.assert_called_once_with(expected_config)

    def test_configure_virtual_template(self):
        result = configure_virtual_template(
            self.device,
            '100',
            'Loopback2',
            False,
            None,
            False,
            False,
            0,
            0,
            '',
            '',
            False,
            False,
            None,
            'ipv6_local_pool',
        )

        expected_config = [
            'interface Virtual-Template 100',
            'ip unnumbered Loopback2',
            'peer default ipv6 pool ipv6_local_pool',
        ]
        self.assertIsNone(result)
        self.assert_configured(expected_config)

    def test_configure_virtual_template_with_pap_username(self):
        result = configure_virtual_template(
            self.device,
            '101',
            no_ppp_authentication=True,
            pap_username='USER',
            pap_password='cisco',
            pap_password_type='0',
        )

        expected_config = [
            'interface Virtual-Template 101',
            'no ppp authentication',
            'ppp pap sent-username USER password 0 cisco',
        ]
        self.assertIsNone(result)
        self.assert_configured(expected_config)

    def test_configure_virtual_template_with_chap_hostname(self):
        result = configure_virtual_template(
            self.device,
            '102',
            auth=True,
            authentication='chap',
            chap_hostname='USER',
            chap_password='cisco',
            chap_password_type='0',
        )

        expected_config = [
            'interface Virtual-Template 102',
            'ppp authentication chap',
            'ppp chap hostname USER',
            'ppp chap password 0 cisco',
        ]
        self.assertIsNone(result)
        self.assert_configured(expected_config)

    def test_configure_virtual_template_with_extended_options(self):
        result = configure_virtual_template(
            self.device,
            '103',
            negotiated=True,
            auth=True,
            authentication='chap',
            mtu=1492,
            pool_name='LOCAL_POOL',
            pool_local=True,
            chap_hostname='USER@example.com',
            chap_password='cisco',
            chap_splitnames=True,
            timeout_ncp=30,
            timeout_idle=60,
            no_logging_event_link_status=True,
        )

        expected_config = [
            'interface Virtual-Template 103',
            'ip address negotiated',
            'no logging event link-status',
            'ppp authentication chap',
            'ppp chap hostname USER@example.com',
            'ppp chap password 0 cisco',
            'ppp chap splitnames',
            'ppp timeout ncp 30',
            'ppp timeout idle 60',
            'mtu 1492',
            'peer default ip address pool local LOCAL_POOL',
        ]
        self.assertIsNone(result)
        self.assert_configured(expected_config)

    def test_configure_virtual_template_with_vrf_and_no_ip_address(self):
        result = configure_virtual_template(
            self.device,
            '104',
            vrf_name='VRF101',
            no_ip_address=True,
            auth=True,
            authentication='chap',
        )

        expected_config = [
            'interface Virtual-Template 104',
            'ip vrf forwarding VRF101',
            'no ip address',
            'ppp authentication chap',
        ]
        self.assertIsNone(result)
        self.assert_configured(expected_config)

    def test_configure_virtual_template_with_mpls_encap(self):
        result = configure_virtual_template(
            self.device,
            100,
            'loopback1',
            True,
            'chap',
            True,
            True,
            1400,
            '30',
            '1500',
            '1460',
            True,
            True,
            'v4_pool',
            'v6_pool',
            True,
            'explicit-null',
        )

        expected_config = [
            'interface Virtual-Template 100',
            'ip unnumbered loopback1',
            'ppp authentication chap',
            'ip tcp adjust-mss 1400',
            'load-interval 30',
            'mtu 1500',
            'ipv6 mtu 1460',
            'no ip redirects',
            'no peer default ip address',
            'peer default ip address pool v4_pool',
            'peer default ipv6 pool v6_pool',
            'mpls ip encapsulate explicit-null',
        ]
        self.assertIsNone(result)
        self.assert_configured(expected_config)
