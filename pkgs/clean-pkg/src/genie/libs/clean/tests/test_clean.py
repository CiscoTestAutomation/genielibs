
import unittest
import functools
import importlib

from unittest import mock
from functools import partial

from genie.libs.clean.clean import (
    StageSection,
    BaseStage,
    CleanTestcase,
    DeviceClean,
    REUSE_LIMIT_MSG,
)
from genie.libs.clean.recovery.recovery import RecoveryOutcome
from genie.libs.clean.stages.image_handler import BaseImageHandler
from genie.conf.base import Device
from genie.abstract.package import AbstractTree
from genie.libs.clean.utils import validate_clean

from pyats.log.utils import banner
from pyats import results
from pyats.clean.exceptions import CleanRetryRequest
from pyats.kleenex.testbed_config import TestbedConfigCollector


class TestStageSection(unittest.TestCase):

    def test_representation(self):
        stage_name = 'banana'

        section = StageSection(function=self, uid=stage_name)

        self.assertEqual(stage_name, section.uid)
        self.assertEqual(f'stage {stage_name}', str(section))


class TestBaseStage(unittest.TestCase):

    class SomeStage(BaseStage):
        def func2(self): pass

        def func1(self): pass

    stage = SomeStage()

    def test_exec_order_attribute_exists(self):
        self.assertTrue(hasattr(self.stage, 'exec_order'))

    def test_exec_order(self):
        self.stage.exec_order = ['func1', 'func2']

        stage_iter = iter(self.stage)

        self.assertEqual(self.stage.func1, next(stage_iter))
        self.assertEqual(self.stage.func2, next(stage_iter))

    def test_exec_order_not_defined(self):
        self.stage.exec_order = []

        expected_msg = r"^The class variable 'exec_order' from .*SomeStage.* is " \
                       r"empty or not defined.$"

        with self.assertRaisesRegex(AttributeError, expected_msg):
            iter(self.stage)

    def test_exec_order_contains_undefined_method(self):
        self.stage.exec_order = ['func1', 'this doesnt exist', 'func2']

        expected_msg = r"^The class variable 'exec_order' from .*SomeStage.* " \
                       r"contains undefined methods: .*this doesnt exist.*$"

        with self.assertRaisesRegex(AttributeError, expected_msg):
            iter(self.stage)

    @mock.patch.multiple(
        stage, func1=mock.DEFAULT, func2=mock.DEFAULT,
        apply_parameters=lambda func, args: partial(func, **args))
    def test_running_stage_methods_called(self, func1, func2):

        self.stage.exec_order = ['func1', 'func2']

        # run the stage
        self.stage()

        # make sure the methods defined in exec_order were called
        func1.assert_called()
        func2.assert_called()

        self.stage(test=123)
        func1.assert_called_with(test=123)


