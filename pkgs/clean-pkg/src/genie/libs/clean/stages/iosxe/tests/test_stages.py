
# Python
import os
import logging
import unittest
from unittest.mock import Mock

# pyATS
from pyats.aetest.steps import Steps
from pyats.aetest.base import TestItem
from pyats.kleenex.engine import KleenexEngine
from pyats.kleenex.loader import KleenexFileLoader
from pyats.aetest.signals import AEtestPassedSignal, AEtestFailedSignal, \
                                 TerminateStepSignal

# Unicon
from unicon.core.errors import SubCommandFailure, ConnectionError, StateMachineError

# Genie
from genie.testbed import load
from genie.libs.clean.stages.iosxe.stages import change_boot_variable
from genie.libs.clean.stages.stages import connect, ping_server, copy_to_linux,\
                                           copy_to_device, write_erase,\
                                           reload, apply_configuration,\
                                           verify_running_image

# Positive Mock Outputs
from genie.libs.clean.stages.iosxe.tests.pos_stage_outputs import \
                                            StageOutputs as PassedStageOutputs,\
                                            get_execute_output as pos_execute,\
                                            get_parsed_output as pos_parsed,\
                                            get_config_output as pos_config

# Negative Mock Outputs
from genie.libs.clean.stages.iosxe.tests.neg_stage_outputs import \
                                            StageOutputs as FailedStageOutputs,\
                                            get_execute_output as neg_execute,\
                                            get_parsed_output as neg_parsed,\
                                            get_config_output as neg_config

# Disable log messages
logging.disable(logging.CRITICAL)

test_path = os.path.dirname(os.path.abspath(__file__))

class PositiveStages(unittest.TestCase):

    def setUp(self):
        # Load sample testbed YAML & clean YAML
        self.tb = load(test_path+'/mock_testbed.yaml')
        self.clean_config = KleenexFileLoader(testbed=self.tb,
                                              invoke_clean=True).\
                                              load(test_path+'/mock_clean.yaml')
        KleenexEngine.update_testbed(self.tb, **self.clean_config['devices'])

        self.steps = Steps()
        self.device = self.tb.devices['PE1']
        self.device.is_ha = None
        self.raw_output = PassedStageOutputs
        self.section = TestItem(uid='test', description='', parameters={})


    def test_stage_connect(self):
        self.device.connect = Mock(return_value=self.raw_output.connect)
        
        # Execute stage: connect
        with self.assertRaises(AEtestPassedSignal):
            connect(self.section, self.device)


    def test_stage_ping_server(self):
        self.device.ping = Mock(return_value=self.raw_output.ping_server)

        # Execute stage: ping_server
        with self.assertRaises(AEtestPassedSignal):
            ping_server(self.section, self.steps, self.device,
                        **self.device.clean.ping_server)


    @unittest.mock.patch('os.path.getsize', Mock(return_value=989519758))
    @unittest.mock.patch('os.path.join', Mock(return_value='/auto/path/images/vmlinux_PE1.bin'))
    @unittest.mock.patch('shutil.copyfile', Mock(return_value=True))
    def test_stage_copy_to_linux(self):
        self.section.history = {}
        self.section.history['copy_to_linux'] = Mock()
        self.section.history['copy_to_linux'].parameters = {}

        self.device.api.modify_filename = Mock(return_value='vmlinux_PE1.bin')
        self.device.api.verify_file_exists_on_server = Mock(return_value=True)
        self.device.api.verify_file_size_stable_on_server = Mock(return_value=True)
        self.device.api.verify_enough_server_disk_space = Mock(return_value=True)

        # Execute stage: copy_to_linux
        with self.assertRaises(AEtestPassedSignal):
            copy_to_linux(self.section, self.steps, self.device,
                          **self.device.clean.copy_to_linux)


    def test_stage_copy_to_device(self):
        self.section.history = {}
        self.section.history['copy_to_device'] = Mock()
        self.section.history['copy_to_device'].parameters = {}

        self.device.execute = Mock(side_effect=pos_execute)
        self.device.parse = Mock(side_effect=pos_parsed)
        self.device.configure = Mock(side_effect=pos_config)

        self.device.api.get_file_size_from_server = Mock(return_value=989519758)
        self.device.api.verify_file_size_stable_on_server = Mock(return_value=True)

        # Execute stage: copy_to_device
        copy_to_device(self.section, self.steps, self.device,
                       **self.device.clean.copy_to_device)
        self.assertEqual('passed', self.section.result.name)


    def test_stage_change_boot_variable(self):
        self.device.parse = Mock(side_effect=pos_parsed)
        self.device.configure = Mock(side_effect=pos_config)
        self.device.execute = Mock(side_effect=pos_execute)

        # Execute stage: change_boot_variable
        with self.assertRaises(AEtestPassedSignal):
            change_boot_variable(self.section, self.steps, self.device,
                                 **self.device.clean.change_boot_variable)


    def test_stage_write_erase(self):
        self.device.execute = Mock(return_value=self.raw_output.write_erase,
                                   error_pattern=['^%\\s*[Ii]nvalid (command|input)'])
        #self.device.execute.error_pattern = iter(MagicMock())

        # Execute stage: write_erase
        with self.assertRaises(AEtestPassedSignal):
            write_erase(self.section, self.steps, self.device,
                        **self.device.clean.write_erase)


    def test_stage_reload(self):
        self.device.reload = Mock(return_value=self.raw_output.reload_output)
        self.device.destroy = Mock(return_value="")
        self.device.connect = Mock(return_value=self.raw_output.reload_connect)
        self.device.parse = Mock(side_effect=pos_parsed)

        # Execute stage: reload
        reload(self.section, self.steps, self.device,
                **self.device.clean.reload)


    def test_stage_apply_configuration(self):
        self.device.configure = Mock(side_effect=StateMachineError('device hostname changed'))
        self.device.destroy = Mock(return_value="")
        self.device.connect = Mock(return_value=self.raw_output.connect)
        self.device.execute = Mock(side_effect=pos_execute)
        
        # Execute stage: apply_configuration
        with self.assertRaises(AEtestPassedSignal):
            apply_configuration(self.section, self.steps, self.device,
                                **self.device.clean.apply_configuration)


    def test_stage_verify_running_image(self):
        self.device.parse = Mock(side_effect=pos_parsed)

        # Execute stage: verify_running_image
        with self.assertRaises(AEtestPassedSignal):
            verify_running_image(self.section, self.steps, self.device,
                                 **self.device.clean.verify_running_image)


