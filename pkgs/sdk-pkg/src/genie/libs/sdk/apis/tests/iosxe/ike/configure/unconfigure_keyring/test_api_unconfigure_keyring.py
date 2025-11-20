from unittest import TestCase
from genie.libs.sdk.apis.iosxe.ike.configure import unconfigure_keyring
from unittest.mock import Mock


class TestUnconfigureKeyring(TestCase):

    def test_unconfigure_keyring(self):
        self.device = Mock()
        result = unconfigure_keyring(self.device, 'myKeyring')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['no crypto keyring myKeyring'],)
        )
