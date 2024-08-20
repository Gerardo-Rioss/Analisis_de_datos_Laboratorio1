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
    print("================== Consultas ==================")
    print('3. Mostrar Todas las Ventas')
    print('4. Mostrar Ventas OnLine')
    print('5. Mostrar Ventas Locales')
    print("========== Actualizar por ID de venta ==========")
    print('6. Monto Total')
    print('7. Cliente')
    print('8. Productos')
    print('9. Dirección del envio')
    print('10. Vendedor')
    print('======================================================')
    print('11. Eliminarar Venta por ID')
    print('======================================================')
    print('12. Salir')
    print('======================================================')

def ingresar_cliente():
    while True:
        try:
            cliente = input('Ingrese el cliente: ')
            if cliente:
                return cliente
            print("Error, debe ingresar el cliente... ")
        except Exception as error:
            print(f'Error inesperado: {error}')

def ingresar_monto_total():
    while True:
        try:
            monto_total = round(
                float(input('Ingrese el monto total de la venta: ')), 2)
            if monto_total > 0:
                return monto_total
            else:
                print('El monto total debe ser mayor a cero.')
        except ValueError:
            print('Error, debe ingresar un número valido.')

def ingresar_productos():
    while True:
        try:
            """ productos = input(
                'Ingrese los productos (separados por coma): ').split(',')
            productos = [prod.strip()for prod in productos if prod.strip()] """
            productos = input('Ingrese los productos (separados por coma): ')
            if productos:
                return productos
            else:
                print('Error, Debe ingresar al menos un producto válido.')
        except ValueError:
            print('Error, ha ocurrido un error al procesar los datos ingresados.-')

def ingresar_direccion_envio():
    while True:
        try:
            direccion_envio = input('Ingrese la dirección del envio: ')
            if direccion_envio:
                return direccion_envio
            else:
                print('Error, debe ingresar alguna dirección.')
        except ValueError:
            print(
                'Error, ha ocurrido un error al procesar los datos ingresados.-')

def ingresar_vendedor():
    while True:
        try:
            vendedor = input('Ingrese el vendedor: ')
            if vendedor:
                return vendedor
            else:
                print('Error, debe ingresar el vendedor.')
        except ValueError:
            print(
                'Error, ha ocurrido un error al procesar los datos ingresados.-')

def ingresar_buscar_id():
    while True:
        try:
            id = int(input('Ingrese la ID de la venta que quiere buscar: '))
            if id > 0:
                return str(id)
            else:
                print('Error, la ID debe ser un numero entero positivo.')
            print("Error, debe ingresar la ID... ")
        except ValueError:
            print('Error: debe ingresar un número entero.')

def ingresar_crear_id():
    while True:
        try:
            id = int(input('Ingrese la ID de la venta que quiere agregar: '))
            if id < 0:
                print('Error, la ID debe ser un numero entero positivo.')
            elif (gestion.leer_venta(id)):
                print('Error, la ID ya existe, debe ingresar otro valor.')
            else:
                return str(id)
        except ValueError:
            print('Error: debe ingresar un número entero.')

def agregar_venta(gestion, tipo_venta):
    try:
        id_venta = ingresar_crear_id()
        fecha = datetime.datetime.now().strftime("%d-%m-%y")
        cliente=ingresar_cliente()
        monto_total= ingresar_monto_total()
        productos= ingresar_productos()

        if tipo_venta == '1':
            direccion_envio= ingresar_direccion_envio()
            venta = VentaOnline(id_venta,fecha,cliente,productos,monto_total, direccion_envio)
        elif tipo_venta == '2':
            vendedor= ingresar_vendedor()        
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
    try:
        id_venta = ingresar_id()
        gestion.leer_venta(id_venta)
    except Exception as e:
        print(f'Error al buscar {e}')
    print('=====================================================================')    
    input('Presione enter para continuar...')

def actualizar_monto_total_venta(gestion):
    try:
        id_venta = ingresar_buscar_id()
        if gestion.leer_venta(id_venta):
            venta = gestion.leer_venta(id_venta)
            print(f"El monto de la venta que quiere actualizar es: {venta.monto_total}")
            nuevo_monto_total = ingresar_monto_total()
            gestion.actualizar_monto_total(id_venta, nuevo_monto_total)
    except Exception as e:
        print(f'Error al actualizar {e}')
    print('=====================================================================')    
    input('Presione enter para continuar...')

def actualizar_cliente(gestion):
    try:
        id_venta = ingresar_buscar_id()
        if gestion.leer_venta(id_venta):
            venta = gestion.leer_venta(id_venta)
            print(f"El cliente que quiere actualizar es: {venta.cliente}")
            nuevo_cliente =ingresar_cliente()
            gestion.actualizar_cliente(id_venta, nuevo_cliente)
    except Exception as e:
        print(f'Error al actualizar {e}')
    print('=====================================================================')    
    input('Presione enter para continuar...')

