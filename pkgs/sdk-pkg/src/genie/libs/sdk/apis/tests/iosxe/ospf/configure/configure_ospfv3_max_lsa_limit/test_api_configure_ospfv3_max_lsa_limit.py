from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.ospf.configure import configure_ospfv3_max_lsa_limit


class TestConfigureOspfv3MaxLsaLimit(TestCase):

    def test_configure_ospfv3_max_lsa_limit(self):
        device = Mock()
        result = configure_ospfv3_max_lsa_limit(
            device,
            '64',
            429496729
        )
        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['router ospfv3 64', 'max-lsa 429496729'],)
        )