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
            