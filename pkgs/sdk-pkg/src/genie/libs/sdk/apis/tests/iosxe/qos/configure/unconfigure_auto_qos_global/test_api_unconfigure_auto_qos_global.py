import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.qos.configure import (
    unconfigure_auto_qos_global
)


class TestUnconfigureAutoQosGlobal(unittest.TestCase):

    def test_unconfigure_auto_qos_global(self):
        device = Mock()

        result = unconfigure_auto_qos_global(
            device,
            'compact'
        )

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('no auto qos global compact',)
        )