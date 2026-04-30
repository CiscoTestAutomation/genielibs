from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform.configure import configure_broadband_aaa


class TestConfigureBroadbandAaa(TestCase):

    def test_configure_broadband_aaa(self):
        device = Mock()
        result = configure_broadband_aaa(
            device,
            'server_1',
            3
        )
        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ([
                'aaa authentication ppp default group server_1',
                'aaa authorization network default group server_1',
                'aaa authorization subscriber-service default group server_1',
                'aaa accounting network default start-stop group server_1',
                'aaa accounting update periodic 3'
            ],)
        )