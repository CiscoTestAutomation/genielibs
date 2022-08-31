import os
import shutil
import tempfile
import unittest
import subprocess


class TestGenieRobot(unittest.TestCase):

    def setUp(self):
        self.logsdir = tempfile.mkdtemp(prefix='robot')

    def tearDown(self):
        shutil.rmtree(self.logsdir)

    def test_robot(self):
        pwd = os.path.dirname(__file__)
        env = os.environ.copy()

        output = []
        with subprocess.Popen('robot -d %s genie.robot' % self.logsdir,
                              shell=True,
                              cwd=pwd,
                              env=env,
                              stdout=subprocess.PIPE,
                              stderr=subprocess.STDOUT) as p:
            for line in p.stdout:
                line = line.decode('utf-8')
                print(line, end='') # interactive display
                output += line

        self.assertEqual(p.returncode, 0)

    def test_diff(self):
        pwd = os.path.dirname(__file__)
        env = os.environ.copy()

        output = []
        with subprocess.Popen('robot -d %s diff.robot' % self.logsdir,
                              shell=True,
                              cwd=pwd,
                              env=env,
                              stdout=subprocess.PIPE,
                              stderr=subprocess.STDOUT) as p:
            for line in p.stdout:
                line = line.decode('utf-8')
                print(line, end='') # interactive display
                output += line

        self.assertEqual(p.returncode, 0)

    def test_libdoc_generation(self):
        from robot.libdoc import LibraryDocumentation
        lib = LibraryDocumentation('genie.libs.robot.GenieRobot')
        assert len(lib.keywords)
