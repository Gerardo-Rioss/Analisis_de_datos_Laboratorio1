import datetime
import json
class Venta:
    def __init__(self,id_venta, fecha, cliente, productos, monto_total):
        self.id_venta = id_venta
        self.fecha = fecha
        self.cliente = cliente
        self.monto_total = self.validar_monto_total(monto_total)
        self.productos = productos 

        @property
        def id_venta(self):
            return self.__id_venta
        @property
        def fecha(self):
            return self.__fecha
        @property
        def cliente(self):
            return self.__cliente
        @property
        def productos(self):
            return self.__productos
        @property
        def monto_total(self):
            return self.__monto_total
        
        @monto_total.setter
        def monto_total(self, nuevo_monto_total):
            self.__monto_total = self.validar_Monto_Total(self, nuevo_monto_total)

        @cliente.setter
        def cliente(self, nuevo_cliente):
            self.__cliente = nuevo_cliente
        
        @productos.setter
        def productos(self,nuevos_productos):
            self.__productos= nuevos_productos
    
    def validar_monto_total(self, monto):
        try:
            monto_total_num = float(monto)
            if monto_total_num <= 0:
                raise ValueError("El monto total debe ser un valor numérico positivo.")
            return monto_total_num
        except ValueError:
            raise ValueError("El monto total debe ser un número válido.")

    def __str__(self):
        return f'ID venta: {self.id_venta}, Fecha: {self.fecha}, Cliente: {self.cliente}, Monto Total: {self.monto_total}, Productos: {self.productos}'
    
    def to_dict(self):
        return {
            'id_venta': self.id_venta,
            'fecha': self.fecha,
            'cliente': self.cliente,
            'monto_total': self.monto_total,
            'productos': self.productos,
        }

class VentaOnline(Venta):
    def __init__(self, id_venta, fecha, cliente, productos, monto_total, direccion_envio,):
        super().__init__(id_venta, fecha, cliente, productos, monto_total)
        self.direccion_envio= direccion_envio

    @property
    def direccion_envio(self):
        return self.__direccion_envio
    
    @direccion_envio.setter
    def direccion_envio(self, nueva_direccion_envio):
        self.__direccion_envio = nueva_direccion_envio

    def __str__(self):
        return f'{super().__str__()}, Dirección envio: {self.direccion_envio}'

    def to_dict(self):
        data=super().to_dict()
        data['direccion_envio']=self.direccion_envio
        return data

class VentaLocal(Venta):
    def __init__(self, id_venta, fecha, cliente, productos, monto_total, vendedor):
        super().__init__(id_venta, fecha, cliente, productos, monto_total)
        self.vendedor= vendedor
    
    @property
    def vendedor(self):
        return self.__vendedor
    
    @vendedor.setter
    def vendedor(self, nuevo_vendedor):
        self.__vendedor = nuevo_vendedor

    def __str__(self):
        return f'{super().__str__()},  Vendedor: {self.vendedor}'

    def to_dict(self):
        data = super().to_dict()
        data['vendedor'] = self.vendedor
        return data

class GestionVentas:
    def __init__(self, archivo):
        self.archivo = archivo
        
    def leer_datos(self):
        try:
            with open(self.archivo, 'r') as file:
                datos = json.load(file)
        except FileNotFoundError:
            return {}
        except Exception as error:
            raise Exception(f'Error al leer datos del archivo: {error}')
        else:
            return datos

    def guardar_datos(self, datos):
        try:
            with open(self.archivo, 'w') as file:
                json.dump(datos, file, indent=4)
        except IOError as error:
            print(
                f'Error al intentar guardar los datos en {self.archivo}: {error}')
        except Exception as error:
            print(f'Error inesperado: {error}')

    def crear_venta(self, venta):
        try:
            datos = self.leer_datos()
            id_venta = str(venta.id_venta)
            if not str(id_venta) in datos.keys():
                datos[id_venta] = venta.to_dict()
                self.guardar_datos(datos)
                print(f"Fecha: {venta.fecha}, Cliente: {venta.cliente}...la venta se guardo correctamente.")
            else:
                print(f"Ya existe la venta con el mismo id '{id_venta}'.")
        except Exception as error:
            print(f'Error inesperado al crear la venta: {error}')

    def leer_venta(self, id_venta):
        try:
            datos = self.leer_datos()
            if id_venta in datos:
                venta_data = datos[id_venta]
                if 'direccion_envio' in venta_data:
                    venta = VentaOnline(**venta_data)
                else:
                    venta = VentaLocal(**venta_data)
                return venta
            
        except Exception as e:
            print('Error al leer venta: {e}')
    
    def actualizar_monto_total(self, id_venta, nuevo_monto_total):
        try:
            datos = self.leer_datos()
            if str(id_venta) in datos.keys():
                datos[id_venta]['monto_total'] = nuevo_monto_total
                self.guardar_datos(datos)
                print(f'El monto total de la venta con id: {id_venta}, fue actualizado con éxito')
            else:
                print(f'No se encontró venta con la id:{id_venta}')
        except Exception as e:
            print(f'Error al actualizar la venta: {e}')
    
    def actualizar_cliente(self, id_venta, nuevo_cliente):
        try:
            datos= self.leer_datos()
            if str(id_venta) in datos.keys():
                datos[id_venta]['cliente']= nuevo_cliente
                self.guardar_datos(datos)
                print('El cliente ha sido modificado con éxito')
            else:
                print(f'No se encontró venta con la id:{id_venta}')
        except Exception as e:
            print(f'Error al actualizar la venta: {e}')

    def actualizar_productos(self, id_venta, nuevos_producto):
        try:
            datos = self.leer_datos()
            if str(id_venta) in datos.keys():
                datos[id_venta]['productos'] = nuevos_producto
                self.guardar_datos(datos)
                print('Los productos han sido modificados con éxito')
            else:
                print(f'No se encontró venta con la id:{id_venta}')
        except Exception as e:
            print(f'Error al actualizar la venta: {e}')
    
    def actualizar_direccion_envio(self, id_venta, nueva_direccion_envio):
        try:
            datos = self.leer_datos()
            if str(id_venta) in datos.keys():
                datos[id_venta]['direccion_envio'] = nueva_direccion_envio
                self.guardar_datos(datos)
                print('Los dirección del envio se ha modificados con éxito')
            else:
                print(f'No se encontró venta con la id:{id_venta}')
        except Exception as e:
            print(f'Error al actualizar la venta: {e}')
    
    def actualizar_vendedor(self, id_venta, nuevo_vendedor):
        try:
            datos = self.leer_datos()
            if str(id_venta) in datos.keys():
                datos[id_venta]['vendedor'] = nuevo_vendedor
                self.guardar_datos(datos)
                print('El vendedor se ha modificados con éxito')
            else:
                print(f'No se encontró venta con la id:{id_venta}')
        except Exception as e:
            print(f'Error al actualizar la venta: {e}')

    def eliminar_venta(self, id_venta):
        try:
            datos = self.leer_datos()
            if str(id_venta) in datos.keys():
                del datos[id_venta]
                self.guardar_datos(datos)
                print(f'La venta con la id:{id_venta} se ha eliminado correctamente')
            else:
                print(f'No se encontró la venta con la id:{id_venta}')
        except Exception as e:
            print(f'Error al eliminar la venta: {e}')
