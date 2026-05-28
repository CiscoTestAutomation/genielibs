import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform.configure import unconfigure_broadband_aaa


class TestUnconfigureBroadbandAaa(unittest.TestCase):

    def test_unconfigure_broadband_aaa(self):
        device = Mock()

        result = unconfigure_broadband_aaa(device, 'server_1', 3)

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ([
                'no aaa authentication ppp default group server_1',
                'no aaa authorization network default group server_1',
                'no aaa authorization subscriber-service default group server_1',
                'no aaa accounting network default start-stop group server_1',
                'no aaa accounting update periodic 3'
            ],)
        )