import logging, re
log = logging.getLogger()


def decode_core(device, corefile, result_file='', timeout=300):
    """ Function to decode the given corefile """

    cmd = "/auto/mcp-project1/decoder/decode.py --noemail {cf}".format(
        cf=corefile)
    decode_output = ''

    try:
        decode_output = device.api.execute("{command}".format(command=cmd),
                                           timeout=timeout)
    except Exception as e:
        raise Exception('decoding core file is failed. {}'.format(e))

    if result_file:
        output = decode_output.splitlines()
        with open(result_file, 'w') as f:
            for line in output:
                f.write(line + "\n")

    if 'CORE file decode failed' in decode_output:
        raise Exception('Failed to decode core file.')

    return decode_output

def cdets_lookup(device, corefile, result_file, timeout=300):
    """ Function to return matching cdets given a corefile
    Note: The corefile should already be decoded as this function searches
    for the entry within the decoder archived database """
    res={}
    cmd = "/auto/binos-tools-hard/bin/binos-tools/decoder_db_utils/archive_lookup.py -f "
    if corefile:
        cmd += corefile
        try:
            output = device.execute("{command}".format(command=cmd), timeout=timeout)
        except Exception as e:
            raise Exception('Could not lookup cdets. {}'.format(e))
        output = output.strip()
        with open(result_file, 'a') as f:
            """output is a string with cdets and backtrace information"""
            if output.find('[]') != -1:
                bt_not_found = (output.find('None') != -1)
                if bt_not_found:
                    f.write("\n\nBacktrace is empty !!\n")
                else:
                    f.write("\n\nCDETS not found !!\n")
            else:
                cdets = output.split('\"')[1]
                f.write("\n\nCDETS with matching backtrace: {}\n".format(cdets))
                cdets=re.sub(r'[,\'\[\]\(\)]', '', cdets).split(' ')
                res['defect']={}
                i=0
                while i<len(cdets)-2:
                    res['defect'][cdets[i]] = {'state':cdets[i+1], 'percentage': cdets[i+2]}
                    i=i+3
    return res


def topic_search(device, result_file, timeout=300):
    """ Function to get the cdets from the result_file using topic_search api 
        Args:
            result_file (decoded text file)

        timeout (`int`):
            timeout to search topic. Default to 300 secs

        Returns:
            output (CDETS)
    """

    output = ""
    cmd = "/auto/binos-tools-hard/bin/binos-tools/decoder_db_utils/topic_search.py -f "
    if result_file:
        cmd += result_file
        try:
            output = device.execute(cmd, timeout=timeout)
        except Exception as e:
            log.warning('Topic search failed. {}'.format(e))
    if output != "":
        with open(result_file, 'a') as f:
            result = "Topic Search Result: {}".format(output)
            f.write(result)

    return output
