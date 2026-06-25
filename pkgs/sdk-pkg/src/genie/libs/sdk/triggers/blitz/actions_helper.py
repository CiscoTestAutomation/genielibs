import re
import ast
import logging
import operator
import xmltodict
import xml.etree.ElementTree as ET
import time
import requests
from threading import Thread

# from genie
from genie.utils.dq import Dq
from genie.conf.base import Device
from genie.conf.base.utils import QDict
from genie.utils.timeout import Timeout
from genie.ops.utils import get_ops_exclude
from genie.libs.parser.utils import get_parser_exclude
from genie.metaparser.util.exceptions import SchemaEmptyParserError
from genie.libs.sdk.triggers.blitz.markup import save_variable

# from pyats
from pyats.easypy import runtime
from pyats.results import Passed, Failed

# from unicon
from unicon.eal.dialogs import Statement, Dialog, statement_action_helper
from unicon.core.errors import TimeoutError as UniconTimeoutError


log = logging.getLogger(__name__)


def configure_handler(step, device, command, expected_failure=False, **kwargs):
    # checking to see if action is 'configure' or 'configure_handler'
    action = kwargs.pop('action', 'configure')
    connection_alias = kwargs.get('connection_alias', None)
    result_status = kwargs.get('result_status', None)
    failed_result_status = kwargs.get('failed_result_status', None)

    # configure dual commands should be entered as a list
    if action == 'configure_dual':
        command = command.splitlines()

    if 'reply' in kwargs:
        kwargs.update({'reply': _prompt_handler(kwargs['reply'])})
    try:
        if connection_alias:
           connection_alias_obj = getattr(device, connection_alias)
           if action == "configure":
              output = connection_alias_obj.configure(command, **kwargs)
           elif action == "configure_dual":
              output = connection_alias_obj.configure_dual(command, **kwargs)
        else:
            output = getattr(device, action)(command, **kwargs)

        if expected_failure and step.result == Passed:
            step.failed(
                f"{action} did not fail as expected, but completed successfully"
            )


    except Exception as e:
        if 'maple' in kwargs:
            step.passx("Invalid config command executed")
        if not expected_failure:
            step.failed('{} failed {}'.format(action, str(e)))
        else:
            step.passed(
                '{} failed as expected, the step test result is set as passed'.format(action))

    # steps.result will only change to result_status if it is passed.
    if result_status and step.result == Passed:
        result_status_message = 'The {} result status is changed from passed to {}' \
                                ' based on the result_status'.format(action, result_status)
        log.warning(result_status_message)
        getattr(step, result_status)(result_status_message)
    elif failed_result_status and step.result == Failed:
        result_status_message = 'The {} result status is changed from failed to {}' \
                                ' based on the result_status'.format(action, failed_result_status)
        log.warning(result_status_message)
        getattr(step, failed_result_status)(result_status_message)

    return output

def parse_handler(step,
                  device,
                  command,
                  expected_failure=False,
                  include=None,
                  exclude=None,
                  result_status=None,
                  max_time=None,
                  check_interval=None,
                  continue_=True,
                  arguments=None,
                  **extra_kwargs):

    if not arguments:
        arguments = {}
    else:
        log.info('Arguments passed:\n{}'.format('\n'.join(
            '{}:\n{}'.format(k,v) for k,v in arguments.items())))

    context=extra_kwargs.get('context', None)
    connection_alias=extra_kwargs.get('connection_alias', None)

    kwargs = {'steps': step,
              'device': device,
              'command': command,
              'include': include,
              'exclude': exclude,
              'result_status': result_status,
              'max_time': max_time,
              'check_interval': check_interval,
              'continue_': continue_,
              'action': 'parse',
              'expected_failure': expected_failure,
              'extra_kwargs': extra_kwargs}

    # handeling parse command
    try:
        if None not in (context, connection_alias):
            output = device.parse(command, context=context, alias=connection_alias, **arguments)
        elif context is not None:
            output = device.parse(command, context=context, **arguments)
        elif connection_alias is not None:
            output = device.parse(command, alias=connection_alias, **arguments)
        else:
            output = device.parse(command, **arguments)


    # check if the parser is empty then return an empty dictionary
    except SchemaEmptyParserError:
        if include or exclude or (max_time and check_interval):
            kwargs.update({'output': ''})
            return _output_query_template(**kwargs)
        else:
            step.passed('The result of this command is an empty parser.')

    else:
        # go through the include/exclude process
        kwargs.update({'output': output})
        return _output_query_template(**kwargs)

def execute_handler(step,
                    device,
                    command,
                    expected_failure=False,
                    scope=None,
                    include=None,
                    exclude=None,
                    result_status=None,
                    max_time=None,
                    check_interval=None,
                    continue_=True,
                    blitz_obj=None,
                    section=None,
                    ret_dict=None,
                    extract=None,
                    **extra_kwargs):

    if 'reply' in extra_kwargs:
        extra_kwargs.update({'reply': _prompt_handler(extra_kwargs['reply'])})

    connection_alias=extra_kwargs.get('connection_alias', None)

    output = ''
    # handeling execute command
    try:
        if connection_alias:
            connection_alias_obj = getattr(device, connection_alias)
            output = connection_alias_obj.execute(command, **extra_kwargs)
        else:
            output = device.execute(command, **extra_kwargs)
    except Exception as e:
        if not expected_failure:
            step.failed("Step failed because of this error: {e}".format(e=e))
        else:
            step.passed('Execute failed as expected, the step test result is set as passed')

    kwargs = {'output': output,
              'steps': step,
              'device': device,
              'command': command,
              'include': include,
              'exclude': exclude,
              'result_status':result_status,
              'max_time': max_time,
              'check_interval': check_interval,
              'continue_': continue_,
              'action': 'execute',
              'expected_failure': expected_failure,
              'scope': scope,
              'extract': extract,
              'blitz_obj': blitz_obj,
              'section': section,
              'ret_dict': ret_dict,
              'extra_kwargs': extra_kwargs}

    return _output_query_template(**kwargs)

def learn_handler(step,
                  device,
                  command,
                  expected_failure=False,
                  include=None,
                  exclude=None,
                  result_status=None,
                  max_time=None,
                  check_interval=None,
                  continue_=True,
                  **extra_kwargs):

    # Save the to_dict learn output,
    learned_value = device.learn(command)
    output = \
        learned_value if isinstance(learned_value, dict) else learned_value.to_dict()

    kwargs = {'output': output,
              'steps': step,
              'device': device,
              'command': command,
              'include': include,
              'exclude': exclude,
              'result_status':result_status,
              'max_time': max_time,
              'check_interval': check_interval,
              'continue_': continue_,
              'action': 'learn',
              'expected_failure': expected_failure,
              'extra_kwargs': extra_kwargs}

    return _output_query_template(**kwargs)

