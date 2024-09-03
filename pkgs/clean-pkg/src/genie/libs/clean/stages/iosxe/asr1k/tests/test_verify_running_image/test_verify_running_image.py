import unittest

from pyats.results import Passed, Failed
from pyats.topology import loader
from pyats.aetest.steps import Steps
from pyats.aetest.signals import TerminateStepSignal

from genie.libs.clean.stages.stages import VerifyRunningImage


class TestIosXEConnect(unittest.TestCase):
    """ Run unit testing on a mocked IOSXE asr1k device """

    @classmethod
    def setUpClass(cls):
        testbed = """
        devices:
            router:
                connections:
                    defaults:
                        class: unicon.Unicon
                    a:
                        command: mock_device_cli --os iosxe --mock_data_dir mock_data --state verify_running_image
                        protocol: unknown
                os: iosxe
                platform: asr1k
                type: router
                custom:
                    abstraction:
                        order: [os, platform]
        """
        cls.testbed = loader.load(testbed)
        cls.device = cls.testbed.devices['router']
        cls.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_verify_running_image_pass_without_regex(self):
        # Make sure we have a unique Steps() object for result verification
        self.steps = Steps()

        # And we want the following methods to be mocked to simulate the stage.
        self.verify_running_image = VerifyRunningImage()

        image = 'bootflash:/image.SSA.XYZ'

        with self.assertLogs(level='INFO') as log:
            self.verify_running_image(steps=self.steps, device=self.device, images=[image])
            self.assertIn("INFO:pyats.aetest.steps.implementation:Passed reason: " +
                          f"Successfully verified running image on device {self.device.name}", log.output)

        # Check the results is as expected.
        self.assertEqual(Passed, self.steps.details[0].result)

    def test_verify_running_image_pass_with_regex(self):
        # Make sure we have a unique Steps() object for result verification
        self.steps = Steps()

        # And we want the following methods to be mocked to simulate the stage.
        self.verify_running_image = VerifyRunningImage()

        image = 'bootflash:/image.SSA.XYZ.bin'

        with self.assertLogs(level='INFO') as log:
            self.verify_running_image(steps=self.steps, device=self.device, images=[image], regex_search=True)
            self.assertIn("INFO:pyats.aetest.steps.implementation:Passed reason: " +
                          f"Successfully verified running image on device {self.device.name}", log.output)

        # Check the results is as expected.
        self.assertEqual(Passed, self.steps.details[0].result)

    def test_verify_running_image_pass_with_regex_1(self):
        # Make sure we have a unique Steps() object for result verification
        self.steps = Steps()

        # And we want the following methods to be mocked to simulate the stage.
        self.verify_running_image = VerifyRunningImage()

        image = 'bootflash:/image.SSA'

        with self.assertLogs(level='INFO') as log:
            self.verify_running_image(steps=self.steps, device=self.device, images=[image], regex_search=True)
            self.assertIn("INFO:pyats.aetest.steps.implementation:Passed reason: " +
                          f"Successfully verified running image on device {self.device.name}", log.output)

        # Check the results is as expected.
        self.assertEqual(Passed, self.steps.details[0].result)

    def test_verify_running_image_pass_with_regex_2(self):
        # Make sure we have a unique Steps() object for result verification
        self.steps = Steps()

        # And we want the following methods to be mocked to simulate the stage.
        self.verify_running_image = VerifyRunningImage()

        image = 'bootflash:/image.SSA.XYZ'

        with self.assertLogs(level='INFO') as log:
            self.verify_running_image(steps=self.steps, device=self.device, images=[image], regex_search=True)
            self.assertIn("INFO:pyats.aetest.steps.implementation:Passed reason: " +
                          f"Successfully verified running image on device {self.device.name}", log.output)

        # Check the results is as expected.
        self.assertEqual(Passed, self.steps.details[0].result)

    def test_verify_running_image_fail_without_regex(self):
        # Make sure we have a unique Steps() object for result verification
        self.steps = Steps()

        # And we want the following methods to be mocked to simulate the stage.
        self.verify_running_image = VerifyRunningImage()

        image = 'bootflash:/image.SSAB.XYZ.bin'

        with self.assertRaises(TerminateStepSignal):
            self.verify_running_image(steps=self.steps, device=self.device, images=[image])

        # Check the results is as expected.
        self.assertEqual(Failed, self.steps.details[0].result)

    def test_verify_running_image_fail_with_regex(self):
        # Make sure we have a unique Steps() object for result verification
        self.steps = Steps()

        # And we want the following methods to be mocked to simulate the stage.
        self.verify_running_image = VerifyRunningImage()

        image = 'bootflash:/image.SSAB'

        with self.assertRaises(TerminateStepSignal):
            self.verify_running_image(steps=self.steps, device=self.device, images=[image], regex=True)

        # Check the results is as expected.
        self.assertEqual(Failed, self.steps.details[0].result)

    def test_verify_running_image_fail_with_regex_1(self):
        # Make sure we have a unique Steps() object for result verification
        self.steps = Steps()

        # And we want the following methods to be mocked to simulate the stage.
        self.verify_running_image = VerifyRunningImage()

        image = 'bootflash:/image.SSA.XYZ1'

        with self.assertRaises(TerminateStepSignal):
            self.verify_running_image(steps=self.steps, device=self.device, images=[image], regex=True)

        # Check the results is as expected.
        self.assertEqual(Failed, self.steps.details[0].result)

    def test_verify_running_image_fail_with_regex_2(self):
        # Make sure we have a unique Steps() object for result verification
        self.steps = Steps()

        # And we want the following methods to be mocked to simulate the stage.
        self.verify_running_image = VerifyRunningImage()

        image = 'bootflash:/image'

        with self.assertRaises(TerminateStepSignal):
            self.verify_running_image(steps=self.steps, device=self.device, images=[image], regex=True)

        # Check the results is as expected.
        self.assertEqual(Failed, self.steps.details[0].result)
