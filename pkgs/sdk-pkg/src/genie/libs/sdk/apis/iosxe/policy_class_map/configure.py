"""Common configure functions for interface"""
# Python
import logging

# Unicon
from unicon.core.errors import SubCommandFailure

# Steps
from pyats.aetest.steps import Steps

log = logging.getLogger(__name__)

def configure_class_map(device,
        class_name,
        match_val,
        match_mode=None,
        match_val1=None,
        match_mode1=None,
        class_match_type='match-all',
        access_group=False):
    """ Configures class-map
        Args:
             device ('obj'): device to use
             class_name ('str'): name of the class
             match_val  ('str'): values of the match
             match_mode ('str',optional): name of the match_mode, default is None
             match_val1 ('str',optional): name of the match_mode 2, default is None
             match_mode1 ('str',optional): name of the match_mode type, default is None
             class_match_type ('str',optional): name of the match type, default is match-all
             access_group ('bool', optional): create class match with acls groups, default is False

        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.info(
        "Configuring class_map {class_name} with {match_mode} {class_match_type}".format(
            class_name=class_name,
            match_mode=match_mode,
            class_match_type=class_match_type
        )
    )
    cmd = [f"class-map {class_match_type} {class_name}"]
    if access_group:
        cmd.append(f"match access-group name {match_val}")
    elif match_mode:
        cmd.append(f"match {match_mode}  {match_val}")
    if match_val1 and match_mode1:
        cmd.append(f"match {match_mode1}  {match_val1}")

    try:
        device.configure(cmd)

    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure class_map. Error:\n{error}".format(
                error=e
            )
        )




def unconfigure_class_map(device, class_name, class_match_type='match-all'):
    """ Unconfigures class-map
        Args:
             device ('obj'): device to use
             class_name ('str'): name of the class
             class_match_type ('str',optional): name of the match type, default is 'match-all'

        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.info(
        "Unconfiguring class_map {class_name}".format(
            class_name=class_name,
        )
    )

    cmd = f"no class-map {class_match_type} {class_name}"

    try:
        device.configure(cmd)

    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure class_map. Error:\n{error}".format(
                error=e
            )
        )


def configure_class_map_type_traffic(
    device,
    class_name,
    match_type="match-any",
    input_acl=None,
    output_acl=None,
):
    """Configure class-map type traffic.

        Args:
            device ('obj'): device to use
            class_name ('str'): name of the class-map
            match_type ('str', optional): match type, default is match-any
            input_acl ('str', optional): input ACL name
            output_acl ('str', optional): output ACL name

        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.debug(
        "Configuring class-map type traffic {class_name}".format(
            class_name=class_name,
        )
    )

    cmd = [f"class-map type traffic {match_type} {class_name}"]
    if output_acl:
        cmd.append(f"match access-group output name {output_acl}")
    if input_acl:
        cmd.append(f"match access-group input name {input_acl}")

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure class-map type traffic. Error:\n{error}".format(
                error=e
            )
        )


def configure_class_map_access_group_on_device(device, class_map_name, acc_list_number):
    """ Configure class-map access-group on device
        Args:
            device ('obj'): device to use
            class_map_name ('str'): class-map name on which we need to configure
            acc_list_number ('str') : access-list number/name
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.debug("Configuring class-map access-group on device")
    configs = [f'class-map match-all {class_map_name}',
           f'match access-group {acc_list_number}']
    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not configure class-map access-group on device {device}. Error:\n{e}")

def configure_traffic_class_for_class_map(device, class_map_name, matching_statement, traffic_class_value):
    """ Configure traffic-class for class-map on device
        Args:
            device ('obj'): device to use
            class_map_name ('str'): Class-map name
            matching_statement ('str') : matching statements under the classmap (match-any/match-all)
            traffic_class_value ('int'): Traffic Class value from 0 to 7
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.debug("Configuring traffic-class for class-map on device")
    cmd = [f'class-map {matching_statement} {class_map_name}',
        f'match traffic-class {traffic_class_value}']
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not configure traffic-class for class-map on device {device}. Error:\n{e}")

def configure_class_map_match_protocol_attribute(device, class_match_type, class_name, attribute_name, attribute_value):
    """ Configures a class-map with a 'match protocol attribute' statement.
        Args:
            device ('obj'): device to use
            class_match_type ('str'): The class match type (e.g., 'match-all').
            class_name ('str'): The name of the class-map (e.g., 'c-attr').
            attribute_name ('str'): The name of the protocol attribute (e.g., 'business-relevance').
            attribute_value ('str'): The value of the protocol attribute (e.g., 'business-relevant').
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.debug(
        f"Configuring class-map {class_name} with match protocol attribute {attribute_name} {attribute_value}"
    )
    cmd = [f"class-map {class_match_type} {class_name}"]
    cmd.append(f"match protocol attribute {attribute_name} {attribute_value}")

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not configure class-map. Error:\n{e}"
        )


