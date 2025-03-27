from unittest import TestCase
from genie.libs.sdk.apis.iosxe.flow.configure import unconfigure_device_sampler
from unittest.mock import Mock


class TestUnconfigureDeviceSampler(TestCase):

    def test_unconfigure_device_sampler(self):
        self.device = Mock()
        result = unconfigure_device_sampler(self.device, 'sampler1')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['no sampler sampler1'],)
        )