class TestGeneratedTestbedConfig(unittest.TestCase):

    @mock.patch('genie.libs.clean.clean.get_image_handler', return_value=None)
    def test_clean_testcase_injects_collector_into_stage_parameters(
            self, _get_image_handler: mock.Mock) -> None:
        """Verify a Clean testcase exposes its collector to every stage."""
        # Define the minimal device and stage shapes needed for iteration.
        class DeviceStub:
            """Provide deterministic clean configuration for the stage test."""

            name = 'uut'
            clean = {'order': ['GeneratePeer']}

        class GeneratePeer(BaseStage):
            """Represent a schema-valid stage receiving injected parameters."""

            schema = {}

        # Construct a testcase with the exact collector stages should mutate.
        collector = TestbedConfigCollector()
        testcase = CleanTestcase(
            DeviceStub(), 3, testbed_config=collector)
        testcase.discover = mock.Mock()
        testcase.stages = {
            'GeneratePeer': {
                'func': GeneratePeer,
                'change_order_if_pass': None,
                'change_order_if_fail': None,
                'stage_reuse_limit': None,
                'args': {},
            },
        }

        # Materialize one stage to build its parameter dictionary.
        stage = next(iter(testcase))

        # Identity is required; a copy would hide output from the worker.
        self.assertIs(stage.parameters['testbed_config'], collector)

    @mock.patch('genie.libs.clean.clean.get_image_handler', return_value=None)
    def test_clean_testcase_reserves_collector_parameter(
            self, _get_image_handler: mock.Mock) -> None:
        """Verify configured stage arguments cannot replace the collector."""
        class DeviceStub:
            """Provide deterministic clean configuration for the stage test."""

            name = 'uut'
            clean = {'order': ['GeneratePeer']}

        class GeneratePeer(BaseStage):
            """Represent a stage with a conflicting configured parameter."""

            schema = {}

        collector = TestbedConfigCollector()
        testcase = CleanTestcase(DeviceStub(), 3, testbed_config=collector)
        testcase.discover = mock.Mock()
        testcase.stages = {
            'GeneratePeer': {
                'func': GeneratePeer,
                'change_order_if_pass': None,
                'change_order_if_fail': None,
                'stage_reuse_limit': None,
                'args': {'testbed_config': {'unexpected': True}},
            },
        }

        # Internal plumbing must win over user configuration at the boundary.
        stage = next(iter(testcase))
        self.assertIs(stage.parameters['testbed_config'], collector)

    @mock.patch('genie.libs.clean.clean.get_image_handler', return_value=None)
    def test_clean_testcase_preserves_legacy_parameter_without_collector(
            self, _get_image_handler: mock.Mock) -> None:
        """Verify pre-collector pyATS values remain available to stages."""
        class DeviceStub:
            """Provide deterministic clean configuration for the stage test."""

            name = 'uut'
            clean = {'order': ['GeneratePeer']}

        class GeneratePeer(BaseStage):
            """Represent a stage receiving a legacy configured value."""

            schema = {}

        legacy_value = {'mode': 'legacy'}
        testcase = CleanTestcase(DeviceStub(), 3, testbed_config=None)
        testcase.discover = mock.Mock()
        testcase.stages = {
            'GeneratePeer': {
                'func': GeneratePeer,
                'change_order_if_pass': None,
                'change_order_if_fail': None,
                'stage_reuse_limit': None,
                'args': {'testbed_config': legacy_value},
            },
        }

        # No internal collector means the configured compatibility value wins.
        stage = next(iter(testcase))
        self.assertIs(stage.parameters['testbed_config'], legacy_value)

    @mock.patch('genie.libs.clean.clean.CleanTestcase')
    @mock.patch('genie.libs.clean.clean.load')
    def test_device_clean_passes_its_collector_to_clean_testcase(
            self, load_mock: mock.Mock,
            testcase_class: mock.Mock) -> None:
        """Verify DeviceClean forwards its collector by identity."""
        # Arrange conversion from the worker's pyATS device to a Genie device.
        original_device = mock.Mock(name='original-device')
        original_device.name = 'uut'
        original_device.testbed = mock.Mock()
        genie_device = mock.Mock()
        genie_device.name = 'uut'
        load_mock.return_value.devices = {'uut': genie_device}

        # Make the mocked Clean testcase complete successfully.
        testcase = testcase_class.return_value
        testcase.return_value = results.Passed
        testcase.parameters = {}
        cleaner = DeviceClean()

        # Execute DeviceClean through its normal public entry point.
        cleaner.clean(original_device)

        # The constructed testcase must receive the cleaner-owned collector.
        testcase_class.assert_called_once_with(
            genie_device, mock.ANY,
            testbed_config=cleaner.testbed_config)

    @mock.patch('genie.libs.clean.clean.CleanTestcase')
    @mock.patch('genie.libs.clean.clean.load')
    def test_device_clean_without_collector_passes_none(
            self, load_mock: mock.Mock,
            testcase_class: mock.Mock) -> None:
        """Verify legacy uninitialized cleaners remain backward compatible."""
        # Arrange a device conversion identical to the normal DeviceClean path.
        original_device = mock.Mock()
        original_device.name = 'uut'
        original_device.testbed = mock.Mock()
        genie_device = mock.Mock()
        genie_device.name = 'uut'
        load_mock.return_value.devices = {'uut': genie_device}

        # Bypass BaseCleaner initialization to model a legacy/custom caller.
        testcase = testcase_class.return_value
        testcase.return_value = results.Passed
        testcase.parameters = {}
        cleaner = object.__new__(DeviceClean)

        # Clean must execute without assuming the collector attribute exists.
        cleaner.clean(original_device)

        # A missing collector is represented explicitly as an inert None value.
        testcase_class.assert_called_once_with(
            genie_device, mock.ANY, testbed_config=None)


source_json = {
        "SomeStage": {
            "folders": {
                "iosxe": {
                    "package": "genie.libs.clean",
                    "module_name": "stages.stages",
                    "uid": "SomeStage",
                    "tokens": {
                        "os": "iosxe"
                    }
                }
            }
        },
        "SomeOtherStage": {
            "folders": {
                "iosxe": {
                    "package": "genie.libs.clean",
                    "module_name": "stages.stages",
                    "uid": "SomeOtherStage",
                    "tokens": {
                        "os": "iosxe"
                    }
                }
            }
        },
        "token_order": ["os"],
        "tokens": {
            "os": ["iosxe"]
        }
    }

def clean_json():
    # mock load_clean_json function to return a new abstract matrix each test
    return AbstractTree.from_json(source_json)

