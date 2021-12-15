# Python
import logging
import time
import re
from genie.utils.timeout import Timeout
from genie.metaparser.util.exceptions import SchemaEmptyParserError

# unicon
from unicon.eal.dialogs import Dialog, Statement

log = logging.getLogger(__name__)


def get_aaa_member(device, leaf, keyword, intf):
    '''Get aaa member by parsing variuos aaa related commands
        Args:
            device (`obj`): Device object
            leaf   (`str`): Need xpath value for this leaf
                            ref:accounting-method, athorization-method,
                            athenticating-method, event-type, role, username,
                            password, secret, server-name, server-type, opens,
                            closes, aborts, reject, request, timeouts, source-address
            keyword (`str`): This argument highlihgts particular section from
                            'show run aaa' command.
                            eg:"show run aaa | sec " + keyword => keyword = accounting
            intf   (`str`): interface name
        Returns:
            Valid xpath value for the leaf or None
    '''
    #Nested function to send master key to cli interface
    def send_master_key(spawn, key):
        spawn.sendline(f'{key}')

    key_dialog = Dialog([
        Statement(pattern=r'.*New key:*',
                  action=send_master_key,
                  args={"key":keyword},
                  loop_continue=True,
                  continue_timer=False),
        Statement(pattern=r'.*Confirm key:*',
                  action=send_master_key,
                  args={"key":keyword},
                  loop_continue=True,
                  continue_timer=False),
        Statement(pattern=r'.*Old key:*',
                  action=send_master_key,
                  args={"key":keyword},
                  loop_continue=True,
                  continue_timer=False),
    ])

    if (leaf == "accounting-method"):
        output = []
        count = 0
        cmd = "show run aaa | sec " + keyword
        out = device.execute(cmd)
        #start contains index of "default"
        start = out.index("default")
        #container is a substring of "out" starting from "default"
        container = out[start:]
        if 'aaa' in container:
            end = container.index("aaa")
            #start contains the index of "group"
            start = container.index("group")
            #sub_str contains the length of "group"
            sub_str = len("group")
            #container2 is the substringof container
            container2 = container[start + sub_str + 1:end]
            #container2 is split into a list
            container2 = container2.split()
            for value in container2:
                if value != 'group':
                    count = count + 1
                    output.append(value)
        else:
            #start contains the index of "group"
            start = container.index("group")
            #sub_str contains the length of "group"
            sub_str = len("group")
            container2 = container[start + sub_str + 1:]
            container2 = container2.split()
            for value in container2:
                if value != 'group':
                    count = count + 1
                    output.append(value)
        if output[count - 1] == "radius":
            return "oc-aaa-types:RADIUS_ALL"
        elif output[count - 1] == "tacacs+":
            return "oc-aaa-types:TACACS_ALL"
        elif output[count - 1] == "local":
            return "oc-aaa-types:LOCAL"
        return None
    elif (leaf == "authentication-method" or leaf == "authorization-method"):
        tar_list = ['oc-aaa-types:LOCAL','oc-aaa-types:RADIUS_ALL',
                    'oc-aaa-types:TACACS_ALL']
        cmd = "show run aaa | sec " + keyword
        out = device.execute(cmd)
        if (leaf == "authentication-method"):
            start = out.index("login")
        elif(leaf == "authorization-method"):
            start = out.index("exec")
        leaf_str = "aaa " + keyword
        sub_str = len(leaf_str)
        #container is a substring of "out" starting from "exec"
        container = out[start:]
        start = container.index(leaf_str)
        #input_val is a substring of "out"
        input_val = out[0:start + sub_str]
        #src_list holds output values
        src_list = []
        count = 0
        if "local" in input_val:
            src_list.append('local')
            count = count + 1
        if "radius" in input_val:
            src_list.append('radius')
            count = count + 1
        if "tacacs+" in input_val:
            src_list.append('tacacs+')
            count = count + 1
        return tar_list[count - 1]
    elif(leaf == "event-type" or leaf == "role"):
        cmd = "show run aaa | sec " + keyword
        out = device.execute(cmd)
        output = 'Null'
        method_str = "aaa " + keyword
        if (leaf == 'event-type'):
            start = out.index(method_str)
            sub_str = len(method_str)
            end = out.index("default")
            output = (out[start + sub_str + 1:end])
            if ((output == "exec ") and (keyword == "authorization")):
                return "oc-aaa-types:AAA_AUTHORIZATION_EVENT_CONFIG"
            elif ((output == "exec ") and (keyword == "accounting")):
                return "oc-aaa-types:AAA_ACCOUNTING_EVENT_LOGIN"
            else:
                if keyword == "authorization":
                    return "oc-aaa-types:AAA_AUTHORIZATION_EVENT_COMMAND"
                else:
                    return "oc-aaa-types:AAA_ACCOUNTING_EVENT_COMMAND"
        elif (leaf == 'role'):
            start = out.index("default")
            sub_str = len("default")
            end = out.index("group")
            output = (out[start + sub_str + 1:end])
            if (output == "start-stop "):
                return "START_STOP"
            elif (output == "stop-only "):
                return "STOP"
            else:
                return None
    elif (leaf == "username" or leaf == "password" or leaf == "secret" 
            or leaf == "privilege"):
        cmd = "show run aaa | sec "
        cmd = cmd + keyword
        out = device.execute(cmd)
        info = out.split()
        index = info.index(leaf)
        if (leaf == "password" or leaf == "secret"):
            return (info[index+2])
        elif (leaf == "privilege"):
            role = int(info[index+1])
            if (role == 15):
                return "oc-aaa-types:SYSTEM_ROLE_ADMIN"
            else:
                return (role)
        else:
            return (info[index+1])
    elif (leaf == "server-name" or leaf == "server-type" 
            or leaf == "server-private" or leaf == "timeout"):
        cmd = "show run | sec " + keyword
        out = device.execute(cmd)
        info = out.split()
        i = 0
        for out in info:
            i+= 1
            if (leaf == "server-name" or leaf == "server-type"):
                if out == 'server':
                    break
            else:
                if out == leaf:
                    break
        if (leaf == "server-name"):
            ret_val = info[i + 1]
        elif (leaf == "server-type"):
            if info[i] == "tacacs+":
               ret_val = "oc-aaa:TACACS"
            elif info[i] == "radius":
               ret_val = "oc-aaa:RADIUS"
        else:
            ret_val = info[i]
        return ret_val
    elif (leaf == "opens" or leaf == "closes" or leaf == "aborts" 
            or leaf == "failures" or leaf == "connection-timeouts"):
        cmd = "show tacacs private "
        out = device.execute(cmd)
        i = out.split("Tacacs+")
        if leaf == "connection-timeouts":
            leaf = "Timeouts"
        elif leaf == "failures":
            leaf = "errors"
        input_leaf = leaf + ":"
        input_group = keyword
        ret = None
        for target_item in i:
            if input_group in target_item:
                x = target_item.split()
                index = x.index(input_leaf)
                ret = (x[index + 1])
        return ret
    elif(leaf == "reject" or leaf == "request" or leaf == "timeouts" 
            or leaf == "accept" or leaf == "total responses" 
            or leaf == "error" or leaf == "retransmission"):
        cmd = "show aaa servers | sec " + keyword
        out = device.execute(cmd)
        if (leaf == "request" or leaf == "error"):
            list_AA = out.split("Elapsed")
        else:
            list_AA = out.split("Account")
        list_index = list_AA[0]
        lists = list_index.split()
        var = 0
        num = 0
        for out in lists:
            var += 1
            if out == leaf:
                str = lists[var]
                if leaf == "retransmission":
                    num = num + int(str)
                else:
                    num += int(str[:-1])
        return(num)
    elif (leaf == "variable"):
        return keyword
    elif (leaf == 'source-address'):
        out = device.execute("show ip interface brief")
        info = out.split()
        index = info.index(intf)
        return (info[index+1])
    elif (leaf == 'hash-key'):
        #to validate secret-key-hahsed leaf
        cmd = f'show run | sec {keyword}'
        out = device.execute(cmd)
        info = re.compile(r'key 6 (.*)')
        return re.findall(info, out)[0]
    elif (leaf == "masterkey"):
        #set master key
        device.configure("password encryption aes", timeout = 10)
        device.configure("key config-key password-encrypt", reply = key_dialog, allow_state_change = True)
        return None
    else:
        cmd = "show run | sec " + keyword
        out = device.execute(cmd)
        info = out.split()
        index = info.index(leaf)
        return (info[index+1])


