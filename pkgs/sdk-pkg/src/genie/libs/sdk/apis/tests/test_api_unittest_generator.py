from unittest import TestCase
from unittest.mock import Mock, MagicMock, patch, mock_open
from collections import ChainMap
from genie.libs.sdk.apis.api_unittest_generator import (
    APIUTGenerator, TestGenerator, TestFactory,
    ParserTestGenerator, ConfigureTestGenerator, ExecuteTestGenerator
)
from genie.libs.sdk.apis.api_unittest_generator import Path
from unicon.core.errors import ConnectionError
import pprint
import os
from datetime import datetime
from inspect import getmembers, isfunction

TEST_ARGS_YAML = {
    'default': {
        'arguments': {
            'interface': 'GigabitEthernet1',
            'interface_list': ['GigabitEthernet1'],
            'ip_address': '172.16.1.139'
        }
    },
    'get_interface_carrier_delay': {
        'arguments': [
            {
                'delay_type': 'up',
                'expected_output': None
            },
            {
                'delay_type': 'down',
                'expected_output': 'blah'
            }
        ]
    }
}

class TestParserGenerator(TestCase):
    def setUp(self):
        self.device = Mock()
        self.device.name = 'fake_device'
        self.device.os = 'fake_os'
        self.device.platform = 'fake_platform'
        self.device.type = 'fake_type'
        self.module_import = 'mock_module'
        self.api = Mock()
        self.api.__name__ = 'mock_api'
        self.test_generator = ParserTestGenerator(self.device, self.module_import, self.api)

    def test_build_imports(self):
        expected_imports = [
            'import os',
            'from pyats.topology import loader',
            'from unittest import TestCase',
            'from mock_module import mock_api'
        ]
        self.assertEqual(self.test_generator._build_imports(), expected_imports)

    def test_build_test_class(self):
        expected_class = {
            'api': 'mock_api',
            'class_name': 'TestMockApi',
            'device': 'fake_device',
            'imports': [
                'import os',
                'from pyats.topology import loader',
                'from unittest import TestCase',
                'from mock_module import mock_api'
            ]
        }
        self.assertEqual(self.test_generator.build_test_class(), expected_class)

    def test_build_test_method(self):
        arguments = 'arg1, arg2'
        result = {'key': 'value'}
        expected_method = {
            'api': 'mock_api',
            'arguments': arguments,
            'expected_output': pprint.pformat(result)
        }
        self.assertEqual(self.test_generator.build_test_method(arguments, result), expected_method)

    def test_build_write_args(self):
        arguments = ['arg1', 'arg2']
        varargs = ['var1']
        kwargs = {'kwarg1': 'value1'}
        expected_args = "'arg1', 'arg2', var1, kwarg1='value1'"
        self.assertEqual(self.test_generator.build_write_args(arguments, varargs, kwargs), expected_args)

        self.assertEqual(
            self.test_generator.build_write_args([self.device], (), {}),
            'self.device'
        )

        # test with existing arguments
        self.assertEqual(
            self.test_generator.build_write_args(['intf1', 'abcd'], (), {}),
            "'intf1', 'abcd'"
        )

        # test with empty arguments
        self.assertEqual(self.test_generator.build_write_args([], (), {}), '')

    def test_create_testbed(self):
        self.maxDiff = None
        self.assertEqual(
            self.test_generator._create_testbed(),
            {               
            'cmd':
                'mock_device_cli --os fake_os '
                '--mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect',
            'device': 'fake_device',
            'has_mock_data': True,
            'os': 'fake_os',
            'platform': 'fake_platform',
            'type': 'fake_type',
            }
        )

class TestConfigureGenerator(TestCase):
    def setUp(self):
        self.device = Mock()
        self.device.name = 'fake_device'
        self.device.os = 'fake_os'
        self.device.platform = 'fake_platform'
        self.device.type = 'fake_type'
        self.module_import = 'mock_module'
        self.api = Mock()
        self.api.__name__ = 'mock_api'
        self.test_generator = ConfigureTestGenerator(self.device, self.module_import, self.api)

    def test_build_imports(self):
        expected_imports = [
            'from unittest import TestCase',
            'from mock_module import mock_api',
            'from unittest.mock import Mock'
        ]
        self.assertEqual(self.test_generator._build_imports(), expected_imports)

    def test_build_test_class(self):
        expected_class = {
            'api': 'mock_api',
            'class_name': 'TestMockApi',
            'device': 'fake_device',
            'imports': [
                'from unittest import TestCase',
                'from mock_module import mock_api',
                'from unittest.mock import Mock'
            ]
        }
        self.assertEqual(self.test_generator.build_test_class(), expected_class)

    @patch('genie.libs.sdk.apis.api_unittest_generator.dill')
    @patch('builtins.open', new_callable=mock_open)
    def test_create_mock_variables_configure(self, mock_open, mock_dill):
        self.test_generator.get_mock_data_file = Mock()
        mock_dill.load.return_value = {
            'configure': {
                "['ip access-list extended acl_in', 'permit ip any any']": [],
            },
        }

        self.assertEqual(
            self.test_generator._create_mock_variables(),
            {
                'test_type': 'configure',
                'configure_calls': [['ip access-list extended acl_in', 'permit ip any any']],
            }
        )

        mock_dill.load.return_value = {
            'configure': {
                "interface GigabitEthernet1\nno ip access-group acl_in in": [],
            },
        }

        self.assertEqual(
            self.test_generator._create_mock_variables(),
            {
                'test_type': 'configure',
                'configure_calls': [pprint.pformat("interface GigabitEthernet1\nno ip access-group acl_in in")],
            }
        )

