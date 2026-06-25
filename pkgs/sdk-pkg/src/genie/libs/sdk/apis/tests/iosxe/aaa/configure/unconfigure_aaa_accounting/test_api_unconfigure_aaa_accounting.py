import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.aaa.configure import unconfigure_aaa_accounting
from unicon.core.errors import SubCommandFailure


class TestUnconfigureAaaAccounting(unittest.TestCase):

    def test_unconfigure_network_named_list(self):
        device = Mock()
        unconfigure_aaa_accounting(
            device, 'network', acct_list='ACCT_LIST',
            record_type='start-stop', methods=['group RADIUS_GRP'],
        )
        device.configure.assert_called_once_with(
            'no aaa accounting network ACCT_LIST start-stop group RADIUS_GRP'
        )

    def test_unconfigure_system_default(self):
        device = Mock()
        unconfigure_aaa_accounting(
            device, 'system', acct_list='default',
            record_type='start-stop', methods=['group radius'],
        )
        device.configure.assert_called_once_with(
            'no aaa accounting system default start-stop group radius'
        )

    def test_unconfigure_update_newinfo(self):
        device = Mock()
        unconfigure_aaa_accounting(device, 'update', extras='newinfo')
        device.configure.assert_called_once_with(
            'no aaa accounting update newinfo'
        )

    def test_unconfigure_exec_default(self):
        device = Mock()
        unconfigure_aaa_accounting(device, 'exec', acct_list='default')
        device.configure.assert_called_once_with(
            'no aaa accounting exec default'
        )

    def test_unconfigure_network_default(self):
        device = Mock()
        unconfigure_aaa_accounting(
            device, 'network', acct_list='default'
        )
        device.configure.assert_called_once_with(
            'no aaa accounting network default'
        )

    def test_unconfigure_system_default_no_methods(self):
        device = Mock()
        unconfigure_aaa_accounting(
            device, 'system', acct_list='default'
        )
        device.configure.assert_called_once_with(
            'no aaa accounting system default'
        )

    def test_unconfigure_update_periodic(self):
        device = Mock()
        unconfigure_aaa_accounting(
            device, 'update', extras=['periodic', '5']
        )
        device.configure.assert_called_once_with(
            'no aaa accounting update periodic 5'
        )

    def test_unconfigure_failure(self):
        device = Mock()
        device.configure.side_effect = SubCommandFailure('error')
        with self.assertRaises(SubCommandFailure):
            unconfigure_aaa_accounting(
                device, 'network', acct_list='ACCT_LIST',
                record_type='start-stop', methods=['group RADIUS_GRP'],
            )


if __name__ == '__main__':
    unittest.main()
