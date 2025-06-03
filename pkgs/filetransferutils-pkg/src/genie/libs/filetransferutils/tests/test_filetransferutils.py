import os
import io
import re
import sys
import stat
import time
import ftplib
import datetime
import logging
import unittest
import tempfile
import subprocess
import importlib
import requests

from unittest.mock import patch, call, Mock, MagicMock, create_autospec
from unittest import skipIf
from pyats.datastructures import AttrDict
from pyats.topology.credentials import Credentials

# Turn on debug to see logs in unit test.
debug = False

if debug:
    logging.basicConfig(level=logging.DEBUG)

from genie.libs.filetransferutils.bases.fileutils import FileUtilsBase as FileUtils
from genie.libs.filetransferutils.bases import fileutils as fileutils_base_module

from genie.libs.filetransferutils import fileutils \
    as fileutils_linux_module

from genie.libs.filetransferutils.bases.fileutils import (
    DEFAULT_CHECK_FILE_DELAY_SECONDS,
    DEFAULT_CHECK_FILE_MAX_TRIES,
    DEFAULT_TIMEOUT_SECONDS,
)

from genie.libs.filetransferutils import fileutils \
    as fu_local_plugin

from genie.libs.filetransferutils.protocols.ftp import fileutils as ftp_fu
from genie.libs.filetransferutils.protocols.scp import fileutils as scp_fu
from genie.libs.filetransferutils.protocols.sftp import fileutils as sftp_fu
from genie.libs.filetransferutils.protocols.tftp import fileutils as tftp_fu

try:
    import paramiko as paramiko_module
    from paramiko import AutoAddPolicy, AuthenticationException, SFTPClient

    import scp as scp_module
    from scp import SCPClient
    paramiko_installed = True
except ImportError:
    paramiko_installed = False


class test_filetransferutils(unittest.TestCase):

    def test_fu_from_device_protocol(self):
        # Instantiate a filetransferutils instance for each os and protocol
        for os_ in ['ios', 'iosxe', 'iosxr', 'nxos']:
            device = AttrDict(os=os_)
            for proto in ['ftp', 'tftp', 'scp', 'sftp', 'http']:
                fu = FileUtils.from_device(device, protocol=proto)
                self.assertIn(
                    'genie.libs.filetransferutils.plugins.{os_}.{proto}.fileutils.FileUtils'
                    .format(os_=os_, proto=proto),
                    str(fu.__class__))
                self.assertEqual(fu.protocol, proto)
                self.assertEqual(fu.os, os_)


class TestBaseFileUtils(unittest.TestCase):

    testbed_1 = AttrDict()
    testbed_1.servers = AttrDict(
        server_name = dict(
            username="myuser", password="mypw", address='1.1.1.1'),
        alt_server2_name = dict(
            server="real_server2_name",
            username="myuser2",
            password="mypw2",
            address='2.2.2.2'),
        ALT_SERVER3_NAME = dict(
            server="REAL_SERVER3_NAME",
            username="myuser3",
            password="mypw3",
            address='3.3.3.3'),
    )

    testbed_2 = AttrDict()
    testbed_2.servers = AttrDict(
        server_name = dict(
            username="myuser", password="mypw", address='1.1.1.1',
            credentials = Credentials(dict(
                default=dict(username='defun', password='defpw'),
                ftp=dict(username='ftpun', password='ftppw'),
                scp=dict(username='scpun', password='scppw'),
            )),
        ),
    )

    testbed_3 = AttrDict()
    testbed_3.servers = AttrDict(
        server_name = dict(
            credentials = Credentials(dict(
                default=dict(username='defun', password='defpw'),
                ftp=dict(username='ftpun', password='ftppw'),
                tftp=dict(username='tftpun', password='tftppw'),
            )),
        ),
    )

    testbed_4 = AttrDict()
    testbed_4.servers = AttrDict(
        server_name = dict(
            username="myuser", password="mypw"),
        alt_server2_name = dict(
            server="1",
            username="myuser2",
            password="mypw2"),
    )

    def test_known_os(self):
        fu = FileUtils()

    def test_unknown_os(self):
        with self.assertRaisesRegex(Exception,
                "Cannot find fileutils plugin for os unknown"):
            fu_unknown = FileUtils(os='unknown')


    def test_create_from_device_implicit_tb(self):
        testbed = AttrDict()
        testbed.setdefault('servers', {}).setdefault('server.domain.com',
            {'username': 'my_user', 'password': 'my_password'})
        device = AttrDict(os='iosxe', testbed=testbed)
        fu = FileUtils.from_device(device, arg1='value1')
        self.assertIn('genie.libs.filetransferutils.plugins.iosxe.fileutils.FileUtils',
            str(fu.__class__))
        self.assertEqual(fu.testbed, testbed)
        self.assertEqual(fu.arg1, 'value1')
        self.assertEqual(fu.os, 'iosxe')


    def test_create_from_device_explicit_tb(self):
        testbed = AttrDict()
        testbed.setdefault('servers', {}).setdefault('server.domain.com',
            {'username': 'my_user', 'password': 'my_password'})
        testbed2 = AttrDict()
        testbed2.setdefault('servers', {}).setdefault('server2.domain.com',
            {'username': 'my_user2', 'password': 'my_password2'})
        device = AttrDict(os='iosxe', testbed=testbed)
        fu = FileUtils.from_device(device, testbed=testbed2, arg1='value1')
        self.assertIn('genie.libs.filetransferutils.plugins.iosxe.fileutils.FileUtils',
            str(fu.__class__))
        self.assertEqual(fu.testbed, testbed)
        self.assertEqual(fu.arg1, 'value1')
        self.assertEqual(fu.os, 'iosxe')


    def test_create_from_no_tb_device_explicit_tb(self):
        testbed2 = AttrDict()
        testbed2.setdefault('servers', {}).setdefault('server2.domain.com',
            {'username': 'my_user2', 'password': 'my_password2'})
        device = AttrDict(os='iosxe')
        fu = FileUtils.from_device(device, testbed=testbed2, arg1='value1')
        self.assertIn('genie.libs.filetransferutils.plugins.iosxe.fileutils.FileUtils',
            str(fu.__class__))
        self.assertEqual(fu.testbed, testbed2)
        self.assertEqual(fu.arg1, 'value1')
        self.assertEqual(fu.os, 'iosxe')


    def test_create_from_no_tb_device_no_tb(self):
        device = AttrDict(os='iosxe')
        fu = FileUtils.from_device(device, arg1='value1')
        self.assertIn('genie.libs.filetransferutils.plugins.iosxe.fileutils.FileUtils',
            str(fu.__class__))
        self.assertEqual(fu.testbed, None)
        self.assertEqual(fu.arg1, 'value1')
        self.assertEqual(fu.os, 'iosxe')


    def test_unknown_protocol(self):
        with self.assertRaisesRegex(Exception,
                "The protocol unknown is not supported."):
            fu = FileUtils()
            fu_unknown = fu.get_child('unknown')


    def test_create_child(self):
        fu = FileUtils()
        fu_ftp = fu.get_child('ftp')
        self.assertIs(fu_ftp.parent, fu)


    def test_child_cache(self):
        fu = FileUtils()
        fu_ftp = fu.get_child('ftp')
        fu_ftp2 = fu.get_child('ftp')
        self.assertIs(fu_ftp, fu_ftp2)

        fu.remove_child('ftp')
        fu_ftp = fu.get_child('ftp')
        self.assertIsNot(fu_ftp, fu_ftp2)


    def test_context_mgr(self):
        fu = FileUtils()
        ftp_child_mock = create_autospec(
            ftp_fu.FileUtils, instance=True)
        fu.children.update(dict(ftp=ftp_child_mock))
        with fu:
            pass
        expected_mock_calls = [call.close(),]
        self.assertTrue(ftp_child_mock.mock_calls, expected_mock_calls)


    def test_parse_local_url(self):
        fu = FileUtils()
        self.assertTrue(fu.is_local("file:///path/to/file"))
        self.assertTrue(fu.is_local("/path/to/file"))
        self.assertFalse(fu.is_local("ftp://server:1234/path/to/file"))


    def test_parse_remote_url(self):
        fu = FileUtils()
        self.assertFalse(fu.is_remote("file:///path/to/file"))
        self.assertFalse(fu.is_remote("/path/to/file"))
        self.assertTrue(fu.is_remote("ftp://server:1234/path/to/file"))


    def test_parse_protocol_url(self):
        fu = FileUtils()
        self.assertEqual(fu.get_protocol("file:///path/to/file"), "file")
        self.assertEqual(fu.get_protocol("/path/to/file"), None)
        self.assertEqual(fu.get_protocol(
            "ftp://server:1234/path/to/file"), "ftp")
        self.assertEqual(fu.get_protocol(
            '/path/to/file',
            "ftp://server:1234/path/to/file"), "ftp")


    def test_get_server_block_by_name(self):
        fu = FileUtils(testbed=self.testbed_1)
        tb = fu.get_server_block("server_name")
        self.assertEqual(tb, {
            'username': 'myuser', 'password': 'mypw', 'address': '1.1.1.1',
        })


    def test_get_server_block_unknown_name(self):
        fu = FileUtils(testbed=self.testbed_1)
        tb = fu.get_server_block("unknown_server_name")
        self.assertEqual(tb, {})


    def test_get_server_block_number(self):
        server_block = FileUtils(testbed=self.testbed_4)
        server_block.get_local_ip = MagicMock(return_value="1.1.1.1")
        tb = server_block.get_server_block("1")
        self.assertEqual(tb, {
            'username': 'myuser2', 'password': 'mypw2',
            'server': '1',
        })


    def test_get_server_block_by_alt_name(self):
        fu = FileUtils(testbed=self.testbed_1)
        tb = fu.get_server_block("alt_server2_name")
        self.assertEqual(tb, {
            'username': 'myuser2', 'password': 'mypw2', 'address': '2.2.2.2',
            'server': 'real_server2_name',
        })
        # Test casefold
        tb = fu.get_server_block("alt_server3_name")
        self.assertEqual(tb, {
            'username': 'myuser3', 'password': 'mypw3', 'address': '3.3.3.3',
            'server': 'REAL_SERVER3_NAME',
        })


    def test_get_server_block_by_address(self):
        fu = FileUtils(testbed=self.testbed_1)
        tb = fu.get_server_block("2.2.2.2")
        self.assertEqual(tb, {
            'username': 'myuser2', 'password': 'mypw2', 'address': '2.2.2.2',
            'server': 'real_server2_name',
        })


    def test_get_server_block_by_server_name(self):
        fu = FileUtils(testbed=self.testbed_1)
        tb = fu.get_server_block("real_server2_name")
        self.assertEqual(tb, {
            'username': 'myuser2', 'password': 'mypw2', 'address': '2.2.2.2',
            'server': 'real_server2_name',
        })
        # Test casefold
        tb = fu.get_server_block("real_server3_name")
        self.assertEqual(tb, {
            'username': 'myuser3', 'password': 'mypw3', 'address': '3.3.3.3',
            'server': 'REAL_SERVER3_NAME',
        })


    def test_get_auth_by_server_name(self):
        fu = FileUtils(testbed=self.testbed_1)
        username, password = fu.get_auth("real_server2_name")
        self.assertEqual(username, "myuser2")
        self.assertEqual(password, "mypw2")


    def test_get_auth_legacy_with_credentials(self):
        """ Test that credentials (if provided) trump legacy auth. """
        fu = FileUtils(testbed=self.testbed_2)

        username, password = fu.get_auth("server_name")
        self.assertEqual(username, "defun")
        self.assertEqual(password, "defpw")

        fu_ftp = fu.get_child('ftp')
        username, password = fu_ftp.get_auth("server_name")
        self.assertEqual(username, "ftpun")
        self.assertEqual(password, "ftppw")


    def test_get_auth_credentials(self):
        fu = FileUtils(testbed=self.testbed_3)

        username, password = fu.get_auth("server_name")
        self.assertEqual(username, "defun")
        self.assertEqual(password, "defpw")

        fu_ftp = fu.get_child('ftp')
        username, password = fu_ftp.get_auth("server_name")
        self.assertEqual(username, "ftpun")
        self.assertEqual(password, "ftppw")


    def test_get_auth_credentials_dotted_abstraction_key(self):
        fu = FileUtils(testbed=self.testbed_3)
        fu_ftp = fu.get_child('tftp')
        username, password = fu_ftp.get_auth("server_name")
        self.assertEqual(username, "tftpun")
        self.assertEqual(password, "tftppw")


    @patch.object(fileutils_base_module, 'time')
    def test_check_file_exception_no_stability(self, time_mock):
        fu = FileUtils(testbed=self.testbed_1)
        with self.assertRaisesRegex(Exception,
                re.escape("Failure to check existence and length of file "
                "ftp://server:1234/path/to/file.")):
            with patch.object(fu, 'stat') as stat_mock:
                stat_mock.side_effect = Exception("Boom, stat failed.")
                fu.checkfile("ftp://server:1234/path/to/file")

        expected_sleep_calls=[call(DEFAULT_CHECK_FILE_DELAY_SECONDS) \
            for count in range(DEFAULT_CHECK_FILE_MAX_TRIES)]
        self.assertEqual(time_mock.sleep.mock_calls, expected_sleep_calls)


    @patch.object(fileutils_base_module, 'time')
    def test_check_file_exception_stability(self, time_mock):
        fu = FileUtils(testbed=self.testbed_1)
        with self.assertLogs('genie.libs.filetransferutils.bases.fileutils',
                logging.WARNING) as cm:
            with self.assertRaisesRegex(Exception,
                    re.escape("Failure to check existence and length of file "
                    "ftp://server:1234/path/to/file.")):
                with patch.object(fu, 'stat') as stat_mock:
                    stat_mock.side_effect = Exception("Boom, stat failed.")
                    fu.checkfile(
                        "ftp://server:1234/path/to/file",
                        check_stability=True)
        expected_log = \
            "WARNING:genie.libs.filetransferutils.bases.fileutils:"\
            "File stat error : Boom, stat failed."
        self.assertEqual(cm.output, \
            [expected_log] * DEFAULT_CHECK_FILE_MAX_TRIES)

        expected_sleep_calls=[call(DEFAULT_CHECK_FILE_DELAY_SECONDS) \
            for count in range(DEFAULT_CHECK_FILE_MAX_TRIES)]
        self.assertEqual(time_mock.sleep.mock_calls, expected_sleep_calls)


    @patch.object(fileutils_base_module, 'time')
    def test_check_file_exception_good_no_stability(self, time_mock):
        fu = FileUtils(testbed=self.testbed_1)
        stat_return = AttrDict(st_size = 123)
        retry_range = range(DEFAULT_CHECK_FILE_MAX_TRIES)
        with patch.object(fu, 'stat') as stat_mock:
            stat_mock.side_effect = [
                Exception("Boom, stat failed.") if count == 0 \
                else stat_return for count in retry_range]
            fu.checkfile("ftp://server:1234/path/to/file")

        expected_sleep_calls=[call(DEFAULT_CHECK_FILE_DELAY_SECONDS),]
        self.assertEqual(time_mock.sleep.mock_calls, expected_sleep_calls)


    @patch.object(fileutils_base_module, 'time')
    def test_check_file_exception_good_stability(self, time_mock):
        fu = FileUtils(testbed=self.testbed_1)
        retry_range = range(DEFAULT_CHECK_FILE_MAX_TRIES)
        stat_return = AttrDict(st_size = 123)
        with patch.object(fu, 'stat') as stat_mock:
            stat_mock.side_effect = [
                Exception("Boom, stat failed.") if count == 0 \
                else stat_return for count in retry_range]
            fu.checkfile(
                "ftp://server:1234/path/to/file",
                check_stability=True)

        expected_sleep_calls=[call(DEFAULT_CHECK_FILE_DELAY_SECONDS) \
            for count in range(DEFAULT_CHECK_FILE_MAX_TRIES)]
        self.assertEqual(time_mock.sleep.mock_calls, expected_sleep_calls)


    @patch.object(fileutils_base_module, 'time')
    def test_check_file_exception_unstable(self, time_mock):
        fu = FileUtils(testbed=self.testbed_1)
        retry_range = range(DEFAULT_CHECK_FILE_MAX_TRIES)
        with self.assertRaisesRegex(Exception,
                re.escape("The length of file ftp://server:1234/path/to/file "
                    "is not stable.")):
            with patch.object(fu, 'stat') as stat_mock:
                stat_mock.side_effect = [
                    Exception("Boom, stat failed.") if count == 0 \
                    else AttrDict(st_size = count) for count in retry_range]
                fu.checkfile(
                    "ftp://server:1234/path/to/file",
                    check_stability=True)

        expected_sleep_calls=[call(DEFAULT_CHECK_FILE_DELAY_SECONDS) \
            for count in range(DEFAULT_CHECK_FILE_MAX_TRIES)]
        self.assertEqual(time_mock.sleep.mock_calls, expected_sleep_calls)


    @patch.object(fileutils_base_module, 'time')
    def test_check_file_unstable(self, time_mock):
        fu = FileUtils(testbed=self.testbed_1)
        retry_range = range(DEFAULT_CHECK_FILE_MAX_TRIES)
        with self.assertRaisesRegex(Exception,
                re.escape("The length of file ftp://server:1234/path/to/file "
                    "is not stable.")):
            with patch.object(fu, 'stat') as stat_mock:
                stat_mock.side_effect = [
                    AttrDict(st_size = count) for count in retry_range]
                fu.checkfile(
                    "ftp://server:1234/path/to/file",
                    check_stability=True)

        expected_sleep_calls=[call(DEFAULT_CHECK_FILE_DELAY_SECONDS) \
            for count in range(DEFAULT_CHECK_FILE_MAX_TRIES)]
        self.assertEqual(time_mock.sleep.mock_calls, expected_sleep_calls)


    @patch.object(fileutils_base_module, 'time')
    def test_check_file_unstable_then_stable(self, time_mock):
        fu = FileUtils(testbed=self.testbed_1)
        retry_range = range(DEFAULT_CHECK_FILE_MAX_TRIES)
        with patch.object(fu, 'stat') as stat_mock:
            stat_mock.side_effect = [
                AttrDict(st_size = count) if count in retry_range[:-2] \
                else AttrDict(st_size = 123) for count in retry_range]
            fu.checkfile(
                "ftp://server:1234/path/to/file",
                check_stability=True)

        expected_sleep_calls=[call(DEFAULT_CHECK_FILE_DELAY_SECONDS) \
            for count in range(DEFAULT_CHECK_FILE_MAX_TRIES)]
        self.assertEqual(time_mock.sleep.mock_calls, expected_sleep_calls)

    def test_validate_and_update_url(self):
        fu = FileUtils(testbed=self.testbed_2)
        self.assertEqual('ftp://ftpun:ftppw@1.1.1.1',
                         fu.validate_and_update_url('ftp://1.1.1.1'))
        self.assertEqual('scp://scpun@1.1.1.1',
                         fu.validate_and_update_url('scp://1.1.1.1'))
        self.assertEqual('1.1.1.1',
                         fu.validate_and_update_url('1.1.1.1'))

