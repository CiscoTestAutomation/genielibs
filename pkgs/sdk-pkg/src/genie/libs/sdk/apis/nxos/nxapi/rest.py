import logging
import json
import copy

# Logger
log = logging.getLogger(__name__)

def nxapi_method_nxapi_rest(device, action, commands='', input_type='cli',
                            dn='/api/mo/sys.json', rest_method='POST',
                            timeout=30, alias='cli', expected_return_code=None):
    """ NX-API Method: NXAPI-REST (DME)

        Args:
            device (obj): Device to run on

            action (str): One of these actions:
                - convert, convert-with-dn, convert-for-replace, send

            commands (str): The input (CLI commands, models, etc)

            # For convert action
            input_type (str): Specify input type:
                - cli, model

            # For send action
            dn (str): endpoint for any send actions
            rest_method (str): POST, GET, etc...

            # Optional
            timeout (int): timeout for rest call

            # Optional if this is the only connection defined
            alias (str): The alias for the nxapi connection

            # Optional
            expected_return_code (str): used for negative testing.
    """
    try:
        rest = getattr(device, alias)
    except AttributeError as e:
        raise Exception("'{dev}' does not have a connection with the "
                        "alias '{alias}'"
                        .format(dev=device.name, alias=alias)) from e

    # To make comparisons easy
    action = action.lower().replace("-", "_")
    input_type = input_type.lower()
    rest_method = rest_method.lower()

    convert_option_mapper = {
        'convert': 'default',
        'convert_with_dn': 'with-dn',
        'convert_for_replace': 'for-cr'
    }

    if action in convert_option_mapper:
        # overriding user input as the convert
        # actions are all post methods only
        rest_method = 'post'
        # overriding user input as all convert
        # actions get sent to /ins
        dn='/ins'

        if input_type == 'cli':
            method = 'cli_rest'
        elif input_type == 'model':
            # the api requires this format
            commands = [json.dumps('/api/mo/sys.json\n' + commands).strip('"')]
            method = 'rest_cli'
        else:
            raise Exception("'{input_type}' is an invalid input type"
                            .format(input_type=input_type))

        # build the payload
        payload = _nxapi_payload_builder(
            commands=commands,
            payload_format='json_rpc',
            method=method,
            option=convert_option_mapper[action]
        )
    elif action == 'send':
        payload = commands
    else:
        raise Exception("'{action}' is an invalid action for NXAPI-REST "
                        "(DME)".format(action=action))

    kwargs = {
        'dn': dn,
        'timeout': timeout,
        'headers': {'Content-Type': 'application/json-rpc'}
    }

    if rest_method == 'post':
        kwargs.update({'payload': payload})

    if expected_return_code:
        kwargs.update({'expected_return_code': expected_return_code})

    # send rest request
    try:
        output = getattr(rest, rest_method)(**kwargs)
    except AttributeError as e:
        raise Exception("The rest_method '{rest_method}' does not exist "
                        "in the connector with the alias '{alias}'."
                        .format(rest_method=rest_method,
                                alias=alias)) from e

    # Return as is if the method is get
    if rest_method == 'get':
        return output

    # if a convert action we need to do what the gui does
    if action in convert_option_mapper:
        # from the response get the dictionary with a result
        if isinstance(output, list):
            output = output[-1]

        output = output.get('result', {}).get('msg')

        # The nxapi returns this at the end of the message.
        # But the GUI strips it - So it gets stripped here too
        if output:
            output = output.replace("===ERROR===", "")

    # returning the message rather than the entire payload because
    # this is what the gui does
    return output

