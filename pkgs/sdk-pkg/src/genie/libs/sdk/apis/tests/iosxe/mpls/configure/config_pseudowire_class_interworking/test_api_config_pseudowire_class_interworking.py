from unittest import TestCase
from genie.libs.sdk.apis.iosxe.mpls.configure import config_pseudowire_class_interworking
from unittest.mock import Mock


class TestConfigPseudowireClassInterworking(TestCase):

    def test_config_pseudowire_class_interworking(self):
        self.device = Mock()
        result = config_pseudowire_class_interworking(self.device, 'C2', 'ethernet')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['pseudowire-class C2', 'encapsulation mpls', 'interworking ethernet'],)
        )
