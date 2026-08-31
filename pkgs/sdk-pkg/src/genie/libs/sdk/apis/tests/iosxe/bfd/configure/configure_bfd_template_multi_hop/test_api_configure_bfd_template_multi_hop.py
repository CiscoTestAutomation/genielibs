from unittest import TestCase
from genie.libs.sdk.apis.iosxe.bfd.configure import configure_bfd_template_multi_hop
from unittest.mock import Mock


class TestConfigureBfdTemplateMultiHop(TestCase):

    def test_configure_bfd_template_multi_hop(self):
        self.device = Mock()
        result = configure_bfd_template_multi_hop(self.device, 'bfd_temp', 750, 750, 3)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['bfd-template multi-hop bfd_temp', 'interval min-tx 750 min-rx 750 multiplier 3'],)
        )
