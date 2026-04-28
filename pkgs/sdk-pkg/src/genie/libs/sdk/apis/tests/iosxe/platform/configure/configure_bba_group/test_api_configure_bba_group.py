from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform.configure import configure_bba_group


class TestConfigureBbaGroup(TestCase):

    def test_configure_bba_group(self):
        device = Mock()
        result = configure_bba_group(
            device,
            'global_100',
            '100',
            None,
            'minimum 1500 maximum 1700'
        )
        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ([
                'bba-group pppoe global_100',
                'virtual-template 100',
                'tag ppp-max-payload minimum 1500 maximum 1700'
            ],)
        )