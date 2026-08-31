from unittest import TestCase
from genie.libs.sdk.apis.iosxe.bfd.configure import unconfigure_bfd_template_multi_hop
from unittest.mock import Mock


class TestUnconfigureBfdTemplateMultiHop(TestCase):

    def test_unconfigure_bfd_template_multi_hop(self):
        self.device = Mock()
        result = unconfigure_bfd_template_multi_hop(self.device, 'bfd_temp')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ('no bfd-template multi-hop bfd_temp',)
        )
