from unittest import TestCase
from genie.libs.sdk.apis.iosxe.aaa.configure import unconfigure_aaa_accounting_dot1x_default_start_stop_group
from unittest.mock import Mock


class TestUnconfigureAaaAccountingDot1xDefaultStartStopGroup(TestCase):

    def test_unconfigure_aaa_accounting_dot1x_default_start_stop_group(self):
        self.device = Mock()
        unconfigure_aaa_accounting_dot1x_default_start_stop_group(self.device, 'srvgrp')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ('no aaa accounting dot1x default start-stop group srvgrp',)
        )