class TestExecuteGenerator(TestCase):
    def setUp(self):
        self.device = Mock()
        self.device.name = 'fake_device'
        self.device.os = 'fake_os'
        self.device.platform = 'fake_platform'
        self.device.type = 'fake_type'
        self.module_import = 'mock_module'
        self.api = Mock()
        self.api.__name__ = 'mock_api'
        self.test_generator = ExecuteTestGenerator(self.device, self.module_import, self.api)

    def test_build_imports(self):
        expected_imports = [
            'from unittest import TestCase',
            'from mock_module import mock_api',
            'from unittest.mock import Mock'
        ]
        self.assertEqual(self.test_generator._build_imports(), expected_imports)

    def test_build_test_class(self):
        expected_class = {
            'api': 'mock_api',
            'class_name': 'TestMockApi',
            'device': 'fake_device',
            'imports': [
                'from unittest import TestCase',
                'from mock_module import mock_api',
                'from unittest.mock import Mock'
            ]
        }
        self.assertEqual(self.test_generator.build_test_class(), expected_class)

    @patch('genie.libs.sdk.apis.api_unittest_generator.dill')
    @patch('builtins.open', new_callable=mock_open)
    def test_create_mock_variables_execute(self, mock_open, mock_dill):
        self.test_generator.get_mock_data_file = Mock()
        mock_dill.load.return_value = {
            'execute': {
                'some_command': [{'output': 'some_output'}]
            }
        }

        self.assertEqual(
            self.test_generator._create_mock_variables(),
            {
                'test_type': 'execute',
                'execute_asserts': {'some_command': 'some_output'},
            }
        )


class TestTestFactory(TestCase):
    @patch('genie.libs.sdk.apis.api_unittest_generator.TestFactory._inspect_function')
    def test_select_test_generator(self, mock_inspect_function):
        mock_inspect_function.return_value = ['parse', 'execute']
        result = TestFactory.select_test_generator('device', 'mock_import', 'mock_function')

        self.assertIsInstance(result, ParserTestGenerator)
        mock_inspect_function.assert_called_once_with('mock_function', 'device')

        mock_inspect_function.return_value = ['execute', 'execute']
        result = TestFactory.select_test_generator('device', 'mock_import', 'mock_function')

        self.assertIsInstance(result, ExecuteTestGenerator)

        mock_inspect_function.return_value = ['configure']
        result = TestFactory.select_test_generator('device', 'mock_import', 'mock_function')

        # Assert the expected behavior
        self.assertIsInstance(result, ConfigureTestGenerator)

        mock_inspect_function.return_value = ['some_other_test']
        result = TestFactory.select_test_generator('device', 'mock_import', 'mock_function')
        self.assertIsInstance(result, ParserTestGenerator)

