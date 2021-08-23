# Python
import logging

# Genie
from genie.metaparser.util.exceptions import SchemaEmptyParserError

log = logging.getLogger(__name__)

def get_lacp_member(device, port_channel, count, member, intf_list, internal=False):
    """ This API parse's 'show lacp internal/neighbor' commands and return requested member
        Args:
            device (`obj`): Device object
            port_channel (`str`): Port channel name
            count (`int`): Required interface count
            member (`str`): Specify one of them to search ‘interface’, ‘port_num’, ‘oper_key’ or ‘partner_id’
                             ex.) member=‘interface’
            intf_list(`list'): List of interfaces
            internal (`bool`): True = internal command and False = neighbor command
        Returns:
            If success, returns member value or None
    """
    if (internal == True):
        out = device.parse("show lacp internal")
    else:
        out = device.parse("show lacp neighbor")

    port_channel =  port_channel.capitalize()

    if (
        out
        and "interfaces" in out
        and port_channel in out["interfaces"]
        and "members" in out["interfaces"][port_channel]
    ):
        for intf in out["interfaces"][port_channel]["members"]:
            if out["interfaces"][port_channel]["members"][intf][member]:
                if member == "partner_id":
                    res = out["interfaces"][port_channel]["members"][intf][member]
                    #The example value in res: 50f7.22b2.f200
                    res1 = ''.join([res[i] for i in range(len(res)) if res[i] != '.'])
                    #The example value in res1: 50f722b2f200
                    res2 = ':'.join(res1[i:i + 2] for i in range(0, len(res1), 2))
                    #The example value in res2: 50.f7.22.b2.f2.00
                    return res2
                elif member == "interface":
                    ifs = out["interfaces"][port_channel]["members"][intf][member]
                    if ifs == intf_list[count]:
                        return ifs
                else:
                    temp = "interface"
                    ifs = out["interfaces"][port_channel]["members"][intf][temp]
                    if ifs == intf_list[count]:
                        return out["interfaces"][port_channel]["members"][intf][member]
    return None

def get_lacp_sys_id(device):
    """ This API parse's 'show lacp sys-id' command and return sys id
        Args:
            device (`obj`): Device object
        Returns:
            Returns system id
    """
    res = device.execute("show lacp sys-id")
    #cli output for 'show lacp sys-id' example res: 32768, 70d3.7984.aa80
    res = ''.join([res[i] for i in range(len(res)) if i > 6])
    #Now the value in res: 70d3.7984.aa80
    res1 = ''.join([res[i] for i in range(len(res)) if res[i] != '.'])
    #Now the value in res1 : 70d37984aa80
    sys_id = ':'.join(res1[i:i + 2] for i in range(0, len(res1), 2))
    #After adding dots at required places sys id as 70:d3:79:84:aa:80
    return sys_id

def get_lacp_intf_count(device, port_channel):
    """ This API parse 'show lacp internal' command and return number of member interfaces
        Args:
            device (`obj`): Device object
            port_channel (`str`): Port channel name
        Returns:
            Returns interface count
    """
    try:
        out = device.parse("show lacp internal")
    except SchemaEmptyParserError:
        return 0

    port_channel =  port_channel.capitalize()

    count = 0
    if (
        out
        and "interfaces" in out
        and port_channel in out["interfaces"]
        and "members" in out["interfaces"][port_channel]
    ):
        for intf in out["interfaces"][port_channel]["members"]:
            if out["interfaces"][port_channel]["members"][intf]:
                temp = "interface"
                ifs =  out["interfaces"][port_channel]["members"][intf][temp]
                count = count + 1
    return count

def get_lacp_intf_list(device, port_channel):
    """ This API parse 'show lacp internal' command and return interface list
        Args:
            device (`obj`): Device object
            port_channel (`str`): Port channel name
        Returns:
            Returns interface list
    """

    try:
        out = device.parse("show lacp internal")
    except SchemaEmptyParserError:
        return []

    port_channel =  port_channel.capitalize()

    intf_list = []
    if (
        out
        and "interfaces" in out
        and port_channel in out["interfaces"]
        and "members" in out["interfaces"][port_channel]
    ):
        for intf in out["interfaces"][port_channel]["members"]:
            if out["interfaces"][port_channel]["members"][intf]:
                temp = "interface"
                ifs =  out["interfaces"][port_channel]["members"][intf][temp]
                intf_list.append(ifs)
    return intf_list
