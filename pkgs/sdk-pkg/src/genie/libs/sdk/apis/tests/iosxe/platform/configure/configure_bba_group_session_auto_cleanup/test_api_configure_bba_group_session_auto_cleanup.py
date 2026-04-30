from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform.configure import configure_bba_group_session_auto_cleanup


class TestConfigureBbaGroupSessionAutoCleanup(TestCase):

    def test_configure_bba_group_session_auto_cleanup(self):
        device = Mock()
        result = configure_bba_group_session_auto_cleanup(
            device,
            'PPPOE',
            True
        )
        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['bba-group pppoe PPPOE', 'session auto cleanup'],)
        )