class TestCleanTestcase(unittest.TestCase):
    class Connect(BaseStage):
        schema = {}

    class SomeStage(BaseStage):
        schema = {}

    class SomeOtherStage(BaseStage):
        schema = {}

    def setUp(self):
        self.device = Device(
            name='TestDevice', os='iosxe',
            custom={'abstraction': {'order': ['os']}})

        self.global_stage_reuse_limit = 3

    @mock.patch('genie.libs.clean.clean.load_clean_json', mock.Mock(side_effect=clean_json))
    @mock.patch('genie.libs.clean.stages.stages.SomeStage', SomeStage, create=True)
    def test_discover(self):

        self.device.clean = {
            'SomeStage': {},
            'order': ['SomeStage']
        }

        clean_testcase = CleanTestcase(
            device=self.device,
            global_stage_reuse_limit=self.global_stage_reuse_limit)

        clean_testcase.discover()

        self.assertEqual(self.SomeStage, clean_testcase.stages['SomeStage']['func'])

    @mock.patch('genie.libs.clean.clean.load_clean_json', mock.Mock(side_effect=clean_json))
    @mock.patch('genie.libs.clean.stages.stages.SomeStage', SomeStage, create=True)
    def test_discover_with_image_handler(self):

        self.device.clean = {
            'images': ['image.bin'],
            'SomeStage': {},
            'order': ['SomeStage']
        }

        clean_testcase = CleanTestcase(
            device=self.device,
            global_stage_reuse_limit=self.global_stage_reuse_limit)

        self.assertTrue(isinstance(clean_testcase.image_handler, BaseImageHandler))

        clean_testcase.image_handler.update_section = mock.Mock()

        clean_testcase.discover()

        clean_testcase.image_handler.update_section.assert_called_with('SomeStage')

    @mock.patch('genie.libs.clean.clean.load_clean_json', mock.Mock(side_effect=clean_json))
    @mock.patch('genie.libs.clean.stages.stages.SomeStage', SomeStage, create=True)
    def test_discover_custom_stage_source(self):
        self.device.clean = {
            'SomeStage': {
                'source': {
                    'pkg': 'genie.libs.clean',
                    'class': 'stages.stages.SomeStage'
                }
            },
            'order': ['SomeStage']
        }

        clean_testcase = CleanTestcase(
            device=self.device,
            global_stage_reuse_limit=self.global_stage_reuse_limit)

        clean_testcase.discover()

        self.assertEqual(self.SomeStage, clean_testcase.stages['SomeStage']['func'])

    @mock.patch('genie.libs.clean.clean.load_clean_json', mock.Mock(side_effect=clean_json))
    @mock.patch('genie.libs.clean.stages.stages.SomeStage', SomeStage, create=True)
    def test_discover_invalid_stage_schema(self):
        self.device.clean = {
            'SomeStage': {'Not in schema': None},
            'order': ['SomeStage']
        }

        clean_testcase = CleanTestcase(
            device=self.device,
            global_stage_reuse_limit=self.global_stage_reuse_limit)

        expected_msg = r"Not in schema:       <<<"

        with self.assertRaisesRegex(ValueError, expected_msg):
            clean_testcase.discover()

    @mock.patch('genie.libs.clean.clean.load_clean_json', mock.Mock(side_effect=clean_json))
    def test_discover_stage_doesnt_exist_in_json(self):

        self.device.clean = {
            'ThisStageDoesntExist': {},
            'order': ['ThisStageDoesntExist']
        }

        clean_testcase = CleanTestcase(
            device=self.device,
            global_stage_reuse_limit=self.global_stage_reuse_limit)

        expected_msg = r"The clean stage 'ThisStageDoesntExist' does not exist " \
                       r"in the json file"

        with self.assertRaisesRegex(Exception, expected_msg):
            clean_testcase.discover()

    @mock.patch('genie.libs.clean.clean.load_clean_json', mock.Mock(side_effect=clean_json))
    def test_discover_stage_doesnt_exist(self):

        self.device.clean = {
            'SomeStage': {},
            'order': ['SomeStage']
        }

        clean_testcase = CleanTestcase(
            device=self.device,
            global_stage_reuse_limit=self.global_stage_reuse_limit)

        expected_msg = r"The clean stage 'SomeStage' does not exist under the " \
                       r"following abstraction tokens: \{.*\}"

        with self.assertRaisesRegex(Exception, expected_msg):
            clean_testcase.discover()

    @mock.patch('genie.libs.clean.clean.load_clean_json', mock.Mock(side_effect=clean_json))
    @mock.patch('genie.libs.clean.stages.stages.SomeStage', SomeStage, create=True)
    def test_discover_device_recovery_not_in_yaml(self):
        self.device.clean = {
            'SomeStage': {},
            'order': ['SomeStage']
        }

        clean_testcase = CleanTestcase(
            device=self.device,
            global_stage_reuse_limit=self.global_stage_reuse_limit)

        self.assertEqual(None, clean_testcase.device_recovery_processor)

        clean_testcase.discover()

        self.assertEqual(None, clean_testcase.device_recovery_processor)

    @mock.patch('genie.libs.clean.clean.load_clean_json', mock.Mock(side_effect=clean_json))
    @mock.patch('genie.libs.clean.stages.stages.SomeStage', SomeStage, create=True)
    def test_discover_device_recovery_in_yaml(self):

        self.device.clean = {
            'device_recovery': {
                'golden_image': [
                    'golden.bin'
                ]
            },
            'order': []
        }

        clean_testcase = CleanTestcase(
            device=self.device,
            global_stage_reuse_limit=self.global_stage_reuse_limit)

        self.assertEqual(None, clean_testcase.device_recovery_processor)

        clean_testcase.discover()

        self.assertIsInstance(clean_testcase.device_recovery_processor,
                              functools.partial)

    @mock.patch('genie.libs.clean.clean.load_clean_json', mock.Mock(side_effect=clean_json))
    @mock.patch('genie.libs.clean.stages.stages.SomeStage', SomeStage, create=True)
    def test_iter(self):
        self.device.clean = {
            'SomeStage': {},
            'order': ['SomeStage']
        }

        clean_testcase = CleanTestcase(
            device=self.device,
            global_stage_reuse_limit=self.global_stage_reuse_limit)

        iterator = iter(clean_testcase)

        self.assertEqual('stage SomeStage', str(next(iterator)))

    @mock.patch('genie.libs.clean.clean.load_clean_json', mock.Mock(side_effect=clean_json))
    @mock.patch('genie.libs.clean.stages.stages.SomeStage', SomeStage, create=True)
    def test_iter_unique_stage_uids(self):
        self.device.clean = {
            'SomeStage': {},
            'SomeStage__2': {},
            'order': ['SomeStage', 'SomeStage__2', 'SomeStage']
        }

        clean_testcase = CleanTestcase(
            device=self.device,
            global_stage_reuse_limit=self.global_stage_reuse_limit)

        iterator = iter(clean_testcase)

        self.assertEqual('stage SomeStage', str(next(iterator)))
        self.assertEqual('stage SomeStage(2)', str(next(iterator)))
        self.assertEqual('stage SomeStage(3)', str(next(iterator)))

    @mock.patch('genie.libs.clean.clean.load_clean_json',
                mock.Mock(return_value={}))
    @mock.patch('genie.libs.clean.clean.get_clean_function',
                mock.Mock(return_value=Connect))
    def test_iter_connect_recovery_requests_retry_preserves_error(self):

        self.device.clean = {
            'Connect': {},
            'device_recovery': {
                'golden_image': [
                    'golden.bin'
                ]
            },
            'order': ['Connect']
        }

        clean_testcase = CleanTestcase(
            device=self.device,
            global_stage_reuse_limit=self.global_stage_reuse_limit)

        iterator = iter(clean_testcase)
        stage = next(iterator)

        self.assertEqual(clean_testcase.device_recovery_processor,
                         stage.function.__processors__.post[0])
        self.assertTrue(stage.result_rollup)

        stage.result = results.Errored
        clean_testcase.parameters.setdefault(
            'recovery_outcomes', {})[stage.uid] = RecoveryOutcome(
                stage_uid=stage.uid,
                attempted=True,
                result=results.Passed,
                reason='Device recovered after Connect; retry Clean',
                terminate_clean=True,
                retry_clean=True,
                block_following_sections=True,
                clean_flow_result=results.Blocked)

        with self.assertRaises(StopIteration):
            next(iterator)

        self.assertEqual(results.Errored, clean_testcase.result)
        self.assertEqual(
            'Connect',
            clean_testcase.parameters['clean_retry_request'].stage_uid)

    @mock.patch('genie.libs.clean.clean.load_clean_json',
                mock.Mock(return_value={}))
    @mock.patch('genie.libs.clean.clean.get_clean_function',
                mock.Mock(return_value=Connect))
    def test_iter_connect_without_recovery_outcome_preserves_error(self):
        self.device.clean = {
            'Connect': {},
            'device_recovery': {
                'golden_image': [
                    'golden.bin'
                ]
            },
            'order': ['Connect']
        }

        clean_testcase = CleanTestcase(
            device=self.device,
            global_stage_reuse_limit=self.global_stage_reuse_limit)

        iterator = iter(clean_testcase)
        stage = next(iterator)
        stage.result = results.Errored

        with self.assertRaises(StopIteration):
            next(iterator)

        self.assertEqual(results.Errored, clean_testcase.result)

    @mock.patch('genie.libs.clean.clean.aetest')
    @mock.patch('genie.libs.clean.clean.load_clean_json',
                mock.Mock(side_effect=clean_json))
    @mock.patch('genie.libs.clean.stages.stages.SomeStage',
                SomeStage, create=True)
    def test_iter_device_recovery_preserves_stage_error(self, mocked_aetest):
        self.device.clean = {
            'SomeStage': {},
            'device_recovery': {
                'golden_image': [
                    'golden.bin'
                ]
            },
            'order': ['SomeStage']
        }

        clean_testcase = CleanTestcase(
            device=self.device,
            global_stage_reuse_limit=self.global_stage_reuse_limit)

        mocked_aetest.executer.goto = None
        iterator = iter(clean_testcase)
        stage = next(iterator)
        self.assertTrue(stage.result_rollup)
        stage.result = results.Errored

        with self.assertRaises(StopIteration):
            next(iterator)

        self.assertEqual(results.Errored, clean_testcase.result)


    @mock.patch('genie.libs.clean.clean.load_clean_json', mock.Mock(side_effect=clean_json))
    @mock.patch('genie.libs.clean.stages.stages.SomeStage', SomeStage, create=True)
    def test_iter_with_image_handler(self):
        self.device.clean = {
            'images': ['image.bin'],
            'SomeStage': {},
            'SomeStage__2': {},
            'order': ['SomeStage', 'SomeStage__2']
        }

        clean_testcase = CleanTestcase(
            device=self.device,
            global_stage_reuse_limit=self.global_stage_reuse_limit)

        clean_testcase.image_handler.update_section = mock.Mock()
        iterator = iter(clean_testcase)

        self.assertEqual('stage SomeStage', str(next(iterator)))
        clean_testcase.image_handler.update_section.assert_called_with('SomeStage', update_history=True)

        self.assertEqual('stage SomeStage(2)', str(next(iterator)))
        clean_testcase.image_handler.update_section.assert_called_with('SomeStage__2', update_history=True)

    @mock.patch('genie.libs.clean.clean.load_clean_json', mock.Mock(side_effect=clean_json))
    @mock.patch('genie.libs.clean.stages.stages.SomeStage', SomeStage, create=True)
    def test_iter_stage_in_order_but_not_declared(self):
        self.device.clean = {
            'order': ['SomeStage', 'SomeStage__2']
        }

        clean_testcase = CleanTestcase(
            device=self.device,
            global_stage_reuse_limit=self.global_stage_reuse_limit)

        iterator = iter(clean_testcase)

        expected_msg = r"Stage 'SomeStage' has no configuration in clean.yaml " \
                       r"for device TestDevice"

        with self.assertRaisesRegex(Exception, expected_msg):
            next(iterator)

    @mock.patch('genie.libs.clean.clean.log')
    @mock.patch('genie.libs.clean.clean.aetest')
    @mock.patch('genie.libs.clean.clean.load_clean_json', mock.Mock(side_effect=clean_json))
    @mock.patch('genie.libs.clean.stages.stages.SomeStage', SomeStage, create=True)
    def test_iter_infinite_loop_scenario(self, mocked_aetest, mocked_log):
        self.device.clean = {
            'SomeStage': {
                'change_order_if_pass': [
                    'SomeStage'
                ]
            },
            'order': ['SomeStage']
        }

        clean_testcase = CleanTestcase(
            device=self.device,
            global_stage_reuse_limit=self.global_stage_reuse_limit)

        mocked_aetest.executer.goto = None

        iterator = iter(clean_testcase)

        for _ in range(self.global_stage_reuse_limit + 1):
            next(iterator)

        mocked_log.error.assert_called_with(
            banner(REUSE_LIMIT_MSG.format(
                stage='SomeStage', limit=self.global_stage_reuse_limit))
        )

        self.assertEqual(results.Blocked, mocked_aetest.executer.goto_result)
        self.assertEqual([['Infinite loop scenario', str]], mocked_aetest.executer.goto)

    @mock.patch('genie.libs.clean.clean.log')
    @mock.patch('genie.libs.clean.clean.aetest')
    @mock.patch('genie.libs.clean.clean.load_clean_json', mock.Mock(side_effect=clean_json))
    @mock.patch('genie.libs.clean.stages.stages.SomeStage', SomeStage, create=True)
    def test_iter_failed_stage(self, mocked_aetest, mocked_log):
        self.device.clean = {
            'SomeStage': {
                'change_order_if_pass': [
                    'SomeStage'
                ]
            },
            'order': ['SomeStage', 'SomeStage']
        }

        clean_testcase = CleanTestcase(
            device=self.device,
            global_stage_reuse_limit=self.global_stage_reuse_limit)

        mocked_aetest.executer.goto = None

        iterator = iter(clean_testcase)

        stage = next(iterator)
        stage.result = results.Failed

        next(iterator)

        mocked_log.error.assert_called_with(
            banner("*** Terminating Genie Clean ***")
        )

        self.assertEqual(results.Blocked, mocked_aetest.executer.goto_result)
        self.assertEqual([['SomeStage has failed', str]], mocked_aetest.executer.goto)

    @mock.patch('genie.libs.clean.clean.aetest')
    @mock.patch('genie.libs.clean.clean.load_clean_json', mock.Mock(side_effect=clean_json))
    @mock.patch('genie.libs.clean.stages.stages.SomeStage', SomeStage, create=True)
    def test_iter_recovery_termination_marks_clean_flow(self, mocked_aetest):
        self.device.clean = {
            'SomeStage': {},
            'order': ['SomeStage']
        }

        clean_testcase = CleanTestcase(
            device=self.device,
            global_stage_reuse_limit=self.global_stage_reuse_limit)

        iterator = iter(clean_testcase)

        stage = next(iterator)
        stage.result = results.Passed
        clean_testcase.parameters.setdefault(
            'recovery_outcomes', {})[stage.uid] = RecoveryOutcome(
                stage_uid=stage.uid,
                attempted=True,
                result=results.Passed,
                reason='Device recovered after SomeStage; clean terminated',
                terminate_clean=True,
                block_following_sections=True,
                clean_flow_result=results.Blocked)

        with self.assertRaises(StopIteration):
            next(iterator)

        self.assertEqual(results.Passed, stage.result)
        self.assertEqual(results.Blocked, clean_testcase.result)
        self.assertEqual(results.Blocked, mocked_aetest.executer.goto_result)
        self.assertEqual(
            [['Device recovered after SomeStage; clean terminated', str]],
            mocked_aetest.executer.goto)

    @mock.patch('genie.libs.clean.clean.aetest')
    @mock.patch('genie.libs.clean.clean.load_clean_json',
                mock.Mock(side_effect=clean_json))
    @mock.patch('genie.libs.clean.stages.stages.SomeStage',
                SomeStage, create=True)
    def test_iter_recovery_retry_preserves_reachability_error(
            self, mocked_aetest):
        self.device.clean = {
            'SomeStage': {},
            'order': ['SomeStage']
        }

        clean_testcase = CleanTestcase(
            device=self.device,
            global_stage_reuse_limit=self.global_stage_reuse_limit)

        iterator = iter(clean_testcase)
        stage = next(iterator)
        stage.result = results.Passed
        outcome = RecoveryOutcome(
            stage_uid=stage.uid,
            attempted=True,
            result=results.Errored,
            reason='Device recovered after SomeStage; retry Clean',
            terminate_clean=True,
            retry_clean=True,
            block_following_sections=True,
            clean_flow_result=results.Blocked)
        clean_testcase.parameters.setdefault(
            'recovery_outcomes', {})[stage.uid] = outcome

        with self.assertRaises(StopIteration):
            next(iterator)

        self.assertEqual(results.Passed, stage.result)
        self.assertEqual(results.Blocked, clean_testcase.result)
        self.assertEqual(results.Blocked, mocked_aetest.executer.goto_result)
        self.assertIs(
            outcome, clean_testcase.parameters['clean_retry_request'])
        self.assertEqual(
            results.Errored,
            clean_testcase.parameters['clean_retry_request'].result)

    @mock.patch('genie.libs.clean.clean.aetest')
    @mock.patch('genie.libs.clean.clean.load_clean_json', mock.Mock(side_effect=clean_json))
    @mock.patch('genie.libs.clean.stages.stages.SomeStage', SomeStage, create=True)
    def test_iter_recovery_termination_preserves_failed_stage(self, mocked_aetest):
        self.device.clean = {
            'SomeStage': {},
            'order': ['SomeStage']
        }

        clean_testcase = CleanTestcase(
            device=self.device,
            global_stage_reuse_limit=self.global_stage_reuse_limit)

        iterator = iter(clean_testcase)

        stage = next(iterator)
        stage.result = results.Failed
        clean_testcase.parameters.setdefault(
            'recovery_outcomes', {})[stage.uid] = RecoveryOutcome(
                stage_uid=stage.uid,
                attempted=True,
                result=results.Passed,
                reason='Device recovered after SomeStage; clean terminated',
                terminate_clean=True,
                block_following_sections=True,
                clean_flow_result=results.Blocked)

        with self.assertRaises(StopIteration):
            next(iterator)

        self.assertEqual(results.Failed, stage.result)
        self.assertEqual(results.Failed, clean_testcase.result)
        self.assertEqual(results.Blocked, mocked_aetest.executer.goto_result)

    @mock.patch('genie.libs.clean.clean.aetest')
    @mock.patch('genie.libs.clean.clean.load_clean_json', mock.Mock(side_effect=clean_json))
    @mock.patch('genie.libs.clean.stages.stages.SomeStage', SomeStage, create=True)
    def test_iter_recovery_termination_preserves_errored_stage(self, mocked_aetest):
        self.device.clean = {
            'SomeStage': {},
            'order': ['SomeStage']
        }

        clean_testcase = CleanTestcase(
            device=self.device,
            global_stage_reuse_limit=self.global_stage_reuse_limit)

        iterator = iter(clean_testcase)

        stage = next(iterator)
        stage.result = results.Errored
        clean_testcase.parameters.setdefault(
            'recovery_outcomes', {})[stage.uid] = RecoveryOutcome(
                stage_uid=stage.uid,
                attempted=True,
                result=results.Passed,
                reason='Device recovered after SomeStage; clean terminated',
                terminate_clean=True,
                block_following_sections=True,
                clean_flow_result=results.Blocked)

        with self.assertRaises(StopIteration):
            next(iterator)

        self.assertEqual(results.Errored, stage.result)
        self.assertEqual(results.Errored, clean_testcase.result)
        self.assertEqual(results.Blocked, mocked_aetest.executer.goto_result)

    @mock.patch('genie.libs.clean.clean.log')
    @mock.patch('genie.libs.clean.clean.load_clean_json', mock.Mock(side_effect=clean_json))
    @mock.patch('genie.libs.clean.stages.stages.SomeStage', SomeStage, create=True)
    @mock.patch('genie.libs.clean.stages.stages.SomeOtherStage', SomeOtherStage, create=True)
    def test_iter_change_order_if_pass(self, mocked_log):
        self.device.clean = {
            'SomeOtherStage': {},
            'SomeStage': {
                'change_order_if_pass': [
                    'SomeOtherStage'
                ]
            },
            'order': ['SomeStage']
        }

        clean_testcase = CleanTestcase(
            device=self.device,
            global_stage_reuse_limit=self.global_stage_reuse_limit)

        iterator = iter(clean_testcase)

        stage = next(iterator)
        stage.result = results.Passed

        stage = next(iterator)

        mocked_log.warning.assert_called_with(
            "Due to 'change_order_if_pass' the order of clean is changed "
            "to:\n- SomeOtherStage"
        )

        self.assertEqual('SomeOtherStage', stage.uid)

    @mock.patch('genie.libs.clean.clean.log')
    @mock.patch('genie.libs.clean.clean.load_clean_json', mock.Mock(side_effect=clean_json))
    @mock.patch('genie.libs.clean.stages.stages.SomeStage', SomeStage, create=True)
    @mock.patch('genie.libs.clean.stages.stages.SomeOtherStage', SomeOtherStage, create=True)
    def test_iter_change_order_if_fail(self, mocked_log):
        self.device.clean = {
            'SomeOtherStage': {},
            'SomeStage': {
                'change_order_if_fail': [
                    'SomeOtherStage'
                ]
            },
            'order': ['SomeStage']
        }

        clean_testcase = CleanTestcase(
            device=self.device,
            global_stage_reuse_limit=self.global_stage_reuse_limit,
            parent=mock.Mock(__result__=None))

        iterator = iter(clean_testcase)

        stage = next(iterator)
        stage.result = results.Failed

        stage = next(iterator)

        mocked_log.warning.assert_called_with(
            "Due to 'change_order_if_fail' the order of clean is changed "
            "to:\n- SomeOtherStage"
        )

        self.assertEqual('SomeOtherStage', stage.uid)

    @mock.patch('genie.libs.clean.clean.load_clean_json', mock.Mock(return_value=clean_json()))
    @mock.patch('genie.libs.clean.stages.stages.SomeStage', SomeStage, create=True)
    def test_discover_image_handler_image_override_false(self):
        self.device.clean = {
            'images': ['/my/image.bin'],
            'SomeStage': {},
            'order': ['SomeStage'],
            'image_management': {
                'override_stage_images': False
            },
        }
        clean_testcase = CleanTestcase(
            device=self.device,
            global_stage_reuse_limit=self.global_stage_reuse_limit)

        clean_testcase.discover()

        self.assertEqual(clean_testcase.image_handler.override_stage_images, False)

    @mock.patch('genie.libs.clean.clean.load_clean_json', mock.Mock(return_value=clean_json))
    @mock.patch('genie.libs.clean.stages.stages.SomeStage', SomeStage, create=True)
    def test_discover_image_handler_image_override_true(self):
        self.device.clean = {
            'images': ['/my/image.bin'],
            'SomeStage': {
                'source': {
                    'pkg': 'genie.libs.clean',
                    'class': 'stages.stages.SomeStage'
                }
            },
            'order': ['SomeStage'],
            'image_management': {
                'override_stage_images': True
            },
        }

        clean_testcase = CleanTestcase(
            device=self.device,
            global_stage_reuse_limit=self.global_stage_reuse_limit)

        clean_testcase.discover()

        self.assertEqual(clean_testcase.image_handler.override_stage_images, True)

    @mock.patch('genie.libs.clean.clean.load_clean_json', mock.Mock(return_value=clean_json))
    @mock.patch('genie.libs.clean.stages.stages.SomeStage', SomeStage, create=True)
    def test_discover_image_handler_image_override_default(self):
        self.device.clean = {
            'images': ['/my/image.bin'],
            'SomeStage': {
                'source': {
                    'pkg': 'genie.libs.clean',
                    'class': 'stages.stages.SomeStage'
                }
            },
            'order': ['SomeStage']
        }

        clean_testcase = CleanTestcase(
            device=self.device,
            global_stage_reuse_limit=self.global_stage_reuse_limit)

        clean_testcase.discover()

        self.assertEqual(clean_testcase.image_handler.override_stage_images, True)


