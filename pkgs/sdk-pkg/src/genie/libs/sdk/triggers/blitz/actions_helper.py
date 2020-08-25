import re
import logging
import operator
import xmltodict
import xml.etree.ElementTree as ET

# from genie
from genie.utils.dq import Dq
from genie.conf.base.utils import QDict
from genie.utils.timeout import Timeout
from genie.ops.utils import get_ops_exclude
from genie.libs.parser.utils import get_parser_exclude
from genie.metaparser.util.exceptions import SchemaEmptyParserError

# from pyats
from pyats.results import Passed, Failed

# from unicon
from unicon.eal.dialogs import Statement, Dialog

log = logging.getLogger(__name__)


def configure_handler(self, step, device, command, reply=None):

    kwargs = {}
    if reply:
        kwargs.update({'reply': _prompt_handler(reply)})

    try:
        # if reply dialog exist append to command if not configure normal command
        output = device.configure(command, **kwargs)
    except Exception as e:
        step.failed('Configure failed {}'.format(str(e)))

    return output


def parse_handler(self,
                  step,
                  device,
                  command,
                  include=None,
                  exclude=None,
                  max_time=None,
                  check_interval=None,
                  continue_=True,
                  action='parse'):
    # handeling parse command
    try:
        output = device.parse(command)
    # check if the parser is empty then return an empty dictionary
    except SchemaEmptyParserError:
        if include or exclude or (max_time and check_interval):
            output = ''
            return _output_query_template(self, output, step, device, command,
                                          include, exclude, max_time,
                                          check_interval, continue_, action)
        else:
            step.passed('The result of this command is an empty parser.')

    else:
        # go through the include/exclude process
        return _output_query_template(self, output, step, device, command,
                                      include, exclude, max_time,
                                      check_interval, continue_, action)


def execute_handler(self,
                    step,
                    device,
                    command,
                    include=None,
                    exclude=None,
                    max_time=None,
                    check_interval=None,
                    continue_=True,
                    action='execute',
                    reply=None):

    kwargs = {}
    if reply:
        kwargs.update({'reply': _prompt_handler(reply)})

    # handeling execute command
    output = device.execute(command, **kwargs)

    return _output_query_template(self,
                                  output,
                                  step,
                                  device,
                                  command,
                                  include,
                                  exclude,
                                  max_time,
                                  check_interval,
                                  continue_,
                                  action,
                                  reply=reply)


def learn_handler(self,
                  step,
                  device,
                  command,
                  include=None,
                  exclude=None,
                  max_time=None,
                  check_interval=None,
                  continue_=True,
                  action='learn'):

    # Save the to_dict learn output,
    output = device.learn(command).to_dict()
    return _output_query_template(self, output, step, device, command, include,
                                  exclude, max_time, check_interval, continue_,
                                  action)


def api_handler(self,
                step,
                device,
                command,
                include=None,
                exclude=None,
                max_time=None,
                check_interval=None,
                continue_=True,
                arguments=None,
                action='api'):
    #handeling api command
    output = None
    # if no arguments send an empty argument list to api function
    if not arguments:
        arguments = {}

    # check the os and decide how to call the api_function
    # will be changed when we figure out the use of device.type for more general use
    api_function = device if device.os == 'ixianative' else device.api
    if arguments.get('device'):
        # if device does not exist error
        try:
            arg_device = device.testbed.devices[arguments['device']]
        except KeyError as e:
            step.errored('Cannot find device {} in testbed'.format(
                arguments['device']))
        else:
            arguments['device'] = arg_device

    try:
        output = getattr(api_function, command)(**arguments)
    except (AttributeError, TypeError
            ) as e:  # if could not find api or the kwargs is wrong for api
        step.errored(str(e))
    except Exception as e:  # anything else
        step.failed(str(e))

    return _output_query_template(self,
                                  output,
                                  step,
                                  device,
                                  command,
                                  include,
                                  exclude,
                                  max_time,
                                  check_interval,
                                  continue_,
                                  action,
                                  arguments=arguments)


def rest_handler(self,
                 device,
                 method,
                 step,
                 continue_=True,
                 include=None,
                 exclude=None,
                 max_time=None,
                 check_interval=None,
                 action='rest',
                 connection_alias='rest',
                 *args,
                 **kwargs):
    output = ''

    # Checking the connection alias
    try:
        device_alias = getattr(device, connection_alias)
    except AttributeError as e:
        raise Exception("'{dev}' does not have a connection with the "
                        "alias '{alias}'".format(
                            dev=device.name, alias=connection_alias)) from e

    # Calling the http protocol
    try:
        output = getattr(device_alias, method)(**kwargs)
    except Exception as e:
        step.failed("REST method '{}' failed. Error: {}".format(method, e))

    # if xml convert it to json
    if output and ET.iselement(output):
        output = xmltodict.parse(output)

    log.info(output)

    return _output_query_template(self,
                                  output,
                                  step,
                                  device,
                                  method,
                                  include,
                                  exclude,
                                  max_time,
                                  check_interval,
                                  continue_,
                                  action,
                                  rest_device_alias=device_alias,
                                  rest_kwargs=kwargs)


