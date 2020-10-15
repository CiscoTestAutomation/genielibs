# Python
import logging

# Genie
from genie.metaparser.util.exceptions import SchemaEmptyParserError

# Logger
log = logging.getLogger(__name__)

def get_platform_default_dir(device, output=None):
    '''Get the default directory of this device

        Args:
            device (`obj`): Device object
            output (`str`): Output of `dir` command
        Returns:
            default_dir (`str`): Default directory of the system
    '''

    try:
        output = device.parse("dir", output=output)
    except SchemaEmptyParserError as e:
        raise Exception("Command 'dir' did not return any output") from e

    default_dir = output.setdefault('dir', {}).get('dir', '').replace('/', '')

    return default_dir

def get_platform_core(device, default_dir, output=None, keyword=['.core.gz']):
    '''Get the default directory of this device

        Args:
            device      (`obj`) : Device object
            default_dir (`str`) : default directory on device
            output      (`str`) : Output of `dir` command
            keyword     (`list`): List of keywords to search
        Returns:
            corefiles (`list`): List of found core files
    '''

    cmd = "dir {default_dir}/core/".format(default_dir=default_dir)

    try:
        # sample output:
        # #dir bootflash:core
        # Directory of bootflash:/core/
        #
        # 64899  -rw-           501904  Aug 28 2015 10:16:28 +00:00  RP_0_vman_23519_1440756987.core.gz
        output = device.parse(cmd, output=output)
    except SchemaEmptyParserError:
        # empty is possible. so pass instead of exception
        pass

    corefiles = []
    if output:
        for file in output.q.get_values('files'):
            for kw in keyword:
                if kw in file:
                    corefiles.append('file')

    return corefiles


def get_platform_logging(device,
                         command='show logging',
                         files=None,
                         keywords=None,
                         output=None):
    '''Get logging messages

        Args:
            device    (`obj`): Device object
            command   (`str`): Override show command
            files    (`list`): Not applicable on this platform
            keywords (`list`): List of keywords to match
            output    (`str`): Output of show command
        Returns:
            logs     (`list`): list of logging messages
    '''

    # check keywords and create strings for `include` option
    kw = ''
    if isinstance(keywords, list):
        kw = '|'.join(keywords)

    # check if keywords are given and create a command
    if kw:
        cmd = "{command} | include {kw}".format(command=command, kw=kw)
    else:
        cmd = command

    parsed = {}
    try:
        parsed = device.parse(cmd, output=output)
    except SchemaEmptyParserError as e:
        # empty is possible. so pass instead of exception
        pass

    return parsed.setdefault('logs', [])

    
def get_platform_cpu_load(device,
                          command='show processes cpu',
                          processes=None,
                          check_key='five_sec_cpu',
                          output=None):
    '''Get cpu load on device
        Args:
            device     (`obj`): Device object
            command    (`str`): Override show command
                                Default to `show processes cpu`
            processes (`list`): List of processes to check
            check_key  (`str`): Key to check in parsed output
                                Default to `five_sec_cpu`
            output     (`str`): Output of show command
        Returns:
            cpu_load   (`int`): Cpu load (5 secs average by default) on the device (percentage)
                                If multiple processes are given, returns average.
    '''

    cpu_load = 0

    try:
        parsed = device.parse(command, output=output)
    except SchemaEmptyParserError as e:
        log.error("Command '{cmd}' did not return any output\n{msg}".\
                  format(cmd=command, msg=str(e)))
        return None

    if processes:
        count = 0
        for ps_item in processes:
            # To get process id based on check_key
            # {
            #   (snip))
            #   "sort": {
            #     "1": {
            #       "process": "Chunk Manager",
            #       (snip)
            #       "five_sec_cpu": 0.0,
            pids = parsed.q.contains_key_value(
                'process', ps_item, value_regex=True).get_values('sort')
            count = len(pids)
            for pid in pids:
                cpu_load += parsed.q.contains_key_value('sort',
                                                        pid).get_values(
                                                            check_key, 0)
        if count == 0:
            cpu_load = 0
        else:
            cpu_load /= count
    else:
        cpu_load = float(parsed['five_sec_cpu_total'])

    return cpu_load


def get_platform_cpu_load_detail(device,
                                 command='show processes cpu',
                                 processes=None,
                                 check_key='five_sec_cpu',
                                 output=None):
    '''Get cpu load on device

        Args:
            device     (`obj`): Device object
            command    (`str`): Override show command
                                Default to `show processes cpu`
            processes (`list`): List of processes to check
            check_key  (`str`): Key to check in parsed output
                                Default to `five_sec_cpu_total`
            output     (`str`): Output of show command
        Returns:
            cpu_load_dict  (`dict`): Cpu load dictionary on the device
                                     example:
                                     {
                                         'OMP': 0.0,
                                         'NAT-ROUTE': 0.0,
                                     }
    '''

    cpu_load_dict = {}

    try:
        parsed = device.parse(command, output=output)
    except SchemaEmptyParserError as e:
        log.error("Command '{cmd}' did not return any output\n{msg}".\
                  format(cmd=command, msg=str(e)))
        return None

    all_processes = parsed.q.get_values('process')

    if processes or all_processes:
        for ps_item in processes or all_processes:
            # To get process id based on check_key
            # {
            #   (snip))
            #   "sort": {
            #     "1": {
            #       "process": "Chunk Manager",
            #       (snip)
            #       "five_sec_cpu": 0.0,
            indexes = parsed.q.contains_key_value(
                'process', ps_item, value_regex=True).get_values('sort')
            for index in indexes:
                process = parsed.q.contains_key_value('sort', index).get_values('process', 0)
                cpu_load_dict.update({
                    process:
                    parsed.q.contains_key_value('sort',
                                                index).get_values(check_key, 0)
                })

    return cpu_load_dict


