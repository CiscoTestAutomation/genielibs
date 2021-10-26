# Python
import logging
from functools import partial
from collections import OrderedDict

# pyATS
from pyats import aetest
from pyats import results
from pyats.results import Passed, Passx, Failed, Errored
from pyats.aetest import Testcase
from pyats.aetest.container import TestContainer
from pyats.log.utils import banner
from pyats.aetest import processors
from pyats.kleenex.bases import BaseCleaner
from pyats.aetest.parameters import ParameterDict
from pyats.aetest.sections import TestSection

# Genie
from genie.testbed import load
from genie.harness.utils import load_class
from genie.libs.clean.utils import (
    pretty_schema_exception,
    get_clean_function,
    load_clean_json,
    get_image_handler)
from genie.metaparser.util.schemaengine import Schema
from genie.libs.clean.recovery import recovery_processor, block_section

# Logger
log = logging.getLogger(__name__)

NOT_A_STAGE = ['device_recovery', 'images', 'order']

GLOBAL_STAGE_REUSE_LIMIT = 3

REUSE_LIMIT_MSG = """\n
*** Terminating Genie Clean ***
\u0020
To protect against an infinite loop scenario.
\u0020
stage_reuse_limit = {limit}
{stage} ran {limit} times
"""


class StageSection(TestSection):

    def __str__(self):
        '''Context __str__

        Formats the logging output

        Example
        -------
            >>> str(section)
        '''
        return 'stage %s' %(self.uid)


class BaseStage(TestContainer):
    """ Container for class based clean stages.

    This container enables executing an instantiated class just like a function.
    Class methods are executed based on the run_order list defined. If a method
    in the exec_order list does not exist within the class an AttributeError
    will be raised.

    Examples
    --------
        >>> class Stage(BaseStage):
        ...     exec_order = ['func1', 'func2']
        ...     def func2(self):
        ...         print("I am func2")
        ...     def func1(self):
        ...         print("I am func1")
        ...
        >>> stage = Stage()
        >>> stage()
        I am func1
        I am func2

        >>> class Stage(BaseStage):
        ...     exec_order = ['func1', 'some_other_func', 'func2']
        ...     def func1(self):
        ...         print("I am func1")
        ...     def func2(self):
        ...         print("I am func2")
        ...
        >>> stage = Stage()
        >>> stage()
        Traceback (most recent call last):
          (snip)
        AttributeError: The class variable 'exec_order' from <class '__main__.Stage'> contains undefined methods: some_other_func
    """

    exec_order = []

    def __call__(self, **parameters):
        # Update the parameters with user provided
        self.parameters.update(parameters)

        for func in self:
            # Retrieve a partial func with all func args populated
            func = self.apply_parameters(func, self.parameters)
            func()

    def __iter__(self):
        undefined_methods = []
        methods = []

        # Ensure all methods are defined and retrieve them
        for method_name in self.exec_order:
            try:
                method = getattr(self, method_name)
            except AttributeError:
                undefined_methods.append(method_name)
            else:
                methods.append(method)

        if undefined_methods:
            raise AttributeError(
                "The class variable 'exec_order' from {} contains undefined methods: "
                "{}".format(self.__class__, ', '.join(undefined_methods)))

        return iter(methods)


