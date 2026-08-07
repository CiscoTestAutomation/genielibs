import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.scp.configure import (
    configure_scp_local_auth
)


class TestConfigureScpLocalAuth(unittest.TestCase):

    def test_configure_scp_local_auth(self):
        device = Mock()

        result = configure_scp_local_auth(
            device,
            'admin',
            'Bgl11lab@123',
            True
        )

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['aaa new-model',
              'aaa authentication login default local',
              'aaa authorization exec default local',
              'line vty 0 4',
              'transport input ssh',
              'username admin password Bgl11lab@123',
              'ip scp server enable'],)
        )