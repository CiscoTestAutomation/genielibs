from pyats.utils.fileutils import FileUtils

def show_tech(device, features):
    if not hasattr(device, 'filetransfer_attributes'):
        raise Exception('No information about file transfer on the device')

    address = device.filetransfer_attributes['server_address']
    protocol = device.filetransfer_attributes['protocol']
    path = device.filetransfer_attributes.get('path', '')

    for feature in features:
        file_ = '{p}_{f}'.format(p=path, f=feature)
        url = '{p}://{address}/{file}'.format(p=protocol,
            address=address, file=file_)
        device.execute('show tech-support {f} | redirect {u}'.format(f=feature,
                                                                     u=url))
