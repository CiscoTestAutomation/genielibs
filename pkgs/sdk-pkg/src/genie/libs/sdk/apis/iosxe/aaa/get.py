# Python
import logging
import re

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
    else:
        cmd = "show run | sec " + keyword
        out = device.execute(cmd)
        info = out.split()
        index = info.index(leaf)
        return (info[index+1])

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
