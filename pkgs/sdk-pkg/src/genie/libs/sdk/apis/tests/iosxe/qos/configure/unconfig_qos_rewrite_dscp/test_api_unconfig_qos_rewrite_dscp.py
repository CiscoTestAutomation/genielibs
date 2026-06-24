import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.qos.configure import (
    unconfig_qos_rewrite_dscp
)


class TestUnconfigQosRewriteDscp(unittest.TestCase):

    def test_unconfig_qos_rewrite_dscp(self):
        device = Mock()

        result = unconfig_qos_rewrite_dscp(device)

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('no qos rewrite ip dscp',)
        )