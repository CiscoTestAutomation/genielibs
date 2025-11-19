from unittest import TestCase
from genie.libs.sdk.apis.iosxe.cat9k.c9400.execute import execute_clear_install_state
from unittest.mock import Mock, MagicMock, patch, call
from unicon.core.errors import SubCommandFailure


class TestExecuteClearInstallState(TestCase):

    def setUp(self):
        """Set up common test fixtures"""
        self.device = Mock()
        self.device.name = 'test_device'
        self.device.api = Mock()
        
        # Actual write memory output
        self.write_memory_output = """write memory
        Building configuration...
        [OK]"""

        # Actual reload output
        self.reload_output = """This command will remove all the provisioned SMUs, and rollback points. Use this command with caution.
        A reload is required for this process. Press y to continue [y/n]y
        --- Starting clear_install_state ---
        Performing clear_install_state on Active/Standby
        [1] clear_install_state package(s) on R1
        [1] Finished clear_install_state on R1
        [1] clear_install_state package(s) on R0
        [1] Finished clear_install_state on R0
        Checking status of clear_install_state on [R1 R0]
        clear_install_state: Passed on [R1 R0]
        Finished clear_install_state

        Send model notification for  before reload
        Install will reload the system now!

        Requesting RP pvp reload

        Initializing Hardware......


        System Bootstrap, Version 17.10.0.1r, DEVELOPMENT SOFTWARE

        Copyright (c) 1994-2022 by cisco Systems, Inc.

        Compiled Tue Aug  2 15:22:37 2022 by nmusini

        If you have a negotiated agreement with Cisco that includes this Software, the
        terms of that agreement apply as well. In the event of a conflict, the order 
        of precedence stated in your negotiated agreement controls.
        Cisco Software is licensed on a term and/or subscription-basis. The license to
        the Software is valid only for the duration of the specified term, or in the
        case of a subscription-based license, only so long as all required subscription
        payments are current and fully paid-up. While Cisco may provide you
        licensing-related alerts, it is your sole responsibility to monitor your usage.
        Using Cisco Software without a valid license is not permitted and may result in
        fees charged to your account. Cisco reserves the right to terminate access to,
        or restrict the functionality of, any Cisco Software, or any features thereof,
        that are being used without a valid license.

        FIPS key on Standby is not configured.
        If Active is  FIPS configured, please make sure to configure FIPS on Standby also.
        Else switch is in non-standard operating mode.
        cisco C9410R (X86) processor (revision V01) with 1568427K/6147K bytes of memory.
        Processor board ID FXS2132Q0JA
        32768K bytes of non-volatile configuration memory.
        15990508K bytes of physical memory.
        10444800K bytes of Bootflash at bootflash:.
        1638400K bytes of Crash Files at crashinfo:.

        Base Ethernet MAC Address          : xxxx
        Motherboard Assembly Number        : xxxx
        Motherboard Serial Number          : xxxx
        Model Revision Number              : xxxx
        Motherboard Revision Number        : x
        Model Number                       : xxxx              
        System Serial Number               : xxxx

        Press RETURN to get started!"""
                
    def test_execute_clear_install_state_success(self):
        """Test successful execution of clear install state"""

        self.device.subconnections = None
        self.device.api.execute_write_memory = Mock(return_value=self.write_memory_output)
        self.device.reload = Mock(return_value=self.reload_output)

        result = execute_clear_install_state(self.device)

        self.assertTrue(result)
        self.device.api.execute_write_memory.assert_called_once()
        self.device.reload.assert_called_once()
