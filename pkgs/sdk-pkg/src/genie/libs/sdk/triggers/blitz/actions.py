import os
import json
import time
import logging
from datetime import datetime
from threading import Thread

# from pyats
from pyats.easypy import runtime
from pyats.log.utils import banner
from pyats.reporter.server import LogLineCounter

# from genie
from genie.libs import sdk
from genie.utils.diff import Diff
from genie.ops.utils import get_ops_exclude
from genie.harness.standalone import run_genie_sdk

from pkg_resources import get_distribution
from .maple import maple, maple_search
from .yangexec import run_netconf, run_gnmi, run_restconf
from .actions_helper import (configure_handler, api_handler, learn_handler,
                             parse_handler, execute_handler, _get_exclude,
                             _condition_validator, rest_handler,
                             bash_console_handler, dialog_handler,
                             yang_handler,)
from .yang_snapshot import YangSnapshot

# skip in case pyats.contrib is not installed
try:
    import requests
    from requests_toolbelt.multipart.encoder import MultipartEncoder
except Exception:
    pass

log = logging.getLogger(__name__)


# decorator for pyATS Health Check
# result with data will be added to pyATS extra field
def add_result_as_extra(func):
    def wrapper(*args, **kwargs):
        # adding extra is done only when it's pyATS health
        if kwargs['self'].__class__.__name__ == 'Health':
            health_data = {}

            section = kwargs['section']

            # starttime
            starttime = datetime.now()

            # execute action for Health class
            action_output = func(*args, **kwargs)

            # get section info
            section_info = section.reporter.client.get_section()

            # if no output from blitz action, no point to execute
            # for health_data and extra
            if action_output:
                # set attributes for health_data
                fullid = section_info['fullid']
                jobid = runtime.job.uid
                # in case common api, device doesn't exist
                if 'device' in kwargs:
                    device_name = kwargs['device'].name
                else:
                    device_name = ''
                testbed_name = runtime.testbed.name
                health_name = kwargs['name']
                stoptime = datetime.now()
                health_type = 'processor'
                # if health dedicated APIs, will get from action_output['health_data']
                # if not, just grab return from API
                if isinstance(action_output,
                              dict) and 'health_data' in action_output:
                    health_output = action_output['health_data']
                else:
                    health_output = action_output
                logs_logfile = section_info['logs']['file']
                logs_begin = section_info['logs']['begin']
                logs_begin_lines = section_info['logs']['begin_lines']

                # build health_data
                # at this point, size/size_lines are not available
                # because we might show debug logging after
                health_data = {
                    'fullid': fullid,
                    'jobid': jobid,
                    'testbed': testbed_name,
                    'device': device_name,
                    'health_name': health_name,
                    'starttime': starttime.isoformat(),
                    'stoptime': stoptime.isoformat(),
                    'type': health_type,
                    'health_output': health_output,
                    'logs': {
                        'file': logs_logfile,
                        'begin': logs_begin,
                        'begin_lines': logs_begin_lines,
                    }
                }

                log.debug('health_data to health_results.json:\n' +
                          json.dumps(health_data, indent=2, sort_keys=True))

                # add extra for pyATS Health Check result
                extra_action_result = {}

                health_result = kwargs['steps'].result.name

                extra_action_result = {
                    'fullid': fullid,
                    'starttime': starttime.isoformat(),
                    'stoptime': stoptime.isoformat(),
                    'health_name': health_name,
                    'type': health_type,
                    'result': health_result
                }

                # add extra to processor
                add_extra_args = {
                    "%EXTEND_LIST{health}": [extra_action_result]
                }
                section.reporter.client.add_extra(**add_extra_args)

                log.debug('extra to section:\n' +
                          json.dumps({'health': [extra_action_result]},
                                     indent=2,
                                     sort_keys=True))

                # calculating size and size_lines for logs
                # because section is not done yet
                logs_size = os.path.getsize(
                    section_info['logfile']) - logs_begin
                end_size = logs_begin + logs_size
                ctx = section.reporter.client.get_section_ctx()
                lc = LogLineCounter(ctx.logfile)
                logs_end_lines = lc._get_lines(end_size)
                logs_size_lines = logs_end_lines - logs_begin_lines
                lc.close()

                # update health_data with latest size and size_lines
                # need to update latest size after having debug message
                health_data['logs'].update({
                    'size': logs_size,
                    'size_lines': logs_size_lines,
                })
                # added health_result to health_data
                health_data.update({'result': health_result})

                # add health_data to runtime.health_results
                if health_data:
                    all_health_data = runtime.health_results['health_data']
                    all_health_data.append(health_data)
                    runtime.health_results['health_data'] = all_health_data

                # send webex notification in case not passed or passx
                if (runtime.args.health_notify_webex or
                        runtime.args.health_webex) and health_result not in [
                            'passed', 'passx'
                        ]:
                    # get pid
                    pid = os.getpid()
                    # assume as forked process and build filename
                    forked_logname = section_info['logfile']+':pid-'+str(pid)
                    # check if forked log filename exist or not
                    if os.path.isfile(forked_logname):
                        logfile = forked_logname
                    else:
                        logfile = section_info['logfile']

                    health_value = None
                    # save variable to use saved variable 'health_value' in webex notification template
                    if 'save' in kwargs:
                        updated_ret_dict = kwargs[
                            'self']._filter_and_save_action_output(
                                section, kwargs['ret_dict'], kwargs['save'],
                                action_output)
                        health_value = updated_ret_dict['saved_vars'].get(
                            'health_value', None)
                    # no save variable is configured in YAML
                    else:
                        health_value = 'N/A. No save_variable `health_value` in pyATS Health yaml'

                    # get information for webex notification template
                    host = runtime.env.host.name
                    host_os = runtime.env.host.distro
                    python_env = runtime.env.prefix
                    python_ver = runtime.env.python.version
                    try:
                        pyats_ver = get_distribution('ats').version
                    except Exception:
                        pyats_ver = get_distribution('pyats').version
                    # Build payload
                    # Device        : {device_name}
                    # Health Name   : {health_name}
                    # Health Type   : {health_type}
                    # Health Result : {health_result}
                    # Health Value  : {health_value}

                    # Job ID        : {jobid}
                    # Host          : {host} ({host_os})
                    # Python Env    : {python_env} / pyATS {pyats_ver} / Python {python_ver}
                    # Full-ID       : {fullid}
                    # Testbed       : {testbed_name}
                    # Start Time    : {starttime}
                    # Stop Time     : {stoptime}

                    # build payload for webex notification template
                    payload = {
                        'markdown':
                        runtime.health_webex['msg'].format(
                            device_name=device_name,
                            health_name=health_name,
                            health_type=health_type,
                            health_result=health_result,
                            health_value=health_value,
                            jobid=jobid,
                            host=host,
                            host_os=host_os,
                            python_env=python_env,
                            pyats_ver=pyats_ver,
                            python_ver=python_ver,
                            fullid=fullid,
                            testbed_name=testbed_name,
                            starttime=starttime,
                            stoptime=stoptime)
                    }


                    # set destination space or person
                    if runtime.health_webex['space']:
                        payload['roomId'] = runtime.health_webex['space']
                    elif runtime.health_webex['email']:
                        payload['toPersonEmail'] = runtime.health_webex[
                            'email']

                    with open(logfile, 'r') as f:
                        log_content = f.read()

                    payload['files'] = (logfile, log_content, 'text/plain')
                    try:
                        multipart_data = MultipartEncoder(payload)
                    except NameError as e:
                        raise Exception("pyats.contrib package might not be installed yet. Please check and install by 'pip install pyats.contrib': {}".format(e))
                    runtime.health_webex['headers']['Content-Type'] = multipart_data.content_type
                    log.info('Sending pyATS Health Check Webex notification')
                    try:
                        # Attempt POST
                        r = requests.post(
                            runtime.health_webex['url'],
                            data=multipart_data,
                            headers=runtime.health_webex['headers'])
                        log.debug('notification status: %s' % r.status_code)
                        log.debug(r.text)
                    except Exception:
                        log.exception(
                            'Failed to send pyATS Health Check Webex notification:'
                        )

        else:
            # execute action for Blitz class
            action_output = func(*args, **kwargs)

        return action_output

    return wrapper