def api_handler(step,
                command,
                device=None,
                expected_failure=False,
                include=None,
                exclude=None,
                result_status=None,
                failed_result_status=None,
                max_time=None,
                check_interval=None,
                continue_=True,
                arguments=None,
                **kwargs):

    #handling api command
    output = None
    # if no arguments send an empty argument list to api function
    if not arguments:
        arguments = {}

    common_api = kwargs.get('common_api')
    # To support below both cases.
    # 1. when tb file is passed via gRun in job file
    # 2. when tb file is passed via CLI to pyats run command
    # (pyATS Health Check ues runtime.testbed)
    if kwargs['blitz_obj'].parameters.get('testbed'):
        testbed = kwargs['blitz_obj'].parameters.get('testbed')
    else:
        testbed = runtime.testbed

    # updating the device object
    device = _api_device_update(arguments,
                                testbed,
                                step,
                                command,
                                device=device,
                                common_api=common_api)
    # check if device has API attribute, otherwise fallback to device default behavior
    api_function = device if not hasattr(device, 'api') else device.api

    # check if command as device object
    # tgn action uses device object function
    if command not in dir(api_function) and command in dir(device):
        api_function = device

    # Skip if API is not available
    if command in dir(api_function):
        try:
            output = getattr(api_function, command)(**arguments)
        except TypeError as e:
            # kwargs is wrong for api
            if not expected_failure:
                step.errored("Got an error with API {c}: {e}\nAPI arguments: {a}".format(c=command, e=e, a=arguments))
            else:
                step.passed('API failed as expected, the step test result is set as passed')
        except Exception as e:
            # anything else
            if not expected_failure:
                step.failed(str(e))
            else:
                step.passed('API failed as expected, the step test result is set as passed')
    else:
        step.skipped(f'API {command} not available for device {device.name}')

    kwargs = {'output': output,
              'steps': step,
              'device': device,
              'command': command,
              'include': include,
              'exclude': exclude,
              'result_status': result_status,
              'failed_result_status': failed_result_status,
              'max_time': max_time,
              'check_interval': check_interval,
              'continue_': continue_,
              'action': 'api',
              'expected_failure': expected_failure,
              'arguments':arguments,
              'extra_kwargs':kwargs}

    return _output_query_template(**kwargs)

def yang_handler(step,
                 device,
                 protocol,
                 include=None,
                 exclude=None,
                 continue_=True,
                 max_time=None,
                 check_interval=None,
                 **extra_kwargs):

    # To handle yang action
    kwargs = {
        'output': extra_kwargs.pop('output', None),
        'steps': step,
        'device': device,
        'command': protocol,
        'include': include,
        'exclude': exclude,
        'max_time': max_time,
        'check_interval': check_interval,
        'continue_': continue_,
        'action': 'yang',
        'extra_kwargs': extra_kwargs
    }

    # go through the include/exclude process
    return _output_query_template(**kwargs)


def _api_device_update(arguments, testbed, step, command, device=None, common_api=None):
    """
        Updating the device obj with regards to the user input
        1) Allow user to both provide device in the body and arguments of the action
        2) Allow user to provide device value in either body or arguments of the action
        3) Allow user to provide no device for api's that are common utils
    """

    # if api and arguments both contains device, need to make sure
    # that the device in the arguments is as same as the one in api
    if (
        arguments.get('device')
        and device
        and arguments.get('device') not in [device.name, device.alias]
    ):

        step.errored('Device provided in the arguments {} '
                     'is not as same as the one provided in api {}'
                     .format(arguments['device'], device))
    if device:

        return device

    # if not device in api and arguments contains device need to make sure
    # that device is a valid one and exist in the testbed
    if arguments.get('device'):

        try:
            arg_device = testbed.devices[arguments['device']]
        except KeyError as e:
            step.errored('Cannot find device {} in testbed'.format(
                arguments['device']))

        arguments['device'] = arg_device
        return arg_device

    # if common api
    if common_api:
        return Device(name='a', os='', custom={'abstraction':{'order': ['origin']}})

    step.errored("No device is provided and the api '{}'"
                 "is not a common api".format(command))

def bash_console_handler(device,
                         step,
                         commands,
                         expected_failure=False,
                         include=None,
                         exclude=None,
                         result_status=None,
                         max_time=None,
                         check_interval=None,
                         continue_=True,
                         **extra_kwargs):

    output_dict = {}

    custom_msg = extra_kwargs.pop('custom_verification_message', None)

    with device.bash_console(**extra_kwargs) as bash:
        for command in commands:
            bash_command_output = bash.execute(command, **extra_kwargs)
            if isinstance(bash_command_output, dict):
                output_dict.update(bash_command_output)
            else:
                output_dict.update({command:bash_command_output})

    extra_kwargs.update({'custom_verification_message':custom_msg})
    kwargs = {'output': output_dict,
              'steps': step,
              'device': device,
              'command': command,
              'include': include,
              'exclude': exclude,
              'result_status': result_status,
              'max_time': max_time,
              'check_interval': check_interval,
              'continue_': continue_,
              'action': 'bash_console',
              'expected_failure': expected_failure,
              'extra_kwargs':extra_kwargs}

    return _output_query_template(**kwargs)

def rest_handler(device,
                 method,
                 step,
                 expected_failure=False,
                 continue_=True,
                 include=None,
                 exclude=None,
                 result_status=None,
                 max_time=None,
                 check_interval=None,
                 connection_alias='rest',
                 save=None,
                 **extra_kwargs):
    output = ''

    custom_msg = extra_kwargs.pop('custom_verification_message', None)

    # Checking the connection alias
    try:
        device_alias = getattr(device, connection_alias)
    except AttributeError as e:
        raise Exception("'{dev}' does not have a connection with the "
                        "alias '{alias}'".format(
                            dev=device.name, alias=connection_alias)) from e
    # Calling the http protocol
    try:
        output = getattr(device_alias, method)(**extra_kwargs)

    except Exception as e:
        if not expected_failure:
            step.failed("REST method '{}' failed. Error: {}".format(method, e))
        else:
            step.passed('Rest failed as expected, the step test result is set as passed')

    # if xml convert it to json
    if output and ET.iselement(output):
        output = xmltodict.parse(output)
    # To convert the response object to a json
    if isinstance(output, requests.Response):
        output = output.json()

    log.info(output)

    extra_kwargs.update({'custom_verification_message':custom_msg})
    kwargs = {'output': output,
              'steps': step,
              'device': device,
              'command': method,
              'include': include,
              'exclude': exclude,
              'result_status':result_status,
              'max_time': max_time,
              'check_interval': check_interval,
              'continue_': continue_,
              'action': 'rest',
              'rest_device_alias': device_alias,
              'expected_failure': expected_failure,
              'extra_kwargs':extra_kwargs}

    return _output_query_template(**kwargs)


def dialog_handler(step,
                   device,
                   action,
                   expect,
                   arguments=None,
                   include=None,
                   exclude=None,
                   timeout=None,
                   continue_=True,
                   **extra_kwargs):
    '''
    Handles dialog actions and returns the output of the process
    '''
    handle = device.active if device.is_ha else device

    if not re.match(r'^\^?\(?\.\*', expect):
        expect = '^.*?{}'.format(expect)

    if action:
        callback, arg = statement_action_helper(action)
        callback(device.spawn, arg)

    dialog = Dialog([
        Statement(pattern=expect, args=arguments, loop_continue=False)
    ])

    try:
        result = dialog.process(handle.spawn,
                                timeout=timeout,
                                prompt_recovery=False,
                                context=device.context)
    except UniconTimeoutError:
        log.exception('Dialog failed due to timeout')
        step.failed()

    output = result.match_output

    kwargs = {
        'output': output,
        'steps': step,
        'device': device,
        'command': action,
        'include': include,
        'exclude': exclude,
        'result_status': extra_kwargs.pop('result_status', None),
        'max_time': extra_kwargs.pop('max_time', 0),
        'check_interval': extra_kwargs.pop('check_interval', 0),
        'continue_': continue_,
        'action': 'dialog',
        'expected_failure': extra_kwargs.pop('expected_failure', False),
        'extra_kwargs': extra_kwargs
    }
    return _output_query_template(**kwargs)


def _prompt_handler(reply):

    # handeling the reply for instances that a prompt message would get displayed in the console
    dialog_list = [Statement(**statement) for statement in reply]
    return Dialog(dialog_list)