def nxapi_method_nxapi_cli(device, action, commands, message_format='json_rpc',
              command_type='cli', error_action=None, chunk=False,
              sid='sid', timeout=30, alias='cli', expected_return_code=None):
    """ NX-API Method: NXAPI-CLI

        Args:
            device (obj): Device to run on

            action (str): One of these actions:
                - output_schema, send

            commands (str): The input (CLI commands, models, etc)

            message_format (str): Format of the message:
                - json_rpc, json, xml

            command_type (str): Type of command:
                - cli, cli_ascii, cli_array, cli_show, cli_show_ascii,
                  cli_conf, bash

            # Optional depending on above arguments
            error_action (str): Action to take if error:
                - stop_on_error, continue_on_error, rollback_on_error
            chunk (bool): True to chunk output else False
            sid (str): SID from previous chunk to get the next chunk

            # Optional
            timeout (int): timeout for rest call

            # Optional if this is the only connection defined
            alias (str): The alias for the nxapi connection

            # Optional
            expected_return_code (str): used for negative testing.
    """
    try:
        rest = getattr(device, alias)
    except AttributeError as e:
        raise Exception("'{dev}' does not have a connection with the "
                        "alias '{alias}'"
                        .format(dev=device.name, alias=alias)) from e

    # To make comparisons easy
    action = action.lower().replace('-', '_')
    message_format = message_format.lower().replace('-', '_')
    command_type = command_type.lower().replace('-', '_')
    if error_action:
        error_action = error_action.lower().replace('-', '_')

    # output_schema action uses the exact same payload as the
    # json-rpc message format
    if message_format == 'json_rpc' or action == 'output_schema':
        headers = {'Content-Type': 'application/json-rpc'}

        # this isn't an option in the gui but
        # needs to be set for output_schema
        # so we set it for the user
        if action == 'output_schema':
            command_type = 'cli_schema'

    elif message_format == 'xml':
        headers = {'Content-Type': 'application/xml'}

    elif message_format == 'json':
        headers = {'Content-Type': 'application/json'}
    else:
        raise Exception("'{message_format}' is and invalid message_format"
                        .format(message_format=message_format))

    payload = _nxapi_payload_builder(
        commands=commands,
        payload_format=message_format,
        method=command_type,
        error_action=error_action,
        chunk=chunk,
        sid=sid)

    try:
        return rest.post(
            dn='/ins',
            payload=payload,
            timeout=timeout,
            headers=headers,
            expected_return_code=expected_return_code
        )
    except AttributeError as e:
        raise Exception("The rest_method 'post' does not exist "
                        "in the connector with the alias '{alias}'."
                        .format(alias=alias)) from e

def nxapi_method_restconf(device, action, commands,
                          dn='restconf/data/Cisco-NX-OS-device:System/',
                          message_format='json', rest_method='POST',
                          timeout=30, alias='cli', expected_return_code=None):
    """ NX-API Method: NXAPI-CLI

        Args:
            device (obj): Device to run on

            action (str): One of these actions:
                - send, convert

            commands (str): The input (CLI commands, models, etc)

            message_format (str): Format of the message:
                - json, xml

            # For send action
            dn (str): endpoint for any send actions
            rest_method (str): POST, GET, etc...

            # Optional
            timeout (int): timeout for rest call

            # Optional if this is the only connection defined
            alias (str): The alias for the nxapi connection

            # Optional
            expected_return_code (str): used for negative testing.
    """
    try:
        rest = getattr(device, alias)
    except AttributeError as e:
        raise Exception("'{dev}' does not have a connection with the "
                        "alias '{alias}'"
                        .format(dev=device.name, alias=alias)) from e

    if action == 'convert':
        if message_format == 'json':
            method = 'cli_yang_json'
        elif message_format == 'xml':
            method = 'cli_yang_xml'
        else:
            raise Exception("'{message_format}' is an invalid message_format"
                            .format(message_format=message_format))

        # overriding user input as all convert
        # actions get sent to /ins
        dn = '/ins'

        headers={'Content-Type': 'application/json-rpc'}

        payload = _nxapi_payload_builder(
            commands=commands,
            payload_format='json_rpc',
            method=method)

    elif action == 'send':
        if message_format == 'json':
            headers = {'Content-Type': 'application/yang.data+json'}
        elif message_format == 'xml':
            headers = {'Content-Type': 'application/yang.data+xml'}
        else:
            raise Exception("'{message_format}' is an invalid message_format"
                            .format(message_format=message_format))

        payload=commands
    else:
        raise Exception("'{action}' is an invalid action for RESTCONF (Yang)"
                        .format(action=action))

    rest_kwargs = {
        'dn': dn,
        'timeout': timeout,
        'headers': headers,
        'expected_return_code': expected_return_code
    }

    if rest_method.lower() != 'delete':
        rest_kwargs.update({'payload': payload})

    try:
        output = getattr(rest, rest_method.lower())(**rest_kwargs)
    except AttributeError as e:
        raise Exception("The rest_method '{rest_method}' does not exist "
                        "in the connector with the alias '{alias}'."
                        .format(rest_method=rest_method,
                                alias=alias)) from e

    # if a convert action we need to do what the gui does
    if action == 'convert':
        # from the response get the dictionary with a result
        if isinstance(output, list):
            for item in output:
                result = item.get('result')
                if not result:
                    continue
                output = item
                break

        output = output.get('result', {}).get('msg')

        # The GUI strips the 'system' in the hierarchy
        # so we do it here too
        lines = output.splitlines(keepends=True)
        if message_format == 'json':
            # system is the second line and second last line
            del lines[1]
            del lines [-2]
        elif message_format == 'xml':
            # system is the first line and last line
            del lines[0]
            del lines [-1]

        output = ''.join(lines)

    return output

