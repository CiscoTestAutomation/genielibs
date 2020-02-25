
# Python
import re
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
            config_data = device.execute("cat {}".format(config_data))
        
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

def start_routem_process(device, config, routem_executable):
    """ Starts the routem executable with the provided config
        Args:
            config ('str'): Path to config file or raw config data
            routem_executable ('str'): Path to routem executable file 
        Raise:
            None
        Returns:
            Success (bool): Whether or not the operation was successful
    """
    # Test if config file exists
    try: 
        device.execute("ls {}".format(config))
    except Exception:
        # If file is not found then create a config file
        # Config data must end in new line
        if len(config) > 0 and not config[-1] == "\n": 
            config += "\n"

        encoded = base64.b64encode(bytes(config, "utf-8")).decode("utf-8")
        id = uuid.uuid4().hex
        config = "/tmp/config_{}.conf".format(id)

        # Decode base 64 data into temporary file
        device.execute("CONFIG=\"{}\"".format(encoded))
        device.execute("echo $CONFIG | base64 -d > /tmp/config_{}.conf".format(id))
    
    # Start routem process in background
    try:
        device.execute("nohup {} -f {} -i &>/dev/null &".format(routem_executable, config))
    except Exception:
        return False

    return True