class _ExecuteScopeError(Exception):
    pass


class _ExecuteScopeNotFound(_ExecuteScopeError):
    pass


class _ExecuteExtractError(Exception):
    pass


class _ExecuteExtractRetryable(_ExecuteExtractError):
    pass


def _get_scope_mode(scope):
    if not isinstance(scope, dict):
        raise _ExecuteScopeError("'scope' must be a dictionary")

    unsupported = [key for key in ('before', 'after', 'window') if key in scope]
    if unsupported:
        raise _ExecuteScopeError(
            "Unsupported execute scope field(s): {}".format(
                ', '.join(unsupported)))

    modes = []
    if scope.get('start') is not None or scope.get('end') is not None:
        modes.append('start')
    if scope.get('block_regex') is not None:
        modes.append('block_regex')
    if scope.get('line_regex') is not None:
        modes.append('line_regex')

    if len(modes) != 1:
        raise _ExecuteScopeError(
            "Execute scope must define exactly one of start/end, "
            "block_regex, or line_regex")

    return modes[0]


def _get_scope_regex(scope, field, required=True):
    value = scope.get(field)
    if value is None:
        if required:
            raise _ExecuteScopeError(
                "Execute scope field '{}' is required".format(field))
        return None

    value = str(value)
    if not value:
        raise _ExecuteScopeError(
            "Execute scope field '{}' cannot be empty".format(field))

    try:
        return re.compile(value, re.MULTILINE)
    except re.error as exc:
        raise _ExecuteScopeError(
            "Invalid execute scope regex for '{}': {}".format(field, exc))


def _get_scope_block_regex(scope):
    value = scope.get('block_regex')
    if value is None or not str(value):
        raise _ExecuteScopeError(
            "Execute scope field 'block_regex' cannot be empty")

    try:
        return re.compile(str(value), re.DOTALL | re.MULTILINE)
    except re.error as exc:
        raise _ExecuteScopeError(
            "Invalid execute scope regex for 'block_regex': {}".format(exc))


def _normalize_scope_occurrence(scope):
    occurrence = scope.get('occurrence', 'first')

    if isinstance(occurrence, bool):
        raise _ExecuteScopeError("Execute scope occurrence is invalid")

    if isinstance(occurrence, int):
        if occurrence < 0:
            raise _ExecuteScopeError(
                "Execute scope occurrence cannot be negative")
        return occurrence

    occurrence = str(occurrence).strip().lower()
    if occurrence in ('first', 'last', 'all'):
        return occurrence

    try:
        occurrence = int(occurrence)
    except ValueError:
        raise _ExecuteScopeError(
            "Execute scope occurrence must be first, last, all, or an integer")

    if occurrence < 0:
        raise _ExecuteScopeError(
            "Execute scope occurrence cannot be negative")
    return occurrence


def _line_end_index(output, index):
    newline_index = output.find('\n', index)
    if newline_index == -1:
        return len(output)
    return newline_index + 1


def _select_scope_parts(parts, occurrence):
    if not parts:
        raise _ExecuteScopeNotFound("Execute scope block not found")

    if occurrence == 'all':
        return parts, True
    if occurrence == 'first':
        return [parts[0]], False
    if occurrence == 'last':
        return [parts[-1]], False

    if occurrence >= len(parts):
        raise _ExecuteScopeNotFound(
            "Execute scope occurrence '{}' was not found".format(occurrence))
    return [parts[occurrence]], False


def _join_scope_parts(parts):
    return '\n'.join(part.rstrip('\n') for part in parts)


def _scope_with_start_end(output, scope):
    start_pattern = _get_scope_regex(scope, 'start')
    end_pattern = _get_scope_regex(scope, 'end', required=False)
    include_start = scope.get('include_start', True)
    include_end = scope.get('include_end', False)

    parts = []
    for start_match in start_pattern.finditer(output):
        if start_match.start() == start_match.end():
            raise _ExecuteScopeNotFound(
                "Execute scope start regex matched an empty string")

        block_start = start_match.start()
        if not include_start:
            block_start = _line_end_index(output, start_match.end())

        block_end = len(output)
        if end_pattern:
            end_match = end_pattern.search(output, start_match.end())
            if end_match:
                if end_match.start() == end_match.end():
                    raise _ExecuteScopeNotFound(
                        "Execute scope end regex matched an empty string")
                block_end = end_match.start()
                if include_end:
                    block_end = _line_end_index(output, end_match.end())

        parts.append(output[block_start:block_end])

    return parts


def _scope_with_block_regex(output, scope):
    pattern = _get_scope_block_regex(scope)
    parts = []

    for match in pattern.finditer(output):
        if match.start() == match.end():
            raise _ExecuteScopeNotFound(
                "Execute scope block_regex matched an empty string")
        if match.groups():
            parts.append(match.group(1))
        else:
            parts.append(match.group(0))

    return parts


def _scope_with_line_regex(output, scope):
    pattern = _get_scope_regex(scope, 'line_regex')
    parts = []

    for line in output.splitlines(True):
        if pattern.search(line):
            parts.append(line)

    return parts


def _save_execute_scope(scope, scoped_output, blitz_obj, section, ret_dict):
    save_as = scope.get('save_as')
    if not save_as:
        return

    if blitz_obj and section:
        save_variable(blitz_obj, section, save_as, scoped_output)

    if ret_dict is not None:
        ret_dict.setdefault('saved_vars', {})
        ret_dict['saved_vars'].update({save_as: scoped_output})


def _apply_execute_scope(output,
                         scope,
                         blitz_obj=None,
                         section=None,
                         ret_dict=None):
    if not scope:
        return output, [output], False

    output = '' if output is None else str(output)
    mode = _get_scope_mode(scope)
    occurrence = _normalize_scope_occurrence(scope)

    if mode == 'start':
        parts = _scope_with_start_end(output, scope)
    elif mode == 'block_regex':
        parts = _scope_with_block_regex(output, scope)
    else:
        parts = _scope_with_line_regex(output, scope)

    try:
        selected_parts, verify_each = _select_scope_parts(parts, occurrence)
    except _ExecuteScopeNotFound:
        if scope.get('required', True):
            raise
        _save_execute_scope(scope, output, blitz_obj, section, ret_dict)
        return output, [output], False

    if verify_each:
        scoped_output = _join_scope_parts(selected_parts)
    else:
        scoped_output = selected_parts[0]

    _save_execute_scope(scope, scoped_output, blitz_obj, section, ret_dict)
    return scoped_output, selected_parts, verify_each


def _verify_execute_scope_query(scoped_output, scoped_parts, verify_each,
                                query, style):
    pattern = re.compile(str(query))

    if not verify_each:
        found = pattern.search(str(scoped_output))
        return _verify_include_exclude(
            action_output=found,
            operation=None,
            expected_value=None,
            style=style,
            key=query,
            query_type='execute_query')

    matched_indexes = []
    for index, part in enumerate(scoped_parts):
        if pattern.search(str(part)):
            matched_indexes.append(index)

    if style == 'included':
        if len(matched_indexes) == len(scoped_parts):
            return Passed, (
                "'include' criteria is present in all scoped outputs.")
        return Failed, (
            "'include' criteria is not present in scoped output index {}."
            .format(_first_missing_index(matched_indexes, len(scoped_parts))))

    if not matched_indexes:
        return Passed, (
            "'exclude' criteria is not present in any scoped output.")
    return Failed, (
        "'exclude' criteria is present in scoped output index {}."
        .format(matched_indexes[0]))


