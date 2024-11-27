from __future__ import annotations
import argparse
import ast
import dill
import importlib
import inspect
import logging
import os
import pprint
import re
import shutil
import sys
import yaml

from collections import ChainMap
from datetime import datetime
from inspect import getmembers, getfullargspec, isfunction
from jinja2 import Environment, FileSystemLoader
from pathlib import Path

from pyats.topology import loader
from unicon.core.errors import ConnectionError

logger = logging.getLogger('api_unittest_generator')

# uses timestamp to avoid writing over existing folder
TEMP_DIR = '/tmp/test_generator_{}'.\
    format(datetime.now().strftime('%Y%m%d%H%m%s'))

# jinja template files
TEMPLATE_FOLDER = os.path.join(os.path.dirname(__file__), 'test_templates')
TEMPLATE_TEST = 'test_api.py.jinja'

# test file name prefix for API tests generated
TEST_FILE_NAME_PREFIX = 'test_api_'

MOCK_DATA_FOLDER = 'mock_data'
MOCK_DATA_FILE_NAME = 'mock_data.yaml'

DEFAULT_HEADER_WIDTH = 80
DEFAULT_DESTINATION = os.path.join(os.path.dirname(__file__), 'tests')

# method to simplify printing Report headers
def print_header(title):
    logger.info('='*DEFAULT_HEADER_WIDTH)
    logger.info(title.center(DEFAULT_HEADER_WIDTH))
    logger.info('='*DEFAULT_HEADER_WIDTH)


class TestReport:
    def __init__(self, *args, **kwargs):
        self._tests = {'passed': {}, 'failed': {}}
        self.start_time = datetime.now()
        self.end_time = None

    def add_test_result(self, values, success:bool):
        """
        Adds API test to a dictionary containing successful tests

        Args:
            values (dict): all key-value pairs to add
            success (bool): if it is a successful test or a failure
        Returns:
            None
        """
        test_result = 'passed' if success else 'failed'
        self._tests[test_result].update(values)

    def print_results(self, *args, **kwargs):
        """
        Prints report displaying Test results.

        Returns:
            None
        """
        # if test has not finished, set end time
        if not self.end_time:
            self.end_time = datetime.now()

        print_header('Test Generator Results')
        time_elapsed = self.end_time - self.start_time

        tests_passed = len(self._tests['passed'])
        tests_failed = len(self._tests['failed'])

        tests_processed = tests_passed + tests_failed

        tests_pass_percent = (tests_passed / tests_processed)*100 \
            if tests_processed > 0 else 0

        tests_fail_percent = (tests_failed / tests_processed)*100 \
            if tests_processed > 0 else 0

        if 'destination' in kwargs:
            logger.info('Destination Folder: {}'.format(kwargs['destination']))

        # tests were generated in a different root folder
        if 'base_destination' in kwargs:
            logger.warning(
                'Tests were not generated using the proper test folder structure.\n'
                'Found: {}\n'
                'Expected: {}'
                .format(kwargs['base_destination'], DEFAULT_DESTINATION)
            )

        logger.info('APIs processed: {}'.format(tests_processed))
        logger.info('Time elapsed: {}'.format(time_elapsed))

        logger.info('Tests Created: {}({}%)'.
                    format(tests_passed, tests_pass_percent))

        logger.info('Tests Not Created: {}({}%)'.
                    format(tests_failed, tests_fail_percent))

        if tests_failed > 0:
            print_header('Tests Not Created')

            for k, v in self._tests['failed'].items():
                logger.info('{}: {}'.format(k, v))

        logger.info('='*DEFAULT_HEADER_WIDTH)
        logger.warning('Tests have been generated but still need to be executed to ensure they work correctly.')
        logger.warning('To run the tests, navigate to the folder created by the script and use the following command:')
        logger.warning('python -m unittest test_*.py')
        logger.info('='*DEFAULT_HEADER_WIDTH)


class MethodCallVisitor(ast.NodeVisitor):
    def __init__(self, device_class_name):
        self.device_class_name = device_class_name
        self.calls = []

    def visit_Call(self, node):
        if isinstance(node.func, ast.Attribute):
            if isinstance(node.func.value, ast.Name) and node.func.value.id == self.device_class_name:
                self.calls.append(node.func.attr)
        self.generic_visit(node)