def actualizar_productos(gestion):
    try:
        id_venta = ingresar_buscar_id()
        if gestion.leer_venta(id_venta):
            venta = gestion.leer_venta(id_venta)
            print(f"Los productos que quiere actualizar son: {venta.productos}")
            nuevos_productos = ingresar_productos()
            gestion.actualizar_productos(id_venta, nuevos_productos)
    except Exception as e:
        print(f'Error al actualizar {e}')
    print('=====================================================================')    
    input('Presione enter para continuar...')

def actualizar_direccion_envio(gestion):
    try:
        id_venta = ingresar_buscar_id()
        if gestion.leer_venta(id_venta):
            venta = gestion.leer_venta(id_venta)
            if isinstance(venta, VentaOnline):
                print(f"La direccion que quiere actualizar es: {venta.direccion_envio}")
                nueva_direccion = ingresar_direccion_envio()
                gestion.actualizar_direccion_envio(id_venta, nueva_direccion)
            else:
                print('No existe una venta OnLIne Con esa ID.')
    except Exception as e:
        print(f'Error al actualizar {e}')
    print('=====================================================================')    
    input('Presione enter para continuar...')

def actualizar_vendedor(gestion):
    try:
        id_venta = ingresar_buscar_id()
        if gestion.leer_venta(id_venta):
            venta= gestion.leer_venta(id_venta)
            if isinstance(venta,VentaLocal):
                print(f"El vendedor que quiere actualizar es: {venta.vendedor}")
                nuevo_vendedor = ingresar_vendedor()
                gestion.actualizar_vendedor(id_venta, nuevo_vendedor)
            else:
                print('No existe una venta Local con  esa ID')
    except Exception as e:
        print(f'Error al actualizar {e}')
    print('=====================================================================')    
    input('Presione enter para continuar...')

def eliminar_venta_por_id(gestion):
    try:
        id_venta = ingresar_buscar_id()
        gestion.eliminar_venta(id_venta)
    except Exception as e:
        print(f'Error al eliminar la venta {e}')
    print('=====================================================================')    
    input('Presione enter para continuar...')

def mostrar_todas_las_ventas(gestion):
    try:
        print('=============== Listado completa de las  Ventas ==============')
        ventas= gestion.leer_todas_las_ventas()
        for venta in ventas:
            if isinstance(venta, VentaOnline):
                print(f"id: {venta.id_venta} - CLiente {venta.cliente} - Monto: ${(venta.monto_total):.2f} - VENTA ONLINE - Dirección envío: {venta.direccion_envio}")
            elif isinstance(venta,VentaLocal):
                print(f"id: {venta.id_venta} - CLiente {venta.cliente} - Monto: ${(venta.monto_total):.2f} - VENTA LOCAL - Vendedor: {venta.vendedor}")
    except Exception as e:
        print(f'Error al mostrar las ventas {e}')
    print('=====================================================================')
    input('Presione enter para continuar...')

def mostrar_todas_las_ventas_online(gestion):
    try:
        print('=============== Listado completo de las  Ventas Online ==============')
        for venta in gestion.leer_todas_las_ventas():
            if isinstance(venta, VentaOnline):
                    print(f"id: {venta.id_venta} - CLiente {venta.cliente} - Monto: ${(venta.monto_total):.2f} - VENTA ONLINE - Dirección envío: {venta.direccion_envio}")
    except Exception as e:
        print(f'Error al mostrar las ventas {e}')
    print('=====================================================================')
    input('Presione enter para continuar...')

def mostrar_todas_las_ventas_local(gestion):
    try:
        print('=============== Listado completo de las  Ventas Local ==============')
        for venta in gestion.leer_todas_las_ventas():
            if isinstance(venta, VentaLocal):
                print(f"id: {venta.id_venta} - CLiente {venta.cliente} - Monto: ${(venta.monto_total):.2f} - VENTA LOCAL - Vendedor: {venta.vendedor}")
    except Exception as e:
        print(f'Error al mostrar las ventas {e}')
    print('=====================================================================')
    input('Presione enter para continuar...')

if __name__ == '__main__':
    gestion = GestionVentas()

    while True:
        limpiar_pantalla()
        mostrar_menu()
        opcion = input('Seleccione una opción: ')

        if opcion == '1' or opcion == '2':
            agregar_venta(gestion, opcion)
        elif opcion == '3':
            mostrar_todas_las_ventas(gestion)
        elif opcion == '4':
            mostrar_todas_las_ventas_online(gestion)
        elif opcion == '5':
            mostrar_todas_las_ventas_local(gestion)
        elif opcion == '6':
            actualizar_monto_total_venta(gestion)
        elif opcion == '7':
            actualizar_cliente(gestion)
        elif opcion == '8':
            actualizar_productos(gestion)
        elif opcion == '9':
            actualizar_direccion_envio(gestion)
        elif opcion == '10':
            actualizar_vendedor(gestion)
        elif opcion == '11':
            eliminar_venta_por_id(gestion)
        elif opcion == '12':
            print('Saliendo del programa...')
            break
        else:
            print('Opción no válida. Por favor, seleccione una opción válida (1-6)')