@add_result_as_extra
def configure(self,
              device,
              steps,
              section,
              name,
              command,
              alias=None,
              connection_alias=None,
              result_status=None,
              expected_failure=False,
              continue_=True,
              processor='',
              health_uids=None,
              health_groups=None,
              health_sections=None,
              **kwargs):

    if 'ret_dict' in kwargs:
        kwargs.pop('ret_dict')

    # checking if custom msg else default msg will be written
    msg = kwargs.pop('custom_substep_message',
                     "Configuring '{device}'".format(device=device.name))

    # default output set to none in case of an exception
    output = None
    with steps.start(msg, continue_=continue_) as step:

        kwargs.update({'step': step,
                       'device': device,
                       'command': command,
                       'connection_alias': connection_alias,
                       'result_status': result_status,
                       'expected_failure': expected_failure})

        output = configure_handler(**kwargs)

    return output

# saved ON_CHANGE subscriptions waiting for change to happen
active_subscriptions = {}

@add_result_as_extra
def check_yang_subscribe(self,
                         steps,
                         device,
                         **kwargs):
    """Look for subscribe, wait for subscribe thread to stop, return result."""

    subscribe_thread = None
    hostname = None
    del_from_active = False
    if hasattr(device, 'name'):
        hostname = device.name
    elif hasattr(device, 'device') and hasattr(device.device, 'name'):
        hostname = device.device.name
    if hostname is None:
        # how did we get this far?
        log.error('YANG Subscribe check, cannot find hostname')
        return

    if hostname in active_subscriptions:
        log.info(f"Request being sent:\n{active_subscriptions[hostname].request}")
        del_from_active = True
        # ON_CHANGE thread waiting for change
        subscribe_thread = active_subscriptions[hostname]
        if subscribe_thread.stopped():
            log.info('ON_CHANGE subscribe terminated...')
            subscribe_thread.stop()
            del active_subscriptions[hostname]
            return

    if subscribe_thread is not None:
        # Wait for subscribe thread to finish and return result.
        while not subscribe_thread.stopped():
            log.info('Waiting for notification...')
            time.sleep(1)
        # set subscribe result
        if not subscribe_thread.result:
            steps.failed('subscription failed')
        if del_from_active:
            del active_subscriptions[hostname]

