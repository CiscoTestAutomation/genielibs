import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.policy_map.configure import configure_hqos_policer_map


class TestConfigureHqosPolicerMap(unittest.TestCase):

    def test_configure_hqos_policer_map(self):
        device = Mock()

        result = configure_hqos_policer_map(
            device,
            'cs3',
            'tc7',
            '5',
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            False
        )

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ([
                'policy-map cs3',
                'class tc7',
                'police cir percent 5 conform-action transmit'
            ],)
        )