class TestBaseLinuxFileUtils(unittest.TestCase):

    # Specified with server key and explicit address
    testbed_1 = AttrDict()
    testbed_1.servers = AttrDict(
        server_alias = dict(
            server='server_name', address='1.1.1.1',
            username="myuser", password="mypw"),
    )


    def test_validate_url_good_address(self):
        fu = FileUtils(testbed=self.testbed_1)
        url = 'ftp://1.1.1.1/path/to/stuff'
        hostname, port, path = fu.validate_and_parse_url(url, 'mymethod')
        self.assertEqual(hostname, '1.1.1.1')
        self.assertEqual(port, None)
        self.assertEqual(path, "/path/to/stuff")


    @patch.object(subprocess, 'check_call')
    def test_validate_url_undeclared_address(self, check_call):
        """ Test that undeclared address is allowed as a server name.
        The assumption is that transfers are only possible via local auth
        and scp/sftp protocols, since no auth can be obtained from the
        testbed server block.
        """
        fu = FileUtils(testbed=self.testbed_1)
        url = 'ftp://2.2.2.2/path/to/stuff'
        hostname, port, path = fu.validate_and_parse_url(url, 'mymethod')
        self.assertEqual(hostname, '2.2.2.2')
        self.assertEqual(port, None)
        self.assertEqual(path, "/path/to/stuff")



