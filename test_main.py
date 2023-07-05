import unittest
from mock import patch
from main import *

class TestLogin(unittest.TestCase):
    def test_login(self):
        with mock.patch('builtins.input', return_value="1"):
    # Resto del código de prueba
    # ...
        inputs = ["1", "admin", "password"]
        input_mock = lambda _: inputs.pop(0)
        expected_output = "El nombre y la contraseña coinciden.\nBienvenido admin\n"
        
        with patch('builtins.input', input_mock), \
             patch('builtins.print') as mock_print:
            login()
            mock_print.assert_called_with(expected_output)


if __name__ == '__main__':
    unittest.main()
