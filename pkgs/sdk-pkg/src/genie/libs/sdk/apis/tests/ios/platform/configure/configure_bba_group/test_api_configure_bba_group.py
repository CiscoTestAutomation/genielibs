from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.ios.platform.configure import configure_bba_group


class TestConfigureBbaGroup(TestCase):

    def test_configure_bba_group(self):
        device = Mock()

        result = configure_bba_group(
            device,
            'global_100',
            '100',
            None,
            'minimum 1500 maximum 1700'
        )

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ([
                'bba-group pppoe global_100',
                'virtual-template 100',
                'tag ppp-max-payload minimum 1500 maximum 1700'
            ],)
        )

    def test_configure_bba_group_with_session_limits(self):
        device = Mock()

        result = configure_bba_group(
            device=device,
            name='100',
            vt_number='100',
            session_per_vlan_limit='1000',
            session_per_mac_limit='1000'
        )

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ([
                'bba-group pppoe 100',
                'virtual-template 100',
                'sessions per-vlan limit 1000',
                'sessions per-mac limit 1000'
            ],)
        )