class TestBaseLinuxFtpFileUtils(unittest.TestCase):

    # Specified without server key
    testbed_1 = AttrDict()
    testbed_1.servers = AttrDict(
        server_name = dict(
            username="myuser", password="mypw", address='1.1.1.1'),
    )

    # Specified with server key but without explicit address
    testbed_2 = AttrDict()
    testbed_2.servers = AttrDict(
        server_alias = dict(
            server='server_name',
            username="myuser", password="mypw"),
    )

    # Specified with server key and explicit address
    testbed_3 = AttrDict()
    testbed_3.servers = AttrDict(
        server_alias = dict(
            server='server_name', address='1.1.1.1',
            username="myuser", password="mypw"),
    )

    # Specified with server key and multiple address
    testbed_4 = AttrDict()
    testbed_4.servers = AttrDict(
        server_alias = dict(
            server='server_name', address=['1.1.1.1', '2.2.2.2'],
            username="myuser", password="mypw"),
    )

    @patch.object(subprocess, 'check_call')
    def test_copyfile_local_remote(self, check_call):
        fu = FileUtils(testbed=self.testbed_1)

        with tempfile.NamedTemporaryFile() as fp:
            lcl_file = fp.name
            with patch.object(ftp_fu , 'FTP', autospec=True) \
                    as ftp_mock:
                ftp_sess_mock = create_autospec(ftplib.FTP, instance=True)
                ftp_mock.return_value = ftp_sess_mock
                ftp_sess_enter_mock = create_autospec(
                    ftplib.FTP, instance=True)
                ftp_sess_mock.__enter__.return_value = ftp_sess_enter_mock
                fu.copyfile('file://{lcl_file_path}'.format(
                    lcl_file_path = lcl_file),
                   'ftp://server_name/path/to/remote/file')
                expected_mock_calls = [
                 call(),
                 call().__enter__(),
                 call().__enter__().connect(
                    port=0, timeout=1200, host='1.1.1.1'),
                 call().__enter__().login(user='myuser', passwd='mypw'),
                ]
                self.assertEqual(ftp_mock.mock_calls[:4], expected_mock_calls)
                actual_call = str(ftp_mock.mock_calls[4])
                self.assertRegex(actual_call, "call.*__enter__.*storbinary")
                self.assertRegex(actual_call, "callback.*copyfile.*upload_cb")
                self.assertRegex(actual_call, "cmd='STOR path/to/remote/file'")
                self.assertRegex(actual_call, "fp.*name='{lcl_file}'".\
                    format(lcl_file = lcl_file))
                self.assertEqual(ftp_mock.mock_calls[5],
                    call().__exit__(None, None, None))

    @patch.object(subprocess, 'check_call')
    def test_copyfile_local_remote_no_strip_leading_slash(self, check_call):
        fu = FileUtils(testbed=self.testbed_1)

        with tempfile.NamedTemporaryFile() as fp:
            lcl_file = fp.name
            with patch.object(ftp_fu , 'FTP', autospec=True) \
                    as ftp_mock:
                ftp_sess_mock = create_autospec(ftplib.FTP, instance=True)
                ftp_mock.return_value = ftp_sess_mock
                ftp_sess_enter_mock = create_autospec(
                    ftplib.FTP, instance=True)
                ftp_sess_mock.__enter__.return_value = ftp_sess_enter_mock
                fu.copyfile('file://{lcl_file_path}'.format(
                    lcl_file_path = lcl_file),
                   'ftp://server_name/path/to/remote/file',
                   strip_leading_slash=False)
                expected_mock_calls = [
                 call(),
                 call().__enter__(),
                 call().__enter__().connect(
                    port=0, timeout=1200, host='1.1.1.1'),
                 call().__enter__().login(user='myuser', passwd='mypw'),
                ]
                self.assertEqual(ftp_mock.mock_calls[:4], expected_mock_calls)
                actual_call = str(ftp_mock.mock_calls[4])
                self.assertRegex(actual_call, "call.*__enter__.*storbinary")
                self.assertRegex(actual_call, "callback.*copyfile.*upload_cb")
                self.assertRegex(actual_call,
                    "cmd='STOR /path/to/remote/file'")
                self.assertRegex(actual_call, "fp.*name='{lcl_file}'".\
                    format(lcl_file = lcl_file))
                self.assertEqual(ftp_mock.mock_calls[5],
                    call().__exit__(None, None, None))


    def test_copyfile_relative_local_remote1(self):
        """ Test relative local file with alphanumeric first character.
        Local filename has no preceding slash, so cannot specify file:// prefix.
        """
        fu = FileUtils(testbed=self.testbed_1)

        def mocked_expanduser(filename, *args, **kwargs):
            return filename

        with tempfile.NamedTemporaryFile() as fp:
            lcl_file = fp.name
            lcl_file_dirname = os.path.dirname(fp.name)
            lcl_file_basename = os.path.basename(fp.name)
            with patch.object(ftp_fu, 'FTP', autospec=True) \
                    as ftp_mock:
                with patch.object(fu_local_plugin , 'os', autospec=True) \
                        as os_mock:
                    os_path_expanduser_mock = Mock(
                        side_effect=mocked_expanduser)

                    os_path_abspath_mock = Mock(return_value=lcl_file)
                    os_path_mock = Mock(
                        abspath=os_path_abspath_mock,
                        expanduser=os_path_expanduser_mock)
                    os_mock.path = os_path_mock
                    ftp_sess_mock = create_autospec(ftplib.FTP, instance=True)
                    ftp_mock.return_value = ftp_sess_mock
                    ftp_sess_enter_mock = create_autospec(
                        ftplib.FTP, instance=True)
                    ftp_sess_mock.__enter__.return_value = ftp_sess_enter_mock
                    fu.copyfile('{lcl_file_rel_path}'.format(
                        lcl_file_rel_path = lcl_file_basename),
                       'ftp://server_name/path/to/remote/file')
                    expected_mock_calls = [
                     call(),
                     call().__enter__(),
                     call().__enter__().connect(
                        port=0, timeout=1200, host='1.1.1.1'),
                     call().__enter__().login(user='myuser', passwd='mypw'),
                    ]
                    self.assertEqual(
                        ftp_mock.mock_calls[:4], expected_mock_calls)

                    actual_call = str(ftp_mock.mock_calls[4])
                    self.assertRegex(actual_call, "call.*__enter__.*storbinary")

                    self.assertRegex(
                        actual_call, "callback.*copyfile.*upload_cb")

                    self.assertRegex(
                        actual_call, "cmd='STOR path/to/remote/file'")

                    self.assertRegex(actual_call, "fp.*name='{lcl_file}'".\
                        format(lcl_file = lcl_file))
                    self.assertEqual(ftp_mock.mock_calls[5],
                        call().__exit__(None, None, None))
                    self.assertEqual(os_path_abspath_mock.mock_calls,
                        [call(lcl_file_basename)])


    def test_copyfile_relative_local_remote2(self):
        """ Test relative local file with single dotted first character.
        Local filename has no preceding slash, so cannot specify file:// prefix.
        """
        fu = FileUtils(testbed=self.testbed_1)

        def mocked_expanduser(filename, *args, **kwargs):
            return filename

        with tempfile.NamedTemporaryFile() as fp:
            lcl_file = fp.name
            lcl_file_dirname = os.path.dirname(fp.name)
            lcl_file_basename = os.path.basename(fp.name)
            with patch.object(ftp_fu, 'FTP', autospec=True) \
                    as ftp_mock:
                with patch.object(fu_local_plugin , 'os', autospec=True) \
                        as os_mock:
                    os_path_expanduser_mock = Mock(
                        side_effect=mocked_expanduser)
                    os_path_abspath_mock = Mock(return_value=lcl_file)
                    os_path_mock = Mock(
                        abspath=os_path_abspath_mock,
                        expanduser=os_path_expanduser_mock)
                    os_mock.path = os_path_mock
                    ftp_sess_mock = create_autospec(ftplib.FTP, instance=True)
                    ftp_mock.return_value = ftp_sess_mock
                    ftp_sess_enter_mock = create_autospec(
                        ftplib.FTP, instance=True)
                    ftp_sess_mock.__enter__.return_value = ftp_sess_enter_mock
                    fu.copyfile('./{lcl_file_rel_path}'.format(
                        lcl_file_rel_path = lcl_file_basename),
                       'ftp://server_name/path/to/remote/file')
                    expected_mock_calls = [
                     call(),
                     call().__enter__(),
                     call().__enter__().connect(
                        port=0, timeout=1200, host='1.1.1.1'),
                     call().__enter__().login(user='myuser', passwd='mypw'),
                    ]
                    self.assertEqual(
                        ftp_mock.mock_calls[:4], expected_mock_calls)

                    actual_call = str(ftp_mock.mock_calls[4])
                    self.assertRegex(actual_call, "call.*__enter__.*storbinary")

                    self.assertRegex(
                        actual_call, "callback.*copyfile.*upload_cb")

                    self.assertRegex(
                        actual_call, "cmd='STOR path/to/remote/file'")

                    self.assertRegex(actual_call, "fp.*name='{lcl_file}'".\
                        format(lcl_file = lcl_file))
                    self.assertEqual(ftp_mock.mock_calls[5],
                        call().__exit__(None, None, None))
                    self.assertEqual(os_path_abspath_mock.mock_calls,
                        [call('./{lcl_file}'.format(
                            lcl_file=lcl_file_basename))])


    def test_copyfile_relative_local_remote3(self):
        """ Test local file relative to calling user's home directory.
        Local filename has no preceding slash, so cannot specify file:// prefix.
        """
        fu = FileUtils(testbed=self.testbed_1)

        with tempfile.NamedTemporaryFile() as fp:
            lcl_file = fp.name
            lcl_file_dirname = os.path.dirname(fp.name)
            lcl_file_basename = os.path.basename(fp.name)
            with patch.object(ftp_fu, 'FTP', autospec=True) \
                    as ftp_mock:
                with patch.object(fu_local_plugin , 'os', autospec=True) \
                        as os_mock:
                    os_path_expanduser_mock = Mock(return_value=lcl_file)
                    os_path_abspath_mock = Mock(return_value=lcl_file)
                    os_path_mock = Mock(
                        abspath=os_path_abspath_mock,
                        expanduser=os_path_expanduser_mock)
                    os_mock.path = os_path_mock
                    ftp_sess_mock = create_autospec(ftplib.FTP, instance=True)
                    ftp_mock.return_value = ftp_sess_mock
                    ftp_sess_enter_mock = create_autospec(
                        ftplib.FTP, instance=True)
                    ftp_sess_mock.__enter__.return_value = ftp_sess_enter_mock
                    fu.copyfile('~/{lcl_file_rel_path}'.format(
                        lcl_file_rel_path = lcl_file_basename),
                       'ftp://server_name/path/to/remote/file')
                    expected_mock_calls = [
                     call(),
                     call().__enter__(),
                     call().__enter__().connect(
                        port=0, timeout=1200, host='1.1.1.1'),
                     call().__enter__().login(user='myuser', passwd='mypw'),
                    ]
                    self.assertEqual(
                        ftp_mock.mock_calls[:4], expected_mock_calls)
                    actual_call = str(ftp_mock.mock_calls[4])
                    self.assertRegex(actual_call, "call.*__enter__.*storbinary")

                    self.assertRegex(
                        actual_call, "callback.*copyfile.*upload_cb")

                    self.assertRegex(
                        actual_call, "cmd='STOR path/to/remote/file'")

                    self.assertRegex(actual_call, "fp.*name='{lcl_file}'".\
                        format(lcl_file = lcl_file))
                    self.assertEqual(ftp_mock.mock_calls[5],
                        call().__exit__(None, None, None))
                    self.assertEqual(os_path_expanduser_mock.mock_calls,
                        [call('~/{lcl_file}'.format(
                            lcl_file=lcl_file_basename))])
                    self.assertEqual(os_path_abspath_mock.mock_calls,
                        [call('{lcl_file}'.format(
                            lcl_file=lcl_file))])

    @patch.object(subprocess, 'check_call')
    def test_copyfile_local_remote_asalias_no_explicit_ip(self, check_call):
        fu = FileUtils(testbed=self.testbed_2)

        with tempfile.NamedTemporaryFile() as fp:
            lcl_file = fp.name
            with patch.object(ftp_fu , 'FTP', autospec=True) \
                    as ftp_mock:
                ftp_sess_mock = create_autospec(ftplib.FTP, instance=True)
                ftp_mock.return_value = ftp_sess_mock
                ftp_sess_enter_mock = create_autospec(
                    ftplib.FTP, instance=True)
                ftp_sess_mock.__enter__.return_value = ftp_sess_enter_mock
                fu.copyfile('file://{lcl_file_path}'.format(
                    lcl_file_path = lcl_file),
                   'ftp://server_alias/path/to/remote/file')
                expected_mock_calls = [
                 call(),
                 call().__enter__(),
                 call().__enter__().connect(
                    port=0, timeout=1200, host='server_name'),
                 call().__enter__().login(user='myuser', passwd='mypw'),
                ]
                self.assertEqual(ftp_mock.mock_calls[:4], expected_mock_calls)
                actual_call = str(ftp_mock.mock_calls[4])
                self.assertRegex(actual_call, "call.*__enter__.*storbinary")
                self.assertRegex(actual_call, "callback.*copyfile.*upload_cb")
                self.assertRegex(actual_call, "cmd='STOR path/to/remote/file'")
                self.assertRegex(actual_call, "fp.*name='{lcl_file}'".\
                    format(lcl_file = lcl_file))
                self.assertEqual(ftp_mock.mock_calls[5],
                    call().__exit__(None, None, None))

    @patch.object(subprocess, 'check_call')
    def test_copyfile_local_remote_asalias_with_explicit_ip(self, check_call):
        fu = FileUtils(testbed=self.testbed_3)

        with tempfile.NamedTemporaryFile() as fp:
            lcl_file = fp.name
            with patch.object(ftp_fu , 'FTP', autospec=True) \
                    as ftp_mock:
                ftp_sess_mock = create_autospec(ftplib.FTP, instance=True)
                ftp_mock.return_value = ftp_sess_mock
                ftp_sess_enter_mock = create_autospec(
                    ftplib.FTP, instance=True)
                ftp_sess_mock.__enter__.return_value = ftp_sess_enter_mock
                fu.copyfile('file://{lcl_file_path}'.format(
                    lcl_file_path = lcl_file),
                   'ftp://server_alias/path/to/remote/file')
                expected_mock_calls = [
                 call(),
                 call().__enter__(),
                 call().__enter__().connect(
                    port=0, timeout=1200, host='1.1.1.1'),
                 call().__enter__().login(user='myuser', passwd='mypw'),
                ]
                self.assertEqual(ftp_mock.mock_calls[:4], expected_mock_calls)
                actual_call = str(ftp_mock.mock_calls[4])
                self.assertRegex(actual_call, "call.*__enter__.*storbinary")
                self.assertRegex(actual_call, "callback.*copyfile.*upload_cb")
                self.assertRegex(actual_call, "cmd='STOR path/to/remote/file'")
                self.assertRegex(actual_call, "fp.*name='{lcl_file}'".\
                    format(lcl_file = lcl_file))
                self.assertEqual(ftp_mock.mock_calls[5],
                    call().__exit__(None, None, None))

    @patch.object(subprocess, 'check_call')
    def test_copyfile_remote_local(self, check_call):
        fu = FileUtils(testbed=self.testbed_1)

        with tempfile.NamedTemporaryFile() as fp:
            lcl_file = fp.name
            with patch.object(ftp_fu , 'FTP', autospec=True) \
                    as ftp_mock:
                ftp_sess_mock = create_autospec(ftplib.FTP, instance=True)
                ftp_mock.return_value = ftp_sess_mock
                ftp_sess_enter_mock = create_autospec(
                    ftplib.FTP, instance=True)
                ftp_sess_mock.__enter__.return_value = ftp_sess_enter_mock
                fu.copyfile(
                   'ftp://server_name/path/to/remote/file',
                    'file://{lcl_file_path}'.format(
                    lcl_file_path = lcl_file)
                )
                expected_mock_calls = [
                 call(),
                 call().__enter__(),
                 call().__enter__().connect(
                    port=0, timeout=fu.DEFAULT_COPY_TIMEOUT_SECONDS,
                    host='1.1.1.1'),
                 call().__enter__().login(user='myuser', passwd='mypw'),
                ]
                self.assertEqual(ftp_mock.mock_calls[:4], expected_mock_calls)
                actual_call = str(ftp_mock.mock_calls[4])
                self.assertRegex(actual_call, "call.*__enter__.*retrbinary")
                self.assertRegex(actual_call,
                    "callback.*copyfile.*download_cb")
                self.assertRegex(actual_call, "cmd='RETR path/to/remote/file'")
                self.assertEqual(ftp_mock.mock_calls[5],
                    call().__exit__(None, None, None))

    @patch.object(subprocess, 'check_call')
    def test_copyfile_remote_local_no_strip_leading_slash(self, check_call):
        fu = FileUtils(testbed=self.testbed_1)

        with tempfile.NamedTemporaryFile() as fp:
            lcl_file = fp.name
            with patch.object(ftp_fu , 'FTP', autospec=True) \
                    as ftp_mock:
                ftp_sess_mock = create_autospec(ftplib.FTP, instance=True)
                ftp_mock.return_value = ftp_sess_mock
                ftp_sess_enter_mock = create_autospec(
                    ftplib.FTP, instance=True)
                ftp_sess_mock.__enter__.return_value = ftp_sess_enter_mock
                fu.copyfile(
                   'ftp://server_name/path/to/remote/file',
                    'file://{lcl_file_path}'.format(
                    lcl_file_path = lcl_file,
                    ),
                    strip_leading_slash=False
                )
                expected_mock_calls = [
                 call(),
                 call().__enter__(),
                 call().__enter__().connect(
                    port=0, timeout=fu.DEFAULT_COPY_TIMEOUT_SECONDS,
                    host='1.1.1.1'),
                 call().__enter__().login(user='myuser', passwd='mypw'),
                ]
                self.assertEqual(ftp_mock.mock_calls[:4], expected_mock_calls)
                actual_call = str(ftp_mock.mock_calls[4])
                self.assertRegex(actual_call, "call.*__enter__.*retrbinary")
                self.assertRegex(actual_call,
                    "callback.*copyfile.*download_cb")
                self.assertRegex(actual_call,
                    "cmd='RETR /path/to/remote/file'")
                self.assertEqual(ftp_mock.mock_calls[5],
                    call().__exit__(None, None, None))

    @patch.object(subprocess, 'check_call')
    def test_dir_remote(self, check_call):
        """ Test dir against server top level directory. """
        fu = FileUtils(testbed=self.testbed_1)

        with patch.object(ftp_fu , 'FTP', autospec=True) as ftp_mock:
            ftp_sess_mock = create_autospec(ftplib.FTP, instance=True)
            ftp_mock.return_value = ftp_sess_mock
            ftp_sess_enter_mock = create_autospec(ftplib.FTP, instance=True)
            ftp_sess_mock.__enter__.return_value = ftp_sess_enter_mock
            ftp_sess_enter_mock.nlst.return_value = ['list', 'of', 'files',]
            result = fu.dir( 'ftp://server_name/')
            expected_mock_calls = [
             call(),
             call().__enter__(),
             call().__enter__().connect(port=0,
                timeout=fu.DEFAULT_TIMEOUT_SECONDS, host='1.1.1.1'),
             call().__enter__().login(user='myuser', passwd='mypw'),
            ]
            self.assertEqual(ftp_mock.mock_calls[:4], expected_mock_calls)
            actual_call = str(ftp_mock.mock_calls[4])
            self.assertRegex(actual_call,
                re.escape("call().__enter__().nlst('')"))
            self.assertEqual(ftp_mock.mock_calls[5],
                call().__exit__(None, None, None))
            self.assertEqual(result, [
                'ftp://server_name/list',
                'ftp://server_name/of',
                'ftp://server_name/files',
            ])

    @patch.object(subprocess, 'check_call')
    def test_dir_remote_no_leading_slash(self, check_call):
        """ Test dir against server top level directory. """
        fu = FileUtils(testbed=self.testbed_1)

        with patch.object(ftp_fu , 'FTP', autospec=True) as ftp_mock:
            ftp_sess_mock = create_autospec(ftplib.FTP, instance=True)
            ftp_mock.return_value = ftp_sess_mock
            ftp_sess_enter_mock = create_autospec(ftplib.FTP, instance=True)
            ftp_sess_mock.__enter__.return_value = ftp_sess_enter_mock
            ftp_sess_enter_mock.nlst.return_value = ['list', 'of', 'files',]
            result = fu.dir( 'ftp://server_name/', strip_leading_slash=False)
            expected_mock_calls = [
             call(),
             call().__enter__(),
             call().__enter__().connect(port=0,
                timeout=fu.DEFAULT_TIMEOUT_SECONDS, host='1.1.1.1'),
             call().__enter__().login(user='myuser', passwd='mypw'),
            ]
            self.assertEqual(ftp_mock.mock_calls[:4], expected_mock_calls)
            actual_call = str(ftp_mock.mock_calls[4])
            self.assertRegex(actual_call,
                re.escape("call().__enter__().nlst('/')"))
            self.assertEqual(ftp_mock.mock_calls[5],
                call().__exit__(None, None, None))
            self.assertEqual(result, [
                'ftp://server_name/list',
                'ftp://server_name/of',
                'ftp://server_name/files',
            ])

    @patch.object(subprocess, 'check_call')
    def test_dir_remote2(self, check_call):
        """ Test dir against server that doesn't quote leading directories. """
        fu = FileUtils(testbed=self.testbed_1)

        with patch.object(ftp_fu , 'FTP', autospec=True) as ftp_mock:
            ftp_sess_mock = create_autospec(ftplib.FTP, instance=True)
            ftp_mock.return_value = ftp_sess_mock
            ftp_sess_enter_mock = create_autospec(ftplib.FTP, instance=True)
            ftp_sess_mock.__enter__.return_value = ftp_sess_enter_mock
            ftp_sess_enter_mock.nlst.return_value = ['list', 'of', 'files',]
            result = fu.dir( 'ftp://server_name/path/to/remote/file')
            expected_mock_calls = [
             call(),
             call().__enter__(),
             call().__enter__().connect(port=0,
                timeout=fu.DEFAULT_TIMEOUT_SECONDS, host='1.1.1.1'),
             call().__enter__().login(user='myuser', passwd='mypw'),
            ]
            self.assertEqual(ftp_mock.mock_calls[:4], expected_mock_calls)
            actual_call = str(ftp_mock.mock_calls[4])
            self.assertRegex(actual_call,
                re.escape("call().__enter__().nlst('path/to/remote/file')"))
            self.assertEqual(ftp_mock.mock_calls[5],
                call().__exit__(None, None, None))
            self.assertEqual(result, [
                'ftp://server_name/path/to/remote/file/list',
                'ftp://server_name/path/to/remote/file/of',
                'ftp://server_name/path/to/remote/file/files',
            ])

    @patch.object(subprocess, 'check_call')
    def test_dir_remote3(self, check_call):
        """ Test dir against server that quotes leading directories. """
        fu = FileUtils(testbed=self.testbed_1)

        with patch.object(ftp_fu , 'FTP', autospec=True) as ftp_mock:
            ftp_sess_mock = create_autospec(ftplib.FTP, instance=True)
            ftp_mock.return_value = ftp_sess_mock
            ftp_sess_enter_mock = create_autospec(ftplib.FTP, instance=True)
            ftp_sess_mock.__enter__.return_value = ftp_sess_enter_mock
            ftp_sess_enter_mock.nlst.return_value = [
                'path/to/remote/file/list',
                '/path/to/remote/file/of',
                '/path/to/remote/file/files',]
            result = fu.dir( 'ftp://server_name/path/to/remote/file')
            expected_mock_calls = [
             call(),
             call().__enter__(),
             call().__enter__().connect(port=0,
                timeout=fu.DEFAULT_TIMEOUT_SECONDS, host='1.1.1.1'),
             call().__enter__().login(user='myuser', passwd='mypw'),
            ]
            self.assertEqual(ftp_mock.mock_calls[:4], expected_mock_calls)
            actual_call = str(ftp_mock.mock_calls[4])
            self.assertRegex(actual_call,
                re.escape("call().__enter__().nlst('path/to/remote/file')"))
            self.assertEqual(ftp_mock.mock_calls[5],
                call().__exit__(None, None, None))
            self.assertEqual(result, [
                'ftp://server_name/path/to/remote/file/list',
                'ftp://server_name/path/to/remote/file/of',
                'ftp://server_name/path/to/remote/file/files',
            ])

    @patch.object(subprocess, 'check_call')
    def test_stat_recent(self, check_call):

        def mock_dir(path, cb):
            dir_return = ('-r--r--r--    1 839389   25       423102083 '
                'Feb 01 17:15 my_file')
            cb(dir_return)

        fu = FileUtils(testbed=self.testbed_1)

        with patch.object(ftp_fu , 'FTP', autospec=True) as ftp_mock:
            ftp_sess_mock = create_autospec(ftplib.FTP, instance=True)
            ftp_mock.return_value = ftp_sess_mock
            ftp_sess_enter_mock = create_autospec(ftplib.FTP, instance=True)
            ftp_sess_mock.__enter__.return_value = ftp_sess_enter_mock
            ftp_sess_enter_mock.dir.side_effect = mock_dir
            result = fu.stat('ftp://server_name/path/to/remote/my_file',
                strip_leading_slash=False)
            expected_mock_calls = [
             call(),
             call().__enter__(),
             call().__enter__().connect(port=0,
                timeout=fu.DEFAULT_TIMEOUT_SECONDS, host='1.1.1.1'),
             call().__enter__().login(user='myuser', passwd='mypw'),
            ]

            # The mtime has been corrected to UTC for the purposes of the test
            current_year = datetime.date.today().year
            expected_mtime = datetime.datetime(
                current_year, 2, 1, 17, 15, 0, 0, None).timestamp() - time.timezone

            expected_stat_output = AttrDict(
                st_mode = 33060,
                st_uid = 839389,
                st_size = 423102083,
                st_gid = 25,
                st_mtime = expected_mtime,
                st_nlink = 1,
            )

            self.assertEqual(ftp_mock.mock_calls[:4], expected_mock_calls)
            actual_call = str(ftp_mock.mock_calls[4])
            self.assertRegex(actual_call,
                r"call\(\).__enter__\(\).dir\('/path/to/remote/my_file',"
                r".*dir_output_callback.*\)")
            self.assertEqual(ftp_mock.mock_calls[5],
                call().__exit__(None, None, None))
            self.assertEqual(dict(result), dict(expected_stat_output))

            # Correct expectation to UTC
            self.assertEqual(datetime.datetime.fromtimestamp(
                result.st_mtime + time.timezone).\
                strftime("%b %d %H:%M %Y"), 'Feb 01 17:15 {}'.\
                format(current_year))

            self.assertEqual(stat.filemode(result.st_mode), '-r--r--r--')

    @patch.object(subprocess, 'check_call')
    def test_stat_recent_no_group(self, check_call):

        def mock_dir(path, cb):
            dir_return = ('-r--r--r--    1      503   964364800 '
                'Feb 19 17:08 my_file.py')
            cb(dir_return)

        fu = FileUtils(testbed=self.testbed_1)

        with patch.object(ftp_fu , 'FTP', autospec=True) as ftp_mock:
            ftp_sess_mock = create_autospec(ftplib.FTP, instance=True)
            ftp_mock.return_value = ftp_sess_mock
            ftp_sess_enter_mock = create_autospec(ftplib.FTP, instance=True)
            ftp_sess_mock.__enter__.return_value = ftp_sess_enter_mock
            ftp_sess_enter_mock.dir.side_effect = mock_dir
            result = fu.stat('ftp://server_name/path/to/remote/my_file',
                strip_leading_slash=False)
            expected_mock_calls = [
             call(),
             call().__enter__(),
             call().__enter__().connect(port=0,
                timeout=fu.DEFAULT_TIMEOUT_SECONDS, host='1.1.1.1'),
             call().__enter__().login(user='myuser', passwd='mypw'),
            ]

            # The mtime has been corrected to UTC for the purposes of the test
            current_year = datetime.date.today().year
            expected_mtime = datetime.datetime(
                current_year, 2, 19, 17, 8, 0, 0, None).timestamp() - time.timezone

            expected_stat_output = AttrDict(
                st_mode = 33060,
                st_uid = 503,
                st_size = 964364800,
                st_mtime = expected_mtime,
                st_nlink = 1,
            )

            self.assertEqual(ftp_mock.mock_calls[:4], expected_mock_calls)
            actual_call = str(ftp_mock.mock_calls[4])
            self.assertRegex(actual_call,
                r"call\(\).__enter__\(\).dir\('/path/to/remote/my_file',"
                r".*dir_output_callback.*\)")
            self.assertEqual(ftp_mock.mock_calls[5],
                call().__exit__(None, None, None))
            self.assertEqual(dict(result), dict(expected_stat_output))

            # Correct expectation to UTC
            self.assertEqual(datetime.datetime.fromtimestamp(
                result.st_mtime + time.timezone).\
                strftime("%b %d %H:%M %Y"), 'Feb 19 17:08 {}'.\
                format(current_year))

            self.assertEqual(stat.filemode(result.st_mode), '-r--r--r--')

    @patch.object(subprocess, 'check_call')
    def test_stat_non_recent(self, check_call):

        def mock_dir(path, cb):
            dir_return = ( '-rwxrwxrwx    1 281560   25              '
                '0 May 18  2010 test_cfg')
            cb(dir_return)

        fu = FileUtils(testbed=self.testbed_1)

        with patch.object(ftp_fu , 'FTP', autospec=True) as ftp_mock:
            ftp_sess_mock = create_autospec(ftplib.FTP, instance=True)
            ftp_mock.return_value = ftp_sess_mock
            ftp_sess_enter_mock = create_autospec(ftplib.FTP, instance=True)
            ftp_sess_mock.__enter__.return_value = ftp_sess_enter_mock
            ftp_sess_enter_mock.dir.side_effect = mock_dir
            result = fu.stat('ftp://server_name/path/to/remote/my_file')
            expected_mock_calls = [
             call(),
             call().__enter__(),
             call().__enter__().connect(port=0,
                timeout=fu.DEFAULT_TIMEOUT_SECONDS, host='1.1.1.1'),
             call().__enter__().login(user='myuser', passwd='mypw'),
            ]

            expected_mtime = datetime.datetime(
                year=2010, month=5, day=18).timestamp() - time.timezone
            expected_stat_output = AttrDict(
                st_mode = 33279,
                st_uid = 281560,
                st_size = 0,
                st_gid = 25,
                st_mtime = expected_mtime,
                st_nlink = 1,
            )

            self.assertEqual(ftp_mock.mock_calls[:4], expected_mock_calls)
            actual_call = str(ftp_mock.mock_calls[4])
            self.assertRegex(actual_call,
                r"call\(\).__enter__\(\).dir\('path/to/remote/my_file',"
                r".*dir_output_callback.*\)")
            self.assertEqual(ftp_mock.mock_calls[5],
                call().__exit__(None, None, None))
            self.assertEqual(dict(result), dict(expected_stat_output))

            # Correct expectation to UTC
            self.assertEqual(datetime.datetime.fromtimestamp(
                result.st_mtime + time.timezone).\
                strftime("%b %d %H:%M %Y"), 'May 18 00:00 2010')

            self.assertEqual(stat.filemode(result.st_mode), '-rwxrwxrwx')

    @patch.object(subprocess, 'check_call')
    def test_stat_recent_id_names(self, check_call):

        def mock_dir(path, cb):
            dir_return = ('-r--r--r--    1 ftp   ftp       423102083 '
                'Feb 01 17:15 my_file')
            cb(dir_return)

        fu = FileUtils(testbed=self.testbed_1)

        with patch.object(ftp_fu , 'FTP', autospec=True) as ftp_mock:
            ftp_sess_mock = create_autospec(ftplib.FTP, instance=True)
            ftp_mock.return_value = ftp_sess_mock
            ftp_sess_enter_mock = create_autospec(ftplib.FTP, instance=True)
            ftp_sess_mock.__enter__.return_value = ftp_sess_enter_mock
            ftp_sess_enter_mock.dir.side_effect = mock_dir
            result = fu.stat('ftp://server_name/path/to/remote/my_file')
            expected_mock_calls = [
             call(),
             call().__enter__(),
             call().__enter__().connect(port=0,
                timeout=fu.DEFAULT_TIMEOUT_SECONDS, host='1.1.1.1'),
             call().__enter__().login(user='myuser', passwd='mypw'),
            ]

            # The mtime has been corrected to UTC for the purposes of the test
            current_year = datetime.date.today().year
            expected_mtime = datetime.datetime(
                current_year, 2, 1, 17, 15, 0, 0, None).timestamp() - time.timezone

            expected_stat_output = AttrDict(
                st_mode = 33060,
                st_uid = 'ftp',
                st_size = 423102083,
                st_gid = 'ftp',
                st_mtime = expected_mtime,
                st_nlink = 1,
            )

            self.assertEqual(ftp_mock.mock_calls[:4], expected_mock_calls)
            actual_call = str(ftp_mock.mock_calls[4])
            self.assertRegex(actual_call,
                r"call\(\).__enter__\(\).dir\('path/to/remote/my_file',"
                r".*dir_output_callback.*\)")
            self.assertEqual(ftp_mock.mock_calls[5],
                call().__exit__(None, None, None))
            self.assertEqual(dict(result), dict(expected_stat_output))

            # Correct expectation to UTC
            self.assertEqual(datetime.datetime.fromtimestamp(
                result.st_mtime + time.timezone).\
                strftime("%b %d %H:%M %Y"), 'Feb 01 17:15 {}'.\
                format(current_year))

            self.assertEqual(stat.filemode(result.st_mode), '-r--r--r--')

    @patch.object(subprocess, 'check_call')
    def test_stat_non_recent_id_names(self, check_call):

        def mock_dir(path, cb):
            dir_return = ( '-rwxrwxrwx    1 ftp   ftp              '
                '0 May 18  2010 test_cfg')
            cb(dir_return)

        fu = FileUtils(testbed=self.testbed_1)

        with patch.object(ftp_fu , 'FTP', autospec=True) as ftp_mock:
            ftp_sess_mock = create_autospec(ftplib.FTP, instance=True)
            ftp_mock.return_value = ftp_sess_mock
            ftp_sess_enter_mock = create_autospec(ftplib.FTP, instance=True)
            ftp_sess_mock.__enter__.return_value = ftp_sess_enter_mock
            ftp_sess_enter_mock.dir.side_effect = mock_dir
            result = fu.stat('ftp://server_name/path/to/remote/my_file')
            expected_mock_calls = [
             call(),
             call().__enter__(),
             call().__enter__().connect(port=0,
                timeout=fu.DEFAULT_TIMEOUT_SECONDS, host='1.1.1.1'),
             call().__enter__().login(user='myuser', passwd='mypw'),
            ]

            expected_mtime = datetime.datetime(
                year=2010, month=5, day=18).timestamp() - time.timezone
            expected_stat_output = AttrDict(
                st_mode = 33279,
                st_uid = 'ftp',
                st_size = 0,
                st_gid = 'ftp',
                st_mtime = expected_mtime,
                st_nlink = 1,
            )

            self.assertEqual(ftp_mock.mock_calls[:4], expected_mock_calls)
            actual_call = str(ftp_mock.mock_calls[4])
            self.assertRegex(actual_call,
                r"call\(\).__enter__\(\).dir\('path/to/remote/my_file',"
                r".*dir_output_callback.*\)")
            self.assertEqual(ftp_mock.mock_calls[5],
                call().__exit__(None, None, None))
            self.assertEqual(dict(result), dict(expected_stat_output))

            # Correct expectation to UTC
            self.assertEqual(datetime.datetime.fromtimestamp(
                result.st_mtime + time.timezone).\
                strftime("%b %d %H:%M %Y"), 'May 18 00:00 2010')

            self.assertEqual(stat.filemode(result.st_mode), '-rwxrwxrwx')

    @patch.object(subprocess, 'check_call')
    def test_stat_on_directory(self, check_call):

        def mock_dir(path, cb):
            dir_return = ( '-rwxrwxrwx    1 281560   25              '
                '0 May 18  2010 test_cfg')
            cb(dir_return)
            cb(dir_return)

        fu = FileUtils(testbed=self.testbed_1)

        with patch.object(ftp_fu , 'FTP', autospec=True) as ftp_mock:
            ftp_sess_mock = create_autospec(ftplib.FTP, instance=True)
            ftp_mock.return_value = ftp_sess_mock
            ftp_sess_enter_mock = create_autospec(ftplib.FTP, instance=True)
            ftp_sess_mock.__enter__.return_value = ftp_sess_enter_mock
            ftp_sess_enter_mock.dir.side_effect = mock_dir
            with self.assertRaisesRegex(Exception,
                    "More than one result was found, "
                    "did you request a stat of a directory ?"):
                result = fu.stat('ftp://server_name/path/to/remote/my_file')

    @patch.object(subprocess, 'check_call')
    def test_chmod(self, check_call):
        fu = FileUtils(testbed=self.testbed_1)

        with patch.object(ftp_fu , 'FTP', autospec=True) as ftp_mock:
            ftp_sess_mock = create_autospec(ftplib.FTP, instance=True)
            ftp_mock.return_value = ftp_sess_mock
            ftp_sess_enter_mock = create_autospec(
                ftplib.FTP, instance=True)
            ftp_sess_mock.__enter__.return_value = ftp_sess_enter_mock

            mode  = stat.S_IRWXU | stat.S_IRGRP | stat.S_IXGRP | stat.S_IXOTH
            fu.chmod('ftp://server_name/path/to/remote/file', mode)
            expected_mock_calls = [
             call(),
             call().__enter__(),
             call().__enter__().connect(
                port=0, timeout=fu.DEFAULT_TIMEOUT_SECONDS,
                host='1.1.1.1'),
             call().__enter__().login(user='myuser', passwd='mypw'),
            ]
            self.assertEqual(ftp_mock.mock_calls[:4], expected_mock_calls)
            actual_call = str(ftp_mock.mock_calls[4])
            self.assertRegex(actual_call, re.escape(
                "call().__enter__().voidcmd('SITE CHMOD 751 "
                "path/to/remote/file')"))
            self.assertEqual(ftp_mock.mock_calls[5],
                call().__exit__(None, None, None))

    @patch.object(subprocess, 'check_call')
    def test_chmod_no_strip_leading_slash(self, check_call):
        fu = FileUtils(testbed=self.testbed_1)

        with patch.object(ftp_fu , 'FTP', autospec=True) as ftp_mock:
            ftp_sess_mock = create_autospec(ftplib.FTP, instance=True)
            ftp_mock.return_value = ftp_sess_mock
            ftp_sess_enter_mock = create_autospec(
                ftplib.FTP, instance=True)
            ftp_sess_mock.__enter__.return_value = ftp_sess_enter_mock

            mode  = stat.S_IRWXU | stat.S_IRGRP | stat.S_IXGRP | stat.S_IXOTH
            fu.chmod('ftp://server_name/path/to/remote/file', mode,
                strip_leading_slash=False)
            expected_mock_calls = [
             call(),
             call().__enter__(),
             call().__enter__().connect(
                port=0, timeout=fu.DEFAULT_TIMEOUT_SECONDS,
                host='1.1.1.1'),
             call().__enter__().login(user='myuser', passwd='mypw'),
            ]
            self.assertEqual(ftp_mock.mock_calls[:4], expected_mock_calls)
            actual_call = str(ftp_mock.mock_calls[4])
            self.assertRegex(actual_call, re.escape(
                "call().__enter__().voidcmd('SITE CHMOD 751 "
                "/path/to/remote/file')"))
            self.assertEqual(ftp_mock.mock_calls[5],
                call().__exit__(None, None, None))

    @patch.object(subprocess, 'check_call')
    def test_delete(self, check_call):
        fu = FileUtils(testbed=self.testbed_1)

        with patch.object(ftp_fu , 'FTP', autospec=True) as ftp_mock:
            ftp_sess_mock = create_autospec(ftplib.FTP, instance=True)

            ftp_mock.return_value = ftp_sess_mock
            ftp_sess_enter_mock = create_autospec(
                ftplib.FTP, instance=True)
            ftp_sess_mock.__enter__.return_value = ftp_sess_enter_mock

            fu.deletefile('ftp://server_name/path/to/remote/file')
            expected_mock_calls = [
             call(),
             call().__enter__(),
             call().__enter__().connect(
                port=0, timeout=fu.DEFAULT_TIMEOUT_SECONDS,
                host='1.1.1.1'),
             call().__enter__().login(user='myuser', passwd='mypw'),
            ]
            self.assertEqual(ftp_mock.mock_calls[:4], expected_mock_calls)
            actual_call = str(ftp_mock.mock_calls[4])
            self.assertRegex(actual_call, re.escape(
                "call().__enter__().delete(filename='path/to/remote/file')"))
            self.assertEqual(ftp_mock.mock_calls[5],
                call().__exit__(None, None, None))

    @patch.object(subprocess, 'check_call')
    def test_delete_no_strip_leading_slash(self, check_call):
        fu = FileUtils(testbed=self.testbed_1)

        with patch.object(ftp_fu , 'FTP', autospec=True) as ftp_mock:
            ftp_sess_mock = create_autospec(ftplib.FTP, instance=True)

            ftp_mock.return_value = ftp_sess_mock
            ftp_sess_enter_mock = create_autospec(
                ftplib.FTP, instance=True)
            ftp_sess_mock.__enter__.return_value = ftp_sess_enter_mock

            fu.deletefile('ftp://server_name/path/to/remote/file',
                strip_leading_slash=False)
            expected_mock_calls = [
             call(),
             call().__enter__(),
             call().__enter__().connect(
                port=0, timeout=fu.DEFAULT_TIMEOUT_SECONDS,
                host='1.1.1.1'),
             call().__enter__().login(user='myuser', passwd='mypw'),
            ]
            self.assertEqual(ftp_mock.mock_calls[:4], expected_mock_calls)
            actual_call = str(ftp_mock.mock_calls[4])
            self.assertRegex(actual_call, re.escape(
                "call().__enter__().delete(filename='/path/to/remote/file')"))
            self.assertEqual(ftp_mock.mock_calls[5],
                call().__exit__(None, None, None))

    @patch.object(subprocess, 'check_call')
    def test_rename(self, check_call):
        fu = FileUtils(testbed=self.testbed_1)

        with patch.object(ftp_fu , 'FTP', autospec=True) as ftp_mock:
            ftp_sess_mock = create_autospec(ftplib.FTP, instance=True)
            ftp_mock.return_value = ftp_sess_mock
            ftp_sess_enter_mock = create_autospec(
                ftplib.FTP, instance=True)
            ftp_sess_mock.__enter__.return_value = ftp_sess_enter_mock

            fu.renamefile(
                'ftp://server_name/path/to/remote/file',
                'ftp://server_name/path/to/remote/renamed_file',
            )
            expected_mock_calls = [
             call(),
             call().__enter__(),
             call().__enter__().connect(
                port=0, timeout=fu.DEFAULT_TIMEOUT_SECONDS,
                host='1.1.1.1'),
             call().__enter__().login(user='myuser', passwd='mypw'),
            ]
            self.assertEqual(ftp_mock.mock_calls[:4], expected_mock_calls)
            actual_call = str(ftp_mock.mock_calls[4])
            self.assertRegex(actual_call, re.escape(
                "call().__enter__().rename("))
            self.assertRegex(actual_call, re.escape(
                "fromname='path/to/remote/file'"))
            self.assertRegex(actual_call, re.escape(
                "toname='path/to/remote/renamed_file'"))
            self.assertEqual(ftp_mock.mock_calls[5],
                call().__exit__(None, None, None))

    @patch.object(subprocess, 'check_call')
    def test_rename_no_strip_leading_slash(self, check_call):
        fu = FileUtils(testbed=self.testbed_1)

        with patch.object(ftp_fu , 'FTP', autospec=True) as ftp_mock:
            ftp_sess_mock = create_autospec(ftplib.FTP, instance=True)
            ftp_mock.return_value = ftp_sess_mock
            ftp_sess_enter_mock = create_autospec(
                ftplib.FTP, instance=True)
            ftp_sess_mock.__enter__.return_value = ftp_sess_enter_mock

            fu.renamefile(
                'ftp://server_name/path/to/remote/file',
                'ftp://server_name/path/to/remote/renamed_file',
                strip_leading_slash=False
            )
            expected_mock_calls = [
             call(),
             call().__enter__(),
             call().__enter__().connect(
                port=0, timeout=fu.DEFAULT_TIMEOUT_SECONDS,
                host='1.1.1.1'),
             call().__enter__().login(user='myuser', passwd='mypw'),
            ]
            self.assertEqual(ftp_mock.mock_calls[:4], expected_mock_calls)
            actual_call = str(ftp_mock.mock_calls[4])
            self.assertRegex(actual_call, re.escape(
                "call().__enter__().rename("))
            self.assertRegex(actual_call, re.escape(
                "fromname='/path/to/remote/file'"))
            self.assertRegex(actual_call, re.escape(
                "toname='/path/to/remote/renamed_file'"))
            self.assertEqual(ftp_mock.mock_calls[5],
                call().__exit__(None, None, None))

    def test_multiple_address(self):
        def check_call(cmd, *args, **kwargs):
            if '1.1.1.1' in ' '.join(cmd):
                raise subprocess.CalledProcessError(1, cmd)

        with patch.object(subprocess, 'check_call', new_callable=lambda: check_call):

            fu = FileUtils(testbed=self.testbed_4)

            with patch.object(ftp_fu , 'FTP', autospec=True) as ftp_mock:
                ftp_sess_mock = create_autospec(ftplib.FTP, instance=True)
                ftp_mock.return_value = ftp_sess_mock
                ftp_sess_enter_mock = create_autospec(
                    ftplib.FTP, instance=True)
                ftp_sess_mock.__enter__.return_value = ftp_sess_enter_mock

                fu.renamefile(
                    'ftp://server_name/path/to/remote/file',
                    'ftp://server_name/path/to/remote/renamed_file',
                )
                expected_mock_calls = [
                 call(),
                 call().__enter__(),
                 call().__enter__().connect(
                    port=0, timeout=fu.DEFAULT_TIMEOUT_SECONDS,
                    host='2.2.2.2'),
                 call().__enter__().login(user='myuser', passwd='mypw'),
                ]
                self.assertEqual(ftp_mock.mock_calls[:4], expected_mock_calls)
                actual_call = str(ftp_mock.mock_calls[4])
                self.assertRegex(actual_call, re.escape(
                    "call().__enter__().rename("))
                self.assertRegex(actual_call, re.escape(
                    "fromname='path/to/remote/file'"))
                self.assertRegex(actual_call, re.escape(
                    "toname='path/to/remote/renamed_file'"))
                self.assertEqual(ftp_mock.mock_calls[5],
                    call().__exit__(None, None, None))

