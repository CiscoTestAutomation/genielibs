from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.ospf.configure import configure_maximum_path_under_ospf


class TestConfigureMaximumPathUnderOspf(TestCase):

    def test_configure_maximum_path_under_ospf(self):
        device = Mock()
        result = configure_maximum_path_under_ospf(
            device,
            '1',
            5
        )
        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['router ospf 1', 'maximum-path 5'],)
        )