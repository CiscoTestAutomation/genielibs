# Python
import os
import re
import time
import logging
# Unicon
from unicon.core.errors import SubCommandFailure

# Logger
log = logging.getLogger(__name__)

def change_file_permissions(device, full_file_path, permission):
    """
    Function to generate a dummy file using the 'dd' command.
    Args:
        device ('obj'): Device object
        full_file_path (str): The path where the file will be created.
        permission (str): Permission of file 
    """
    try:
        device.execute(
            f"chmod {permission} {full_file_path}"
        )

    except SubCommandFailure as e:
        raise SubCommandFailure(f"Error: Failed to change permissions for {full_file_path}. {e}")
        
def generate_dummy_file(device, file_path, file_name, block_size, count):
    """
    Function to generate a dummy file using the 'dd' command.
    Args:
	device ('obj'): Device object
        file_path (str): The path where the file will be created.
        file_name (str): The name of the dummy file.
        block_size (str): The size of each block.
        count (int): The number of blocks to write.
    """
    try:
        full_file_path = f"{file_path}/{file_name}"
        device.execute(
            f"dd if=/dev/zero of={full_file_path} bs={block_size} count={count}"
	    )

    except SubCommandFailure as e:
        raise SubCommandFailure(f"An error occurred during file generate using dd command:\n{e}")
   