class TestGenerator:
    def __init__(self, device, module_import, api):
        self.device = device
        self.module_import = module_import
        self.api = api

    def _build_imports(self):
        return [
            'from unittest import TestCase',
            'from {} import {}'.format(self.module_import, self.api.__name__)
        ]

    def build_test_class(self):
        """
        Creates a test class for the given API.

        Returns:
            dict: a dictionary containing the file content.
        """

        api_name = self.api.__name__

        # load module into unit test
        # Create setUpClass to connect to mocked device
        imports = self._build_imports()

        class_name = 'Test' + ''.join(
            [c.capitalize() for c in api_name.split('_')])

        ret_dict = {
            'api': api_name,
            'class_name': class_name,
            'device': self.device.name,
            'imports': imports,
        }

        return ret_dict

    def build_test_method(self, arguments, result):
        """
        Creates a test method for the given API and its arguments.

        Args:
            api_name (str): The name of the API.
            arguments (str): A comma-separated string containing test arguments
            result: the output of the API call
        Returns:
            dict: Arguments to render a test method in the jinja template
        """
        expected_output = pprint.pformat(result)

        ret_dict = {
            'api': self.api.__name__,
            'arguments': arguments,
            'expected_output': expected_output
        }

        return ret_dict

    def build_write_args(self, arguments, varargs, kwargs):
        """
        Builds a string containing all arguments used in a test.

        Args:
            arguments (dict): The arguments necessary to run the test
            varargs (dict): Positional arguments necessary to run the test
            kwargs (dict): Keyword arguments necessary to run the test
        Returns:
            str: a string containing all arguments used in the API call
        """

        write_args = []

        for value in arguments:
            if value == self.device:
                arg_value = 'self.device'
            else:
                arg_value = pprint.pformat(value)
            write_args.append('{}'.format(arg_value))
        if varargs:
            for var in varargs:
                write_args.append('{}'.format(var))
        if kwargs:
            for key, value in kwargs.items():
                arg_value = pprint.pformat(value)
                write_args.append('{}={}'.format(key, arg_value))

        return ', '.join(write_args)

    def create_test_files(self, test_file_data:dict, template:"Template", destination:str):
        """
        Arguments:
            test_file_data (dict): Dictionary containing all data required to build the test script
            template (Template): Jinja template
        """
        api_folder = os.path.join(destination, self.api.__name__)

        Path(api_folder).mkdir(parents=True, exist_ok=True)
            
        # create empty __init__.py file
        with open(os.path.join(api_folder, '__init__.py'), 'w'): pass

        file_name = os.path.join(
            api_folder, f'{TEST_FILE_NAME_PREFIX}{self.api.__name__}.py')

        # generate file content from jinja template
        content = template.render(test_file_data)
        with open(file_name, 'w') as tf:
            tf.write(content)

    def get_api_expected_output(self, arguments, api_result, index=0):
        api = arguments.get(self.api.__name__, {})
        if 'arguments' in api:
            if isinstance(api['arguments'], list):
                test_instance = api['arguments'][index]
            else:
                test_instance = api['arguments']
            # if expected output is provided, return it
            # if not, use API result instead
            if expected_result := test_instance.get('expected_output'):
                return expected_result
            else:
                return api_result
        return None

    def get_mock_data_file(self):
        # collects data from pickle file with device name
        return os.path.join(TEMP_DIR, self.device.name)


