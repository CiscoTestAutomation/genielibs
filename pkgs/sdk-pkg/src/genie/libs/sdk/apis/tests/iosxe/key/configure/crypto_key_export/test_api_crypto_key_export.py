import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.key.configure import crypto_key_export


class TestCryptoKeyExport(unittest.TestCase):

 @classmethod
 def setUpClass(self):
  testbed = f"""
        devices:
          INT1:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: iosxe
            type: iosxe
        """
  self.testbed = loader.load(testbed)
  self.device = self.testbed.devices['INT1']
  self.device.connect(
   learn_hostname=True,
   init_config_commands=[],
   init_exec_commands=[]
  )

 def test_crypto_key_export(self):
  result = crypto_key_export(self.device, 'rsa', 'REKEYRSA', 'terminal', 'aes', 'test12345', 30)
  expected_output = ('crypto key export rsa REKEYRSA pem terminal aes test12345\r\n'
                     '% Key name: REKEYRSA\r\n'
                     '   Usage: General Purpose Key\r\n'
                     '   Key data:\r\n'
                     '-----BEGIN PUBLIC KEY-----\r\n'
                     'MIICIjANBgkqhkiG9w0BAQEFAAOCAg8AMIICCgKCAgEAyc9qy/fE+JCcccOKZbm4\r\n'
                     'fWaXi36RJz2P3KtlhxF7Afmoe+khxzm1aPQIRBedJTA/KzSgF+VVS6T74pSZqR8p\r\n'
                     '9aIkOnTUS151dt6y2l7x702MBPPHZDKj0xpC3Oz31xZRYR68MUG312ZpLMtSOFDt\r\n'
                     'EctHosJJ0oj/5GyaJsDCH0PwUa3L9yLlpHf3p1B6xDw8A/+alaFA/J6pEKcLY+Ej\r\n'
                     'Sd2Avjk3OgStOsKX3d5d/YaUK6gy4bGYCpPmsK35piPDPh9VPPst4o2Ahxzfr0V2\r\n'
                     'I6hmnUXK4mew9mCvg3/3RhawjcnGoBzfx0xpFETYnpVhCVpvD8GSokbDIlv1C1dw\r\n'
                     'Qd/2bJd5Jw4/8S1H10M4hysWmJaV8wqzJw6ZKFNlEwCnHPSJaHiaiUsUt8XDw43I\r\n'
                     '8DWivRQwjecflURT1r2IZNjgvSpTTXU8mu3uwDNlGjqwloAtaJzbdc7TQF48MFsq\r\n'
                     'w7ExPqahekcp4uPqONHZdBF2HPEsdNr12KiV4385+YyFJQOiu0AVCKvimamp+QFh\r\n'
                     'XroaSZa1W2ghjCz3YaGhaHZ6b3/kBbF99ulA33NOPDR1Yj7BZAjXTIYKxQSjXMEd\r\n'
                     'n+a6j4Gc1rl1OARch9Scptc5yaRrSObxvWbbYZtMbn1ZGkIRCeoDaAjys6vzzs4M\r\n'
                     'pk0iHO4wQ51fK0SdKCfehJcCAwEAAQ==\r\n'
                     '-----END PUBLIC KEY-----\r\n'
                     '\r\n'
                     'base64 len 3248-----BEGIN RSA PRIVATE KEY-----\r\n'
                     'Proc-Type: 4,ENCRYPTED\r\n'
                     'DEK-Info: AES-256-CBC,E260A075DD2F96C76B96DDB973E5D510\r\n'
                     '\r\n'
                     'tXPUwR9AiXktOzAwsgXpe3PkUr4ucHjsQlv2qR1QwyJNS38vtofKD6wJGqlNSi2O\r\n'
                     'FTj6VeDNFN6R46eyOIe1MwjaNlGKInG2Z71J2q0mleVXktOBlTQtKmZWQ7EUscQA\r\n'
                     'nUKFNyI1q4w5JaL6g8UkrHZOj2zf15u7Jd/wlDxtrK0GLiGFWsuKJGz6gWYAyw5C\r\n'
                     '/que/v3O1UEEjLKEgdNRed9V/Dt9u5tSbTDos6i5ZvLfEAvVXc5CH4HLECjdpk5c\r\n'
                     '7dmZpp6w3VTW9vy+iuam/wVGTQjpovuy+To+TwY8euEBDmSTnwXUPKicpvYaS2Lp\r\n'
                     'cFx4hEJoqF6yianKGJ/E7l9atXSLM1VTyMeSLe6NoUfY62E/TRkF1ZYT+P95LBAL\r\n'
                     'WuaDFN9I/iGKDEenDumupuqhlCmuHlTp61p9EVxlj3J4T4nyiTwdhq6nTDK2uVNI\r\n'
                     'rMzZYHkOzon+2vopXqORz8b88zjqma1mdqAP9oHNk0V8iiUqU4IJXT9SNgldQy7U\r\n'
                     'YrJKlbf6cJZUw48SQ5QG2EBdiXO2ceX5uLARjVkWxbIZXq0Q5rzSa7SB6XlYzq9H\r\n'
                     'upoWThFHcZxO7jDRnsRNXVNSXq/son6TtgAF5aMxDPgjf3oBzgQ9Zb//HeO78j5o\r\n'
                     '6LHu1iW4NLv8OBMacMic7kh1MySPSDtLGXqIfW6AlTVa/lcmW5fJDtHmoESMp/4V\r\n'
                     'HI71ZOE/wVCWFUiAC1gXrRTrplqcJXuDq49slI4dLFGixjoQU/wGDb6YeSuuABXI\r\n'
                     'X4bI/MQcgnar7aUXGkjEP/GuIagNtL/8fhniCfn+kQOqXvNTzV+ovWtkvhdyMpdP\r\n'
                     'UROQyp47WFRx7SfLDKb7pwaCzdcDxp8re7NGle7GUckjOijP2nhaoYOxVzYzPsvD\r\n'
                     '/ZxL9kmptK93repXFAK0yXKO0+vVSE9Ohj9Hq43OGro0FMutAdz8UVZEXbQ44GQV\r\n'
                     'gr2MEDvTvQ0crGe2NVJVtaUv3WSjmBN1sstpuBHAXeXlwbh3RkhPYL6nj8m+hM0N\r\n'
                     'iCoqIYdvhIrrXek9x/knn2IMELeAEnS5Xyugm+qEm0wGhohUfBk82CE6tN4Gqkv+\r\n'
                     'IezGF8CJUX3ukpqrILLgy/wRymIskedYvIZMYznn2NTHI8WzxIxG7bEf1zJkIrB+\r\n'
                     'O3z9jhJCvHOYnGV6F+C6la/K6X8IyFEswQytoxV6DWB/rJsHVzt2tUzLtPL/r3U6\r\n'
                     'kcZpzLTsHJV/8dBdwCxj9ZgBetS9WFnnQWxG0Bxl7n/btMtW3gl4MKb9JBHBmBCI\r\n'
                     '2/mQTwOz7HqJquoFKfwVBQXrwNOZJRPEEZK2Y+1zrQ9fEosK0ybdLYA+585LpbkP\r\n'
                     'AJU6HlTo3HeAwZim1cL7CR02gI1DAUrvIXQXrgiaTgIAtmHddIy+P9Q2p2fKkt8Q\r\n'
                     'fMkN+B5wq57Sws7B5W1zbBO9oflMjQ+kVImNfDvfYkgW/0UDgxrT67fYCyEuNXuq\r\n'
                     'qccH5eVK7a3cMo8fT4aVBJO3AlZ+4EObKJS3K55JFIQjLrgOoRbMY95cYgvmHZ7I\r\n'
                     'L0REqG2uMASHWEKrlQayv2CqtacJd1wcKBQfeepkCs6q2aOkExAv5Ny9xNopHpfg\r\n'
                     'RgYVeHZ2rrh74jawsZ/d6mvKkeaAmsLyHggjd3V0sNnA4qz9jJooLjG0FNxCBhst\r\n'
                     'to4QaDVYfbTNjIlXqESxC6r1qypKumghmvbYyImPA3ijRjnJG0AI3V71g7jELaUh\r\n'
                     'PzddcjLO0k4jFnsFGnqodA1ihL0yL02t49X/ej54zumJcskFL81dNbT+zvRRTP6P\r\n'
                     'DS65/+0S4d5zd5QxTVK+B2xJX+P7tJd/86nrRLs+p5GosJFO9O6uwieNMKoNspDH\r\n'
                     'oZANPeLA4+xUYW2HHB9C8gpSToyLjZEnxQdp2k40LjzTfahQJNS0txxchOgFSePr\r\n'
                     'V2k09uCbP2n2He3Vm1RAuKVQqVGqe0XbpQPc2/F/QlR9TSbbEedwk5L/Gc2evCLl\r\n'
                     '6WQxEiQLhkNfPwelt8WBVeYUVK3fj2rLhFRd5FR9IlJtddhac02pr9pVVy0F+nNZ\r\n'
                     '165oEzOaMPKmWOzUqR4LdotgsmOQ0mI69u2HbIG65cPP2xh3c8ZLXS9GOowkESAD\r\n'
                     'XDm4h56qO+A37dlnDbdAXlIY22bj13dDPF1xuqFHbiR3SU+HcAJNHS7aEjOmonwf\r\n'
                     '8MWgTB72mu3dVtEwQU6d+JCd396JGm7h5Q6lcezTWIAjFCYHAwgfZcpFq3dGd/xp\r\n'
                     '76sV9UrjmnMmonVE0Up6n4Ji5D8JrYN8Huu9ajxXkwuvvxNGNuBPHqj1FO+gK40j\r\n'
                     'yb/kqn6gedpKQ4iltxgZequAbW6yRq2dEs654nGyDMbFVJbSq4kduezUZFNsQSD3\r\n'
                     'UfGnECbFMEpITNNdcykSM0OGSMcS2okYm/aZAXWoH0BmV0oUSmVcrL+wgm/3HpE+\r\n'
                     'SdwalIlvGC3lvozO8c6qwLX+QRXAslEfbIW4P7boB5yF4UTbGM84jgkIQg5QelL0\r\n'
                     '4HXTtaCca4GATAEmE+YbSKfH2ZIwEB7Mxrj9cS/6XIVnVmoKDsJMp9k6ODw0hQNh\r\n'
                     'JXrCaqLnuNIl0B6tdR4KXZieDTXjpNe74ZUPv9fjl1eRl9nt8utexDEqN6F2RMEM\r\n'
                     'd8TckE5pJCPN4pzCTxRGgGgyw0CJRuJA4PB8VIbmJzYjvAia/Pt1fS+CdzoTAuqa\r\n'
                     'IcfIRBUTUA15l2aWqX5PLGLOFc5OFSeIhlzIl+nY/b8AGOqtXyUcFEwc0ivPOVHt\r\n'
                     'fwhy7IGNu3DHwYQdC/sYNWZGPoqX31qtRCeWPIOohui9rnItLC7itJjozpOzy1C1\r\n'
                     'GxInCm4yT8selgbOZbiR9spE+xFHR9LxwHDanKtg0QdrNlpHVS0kHXMOeOK/KXce\r\n'
                     'kRNedllo8dbuxHMzWLIHaqxfjHg0h+CajnCseEvY+jjr/sXcG5GYf9ZyjtRpUduB\r\n'
                     'pMwHMGCvoyAMsRkd994RSiuZzTwiql4elVJnBGMiVwknT1TNoq59jOAuXkWwFCDI\r\n'
                     '+vSjhRb6lpvQ/x3ki+KIAvA26JOeSJ6zFIxFBp61Az15dGoPnKkbHVaWBL7bI8OQ\r\n'
                     'fLWUHENtEhoyQhMUSt3MxOzkqHccjhuGzLEjFBkAhF6xIewc1g2t5rd/jxX20VEn\r\n'
                     'SN2UyoaUyBM=\r\n'
                     '-----END RSA PRIVATE KEY-----\r\n')
  self.assertIn(expected_output, result)