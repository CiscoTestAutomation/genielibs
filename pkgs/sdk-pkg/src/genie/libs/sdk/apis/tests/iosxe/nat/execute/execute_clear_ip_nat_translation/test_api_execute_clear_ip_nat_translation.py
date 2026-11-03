from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.nat.execute import (
    execute_clear_ip_nat_translation,
)


class TestExecuteClearIpNatTranslation(TestCase):

    def test_clear_inside_and_outside_translation(self):
        device = Mock()
        device.execute.return_value = '%Translation not found'
        result = execute_clear_ip_nat_translation(
            device,
            inside_local_ip='1.1.1.1',
            inside_global_ip='2.2.2.2',
            outside_local_ip='3.3.3.3',
            outside_global_ip='5.5.5.5',
        )

        self.assertEqual(result, '%Translation not found')
        device.execute.assert_called_once_with(
            'clear ip nat translation inside 2.2.2.2 1.1.1.1 '
            'outside 3.3.3.3 5.5.5.5'
        )

    def test_clear_inside_translation(self):
        device = Mock()
        device.execute.return_value = '%Translation not found'
        result = execute_clear_ip_nat_translation(
            device,
            inside_local_ip='1.1.1.1',
            inside_global_ip='2.2.2.2',
        )

        self.assertEqual(result, '%Translation not found')
        device.execute.assert_called_once_with(
            'clear ip nat translation inside 2.2.2.2 1.1.1.1'
        )

    def test_clear_all_translations_forced(self):
        device = Mock()
        device.execute.return_value = ''
        result = execute_clear_ip_nat_translation(device, forced=True)

        self.assertEqual(result, '')
        device.execute.assert_called_once_with(
            'clear ip nat translation forced'
        )

    def test_clear_inside_translation_forced(self):
        device = Mock()
        device.execute.return_value = '%Translation not found'
        result = execute_clear_ip_nat_translation(
            device,
            forced=True,
            inside_local_ip='1.1.1.1',
            inside_global_ip='2.2.2.2',
        )

        self.assertEqual(result, '%Translation not found')
        device.execute.assert_called_once_with(
            'clear ip nat translation inside 2.2.2.2 1.1.1.1 forced'
        )

    def test_clear_inside_and_outside_translation_with_ports(self):
        device = Mock()
        device.execute.return_value = '%Translation not found'
        result = execute_clear_ip_nat_translation(
            device,
            udp=True,
            inside_local_ip='1.1.1.1',
            inside_global_ip='2.2.2.2',
            inside_local_port=456,
            inside_global_port=789,
            outside_local_ip='3.3.3.3',
            outside_global_ip='5.5.5.5',
            outside_local_port=345,
            outside_global_port=987,
        )

        self.assertEqual(result, '%Translation not found')
        device.execute.assert_called_once_with(
            'clear ip nat translation udp inside 2.2.2.2 789 '
            '1.1.1.1 456 outside 3.3.3.3 345 5.5.5.5 987'
        )

    def test_clear_inside_translation_tcp(self):
        device = Mock()
        device.execute.return_value = '%Translation not found'
        result = execute_clear_ip_nat_translation(
            device,
            tcp=True,
            inside_local_ip='1.1.1.1',
            inside_global_ip='2.2.2.2',
            inside_local_port=456,
            inside_global_port=789,
        )

        self.assertEqual(result, '%Translation not found')
        device.execute.assert_called_once_with(
            'clear ip nat translation tcp inside 2.2.2.2 789 '
            '1.1.1.1 456'
        )

    def test_clear_inside_translation_udp(self):
        device = Mock()
        device.execute.return_value = '%Translation not found'
        result = execute_clear_ip_nat_translation(
            device,
            udp=True,
            inside_local_ip='1.1.1.1',
            inside_global_ip='2.2.2.2',
            inside_local_port=456,
            inside_global_port=789,
        )

        self.assertEqual(result, '%Translation not found')
        device.execute.assert_called_once_with(
            'clear ip nat translation udp inside 2.2.2.2 789 '
            '1.1.1.1 456'
        )
