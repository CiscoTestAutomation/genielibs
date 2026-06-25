import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform.configure import unconfigure_service_internal


class TestUnconfigureServiceInternal(unittest.TestCase):

    def test_unconfigure_service_internal(self):
        device = Mock()

        result = unconfigure_service_internal(device)

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('no service internal',)
        )