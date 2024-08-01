import unittest

from genie.conf import Genie
from genie.libs.sdk.apis.iosxe.cat9k.platform.get import get_boot_variables


class TestApiIiosxePlatform(unittest.TestCase):

    parsed_outputs = {
        'show boot': {
            "current_boot_variable": "flash:/rio_yang_current.bin;",
            "next_reload_boot_variable": "flash:/rio_yang_next.bin;",
        },
    }

    @classmethod
    def get_parsed_output(cls, arg, **kwargs):
        '''Return the parsed output of the given show command '''
        return cls.parsed_outputs[arg]

    @classmethod
    def setUpClass(cls):
        testbed = """
        devices:
            R1:
                os: iosxe
                type: router
                connections: {}
        """
        cls.tb = Genie.init(testbed)
        cls.device = cls.tb.devices['R1']
        cls.device.parse = cls.get_parsed_output

    def test_get_boot_variables(self):
        boot_vars = get_boot_variables(self.device, 'current')
        self.assertEqual(boot_vars, ['flash:/rio_yang_current.bin'])

        boot_vars = get_boot_variables(self.device, 'next')
        self.assertEqual(boot_vars, ['flash:/rio_yang_next.bin'])

        with self.assertRaises(AssertionError):
            get_boot_variables(self.device, 'does_not_exist')

class TestApiIosxeCat9kPlatform(unittest.TestCase):

    parsed_outputs = {
        'show boot': {
            "boot_variable": "bootflash:/packages.conf",
        }
    }

    @classmethod
    def get_parsed_output(cls, arg, **kwargs):
        '''Return the parsed output of the given show command '''
        return cls.parsed_outputs[arg]

    @classmethod
    def setUpClass(cls):
        testbed = """
        devices:
            R1:
                os: iosxe
                platform: cat9k
                connections: {}
        """
        cls.tb = Genie.init(testbed)
        cls.device = cls.tb.devices['R1']
        cls.device.parse = cls.get_parsed_output

    def test_get_default_boot_variables(self):
        boot_vars = get_boot_variables(self.device, 'current')
        self.assertEqual(boot_vars, ['bootflash:/packages.conf'])

        boot_vars = get_boot_variables(self.device, 'next')
        self.assertEqual(boot_vars, ['bootflash:/packages.conf'])

if __name__ == '__main__':
    unittest.main()