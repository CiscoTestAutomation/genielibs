import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform.configure import unconfigure_virtual_service


class TestUnconfigureVirtualService(unittest.TestCase):

    def test_unconfigure_virtual_service(self):
        device = Mock()

        result = unconfigure_virtual_service(
            device,
            'UTD'
        )

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('no virtual-service UTD',)
        )