# API de Tareas (To-Do)

Ejemplo sencillo de creación de una API gestionada con `Flask` y `Flask-RESTful` que permite realizar operaciones CRUD (Crear, Leer, Actualizar, Eliminar) en una lista de tareas (To-Do).

<strong>Cuidado/Importante:</strong> Este código no tiene implementada lógica para evitar errores.

## Librerías necesarias
- Flask: (`pip install flask`) Framework web ligero en Python que facilita la creación de aplicaciones web.
- Flask-RESTful: (`pip install flask-restful`) Extensión de Flask que facilita la creación de servicios web RESTful en Python.

## Conceptos

En este repositorio aparecen diferentes conceptos que debemos entender.

- <strong>API:</strong> Son las siglas de Interfaz de Programación de Aplicaciones y define cómo interactuar con un software o servicio, permitiendo la comunicación entre diferentes sistemas informáticos.
- <strong>Protocolo HTTP:</strong> Protocolo de Transferencia de Hipertexto, define cómo se comunican los navegadores web y los servidores web, facilitando la transferencia de datos.
- <strong>GET:</strong> Método de solicitud en HTTP utilizado para obtener datos de un recurso específico en un servidor. Los datos se envían a través de la URL.
- <strong>POST:</strong> Método de solicitud en HTTP utilizado para enviar datos al servidor para crear o actualizar un recurso. Los datos se envían en el cuerpo del mensaje HTTP.
- <strong>PUT:</strong> Método de solicitud en HTTP utilizado para enviar datos al servidor para crear o actualizar un recurso. Se usa típicamente para actualizar recursos existentes.
- <strong>DELETE:</strong> Método de solicitud en HTTP utilizado para solicitar al servidor que elimine un recurso específico. Se espera que la eliminación sea irreversible.
- <strong>"Parsear"</strong> es un término informático que se refiere al proceso de analizar una cadena de caracteres o datos en un formato específico, como un lenguaje de programación o un formato estructurado, para extraer información o realizar operaciones sobre ella.

## Uso

1. Ejecuta la aplicación Flask:

    ```bash
    python app.py
    ```

2. Una vez la aplicación está activa estará disponible en nuestro servidor local, `http://localhost:5000`.

3. Teniendo en cuenta que hemos creado una API, vamos interactuar con la API utilizando herramientas como `cURL` desde la terminal. Aquí hay algunos ejemplos de cómo hacerlo:

   - Para obtener detalles de una tarea específica:
     ```bash
     curl http://localhost:5000/todos/todo1
     ```

   - Para crear una nueva tarea:
     ```bash
     curl -X POST -H "Content-Type: application/json" -d "{\"task\": \"Crear bbdd no relacional de una tienda de ropa.\"}" http://localhost:5000/todos/todo1
     ```

   - Para actualizar una tarea existente:
     ```bash
     curl -X PUT -H "Content-Type: application/json" -d "{\"task\": \"Crear bbdd no relacional Y SISTEMA GESTIÓN USUARIOS de una tienda de ropa.\"}" http://localhost:5000/todos/todo1
     ```

   - Para eliminar una tarea existente:
     ```bash
     curl -X DELETE http://localhost:5000/todos/todo1
     ```

A la hora de emplear `cURL` hemos definido diferentes parámetros:

  - `-X`: Especifica el método HTTP a utilizar en la solicitud. Por ejemplo, `-X GET` realiza una solicitud `GET`, `-X POST` realiza una solicitud `POST`, etc.

  - `-d`: Envía datos en el cuerpo de la solicitud. Por ejemplo, `-d "param1=value1&param2=value2"` envía datos con los parámetros y valores especificados al servidor. Aclaración, si nos fijamos en el ejemplo de uso, veremos que he añadido barras invertidas a las comillas interiores, esto se debe a que la consola que yo empleo necesita entender que las comillas interiores son parte del string y no parte del cuerpo de la solicitud.

  - `-H`: Permite agregar encabezados personalizados a la solicitud HTTP. Por ejemplo, `-H "Content-Type: application/json"` establece el encabezado Content-Type como application/json.

## Endpoints

### `GET /todos/<string:todo_id>`

Devuelve los detalles de una tarea específica.

#### Parámetros de URL

- `todo_id`: ID único de la tarea.

#### Ejemplo de solicitud

```bash
curl http://localhost:5000/todos/todo1
```

#### Respuesta

```json
{
    "task": "Acabar proyecto EDD."
}
```

### `POST /todos/<string:todo_id>`

Crea una nueva tarea.

#### Parámetros de URL

- `todo_id`: ID único de la tarea.

#### Parámetros de cuerpo (JSON)

- `task`: Descripción de la tarea.

#### Ejemplo de solicitud

```bash
curl -X POST -H "Content-Type: application/json" -d '{"task": "Crear bbdd no relacional de una tienda de ropa."}' http://localhost:5000/todos/todo2
```

#### Respuesta

```json
{
    "task": "Crear bbdd no relacional de una tienda de ropa."
}
```

### `PUT /todos/<string:todo_id>`

Actualiza una tarea existente.

#### Parámetros de URL

- `todo_id`: ID único de la tarea.

#### Parámetros de cuerpo (JSON)

- `task`: Nueva descripción de la tarea.

#### Ejemplo de solicitud

```bash
curl -X PUT -H "Content-Type: application/json" -d '{"task": "Crear bbdd no relacional Y SISTEMA GESTIÓN USUARIOS de una tienda de ropa."}' http://localhost:5000/todos/todo2
```

#### Respuesta

```json
{
    "task": "Crear bbdd no relacional Y SISTEMA GESTIÓN USUARIOS de una tienda de ropa."
}
```

### `DELETE /todos/<string:todo_id>`

Elimina una tarea existente.

#### Parámetros de URL

- `todo_id`: ID único de la tarea.

#### Ejemplo de solicitud

```bash
curl -X DELETE http://localhost:5000/todos/todo2
```

#### Respuesta

La respuesta será vacía y el estado de la respuesta será 204 (Sin contenido).