class NegativeStages(unittest.TestCase):

    def setUp(self):
        # Load sample testbed YAML & clean YAML
        self.tb = load(test_path+'/mock_testbed.yaml')
        self.clean_config = KleenexFileLoader(testbed=self.tb,
                                              invoke_clean=True).\
                                              load(test_path+'/mock_clean.yaml')
        KleenexEngine.update_testbed(self.tb, **self.clean_config['devices'])

        self.steps = Steps()
        self.device = self.tb.devices['PE1']
        self.device.is_ha = None
        self.raw_output = FailedStageOutputs
        self.section = TestItem(uid='test', description='', parameters={})


    def test_stage_connect(self):
        self.device.connect = Mock(side_effect=ConnectionError('negative test'))
        self.device.destroy_all = Mock(return_value="")

        # Execute stage: connect
        with self.assertRaises(AEtestFailedSignal):
            connect(self.section, self.device)


    def test_stage_ping_server(self):
        self.device.ping = Mock(return_value=self.raw_output.ping_server)

        # Execute stage ping_server
        with self.assertRaises(TerminateStepSignal):
            ping_server(self.section, self.steps, self.device,
                        **self.device.clean.ping_server)


    @unittest.mock.patch('os.path.getsize', Mock(return_value=989519758))
    @unittest.mock.patch('os.path.join', Mock(return_value='/auto/path/images/vmlinux_PE1.bin'))
    @unittest.mock.patch('shutil.copyfile', Mock(side_effect=KeyError("negative test")))
    def test_stage_copy_to_linux(self):
        self.section.history = {}
        self.section.history['copy_to_linux'] = Mock()
        self.section.history['copy_to_linux'].parameters = {}
        self.device.api.modify_filename = Mock(return_value='vmlinux_PE1.bin')
        self.device.api.verify_file_exists_on_server = Mock(return_value=True)
        self.device.api.verify_file_size_stable_on_server = Mock(return_value=True)
        self.device.api.verify_enough_server_disk_space = Mock(return_value=True)

        # Execute stage: copy_to_linux
        with self.assertRaises(TerminateStepSignal):
            copy_to_linux(self.section, self.steps, self.device,
                          **self.device.clean.copy_to_linux)


    def test_stage_copy_to_device(self):
        self.section.history = {}
        self.section.history['copy_to_device'] = Mock()
        self.section.history['copy_to_device'].parameters = {}

        self.device.execute = Mock(side_effect=neg_execute)
        self.device.parse = Mock(side_effect=neg_parsed)
        self.device.configure = Mock(side_effect=neg_config)

        self.device.api.get_file_size_from_server = Mock(return_value=989519799)
        self.device.api.verify_file_size_stable_on_server = Mock(return_value=True)

        # Execute stage: copy_to_device
        with self.assertRaises(TerminateStepSignal):
            copy_to_device(self.section, self.steps, self.device,
                           **self.device.clean.copy_to_device)


    def test_stage_change_boot_variable1(self):
        self.device.parse = Mock(side_effect=neg_parsed)
        self.device.configure = Mock(side_effect=KeyError("negative test"))
        self.device.execute = Mock(side_effect=neg_execute)

        # Execute stage: change_boot_variable
        with self.assertRaises(TerminateStepSignal):
            change_boot_variable(self.section, self.steps, self.device,
                                 **self.device.clean.change_boot_variable)


    def test_stage_change_boot_variable2(self):
        self.device.parse = Mock(side_effect=neg_parsed)
        self.device.configure = Mock(side_effect=neg_config)
        self.device.execute = Mock(side_effect=neg_execute)

        # Execute stage: change_boot_variable
        with self.assertRaises(TerminateStepSignal):
            change_boot_variable(self.section, self.steps, self.device,
                                 **self.device.clean.change_boot_variable)


    def test_stage_write_erase(self):
        self.device.execute = Mock(return_value=self.raw_output.write_erase,
                                   error_pattern=['^%\\s*[Ii]nvalid (command|input)'])

        # Execute stage: write_erase
        with self.assertRaises(TerminateStepSignal):
            write_erase(self.section, self.steps, self.device,
                        **self.device.clean.write_erase)


    def test_stage_reload1(self):
        self.device.reload = Mock(side_effect=SubCommandFailure("negative test"))

        # Execute stage: reload
        with self.assertRaises(TerminateStepSignal):
            reload(self.section, self.steps, self.device,
                    **self.device.clean.reload)


    def test_stage_reload2(self):
        self.device.reload = Mock(return_value=self.raw_output.reload_output)
        self.device.destroy = Mock(return_value="")
        self.device.connect = Mock(side_effect=KeyError("negative test"))
        self.device.parse = Mock(side_effect=pos_parsed)

        # Execute stage: reload
        with self.assertRaises(TerminateStepSignal):
            reload(self.section, self.steps, self.device,
                    **self.device.clean.reload)


    def test_stage_reload3(self):
        self.device.reload = Mock(return_value=self.raw_output.reload_output)
        self.device.destroy = Mock(return_value="")
        self.device.connect = Mock(return_value=self.raw_output.reload_connect)
        self.device.parse = Mock(side_effect={})

        # Execute stage: reload
        with self.assertRaises(TerminateStepSignal):
            reload(self.section, self.steps, self.device,
                    **self.device.clean.reload)


    def test_stage_apply_configuration1(self):
        self.device.configure = Mock(side_effect=KeyError('negative test'))
        self.device.destroy = Mock(return_value="")
        self.device.connect = Mock(return_value=self.raw_output.connect)
        
        # Execute stage: apply_configuration
        with self.assertRaises(TerminateStepSignal):
            apply_configuration(self.section, self.steps, self.device,
                                **self.device.clean.apply_configuration)


    def test_stage_apply_configuration2(self):
        self.device.configure = Mock(side_effect=StateMachineError('negative test'))
        self.device.destroy = Mock(return_value="")
        self.device.connect = Mock(return_value=self.raw_output.connect)
        self.device.execute = Mock(return_value="")
        
        # Execute stage: apply_configuration
        with self.assertRaises(TerminateStepSignal):
            apply_configuration(self.section, self.steps, self.device,
                                **self.device.clean.apply_configuration)


    def test_stage_verify_running_image(self):
        self.device.parse = Mock(side_effect=neg_parsed)

        # Execute stage: verify_running_image
        with self.assertRaises(TerminateStepSignal):
            verify_running_image(self.section, self.steps, self.device,
                                 **self.device.clean.verify_running_image)


if __name__ == '__main__':
    unittest.main()
