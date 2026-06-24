import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.qos.configure import (
    configure_auto_qos_global
)


class TestConfigureAutoQosGlobal(unittest.TestCase):

    def test_configure_auto_qos_global(self):
        device = Mock()

        result = configure_auto_qos_global(
            device,
            'compact'
        )

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('auto qos global compact',)
        )