def _nxapi_payload_builder(
        commands, payload_format, method, error_action=None,
        chunk=None, sid=None, option=None
):
    """ Not meant to be called directly.

        Builds the specified type of payload for nxapi calls

    Args:
        commands (str): commands to add to payload
        payload_format (str): type of payload to build
        method (str): method to add to payload
        error_action (str): error action to add to payload
        chunk (bool): chunk to add to payload
        sid (str): sid to add to payload
        option (str): option to add to payload

    returns:
        payload

    """

    error_action_mapper = {
        'stop_on_error': 'stop-on-error',
        'continue_on_error': 'continue-on-error',
        'rollback_on_error': 'rollback-on-error'
    }

    if method != 'rest_cli':
        commands = [line.strip() for line in commands.splitlines() if line]

    if payload_format == 'json_rpc':
        payload = []
        for index, command in enumerate(commands):
            temp = {
                "jsonrpc": "2.0",
                "method": method,
                "params": {
                    "cmd": command,
                    "version": 1
                },
                "id": index + 1
            }
            if option:
                temp.update({'option': option})

            if error_action:
                temp.update({'rollback': error_action_mapper[error_action]})

            payload.append(temp)
        payload = json.dumps(payload)

    elif payload_format in ['json', 'xml']:
        command = ""
        for line in commands:
            command += line + ' ;'

        # remove last ' ;'
        command = command[:-2]

        if payload_format == 'json':
            # build payload
            payload = {
                "ins_api": {
                    "version": "1.0",
                    "type": method,
                    "chunk": "1" if chunk else "0",
                    "sid": sid,
                    "input": command,
                    "output_format": "json"
                }
            }

            if error_action:
                payload['ins_api'].update(
                    {'rollback': error_action_mapper[error_action]}
                )

            payload = json.dumps(payload)

        elif payload_format == 'xml':
            command = ""
            for line in commands:
                command += line + ' ;'

            # remove last ' ;'
            command = command[:-2]

            # First line must be directly after """
            payload = """<?xml version="1.0"?>
            <ins_api>
              <version>1.0</version>
              <type>{type}</type>
              <chunk>{chunk}</chunk>
              <sid>{sid}</sid>
              <input>{input}</input>
              <output_format>xml</output_format>
            </ins_api>
            """.format(type=method,
                       chunk="1" if chunk else "0",
                       sid=sid,
                       input=command)

    return payload