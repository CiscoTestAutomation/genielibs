
# Python
import re

import os

import uuid
import base64

def learn_routem_configs(device, output_config=False):
    """ Gets the current running config on device
        Args:
            output_config ('bool'): Specifies whether the config
            or path of the config is outputted 
        Raise:
            None
        Returns:
            Config ('dict'): {pid: config}
            ex.) Config = {'123': 'config'}
    """
    output = device.parse("ps -ef | grep routem")['pid']
    configs = {}

    for pid, info in output.items():
        config_data = info['cmd'].split()
        
        if len(config_data) == 4:
            config_data = config_data[2]
        else:
            continue

        if output_config:

            try:
                config_data = device.execute("cat {}".format(config_data))
            except:
                raise ValueError("The config file at {} does not exist.".format(config_data))

        configs.setdefault(pid, config_data)

    return configs

def learn_process_pids(device, search):
    """ Finds the PIDs of processes that match the search
        Args:
            search ('str'): The name of the processes to find
        Raise:
            None
        Returns:
            PIDs ('list'): [pid]
            ex.) PIDs = ['123', '456']
    """
    output = device.parse("ps -ef | grep {}".format(search))['pid']

    return list(output.keys())

def kill_processes(device, pids):
    """ Kills the processes with given PIDs 
        Args:
            pids ('list'): List of PIDs
            ex.) pids = [12, 15, 16]
        Raise:
            ValueError: Process with PID does not exist
        Returns:
            None
    """
    for pid in pids:
        output = device.execute("kill {}".format(pid))
        
        if "No such process" in output: 
            raise ValueError("Process with PID {} does not exist.".format(pid))


def copy_data_to_device(device, data, destination, filename=None):
    """ Copies data into a device and creates a file to store that data.
        Args:
            data ('str'): The data to be copied
            destination ('str'): Folder of where to store file
            filename ('str'): Name of the file created. If left none then a 
                random name will be generated
        Raise:
            Exception: Permission Denied, File Creation Failed
        Returns:
            Path (str): path of created file
    """
    # Data must end in new line
    if len(data) > 0 and not data[-1] == "\n": 
        data += "\n"

    # Transforms text data into base64 string
    encoded = base64.b64encode(bytes(data, "utf-8")).decode("utf-8")

    if filename is None:
        id = uuid.uuid4().hex
        filename = os.path.join(destination, id)
    else:
        filename = os.path.join(destination, filename)

    # Decode base 64 data into file
    device.execute("DATA=\"{}\"".format(encoded))
    device_out = device.execute("echo $DATA | base64 -d > {}".format(filename))

    if 'Permission denied' in device_out:
        raise Exception("Permission denied while trying to create file. " + \
            "Make sure {} has the correct permissions!".format(filename))

    # Verify file has been successfully created
    try:
        device.execute("ls {}".format(filename))
    except Exception:
        raise Exception("Creating of file {} has failed. No file created."
                                                            .format(filename))

    if int(device.execute('stat {} --printf="%s\\n"'.format(filename))) == 0: 
        raise Exception("Creating of file {} has failed. Created file has no content"
                                                            .format(filename))

    return filename

def read_data_from_device(device, location):
    """ Reads text data from device and returns it as output
        Args:
            location ('str'): Path to the text file
        Raises:
            Exception: File Does not Exist
        Returns:
            Data ('str'): Text data read from the device
    """
    # IMPORTANT
    # =========
    # This API does not require the device to have network connection
    # copy_from_device is the other API that behaves similar to this one,
    # but it requires network connection since it uses SCP

    return device.execute("cat {}".format(location))

def start_routem_process(device, config, routem_executable, config_save_location="/tmp"):

    """ Starts the routem executable with the provided config
        Args:
            config ('str'): Path to config file or raw config data
            routem_executable ('str'): Path to routem executable file 
            config_save_location ('str'): Path of folder of where to save the config
                file if raw config data is passed into the first argument
        Raise:
            None
        Returns:
            Success (bool): Whether or not the operation was successful
    """
    config = config.strip()

    # Test if config file exists
    try: 
        device.execute("ls {}".format(config))
    except Exception:
        config = device.api.copy_data_to_device(config, config_save_location)

    # Start routem process in background
    try:
        device.execute("nohup {} -f {} -i &>/dev/null &".format(routem_executable, config))
    except Exception:
        return False

    return True


def trex_copy_json(device, json, destination="/opt/trex"):
    """ Copies trex json config data to the trex folder
        Args:
            json (str): the json config in text form or path to json file on
                local machine
            destination (str): folder of where to put trex-config.json in
        Raise:
            None
        Returns:
            Success (bool): Whether or not the operation was successful
    """
    try:
        # Try to gain root access
        # If user don't have root permission this will throw error
        # That's fine as sometimes root is not needed to create a file
        device.execute("sudo -s")
    except Exception:
        pass

    # If path is passed in instead of text we read that file
    if os.path.exists(json):
        with open(json) as file:
            json = file.read()

    device.api.copy_data_to_device(json, destination, 'trex-config.json')
    return True

def start_trex_process(device, location = "/opt/trex"):
    """ Starts a trex process on the device
        Args:
            location (str): folder location of where the trex executable is at
        Raise:
            None
        Returns:
            Success (bool): Whether or not the operation was successful
    """
    device.execute("cd {}".format(location))
    device.execute("nohup sudo ./bringup.sh trex-config.json &>/dev/null &")
    return True

def is_process_started(device, name):
    """ Checks if a trex process is running right now.
        Args:
            name (str): Name of the process to search for
        Raise:
            None
        Returns:
            Running (bool): Whether or not the process is running
    """
    output = device.parse("ps -ef | grep %s" % name)['pid']
    
    # Minus one to discount the grep process
    return len(output) - 1 > 0

