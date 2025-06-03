from unittest import TestCase
from genie.libs.sdk.apis.iosxe.cts.configure import unconfigure_cts_enforcement_logging
from unittest.mock import Mock


class TestUnconfigureCtsEnforcementLogging(TestCase):

    def test_unconfigure_cts_enforcement_logging(self):
        self.device = Mock()
        result = unconfigure_cts_enforcement_logging(self.device, '5')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ('no cts role-based enforcement logging-interval 5',)
        )