@add_result_as_extra
def configure_dual(self,
                   device,
                   steps,
                   section,
                   name,
                   command,
                   alias=None,
                   expected_failure=False,
                   continue_=True,
                   processor='',
                   result_status=None,
                   health_uids=None,
                   health_groups=None,
                   health_sections=None,
                   **kwargs):

    if 'ret_dict' in kwargs:
        kwargs.pop('ret_dict')

    # checking if custom msg else default msg will be written
    msg = kwargs.pop(
        'custom_substep_message',
        "Configuring '{device}' in (config-dual-stage) prompt".format(
            device=device.name))

    # default output set to none in case of an exception
    output = None
    with steps.start(msg, continue_=continue_) as step:

        kwargs.update({'step': step,
                       'device': device,
                       'command': command,
                       'action': 'configure_dual',
                       'result_status': result_status,
                       'expected_failure': expected_failure})

        output = configure_handler(**kwargs)

    return output


@add_result_as_extra
def parse(self,
          device,
          steps,
          section,
          name,
          command,
          expected_failure=False,
          connection_alias=None,
          alias=None,
          context=None,
          include=None,
          exclude=None,
          result_status=None,
          max_time=None,
          check_interval=None,
          continue_=True,
          processor='',
          health_uids=None,
          health_groups=None,
          health_sections=None,
          *args,
          **kwargs):

    if 'ret_dict' in kwargs:
        kwargs.pop('ret_dict')

    # checking if custom msg else default msg will be written
    msg = kwargs.pop('custom_substep_message',
                     "Parsing '{c}' on '{d}'".format(c=command, d=device.name))
    context = kwargs.pop('context', None)

    # action parse
    output = {}
    with steps.start(msg, continue_=continue_) as step:

        arguments = kwargs.get('arguments', None)
        handler_kwargs = {'step': step,
                          'device': device,
                          'command': command,
                          'context': context,
                          'alias': alias,
                          'connection_alias': connection_alias,
                          'include': include,
                          'exclude': exclude,
                          'result_status': result_status,
                          'max_time': max_time,
                          'check_interval': check_interval,
                          'continue_': continue_,
                          'expected_failure': expected_failure,
                          'arguments': arguments,
                          'custom_verification_message': kwargs.pop('custom_verification_message', None)}

        output = parse_handler(**handler_kwargs)

    return output


@add_result_as_extra
def execute(self,
            device,
            steps,
            section,
            name,
            command,
            expected_failure=False,
            alias=None,
            connection_alias=None,
            include=None,
            exclude=None,
            result_status=None,
            max_time=None,
            check_interval=None,
            continue_=True,
            processor='',
            health_uids=None,
            health_groups=None,
            health_sections=None,
            **kwargs):

    if 'ret_dict' in kwargs:
        kwargs.pop('ret_dict')

    # checking if custom msg else default msg will be written
    msg = kwargs.pop(
        'custom_substep_message',
        "Executing '{c}' on '{d}'".format(c=command, d=device.name))

    # action execute
    output = None
    with steps.start(msg, continue_=continue_) as step:

        kwargs.update({
            'step': step,
            'device': device,
            'command': command,
            'connection_alias': connection_alias,
            'include': include,
            'exclude': exclude,
            'result_status': result_status,
            'max_time': max_time,
            'check_interval': check_interval,
            'continue_': continue_,
            'expected_failure': expected_failure
        })

        output = execute_handler(**kwargs)

    return output


