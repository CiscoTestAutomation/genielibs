import os
import unittest
from unittest import mock
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.startup_config.configure import configure_ignore_startup_config, unconfigure_ignore_startup_config

class TestStartupConfigConfigure(unittest.TestCase):

    def test_configure_ignore_startup_config(self):
        device = mock.Mock()
        device.execute = mock.Mock()
        device.configure = mock.Mock() 
        
        device.state_machine.current_state = 'rommon'
        configure_ignore_startup_config(device)
        device.execute.assert_called_once_with('confreg 0x2142')
        
        device.state_machine.current_state = 'enable'
        configure_ignore_startup_config(device)
        device.configure.assert_called_once_with('config-register 0x2142')
        

    def test_unconfigure_ignore_startup_config(self):
        device = mock.Mock()
        device.execute = mock.Mock()
        device.configure = mock.Mock() 
        
        device.state_machine.current_state = 'rommon'
        unconfigure_ignore_startup_config(device)
        device.execute.assert_called_once_with('confreg 0x2102')
        
        device.state_machine.current_state = 'enable'
        unconfigure_ignore_startup_config(device)
        device.configure.assert_called_once_with('config-register 0x2102')