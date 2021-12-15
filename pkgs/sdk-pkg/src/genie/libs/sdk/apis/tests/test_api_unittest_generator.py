from unittest import TestCase
from unittest.mock import MagicMock, patch, mock_open
from collections import ChainMap
from genie.libs.sdk.apis.api_unittest_generator import TestGenerator
from genie.libs.sdk.apis.api_unittest_generator import Path

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


class TestAPIUnittestGenerator(TestCase):

    def setUp(self):
        self.testbed = MagicMock()
        self.device = MagicMock()
        self.device.name = 'fake_device'
        self.device.os = 'fake_os'
        self.device.platform = 'fake_platform'
        self.device.type = 'fake_type'
        self.testbed.devices.__getitem__.return_value = self.device

    def test_load_arguments(self):
        test_args = 'interface:intf1,another_var:abcd'

        # skips module import
        with patch.object(TestGenerator, '_get_apis'):
            ut_gen = TestGenerator(
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
        with patch.object(TestGenerator, '_get_apis'):
            with patch("builtins.open", mock_open()) as mo:
                mo.return_value = MagicMock()
                # mock loading a yaml file
                with patch("yaml.load") as md:
                    md.return_value = TEST_ARGS_YAML
                    ut_gen = TestGenerator(
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

    def test_get_api_expected_output(self):
        # skipping __init__ as it is not necessary for this test
        with patch.object(TestGenerator, '__init__') as mt:
            mt.return_value = None
            ut_gen = TestGenerator()
            ut_gen.test_arguments = TEST_ARGS_YAML

        self.assertEqual(
            ut_gen._get_api_expected_output('get_interface_carrier_delay'),
            None)
        self.assertEqual(
            ut_gen._get_api_expected_output(
                'get_interface_carrier_delay', index=1),
            'blah')

    def test_build_api_args(self):
        test_args = 'interface:intf1,another_arg:abcd'

        # skips module import
        with patch.object(TestGenerator, '_get_apis'):
            ut_gen = TestGenerator(
                testbed=self.testbed,
                device='blah',
                module='interface.get',
                api='get_bundled_interface',
                test_arguments=test_args
            )

        # test with device as an argument
        # get_bundled_interface(device)
        self.assertEqual(
            ut_gen._build_api_args(
                'get_bundled_interface',
                ['device'],
                '',
                '',
                None
            ),
            [([self.device], (), {})]
        )

        # test with existing and default arguments
        # get_bundled_interface(interface, another_arg, test=None)
        self.assertEqual(
            ut_gen._build_api_args(
                'get_bundled_interface',
                ['interface', 'another_arg', 'test'],
                '',
                '',
                (None,)  # None is a default argument
            ),
            [(['intf1', 'abcd', None], (), {})]
        )

        # test with non-existing arguments
        # get_bundled_interface()
        self.assertEqual(
            ut_gen._build_api_args(
                'get_bundled_interface',
                ['not_an_arg'],
                '',
                '',
                None
            ),
            [([], (), {})]
        )

    def test_build_api_varargs(self):
        test_args = 'interface:intf1,another_arg:abcd'

        # skips module import
        with patch.object(TestGenerator, '_get_apis'):
            ut_gen = TestGenerator(
                testbed=self.testbed,
                device='blah',
                module='fake_module.get',
                api='get_var_args_test',
                test_arguments=test_args
            )
            ut_gen.test_arguments = {
                'default': {
                    'arguments': {
                        'arg1': 'some_arg',
                        'arg2': [1, 2, 3]
                    }
                }
            }

        # test with positional arguments
        # get_var_args_test(arg1, *arg2)
        self.assertEqual(
            ut_gen._build_api_args(
                'get_var_args_test',
                ['arg1'],
                'arg2',
                '',
                None
            ),
            [(['some_arg'], (1, 2, 3), {})]
        )

    def test_build_api_kwargs(self):
        # skips module import
        with patch.object(TestGenerator, '_get_apis'):
            ut_gen = TestGenerator(
                testbed=self.testbed,
                device='blah',
                module='jinja.get',
                api='load_jinja_template',
                test_arguments_yaml=''
            )
            ut_gen.test_arguments = {
                'default': {
                    'arguments': {
                        'path': '',
                        'file': 'interface.j2',
                        'kwargs': {
                            'interface': '',
                            'desc': 'test description'
                        }
                    }
                }
            }

        # test with keyword arguments
        # load_jinja_template(path, file, **kwargs)
        self.assertEqual(
            ut_gen._build_api_args(
                'load_jinja_template',
                ['path', 'file'],
                '',
                'kwargs',
                None
            ),
            [(
                ['', 'interface.j2'],  # args
                (),  # positional args
                {'interface': '', 'desc': 'test description'}  # kwargs
            )]
        )

    def test_build_test_class(self):
        # skipping __init__ as it is not necessary for this test
        with patch.object(TestGenerator, '__init__') as mt:
            mt.return_value = None
            ut_gen = TestGenerator()
        ut_gen.test_arguments = TEST_ARGS_YAML
        ut_gen.module_import = 'fake_module'
        ut_gen.device = self.device

        expected_test_class = {
            'api': 'get_fake_api',
            'class_name': 'TestGetFakeApi',
            'device': 'fake_device',
            'imports': [
                'import unittest',
                'from pyats.topology import loader',
                'from fake_module import get_fake_api'
            ]
        }

        self.assertEqual(
            ut_gen._build_test_class('get_fake_api'),
            expected_test_class
        )

    def test_build_test_method(self):
        arguments = 'a=1, b=2, c="3"'
        api_name = 'get_interface_names'
        value = 'abc'

        # skipping __init__ as it is not necessary for this test
        with patch.object(TestGenerator, '__init__') as mt:
            mt.return_value = None
            ut_gen = TestGenerator()

        self.assertEqual(
            ut_gen._build_test_method(api_name, arguments, value),
            {
                'api': 'get_interface_names',
                'arguments': 'a=1, b=2, c="3"',
                'expected_output': "'abc'"
            }
        )

        pass

    def test_build_write_args(self):
        # skipping __init__ as it is not necessary for this test
        with patch.object(TestGenerator, '__init__') as mt:
            mt.return_value = None
            ut_gen = TestGenerator()
            ut_gen.device = self.device

        # test with device as an argument
        self.assertEqual(
            ut_gen._build_write_args(
                [self.device],
                (),
                {}
            ),
            'self.device'
        )

        # test with existing arguments
        self.assertEqual(
            ut_gen._build_write_args(
                ['intf1', 'abcd'],
                (),
                {}
            ),
            "'intf1', 'abcd'"
        )

        # test with empty arguments
        self.assertEqual(
            ut_gen._build_write_args([], (), {}),
            ''
        )

    def test_create_testbed(self):
        # skipping __init__ as it is not necessary for this test
        with patch.object(TestGenerator, '__init__') as mt:
            mt.return_value = None
            ut_gen = TestGenerator()
        ut_gen.device = self.device

        self.assertEqual(
            ut_gen._create_testbed(),
            {
                'cmd':
                    'mock_device_cli --os fake_os '
                    '--mock_data_dir mock_data --state connect',
                'device': 'fake_device',
                'os': 'fake_os',
                'platform': 'fake_platform',
                'type': 'fake_type',
            }
        )

    def test_get_test_arguments(self):
        # skipping __init__ as it is not necessary for this test
        with patch.object(TestGenerator, '__init__') as mt:
            mt.return_value = None
            ut_gen = TestGenerator()
        ut_gen.test_arguments = TEST_ARGS_YAML

        # test with an api in test arguments yaml
        self.assertEqual(
            ut_gen._get_test_arguments('get_interface_carrier_delay'),
            [
                ChainMap(
                    {'delay_type': 'up', 'expected_output': None},
                    {'interface': 'GigabitEthernet1',
                     'interface_list': ['GigabitEthernet1'],
                     'ip_address': '172.16.1.139'}),
                ChainMap(
                    {'delay_type': 'down', 'expected_output': 'blah'},
                    {'interface': 'GigabitEthernet1',
                     'interface_list': ['GigabitEthernet1'],
                     'ip_address': '172.16.1.139'})
            ]
        )

        # test with an api not in test arguments yaml
        self.assertEqual(
            ut_gen._get_test_arguments('get_some_random_api'),
            [
                ChainMap({
                    'interface': 'GigabitEthernet1',
                    'interface_list': ['GigabitEthernet1'],
                    'ip_address': '172.16.1.139'
                })
            ]
        )

    @patch('genie.libs.sdk.apis.api_unittest_generator.importlib')
    def test_get_apis_single_api(self, mock_import):
        # skipping __init__ as it is not necessary for this test
        with patch.object(TestGenerator, '__init__') as mt:
            mt.return_value = None
            ut_gen = TestGenerator()
        ut_gen.device = self.device
        ut_gen.exclude_apis = []

        # assert with single API
        mock_import.util.find_spec.return_value = ''
        ut_gen.module = \
            mock_import.import_module.return_value = MagicMock()
        ut_gen.module.fake_api_1 = 'fake_api_1'
        apis = ut_gen._get_apis(module='interface.get', api='fake_api_1')

        self.assertEqual(
            apis,
            [('fake_api_1', ut_gen.module.fake_api_1)]
        )

    @patch('genie.libs.sdk.apis.api_unittest_generator.importlib')
    @patch('genie.libs.sdk.apis.api_unittest_generator.getmembers')
    def test_get_apis_module(self, mock_members, mock_import):
        # skipping __init__ as it is not necessary for this test
        with patch.object(TestGenerator, '__init__') as mt:
            mt.return_value = None
            ut_gen = TestGenerator()
        ut_gen.device = self.device
        ut_gen.exclude_apis = {}

        # assert getting all APIs
        mock_import.util.find_spec.return_value = ''
        ut_gen.module = \
            mock_import.import_module.return_value = MagicMock()

        mock_members.return_value = [
            ('fake_api_1', 'fake_api_1'),
            ('fake_api_2', 'fake_api_2')]

        apis = ut_gen._get_apis(module='interface.get')
        self.assertEqual(
            apis,
            [('fake_api_1', 'fake_api_1'),
             ('fake_api_2', 'fake_api_2')]
        )

        # assert getting APIs with exclude
        ut_gen.exclude_apis = {'regex': '_1'}
        apis = ut_gen._get_apis(module='interface.get')
        self.assertEqual(
            apis,
            [('fake_api_2', 'fake_api_2')]
        )

    @patch.object(Path, 'is_file')
    @patch('genie.libs.sdk.apis.api_unittest_generator.importlib')
    def test_get_apis_module_path(self, mock_import, mock_is_file):
        # skipping __init__ as it is not necessary for this test
        with patch.object(TestGenerator, '__init__') as mt:
            mt.return_value = None
            ut_gen = TestGenerator()
        ut_gen.device = self.device
        ut_gen.exclude_apis = {}

        path_1 = 'somepath/genie/libs/sdk/apis/nxos/interface/get.py'
        mock_is_file.return_value = True
        ut_gen._get_apis(module_path=path_1)

        # assert module path
        self.assertEqual(
            ut_gen.module_import,
            'genie.libs.sdk.apis.nxos.interface.get'
        )
        # assert default path
        self.assertEqual(
            ut_gen.destination,
            'tests/nxos/interface/get'
        )

        path_2 = 'somepath/genielibs/src/sdk/apis/iosxe/interface/verify.py'
        ut_gen._get_apis(module_path=path_2, destination='fake_folder')
        # assert module path
        self.assertEqual(
            ut_gen.module_import,
            'genie.libs.sdk.apis.iosxe.interface.verify'
        )

        # assert with different destination
        self.assertEqual(
            ut_gen.destination,
            'fake_folder/iosxe/interface/verify'
        )

        path_3 = 'somepath/genielibs/src/sdk/apis/jinja/utils.py'
        ut_gen._get_apis(module_path=path_3)
        # assert module path
        self.assertEqual(
            ut_gen.module_import,
            'genie.libs.sdk.apis.jinja.utils'
        )
