import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.aaa.configure import configure_aaa_accounting
from unicon.core.errors import SubCommandFailure


class TestConfigureAaaAccounting(unittest.TestCase):

    def test_configure_network_named_list(self):
        device = Mock()
        configure_aaa_accounting(
            device, 'network', acct_list='ACCT_LIST',
            record_type='start-stop', methods=['group RADIUS_GRP'],
        )
        device.configure.assert_called_once_with(
            'aaa accounting network ACCT_LIST start-stop group RADIUS_GRP'
        )

    def test_configure_system_default(self):
        device = Mock()
        configure_aaa_accounting(
            device, 'system', acct_list='default',
            record_type='start-stop', methods=['group radius'],
        )
        device.configure.assert_called_once_with(
            'aaa accounting system default start-stop group radius'
        )

    def test_configure_update_newinfo(self):
        device = Mock()
        configure_aaa_accounting(device, 'update', extras='newinfo')
        device.configure.assert_called_once_with(
            'aaa accounting update newinfo'
        )

    def test_configure_update_periodic(self):
        device = Mock()
        configure_aaa_accounting(
            device, 'update', extras=['periodic', '5']
        )
        device.configure.assert_called_once_with(
            'aaa accounting update periodic 5'
        )

    def test_configure_nested(self):
        device = Mock()
        configure_aaa_accounting(device, 'nested')
        device.configure.assert_called_once_with('aaa accounting nested')

    def test_configure_include(self):
        device = Mock()
        configure_aaa_accounting(device, 'include')
        device.configure.assert_called_once_with('aaa accounting include')

    def test_configure_jitter_maximum(self):
        device = Mock()
        configure_aaa_accounting(
            device, 'jitter', extras=['maximum', '5']
        )
        device.configure.assert_called_once_with(
            'aaa accounting jitter maximum 5'
        )

    def test_configure_exec_named_list_no_record_type(self):
        device = Mock()
        configure_aaa_accounting(
            device, 'exec', acct_list='default'
        )
        device.configure.assert_called_once_with(
            'aaa accounting exec default'
        )

    def test_configure_failure(self):
        device = Mock()
        device.configure.side_effect = SubCommandFailure('error')
        with self.assertRaises(SubCommandFailure):
            configure_aaa_accounting(
                device, 'network', acct_list='ACCT_LIST',
                record_type='start-stop', methods=['group RADIUS_GRP'],
            )


if __name__ == '__main__':
    unittest.main()
