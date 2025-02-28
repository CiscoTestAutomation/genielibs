import logging
import unittest


from unittest.mock import Mock, MagicMock

from genie.libs.clean.stages.iosxe.c9800.stages import ConfigureRrmDcaChannel 
from genie.libs.clean.stages.tests.utils import CommonStageTests, create_test_device

from pyats.aetest.steps import Steps
from pyats.results import Passed, Failed
from pyats.aetest.signals import TerminateStepSignal
from unicon.eal.dialogs import Statement, Dialog

# Disable logging. It may be useful to comment this out when developing tests.
logging.disable(logging.CRITICAL)


class TestRrmDcaChannel(unittest.TestCase):

    def setUp(self):
        # Instantiate class object
        self.cls = ConfigureRrmDcaChannel()

        # Instantiate device object. This also sets up commonly needed
        # attributes and Mock objects associated with the device.
        self.device = create_test_device('vidya-ewlc-5', os='iosxe', platform='c9800')

    def test_pass_configure_rrm_dca_channel(self):
        # Make sure we have a unique Steps() object for result verification
        steps = Steps()

        # And we want the configure_ap_tx_power api to be mocked.
        # This simulates the pass case.
        self.device.configure = Mock()

        # Call the method to be tested (clean step inside class)
        self.cls.configure_rrm_dca_channel(device=self.device, steps=steps)

        # Check that the result is expected
        self.assertEqual(Passed, steps.details[0].result)

    def test_fail_configure_rrm_dca_channel(self):
        # Make sure we have a unique Steps() object for result verification
        steps = Steps()

        # And we want the configure_ap_tx_power api to be mocked to raise an
        # exception when called. This simulates the fail case.
        self.device.configure = Mock(side_effect=Exception)

        # We expect this step to fail so make sure it raises the signal
        with self.assertRaises(TerminateStepSignal):
            self.cls.configure_rrm_dca_channel(device=self.device, steps=steps)

        # Check the overall result is as expected
        self.assertEqual(Failed, steps.details[0].result)

    def test_pass_verify_rrm_dcs_channels_removed(self):
        # Make sure we have a unique Steps() object for result verification
        steps = Steps()
        data={'show ap dot11 5ghz channel':'''Leader Automatic Channel Assignment
              Channel Assignment Mode                    : AUTO
              Channel Update Interval                    : 600 seconds
              Anchor time (Hour of the day)              : 0
              Channel Update Contribution
                Noise                                    : Enable
                Interference                             : Enable
                Load                                     : Disable
                Device Aware                             : Disable
              CleanAir Event-driven RRM option           : Disabled
              Zero Wait DFS                              : Disabled
              Channel Assignment Leader                  : vidya-ewlc-5 (9.4.62.51) (2001:9:4:62::51)
              Last Run                                   : 267 seconds ago
            
              DCA Sensitivity Level                      : MEDIUM : 15 dB
              DCA 802.11n/ac Channel Width               : best
              DBS Max Channel Width                      : 40 MHz
              DCA Minimum Energy Limit                   : -95 dBm
              Channel Energy Levels
                Minimum                                  : -72 dBm
                Average                                  : 13 dBm
                Maximum                                  : -72 dBm
              Channel Dwell Times
                Minimum                                  : 9 days 0 hour 24 minutes 18 seconds 
                Average                                  : 21 days 17 hours 21 minutes 42 seconds 
                Maximum                                  : 26 days 20 hours 18 minutes 7 seconds 
              802.11a 5 GHz Auto-RF Channel List
                Allowed Channel List                     : 36,40,44,48,149,153,157,161
                Unused Channel List                      : 52,56,60,64,100,104,108,112,116,120,124,128,132,136,140,144
        '''}

        # And we want the configure_ap_tx_power api to be mocked.
        # This simulates the pass case.
        self.device.execute = Mock(side_effect=lambda x: data[x])

        # Call the method to be tested (clean step inside class)
        self.cls.verify_rrm_dcs_channels_removed(device=self.device, steps=steps)

        # Check that the result is expected
        self.assertEqual(Passed, steps.details[0].result)

    def test_fail_verify_rrm_dcs_channels_removed(self):
        # Make sure we have a unique Steps() object for result verification
        steps = Steps()
        data = {'show ap dot11 5ghz channel': '''Leader Automatic Channel Assignment
              Channel Assignment Mode                    : AUTO
              Channel Update Interval                    : 600 seconds
              Anchor time (Hour of the day)              : 0
              Channel Update Contribution
                Noise                                    : Enable
                Interference                             : Enable
                Load                                     : Disable
                Device Aware                             : Disable
              CleanAir Event-driven RRM option           : Disabled
              Zero Wait DFS                              : Disabled
              Channel Assignment Leader                  : vidya-ewlc-5 (9.4.62.51) (2001:9:4:62::51)
              Last Run                                   : 267 seconds ago

              DCA Sensitivity Level                      : MEDIUM : 15 dB
              DCA 802.11n/ac Channel Width               : best
              DBS Max Channel Width                      : 40 MHz
              DCA Minimum Energy Limit                   : -95 dBm
              Channel Energy Levels
                Minimum                                  : -72 dBm
                Average                                  : 13 dBm
                Maximum                                  : -72 dBm
              Channel Dwell Times
                Minimum                                  : 9 days 0 hour 24 minutes 18 seconds 
                Average                                  : 21 days 17 hours 21 minutes 42 seconds 
                Maximum                                  : 26 days 20 hours 18 minutes 7 seconds 
              802.11a 5 GHz Auto-RF Channel List
                Allowed Channel List                     : 36,40,44,48,149,153,157,161
                Unused Channel List                      : 52,56,60,64,116,120,124,128,132,136,140,144
        '''}

        # And we want the configure_ap_tx_power api to be mocked.
        # This simulates the pass case.
        self.device.execute = Mock(side_effect=lambda x: data[x])

        # Call the method to be tested (clean step inside class)
        with self.assertRaises(TerminateStepSignal):
            self.cls.verify_rrm_dcs_channels_removed(device=self.device, steps=steps)

        # Check that the result is expected

        self.assertEqual(Failed, steps.details[0].result)