def _prompt_handler(reply):

    # handeling the reply for instances that a prompt message would get displayed in the console
    dialog_list = [Statement(**statement) for statement in reply]
    return Dialog(dialog_list)


def _output_query_template(self,
                           output,
                           steps,
                           device,
                           command,
                           include,
                           exclude,
                           max_time,
                           check_interval,
                           continue_,
                           action,
                           reply=None,
                           arguments=None,
                           rest_device_alias=None,
                           rest_kwargs={}):

    keys = _include_exclude_list(include, exclude)
    max_time, check_interval = _get_timeout_from_ratios(
        device=device, max_time=max_time, check_interval=check_interval)

    timeout = Timeout(max_time, check_interval)
    for query, style in keys:
        # dict that would be sent with various data for inclusion/exclusion check
        kwargs = {}
        send_cmd = False
        # for each query and style
        with steps.start("Verify that '{query}' is {style} in the output".\
                    format(query=query, style=style), continue_=continue_) as substep:

            while True:

                if send_cmd:
                    try:
                        output = _send_command(
                            command,
                            device,
                            action,
                            arguments=arguments,
                            reply=reply,
                            rest_device_alias=rest_device_alias,
                            rest_kwargs=rest_kwargs)
                    except SchemaEmptyParserError:
                        # add empty to proceed `include`/`exclude`/`max_time`/`check_interval`
                        output = ''

                if action in ['execute', 'maple_search']:
                    # validating the inclusion/exclusion of action execute,
                    pattern = re.compile(str(query))
                    found = pattern.search(str(output))
                    kwargs.update({
                        'action_output': found,
                        'operation': None,
                        'expected_value': None,
                        'style': style,
                        'key': query,
                        'query_type': 'execute_query'
                    })
                else:
                    # verifying the inclusion/exclusion of actions : learn, parse and api
                    found = _get_output_from_query_validators(output, query)
                    kwargs = found
                    kwargs.update({'style': style, 'key': None})

                # Function would return (pass | fail | error)
                step_result, message = _verify_include_exclude(**kwargs)

                if step_result == Passed:
                    substep.passed(message)

                send_cmd = True
                timeout.sleep()
                if not timeout.iterate():
                    break

            # failing logic in case of timeout
            substep.failed(message)

    return output


def _send_command(command,
                  device,
                  action,
                  arguments=None,
                  reply=None,
                  rest_device_alias=None,
                  rest_kwargs={}):

    # sending command to get restarted if max_time
    kwargs = {}

    # if api
    if action == 'api':
        if not arguments:
            arguments = {}
        if device.os == 'ixianative':
            api_func = device
        else:
            api_func = device.api

        return getattr(api_func, command)(**arguments)

    # if learn
    elif action == ' learn':
        return getattr(device, action)(command).to_dict()

    # if rest action
    elif action == 'rest':
        output = getattr(rest_device_alias, command)(**rest_kwargs)
        log.info(output)
        return output

    # for everything else, just check if reply should get updated

    if reply and action == 'execute':
        kwargs.update({'reply': _prompt_handler(reply)})

    return getattr(device, action)(command, **kwargs)


def _include_exclude_list(include, exclude):
    # create the list of queries that would be checked for include or exclude
    keys = []
    if include:
        for item in include:
            keys.append((item, 'included'))
    if exclude:
        for item in exclude:
            keys.append((item, 'excluded'))

    return keys


def _get_timeout_from_ratios(device, max_time, check_interval):

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


def _verify_include_exclude(action_output,
                            style,
                            query_type,
                            operation=None,
                            expected_value=None,
                            key=None):
    # Checking the inclusion or exclusion and verifies result values
    # With regards to different operations for actions ('api','parse', 'learn')
    if query_type in ['non_dq_query', 'compare_query']:
        # if a value exist to compare the result
        return _verify_string_query_include_exclude(action_output,
                                                    expected_value,
                                                    style,
                                                    operation=operation)
    else:
        # if results are dictionary and the queries are in dq format ( contains('value'))
        return _verify_dq_query_and_execute_include_exclude(
            action_output, style, key)


def _verify_string_query_include_exclude(action_output,
                                         expected_value,
                                         style,
                                         operation=None):
    # the query is in this format : ">= 1200"
    # verify the operator and value results for non dq queries (mostly apis)
    if not operation:
        # default operation based on style
        if style == 'included':
            operation = '=='
        elif style == 'excluded':
            operation = '!='

    # message template for the case that we are validating the result within a range
    msg_if_range = 'The result "{result}" is "{operation}" the range provided in the trigger datafile'
    # message template for other general cases
    msg = 'The result "{result}" is "{operation}" to "{value}" provided in the trigger datafile"'

    if _evaluate_operator(result=action_output,
                          operation=operation,
                          value=expected_value):
        # Step would be Passed

        # The only current exception, when user asks for checking a range
        if isinstance(expected_value, range):
            return (Passed,
                    msg_if_range.format(result=action_output,
                                        operation=operation))

        return (Passed,
                msg.format(result=action_output,
                           value=expected_value,
                           operation=operation))

    else:

        if isinstance(expected_value, range):
            return (Failed,
                    msg_if_range.format(result=action_output,
                                        operation="not " + operation))

        return (Failed,
                msg.format(result=action_output,
                           value=expected_value,
                           operation="not " + operation))


