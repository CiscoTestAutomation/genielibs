import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.scp.configure import (
    unconfigure_scp_local_auth
)


class TestUnconfigureScpLocalAuth(unittest.TestCase):

    def test_unconfigure_scp_local_auth(self):
        device = Mock()

        result = unconfigure_scp_local_auth(
            device,
            'admin',
            'Bgl11lab@123',
            True
        )

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['aaa new-model',
              'no aaa authentication login default local',
              'no aaa authorization exec default local',
              'line vty 0 4',
              'transport input none',
              'no username admin password Bgl11lab@123',
              'no ip scp server enable'],)
        )