@add_result_as_extra
def api(self,
        steps,
        section,
        name,
        function,
        device=None,
        expected_failure=False,
        arguments=None,
        include=None,
        exclude=None,
        result_status=None,
        max_time=None,
        check_interval=None,
        continue_=True,
        processor='',
        health_uids=None,
        health_groups=None,
        health_sections=None,
        alias=None,
        **kwargs):

    if 'ret_dict' in kwargs:
        kwargs.pop('ret_dict')

    # action api
    output = None

    if not device:
        default_msg = "Calling API {f}".format(f=function)
    else:
        default_msg = "Calling API '{f}' on '{d}'".format(f=function,
                                                          d=device.name)

    msg = kwargs.pop('custom_substep_message', default_msg)

    # check if the step logs needs to be suppressed
    suppress_logs = bool(self.parameters.get('suppress_logs'))

    with steps.start(msg, continue_=continue_, suppress_logs=suppress_logs) as step:

        kwargs.update({'step': step,
                       'device': device,
                       'command': function,
                       'include': include,
                       'exclude': exclude,
                       'result_status': result_status,
                       'max_time': max_time,
                       'check_interval': check_interval,
                       'continue_': continue_,
                       'arguments': arguments,
                       'expected_failure': expected_failure,
                       'blitz_obj': self})

        output = api_handler(**kwargs)

    log.debug('api return value: {o}'.format(o=output))
    return output


@add_result_as_extra
def learn(self,
          device,
          steps,
          section,
          name,
          feature,
          alias=None,
          include=None,
          exclude=None,
          result_status=None,
          max_time=None,
          check_interval=None,
          expected_failure=False,
          continue_=True,
          processor='',
          health_uids=None,
          health_groups=None,
          health_sections=None,
          **kwargs):

    if 'ret_dict' in kwargs:
        kwargs.pop('ret_dict')

    msg = kwargs.pop(
        'custom_substep_message',
        "Learning '{f}' on '{d}'".format(f=feature, d=device.name))
    # action learn
    output = None
    with steps.start(msg, continue_=continue_) as step:

        kwargs.update({'step': step,
                        'device': device,
                        'command': feature,
                        'include': include,
                        'exclude': exclude,
                        'result_status': result_status,
                        'max_time': max_time,
                        'check_interval': check_interval,
                        'continue_': continue_,
                        'expected_failure': expected_failure})

        output = learn_handler(**kwargs)

    return output


@add_result_as_extra
def compare(self,
            steps,
            section,
            name,
            items,
            continue_=True,
            alias=None,
            result_status=None,
            processor='',
            health_uids=None,
            health_groups=None,
            health_sections=None,
            **kwargs):

    if 'ret_dict' in kwargs:
        kwargs.pop('ret_dict')

    # action compare
    if not items:

        steps.failed('No item is provided for comparision')

    msg = kwargs.pop('custom_substep_message', None)

    for comp_item in items:

        if not msg:
            msg = "Verifying the following comparison request {}"\
                    .format(comp_item)

        with steps.start(msg, continue_=continue_) as step:

            condition = _condition_validator(comp_item)
            result = 'passed' if condition else 'failed'
            getattr(step, result)(
                'The following arithmetic statement {} is {}'.format(
                    comp_item, condition))


    # steps.result will only change to result_status if it is passed.
    if result_status and steps.result.name == "passed":
        result_status_message = 'The compare result status is changed from passed to {}' \
                                ' based on the result_status'.format(result_status)
        log.warning('The compare result status is changed from passed to {}' \
                    ' based on the result_status'.format(result_status))
        getattr(steps, result_status)(result_status_message)


@add_result_as_extra
def sleep(self,
          steps,
          section,
          name,
          sleep_time,
          continue_=True,
          processor='',
          health_uids=None,
          health_groups=None,
          health_sections=None,
          result_status=None,
          *args,
          **kwargs):

    if 'ret_dict' in kwargs:
        kwargs.pop('ret_dict')

    log.info('Sleeping for {s} seconds'.format(s=sleep_time))
    time.sleep(float(sleep_time))

    # steps.result will only change to result_status if it is passed.
    if result_status and steps.result.name=="passed":
        result_status_message = 'The sleep result status is changed from passed to {}' \
                                ' based on the result_status'.format(result_status)
        log.warning('The sleep result status is changed from passed to {}' \
                    ' based on the result_status'.format(result_status))
        getattr(steps, result_status)(result_status_message)


@add_result_as_extra
def rest(self,
         device,
         method,
         steps,
         section,
         name,
         expected_failure=False,
         continue_=True,
         include=None,
         exclude=None,
         result_status=None,
         max_time=None,
         check_interval=None,
         connection_alias='rest',
         processor='',
         health_uids=None,
         health_groups=None,
         health_sections=None,
         *args,
         **kwargs):

    if 'ret_dict' in kwargs:
        kwargs.pop('ret_dict')

    msg = kwargs.pop('custom_substep_message',
                     "Submitting a '{m}' call to a REST API on '{d}'".\
                     format(m=method, d=device.name))

    # action rest
    output = None
    with steps.start(msg, continue_=continue_) as step:

        kwargs.update({'device': device,
                       'method': method,
                       'step': step,
                       'expected_failure':expected_failure,
                       'continue_':continue_,
                       'include':include,
                       'exclude':exclude,
                       'result_status':result_status,
                       'max_time':max_time,
                       'check_interval':check_interval,
                       'connection_alias':connection_alias})

        output = rest_handler(**kwargs)

    return output


