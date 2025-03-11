import logging
import unittest

from unittest.mock import Mock

from genie.libs.clean.stages.iosxe.c9800.stages import ConfigureApTxPower
from genie.libs.clean.stages.tests.utils import create_test_device

from pyats.aetest.steps import Steps
from pyats.results import Passed, Failed
from pyats.aetest.signals import TerminateStepSignal
from unicon.core.errors import SubCommandFailure

# Disable logging. It may be useful to comment this out when developing tests.
logging.disable(logging.CRITICAL)


class TestConfigureApTxPower(unittest.TestCase):

    def setUp(self):
        # Instantiate class object
        self.cls = ConfigureApTxPower()

        # Instantiate device object. This also sets up commonly needed
        # attributes and Mock objects associated with the device.
        self.device = create_test_device('vidya-ewlc-5', os='iosxe', platform='c9800')

    def test_pass_configure_ap_tx_power(self):
        # Make sure we have a unique Steps() object for result verification
        steps = Steps()
        data = {'show ap summary': '''Number of APs: 4

                AP Name                            Slots    AP Model              Ethernet MAC    Radio MAC       Location                          Country     IP Address                                 State         
                -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
                AP002C.C862.E708                     2      AIR-AP1815I-A-K9      002c.c862.e708  002c.c88a.fd20  default location                  US          9.4.57.125                                 Registered    
                AP188B.4500.44C8                     2      AIR-AP1832I-D-K9      188b.4500.44c8  188b.4501.7c60  default location                  IN          9.4.57.120                                 Registered    
                AP188B.4500.5EE8                     2      AIR-AP1852I-D-K9      188b.4500.5ee8  188b.4501.e4e0  default location                  IN          9.4.57.121                                 Registered    
                APCC16.7EDB.4168                     2      AIR-AP2802I-D-K9      cc16.7edb.4168  a0e0.af91.9e60  default location                  IN          9.4.57.119                                 Registered '''}

        # And we want the configure_ap_tx_power api to be mocked.
        # This simulates the pass case.
        self.device.configure = Mock()
        self.device.execute = Mock(side_effect=lambda x: data[x])
        self.device.api.execute_ap_tx_power_commands = Mock()

        # Call the method to be tested (clean step inside class)
        self.cls.configure_ap_tx_power(device=self.device, steps=steps,
                                       access_points=['AP002C.C862.E708', 'AP188B.4500.44C8'])

        # Check that the result is expected
        self.assertEqual(Passed, steps.details[0].result)

    def test_fail_configure_ap_tx_power(self):
        # Make sure we have a unique Steps() object for result verification
        steps = Steps()
        data = {'show ap summary': '''Number of APs: 4

                AP Name                            Slots    AP Model              Ethernet MAC    Radio MAC       Location                          Country     IP Address                                 State         
                -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
                AP002C.C862.E708                     2      AIR-AP1815I-A-K9      002c.c862.e708  002c.c88a.fd20  default location                  US          9.4.57.125                                 Registered    
                AP188B.4500.44C8                     2      AIR-AP1832I-D-K9      188b.4500.44c8  188b.4501.7c60  default location                  IN          9.4.57.120                                 Registered    
                AP188B.4500.5EE8                     2      AIR-AP1852I-D-K9      188b.4500.5ee8  188b.4501.e4e0  default location                  IN          9.4.57.121                                 Registered    
                APCC16.7EDB.4168                     2      AIR-AP2802I-D-K9      cc16.7edb.4168  a0e0.af91.9e60  default location                  IN          9.4.57.119                                 Registered '''}

        # And we want the configure_ap_tx_power api to be mocked.
        # This simulates the pass case.
        self.device.configure = Mock()
        self.device.execute = Mock(side_effect=lambda x: data[x])
        self.device.api.execute_ap_tx_power_commands = Mock(side_effect=SubCommandFailure)

        # Call the method to be tested (clean step inside class)
        with self.assertRaises(TerminateStepSignal):
            self.cls.configure_ap_tx_power(device=self.device, steps=steps,
                                           access_points=['AP045F.B97A.F590', 'APCC16.7EDB.4567'])

        # Check that the result is expected
        self.assertEqual(Failed, steps.details[0].result)

    def test_pass_verify_ap_tx_power(self):
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
                Unused Channel List                      : 52,56,60,64,100,104,108,112,116,120,124,128,132,136,140,144
        ''', 'show ap dot11 5ghz summary': '''* global assignment

            AP Name                           Mac Address     Slot    Admin State    Oper State    Width    Txpwr           Channel                             Mode
            ---------------------------------------------------------------------------------------------------------------------------------------------------------
            AP002C.C862.E708                  002c.c88a.fd20  1       Disabled       Down          40       1/8 (20 dBm)    (161,157)*                          Local      
            AP188B.4500.44C8                  188b.4501.7c60  1       Disabled       Down          40       1/8 (22 dBm)    (157,161)*                          Local      
            AP188B.4500.5EE8                  188b.4501.e4e0  1       Disabled       Down          40       *1/8 (23 dBm)   (161,157)*                          Local      
            APCC16.7EDB.4168                  a0e0.af91.9e60  1       Enabled        Up            40       *1/8 (22 dBm)   (36,40)                             Local '''}

        # And we want the configure_ap_tx_power api to be mocked.
        # This simulates the pass case.
        self.device.execute = Mock(side_effect=lambda x: data[x])

        # Call the method to be tested (clean step inside class)
        self.cls.verify_ap_tx_power_configure(device=self.device, steps=steps,
                                              access_points=['AP002C.C862.E708', 'AP188B.4500.44C8'])

        # Check that the result is expected
        self.assertEqual(Passed, steps.details[0].result)

    def test_fail_verify_ap_tx_power(self):
        # Make sure we have a unique Steps() object for result verification
        steps = Steps()
        data = {'show ap dot11 5ghz channel': '''Leader Automatic Channel Assignment
              Channel Assignment Mode                    : MANUAL
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
        ''', 'show ap dot11 5ghz summary': '''* global assignment

            AP Name                           Mac Address     Slot    Admin State    Oper State    Width    Txpwr           Channel                             Mode
            ---------------------------------------------------------------------------------------------------------------------------------------------------------
            AP002C.C862.E708                  002c.c88a.fd20  1       Disabled       Down          40       2/8 (20 dBm)    (161,157)*                          Local      
            AP188B.4500.44C8                  188b.4501.7c60  1       Disabled       Down          40       4/8 (22 dBm)    (157,161)*                          Local      
            AP188B.4500.5EE8                  188b.4501.e4e0  1       Disabled       Down          40       *1/8 (23 dBm)   (161,157)*                          Local      
            APCC16.7EDB.4168                  a0e0.af91.9e60  1       Enabled        Up            40       *1/8 (22 dBm)   (36,40)                             Local '''}

        # And we want the configure_ap_tx_power api to be mocked.

        # This simulates the pass case.
        self.device.execute = Mock(side_effect=lambda x: data[x])

        # Call the method to be tested (clean step inside class)
        with self.assertRaises(TerminateStepSignal):
            self.cls.verify_ap_tx_power_configure(device=self.device, steps=steps,
                                                  access_points=['AP002C.C862.E708', 'AP188B.4500.44C8'])

        # Check that the result is expected
        self.assertEqual(Failed, steps.details[0].result)
