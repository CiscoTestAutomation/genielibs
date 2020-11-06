import os
from pyats.utils.fileutils import FileUtils


class TcpDump(object):
    '''
        Run TcpDump command to a linux server
        Can save pcap file if pcap_file is provided
        If a local_dir is provided, it will copy back the pcap file to this
        directory

        Example:
            from genie.libs.sdk.libs.utils.tcpdump import TcpDump

            # Local dir should be runinfo as we need to keep all those pcap
            # files with testcase on it.
            pcap_file =  testcasename.pcap
            # local_dir =  runinfo/pcap directory
            t = TcpDump(d, pcap_file = '/tmp/output23.pcap',
                        local_dir='/Users/jeaubin/pcap')
            d.connect()

            t.send('tcpdump -i any udp port 514 -vn')
            # wait some time
            t.stop()
            x = t.parse()
            x[0]['IP']['dst']
    '''
    def __init__(self, device, pcap_file=None, protocol='scp', local_dir=None):
        self.device = device
        self.protocol = protocol
        self.pcap_file = pcap_file
        self.local_dir = local_dir

    def send(self, cmd, attach_pcap=True):
        cmd = '{c}'.format(c=cmd)
        if self.pcap_file and attach_pcap:
            cmd = '{c} -w {pf}'.format(c=cmd, pf=self.pcap_file)
        self.device.send(cmd+'\n')

    def stop(self):
        # Get buffer
        output = self.device.expect(".*")

        # send cntrl+c
        self.device.send('\x03')
        # Bring back the pcap file if any
        if self.pcap_file and self.local_dir:
            # Copy it back to local host

            # Find server
            servers = self.device.testbed.servers

            # Check if there is a self.protocol server
            if self.protocol not in servers:
                raise Exception("'{p}' server missing in the testbed "
                                "yaml file".format(p=self.protocol))

            # Find ip
            ip = servers[self.protocol]['address']
            port = servers[self.protocol].get('custom', {}).get('port', 22)
            local_file = os.path.join(self.local_dir,
                                      os.path.basename(self.pcap_file))

            # Create directory if doesnt exists
            os.makedirs(self.local_dir, exist_ok=True)
            with FileUtils(testbed=self.device.testbed) as futils:
                futils.get_child(self.protocol)
                futils.children[self.protocol].SSH_DEFAULT_PORT = port
                futils.copyfile(
                    source = '{p}://{i}/{path}'.format(p=self.protocol, i=ip,
                                                       path=self.pcap_file),
                    destination = self.local_dir)
        return output

    def parse(self):
        try:
            from scapy.all import rdpcap
        except ImportError:
            raise ImportError('scapy is not installed, please install it by running: '
            'pip install scapy') from None

        local_file = os.path.join(self.local_dir,
                                  os.path.basename(self.pcap_file))
        # Make sure it is not of size 0
        if os.path.isfile(local_file) and os.stat(local_file).st_size:
            return rdpcap(local_file)