class CleanTestcase(Testcase):

    def __init__(self, device, global_stage_reuse_limit, *args, **kwargs):
        self.device = device
        self.global_stage_reuse_limit = global_stage_reuse_limit
        self.stages = {}
        self.device_recovery_processor = None
        self.image_handler = get_image_handler(device)
        self.history = OrderedDict()
        super().__init__(*args, **kwargs)

    def __iter__(self):
        '''Built-in function __iter__

        Generator function, yielding each testable item within this container
        in the order of appearance inside the test cases. This is the main
        mechanism that allows looping through CleanTestcase Section's child
        items.
        '''
        self.discover()
        used_uids = {}

        order = self.device.clean['order']
        while True:
            for stage in order:
                if stage not in self.stages:
                    self.failed("Stage '{}' has no configuration"
                                " in clean.yaml for device {}"
                                .format(stage, self.device.name))

                # Check if stage has hit execution limits to protect
                # against an infinite loop scenario
                count = len(used_uids.get(stage, []))
                limit = self.stages[stage]['stage_reuse_limit'] or \
                        self.global_stage_reuse_limit

                if count >= limit:
                    # Dont log this for every remaining stage
                    if not aetest.executer.goto:
                        log.error(banner(REUSE_LIMIT_MSG.format(
                            stage=stage, limit=limit)))

                    aetest.executer.goto_result = results.Blocked
                    aetest.executer.goto = [['Infinite loop scenario', str]]

                # If image handler has a method to update this section - execute it
                if self.image_handler:
                    self.image_handler.update_section(stage)

                cls = self.stages[stage]['func']

                # Get a unique ID for the section
                cls_name = stage.split('__')[0]
                if cls_name not in used_uids:
                    used_uids[cls_name] = []
                    cls.uid = cls.__name__
                else:
                    cls.uid = f"{cls.__name__}({len(used_uids[cls_name])+1})"

                used_uids[cls_name].append(cls.uid)

                cls.parameters = ParameterDict()
                cls.parameters['device'] = self.device

                args = self.stages[stage]['args']
                for parameter, value in args.items():
                    cls.parameters[parameter] = value

                if self.device_recovery_processor:
                    processors.affix(
                        cls,
                        pre=[block_section],
                        post=[self.device_recovery_processor])

                cls = cls()
                cls.__name__ = cls.__uid__
                cls.history = self.history
                cls.history[cls.uid] = cls

                # Create a stage section
                new_section = StageSection(cls, parent=self)

                # For some unknown reason, this is required for internal arguments
                # like 'steps' and 'section' to be propagated. Do not remove.
                cls.parameters.internal = new_section.parameters.internal

                yield new_section

                pass_order = self.stages[stage]['change_order_if_pass']
                if pass_order and new_section.result in [Passed, Passx]:
                    msg = "Due to 'change_order_if_pass' the order of clean " \
                          "is changed to:\n- " + "\n- ".join(pass_order)
                    log.warning(msg)
                    order = pass_order
                    if self.image_handler:
                        self.image_handler.update_image_references(cls)
                    break

                fail_order = self.stages[stage]['change_order_if_fail']
                if fail_order and new_section.result in [Failed, Errored]:
                    msg = "Due to 'change_order_if_fail' the order of clean " \
                          "is changed to:\n- " + "\n- ".join(fail_order)
                    log.warning(msg)
                    order = fail_order

                    # In this case we do not want the overall clean result to
                    # be failed. Leave the section result alone but change the
                    # parents to Passed.
                    new_section.parent.parent.result = Passed
                    new_section.parent.result = Passed
                    new_section.result = Passed
                    break

                if not new_section.result:
                    # Dont log this for every remaining stage
                    if not aetest.executer.goto:
                        log.error(banner("*** Terminating Genie Clean ***"))

                    aetest.executer.goto_result = results.Blocked
                    msg = '{} has {}'.format(new_section.uid, new_section.result)
                    aetest.executer.goto = [[msg, str]]

                # image handler updates latest image
                if self.image_handler:
                    self.image_handler.update_image_references(cls)

            else:
                # Every stage in 'order' successfully ran
                # Break from while loop to finish clean
                break

    def discover(self):
        """ Discovers and loads all clean stages defined within the clean
        yaml file. During loading validate that each stage is a TestSection.
        Once loading is complete a schema validation is executed to ensure
        the data provided is valid.
        """
        clean_schema = {}
        clean_to_validate = {}

        # order is mandatory so verify schema
        clean_schema['order'] = list
        if self.device.clean.get('order'):
            clean_to_validate['order'] = self.device.clean['order']

        # device_recovery is optional so verify schema only if provided
        device_recovery_data = self.device.clean.get('device_recovery')
        if device_recovery_data:
            clean_schema['device_recovery'] = recovery_processor.schema
            clean_to_validate['device_recovery'] = device_recovery_data

            # Setup and save the device recovery processor for later
            # use in __iter__()
            self.device_recovery_processor = partial(
                recovery_processor, **self.device.clean['device_recovery'])

        clean_json = load_clean_json()
        # Verify schema and load each stage
        for stage in self.device.clean:
            if stage in NOT_A_STAGE:
                continue

            if self.image_handler:
                self.image_handler.update_section(stage)

            stage_data = self.device.clean[stage] or {}
            if 'source' not in stage_data:
                # Attempt to load from clean json
                stage_func = get_clean_function(stage, clean_json, self.device)
            else:
                # Attempt to load from the provided source
                stage_func = load_class(stage_data, self.device)

            if hasattr(stage_func, 'schema'):
                clean_schema[stage_func.__name__] = stage_func.schema
                clean_to_validate[stage_func.__name__] = stage_data

            # Save for use later in __iter__()
            self.stages[stage] = {
                'func': stage_func,
                'change_order_if_pass': stage_data.pop('change_order_if_pass', None),
                'change_order_if_fail': stage_data.pop('change_order_if_fail', None),
                'stage_reuse_limit': stage_data.pop('stage_reuse_limit', None),
                'args': stage_data
            }

        try:
            Schema(clean_schema).validate(clean_to_validate)
        except Exception as e:
            raise pretty_schema_exception(e)


class DeviceClean(BaseCleaner):

    def clean(self, device, reporter, *args, **kwargs):

        # In this section we will convert to Genie Testbed
        testbed = load(device.testbed)
        device = testbed.devices[device.name]

        global_stage_reuse_limit = getattr(
            self, 'global_stage_reuse_limit', GLOBAL_STAGE_REUSE_LIMIT)

        clean_testcase = CleanTestcase(device, global_stage_reuse_limit)
        clean_testcase.reporter = reporter.testcase(clean_testcase)
        with clean_testcase:
            # 1. Figure out what section to run
            # 2. Run them
            result = clean_testcase()

            if not result:
                raise Exception("Clean {result}.".format(result=str(result)))


class PyatsDeviceClean(DeviceClean):

    def clean(self, device, reporter, *args, **kwargs):
        super().clean(device, reporter, *args, **kwargs)
