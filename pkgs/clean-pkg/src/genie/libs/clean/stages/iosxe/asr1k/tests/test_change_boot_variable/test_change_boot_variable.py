import unittest

from pyats.results import Passed
from pyats.topology import loader
from pyats.aetest.steps import Steps

from genie.libs.clean.stages.iosxe.stages import ChangeBootVariable


class TestChangeBootVariable1(unittest.TestCase):
    """ Run unit testing on a mocked IOSXE asr1k device """

    def test_change_boot_variable_pass(self):
        testbed = """
        devices:
            router:
                connections:
                    defaults:
                        class: unicon.Unicon
                    a:
                        command: mock_device_cli --os iosxe --mock_data_dir mock_data --state change_boot_variable_1
                        protocol: unknown
                os: iosxe
                platform: asr1k
                model: ASR1001-HX
                type: router
                custom:
                    abstraction:
                        order: [os, platform, model]
        """
        testbed = loader.load(testbed)
        device = testbed.devices['router']
        device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

        # Make sure we have a unique Steps() object for result verification
        steps = Steps()

        # And we want the following methods to be mocked to simulate the stage.
        change_boot_variable = ChangeBootVariable()

        image = 'bootflash:/image.SSA.XYZ'

        change_boot_variable(steps=steps, device=device, images=[image])

        # Check the results is as expected.
        self.assertEqual(Passed, steps.details[0].result)

    def test_change_boot_variable_with_current_running_image(self):
        testbed = """
        devices:
            router:
                connections:
                    defaults:
                        class: unicon.Unicon
                    a:
                        command: mock_device_cli --os iosxe --mock_data_dir mock_data --state change_boot_variable_2
                        protocol: unknown
                os: iosxe
                platform: asr1k
                model: ASR1001-HX
                type: router
                custom:
                    abstraction:
                        order: [os, platform, model]
        """
        testbed = loader.load(testbed)
        device = testbed.devices['router']
        device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )
        # Make sure we have a unique Steps() object for result verification
        steps = Steps()

        # And we want the following methods to be mocked to simulate the stage.
        change_boot_variable = ChangeBootVariable()

        image = 'bootflash:/image.SSA.XYZ'

        with self.assertLogs(level='INFO') as log:
            change_boot_variable(steps=steps, device=device, images=[image], current_running_image=True)
            self.assertIn("INFO:genie.libs.clean.stages.iosxe.stages:" +
                          "Verifying next reload boot variables Using the running image due to 'current_running_image: True'",
                          log.output)

        # Check the results is as expected.
        self.assertEqual(Passed, steps.details[0].result)