def _first_missing_index(matched_indexes, length):
    matched_indexes = set(matched_indexes)
    for index in range(length):
        if index not in matched_indexes:
            return index
    return 0


def _normalize_extract_bool(rule, field, default=False):
    value = rule.get(field, default)
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        value = value.strip().lower()
        if value in ('true', 'yes', 'on', '1'):
            return True
        if value in ('false', 'no', 'off', '0'):
            return False
    raise _ExecuteExtractError(
        "Execute extract rule '{}' field '{}' must be boolean".format(
            rule.get('name'), field))


def _normalize_extract_count(rule, field):
    value = rule.get(field)
    if value is None:
        return None
    if isinstance(value, bool):
        raise _ExecuteExtractError(
            "Execute extract rule '{}' field '{}' must be an integer".format(
                rule.get('name'), field))
    try:
        value = int(value)
    except (TypeError, ValueError):
        raise _ExecuteExtractError(
            "Execute extract rule '{}' field '{}' must be an integer".format(
                rule.get('name'), field))
    if value < 0:
        raise _ExecuteExtractError(
            "Execute extract rule '{}' field '{}' cannot be negative".format(
                rule.get('name'), field))
    return value


def _normalize_extract_group(group):
    if group is None:
        return None
    if isinstance(group, bool):
        raise _ExecuteExtractError(
            "Execute extract group must be a name or integer")
    if isinstance(group, int):
        return group

    group = str(group)
    if not group:
        raise _ExecuteExtractError(
            "Execute extract group must be a name or integer")
    if group.isdigit():
        return int(group)
    return group


def _normalize_extract_type(rule):
    value = str(rule.get('type', 'str')).strip().lower()
    list_match = re.fullmatch(r'list\[(str|int|float|bool)\]', value)
    if list_match:
        if not rule['findall']:
            raise _ExecuteExtractError(
                "Execute extract rule '{}' type '{}' requires findall: true"
                .format(rule['name'], value))
        return list_match.group(1), True

    if value in ('str', 'int', 'float', 'bool'):
        return value, False

    raise _ExecuteExtractError(
        "Execute extract rule '{}' has unsupported type '{}'".format(
            rule['name'], value))


def _normalize_extract_rules(extract):
    if extract is None or extract == []:
        return []
    if not isinstance(extract, list):
        raise _ExecuteExtractError("Execute extract must be a list")

    rules = []
    names = set()
    for index, raw_rule in enumerate(extract):
        if not isinstance(raw_rule, dict):
            raise _ExecuteExtractError(
                "Execute extract rule at index {} must be a dictionary"
                .format(index))

        name = raw_rule.get('name')
        if not isinstance(name, str) or not name:
            raise _ExecuteExtractError(
                "Execute extract rule at index {} must define a name"
                .format(index))
        if name in names:
            raise _ExecuteExtractError(
                "Execute extract rule name '{}' is duplicated".format(name))
        names.add(name)

        regex = raw_rule.get('regex')
        if regex is None or not str(regex):
            raise _ExecuteExtractError(
                "Execute extract rule '{}' must define a regex".format(name))
        try:
            pattern = re.compile(str(regex), re.MULTILINE)
        except re.error as exc:
            raise _ExecuteExtractError(
                "Invalid execute extract regex for '{}': {}".format(
                    name, exc))

        rule = dict(raw_rule)
        rule['name'] = name
        rule['pattern'] = pattern
        rule['findall'] = _normalize_extract_bool(
            raw_rule, 'findall', False)
        rule['required'] = _normalize_extract_bool(
            raw_rule, 'required', False)
        rule['unique'] = _normalize_extract_bool(raw_rule, 'unique', False)
        rule['sort'] = _normalize_extract_bool(raw_rule, 'sort', False)
        rule['base_type'], explicit_list_type = _normalize_extract_type(rule)
        rule['list_output'] = rule['findall'] or explicit_list_type
        rule['group'] = _normalize_extract_group(raw_rule.get('group'))
        rule['min_count'] = _normalize_extract_count(raw_rule, 'min_count')
        rule['max_count'] = _normalize_extract_count(raw_rule, 'max_count')
        if (rule['min_count'] is not None and rule['max_count'] is not None
                and rule['min_count'] > rule['max_count']):
            raise _ExecuteExtractError(
                "Execute extract rule '{}' min_count cannot exceed max_count"
                .format(name))

        save_as = raw_rule.get('save_as', name)
        if not isinstance(save_as, str) or not save_as:
            raise _ExecuteExtractError(
                "Execute extract rule '{}' save_as must be a non-empty string"
                .format(name))
        rule['save_as'] = save_as
        rule['has_default'] = 'default' in raw_rule
        rule['default'] = raw_rule.get('default')
        rules.append(rule)

    return rules


def _has_execute_extract(extract):
    return extract is not None and extract != []


def _select_extract_match_value(rule, match):
    try:
        if rule['group'] is not None:
            return match.group(rule['group'])
        if rule['name'] in match.groupdict():
            return match.group(rule['name'])
        if rule['pattern'].groups == 1:
            return match.group(1)
        if rule['pattern'].groups == 0:
            return match.group(0)
    except (IndexError, KeyError):
        raise _ExecuteExtractError(
            "Execute extract rule '{}' references an invalid group '{}'"
            .format(rule['name'], rule['group']))

    raise _ExecuteExtractError(
        "Execute extract rule '{}' has ambiguous capture groups; set 'group'"
        .format(rule['name']))


def _coerce_extract_value(rule, value):
    base_type = rule['base_type']
    try:
        if base_type == 'str':
            return '' if value is None else str(value)
        if base_type == 'int':
            return int(value)
        if base_type == 'float':
            return float(value)
        if base_type == 'bool':
            if isinstance(value, bool):
                return value
            if isinstance(value, (int, float)) and value in (0, 1):
                return bool(value)
            value_str = str(value).strip().lower()
            if value_str in ('true', 'yes', 'on', '1'):
                return True
            if value_str in ('false', 'no', 'off', '0'):
                return False
    except (TypeError, ValueError):
        pass

    raise _ExecuteExtractError(
        "Execute extract rule '{}' could not coerce value '{}' to {}"
        .format(rule['name'], value, base_type))


def _default_extract_value(rule):
    if rule['has_default']:
        default = rule['default']
        if rule['list_output']:
            if isinstance(default, (list, tuple)):
                values = list(default)
            else:
                values = [default]
            return [_coerce_extract_value(rule, value) for value in values]
        return _coerce_extract_value(rule, default)

    if rule['list_output']:
        return []
    if rule['base_type'] == 'str':
        return ''
    if rule['base_type'] == 'int':
        return 0
    if rule['base_type'] == 'float':
        return 0.0
    return False


def _deduplicate_extract_values(values):
    deduplicated = []
    seen = set()
    for value in values:
        if value in seen:
            continue
        seen.add(value)
        deduplicated.append(value)
    return deduplicated


def _check_extract_count(rule, count):
    min_count = rule['min_count']
    max_count = rule['max_count']

    if min_count is not None and count < min_count:
        raise _ExecuteExtractRetryable(
            "Execute extract rule '{}' found {} matches, fewer than min_count {}"
            .format(rule['name'], count, min_count))
    if max_count is not None and count > max_count:
        raise _ExecuteExtractRetryable(
            "Execute extract rule '{}' found {} matches, more than max_count {}"
            .format(rule['name'], count, max_count))