@skipIf(paramiko_installed == False,
    "Skipping scp unit test because Paramiko and scp are not installed.")
class TestBaseLinuxScpFileUtils(unittest.TestCase):

    # Specified without server key
    testbed_1 = AttrDict()
    testbed_1.servers = AttrDict(
        server_name = dict(
            username="myuser", password="mypw", address='1.1.1.1'),
    )

    # Specified with server key but without explicit address
    testbed_2 = AttrDict()
    testbed_2.servers = AttrDict(
        server_alias = dict(
            server='server_name',
            username="myuser", password="mypw"),
    )

    # Specified with server key and explicit address
    testbed_3 = AttrDict()
    testbed_3.servers = AttrDict(
        server_alias = dict(
            server='server_name', address='1.1.1.1',
            username="myuser", password="mypw"),
    )


    def test_copyfile_local_remote(self):
        fu = FileUtils(testbed=self.testbed_1)

        with tempfile.NamedTemporaryFile() as fp:
            lcl_file = fp.name
            with patch.object(scp_fu , 'SSHClient', autospec=True) \
                    as ssh_mock:
                ssh_sess_mock = create_autospec(
                    paramiko_module.SSHClient, instance=True)
                ssh_mock.return_value = ssh_sess_mock

                with patch.object(scp_fu , 'SCPClient', autospec=True) \
                        as scp_mock:
                    scp_sess_mock = create_autospec(
                        scp_module.SCPClient, instance=True)

                    scp_mock.return_value = scp_sess_mock


                    fu.copyfile('file://{lcl_file_path}'.format(
                        lcl_file_path = lcl_file),
                       'scp://server_name/path/to/remote/file')
                    fu_scp = fu.get_child('scp')
                    expected_ssh_mock_calls = [
                     call(),
                     call().load_system_host_keys(),
                     call().set_missing_host_key_policy(AutoAddPolicy()),
                     call().connect(
                         username='myuser', look_for_keys=True,
                         hostname='1.1.1.1',
                         timeout=fu.DEFAULT_TIMEOUT_SECONDS,
                         port=fu_scp.SSH_DEFAULT_PORT,
                         password='mypw'),
                     call().get_transport()]

                    self.assertEqual(len(ssh_mock.mock_calls), 5)
                    self.assertEqual(
                        ssh_mock.mock_calls[0:1], expected_ssh_mock_calls[0:1])
                    self.assertRegex(str(ssh_mock.mock_calls[2]),
                        r'call\(\)\.set_missing_host_key_policy.*'
                        r'AutoAddPolicy')
                    self.assertEqual(
                        ssh_mock.mock_calls[3:], expected_ssh_mock_calls[3:])

                    self.assertEqual(len(scp_mock.mock_calls), 2)
                    expected_scp_0_pat1 = \
                        r'call\(.*SSHClient\(\)\.get_transport\(\).*id'

                    expected_scp_0_pat2 = \
                        r'socket_timeout={socket_timeout}'.\
                        format(socket_timeout=fu.DEFAULT_TIMEOUT_SECONDS)

                    expected_scp_0_pat3 = (\
                        r'progress=functools\.partial\(.*progress.*filetransferutils\.'
                        r'protocols\.scp\.fileutils\.FileUtils.*\)')

                    self.assertRegex(str(scp_mock.mock_calls[0]),
                        expected_scp_0_pat1)
                    self.assertRegex(str(scp_mock.mock_calls[0]),
                        expected_scp_0_pat2)
                    self.assertRegex(str(scp_mock.mock_calls[0]),
                        expected_scp_0_pat3)

                    self.assertEqual(
                        scp_mock.mock_calls[1], call().put(
                            remote_path='/path/to/remote/file',
                            files=lcl_file))


    def test_copyfile_local_remote_failed_auth(self):
        """ Test a connection that initially fails due to auth exception.
        """
        fu = FileUtils(testbed=self.testbed_1)

        with tempfile.NamedTemporaryFile() as fp:
            lcl_file = fp.name
            with patch.object(scp_fu , 'SSHClient', autospec=True) \
                    as ssh_mock:
                ssh_sess_mock = create_autospec(
                    paramiko_module.SSHClient, instance=True)
                ssh_sess_mock.connect = MagicMock()
                ssh_sess_mock.connect.side_effect=[
                    AuthenticationException, None]
                ssh_mock.return_value = ssh_sess_mock

                with patch.object(scp_fu , 'SCPClient', autospec=True) \
                        as scp_mock:
                    scp_sess_mock = create_autospec(
                        scp_module.SCPClient, instance=True)

                    scp_mock.return_value = scp_sess_mock


                    fu.copyfile('file://{lcl_file_path}'.format(
                        lcl_file_path = lcl_file),
                       'scp://server_name/path/to/remote/file')
                    fu_scp = fu.get_child('scp')
                    expected_ssh_mock_calls = [
                     call(),
                     call().load_system_host_keys(),
                     call().set_missing_host_key_policy(AutoAddPolicy()),
                     call().connect(
                         username='myuser', look_for_keys=True,
                         hostname='1.1.1.1',
                         timeout=fu.DEFAULT_TIMEOUT_SECONDS,
                         port=fu_scp.SSH_DEFAULT_PORT,
                         password='mypw'),
                     call().connect(
                         username='myuser', look_for_keys=False,
                         hostname='1.1.1.1',
                         timeout=fu.DEFAULT_TIMEOUT_SECONDS,
                         port=fu_scp.SSH_DEFAULT_PORT,
                         password='mypw'),
                     call().get_transport()]

                    self.assertEqual(len(ssh_mock.mock_calls), 6)
                    self.assertEqual(
                        ssh_mock.mock_calls[0:1], expected_ssh_mock_calls[0:1])
                    self.assertRegex(str(ssh_mock.mock_calls[2]),
                        r'call\(\)\.set_missing_host_key_policy.*'
                        r'AutoAddPolicy')
                    self.assertEqual(
                        ssh_mock.mock_calls[3:], expected_ssh_mock_calls[3:])

                    self.assertEqual(len(scp_mock.mock_calls), 2)
                    expected_scp_0_pat1 = \
                        r'call\(.*SSHClient\(\)\.get_transport\(\).*id'

                    expected_scp_0_pat2 = \
                        r'socket_timeout={socket_timeout}'.\
                        format(socket_timeout=fu.DEFAULT_TIMEOUT_SECONDS)

                    expected_scp_0_pat3 = (\
                        r'progress=functools\.partial\(.*progress.*filetransferutils\.'
                        r'protocols\.scp\.fileutils\.FileUtils.*\)')

                    self.assertRegex(str(scp_mock.mock_calls[0]),
                        expected_scp_0_pat1)
                    self.assertRegex(str(scp_mock.mock_calls[0]),
                        expected_scp_0_pat2)
                    self.assertRegex(str(scp_mock.mock_calls[0]),
                        expected_scp_0_pat3)

                    self.assertEqual(
                        scp_mock.mock_calls[1], call().put(
                            remote_path='/path/to/remote/file',
                            files=lcl_file))

    def test_copyfile_local_remote_failed_auth_twice(self):
        """ Test a connection that fails twice due to auth exception.
        """
        fu = FileUtils(testbed=self.testbed_1)

        with tempfile.NamedTemporaryFile() as fp:
            lcl_file = fp.name
            with patch.object(scp_fu , 'SSHClient', autospec=True) \
                    as ssh_mock:
                ssh_sess_mock = create_autospec(
                    paramiko_module.SSHClient, instance=True)
                ssh_sess_mock.connect = MagicMock()
                ssh_sess_mock.connect.side_effect=[
                    AuthenticationException, AuthenticationException]
                ssh_mock.return_value = ssh_sess_mock

                with patch.object(scp_fu , 'SCPClient', autospec=True) \
                        as scp_mock:
                    scp_sess_mock = create_autospec(
                        scp_module.SCPClient, instance=True)

                    scp_mock.return_value = scp_sess_mock


                    with self.assertRaises(AuthenticationException):
                        fu.copyfile('file://{lcl_file_path}'.format(
                            lcl_file_path = lcl_file),
                           'scp://server_name/path/to/remote/file')

