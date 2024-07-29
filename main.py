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

def agregar_venta(gestion, tipo_venta):
    try:
        id_venta = str(len(gestion.leer_datos())+1)
        fecha = datetime.datetime.now().strftime("%d-%m-%y")
        
        while True:
            cliente= input('Ingrese el cliente: ')
            if cliente:
                break
            print("Error, debe ingresar el cliente... ")

        while True:
            try:
                monto_total= round(float(input('Ingrese el monto total de la venta: ')),2)
                if monto_total>0:
                    break
                else:
                    print('El monto total debe ser mayor a cero.')
            except ValueError:
                print('Error, debe ingresar un número valido.')
        
        while True:
            try:
                productos= input('Ingrese los productos (separados por coma): ').split(',')
                productos = [prod.strip()for prod in productos if prod.strip()]
                if productos:
                    break
                else:
                    print('Error, Debe ingresar al menos un producto válido.')
            except ValueError:
                print('Error, ha ocurrido un error al procesar los datos ingresados.-')

        if tipo_venta == '1':
            while True:
                try:
                    direccion_envio= input('Ingrese la dirección del envio: ')
                    if direccion_envio:
                        break
                    else:
                        print('Error, debe ingresar alguna dirección.')
                except ValueError:
                    print('Error, ha ocurrido un error al procesar los datos ingresados.-')

            venta = VentaOnline(id_venta,fecha,cliente,productos,monto_total, direccion_envio)
        elif tipo_venta == '2':

            while True:
                try:
                    vendedor= input('Ingrese el vendedor: ')
                    if vendedor:
                        break
                    else:
                        print('Error, debe ingresar el vendedor.')
                except ValueError:
                    print('Error, ha ocurrido un error al procesar los datos ingresados.-')
            venta= VentaLocal(id_venta,fecha,cliente,productos, monto_total, vendedor)
        else:
            print('Opción inválida')
            return
        
        gestion.crear_venta(venta)
        input('Presione enter para continuar...')

    except ValueError as e:
        print(f'Ingrese una opcion valida: {e}')
    except Exception as e:
        print(f'Error inesperado: {e}')

def buscar_venta_por_id(gestion):
    id_venta = input('Ingrese la id de la venta a buscar: ')
    gestion.leer_venta(id_venta)
    input('Presione enter para continuar...')

def actualizar_monto_total_venta(gestion):
    id_venta = input('Ingrese el ID de la venta que quiere actualizar el monto total: ')
    nuevo_monto_total = float(input('Ingrese el nuevo monto de la venta: '))
    gestion.actualizar_monto_total(id_venta, nuevo_monto_total)
    input('Presione enter para continuar...')

def eliminar_venta_por_id(gestion):
    id_venta = input('Ingrese el ID de la venta que quiere eliminar:  ')
    gestion.eliminar_venta(id_venta)
    input('Presione enter para continuar...')

def mostrar_todas_las_ventas(gestion):
    print('=============== Listado completo de las  Ventas ==============')
    for venta in gestion.leer_datos().values():
        if 'direccion_envio' in venta:
            print(f"id: {venta['id_venta']} - CLiente {venta['cliente']} - Monto: ${(venta['monto_total']):.2f} - VENTA ONLINE - Dirección envío: {venta['direccion_envio']}")
        else:
            print(
                f"id: {venta['id_venta']} - CLiente {venta['cliente']} - Monto: ${(venta['monto_total']):.2f} - VENTA LOCAL - Vendedor: {venta['vendedor']}")
    print('=====================================================================')
    input('Presione enter para continuar...')

if __name__ == '__main__':
    archivo_ventas='ventas_db.json'
    gestion = GestionVentas(archivo_ventas)

    while True:
        limpiar_pantalla()
        mostrar_menu()
        opcion = input('Seleccione una opción: ')

        if opcion == '1' or opcion == '2':
            agregar_venta(gestion, opcion)

        elif opcion == '3':
            mostrar_todas_las_ventas(gestion)
        elif opcion == '4':
            actualizar_monto_total_venta(gestion)
        elif opcion == '5':
            eliminar_venta_por_id(gestion)
        elif opcion == '6':
            print('Saliendo del programa...')
            break
        else:
            print('Opción no válida. Por favor, seleccione una opción válida (1-6)')
