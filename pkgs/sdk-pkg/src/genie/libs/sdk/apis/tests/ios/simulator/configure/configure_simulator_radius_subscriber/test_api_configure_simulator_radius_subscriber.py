from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.ios.simulator.configure import configure_simulator_radius_subscriber


class TestConfigureSimulatorRadiusSubscriber(TestCase):

    def test_configure_simulator_radius_subscriber_basic(self):
        self.device = Mock()
        configure_simulator_radius_subscriber(self.device, 8, 'framed')
        self.device.configure.assert_called_once_with(
            [
                "no simulator radius subscriber 8",
                "simulator radius subscriber 8",
                " service framed",
            ]
        )

    def test_configure_simulator_radius_subscriber_with_attributes(self):
        self.device = Mock()
        configure_simulator_radius_subscriber(
            self.device, 9, 'framed',
            attributes=[{'id': 27, 'type': 'numeric', 'value': 60}]
        )
        self.device.configure.assert_called_once_with(
            [
                "no simulator radius subscriber 9",
                "simulator radius subscriber 9",
                " service framed",
                " attribute 27 numeric 60",
            ]
        )

    def test_configure_simulator_radius_subscriber_without_remove(self):
        self.device = Mock()
        configure_simulator_radius_subscriber(
            self.device, 10, 'framed', remove_first=False
        )
        self.device.configure.assert_called_once_with(
            [
                "simulator radius subscriber 10",
                " service framed",
            ]
        )

    def test_configure_simulator_radius_subscriber_with_vsas(self):
        self.device = Mock()
        configure_simulator_radius_subscriber(
            self.device, 11, 'framed',
            vsas=['cisco generic 1 string "subscriber:accounting-list=acct1"',
                  'cisco generic 250 string "service1" prefix "A"']
        )
        self.device.configure.assert_called_once_with(
            [
                "no simulator radius subscriber 11",
                "simulator radius subscriber 11",
                " service framed",
                ' vsa cisco generic 1 string "subscriber:accounting-list=acct1"',
                ' vsa cisco generic 250 string "service1" prefix "A"',
            ]
        )

    def test_configure_simulator_radius_subscriber_with_authentication(self):
        self.device = Mock()
        configure_simulator_radius_subscriber(
            self.device, 30, 'framed',
            authentication='user1 CoA secret123',
            vsas=['cisco generic 252 binary 01'],
            attributes=[{'id': 44, 'type': 'string', 'value': '0000000C'}]
        )
        self.device.configure.assert_called_once_with(
            [
                "no simulator radius subscriber 30",
                "simulator radius subscriber 30",
                " service framed",
                " authentication user1 CoA secret123",
                " vsa cisco generic 252 binary 01",
                " attribute 44 string 0000000C",
            ]
        )

    def test_configure_simulator_radius_subscriber_no_service(self):
        self.device = Mock()
        configure_simulator_radius_subscriber(
            self.device, 18,
            vsas=['cisco generic 251 string "service6"'],
            attributes=[{'id': 27, 'type': 'numeric', 'value': 80}]
        )
        self.device.configure.assert_called_once_with(
            [
                "no simulator radius subscriber 18",
                "simulator radius subscriber 18",
                ' vsa cisco generic 251 string "service6"',
                " attribute 27 numeric 80",
            ]
        )

    def test_configure_simulator_radius_subscriber_with_framed_prefix(self):
        self.device = Mock()
        configure_simulator_radius_subscriber(
            self.device, 8, 'framed',
            framed_prefix='2001:db8:1::/64'
        )
        self.device.configure.assert_called_once_with(
            [
                "no simulator radius subscriber 8",
                "simulator radius subscriber 8",
                " service framed",
                " framed ipv6 prefix 2001:db8:1::/64",
            ]
        )

    def test_configure_simulator_radius_subscriber_negate_framed_prefix(self):
        self.device = Mock()
        configure_simulator_radius_subscriber(
            self.device, 8, 'framed',
            framed_prefix='2001:db8:1::/64', negate=True,
            remove_first=False
        )
        self.device.configure.assert_called_once_with(
            [
                "simulator radius subscriber 8",
                " service framed",
                " no framed ipv6 prefix 2001:db8:1::/64",
            ]
        )

    def test_configure_simulator_radius_subscriber_negate_attribute(self):
        self.device = Mock()
        configure_simulator_radius_subscriber(
            self.device, 8, 'framed',
            attributes=[{'id': 100, 'type': 'string', 'value': '"pool1"'}],
            negate=True, remove_first=False
        )
        self.device.configure.assert_called_once_with(
            [
                "simulator radius subscriber 8",
                " service framed",
                ' no attribute 100 string "pool1"',
            ]
        )
