import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform.configure import unconfigure_virtual_service_activate


class TestUnconfigureVirtualServiceActivate(unittest.TestCase):

    def test_unconfigure_virtual_service_activate(self):
        device = Mock()

        result = unconfigure_virtual_service_activate(
            device,
            'UTD'
        )

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ([
                'virtual-service UTD',
                'no activate'
            ],)
        )