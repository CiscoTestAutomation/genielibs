# Python
import logging

# Logger
log = logging.getLogger(__name__)


def extract_tar_gz(device, path, files, option='-zxvf'):
    """ extract tar.gz file
        Args:
            files (`list`): list of tar.gz files
            option (`str`): option to tar command for extraction
                            Default to `-zxvf`
        Raises:
            N/A
        Returns:
            extracted_files (`list`): extracted file list
    """
    extracted_files = []

    log.debug('files : {f}'.format(f=files))

    for file in files:
        # check if the file has extention `.tar.gz`
        if '.tar.gz' not in file:
            raise Exception('file {f} is not tar.gz file'.format(f=file))
        # create folder_name from filename
        folder_name = file.split('.tar.gz')[0]
        # extract tar.gz file
        output = device.api.execute("cd {p} && mkdir {d} && cd {d} && tar {op} ../{f}".\
            format(p=path, d=folder_name, op=option, f=file))
        # based on output, `extracted_files` list will be created as return
        if output:
            for file in output.split():
                extracted_files.append('{p}/{d}/{f}'.format(p=path,
                                                            d=folder_name,
                                                            f=file))
        if 'cannot create directory' in output:
            raise Exception(
                "Directory {d} already exists and couldn't create".format(
                    d=folder_name))

    return extracted_files
