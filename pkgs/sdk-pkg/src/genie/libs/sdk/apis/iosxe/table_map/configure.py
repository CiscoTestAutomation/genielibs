"""Common configure functions for interface"""
# Python
import logging
import re

# Unicon
from unicon.core.errors import SubCommandFailure

# Steps
from pyats.aetest.steps import Steps

log = logging.getLogger(__name__)
def configure_table_map(device,
        table_map_name,
        from_val,
        to_val,
        default_val='copy'
        ):
    """ Configures table_map
        Args:
             device ('obj'): device to use
             table_map_name('str') : name of the table map  name
             from_val('list') : list of from values
             to_val('list') : list of to values 
             default_val('str'): name of the default, default is copy


        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.debug(
        "Configuring table_map {table_map_name} ".format(
            table_map_name=table_map_name

        )
    )

    cmd = [f"table-map {table_map_name}"]
    cmd.extend([f'map from {table_map_from_valu} to {table_map_to_value}' for table_map_from_valu, table_map_to_value in zip(from_val,to_val)])

    cmd.append(f"default {default_val}") 
    try:
        device.configure(cmd)

    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure class_map. Error:\n{error}".format(
                error=e
            )
        )


def unconfigure_table_map(device, table_map_name):
    """ Unconfigures policy-map
        Args:
             device ('obj'): device to use
             table_map_name ('str'): name of the table

        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.debug(
        "Unconfiguring table_map {table_map_name}".format(
            table_map_name=table_map_name,
        )
    )

    cmd = f"no table-map {table_map_name}"

    try:
        device.configure(cmd)

    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure class_map. Error:\n{error}".format(
                error=e
            )
        )
    
def configure_table_map_set_default(device, table_map_name, sub_option = 'copy'):
    """ 
        Args:
            device ('obj'): device to use
            table_map_name ('str'): name of policy-map
            sub_option ('str'): copy(By default) or ignore or any value
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    try:
        cli = [
            "table-map {}".format(table_map_name), 
            "default {}".format(sub_option)
            ]
        device.configure(cli)
    except SubCommandFailure as e:
        raise SubCommandFailure("Failed to configure table map set default. Error:\n{error}".format(error=e))