@skipIf(paramiko_installed == False,
    "Skipping scp unit test because Paramiko and scp are not installed.")
class TestBaseLinuxSftpFileUtils(unittest.TestCase):

    # Specified without server key
    testbed_1 = AttrDict()
    testbed_1.servers = AttrDict(
        server_name = dict(
            username="myuser", password="mypw", address='1.1.1.1'),
    )

    # Specified with server key but without explicit address
    testbed_2 = AttrDict()
    testbed_2.servers = AttrDict(
        server_alias = dict(
            server='server_name',
            username="myuser", password="mypw"),
    )

    # Specified with server key and explicit address
    testbed_3 = AttrDict()
    testbed_3.servers = AttrDict(
        server_alias = dict(
            server='server_name', address='1.1.1.1',
            username="myuser", password="mypw"),
    )


    def test_copyfile_local_remote(self):
        fu = FileUtils(testbed=self.testbed_1)

        with tempfile.NamedTemporaryFile() as fp:
            lcl_file = fp.name
            with patch.object(sftp_fu , 'SSHClient', autospec=True) \
                    as ssh_mock:
                ssh_sess_mock = create_autospec(
                    paramiko_module.SSHClient, instance=True)
                ssh_mock.return_value = ssh_sess_mock

                sftp_sess_mock = create_autospec(SFTPClient, instance=True)
                ssh_sess_mock.open_sftp = MagicMock()
                ssh_sess_mock.open_sftp.return_value = sftp_sess_mock

                fu.copyfile('file://{lcl_file_path}'.format(
                    lcl_file_path = lcl_file),
                   'sftp://server_name/path/to/remote/file')
                fu_sftp = fu.get_child('sftp')
                expected_ssh_mock_calls = [
                 call(),
                 call().load_system_host_keys(),
                 call().set_missing_host_key_policy(AutoAddPolicy()),
                 call().connect(
                     username='myuser', look_for_keys=True,
                     hostname='1.1.1.1',
                     timeout=fu.DEFAULT_TIMEOUT_SECONDS,
                     port=fu_sftp.SSH_DEFAULT_PORT,
                     password='mypw'),
                 call().open_sftp()]

                self.assertEqual(len(ssh_mock.mock_calls), 6)
                self.assertEqual(
                    ssh_mock.mock_calls[0:1], expected_ssh_mock_calls[0:1])

                self.assertRegex(str(ssh_mock.mock_calls[2]),
                    r'call\(\)\.set_missing_host_key_policy.*'
                    r'AutoAddPolicy')

                self.assertEqual(
                    ssh_mock.mock_calls[3:5], expected_ssh_mock_calls[3:5])

                self.assertRegex(str(ssh_mock.mock_calls[5]),
                    r'call\(\)\.open_sftp\(\)\.put\(.*'
                    r'callback.*copyfile.*progress')

                self.assertRegex(str(ssh_mock.mock_calls[5]),
                    r"""call\(\)\.open_sftp\(\)\.put\(.*"""
                    r"""remotepath='/path/to/remote/file'""")

                self.assertRegex(str(ssh_mock.mock_calls[5]),
                    r"""call\(\)\.open_sftp\(\)\.put\(.*"""
                    r"""localpath='{local_file}'""".\
                    format(local_file = lcl_file))


    def test_copyfile_local_remote_failed_auth(self):
        """ Test a connection that initially fails due to auth exception.
        """
        fu = FileUtils(testbed=self.testbed_1)

        with tempfile.NamedTemporaryFile() as fp:
            lcl_file = fp.name
            with patch.object(sftp_fu , 'SSHClient', autospec=True) \
                    as ssh_mock:
                ssh_sess_mock = create_autospec(
                    paramiko_module.SSHClient, instance=True)
                ssh_sess_mock.connect = MagicMock()
                ssh_sess_mock.connect.side_effect=[
                    AuthenticationException, None]
                ssh_mock.return_value = ssh_sess_mock

                sftp_sess_mock = create_autospec(SFTPClient, instance=True)
                ssh_sess_mock.open_sftp = MagicMock()
                ssh_sess_mock.open_sftp.return_value = sftp_sess_mock

                fu.copyfile('file://{lcl_file_path}'.format(
                    lcl_file_path = lcl_file),
                   'sftp://server_name/path/to/remote/file')
                fu_sftp = fu.get_child('sftp')
                expected_ssh_mock_calls = [
                 call(),
                 call().load_system_host_keys(),
                 call().set_missing_host_key_policy(AutoAddPolicy()),
                 call().connect(
                     username='myuser', look_for_keys=True,
                     hostname='1.1.1.1',
                     timeout=fu.DEFAULT_TIMEOUT_SECONDS,
                     port=fu_sftp.SSH_DEFAULT_PORT,
                     password='mypw'),
                 call().connect(
                     username='myuser', look_for_keys=False,
                     hostname='1.1.1.1',
                     timeout=fu.DEFAULT_TIMEOUT_SECONDS,
                     port=fu_sftp.SSH_DEFAULT_PORT,
                     password='mypw'),
                 call().open_sftp()]

                self.assertEqual(len(ssh_mock.mock_calls), 7)
                self.assertEqual(
                    ssh_mock.mock_calls[0:1], expected_ssh_mock_calls[0:1])

                self.assertRegex(str(ssh_mock.mock_calls[2]),
                    r'call\(\)\.set_missing_host_key_policy.*'
                    r'AutoAddPolicy')

                self.assertEqual(
                    ssh_mock.mock_calls[3:6], expected_ssh_mock_calls[3:6])

                self.assertRegex(str(ssh_mock.mock_calls[6]),
                    r'call\(\)\.open_sftp\(\)\.put\(.*'
                    r'callback.*copyfile.*progress')

                self.assertRegex(str(ssh_mock.mock_calls[6]),
                    r"""call\(\)\.open_sftp\(\)\.put\(.*"""
                    r"""remotepath='/path/to/remote/file'""")

                self.assertRegex(str(ssh_mock.mock_calls[6]),
                    r"""call\(\)\.open_sftp\(\)\.put\(.*"""
                    r"""localpath='{local_file}'""".\
                    format(local_file = lcl_file))

    def test_copyfile_local_remote_failed_auth_twice(self):
        """ Test a connection that initially fails due to auth exception.
        """
        fu = FileUtils(testbed=self.testbed_1)

        with tempfile.NamedTemporaryFile() as fp:
            lcl_file = fp.name
            with patch.object(sftp_fu , 'SSHClient', autospec=True) \
                    as ssh_mock:
                ssh_sess_mock = create_autospec(
                    paramiko_module.SSHClient, instance=True)
                ssh_sess_mock.connect = MagicMock()
                ssh_sess_mock.connect.side_effect=[
                    AuthenticationException, AuthenticationException]
                ssh_mock.return_value = ssh_sess_mock

                sftp_sess_mock = create_autospec(SFTPClient, instance=True)
                ssh_sess_mock.open_sftp = MagicMock()
                ssh_sess_mock.open_sftp.return_value = sftp_sess_mock

                with self.assertRaises(AuthenticationException):
                    fu.copyfile('file://{lcl_file_path}'.format(
                        lcl_file_path = lcl_file),
                       'sftp://server_name/path/to/remote/file')

    def test_getspace_one_line_output(self):
        """Test when disk space info output is in one line"""

        df_output = b'''
Filesystem                      1K-blocks    Used Available Use% Mounted on
1.1.1.1:/workspace/path/to/dir/  33554432 4421312  29133120  14% /ws/aaaa-sjc
        '''

        fu = FileUtils(testbed=self.testbed_1)
        with patch.object(sftp_fu, 'SSHClient', autospec=True) \
                as ssh_mock:
            ssh_sess_mock = create_autospec(
                paramiko_module.SSHClient, instance=True)
            ssh_sess_mock.connect = MagicMock()
            ssh_mock.return_value = ssh_sess_mock
            ssh_sess_mock.exec_command = MagicMock()
            ssh_sess_mock.exec_command.return_value = (None, io.BytesIO(df_output), None)
            sftp_sess_mock = create_autospec(SFTPClient, instance=True)
            ssh_sess_mock.open_sftp = MagicMock()
            ssh_sess_mock.open_sftp.return_value = sftp_sess_mock

            self.assertEqual(fu.getspace('sftp://server_name//path/to/remote/dir/'), 29832314880)

    def test_getspace_two_line_output(self):
        """Test when disk space info output is in two line"""

        df_output = b'''
Filesystem               1K-blocks    Used Available Use% Mounted on
1.1.1.1:/workspace/path/to/dir/long/dir/path
                        33554432 4421312  29133120  14% /ws/aaaa-sjc
        '''

        fu = FileUtils(testbed=self.testbed_1)
        with patch.object(sftp_fu, 'SSHClient', autospec=True) \
                as ssh_mock:
            ssh_sess_mock = create_autospec(
                paramiko_module.SSHClient, instance=True)
            ssh_sess_mock.connect = MagicMock()
            ssh_mock.return_value = ssh_sess_mock
            ssh_sess_mock.exec_command = MagicMock()
            ssh_sess_mock.exec_command.return_value = (None, io.BytesIO(df_output), None)
            sftp_sess_mock = create_autospec(SFTPClient, instance=True)
            ssh_sess_mock.open_sftp = MagicMock()
            ssh_sess_mock.open_sftp.return_value = sftp_sess_mock

            self.assertEqual(fu.getspace('sftp://server_name//path/to/remote/dir/'), 29832314880)


    def test_getspace_fail(self):
        """Test when failed to get disk space info"""

        df_output = b'''
df: `/path/to/remote/dir': No such file or directory
        '''

        fu = FileUtils(testbed=self.testbed_1)
        with patch.object(sftp_fu, 'SSHClient', autospec=True) \
                as ssh_mock:
            ssh_sess_mock = create_autospec(
                paramiko_module.SSHClient, instance=True)
            ssh_sess_mock.connect = MagicMock()
            ssh_mock.return_value = ssh_sess_mock
            ssh_sess_mock.exec_command = MagicMock()
            ssh_sess_mock.exec_command.return_value = (None, io.BytesIO(df_output), None)
            sftp_sess_mock = create_autospec(SFTPClient, instance=True)
            ssh_sess_mock.open_sftp = MagicMock()
            ssh_sess_mock.open_sftp.return_value = sftp_sess_mock

            with self.assertRaisesRegex(Exception, "Cannot find available space"):
                fu.getspace('sftp://server_name//path/to/remote/dir/')

