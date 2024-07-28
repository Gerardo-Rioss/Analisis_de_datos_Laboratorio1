import datetime
import os
import platform

from gestionVentas import(
    VentaLocal,
    VentaOnline,
    GestionVentas,
)

def limpiar_pantalla():
    ''' Limpiar la pantalla según el sistema operativo'''
    if platform.system() == 'Windows':
        os.system('cls')
    else:
        os.system('clear')  # Para Linux/Unix/MacOs

def mostrar_menu():
    print("========== Menú de Gestión de Ventas ==========")
    print('1. Agregar Venta Online')
    print('2. Agregar Venta Local')
    print('3. Mostrar Ventas')
    print('4. Actualizar Monto Total de la venta por ID')
    print('5. Eliminarar Venta por ID')
    print('6. Salir')
    print('======================================================')

def agregarVenta(gestion, tipoVenta):
    try:
        idVenta= input('Ingrese el id de venta: ')
        fecha = datetime.datetime.now().strftime("%d-%m-%y")
        cliente= input('Ingrese el cliente: ')
        montoTotal= float(input('Ingrese el monto total de la venta: '))
        productos= input('Ingrese los productos (separados por coma): ').split(',')

        if tipoVenta == '1':
            direccionEnvio= input('Ingrese la dirección del envio: ')
            venta = VentaOnline(idVenta,fecha,cliente,productos,montoTotal, direccionEnvio)
        elif tipoVenta == '2':
            vendedor= input('Ingrese el vendedor: ')
            venta= VentaLocal(idVenta,fecha,cliente,productos, montoTotal, vendedor)
        else:
            print('Opción inválida')
            return
        
        gestion.crearVenta(venta)
        input('Presione enter para continuar...')

    except ValueError as e:
        print(f'Ingrese una opcion valida: {e}')
    except Exception as e:
        print(f'Error inesperado: {e}')


def buscarVentaPorId(gestion):
    idVenta = input('Ingrese la id de la venta a buscar: ')
    gestion.leerVenta(idVenta)
    input('Presione enter para continuar...')
    

def actualizarMontoTotalVenta(gestion):
    idVenta = input('Ingrese el ID de la venta que quiere actualizar el monto total: ')
    nuevoMontoTotal = float(input('Ingrese el nuevo monto de la venta: '))
    gestion.actualizarMontoTotal(idVenta, nuevoMontoTotal)
    input('Presione enter para continuar...')


def eliminarVentaPorId(gestion):
    idVenta = input('Ingrese el ID de la venta que quiere eliminar:  ')
    gestion.eliminarVenta(idVenta)
    input('Presione enter para continuar...')


def mostrarTodasLasVentas(gestion):
    print('=============== Listado completo de las  Ventas ==============')
    for venta in gestion.leerDatos().values():
        if 'direccionEnvio' in venta:
            print(f"ID {venta['idVenta']} - CLiente {venta['cliente']} - Monto: {venta['montoTotal']} - Dirección envío: {venta['direccionEnvio']}")
        else:
            print(f"ID {venta['idVenta']} - CLiente {venta['cliente']} - Monto: {venta['montoTotal']} - Vendedor: {venta['vendedor']}")
    print('=====================================================================')
    input('Presione enter para continuar...')
        

if __name__ == '__main__':
    archivoVentas='ventas_db.json'
    gestion = GestionVentas(archivoVentas)

    while True:
        limpiar_pantalla()
        mostrar_menu()
        opcion = input('Seleccione una opción: ')

        if opcion == '1' or opcion == '2':
            agregarVenta(gestion, opcion)

        elif opcion == '3':
            mostrarTodasLasVentas(gestion)
        elif opcion == '4':
            actualizarMontoTotalVenta(gestion)
        elif opcion == '5':
            eliminarVentaPorId(gestion)
        elif opcion == '6':
            print('Saliendo del programa...')
            break
        else:
            print('Opción no válida. Por favor, seleccione una opción válida (1-6)')
