import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.qos.configure import (
    configure_auto_qos
)


class TestConfigureAutoQos(unittest.TestCase):

    def test_configure_auto_qos(self):
        device = Mock()

        result = configure_auto_qos(
            device,
            'Hu1/0/3',
            'trust',
            'dscp'
        )

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['interface Hu1/0/3',
              'auto qos trust dscp'],)
        )