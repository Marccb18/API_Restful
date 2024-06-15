markdown
Copy code
# API de Gestión Bancaria

Esta es una API simple para gestionar transacciones bancarias y deudas.

## Requisitos

- Python 3.x
- Flask
- Flask-Restful
- Flask-SQLAlchemy
- WTForms

## Instalación

1. Clona este repositorio:

git clone https://github.com/Marccb18/API_Restful.git

markdown
Copy code

2. Instala las dependencias:

pip install -r requirements.txt

markdown
Copy code

## Uso

Para ejecutar la API, simplemente ejecuta el archivo `app.py`:

python app.py

shell
Copy code

La API estará disponible en `http://127.0.0.1:5000`.

## Métodos de la API

### Transacciones

#### Obtener todas las transacciones

```bash
Obtener el saldo actual y balances
bash
Copy code
curl -X GET http://127.0.0.1:5000/finanzas
Obtener todas las transacciones
bash
Copy code
curl -X GET http://127.0.0.1:5000/transacciones
Obtener una transacción específica
bash
Copy code
curl -X GET http://127.0.0.1:5000/transacciones/1
Crear una nueva transacción
bash
Copy code
curl -X POST -H "Content-Type: application/json" -d '{"concepto": "Pago de factura", "cantidad": 100, "fecha": "01-05-2024", "descripcion": "Pago de factura de electricidad", "es_gasto": true}' http://127.0.0.1:5000/transacciones
Actualizar una transacción existente
bash
Copy code
curl -X PUT -H "Content-Type: application/json" -d '{"concepto": "Pago de factura de agua", "cantidad": 50, "fecha": "02-05-2024", "descripcion": "Pago de factura de agua", "es_gasto": true}' http://127.0.0.1:5000/transacciones/1
Eliminar una transacción
bash
Copy code
curl -X DELETE http://127.0.0.1:5000/transacciones/1
Deudas
Obtener todas las deudas
bash
Copy code
curl -X GET http://127.0.0.1:5000/deudas
Obtener una deuda específica
bash
Copy code
curl -X GET http://127.0.0.1:5000/deudas/1
Crear una nueva deuda
bash
Copy code
curl -X POST -H "Content-Type: application/json" -d '{"concepto": "Préstamo", "cantidad": 200, "deudor": "Juan Pérez", "fecha": "01-05-2024", "comentario": "Préstamo para compra de libro", "pagada": false}' http://127.0.0.1:5000/deudas
Actualizar una deuda existente
bash
Copy code
curl -X PUT -H "Content-Type: application/json" -d '{"concepto": "Préstamo para libro", "cantidad": 150, "deudor": "Juan Pérez", "fecha": "02-05-2024", "comentario": "Préstamo para compra de libro", "pagada": false}' http://127.0.0.1:5000/deudas/1
Eliminar una deuda
bash
Copy code
curl -X DELETE http://127.0.0.1:5000/deudas/1