def get_platform_memory_usage(device,
                              command='show processes memory',
                              processes=None,
                              check_key='processor_pool',
                              output=None):
    '''Get memory usage on device

        Args:
            device         (`obj`): Device object
            command        (`str`): Override show command
                                    Default to `show processes memory`
            processes     (`list`): List of processes to check
                                    If both processes and check_key are given,
                                    processes are preferred.
            check_key      (`str`): Key to check in parsed output
                                    Default to `processor_pool`
            output         (`str`): Output of show command
        Returns:
            memory_usage (`float`): memory usage on the device (percentage)
                                    If multiple processes are given, returns average.
    '''

    memory_usage = 0

    try:
        parsed = device.parse(command, output=output)
    except SchemaEmptyParserError as e:
        log.error("Command '{cmd}' did not return any output\n{msg}".\
                  format(cmd=command, msg=str(e)))
        return None

    if processes:
        count = 0
        memory_holding = 0
        for ps_item in processes:
            # To get process id based on check_key
            # {
            #   "processor_pool": {
            #     "total": 735981852,
            #     "used": 272743032,
            #     "free": 463238820
            #   },
            #   (snip)
            #   "pid": {
            #     "0": {
            #       "index": {
            #         "1": {
            #           "pid": 0,
            #           "tty": 0,
            #           "allocated": 256940960,
            #           "freed": 73576632,
            #           "holding": 158001024,
            #           "getbufs": 392,
            #           "retbufs": 12905093,
            #           "process": "*Init*"
            #         },
            pids = parsed.q.contains_key_value(
                'process', ps_item, value_regex=True).get_values('pid')
            count = len(pids)
            for pid in pids:
                # use `sum` because it's possible one pid returns multiple `holding`
                memory_holding += sum(
                    parsed.q.contains_key_value('pid',
                                                pid).get_values('holding'))
        if parsed.get(check_key, {}).get('total', 0) == 0:
            memory_usage = 0
        else:
            memory_usage = memory_holding / parsed[check_key]['total']
    else:
        if parsed.get(check_key, {}).get('total', 0) == 0:
            memory_usage = 0
        else:
            memory_usage = parsed[check_key]['used'] / parsed[check_key][
                'total']

    return memory_usage * 100


def get_platform_memory_usage_detail(device,
                                     command='show processes memory',
                                     processes=None,
                                     check_key='processor_pool',
                                     output=None):
    '''Get memory usage on device

        Args:
            device         (`obj`): Device object
            command        (`str`): Override show command
                                    Default to `show processes memory`
            processes     (`list`): List of processes to check
                                    If both processes and check_key are given,
                                    processes are preferred.
            check_key      (`str`): Key to check in parsed output
                                    Default to `processor_pool`
            output         (`str`): Output of show command
        Returns:
            memory_usage_dict (`dict`): memory usage dict on the device (percentage)
                                        example:
                                        {
                                            'OMP': 0.0012294695662956926,
                                            'NAT-ROUTE': 0.0012294695662956926,
                                        }
    '''

    regex_items = []
    memory_usage_dict = {}

    try:
        parsed = device.parse(command, output=output)
    except SchemaEmptyParserError as e:
        log.error("Command '{cmd}' did not return any output\n{msg}".\
                  format(cmd=command, msg=str(e)))
        return None

    all_processes = parsed.q.get_values('process')

    if isinstance(processes, list):
        for item in processes:
            regex_items += parsed.q.contains_key_value('process', item, value_regex=True).get_values('process')

    if regex_items:
        processes = regex_items

    if processes or all_processes:
        for ps_item in processes or all_processes:
            # To get process id based on check_key
            # {
            #   "processor_pool": {
            #     "total": 735981852,
            #     "used": 272743032,
            #     "free": 463238820
            #   },
            #   (snip)
            #   "pid": {
            #     "0": {
            #       "index": {
            #         "1": {
            #           "pid": 0,
            #           "tty": 0,
            #           "allocated": 256940960,
            #           "freed": 73576632,
            #           "holding": 158001024,
            #           "getbufs": 392,
            #           "retbufs": 12905093,
            #           "process": "*Init*"
            #         },
            
            pids = parsed.q.contains_key_value(
            'process', ps_item, value_regex=True, escape_special_chars_value=['*']).get_values('pid')

            memory_holding = 0
            for pid in pids:
                # use `sum` because it's possible one pid returns multiple `holding`
                memory_holding += sum(
                    parsed.q.contains_key_value('pid',
                                                pid).get_values('holding'))

            if parsed.get(check_key, {}).get('total', 0) == 0:
                memory_usage = 0
            else:
                memory_usage = memory_holding / parsed[check_key]['total']

            memory_usage_dict.update({ps_item: memory_usage * 100})

    return memory_usage_dict
