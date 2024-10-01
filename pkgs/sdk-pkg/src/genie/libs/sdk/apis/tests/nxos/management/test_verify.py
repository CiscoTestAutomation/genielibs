
import unittest
from genie.libs.sdk.apis.nxos.management.verify import is_management_interface
from unittest.mock import Mock

class TestManagementVerify(unittest.TestCase):

    def test_is_managment_interface(self):
        device = Mock()
        output = is_management_interface(device, 'Mgmt0')
        self.assertEqual(output, False)
        output = is_management_interface(device, 'mgmt0')
        self.assertEqual(output, True)