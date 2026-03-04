from unittest import TestCase
from genie.libs.sdk.apis.iosxe.isis.configure import configure_isis_passive_interface
from unittest.mock import Mock


class TestConfigureIsisPassiveInterface(TestCase):

    def test_configure_isis_passive_interface(self):
        self.device = Mock()
        result = configure_isis_passive_interface(self.device, 'Loopback15')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['router isis', 'passive-interface Loopback15'],)
        )