def _evaluate_extract_rule(rule, output):
    matches = list(rule['pattern'].finditer(output))
    count = len(matches)

    if count == 0 and rule['required']:
        raise _ExecuteExtractRetryable(
            "Execute extract rule '{}' found no matches".format(rule['name']))

    _check_extract_count(rule, count)

    if count == 0:
        return _default_extract_value(rule)

    if rule['list_output']:
        values = [
            _select_extract_match_value(rule, match)
            for match in matches
        ]
        values = [_coerce_extract_value(rule, value) for value in values]
        if rule['unique']:
            values = _deduplicate_extract_values(values)
        if rule['sort']:
            try:
                values = sorted(values)
            except TypeError as exc:
                raise _ExecuteExtractError(
                    "Execute extract rule '{}' could not sort values: {}"
                    .format(rule['name'], exc))
        return values

    value = _select_extract_match_value(rule, matches[0])
    return _coerce_extract_value(rule, value)


def _apply_execute_extract(output,
                           extract,
                           blitz_obj=None,
                           section=None,
                           ret_dict=None):
    rules = _normalize_extract_rules(extract)
    if not rules:
        return {}

    output = '' if output is None else str(output)
    saved_values = {}
    for rule in rules:
        saved_values[rule['save_as']] = _evaluate_extract_rule(rule, output)

    for save_as, value in saved_values.items():
        if blitz_obj and section:
            save_variable(blitz_obj, section, save_as, value)
        if ret_dict is not None:
            ret_dict.setdefault('saved_vars', {})
            ret_dict['saved_vars'].update({save_as: value})

    return saved_values


def _output_query_template(output,
                           steps,
                           device,
                           command,
                           include,
                           exclude,
                           max_time,
                           check_interval,
                           continue_,
                           action,
                           result_status=None,
                           failed_result_status=None,
                           arguments=None,
                           rest_device_alias=None,
                           expected_failure=False,
                           scope=None,
                           blitz_obj=None,
                           section=None,
                           ret_dict=None,
                           extra_kwargs=None,
                           extract=None):

    if not extra_kwargs:
        extra_kwargs = {}

    keys = _include_exclude_list(include, exclude)
    if not action == 'yang':
        max_time, check_interval = _get_timeout_from_ratios(
            device=device, max_time=max_time, check_interval=check_interval)
    timeout = Timeout(max_time, check_interval)
    scoped_output = output

    if action == 'execute' and scope and not keys:
        step_msg = "Apply execute scope to the output"
        send_cmd = False
        step_result = Failed
        message = ''

        with steps.start(step_msg, continue_=continue_) as substep:
            while True:
                if send_cmd:
                    try:
                        output = _send_command(command,
                                               device,
                                               action,
                                               arguments=arguments,
                                               rest_device_alias=rest_device_alias,
                                               **extra_kwargs)
                    except SchemaEmptyParserError:
                        output = ''

                try:
                    scoped_output, _, _ = _apply_execute_scope(
                        output,
                        scope,
                        blitz_obj=blitz_obj,
                        section=section,
                        ret_dict=ret_dict)
                    step_result = Passed
                    message = "Execute scope matched the output."
                except _ExecuteScopeNotFound as exc:
                    step_result = Failed
                    message = str(exc)
                except _ExecuteScopeError as exc:
                    substep.failed(str(exc))
                    return output

                if step_result == Passed:
                    if expected_failure:
                        substep.failed(
                            '{} did not failed as expected, the step test '
                            'result is set as failed'.format(action))
                    else:
                        substep.passed(message)
                    break

                send_cmd = True
                timeout.sleep()
                if not timeout.iterate():
                    break

            if step_result == Failed:
                if expected_failure:
                    substep.passed(
                        '{} failed as expected, the step test result is set '
                        'as passed'.format(action))
                else:
                    substep.failed(message)

        output = scoped_output

    for query, style in keys:

        step_msg = "Verify that '{query}' is {style} in the output".\
                        format(query=query, style=style)
        if 'custom_verification_message' in extra_kwargs:
            custom_message = extra_kwargs.pop('custom_verification_message')
            if custom_message:
                step_msg = custom_message

        # dict that would be sent with various data for inclusion/exclusion check
        kwargs = {}
        send_cmd = False
        # for each query and style
        with steps.start(step_msg, continue_=continue_) as substep:

            while True:
                if send_cmd:
                    try:

                        output = _send_command(command,
                                               device,
                                               action,
                                               arguments=arguments,
                                               rest_device_alias=rest_device_alias,
                                               **extra_kwargs)

                    except SchemaEmptyParserError:
                        # add empty to proceed `include`/`exclude`/`max_time`/`check_interval`
                        output = ''

                if action == 'execute':
                    try:
                        scoped_output, scoped_parts, verify_each = \
                            _apply_execute_scope(
                                output,
                                scope,
                                blitz_obj=blitz_obj,
                                section=section,
                                ret_dict=ret_dict)
                    except _ExecuteScopeNotFound as exc:
                        step_result = Failed
                        message = str(exc)
                    except _ExecuteScopeError as exc:
                        substep.failed(str(exc))
                        return output
                    else:
                        step_result, message = _verify_execute_scope_query(
                            scoped_output, scoped_parts, verify_each, query,
                            style)

                else:
                    # verifying the inclusion/exclusion of actions : learn, parse and api
                    found = _get_output_from_query_validators(output, query)
                    kwargs = found
                    kwargs.update({'style': style, 'key': None})

                    # Function would return (pass | fail | error)
                    step_result, message = _verify_include_exclude(**kwargs)

                if expected_failure and step_result == Failed:
                    substep.passed(message)
                if not expected_failure and step_result == Passed:
                    # step_result will only change to result_status if it is passed.
                    if result_status:
                        log.warning('The result status is changed from passed to {}' \
                                    ' based on the result_status'.format(result_status))
                        getattr(substep, result_status)(message)
                    else:
                        substep.passed(message)
                if failed_result_status and step_result == Failed:
                    # step_result will only change to failed_result_status if it failed.
                    log.warning('The result status is changed from failed to {}' \
                                ' based on the failed_result_status'.format(failed_result_status))
                    getattr(substep, failed_result_status)(message)

                send_cmd = True
                timeout.sleep()
                if not timeout.iterate():
                    break

            # failing logic in case of timeout
            if (
                not expected_failure
                and step_result == Failed
                or expected_failure
                and step_result == Passed
            ):
                substep.failed(message)
            else:
                log.info(
                    '{} failed as expected, the step test result is set as passed'.format(action)
                )

    if action == 'execute' and scope:
        output = scoped_output

    if action == 'execute' and _has_execute_extract(extract):
        step_msg = "Apply execute extract to the output"
        send_cmd = False
        step_result = Failed
        message = ''
        extract_timeout = Timeout(max_time, check_interval)

        with steps.start(step_msg, continue_=continue_) as substep:
            while True:
                extract_output = output
                if send_cmd:
                    try:
                        extract_output = _send_command(
                            command,
                            device,
                            action,
                            arguments=arguments,
                            rest_device_alias=rest_device_alias,
                            **extra_kwargs)
                    except SchemaEmptyParserError:
                        extract_output = ''

                    if scope:
                        try:
                            extract_output, _, _ = _apply_execute_scope(
                                extract_output,
                                scope,
                                blitz_obj=blitz_obj,
                                section=section,
                                ret_dict=ret_dict)
                        except _ExecuteScopeNotFound as exc:
                            step_result = Failed
                            message = str(exc)
                            send_cmd = True
                            extract_timeout.sleep()
                            if not extract_timeout.iterate():
                                break
                            continue
                        except _ExecuteScopeError as exc:
                            substep.failed(str(exc))
                            return output

                try:
                    saved_values = _apply_execute_extract(
                        extract_output,
                        extract,
                        blitz_obj=blitz_obj,
                        section=section,
                        ret_dict=ret_dict)
                    step_result = Passed
                    message = "Execute extract saved variable(s): {}".format(
                        ', '.join(saved_values.keys()))
                    output = extract_output
                except _ExecuteExtractRetryable as exc:
                    step_result = Failed
                    message = str(exc)
                except _ExecuteExtractError as exc:
                    substep.failed(str(exc))
                    return output

                if step_result == Passed:
                    if expected_failure:
                        substep.failed(
                            '{} did not failed as expected, the step test '
                            'result is set as failed'.format(action))
                    else:
                        substep.passed(message)
                    break

                send_cmd = True
                extract_timeout.sleep()
                if not extract_timeout.iterate():
                    break

            if step_result == Failed:
                if expected_failure:
                    substep.passed(
                        '{} failed as expected, the step test result is set '
                        'as passed'.format(action))
                else:
                    substep.failed(message)

    # If no keys, if expected failure, steps results has to be reversed
    if (not keys and expected_failure
            and not (action == 'execute'
                     and (scope or _has_execute_extract(extract)))):
        if steps.result == Passed:
            steps.failed(
                    '{} did not failed as expected, the step test result is set as failed'
                    .format(action)
                    )
        else:

            steps.passed(
                    '{} did failed as expected, the step test result is set as passed'
                    .format(action)
                    )

    # steps.result will only change to result_status if it is passed.
    if result_status and steps.result == Passed:
        result_status_message = 'The {} result status is changed from passed to {}' \
                                ' based on the result_status'.format(action, result_status)
        log.warning(result_status_message)
        getattr(steps, result_status)(result_status_message)
    elif failed_result_status and steps.result == Failed:
        result_status_message = 'The {} result status is changed from failed to {}' \
                                ' based on the result_status'.format(action, failed_result_status)
        log.warning(result_status_message)
        getattr(steps, failed_result_status)(result_status_message)

    return output

