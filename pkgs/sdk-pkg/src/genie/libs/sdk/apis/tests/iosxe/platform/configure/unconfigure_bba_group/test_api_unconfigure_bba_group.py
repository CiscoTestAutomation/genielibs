import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform.configure import unconfigure_bba_group


class TestUnconfigureBbaGroup(unittest.TestCase):

    def test_unconfigure_bba_group(self):
        device = Mock()

        result = unconfigure_bba_group(device, 'global1', '1')

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['no bba-group pppoe global1'],)
        )

    def test_unconfigure_bba_group_without_vt_number(self):
        device = Mock()

        result = unconfigure_bba_group(device, '100')

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['no bba-group pppoe 100'],)
        )
