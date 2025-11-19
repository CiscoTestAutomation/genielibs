from unittest import TestCase
from genie.libs.sdk.apis.iosxe.cts.configure import unconfigure_device_sgt
from unittest.mock import Mock


class TestUnconfigureDeviceSgt(TestCase):

    def test_unconfigure_device_sgt(self):
        self.device = Mock()
        result = unconfigure_device_sgt(self.device)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['no cts sgt'],)
        )