class ParserTestGenerator(TestGenerator):
    """
    This is the original test generator.
    It uses unicon recordings to generate mock data and unit tests that load them to compare outputs
    """
    def _build_imports(self):
        imports = ['import os', 'from pyats.topology import loader']
        imports.extend(super()._build_imports())
        return imports

    def _create_testbed(self):
        """
        Creates the testbed file used to connect to the mock data.

        Args:
            api_name (str): the name of the API
            mock_data_path (str): the path to the mock data folder
        Returns:
            None
        """

        cmd = 'mock_device_cli --os {} --mock_data_dir {{os.path.dirname(__file__)}}/{} --state connect'.\
            format(self.device.os, MOCK_DATA_FOLDER)

        tb_info = {
            'cmd': cmd,
            'device': self.device.name,
            'os': self.device.os,
            'platform': self.device.platform,
            'type': self.device.type,
            'has_mock_data': True
        }

        return tb_info

    def _create_mock_data(self, destination, router='switch'):
        """
        Creates mock data YAML file and corresponding testbed file

        Args:
            api_name (str): name of the API
            router (str): name of the router/hostname
        Returns:
            None
        """

        # creates data YAML file and testbed file
        mock_data_path = os.path.join(
            destination, self.api.__name__, MOCK_DATA_FOLDER)
        outfile = os.path.join(
            mock_data_path, self.device.os, MOCK_DATA_FILE_NAME)

        # collects data from pickle file with device name
        file_name = self.get_mock_data_file()

        self.device.create_yaml(
            file_name, router, outfile, allow_repeated_commands=True)

    def create_test_files(self, test_file_data:dict, template:"Template", destination:str):
        """
        Arguments:
            test_file_data (dict): Dictionary containing all data required to build the test script
            template (Template): Jinja template
            destination (str): Test's parent folder
        """
        test_file_data.update(self._create_testbed())

        super().create_test_files(test_file_data, template, destination)

        # create mock data and testbed file for test cases
        self._create_mock_data(destination, router=self.device.hostname)


class ConfigureTestGenerator(TestGenerator):
    def _build_imports(self):
        imports = super()._build_imports()
        imports.append('from unittest.mock import Mock')
        return imports

    def _create_mock_variables(self):
        data_path = self.get_mock_data_file()

        with open(data_path, 'rb') as f:
            data = dill.load(f)

        configure_calls = []

        for cli, _ in data['configure'].items():
            # breaks multiple commands into a list of commands
            # e.g. ['ip access-list extended acl_in', 'permit ip any any']
            if cli.startswith('[') or cli.endswith(']'):
                # if multiple commands, create one key for each command
                configure_calls.append([c.strip() for c in cli.replace("'", '').strip("']['").split(',')])
            else:
                configure_calls.append(pprint.pformat(cli))

        return {
            'test_type': 'configure',
            'configure_calls': configure_calls
        }

    def create_test_files(self, test_file_data: dict, template: "Template", destination: str):
        test_file_data.update(self._create_mock_variables())
        print('This is the test_file_data:', test_file_data)
        return super().create_test_files(test_file_data, template, destination)


class ExecuteTestGenerator(TestGenerator):
    def _build_imports(self):
        imports = super()._build_imports()
        imports.append('from unittest.mock import Mock')
        return imports

    def _create_mock_variables(self):
        data_path = self.get_mock_data_file()

        with open(data_path, 'rb') as f:
            data = dill.load(f)

        execute_asserts = {}

        for cli, output in data['execute'].items():
            if cli in 'show version':
                continue
            # gets only first output recorded for a command
            # this might not work on all cases
            execute_asserts[cli] = output[0]['output']
        return {
            'test_type': 'execute',
            'execute_asserts': execute_asserts
        }

    def create_test_files(self, test_file_data: dict, template: "Template", destination: str):
        test_file_data.update(self._create_mock_variables())
        return super().create_test_files(test_file_data, template, destination)


class TestFactory:

    @classmethod
    def _inspect_function(cls, func, device_class_name):
        source = ast.parse(inspect.getsource(func))
        visitor = MethodCallVisitor(device_class_name)
        visitor.visit(source)
        return visitor.calls

    @classmethod
    def select_test_generator(cls, device, module_import, api):
        """
        Create a test object based on the API name.

        Args:
            device (obj): The device object.
            api_name (str): The name of the API.
            arguments (str): A comma-separated string containing test arguments.

        Returns:
            Test: An instance of the appropriate test class.
        """
        # extracts a list of all device method calls to determine which approach to use
        method_calls = cls._inspect_function(api, 'device')

        if 'parse' in method_calls:
            return ParserTestGenerator(device, module_import, api)
        elif 'execute' in method_calls:
            return ExecuteTestGenerator(device, module_import,api)
        elif 'configure' in method_calls:
            return ConfigureTestGenerator(device, module_import, api)
        else:
            # default generator for now
            return ParserTestGenerator(device, module_import, api)