@add_result_as_extra
def yang(self,
         device,
         steps,
         section,
         name,
         protocol,
         datastore,
         content,
         operation,
         continue_=True,
         connection=None,
         returns=None,
         result_status=None,
         alias=None,
         processor='',
         health_uids=None,
         health_groups=None,
         health_sections=None,
         include=None,
         exclude=None,
         max_time=None,
         check_interval=None,
         *args,
         **kwargs):

    if 'ret_dict' in kwargs:
        kwargs.pop('ret_dict')

    # Register yang action so that related Xpaths are collected.
    if hasattr(self.parent, 'yang_snapshot'):
        self.parent.yang_snapshot.register(
            device, connection, protocol, operation, content)

    if connection:
        device = getattr(device, connection)
        # Verify that we are connected
        # TODO
        # I think all our connection implementation (unicon, rest, yang)
        # should have an isconnected which does an action on the device, example show
        # clock for cli, to verify.  Right now, we don't have this, we have
        # connected but we all know its of no use.
    if returns is None:
        returns = {}

    # hostname check
    hostname = None
    if hasattr(device, 'name'):
        hostname = device.name
    elif hasattr(device, 'device') and hasattr(device.device, 'name'):
        hostname = device.device.name
    if hostname is None:
        # how did we get this far?
        log.error('YANG action cannot find hostname')
        return

    # Valid protocols mapped to their respective run functions
    protocols = {
        'netconf': run_netconf,
        'gnmi': run_gnmi,
        'restconf': run_restconf
    }


    if protocol in protocols:
        result = protocols[protocol](operation=operation,
                                     device=device,
                                     steps=steps,
                                     datastore=datastore,
                                     rpc_data=content,
                                     returns=returns,
                                     **kwargs)

        msg = kwargs.pop('custom_substep_message',
                     "Submitting a '{m}' call".\
                     format(m=protocol))

        with steps.start(msg, continue_=continue_) as step:

            handler_kwargs = {
                'step': step,
                'device': device,
                'protocol': protocol,
                'alias': alias,
                'include': include,
                'exclude': exclude,
                'max_time': max_time,
                'check_interval': check_interval,
                'continue_': continue_,
                'output': result
                }

            result = yang_handler(**handler_kwargs)

            if isinstance(result, Thread):
                # If the sub_mode is on_change then the yang result is updated to active subscriptions
                if result.sub_mode == 'ON_CHANGE':
                    log.warning(f'Updating active subscriptions for the device {hostname}')
                    active_subscriptions[hostname] = result
                    log.info(f"Waiting notifications for request sent:\n{active_subscriptions[hostname].request}")
                    return
    else:
        result = None

    if not result:
        steps.failed('Yang action has failed')

    # steps.result will only change to result_status if it is passed.
    if result_status and steps.result.name == "passed":
        result_status_message = 'The yang result status is changed from passed to {}' \
                                ' based on the result_status'.format(result_status)
        log.warning('The yang result status is changed from passed to {}' \
                    ' based on the result_status'.format(result_status))
        getattr(steps, result_status)(result_status_message)

    return result


@add_result_as_extra
def configure_replace(self,
                      device,
                      steps,
                      section,
                      name,
                      config,
                      continue_=True,
                      alias=None,
                      result_status=None,
                      iteration=2,
                      interval=30,
                      processor='',
                      health_uids=None,
                      health_groups=None,
                      health_sections=None,
                      timeout=60,
                      **kwargs):

    if 'ret_dict' in kwargs:
        kwargs.pop('ret_dict')

    restore = sdk.libs.abstracted_libs.restore.Restore(device=device)

    # lib.to_url is normally saved via restore.save_configuration()
    # but since we only want the os abstraction and we are providing
    # a config - Just set the to_url equal to the config path provided
    restore.lib.to_url = config

    restore.restore_configuration(
        device=device,
        abstract=None,
        method='config_replace',
        iteration=iteration,
        interval=interval,
        delete_after_restore=False,
        timeout=timeout
    )
    # steps.result will only change to result_status if it is passed.
    if result_status and steps.result.name == "passed":
        result_status_message = 'The configure_replace result status is changed from ' \
                                'passed to {}' \
                                ' based on the result_status'.format(result_status)
        log.warning('The configure_replace result status is changed from passed to {}' \
                    ' based on the result_status'.format(result_status))
        getattr(steps, result_status)(result_status_message)


