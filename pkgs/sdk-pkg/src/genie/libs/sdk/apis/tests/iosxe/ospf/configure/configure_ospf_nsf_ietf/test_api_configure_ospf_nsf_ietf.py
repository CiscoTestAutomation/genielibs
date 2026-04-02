from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.ospf.configure import configure_ospf_nsf_ietf


class TestConfigureOspfNsfIetf(TestCase):

    def test_configure_ospf_nsf_ietf(self):
        device = Mock()
        result = configure_ospf_nsf_ietf(
            device,
            1
        )
        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['router ospf 1', 'nsf ietf'],)
        )