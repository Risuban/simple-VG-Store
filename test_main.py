import pytest
import pandas as pd
from io import StringIO
from unittest.mock import patch
from code import login, agregarinventario, compracliente, showinv


def test_login(monkeypatch):
    inputs = ["1", "admin", "password"]
    input_mock = lambda _: inputs.pop(0)
    monkeypatch.setattr('builtins.input', input_mock)

    # Creamos un archivo CSV temporal para los datos de prueba
    admins_data = "username,hash\nadmin,123456"
    admins_file = StringIO(admins_data)
    pd.DataFrame().to_csv("admins.csv", index=False)
    with open("admins.csv", "w") as file:
        file.write(admins_data)

    assert login() == 1


def test_agregarinventario(monkeypatch):
    inputs = ["Juego 1", "1", "10"]
    input_mock = lambda _: inputs.pop(0)
    monkeypatch.setattr('builtins.input', input_mock)

    # Creamos un archivo CSV temporal para los datos de prueba
    juegos_data = "titulo,genero,plataforma,cantidad_disponible,precio\nJuego 2,Accion,PC,5,19.99"
    juegos_file = StringIO(juegos_data)
    pd.DataFrame().to_csv("juegos.csv", index=False)
    with open("juegos.csv", "w") as file:
        file.write(juegos_data)

    agregarinventario()

    # Verificar que el juego se haya agregado correctamente
    tabla = pd.read_csv("juegos.csv")
    juego = tabla.loc[tabla['titulo'] == "Juego 1"]
    assert not juego.empty
    assert juego['genero'].values[0] == "Accion"
    assert juego['plataforma'].values[0] == "PC"
    assert juego['cantidad_disponible'].values[0] == 15
    assert juego['precio'].values[0] == 1.0


def test_compracliente(monkeypatch):
    inputs = ["Juego 2", "3"]
    input_mock = lambda _: inputs.pop(0)
    monkeypatch.setattr('builtins.input', input_mock)

    # Creamos un archivo CSV temporal para los datos de prueba
    juegos_data = "titulo,genero,plataforma,cantidad_disponible,precio\nJuego 2,Accion,PC,5,19.99"
    juegos_file = StringIO(juegos_data)
    pd.DataFrame().to_csv("juegos.csv", index=False)
    with open("juegos.csv", "w") as file:
        file.write(juegos_data)

    with patch('builtins.print') as mock_print:
        compracliente()

        # Verificar que la cantidad se haya actualizado correctamente
        tabla = pd.read_csv("juegos.csv")
        juego = tabla.loc[tabla['titulo'] == "Juego 2"]
        assert not juego.empty
        assert juego['cantidad_disponible'].values[0] == 2

        # Verificar que se haya impreso el mensaje correcto
        mock_print.assert_called_with("Compra exitosa. El total a pagar es: 59.97 pesos.")


def test_showinv(capfd):
    # Creamos un archivo CSV temporal para los datos de prueba
    juegos_data = "titulo,genero,plataforma,cantidad_disponible,precio\nJuego 1,Accion,PC,10,19.99"
    juegos_file = StringIO(juegos_data)
    pd.DataFrame().to_csv("juegos.csv", index=False)
    with open("juegos.csv", "w") as file:
        file.write(juegos_data)

    showinv()

    # Capturamos la salida y verificamos que los juegos se impriman correctamente
    output = capfd.readouterr().out
    assert "Juego 1" in output
    assert "Accion" in output
    assert "PC" in output
    assert "10" in output
    assert "19.99" in output


# Ejecutar las pruebas
if __name__ == '__main__':
    pytest.main()
