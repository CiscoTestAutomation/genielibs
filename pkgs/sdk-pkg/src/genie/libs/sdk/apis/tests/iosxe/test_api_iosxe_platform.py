
import unittest

from genie.conf import Genie
from genie.metaparser.util.exceptions import SchemaEmptyParserError

from genie.libs.clean.stages.iosxe.tests.iosxe_pos_stage_outputs import get_parsed_output as pos_parsed
from genie.libs.sdk.apis.iosxe.platform.get import (
    get_boot_variables, get_config_register)


class TestApiIiosxePlatform(unittest.TestCase):

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
        cls.device.parse = pos_parsed

    def test_get_boot_variables(self):
        boot_vars = get_boot_variables(self.device, 'current')
        self.assertEqual(boot_vars, ['harddisk:/vmlinux_PE1.bin'])

        boot_vars = get_boot_variables(self.device, 'next')
        self.assertEqual(boot_vars, ['harddisk:/vmlinux_PE1.bin'])

        with self.assertRaises(AssertionError):
            get_boot_variables(self.device, 'does_not_exist')

    def test_get_config_register(self):
        config_reg = get_config_register(self.device)
        self.assertEqual(config_reg, '0x2102')

        # Need updated parsed device output
        # config_reg = get_config_register(self.device, next_reload=True)
        # self.assertEqual(config_reg, '0x2101')


if __name__ == '__main__':
    unittest.main()