import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.qos.configure import (
    config_qos_rewrite_dscp
)


class TestConfigQosRewriteDscp(unittest.TestCase):

    def test_config_qos_rewrite_dscp(self):
        device = Mock()

        result = config_qos_rewrite_dscp(device)

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('qos rewrite ip dscp',)
        )