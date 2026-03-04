from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.multicast.configure import unconfigure_pim_register_source

class TestUnconfigurePimRegisterSource(TestCase):

    def test_unconfigure_pim_register_source(self):
        device = Mock()
        result = unconfigure_pim_register_source(device, 'Loopback101', 'red', False)
        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['no ip pim vrf red register-source Loopback101'],)
        )