def configure_class_map_type_inspect(
        device,
        class_map_name,
        match_type="match-any",
        match_access_group=None,
        match_access_group_name=None,
        match_protocol=None,
        match_class_map=None):
    """ Configure 'class-map type inspect' with match rules (ZBFW)

        Args:
            device ('obj'): Device object
            class_map_name ('str'): Name of the class-map
            match_type ('str', optional): 'match-any' or 'match-all'.
                Defaults to 'match-any'
            match_access_group ('str' or 'list', optional): Numbered access
                group(s) to match. Defaults to None
            match_access_group_name ('str' or 'list', optional): Named access
                group(s) to match. Defaults to None
            match_protocol ('str' or 'list', optional): Protocol(s) to match.
                Defaults to None
            match_class_map ('str' or 'list', optional): Nested class-map(s)
                to match. Defaults to None
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    cmd = [f"class-map type inspect {match_type} {class_map_name}"]
    if match_access_group_name is not None:
        if isinstance(match_access_group_name, str):
            match_access_group_name = [match_access_group_name]
        for acl in match_access_group_name:
            cmd.append(f"match access-group name {acl}")
    if match_access_group is not None:
        if isinstance(match_access_group, (str, int)):
            match_access_group = [match_access_group]
        for acl in match_access_group:
            cmd.append(f"match access-group {acl}")
    if match_protocol is not None:
        if isinstance(match_protocol, str):
            match_protocol = [match_protocol]
        for protocol in match_protocol:
            cmd.append(f"match protocol {protocol}")
    if match_class_map is not None:
        if isinstance(match_class_map, str):
            match_class_map = [match_class_map]
        for child in match_class_map:
            cmd.append(f"match class-map {child}")

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not configure class-map type inspect "
            f"{class_map_name}. Error:\n{e}"
        )


def unconfigure_class_map_type_inspect(
        device,
        class_map_name,
        match_type="match-any",
        match_access_group=None,
        match_access_group_name=None,
        match_protocol=None,
        match_class_map=None,
        remove_class_map=True):
    """ Unconfigure 'class-map type inspect' match rules (ZBFW)

        Args:
            device ('obj'): Device object
            class_map_name ('str'): Name of the class-map
            match_type ('str', optional): 'match-any' or 'match-all'.
                Defaults to 'match-any'
            match_access_group ('str' or 'list', optional): Numbered access
                group(s) to remove. Defaults to None
            match_access_group_name ('str' or 'list', optional): Named access
                group(s) to remove. Defaults to None
            match_protocol ('str' or 'list', optional): Protocol(s) to remove.
                Defaults to None
            match_class_map ('str' or 'list', optional): Nested class-map(s)
                to remove. Defaults to None
            remove_class_map ('bool', optional): Also delete the class-map
                with 'no class-map type inspect ...'. Defaults to True
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    cmd = []
    has_match = any(
        m is not None for m in (
            match_access_group,
            match_access_group_name,
            match_protocol,
            match_class_map,
        )
    )
    if has_match:
        cmd.append(f"class-map type inspect {match_type} {class_map_name}")
        if match_access_group_name is not None:
            if isinstance(match_access_group_name, str):
                match_access_group_name = [match_access_group_name]
            for acl in match_access_group_name:
                cmd.append(f"no match access-group name {acl}")
        if match_access_group is not None:
            if isinstance(match_access_group, (str, int)):
                match_access_group = [match_access_group]
            for acl in match_access_group:
                cmd.append(f"no match access-group {acl}")
        if match_protocol is not None:
            if isinstance(match_protocol, str):
                match_protocol = [match_protocol]
            for protocol in match_protocol:
                cmd.append(f"no match protocol {protocol}")
        if match_class_map is not None:
            if isinstance(match_class_map, str):
                match_class_map = [match_class_map]
            for child in match_class_map:
                cmd.append(f"no match class-map {child}")
        cmd.append("exit")
    if remove_class_map:
        cmd.append(
            f"no class-map type inspect {match_type} {class_map_name}"
        )

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not unconfigure class-map type inspect "
            f"{class_map_name}. Error:\n{e}"
        )
