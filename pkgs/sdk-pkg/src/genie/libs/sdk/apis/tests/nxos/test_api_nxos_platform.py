import unittest
from unittest.mock import Mock

from genie.libs.sdk.apis.nxos.platform.get import get_software_version

from pyats.topology import Device

class TestApiGetSoftwareVersion(unittest.TestCase):
    device1 = Device(name='Device1')
    device1.parse = Mock(return_value=Mock(**{
        'q.contains': Mock(return_value=Mock(**{
            'get_values': Mock(return_value='8.1(1)')
        }))
    }))
    device2 = Device(name="Device2")
    device2.parse = Mock(return_value=Mock(**{
        'q.contains': Mock(return_value=Mock(**{
            'get_values': Mock(return_value='7.3(1)N1(2)')
        }))
    }))

    def test_string_return(self):
        self.assertEqual('8.1(1)', get_software_version(self.device1))
        self.assertEqual('7.3(1)N1(2)', get_software_version(self.device2))

    def test_tuple_return(self):
        self.assertEqual((8, 1, 1),
            get_software_version(self.device1, return_tuple=True))
        self.assertEqual((7, 3, 1, 'N1', 2),
            get_software_version(self.device2, return_tuple=True))

if __name__ == '__main__':
    unittest.main()