def get_auth_session(device, interface=None, mac_address=None, method='dot1x',
                     search_value='Authc Success', timeout=1, interval=1):
    """
    Get the authentication session details for the device interface
    Args:
        device ('obj'): Device object
        interface ('str'): interface to check the authentication session
        mac_address ('str'): mac-address of the session
        search_value (str): key to be matched for method status
        method ('str', optional): dot1x/mab session
        timeout (int, optional): Total timeout in seconds. Defaults to 1
        interval (int, optional): interval in seconds to check for authentication.
                                  Defaults to 1
    Returns:
        None if authentication session is empty
        Authentication session dictionary if session exists
    Raise:
        AttributeError
    """
    if interface is not None:
        interface = interface
    elif interface is None and 'interface' in device.custom and \
            device.custom['interface']:
        interface = device.custom['interface']
    else:
        raise AttributeError("No interface argument was provided and no interface key"
                             " was defined under device.custom")

    if mac_address is not None:
        mac_address = mac_address
    elif mac_address is None and 'mac_address' in device.custom and \
            device.custom['mac_address']:
        mac_address = device.custom['mac_address']
    else:
        raise AttributeError("No mac_address argument was provided and no mac_address "
                             "key was defined under device.custom")

    timeout = Timeout(timeout, interval)
    while timeout.iterate():
        try:
            # get the authentication session
            user_session = device.parse('show authentication sessions interface {} '
                                        'details'.format(interface))
        except SchemaEmptyParserError:
            log.warning("Authentication session is not created, "
                        "Waiting for {} sec".format(interval))
            time.sleep(interval)
            continue

        if user_session.q.contains('interfaces').contains(interface).contains(
                'mac_address').contains(mac_address):
            mac_client = user_session.get('interfaces', {}).get(interface, {}).get(
                'mac_address').get(mac_address, {})
            search_key = mac_client.get('method_status', {}).get(method, {}).get(
                'state')

            # Verify if search criteria matched
            if search_key == search_value:
                return mac_client
            else:
                log.warning("Authentication session is created, but the "
                            "search_value is not matched. "
                            "Waiting for {} sec".format(interval))
                time.sleep(interval)
        else:
            log.warning("Authentication session with interface : {i} and mac "
                        "address : {m} not found. Waiting for {t} secs".format(
                         i=interface, m=mac_address, t=interval))
            time.sleep(interval)

    return None


def get_running_config_section_attr44(device, option):
    """ Return list with configuration section starting with passed keyword
        Args:
            device ('obj') : Device object to extract configuration
            option (`str`) : match string
        Returns:
            Return the configuration with the passed keyword
    """

    output = device.execute(
        "show running-config | include {option}".format(option=option))

    m = {}
    m = re.search(r"radius-server.*(attribute).*(44).*(extend-with-addr)".format(option), output)

    return m