@add_result_as_extra
def save_config_snapshot(self,
                         device,
                         steps,
                         section,
                         name,
                         alias=None,
                         result_status=None,
                         continue_=True,
                         processor='',
                         health_uids=None,
                         health_groups=None,
                         health_sections=None,
                         timeout=60,
                         **kwargs):

    if 'ret_dict' in kwargs:
        kwargs.pop('ret_dict')

    # setup restore object for device
    if not hasattr(self, 'restore'):
        self.restore = {}
    if device not in self.restore:
        self.restore[device] = sdk.libs.abstracted_libs.restore.Restore(
            device=device)

    # Get default directory
    save_dir = getattr(self.parent, 'default_file_system')
    if not save_dir:
        self.parent.default_file_system = {}

    # learn default directory
    if device.name not in save_dir:
        self.parent.default_file_system.update({
            device.name: self.restore[device].abstract.sdk.libs.abstracted_libs.\
                subsection.get_default_dir(device=device)})

    self.restore[device].save_configuration(
        device=device,
        abstract=None,
        method='config_replace',
        default_dir=self.parent.default_file_system,
        timeout=timeout)

    # To keep track of snapshots (whether they are deleted or not)
    self.restore[device].snapshot_deleted = False

    # steps.result will only change to result_status if it is passed.
    if result_status and steps.result.name == "passed":
        result_status_message = 'The save_config_snapshot result status is changed ' \
                                'from passed to {}' \
                                ' based on the result_status'.format(result_status)
        log.warning('The save_config_snapshot result status is changed from passed to {}' \
                    ' based on the result_status'.format(result_status))
        getattr(steps, result_status)(result_status_message)


@add_result_as_extra
def restore_config_snapshot(self,
                            device,
                            steps,
                            section,
                            name,
                            continue_=True,
                            delete_snapshot=True,
                            alias=None,
                            result_status=None,
                            processor='',
                            health_uids=None,
                            health_groups=None,
                            health_sections=None,
                            timeout=60,
                            **kwargs):
    if 'ret_dict' in kwargs:
        kwargs.pop('ret_dict')

    if not hasattr(self, 'restore') or device not in self.restore:
        steps.errored("Must use action 'save_config_snapshot' first.\n\n")

    # If the snapshot file was deleted - error
    if self.restore[device].snapshot_deleted:
        steps.errored(
            "If you want to restore with the same snapshot "
            "multiple times then you must pass 'delete_snapshot=False' "
            "to previous uses of this action. Otherwise the "
            "snapshot will be deleted on the first usage.")

    try:
        self.restore[device].restore_configuration(
            device=device,
            abstract=None,
            method='config_replace',
            delete_after_restore=delete_snapshot,
            timeout=timeout)
    except Exception as e:
        steps.failed(str(e))

    # To keep track of snapshots (whether they are deleted or not)
    if delete_snapshot:
        self.restore[device].snapshot_deleted = True

    # steps.result will only change to result_status if it is passed.
    if result_status and steps.result.name == "passed":
        result_status_message = 'The restore_config_snapshot result status is changed ' \
                                'from passed to {}' \
                                ' based on the result_status'.format(result_status)
        log.warning('The restore_config_snapshot result status is changed from passed to {}' \
                    ' based on the result_status'.format(result_status))
        getattr(steps, result_status)(result_status_message)


@add_result_as_extra
def bash_console(self,
                 device,
                 steps,
                 section,
                 name,
                 commands,
                 expected_failure=False,
                 include=None,
                 exclude=None,
                 result_status=None,
                 max_time=None,
                 check_interval=None,
                 continue_=True,
                 alias=None,
                 processor='',
                 health_uids=None,
                 health_groups=None,
                 health_sections=None,
                 **kwargs):

    # action bash_console
    output = None

    if 'ret_dict' in kwargs:
        kwargs.pop('ret_dict')

    with steps.start("Executing bash commands on '{d}'".\
                    format(d=device.name), continue_=continue_) as step:

        kwargs.update({'step': step,
                       'device': device,
                       'commands': commands,
                       'include': include,
                       'exclude': exclude,
                       'result_status': result_status,
                       'max_time': max_time,
                       'check_interval': check_interval,
                       'continue_': continue_,
                       'expected_failure': expected_failure})

        output = bash_console_handler(**kwargs)

    return output


@add_result_as_extra
def genie_sdk(self,
              steps,
              section,
              name,
              continue_=True,
              result_status=None,
              processor='',
              health_uids=None,
              health_groups=None,
              health_sections=None,
              **kwargs):

    if 'ret_dict' in kwargs:
        kwargs.pop('ret_dict')

    # This is to remove the uut dependency of genie standalone.
    # Since the device we are running the sdk on is in the
    # kwargs we just pass the first device found as the 'uut'
    uut = 'uut'
    for _, params in kwargs.items():
        uut = params.get('devices', ['uut'])[0]
        break

    sdks = list(kwargs.keys())
    run_genie_sdk(self, steps, sdks, uut=uut, parameters=kwargs)

    # steps.result will only change to result_status if it is passed.
    if result_status and steps.result.name == "passed":
        result_status_message = 'The genie_sdk result status is changed ' \
                                'from passed to {}' \
                                ' based on the result_status'.format(result_status)
        log.warning('The genie_sdk result status is changed from passed to {}' \
                    ' based on the result_status'.format(result_status))
        getattr(steps, result_status)(result_status_message)


