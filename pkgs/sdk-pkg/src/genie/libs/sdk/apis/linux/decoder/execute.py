import logging
log = logging.getLogger()

def decode_core(device, corefile, result_file='', timeout=300):
    """ Function to decode the given corefile """

    cmd = "/auto/mcp-project1/decoder/decode.py --noemail {cf}".format(cf=corefile)
    decode_output = ''

    try:
        decode_output = device.execute("{command}".format(command=cmd), timeout=timeout)
    except Exception as e:
        raise Exception('decoding core file is failed. {}'.format(e))
    if 'CORE file decode failed' in decode_output:
        raise Exception('Failed to decode core file.')

    if result_file:
        output = decode_output.splitlines()
        with open(result_file, 'w') as f:
            for line in output:
                f.write(line+"\n")

    return decode_output
