from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.aaa.configure import unconfigure_radius_interface


class TestUnconfigureRadiusInterface(TestCase):

    def test_unconfigure_radius_interface(self):
        device = Mock()
        device.configure.return_value = ""

        result = unconfigure_radius_interface(device, "Loopback0", "ipv4")
        self.assertIsNone(result)

        
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (["no ip radius source-interface Loopback0"],)
        )