import uasyncio as asyncio
import ujson
from config import Config

# Función principal para manejar el cliente, ahora acepta `config` como parámetro
async def handle_client_with_config(reader, writer, config):
    print("Nueva conexión establecida")
    
    try:
        # Leer solicitud HTTP
        request = await reader.read(1024)
        if not request:
            writer.close()
            await writer.wait_closed()
            return
        
        print("Solicitud recibida:", request.decode())
        
        # Parsear método y ruta
        method, path, _ = request.split(b' ', 2)
        method = method.decode()
        path = path.decode()

        # Responder a GET en /config
        if method == 'GET' and path == '/config':
            print("Procesando solicitud GET en /config")
            
            # Cargar configuración actualizada desde el archivo
            config.reload_config()

            response = {
                "led_blink_time": config.led_blink_time,
                "led_blink_quantity": config.led_blink_quantity,
                "st_mode": config.st_mode,
                "st_test": config.st_test,          
                
            }
            writer.write(b'HTTP/1.1 200 OK\r\n')
            writer.write(b'Content-Type: application/json\r\n\r\n')
            writer.write(ujson.dumps(response).encode())

        # Responder a PUT en /config
        elif method == 'PUT' and path == '/config':
            print("Procesando solicitud PUT en /config")
            
            # Separar encabezados y cuerpo
            headers, body_start = request.split(b'\r\n\r\n', 1)
            content_length = 0
            for header in headers.split(b'\r\n'):
                if header.lower().startswith(b'content-length:'):
                    content_length = int(header.split(b':')[1].strip())
            
            # Verificar y completar datos
            if len(body_start) < content_length:
                body_start += await reader.read(content_length - len(body_start))
            
            # Actualizar configuración
            data = ujson.loads(body_start)
            if "led_blink_time" in data:
                config.update_config("led_blink_time", data["led_blink_time"])
            if "led_blink_quantity" in data:
                config.update_config("led_blink_quantity", data["led_blink_quantity"])
            if "st_mode" in data:
                config.update_config("st_mode", data["st_mode"])
            if "st_test" in data:
                config.update_config("st_test", data["st_test"])
            
            # Guardar la nueva configuración en el archivo
            config.save_config()

            response = {"status": "OK", "message": "Configuración actualizada"}
            writer.write(b'HTTP/1.1 200 OK\r\n')
            writer.write(b'Content-Type: application/json\r\n\r\n')
            writer.write(ujson.dumps(response).encode())
        else:
            print("Ruta o método no soportados")
            writer.write(b'HTTP/1.1 404 Not Found\r\n\r\n')
        
    except Exception as e:
        print("Error manejando la solicitud:", e)
        writer.write(b'HTTP/1.1 500 Internal Server Error\r\n\r\n')

    # Cerrar la conexión
    await writer.drain()
    writer.close()
    await writer.wait_closed()

# Función para iniciar el servidor con `config` inyectado
async def start_server_with_config(config):
    #config = Config()    

    async def handle_client(reader, writer):
        await handle_client_with_config(reader, writer, config)

    try:
        print("Iniciando servidor...")
        server = await asyncio.start_server(handle_client, '0.0.0.0', 8080)
        print("Servidor iniciado en puerto 8080")
        await server.wait_closed()
    except Exception as e:
        print(f"Error al iniciar el servidor: {e}")


'''
{
    "st_test": true,
    "led_blink_quantity": 3,
    "st_mode": 0,
    "led_blink_time": 1000
}
'''