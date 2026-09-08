# PadelCenter – Demo (Docker)

## Requisitos
- Tener instalado **Docker Desktop** (Windows/Mac) y estar corriendo.

## Cómo levantar la aplicación

1. Descomprimir la carpeta del proyecto en cualquier ubicación.
2. Abrir una terminal (o PowerShell) dentro de esa carpeta, donde está el archivo `docker-compose.yml`.
3. Ejecutar:

   ```
   docker compose up
   ```

   La primera vez tarda un par de minutos (descarga la imagen base e instala dependencias). Las siguientes veces es casi instantáneo.

4. Abrir el navegador en:

   ```
   http://localhost:8501
   ```

## Para detener la aplicación
En la misma terminal, presionar `Ctrl + C`, o ejecutar en otra terminal:
```
docker compose down
```

## Notas
- Esta es una versión **demo sin persistencia**: los datos cargados (cuentas, pedidos, etc.) viven solo en la sesión del navegador mientras el contenedor está corriendo. Si se reinicia el contenedor, se pierde la información cargada.
- Si el puerto 8501 ya está en uso en la máquina del cliente, se puede cambiar en `docker-compose.yml`, en la línea `ports`, por ejemplo `"8080:8501"`, y luego acceder por `http://localhost:8080`.
