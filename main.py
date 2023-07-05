import pandas as pd
import hashlib
import datetime


def login():
    print("Como desea ingresar")
    print("1. Administrador")
    print("2. Comprador")
    x = input()
    if x == 1 or x == "1":
        #checkadmin
        ruta = "admins.csv"
        tipos_datos = {'cantidad_disponible': int}
        admins = pd.read_csv(ruta, dtype=tipos_datos)
        sha256_hash = hashlib.sha256()
        while True:
            usrnmae = str(input("Ingrese su nombre de usuario: "))
            passw = str(input("Ingrese su contraseña: "))
            sha256_hash = hashlib.sha256()
            sha256_hash.update(passw.encode('utf-8'))
            resultado = admins[(admins['username'] == usrnmae) & (admins['hash'] == sha256_hash.hexdigest())]
            if resultado.empty:
                print("El nombre y la contraseña no coinciden.")
            else: 
                print("El nombre y la contraseña coinciden.")
                print("Bienvenido ", usrnmae)
                return 1
    elif x == 2 or x == "2":
        return 2
    else:
        print("opción no válida, intente nuevamente")
        login()
    return

def guardar_movimiento(juego, accion, cantidad):
    ruta = "movimientos.csv"
    fecha_actual = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    movimiento = {
        'fecha': fecha_actual,
        'juego': juego,
        'accion': accion,
        'cantidad': cantidad
    }
    df = pd.DataFrame(movimiento, index=[0])
    if not pd. read_csv(ruta).empty:
        df.to_csv(ruta, mode='a', header=False, index=False)
    else:
        df.to_csv(ruta, index=False)
    print("Movimiento guardado exitosamente.")

def checknum(x):
    try:
        num = int(x)
        return True
    except:
        print("La entrada no es una cantidad válida")
        return False


def agregarinventario():
    nombre = str(input("¿Qué juego desea agregar al inventario? "))
    ruta = "juegos.csv"
    tabla = pd.read_csv(ruta)
    tabla['cantidad_disponible'] = tabla['cantidad_disponible'].astype(int)
    if nombre in tabla['titulo'].values:
        print("Este título se encuentra en el inventario, solo debe indicar")
        while True:
            cantidad = input("Cantidad a ingresar: ")
            if checknum(cantidad):
                cantidad = int(cantidad)
                break
        juego = tabla.loc[tabla['titulo'] == nombre]
        nueva_cantidad = juego['cantidad_disponible'].values[0] + cantidad
        tabla.loc[tabla['titulo'] == nombre, 'cantidad_disponible'] = nueva_cantidad
        guardar_movimiento(nombre, 'agregar', cantidad)
    else: 
        print("Este título no se encuentra en el inventario, debe ingresar los siguientes datos: ")
        genero = str(input("Género: "))
        plat = str(input("Plataforma: "))
        while True:
            precio = input("Precio: ")
            if checknum(precio):
                break
        while True:
            cantidad = input("Cantidad a ingresar: ")
            if checknum(cantidad):
                cantidad = int(cantidad)
                break
        newjuego = {
            'titulo': nombre,
            'genero': genero,
            'plataforma': plat,
            'cantidad_disponible': cantidad,
            'precio': precio
        }
        tabla = tabla.append(newjuego, ignore_index=True)
        guardar_movimiento(nombre, 'agregar', cantidad)
    tabla.to_csv(ruta, index=False)
    return


def compracliente():
    ruta = "juegos.csv"
    tabla = pd.read_csv(ruta)
    
    print("Juegos disponibles:")
    print(tabla[['titulo', 'genero', 'plataforma', 'cantidad_disponible', 'precio']])
    while True:
        titulo = input("Ingrese el título del juego que desea comprar: ")
        cantidad_comprar = int(input("Ingrese la cantidad que desea comprar: "))
        if checknum(cantidad_comprar):
            juego = tabla.loc[tabla['titulo'] == titulo]
            
            if juego.empty:
                print("El juego no está disponible en el inventario.")
            elif cantidad_comprar > juego['cantidad_disponible'].values[0]:
                print("No hay suficientes juegos en stock para realizar la compra.")
            else:
                juego['cantidad_disponible'] -= cantidad_comprar
                guardar_movimiento(titulo, 'compra', cantidad_comprar)

                precio_total = juego['precio'].values[0] * cantidad_comprar
                print(f"Compra exitosa. El total a pagar es: {precio_total} pesos.")
            break
        else: 
            print("Cantidad inválida, intente nuevamente")
        
    tabla.to_csv(ruta, index=False)
    return
    
    
def showinv():
    ruta = "juegos.csv"
    tabla = pd.read_csv(ruta)
    
    print("Juegos disponibles:")
    print(tabla[['titulo', 'genero', 'plataforma', 'cantidad_disponible', 'precio']])
    return

def menuadmin():
    print("¿Que desea hacer?")
    print("1. Comprar un juego")
    print("2. Vender un juego")
    print("3. Revisar inventario")
    print("4. Salir")
    x = str(input())
    if x == "1":
        agregarinventario()
    elif x == "2":
        compracliente()
    elif x== "3":
        showinv()
    elif x == "4":
        return
    else:
        print("Opción inválida, intente nuevamente")
        menuadmin()
    return
    
    
def menucliente():
    print("¿Que desea hacer?")
    print("1. Ver catálogo")
    print("2. Comprar juego")
    print("3. Salir")
    x = str(input())
    if x == "1":
        showinv()
    elif x == "2":
        compracliente()
    elif x == "3":
        return 
    else:
        print("Opción inválida, intente nuevamente")
        menucliente()
    return
        
def main():
    print("Bienvenido")
    usr = login()
    if usr == 1:
        #menuadmin
        menuadmin()
    elif usr == 2:
        #menucliente
        menucliente()
    print("Hasta luego!")
    return