class TestBaseLinuxHttpFileUtils(unittest.TestCase):

    # Specified without server key
    testbed_1 = AttrDict()
    testbed_1.servers = AttrDict(
        server_name = dict(port=8000,\
        protocol='http', server="http",),
    )

    def test_create_child(self):
        # To test the http implementation of file utils
        fu = FileUtils()
        fu_ftp = fu.get_child('http')
        self.assertIs(fu_ftp.parent, fu)

    @patch('genie.libs.filetransferutils.protocols.http.fileutils.requests.head')
    def test_stat(self, mock_head):
        # Create a mock response object
        mock_response = Mock()
        # Set the headers method of the mock response to return the expected data
        expected_data = {'Content-Length': '1024'}
        mock_response.headers = expected_data
        # Set the status_code attribute of the mock response
        mock_response.status_code = 200
        # Configure the mock get to return the mock response
        mock_head.return_value = mock_response

        # Call the http stat function
        url = 'http://generic:8000//path/to/remote/dir/'
        fu = FileUtils(testbed=self.testbed_1)
        result = fu.stat(url)

        # Assert that the requests.head method was called with the correct URL
        mock_head.assert_called_once_with(url='http://generic:8000//path/to/remote/dir/', timeout=60)
        # Assert that the result is as expected
        self.assertEqual(result.st_size, 1024)