def _include_exclude_list(include, exclude):
    """
    create the list of queries that would be checked for include or exclude
    """
    keys = []
    if include:
        for item in include:
            keys.append((item, 'included'))
    if exclude:
        for item in exclude:
            keys.append((item, 'excluded'))

    return keys

def _get_timeout_from_ratios(device, max_time, check_interval):
    """
    update timeout from ratios provided in tests
    """
    max_time_ratio = device.custom.get('max_time_ratio', None)
    if max_time and max_time_ratio:
        try:
            max_time = int(max_time * float(max_time_ratio))
        except ValueError:
            log.error(
                'The max_time_ratio ({m}) value is not of type float'.format(
                    m=max_time_ratio))

    check_interval_ratio = device.custom.get('check_interval_ratio', None)
    if check_interval and check_interval_ratio:
        try:
            check_interval = int(check_interval * float(check_interval_ratio))
        except ValueError:
            log.error(
                'The check_interval_ratio ({c}) value is not of type float'.
                format(c=check_interval_ratio))

    if max_time and not check_interval:
        check_interval = 0.0

    return max_time, check_interval

def _send_command(command,
                  device,
                  action,
                  arguments=None,
                  rest_device_alias=None,
                  **kwargs):
    """
    sending command to get restarted if max_time and check interval
    """
    # if api
    if action == 'api':
        if not arguments:
            arguments = {}
        api_func = device if device.os == 'ixianative' else device.api
        return getattr(api_func, command)(**arguments)

    # if learn
    elif action == ' learn':
        return getattr(device, action)(command).to_dict()

    # if rest action
    elif action == 'rest':
        output = getattr(rest_device_alias, command)(**kwargs)
        log.info(output)
        return output

    elif action == 'bash_console':

        output_dict = {}
        with device.bash_console(**kwargs) as bash:
            for cmd in command:
                bash_command_output = bash.execute(cmd, **kwargs)
                if isinstance(bash_command_output, dict):
                    output_dict.update(bash_command_output)
                else:
                    output_dict.update({cmd:bash_command_output})

        return output_dict

    # for everything else, just check if reply should get updated

    if  'reply' in kwargs and action == 'execute':
        kwargs.update({'reply': _prompt_handler(kwargs['reply'])})

    return getattr(device, action)(command, **kwargs)

def _get_output_from_query_validators(output, query):
    """the function determines the type of query and
       returns the appropriate result"""

    ret_dict = {}
    # if it is a valid dq query than apply the query and return the output
    if Dq.query_validator(query):
        output = Dq.str_to_dq_query(output, query)
        ret_dict.update({
            'action_output': output,
            'query_type': 'dq_query',
            'operation': None,
            'expected_value': None
        })
    # if the query is itself a dictionary
    elif isinstance(query, (dict, list)):
        # output could of of type dict/QDict
        # NOTE: QDict is the type of the parser output
        if isinstance(output, QDict):
            output = dict(output)

        ret_dict.update({
            'action_output': output,
            'query_type': 'non_dq_query',
            'operation': '',
            'expected_value': query
        })
    else:
        # check for the string query
        output = _string_query_validator(output, query)
        action_output = output['right_hand_value']
        operation = output['operation']
        value = output['left_hand_value']
        ret_dict.update({
            'action_output': action_output,
            'query_type': 'non_dq_query',
            'operation': operation,
            'expected_value': value
        })

    return ret_dict

def _string_query_validator(right_hand_value, query):
    """
        Validating the queries that are string:
        e.g: (>=1220), (!= 100),
             (>= 100 && <= 200), ( == some string)
    """
    # These queries mostly used for verifying api outputs that are digits or string
    # if the query does not match the expected pattern raise valueerror
    ret_dict = {}
    p = re.compile(r'(?P<operation>[>=<!\s]*)(?P<left_hand_value>[\S\s]+)')

    if '&&' in str(query):
        # if range return the value of this function
        return _string_query_range_validator(right_hand_value, query)

    m = p.match(str(query))
    if not m:
        # raising error if query is not inputted as per instructions
        raise ValueError(
            "The query: '{}' is not entered properly".format(query))

    # extract values from include/exclude queries
    # and change their types from string to the proper types
    # accordingly
    groups_dict = _query_values_type_update(
                                            right_hand_value, m.groupdict(), query)

    ret_dict.update({
        'right_hand_value': right_hand_value,
        'operation': groups_dict['operation'],
        'left_hand_value': groups_dict['left_hand_value']
    })

    return ret_dict

def _string_query_range_validator(output, query):
    """
    validating users queries like (>= 1200 && <=2000)
    """
    # list of valid operations in case of a range call we don't want = or !=
    list_of_ops = ['>=', '<=', '>', '<']

    # list of values that later will be our range
    value_list = []
    ret_dict = {}

    # splitting the range input (>=1220 && <=2000) on '&&'
    # making each element of this list as one operation
    # range_query_list[0] = ">=1220" and range_query_list[1] = "<=2000"
    range_query_list = query.split('&&')

    # we need the set to be able to not allow duplicate operators to be in a same query
    set_of_input_ops = set()

    # for each operation and operand
    for q in range_query_list:
        # send it back to _string_query_validator for extracting the value and operator
        single_query_dict = _string_query_validator(output, q)
        # the length of the spillted query cannot be anything other than 2 because it is a range
        # examples of not valid range: >=1220 && ==1300, <1200 && <= 2300, >1200 && <230
        # example of a valid: > 1200 && <= 2300, >= 1220 && <= 2330, >1000 && <2000
        if not single_query_dict['operation'] \
           or single_query_dict['operation'] not in list_of_ops \
           or single_query_dict['operation'] in set_of_input_ops \
           or len(range_query_list) != 2:

            raise Exception('The input is not describing a range')
        range_value = int(single_query_dict['left_hand_value'])
        # have to update this set to make sure that users is not using duplicate operations and it always is using range valid ops
        if single_query_dict['operation'] in ['>', '>=']:
            set_of_input_ops.update(['>', '>='])

        if single_query_dict['operation'] in ['<', '<=']:
            set_of_input_ops.update(['<', '<='])

        # giving user the freedom of using > or >=
        # Using range func, the last value in this function is always excluded.
        # The first value is always included. If users input operation is > the first value
        # should be excluded and if operation is <= the last value should be included.
        # Adding 1 to the value for such instances.
        if single_query_dict['operation'] in ['>', '<=']:
            range_value += 1

        value_list.append(range_value)

    if int(value_list[1]) <= int(value_list[0]):

        raise Exception(
            'This is not describing a range, the end of the '
            'interval {} cannot be smaller or equal its start {}'.format(
                str(value_list[1]), str(value_list[0])))

    # create the range object out of the extracted output and return the value
    value = range(int(value_list[0]), int(value_list[1]))
    operation = 'within'
    ret_dict.update({
        'right_hand_value': output,
        'operation': operation,
        'left_hand_value': value
    })

    return ret_dict

