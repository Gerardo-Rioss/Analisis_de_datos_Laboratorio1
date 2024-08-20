import mysql.connector
from mysql.connector import Error
from decouple import config
import datetime

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
    def __init__(self):
        self.host = config('DB_HOST')
        self.database = config('DB_NAME')
        self.user= config('DB_USER')
        self.password=config('DB_PASSWORD')
        self.port = config('DB_PORT')
        
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
    
    def connect(self):
        '''Establecer una conexión con la base de datos'''
        try:
            connection = mysql.connector.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password,
                port=self.port
            )

            if connection.is_connected():
                return connection

        except Error as e:
            print(f'Error al conectar a la base de datos: {e}')
            return None

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
            connection = self.connect()
            if connection:
                with connection.cursor() as cursor:
                    cursor.execute('SELECT id_venta FROM venta WHERE id_venta = %s', (venta.id_venta,))
                    if cursor.fetchone():
                        print(f'Error: Ya existe una venta con esa id: {venta.id_venta}')
                        return
                    
                    if isinstance(venta, VentaOnline):
                        query = '''
                        INSERT INTO venta (id_venta, fecha, cliente, monto_total, productos)
                        VALUES (%s, %s, %s, %s, %s)
                        '''
                        cursor.execute(query, (venta.id_venta, venta.fecha, venta.cliente, venta.monto_total, venta.productos))

                        query = '''
                        INSERT INTO ventaonline (id_venta, direccion_envio)
                        VALUES (%s, %s)
                        '''

                        cursor.execute(query, (venta.id_venta, venta.direccion_envio))

                    elif isinstance(venta, VentaLocal):
                        query = '''
                        INSERT INTO venta (id_venta, fecha, cliente, monto_total, productos)
                        VALUES (%s, %s, %s, %s, %s)
                        '''
                        cursor.execute(query, ( venta.id_venta, venta.fecha, venta.cliente, venta.monto_total, venta.productos))

                        query = '''
                        INSERT INTO ventalocal (id_venta, vendedor)
                        VALUES (%s, %s)
                        '''

                        cursor.execute(query, (venta.id_venta, venta.vendedor))

                    connection.commit()
                    print(f'Venta: {venta.id_venta},{venta.fecha}, {venta.cliente}, {venta.monto_total}, {venta.productos} creado correctamente')
        except Exception as error:
            print(f'Error inesperado al crear venta: {error}')

    def leer_venta_por_id(self, id_venta):
        try:
            connection = self.connect()
            if connection:
                with connection.cursor(dictionary=True) as cursor:
                    cursor.execute('SELECT * FROM venta WHERE id_venta = %s', (id_venta,))
                    venta_data = cursor.fetchone()

                    if venta_data:
                        cursor.execute('SELECT vendedor FROM ventalocal WHERE id_venta = %s', (id_venta,))
                        vendedor = cursor.fetchone()

                        if vendedor:
                            venta_data['vendedor'] = vendedor['vendedor']
                            venta = VentaLocal(**venta_data)
                        else:
                            cursor.execute('SELECT direccion_envio FROM ventaonline WHERE id_venta = %s', (id_venta,))
                            direccion_envio = cursor.fetchone()
                            if direccion_envio:
                                venta_data['direccion_envio'] = direccion_envio['direccion_envio']
                                venta = VentaOnline(**venta_data)
                            else:
                                venta = Venta(**venta_data)
                        print(f'Venta encontrada encontrado: {venta}')
                    else:
                        print(f'No se encontró la venta con id {id_venta}.')
        except Error as e:
            print('Error al leer venta: {e}')
        finally:
            if connection.is_connected():
                connection.close()
    
    def actualizar_monto_total(self, id_venta, nuevo_monto_total):
        try:
            connection = self.connect()
            if connection:
                with connection.cursor() as cursor:
                    cursor.execute('SELECT * FROM venta WHERE id_venta = %s', (id_venta,))
                    if not cursor.fetchone():
                        print(f'No se encontro ninguna venta con el Número {id_venta}.')
                        return
                    
                    cursor.execute('UPDATE venta SET monto_total = %s WHERE id_venta = %s', (nuevo_monto_total, id_venta))

                    if cursor.rowcount > 0:
                        connection.commit()
                        print(f'La venta con id: {id_venta} se actualizo correctamente.-')
                    else:
                        print(f'No se encontro venta con el numero: {id_venta}')

        except Exception as e:
            print(f'Error al actualizar venta: {e}')
        finally:
            if connection.is_connected():
                connection.close()
    
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
            connection = self.connect()
            if connection:
                with connection.cursor() as cursor:
                    cursor.execute('SELECT * FROM venta WHERE id_venta = %s', (id_venta,))
                    if not cursor.fetchone():
                        print(f'No se encontro la venta con el número: {id_venta}.')
                        return 
                    
                    cursor.execute('DELETE FROM ventalocal WHERE id_venta = %s', (id_venta,))
                    cursor.execute('DELETE FROM ventaonline WHERE id_venta = %s', (id_venta,))
                    cursor.execute('DELETE FROM venta WHERE id_venta = %s', (id_venta,))
                    if cursor.rowcount > 0:
                        connection.commit()
                        print(f'La venta con id: {id_venta} eliminado correctamente')
                    else:
                        print(f'No se encontró ninguna venta con id: {id_venta}')

        except Exception as e:
            print(f'Error al eliminar el colaborador: {e}')
        finally:
            if connection.is_connected():
                connection.close()

    def leer_todas_las_ventas(self):
        try:
            connection = self.connect()
            if connection:
                with connection.cursor(dictionary=True) as cursor:
                    cursor.execute('SELECT * FROM venta')
                    ventas_data = cursor.fetchall()
                    ventas = []
                    for venta_data in ventas_data:
                        id_venta = venta_data['id_venta']
                        cursor.execute('SELECT direccion_envio FROM ventaonline WHERE id_venta = %s', (id_venta,))
                        direccion_envio = cursor.fetchone()
                        if direccion_envio:
                            venta_data['direccion_envio'] = direccion_envio['direccion_envio']
                            venta = VentaOnline(**venta_data)
                        else:
                            cursor.execute('SELECT vendedor FROM ventalocal WHERE id_venta = %s', (id_venta,))
                            vendedor = cursor.fetchone()
                            venta_data['vendedor'] = vendedor['vendedor']
                            venta = VentaLocal(**venta_data)
                        ventas.append(venta)
        except Exception as e:
            print(f'Error al mostrar los ventas: {e}')
        else:
            return ventas
        finally:
            if connection.is_connected():
                connection.close()