class TestBaseLinuxTftpFileUtils(unittest.TestCase):
    from genie.libs.filetransferutils.fileutils import FileUtils
    # Testbed configuration for TFTP
    testbed_1 = AttrDict()
    testbed_1.servers = AttrDict(
        server_name=dict(port=69, protocol='tftp', server="tftp",),
    )

    def test_create_child(self):
        """Test the creation of a TFTP child instance."""
        fu = FileUtils()
        fu_tftp = fu.get_child('tftp')
        self.assertIs(fu_tftp.parent, fu)

    @patch.object(FileUtils, 'execute_in_subprocess')
    @patch.object(FileUtils, 'validate_and_parse_url')
    def test_copyfile_upload(self, mock_validate_and_parse_url, mock_execute_in_subprocess):
        """Test uploading a file using TFTP."""
        # Mock the validate_and_parse_url function to return expected values
        mock_validate_and_parse_url.side_effect = [
            (None, None, "/local/path/to/file.txt"),  # Source path
            ("tftp.server.com", None, "/remote/path/to/file.txt")  # Destination path
        ]

        # Create an instance of FileUtils with the testbed
        fu = FileUtils(testbed=self.testbed_1)

        # Call the copyfile method for upload
        fu.copyfile(
            source="file:///local/path/to/file.txt",
            destination="tftp://tftp.server.com/remote/path/to/file.txt",
        )

        # Assert that validate_and_parse_url was called twice
        self.assertEqual(mock_validate_and_parse_url.call_count, 2)

        # Assert that the correct command was executed
        mock_execute_in_subprocess.assert_called_once_with(
            "curl --upload-file /local/path/to/file.txt tftp://tftp.server.com:69/remote/path/to/file.txt",
            timeout_seconds=1200
        )
