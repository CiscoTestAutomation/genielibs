from unittest import TestCase
from genie.libs.sdk.apis.iosxe.interface.configure import unconfigure_tracking_object
from unittest.mock import Mock


class TestUnconfigureTrackingObject(TestCase):

    def test_unconfigure_tracking_object(self):
        self.device = Mock()
        result = unconfigure_tracking_object(self.device, '301')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['no track 301'],)
        )
