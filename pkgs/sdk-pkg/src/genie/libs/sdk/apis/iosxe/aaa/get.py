# Python
import logging

def get_aaa_member(device, leaf, var, intf):
    '''Get
        Args:
            device (`obj`): Device object
            leaf   (`str`): Need xpath value for this leaf
            var    (`str`): N/A
            intf   (`str`): interface name
        Returns:
            Valid xpath value for the leaf or None
    '''
    if (leaf == "server-name" or leaf == "server-type" 
            or leaf == "server-private" or leaf == "timeout"):
        cmd = "show run | sec " + var
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
        input_group = var
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
        cmd = "show aaa servers | sec " + var
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
        return var
    elif (leaf == 'source-address'):
        out = device.execute("show ip interface brief")
        info = out.split()
        index = info.index(intf)
        return (info[index+1])
    else:
        cmd = "show run | sec " + var
        out = device.execute(cmd)
        info = out.split()
        index = info.index(leaf)
        return (info[index+1])