@add_result_as_extra
def print_(self,
          steps,
          section,
          name,
          continue_=True,
          processor='',
          result_status=None,
          health_uids=None,
          health_groups=None,
          health_sections=None,
          *args,
          **kwargs):

    if 'steps' in kwargs:
        kwargs.pop('steps')

    for key, value in kwargs.items():
        if key not in ['ret_dict']:
            if value.get('type') == 'banner':

                print_value = 'printing message: {k}\n{v}'.format(
                    k=key, v=banner(str(value['value'])))
            else:
                print_value = 'The value of {k}: {v}'.format(k=key,
                                                             v=value['value'])

            log.info(print_value)

    # steps.result will only change to result_status if it is passed.
    if result_status and steps.result.name == "passed":
        result_status_message = 'The print result status is changed ' \
                                'from passed to {}' \
                                ' based on the result_status'.format(result_status)
        log.warning('The print result status is changed from passed to {}' \
                    ' based on the result_status'.format(result_status))
        getattr(steps, result_status)(result_status_message)


@add_result_as_extra
def diff(self,
         steps,
         section,
         name,
         device,
         pre,
         post,
         alias=None,
         continue_=True,
         fail_different=False,
         command=None,
         exclude=None,
         processor='',
         result_status=None,
         health_uids=None,
         health_groups=None,
         health_sections=None,
         feature=None,
         mode=None,
         **kwargs):

    if 'ret_dict' in kwargs:
        kwargs.pop('ret_dict')

    msg = kwargs.pop('custom_substep_message',
                     "Perform Diff for '{device}'".format(device=device.name))

    with steps.start(msg, continue_=continue_) as step:

        exclude_items = _get_exclude(command, device)
        # if feature is given, get exclude from the Ops
        if feature:
            try:
                exclude_items.extend(get_ops_exclude(feature, device))
            except LookupError:
                log.warning(
                    "No Ops for {feature} was found. Couldn't retrieve exclude list."
                    .format(feature=feature))
        # check given mode
        if mode and mode not in ['add', 'remove', 'modified']:
            log.warning(
                "Wrong mode '{mode}' was given. Ignored.".format(mode=mode))
        if exclude and isinstance(exclude, list):
            exclude_items.extend(exclude)
            log.debug('exclude: {exclude}'.format(exclude=exclude_items))

        try:
            diff = Diff(pre, post, exclude=exclude_items, mode=mode)
        except Exception as e:
            step.failed(str(e))

        diff.findDiff()
        # check content of diff
        if str(diff):
            log.info(diff)
            if fail_different:
                step.failed('{pre} and {post} are not '
                            'identical'.format(pre=pre, post=post))
        else:
            step.passed('{pre} and {post} are identical'.format(pre=pre,
                                                                post=post))
    # steps.result will only change to result_status if it is passed.
    if result_status and steps.result.name == "passed":
        result_status_message = 'The diff result status is changed ' \
                                'from passed to {}' \
                                ' based on the result_status'.format(result_status)
        log.warning('The diff result status is changed from passed to {}' \
                    ' based on the result_status'.format(result_status))
        getattr(steps, result_status)(result_status_message)

    return diff


@add_result_as_extra
def dialog(self,
           device,
           steps,
           section,
           name,
           start,
           end,
           sequence,
           alias=None,
           connection_alias=None,
           continue_=True,
           processor='',
           health_uids=None,
           health_groups=None,
           health_sections=None,
           **kwargs):
    '''
    Action to handle interactions with a dialog
    '''

    if 'ret_dict' in kwargs:
        kwargs.pop('ret_dict')

    device.sendline(start)

    # action dialog
    for sequence_item in sequence:
        msg = '{}'.format(
            sequence_item.get(
                'step_msg', 'Expect ' + sequence_item.get('expect'))
        )
        with steps.start(msg, continue_=continue_) as step:

            kwargs.update({
                'step': step,
                'device': device,
                'action': sequence_item.get('action'),
                'expect': sequence_item.get('expect'),
                'include': sequence_item.get('include'),
                'exclude': sequence_item.get('exclude'),
                'timeout': sequence_item.get('timeout', 30),
                'connection_alias': connection_alias,
                'continue_': continue_,
            })

            output = dialog_handler(**kwargs)

    device.sendline(end)
    device.state_machine.go_to('any', device.spawn,
                               context=device.context)

    return output


