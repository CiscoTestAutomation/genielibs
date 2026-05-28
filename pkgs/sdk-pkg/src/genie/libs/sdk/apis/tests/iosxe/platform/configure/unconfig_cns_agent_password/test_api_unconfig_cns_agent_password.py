import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform.configure import unconfig_cns_agent_password


class TestUnconfigCnsAgentPassword(unittest.TestCase):

    def test_unconfig_cns_agent_password(self):
        device = Mock()

        result = unconfig_cns_agent_password(device, '')

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('no cns password',)
        )