# Do we need a better name?
def _query_values_type_update(right_hand_value, groups_dict, query):
    """
    extract values from include/exclude queries
    and change their types from string to the proper types
    accordingly
    """

    left_hand_value = groups_dict['left_hand_value'].strip()
    operation = groups_dict['operation'].replace(' ', '')
    right_hand_value_type = type(right_hand_value)

    # Checking if the type of the query is bool
    # e.g: include:
    #         - True
    if right_hand_value_type == bool and isinstance(query, bool):
        left_hand_value = _true_false_eval(left_hand_value)

    # if the type of output is list
    # either apply regex on items of the list and
    # match, or check if the entire item exist in
    # the list
    elif right_hand_value_type == list:

        try:
            # ast.literal_eval casts string representation of lists/int/dict to the actual values
            # e.g "[1,2,3]" to [1,2,3]
            # e.g or "1" to 1
            left_hand_value = ast.literal_eval(left_hand_value)

            # the include operation is set to contains
            # checks if a list contains the input value
            operation = 'contains'
        except (ValueError, SyntaxError):

            # If errored out then the query is definitely a string
            # if query is string, check if the string(or regex string)
            # exist in the output
            operation = 'contains_regex'
    else:
        try:
            # cast the input value to result value
            # for arithmetic cases with normal operators (>, =, <)
            left_hand_value = right_hand_value_type(left_hand_value)
        except Exception:
            pass

    groups_dict.update({'left_hand_value': left_hand_value,
                        'operation': operation})

    return groups_dict

def _verify_include_exclude(action_output,
                            style,
                            query_type,
                            operation=None,
                            expected_value=None,
                            key=None):
    """ Checking the inclusion or exclusion and verifies result values
        With regards to different operations for actions ('api','parse', 'learn')
    """

    if query_type in ['non_dq_query']:
        # if a value exist to compare the result
        return _verify_string_query_include_exclude(action_output,
                                                    expected_value,
                                                    style,
                                                    operation=operation)

    # if results are dictionary and the queries are in dq format ( contains('value'))
    return _verify_dq_query_and_execute_include_exclude(
                                                        action_output, style, key)

def _verify_string_query_include_exclude(action_output,
                                         expected_value,
                                         style,
                                         operation=None):

    # dictionary of log message templates per each action
    # "within" is for checking range scenario, e.g: 12 > && < 20
    # "others" is for normal arithmetic cases, e.g: >=12, == 11, < 1
    dict_of_log_msg = {
        'within': "The result '{result}' is '{operation}' in the {value}",
        'contains': "The value '{value}' is '{operation}' in the result '{result}'",
        'contains_regex': "The pattern '{value}' is {operation} in the result {result}",
        'others': "The result '{result}' is '{operation}' to '{value}'"
    }

    # update, operation names based on styles and update
    # dictionary of log massages with regards to the styles
    operation, dict_of_log_msg = \
         _operation_to_style_map(style, operation, dict_of_log_msg)

    # operation can be operation itself or in case of checking
    # that if an item exist in a list, be changed to
    # include/exclude for logging purposes
    if operation in ['contains', 'contains_regex',
                     'not_contains', 'not_contains_regex',
                     'within', 'not_within']:
        operation_str = style

    else:
        operation_str = operation

    if _evaluate_operator(result=action_output,
                          operation=operation,
                          value=expected_value):

        query_result = Passed
    else:
        query_result = Failed
        operation_str = 'not ' + operation_str

    if operation in dict_of_log_msg:
        msg = dict_of_log_msg[operation].\
                            format(result=action_output,
                                   value=expected_value,
                                   operation=operation_str)
    else:
        msg = dict_of_log_msg['others'].\
                            format(result=action_output,
                                   value=expected_value,
                                   operation=operation_str)

    return query_result, msg

def _operation_to_style_map(style, operation, dict_of_log_msg):
    """
        Operations need to be updated in cases that:
        1) no operator is provided and the goal is to == or !=
        2) the style is exclude yet we are checking for contains/within/not contains
    """

    if style == 'excluded':
        if not operation:
            operation = '!='

        elif operation in ['contains', 'within', 'contains_regex']:

            # create a new operator for exclusion
            msg = dict_of_log_msg[operation]
            operation = "{}{}".format('not_',operation)
            dict_of_log_msg.update({operation:msg})

    elif style == 'included':
        if not operation:
            operation = '=='

    return (operation, dict_of_log_msg)

def _evaluate_operator(result, operation=None, value=None):
    # convert list, dict from string
    # when only value is given without operator
    # ex. ) if: "$VARIABLES{test}"
    if value == 'None':
        try:
            result = ast.literal_eval(result)
            value = ast.literal_eval(value)
        except ValueError:
            pass

    # used to evaluate the operation results
    # if number 6 operations
    if isinstance(value, (float, int)) and isinstance(result, (float, int)):
        dict_of_ops = {
            '==': operator.eq,
            '>=': operator.ge,
            '>': operator.gt,
            '<=': operator.le,
            '<': operator.le,
            '!=': operator.ne
        }
    elif isinstance(result, (float, int)) and isinstance(value, range):

        # just check if the first argument is within the second argument,
        # changing the operands order of contains function (in)
        # e.g: include:
        #           - > 1220 && < 1800
        dict_of_ops = {'within': lambda item, container: item in container,
                       'not_within': lambda item, container: item not in container,}

    elif isinstance(result, (list, tuple)):

        # contains/not_contains is the operation when the result is a list
        # e.g: result = [1,2,3,4] and wants to see if the output includes 1
        # When matching a pattern or a keyword against items of a list
        # The operation is set to regex/exclude_regex
        # e.g: result = ['banana1', 'banana2', 'apple'] and wants to see if
        # the output includes 'banana.*'
        dict_of_ops = {'contains': operator.contains,
                       'not_contains': operator.contains,
                       'contains_regex': _regex_in_list,
                       'not_contains_regex': _regex_in_list,
                       '==': operator.eq,
                       '!=': operator.ne
                        }

    elif (type(result) == type(value)) and \
         isinstance(result, str) and isinstance(value, str):

        dict_of_ops = {'==': operator.eq, '!=': operator.ne,
                       'contains': operator.contains,
                       'not_contains': operator.contains}

    elif type(result) == type(value):
        # if strings just check  inclusion
        dict_of_ops = {'==': operator.eq, '!=': operator.ne}
    else:
        # if any other type return error
        return False

    # if no operation is given, set '==' and 'True'
    # and bool(result) then return result
    if not operation:
        operation = '=='
        value = True
        eval_oper = dict_of_ops[operation](bool(ast.literal_eval(result)), value)
        log.debug('_evaluate_operator: {}'.format(eval_oper))
        return eval_oper
    # if the operation is not valid errors the testcase
    if operation not in dict_of_ops:
        log.error('Operator {} is not supported'.format(operation))
        return False

    # reverse the outputs for not_contains and when the goal is to not match regex
    if operation in ['not_contains','not_contains_regex']:
        return not dict_of_ops[operation](result, value)

    eval_oper = dict_of_ops[operation](result, value)
    log.debug('return of _evaluate_operator: {}'.format(eval_oper))
    return eval_oper

