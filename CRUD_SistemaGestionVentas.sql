CREATE DATABASE SistemaGestionVentas;
USE SistemaGestionVentas;

CREATE TABLE Venta (
    id_venta INT PRIMARY KEY,
    fecha DATE NOT NULL,
    cliente VARCHAR(100) NOT NULL,
    monto_total DECIMAL(10, 2) NOT NULL,
    productos text NOT NULL
);

CREATE TABLE VentaOnline (
    id_venta INT PRIMARY KEY,
    direccion_envio TEXT,
    FOREIGN KEY (id_venta) REFERENCES Venta(id_venta)
);

CREATE TABLE VentaLocal (
    id_venta INT PRIMARY KEY,
    vendedor VARCHAR(100),
    FOREIGN KEY (id_venta) REFERENCES Venta(id_venta)
);