def _verify_dq_query_and_execute_include_exclude(action_output, style, key):

    # Validating execute include exclude keys and queries that are following dq formats

    # if key is a query of type (contains('status')) then we show the resulted output
    # otherwise the key itself usually for execute action
    if not key:
        key = action_output

    message = "'{k}' is {s} in the output"

    if (style == "included" and action_output
            or style == 'excluded' and not action_output):
        return (Passed, message.format(k=key, s=style))
    else:
        # change the style if it is not included for reporting
        return (Failed, message.format(k=key, s='not ' + style))


def _get_output_from_query_validators(output, query):
    # the function determines the type of query and returns the appropriate result
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


def _condition_validator(items):

    # Checking condition useful for both condition work itself and action compare.
    pattern = re.compile(
        r"(?P<right_hand_value>[^>=<!]+)(?P<ops_and_left_hand_value>[\S\s]+)")

    # split on and|or on each item
    # 12 > 11 and 'sia' == 'sia' --> [12>11, 'sia'=='sia']
    items_list = re.split(r"and|or", items)
    ret_dict = {}

    for item in items_list:

        m = pattern.match(item)
        if not m:
            raise Exception('Wrong input')

        group = m.groupdict()
        right_hand_value = group['right_hand_value'].strip()
        ops_and_left_hand_value = group['ops_and_left_hand_value'].strip()

        try:
            right_hand_value = float(right_hand_value)
        except ValueError:
            pass

        # Extracting right hand, left hand and operator for each comparision
        output = _string_query_validator(right_hand_value,
                                         ops_and_left_hand_value)
        right_hand = output['right_hand_value']
        operation = output['operation']
        left_hand = output['left_hand_value']
        result = _evaluate_operator(right_hand,
                                    operation=operation,
                                    value=left_hand)
        items = items.replace(item, ' ' + str(result) + ' ')

    ret_dict.update({
        'right_hand': right_hand,
        'left_hand': left_hand,
        'operation': operation,
        'condition_output': eval(items)
    })

    return ret_dict


def _string_query_validator(right_hand_value, query):

    # if the query is of type dictionary or a list
    # the output of the parsers are of type QDict
    # hence right_hand_values that are of type
    # QDict or parsers outputs, needs to be caste to dict
    if isinstance(query, (dict, list)):
        if isinstance(right_hand_value, (dict, QDict)):
            right_hand_value = dict(right_hand_value)

        return {
            'right_hand_value': right_hand_value,
            'operation': '',
            'left_hand_value': query
        }

    # Validating users queries like (>=1220), (!= 100), (>= 100 && <= 200), ( == some string)
    # These queries mostly used for verifying api outputs that are digits or string
    # if the query does not match the expected pattern raise valueerror
    ret_dict = {}
    p = re.compile(r'(?P<operation>[>=<!\s]*)(?P<left_hand_value>[\S\s]+)')

    if '&&' in query:
        # if range return the value of this function
        return _string_query_range_validator(right_hand_value, query)

    # striping the query from spaces
    m = p.match(query)
    if not m:
        # raising error if query is not inputted as per instructions
        raise ValueError(
            "The query: '{}' is not entered properly".format(query))

    left_hand_value = m.groupdict()['left_hand_value'].strip(' ')
    operation = m.groupdict()['operation'].replace(' ', '')

    right_hand_value_type = type(right_hand_value)
    try:
        # cast the input value to result value
        left_hand_value = right_hand_value_type(left_hand_value)
    except Exception:
        pass
    finally:
        ret_dict.update({
            'right_hand_value': right_hand_value,
            'operation': operation,
            'left_hand_value': left_hand_value
        })

    return ret_dict


def _string_query_range_validator(output, query):
    # validating users queries like (>= 1200 && <=2000)

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


def _evaluate_operator(result, operation=None, value=None):
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
        dict_of_ops = {'within': lambda item, container: item in container}
    elif type(result) == type(value):

        dict_of_ops = {'==': operator.eq, '!=': operator.ne}

        if isinstance(result, str) and isinstance(value, str):
            # if strings just check  inclusion
            dict_of_ops.update({'in': operator.contains})
    else:
        # if any other type return error
        return False

    # if the operation is not valid errors the testcase
    if operation not in dict_of_ops:
        raise Exception('Operator {} is not supported'.format(operation))

    return dict_of_ops[operation](result, value)


def _get_exclude(command, device):
    exclude = None
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