def _regex_in_list(result, value):

    # loop over each item in a list
    # regex match against each of them
    # if matched anything return True
    return any(re.search(value, str(item)) for item in result)

def _verify_dq_query_and_execute_include_exclude(action_output, style, key):

    # Validating execute include exclude keys and queries that are following dq formats

    # if key is a query of type (contains('status')) then we show the resulted output
    # otherwise the key itself usually for execute action

    msg_style = ''
    message = "'{style}' criteria is {ms}."

    if (style == "included" and
        action_output or
        style == 'excluded' and
        not action_output):

        # change the msg_style depending on style
        msg_style =  "present in output" if style == "included" else "not present in output"
        return (Passed, message.format(style=style[:-1], ms=msg_style))
    else:
        # change the msg_style depending on style
        msg_style = "present in output" if style == "excluded" else "not present in output"
        return (Failed, message.format(style=style[:-1], ms=msg_style))

def _condition_validator(items):

    log.debug('_condition_validator items: {}'.format(items))

    # Checking condition useful for both condition work itself and action compare.
    # e.g: 2 > 1 or '%VARIABLES{ball}' == 'nine' and  '%VARIABLES{yall} > 12'
    pattern = re.compile(
        r"^(?!None$)(?P<right_hand_value>[^>=<!]+)(?P<ops_and_left_hand_value>[\S\s]+)")

    # split on \(\) for cases with "%VARIABLES{name} == 22 and (%VARIABLES{nam} == 12 or %VARIABLES{am} == 32)"
    try:
        items_splitted_on_bracket = re.split(r"\(|\)", items)
    except TypeError:
        # if the items is list or etc, just put in list
        items_splitted_on_bracket = [items]

    for each_item_in_bracket in items_splitted_on_bracket:

        # split on and|or on each item
        # 12 > 11 and 'sia' == 'sia' --> [12>11, 'sia'=='sia']
        try:
            items_list = re.split(r"\s+and\s+|\s+or\s+", each_item_in_bracket)
        except TypeError:
            # if no `and`/`or`, just put in list
            items_list = [each_item_in_bracket]
        for item in items_list:

            try:
                if not item.strip():
                    continue

                m = pattern.match(item)
                # ex.) if: "$VARIABLES{test} == 10"
                if m:
                    group = m.groupdict()
                    right_hand_value = group['right_hand_value']
                    ops_and_left_hand_value = group['ops_and_left_hand_value']
                # ex.) if: "$VARIABLES{test}"
                else:
                    right_hand_value = item
                    ops_and_left_hand_value = " == True"
            # ex.) True (no operator, no left_hand_value)
            except AttributeError:
                right_hand_value = item
                ops_and_left_hand_value = " == True"

            if not isinstance(right_hand_value, bool):
                try:
                    right_hand_value = float(right_hand_value)
                except (ValueError, TypeError):
                    pass

            # Extracting right hand, left hand and operator for each comparision
            output = _string_query_validator(right_hand_value,
                                             ops_and_left_hand_value)

            right_hand = output['right_hand_value']
            right_hand = right_hand.strip() if isinstance(right_hand, str) else right_hand
            operation = output['operation'].strip()
            left_hand = output['left_hand_value']
            left_hand = left_hand if isinstance(left_hand, (float, int)) else left_hand.strip()

            log.debug('right_hand: {}, operation {}, left_hand {}'.format(right_hand, operation, left_hand))
            result = _evaluate_operator(right_hand,
                                        operation=operation,
                                        value=left_hand)
            try:
                items = items.replace(item, ' ' + str(result) + ' ')
            # keep dict/list as is
            except AttributeError:
                pass

    try:
        ret_val = _true_false_eval(items)
    except Exception as e:
        log.error("Invalid boolean expression {}.".format(str(e)))
        ret_val = False

    try:
        ret_val = bool(ret_val)
    except Exception:
        pass

    return ret_val

def _true_false_eval(bool_exp):
    '''
    This function is an alternative to eval
    Type of input that works with function are:

    e.g:
        _true_false_eval("True or False and (True or False)") == True
        _true_false_eval("True and False") == False
        _true_false_eval("True") == True
        _true_false_eval("True and (True and (True or False))") == True
    '''
    dict_of_ops = {'or': operator.or_, 'and': operator.and_}
    dict_of_bools = {'True': True, 'False': False}

    p = re.compile(r"\(([a-zA-Z\s]+)\)")

    # loop while bool_exp is not a boolean,
    # stop looping when its a boolean
    while isinstance(bool_exp, str):
        m = p.search(bool_exp)
        if m:

            # Recursively find out each boolean expression inside brackets
            # and evaluate each expression to its boolean equivalent (True/False) and replace until
            # no brackets left
            bool_exp = bool_exp.replace(m.group(0), str(_true_false_eval(m.group(1))))
            continue

        # list of True and False  ['True', 'False']
        bool_exp_list = re.split(r"\s+and\s+|\s+or\s+", bool_exp)

        # if after splitting on and/or this list contains anything
        # other than True/False raise Exception, because bool_exp
        # only contains True/False
        for item in bool_exp_list:
            if item.strip() not in list(dict_of_bools.keys()):
                # empty string ('') handling. 
                # The case is that VARIABLE is not initialized. Return False
                if bool_exp == '':
                    return False
                raise Exception("{} is an invalid boolean expression. "
                                "A boolean expression only contains of True/False".format(bool_exp))

        # list of and/or ['or']
        and_or_list = re.split(r"\s*True\s*|\s*False\s*", bool_exp)
        and_or_list = [item for item in and_or_list if item.strip()]

        # When collecting and/or if for any reason a value other than
        # and/or is picked up by this list raise Exception
        for item in and_or_list:
            if item.strip() not in list(dict_of_ops.keys()):
                raise Exception("{} is an invalid boolean expression. "
                                "A boolean expression only contains of True/False".format(bool_exp))

        # all the and/or together + 1 == all of the True/False
        # Always the case
        if len(and_or_list) +1 != len(bool_exp_list):
            raise Exception("{} is an invalid boolean expression".format(bool_exp))

        # check bool expression until we have one final True/False
        while len(bool_exp_list) > 1:

            right_hand_val = dict_of_bools[bool_exp_list.pop(0).strip()]
            left_hand_val = dict_of_bools[bool_exp_list.pop(0).strip()]
            ops = and_or_list.pop(0)

            bool_exp_list.insert(0,
                            str(dict_of_ops[ops.strip()](right_hand_val, left_hand_val)))

        bool_exp = dict_of_bools[bool_exp_list[0].strip()]

    return bool_exp

def _get_exclude(command, device):

    if command:
        try:
            # Try parser
            return get_parser_exclude(command, device)
        except Exception:
            pass
        try:
            # Try ops
            return get_ops_exclude(command, device)
        except Exception:
            pass
    return []
