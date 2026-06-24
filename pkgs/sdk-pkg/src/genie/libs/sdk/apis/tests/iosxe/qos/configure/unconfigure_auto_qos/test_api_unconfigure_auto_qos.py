import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.qos.configure import (
    unconfigure_auto_qos
)


class TestUnconfigureAutoQos(unittest.TestCase):

    def test_unconfigure_auto_qos(self):
        device = Mock()

        result = unconfigure_auto_qos(
            device,
            'Hu1/0/3',
            'trust',
            'dscp'
        )

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['interface Hu1/0/3',
              'no auto qos trust dscp'],)
        )