class TestTestGenerator(TestCase):

    def setUp(self):
        self.device = Mock()
        self.device.name = 'mock_device'
        self.module_import = 'mock_module'
        self.api = Mock()
        self.api.__name__ = 'mock_api'
        self.test_generator = TestGenerator(self.device, self.module_import, self.api)

    def test_build_imports(self):
        expected_imports = [
            'from unittest import TestCase',
            'from mock_module import mock_api'
        ]
        self.assertEqual(self.test_generator._build_imports(), expected_imports)

    def test_build_test_class(self):
        expected_class = {
            'api': 'mock_api',
            'class_name': 'TestMockApi',
            'device': 'mock_device',
            'imports': [
                'from unittest import TestCase',
                'from mock_module import mock_api'
            ]
        }
        self.assertEqual(self.test_generator.build_test_class(), expected_class)

    def test_build_test_method(self):
        arguments = 'arg1, arg2'
        result = {'key': 'value'}
        expected_method = {
            'api': 'mock_api',
            'arguments': arguments,
            'expected_output': pprint.pformat(result)
        }
        self.assertEqual(self.test_generator.build_test_method(arguments, result), expected_method)

    def test_build_write_args(self):
        arguments = ['arg1', 'arg2']
        varargs = ['var1']
        kwargs = {'kwarg1': 'value1'}
        expected_args = "'arg1', 'arg2', var1, kwarg1='value1'"
        self.assertEqual(self.test_generator.build_write_args(arguments, varargs, kwargs), expected_args)

        self.assertEqual(
            self.test_generator.build_write_args([self.device], (), {}),
            'self.device'
        )

        # test with existing arguments
        self.assertEqual(
            self.test_generator.build_write_args(['intf1', 'abcd'], (), {}),
            "'intf1', 'abcd'"
        )

        # test with empty arguments
        self.assertEqual(self.test_generator.build_write_args([], (), {}), '')

    @patch('os.path.join', side_effect=lambda *args: '/'.join(args))
    @patch('builtins.open', new_callable=mock_open)
    def test_create_test_files(self, mock_open, mock_path_join):
        mock_test_file_data = {'key': 'mock_api'}
        mock_template = MagicMock()
        api = mock_test_file_data["key"]
        mock_destination = f'mock_destination'
        
        # Mock the behavior of the template rendering if necessary
        mock_template.render.return_value = 'rendered content'
        
        self.test_generator.create_test_files(mock_test_file_data, mock_template, mock_destination)
        
        expected_destination = f'mock_destination/{api}'
        mock_path_join.assert_called_with(expected_destination, f'test_api_{api}.py')
        expected_path = f'{expected_destination}/test_api_{api}.py'
        mock_open.assert_called_with(expected_path, 'w')
        mock_open().write.assert_called_with('rendered content')

    @patch('genie.libs.sdk.apis.api_unittest_generator.TEMP_DIR', new='/mock_temp_dir')
    def test_get_mock_data_file(self):
        expected_path = '/mock_temp_dir/mock_device'
        
        self.assertEqual(self.test_generator.get_mock_data_file(), expected_path)

    def test_get_api_expected_output(self):
        self.assertEqual(self.test_generator.get_api_expected_output(TEST_ARGS_YAML, None), None)
        self.test_generator.api = Mock()
        self.test_generator.api.__name__ = 'get_interface_carrier_delay'
        self.assertEqual(self.test_generator.get_api_expected_output(TEST_ARGS_YAML, None, index=1), 'blah')
        

class TestAPIUTGenerator(TestCase):

    def setUp(self):
        self.testbed = MagicMock()
        self.device = MagicMock()
        self.device.name = 'fake_device'
        self.device.os.return_value = 'fake_os'
        self.device.platform = 'fake_platform'
        self.device.type = 'fake_type'
        self.testbed.devices.__getitem__.return_value = self.device

    def test_load_arguments(self):
        test_args = 'interface:intf1,another_var:abcd'

        # skips module import
        with patch.object(APIUTGenerator, '_get_apis'):
            ut_gen = APIUTGenerator(
                testbed=self.testbed,
                device='blah',
                module='interface.get',
                api='get_bundled_interface',
                test_arguments=test_args
            )
        expected_arguments = {
            'default': {
                'arguments': {
                    'interface': 'intf1',
                    'another_var': 'abcd'
                }
            }
        }
        self.assertEqual(ut_gen.test_arguments, expected_arguments)

    def test_load_arguments_yaml(self):

        test_args_yaml = 'fakepath/ta.yaml'

        # skips module import
        with patch.object(APIUTGenerator, '_get_apis'):
            with patch("builtins.open", mock_open()) as mo:
                mo.return_value = MagicMock()
                # mock loading a yaml file
                with patch("yaml.load") as md:
                    md.return_value = TEST_ARGS_YAML
                    ut_gen = APIUTGenerator(
                        testbed=self.testbed,
                        device='blah',
                        module='interface.get',
                        test_arguments_yaml=test_args_yaml
                    )
        expected_arguments = {
            'default': {
                'arguments': {
                    'interface': 'GigabitEthernet1',
                    'interface_list': ['GigabitEthernet1'],
                    'ip_address': '172.16.1.139'
                }
            },
            'get_interface_carrier_delay': {
                'arguments': [
                    {
                        'delay_type': 'up',
                        'expected_output': None
                    },
                    {
                        'delay_type': 'down',
                        'expected_output': 'blah'
                    }
                ]
            }
        }
        # make sure all tests have the key "arguments"
        self.assertTrue(all(
                'arguments' in ut_gen.test_arguments[k]
                for k in ut_gen.test_arguments.keys()
            )
        )
        self.assertEqual(ut_gen.test_arguments, expected_arguments)

    def test_load_arguments_yaml_no_default(self):

        test_args_yaml = 'fakepath/ta.yaml'

        # skips module import
        with patch.object(APIUTGenerator, '_get_apis'):
            with patch("builtins.open", mock_open()) as mo:
                mo.return_value = MagicMock()
                # mock loading a yaml file
                with patch("yaml.load") as md:
                    md.return_value = {
                        'get_interface_carrier_delay': {
                            'arguments': {
                                'delay_type': 'up',
                            }
                        }
                    }
                    ut_gen = APIUTGenerator(
                        testbed=self.testbed,
                        device='blah',
                        module='interface.get',
                        test_arguments_yaml=test_args_yaml
                    )
        expected_arguments = {
            'get_interface_carrier_delay': {
                'arguments': {
                        'delay_type': 'up',
                }
            }
        }

        self.assertEqual(ut_gen.test_arguments, expected_arguments)