@add_result_as_extra
def yang_snapshot(
    self,
    device,
    steps,
    section,
    name,
    continue_=True,
    processor='',
    health_uids=None,
    health_groups=None,
    health_sections=None,
    result_status=None,
    *args,
    **kwargs,
):
    '''
    Action to collect the device config before a group of test cases. E.g.,
    when a leaf /native/ntp/peer/ipv6[host-name="genericstring"]/burst-opt is
    tested, YangSuite generates five test cases: create, delete, merge,
    replace and remove. These five test cases are in one group. After the last
    test case remove, in this example,
    /native/ntp/peer/ipv6[host-name="genericstring"] remains. This behavior is
    not desirable as its leftover config may impact other test cases in a
    negative way. The yang_snapshot action here is to start collecting config
    snapshot so that the leftover may be removed later.

    Parameters
    ----------
    self : `object`
        pyATS testcase object.

    device : `object`
        pyATS device object.

    steps : `object`
        pyATS Steps object.

    section : `object`
        pyATS Section object.

    name : `str`
        Action name.

    continue_ : `boolean`
        Whether steps should continue in case of failure.

    processor : `str`
        Processor string.

    health_uids : `object`
        UIDs of Genie Health.

    health_groups : `object`
        Groups of Genie Health.

    health_sections : `object`
        Sections of Genie Health.

    result_status : `str`
        It is allowed to change the result status to failed, passed, aborted,
        blocked, skipped, errored or passx when the step is passed. The desired
        result status can be specified here.

    Returns
    -------
    boolean
        Return True when the yang_snapshot action was successful, and False
        otherwise.
    '''

    # Attribute yang_snapshot holds a YangSnapshot object, which contains
    # related snapshot info.
    if not hasattr(self.parent, 'yang_snapshot'):
        self.parent.yang_snapshot = YangSnapshot(device)
    result = self.parent.yang_snapshot.snapshot(
        self, device, steps, section)
    if result:
        steps.passed('Collected a snapshot.')
    else:
        steps.failed('Failed to collect a snapshot.')
    return result


@add_result_as_extra
def yang_snapshot_restore(
    self,
    device,
    steps,
    section,
    name,
    continue_=True,
    processor='',
    health_uids=None,
    health_groups=None,
    health_sections=None,
    result_status=None,
    *args,
    **kwargs,
):
    '''
    Action to remove the leftover config after a group of test cases. E.g.,
    when a leaf /native/ntp/peer/ipv6[host-name="genericstring"]/burst-opt is
    tested, YangSuite generates five test cases: create, delete, merge,
    replace and remove. These five test cases are in one group. After the last
    test case remove, in this example,
    /native/ntp/peer/ipv6[host-name="genericstring"] remains. This behavior is
    not desirable as its leftover config may impact other test cases in a
    negative way. The yang_snapshot_restore action is to detect and remove the
    leftover config caused by Yang actions.

    Parameters
    ----------
    self : `object`
        pyATS testcase object.

    device : `object`
        pyATS device object.

    steps : `object`
        pyATS Steps object.

    section : `object`
        pyATS Section object.

    name : `str`
        Action name.

    continue_ : `boolean`
        Whether steps should continue in case of failure.

    processor : `str`
        Processor string.

    health_uids : `object`
        UIDs of Genie Health.

    health_groups : `object`
        Groups of Genie Health.

    health_sections : `object`
        Sections of Genie Health.

    result_status : `str`
        It is allowed to change the result status to failed, passed, aborted,
        blocked, skipped, errored or passx when the step is passed. The desired
        result status can be specified here.

    Returns
    -------
    boolean
        Return True when the yang_snapshot_restore action was successful, and
        False otherwise. It may return None when the yang_snapshot_restore
        action finds nothing to remove.
    '''

    # Attribute yang_snapshot holds a YangSnapshot object, which contains
    # related snapshot info.
    if not hasattr(self.parent, 'yang_snapshot'):
        self.parent.yang_snapshot = YangSnapshot(device)
    result = self.parent.yang_snapshot.snapshot_restore(
        device, **kwargs)
    if result is None:
        steps.passed('Nothing to remove')
    elif result:
        steps.passed('RPC edit-config is successful and the snapshot is '
                     'restored.')
    else:
        steps.failed('RPC edit-config is not successful so the snapshot is '
                     'not restored.')
    return result


actions = {
    'configure': configure,
    'configure_dual': configure_dual,
    'parse': parse,
    'execute': execute,
    'dialog': dialog,
    'api': api,
    'tgn': api,
    'sleep': sleep,
    'yang': yang,
    'learn': learn,
    'print': print_,
    'rest': rest,
    'configure_replace': configure_replace,
    'save_config_snapshot': save_config_snapshot,
    'restore_config_snapshot': restore_config_snapshot,
    'run_genie_sdk': genie_sdk,
    'maple': maple,
    'compare': compare,
    'maple_search': maple_search,
    'diff': diff,
    'bash_console': bash_console,
    'yang_snapshot': yang_snapshot,
    'yang_snapshot_restore': yang_snapshot_restore,
    'check_yang_subscribe': check_yang_subscribe,
}
