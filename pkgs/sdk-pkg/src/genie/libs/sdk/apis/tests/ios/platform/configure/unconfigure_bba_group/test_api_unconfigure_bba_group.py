import unittest
from unittest.mock import Mock

from genie.libs.sdk.apis.ios.platform.configure import unconfigure_bba_group


class TestUnconfigureBbaGroup(unittest.TestCase):

    def test_unconfigure_bba_group(self):
        device = Mock()

        result = unconfigure_bba_group(device, 'global1')

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['no bba-group pppoe global1'],)
        )

    def test_unconfigure_bba_group_name_only(self):
        device = Mock()

        result = unconfigure_bba_group(device, '100')

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['no bba-group pppoe 100'],)
        )

    def test_unconfigure_bba_group_vt_number(self):
        device = Mock()

        result = unconfigure_bba_group(device, '10', vt_number='10')

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['bba-group pppoe 10', 'no virtual-template 10'],)
        )