class APIUTGenerator:
    def __init__(self,
                 testbed, device,
                 module=None, module_path=None,
                 api=None,
                 test_arguments=None, test_arguments_yaml=None,
                 destination=None):

        self.testbed = testbed
        try:
            self.device = self.testbed.devices[device]
        except KeyError as e:
            raise Exception("{} is not a valid device".format(device)) from e

        # if no destination is specified, create tests folder where this file is located
        destination = destination or DEFAULT_DESTINATION
        if destination != DEFAULT_DESTINATION:
            # store test root folder to warn user when report is printed
            self.base_destination = destination

        # records data from device and stores in temporary folder
        os.environ['UNICON_RECORD'] = TEMP_DIR

        self.exclude_apis = []
        self.apis = self._get_apis(
            module, module_path, api, destination)
        self.test_arguments = self._load_arguments(
            test_arguments, test_arguments_yaml)
        self.report = TestReport()
        self.template_env = Environment(loader=FileSystemLoader(TEMPLATE_FOLDER))

    def run(self):
        """
        Connect to a device and generate test files and data for a set of APIs.
        Create 1 or more tests per API.
        Create 1 mock_data file per API tested.
        """

        for api_name, api in self.apis:
            print_header('Generating tests for API {}'.format(api_name))
            api_args = self._build_api_args(api)

            test_generator = TestFactory.select_test_generator(
                self.device,
                self.module_import,
                api
            )

            test_info = test_generator.build_test_class()

            self._set_stored_data()

            test_class = test_info.setdefault('unit_tests', [])

            # generates a test for each item in the list of API arguments
            for index, test_arg in enumerate(api_args):
                report_result = {}
                expected_output = None
                try:
                    args, varargs, kwargs = test_arg
                    # api call result
                    api_result = api(*args, *varargs, **kwargs)
                    # if test arguments contain the expected output
                    # extract it from list of arguments
                    expected_output = test_generator.get_api_expected_output(self.test_arguments, api_result, index)
                except TypeError as t:
                    message = f'Update test-arguments YAML: {t}'
                    logger.warning(message)
                    report_result = {api_name: message}
                    self.report.add_test_result(report_result, success=False)
                    continue
                except Exception as e:
                    report_result = {api_name: e}
                    self.report.add_test_result(report_result, success=False)
                    continue

                if expected_output and expected_output != api_result:
                    # API result does not match expected_output
                    message = 'API result does not match expected output'
                    logger.warning(message)
                    # add to report as a failure
                    report_result = {api_name: message}
                    self.report.add_test_result(report_result, success=False)
                else:
                    arguments = test_generator.build_write_args(args, varargs, kwargs)
                    test_class.append(
                        test_generator.build_test_method(
                            arguments,
                            expected_output
                        )
                    )
                    report_result = {api_name: 'Created'}
                    self.report.add_test_result(report_result, success=True)

            # if there are tests to generate
            if test_class:
                test_generator.create_test_files(
                    test_file_data=test_info,
                    template=self.template_env.get_template(TEMPLATE_TEST),
                    destination=self.destination
                )
                # resets recording before next API call
                self._reset_stored_data()

        self.device.disconnect()

        # temp directory cleanup (if created)
        self._cleanup()

        print_args = {'destination': self.destination}
        # tests were generated in a folder other than the default
        if hasattr(self, 'base_destination'):
            print_args.update({'base_destination': self.base_destination})
        self.report.print_results(**print_args)

    def _build_api_args(self, api):
        """
        Creates list of test arguments for the given API.

        Args:
            api (obj): the API
        Returns:
            list: List of dictionaries with API arguments and values
        """
        def_args = {}
        args_list = []

        # get arguments from API reference
        argspec = getfullargspec(api)
        args = argspec.args
        varargs = argspec.varargs
        varkw = argspec.varkw
        defaults = argspec.defaults

        test_args_list = self._get_test_arguments(api.__name__)

        # if test arguments are not provided
        if not test_args_list:
            api_args = []
            if 'device' in args:
                api_args.append(self.device)
            args_list = [(api_args, (), {})]
            return args_list

        # get default values for when arguments are not provided
        if defaults:
            def_args = dict(zip(reversed(args), reversed(defaults)))

        # get test arguments values based on argument names
        for test_args_dict in test_args_list:
            api_args = []
            api_varargs = ()
            api_varkw = {}
            for arg in args:
                # devices are not listed as arguments
                # but needed to run the API
                if arg == 'device':
                    value = self.device
                elif arg in test_args_dict:
                    value = test_args_dict[arg]
                elif arg in def_args:
                    value = def_args[arg]
                else:
                    # if cannot find argument, ignore it
                    # if argument is needed, it will show up in the test report
                    continue
                api_args.append(value)
            if varargs and varargs in test_args_dict:
                api_varargs = tuple(test_args_dict[varargs])
            if varkw and varkw in test_args_dict:
                api_varkw = test_args_dict[varkw]
            args_list.append((api_args, api_varargs, api_varkw))

        return args_list 

    def _get_test_arguments(self, api_name):
        '''
        Gets tests arguments for the given API

        Args:
            api_name (str): The name of the API
        Returns:
            list: Arguments and values to run the API.
        '''

        test_args = []
        default = self.test_arguments.get('default', {}).\
            get('arguments', {})
        api_name = self.test_arguments.get(api_name, {}).\
            get('arguments')

        if api_name:
            if isinstance(api_name, list):
                # if multiple tests for the same API
                for test in api_name:
                    test_args.append(ChainMap(test, default))
            else:
                test_args.append(ChainMap(api_name, default))
        elif default:
            test_args.append(ChainMap(default))

        return test_args

    def _load_arguments(self, test_arguments=None, test_arguments_yaml=None):
        """
        Loads test arguments into the class instance.
        Args:
            test_arguments (str): comma-separated key-value pairs.
            test_arguments_yaml (str): a path to a YAML file
        Returns:
            dict: a dict containing the test arguments (if provided).
        """

        arguments = {}
        if test_arguments_yaml:
            try:
                with open(test_arguments_yaml) as f:
                    arguments = yaml.load(f, Loader=yaml.Loader)
                self.exclude_apis = arguments.pop('exclude', [])
            except Exception as e:
                logger.error("Failed to load test arguments")
                raise e
        elif test_arguments:
            # comma-separated key-value pairs e.g. 'x:a,y:b'
            # argument types will be strings
            args_dict = {}
            test_arguments = test_arguments.replace(', ', ',')
            items = test_arguments.split(',')
            for item in items:
                key, value = item.split(':', 1)
                args_dict[key] = value
            # add dictionary values to 'default' test arguments
            arguments['default'] = {
                'arguments': args_dict
            }
        return arguments

    def _get_apis(self, module=None, module_path=None,
                  api=None, destination='tests'):
        """
        Gets the list of APIs that will be processed.

        Args:
            module (str): The name of the module.
            module_path (str): The path to the module.
            api (str): The name of the API (optional)
            destination (str): The path to the destination folder.
        Returns:
            list: Tuples containing the API name and the API itself.
        """
        # path that will contain API folder structure
        destination_path = []

        # check if module is a filepath
        if module_path:
            # extracts folder structure to import in the unittest
            # will import it as genie module
            # e.g. genie.libs.sdk.apis.inteface.get
            try:
                _, genie_path, mod_path = module_path.partition(
                    'genie/libs/sdk/apis')
                if not genie_path:
                    _, genie_path, mod_path = module_path.partition(
                     'genielibs/src/sdk/apis')
                genie_path = 'genie.libs.sdk.apis'
            except Exception as e:
                logger.error(
                    "--module-path has to be a path to a genielibs module")
                raise e

            # ignore file extension
            mod_path, _ = os.path.splitext(mod_path)
            mod_path = mod_path.replace('/', '.')
            self.module_import = ''.join([genie_path, mod_path])

            module_path = Path(module_path)
            if module_path.is_file():
                # get module name, ignore extension
                module_name, _ = module_path.name.split('.')
                spec = importlib.util.spec_from_file_location(
                    module_name, module_path)
                self.module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(self.module)
                # folder structure that will be created for the module
                destination_path = os.path.dirname(module_path).split('/')
                # ignores anything before and including the os index
                base_folder_index = destination_path.index('apis')
                destination_path = destination_path[base_folder_index+1:]
                # add module parent folder
                destination_path.append(module_name)
            else:
                raise ValueError(
                    'A valid module path needs to be provided')
        elif module:
            # try importing lib without OS prefix
            lib_prefix = 'genie.libs.sdk.apis'
            import_string = '{}.{}'.format(
                lib_prefix, module)

            try:
                importlib.util.find_spec(import_string)
            except ModuleNotFoundError:
                # if it does not work, then use os
                import_string = '{}.{}.{}'.\
                    format(lib_prefix, self.device.os, module)
                # considers OS as part of the path
                destination_path.append(self.device.os)

            self.module = importlib.import_module(import_string)
            self.module_import = import_string

            # destination folder examples
            # e.g. iosxe.interface.get, jinja.get
            destination_path += module.split('.')

        self.destination = os.path.join(
            destination,
            *destination_path
        )

        # API list (api_name, api)
        if api:
            apis = [(api, getattr(self.module, api))]
        else:
            # get all APIs from module
            apis = getmembers(self.module, isfunction)

        if self.exclude_apis:
            # remove apis that match the exclude filter
            # filter can be regex or list of names
            if isinstance(self.exclude_apis, dict) \
               and 'regex' in self.exclude_apis:
                try:
                    r = re.compile(self.exclude_apis['regex'])
                except Exception as e:
                    # ignores filter if regex is incorrect
                    logger.warning('Skipped: Invalid Regex - {}'.format(e))
                    return apis

                # removes matches from the list of APIs
                apis = [a for a in apis if not re.search(r, a[0])]
            else:
                apis = [a for a in apis if a[0] not in self.exclude_apis]

        return apis

    def _cleanup(self):
        """Removes temp directory (if created)"""
        if os.path.isdir(TEMP_DIR):
            shutil.rmtree(TEMP_DIR)

    def _set_stored_data(self, folder=TEMP_DIR):
        """
        Connect to device and keep copy of connection data for mock_data files.
        """

        if not self.device.is_connected():
            try:
                self.device.connect(
                    learn_hostname=True,
                    init_config_commands=[],
                    init_exec_commands=[]
                )
            except ConnectionError as ce:
                # Proxy connection - not supported
                logger.error(
                    'Proxy Connection is not supported for Unicon recording.'
                    ' Please try to generate unit test without proxy')
                logger.error(ce)
                raise SystemExit
            else:
                # check if it is a single unicon connection
                if hasattr(self.device, 'stored_data') \
                  and not self.device.is_ha:
                    self._connected_data = self.device.stored_data.copy()
                    os.makedirs(folder, exist_ok=True)
                else:
                    self.device.disconnect()
                    self._cleanup()
                    raise Exception(
                        'Connection not supported: '
                        'only single Unicon connections are supported')

    def _reset_stored_data(self):
        """
        Reset device recording to keep only API-related data in the file.
        Add connection data back to the recording file after resetting it.

        Args:
            None
        Returns:
            None
        """

        # resets stored_data and recording file
        self.device.reset_recording()
        # adds connection data back to the recording
        self.device.update_stored_data(self._connected_data)


