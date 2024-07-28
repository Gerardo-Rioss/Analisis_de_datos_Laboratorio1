import datetime
import json
class Venta:
    def __init__(self,idVenta, fecha, cliente, productos, montoTotal):
        self.idVenta = idVenta
        self.fecha = fecha
        self.cliente = cliente
        self.montoTotal = self.validarMontoTotal(montoTotal)
        self.productos = productos 

        @property
        def idVenta(self):
            return self.__idVenta
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
        def montoTotal(self):
            return self.__montoTotal
        
        @montoTotal.setter
        def montoTotal(self, nuevoMontoTotal):
            self.__montoTotal = self.validarMontoTotal(self, nuevoMontoTotal)

    
    def validarMontoTotal(self, monto):
        try:
            montoTotalNum = float(monto)
            if montoTotalNum <= 0:
                raise ValueError("El monto total debe ser un valor numérico positivo.")
            return montoTotalNum
        except ValueError:
            raise ValueError("El monto total debe ser un número válido.")

    
    def __str__(self):
        return f'ID venta: {self.idVenta}, Fecha: {self.fecha}, Cliente: {self.cliente}, Monto Total: {self.montoTotal}, Productos: {self.productos}'
    
    def to_dict(self):
        return {
            'idVenta': self.idVenta,
            'fecha': self.fecha,
            'cliente': self.cliente,
            'montoTotal': self.montoTotal,
            'productos': self.productos,
        }

class VentaOnline(Venta):
    def __init__(self, idVenta, fecha, cliente, productos, montoTotal, direccionEnvio,):
        super().__init__(idVenta, fecha, cliente, productos, montoTotal)
        self.direccionEnvio= direccionEnvio

    @property
    def direccionEnvio(self):
        return self.__direccionEnvio

    def __str__(self):
        return f'{super().__str__()}, Dirrección envio: {self.direccionEnvio}'

    def to_dict(self):
        data=super().to_dict()
        data['direccionEnvio']=self.direccionEnvio
        return data

class VentaLocal(Venta):
    def __init__(self, idVenta, fecha, cliente, productos, montoTotal, vendedor):
        super().__init__(idVenta, fecha, cliente, productos, montoTotal)
        self.vendedor= vendedor
    
    @property
    def vendedor(self):
        return self.__vendedor

    def __str__(self):
        return f'{super().__str__()},  Vendedor: {self.vendedor}'

    def to_dict(self):
        data = super().to_dict()
        data['vendedor'] = self.vendedor
        return data

class GestionVentas:
    def __init__(self, archivo):
        self.archivo = archivo
        

    def leerDatos(self):
        try:
            with open(self.archivo, 'r') as file:
                datos = json.load(file)
        except FileNotFoundError:
            return {}
        except Exception as error:
            raise Exception(f'Error al leer datos del archivo: {error}')
        else:
            return datos

    def guardarDatos(self, datos):
        try:
            with open(self.archivo, 'w') as file:
                json.dump(datos, file, indent=4)
        except IOError as error:
            print(
                f'Error al intentar guardar los datos en {self.archivo}: {error}')
        except Exception as error:
            print(f'Error inesperado: {error}')

    def crearVenta(self, venta):
        try:
            datos = self.leerDatos()
            idVenta = venta.idVenta
            if not str(idVenta) in datos.keys():
                datos[idVenta] = venta.to_dict()
                self.guardarDatos(datos)
                print(f"Fecha: {venta.fecha}, Cliente: {venta.cliente}...la venta se guardo correctamente.")
            else:
                print(f"Ya existe la venta con el mismo id '{idVenta}'.")
        except Exception as error:
            print(f'Error inesperado al crear la venta: {error}')

    def leerVenta(self, idVenta):
        try:
            datos = self.leerDatos()
            if idVenta in datos:
                venta_data = datos[idVenta]
                if 'direccionEnvio' in venta_data:
                    venta = VentaOnline(**venta_data)
                else:
                    venta = VentaLocal(**venta_data)
                print(f'Se econtro con éxito la venta con id: {idVenta}')
            else:
                print(f'No se encontró la venta con id: {idVenta}')
        except Exception as e:
            print('Error al leer venta: {e}')
    
    def actualizarMontoTotal(self, idVenta, nuevoMontoTotal):
        try:
            datos = self.leerDatos()
            if str(idVenta) in datos.keys():
                datos[idVenta]['montoTotal'] = nuevoMontoTotal
                self.guardarDatos(datos)
                print(f'El monto total de la venta con id:{idVenta}, fue actualiozado con éxito')
            else:
                print(f'No se encontró venta con la id:{idVenta}')
        except Exception as e:
            print(f'Error al actualizar la venta: {e}')

    def eliminarVenta(self, idVenta):
        try:
            datos = self.leerDatos()
            if str(idVenta) in datos.keys():
                del datos[idVenta]
                self.guardarDatos(datos)
                print(f'La venta con la id:{idVenta} se ha eliminado correctamente')
            else:
                print(f'No se encontró la venta con la id:{idVenta}')
        except Exception as e:
            print(f'Error al eliminar la venta: {e}')

    