class TestDeviceClean(unittest.TestCase):

    def setUp(self):
        self.device = mock.MagicMock()
        self.device.name = 'TestDevice'
        self.testbed = mock.MagicMock()
        self.testbed.devices = {'TestDevice': self.device}

    @mock.patch('genie.libs.clean.clean.aetest')
    @mock.patch('genie.libs.clean.clean.CleanTestcase')
    @mock.patch('genie.libs.clean.clean.load')
    def test_successful_recovery_raises_clean_retry_request(
            self, mocked_load, mocked_clean_testcase, mocked_aetest):
        mocked_load.return_value = self.testbed
        outcome = RecoveryOutcome(
            stage_uid='ResetConfiguration',
            attempted=True,
            result=results.Errored,
            reason='Device recovered; retry Clean',
            terminate_clean=True,
            retry_clean=True)
        testcase = mocked_clean_testcase.return_value
        testcase.return_value = results.Failed
        testcase.parameters = {'clean_retry_request': outcome}

        with self.assertRaises(CleanRetryRequest) as cm:
            DeviceClean().clean(self.device)

        self.assertEqual('Device recovered; retry Clean', cm.exception.reason)
        self.assertEqual('ResetConfiguration', cm.exception.stage)
        self.assertEqual(results.Skipped,
                         mocked_aetest.executer.goto_result)
        self.assertEqual([], mocked_aetest.executer.goto)

    @mock.patch('genie.libs.clean.clean.aetest')
    @mock.patch('genie.libs.clean.clean.CleanTestcase')
    @mock.patch('genie.libs.clean.clean.load')
    def test_clean_failure_without_recovery_is_not_retryable(
            self, mocked_load, mocked_clean_testcase, mocked_aetest):
        mocked_load.return_value = self.testbed
        testcase = mocked_clean_testcase.return_value
        testcase.return_value = results.Failed
        testcase.parameters = {}

        with self.assertRaisesRegex(Exception, 'Clean failed') as cm:
            DeviceClean().clean(self.device)

        self.assertNotIsInstance(cm.exception, CleanRetryRequest)
        self.assertEqual(results.Skipped,
                         mocked_aetest.executer.goto_result)
        self.assertEqual([], mocked_aetest.executer.goto)

class TestValidateClean(unittest.TestCase):

    @mock.patch('genie.libs.clean.clean.load_clean_json', mock.Mock(side_effect=clean_json))
    def test_validate_clean_image_management_stage(self):
        expected_result = {'warnings': [], 'exceptions': []}
        clean_yaml = """cleaners:
  DeviceClean:
    module: genie.libs.clean
    devices: [router]

devices:
  router:
    images:
      - /auto/release/path/image.bin

    image_management:
      override_stage_images: False

    connect:

    order:
      - 'connect'
"""
        testbed_yaml = """
testbed:
  name: SAMPLE-TESTBED

devices:
  router:
    os: iosxe
    connections:
      defaults:
        class: unicon.Unicon
"""
        actual_result = validate_clean(clean_yaml, testbed_yaml)
        self.assertEqual(expected_result, actual_result)