if __name__ == '__main__':
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)

    parser = argparse.ArgumentParser()

    parser.add_argument('--testbed-file',
                        dest='testbed',
                        metavar='[FILE]',
                        type=loader.load,
                        required=True,
                        help='Testbed file to load')

    parser.add_argument(
        "--device",
        nargs="?",
        required=True,
        help="Device name",
    )

    test_args_group = parser.add_mutually_exclusive_group()

    test_args_group.add_argument(
        "--test-arguments",
        nargs="?",
        default=None,
        help="comma-separated key-value pairs containing test arguments",
    )

    test_args_group.add_argument(
        "--test-arguments-yaml",
        nargs="?",
        default=None,
        help="YAML file containing test arguments",
    )

    module_group = parser.add_mutually_exclusive_group(required=True)

    module_group.add_argument(
        "--module",
        help="Name of a Module to create unit tests",
    )

    module_group.add_argument(
        "--module-path",
        help="Complete Path to a Module",
    )

    parser.add_argument(
        "--api",
        nargs="?",
        default=None,
        help="API to create single unit test",
    )

    parser.add_argument(
        "--destination",
        nargs="?",
        default=None,
        help="Path to folder where test folder will be created",
    )

    args = parser.parse_args()

    APIUTGenerator(
        args.testbed, args.device,
        module=args.module, module_path=args.module_path,
        api=args.api,
        test_arguments=args.test_arguments,
        test_arguments_yaml=args.test_arguments_yaml,
        destination=args.destination
    ).run()