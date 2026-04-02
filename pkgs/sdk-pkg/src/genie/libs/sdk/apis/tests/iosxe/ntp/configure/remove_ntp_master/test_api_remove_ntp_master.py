from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.ntp.configure import remove_ntp_master

class TestRemoveNtpMaster(TestCase):

    def test_remove_ntp_master(self):
        device = Mock()
        result = remove_ntp_master(device)
        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
          (['no ntp master'],)
        )