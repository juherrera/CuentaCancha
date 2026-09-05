import pandas as pd
import streamlit as st


st.set_page_config(page_title="Productos", layout="wide")


if "productos_catalogo" not in st.session_state:
    st.session_state.productos_catalogo = []

if "productos_catalogo_error" not in st.session_state:
    st.session_state.productos_catalogo_error = ""

if "productos_catalogo_exito" not in st.session_state:
    st.session_state.productos_catalogo_exito = ""


def generar_codigo_producto(id_producto, nombre, usados):
    nombre_limpio = "".join(ch for ch in str(nombre).strip().upper() if ch.isalnum())
    prefijo = nombre_limpio[:3] if nombre_limpio else "PRO"
    codigo_base = f"{prefijo}{id_producto}"
    codigo = codigo_base
    contador = 2
    while codigo in usados:
        codigo = f"{codigo_base}_{contador}"
        contador += 1
    usados.add(codigo)
    return codigo


def validar_catalogo_productos(df):
    columnas_esperadas = ["Icono", "Nombre", "Precio"]
    columnas_disponibles = {str(col).strip(): col for col in df.columns}
    columnas_faltantes = [col for col in columnas_esperadas if col.lower() not in {key.lower() for key in columnas_disponibles}]
    if columnas_faltantes:
        raise ValueError(
            "El archivo no tiene la estructura esperada. Debe incluir las columnas: "
            + ", ".join(columnas_esperadas)
        )

    columnas_renombradas = {
        columnas_disponibles.get(col, col): col
        for col in columnas_esperadas
        for key, value in columnas_disponibles.items()
        if key.lower() == col.lower()
    }
    df = df.rename(columns=columnas_renombradas)

    if df.empty:
        raise ValueError("El archivo está vacío. Debe contener al menos un producto válido.")

    productos = []
    usados = set()
    nombres_vistos = set()
    id_base = 1

    for indice, fila in df.iterrows():
        nombre = str(fila.get("Nombre", "")).strip()
        if not nombre:
            raise ValueError(f"La fila {indice + 2} tiene un nombre vacío.")

        nombre_normalizado = nombre.lower()
        if nombre_normalizado in nombres_vistos:
            raise ValueError(f"El producto '{nombre}' está duplicado dentro del archivo Excel.")
        nombres_vistos.add(nombre_normalizado)

        icono = str(fila.get("Icono", "")).strip() or "📦"
        precio_raw = fila.get("Precio")
        try:
            precio = float(precio_raw)
        except (TypeError, ValueError):
            raise ValueError(f"El producto '{nombre}' tiene un precio inválido.")
        if not pd.notna(precio) or precio <= 0:
            raise ValueError(f"El producto '{nombre}' debe tener un precio mayor que cero.")

        producto = {
            "ID": id_base,
            "Codigo_Producto": generar_codigo_producto(id_base, nombre, usados),
            "Icono": icono,
            "Nombre": nombre,
            "Precio": float(precio),
        }
        productos.append(producto)
        id_base += 1

    if not productos:
        raise ValueError("El archivo no contiene ningún producto válido para cargar.")

    return productos


def cargar_catalogo_desde_excel(archivo):
    if archivo is None:
        raise ValueError("Debes seleccionar un archivo Excel antes de cargar el catálogo.")

    nombre_archivo = str(archivo.name).lower()
    if not nombre_archivo.endswith((".xlsx", ".xls")):
        raise ValueError("El archivo debe ser un Excel válido (.xlsx o .xls).")

    try:
        engine = "openpyxl" if nombre_archivo.endswith(".xlsx") else "xlrd"
        df = pd.read_excel(archivo, engine=engine)
    except Exception as exc:
        raise ValueError(f"No se pudo leer el archivo Excel: {exc}") from exc

    if df.empty:
        raise ValueError("El archivo está vacío. Debe contener al menos un producto válido.")

    productos_nuevos = validar_catalogo_productos(df)
    st.session_state.productos_catalogo = productos_nuevos
    st.session_state.productos_catalogo_error = ""
    st.session_state.productos_catalogo_exito = (
        f"Catálogo cargado correctamente. Se registraron {len(productos_nuevos)} productos."
    )
    return productos_nuevos


if st.button("← Volver a principal"):
    st.switch_page("app.py")

st.title("🥤 Mantenedor de Productos")
st.caption("Carga un archivo Excel con el catálogo de productos para usarlo en la gestión de cuentas.")

archivo = st.file_uploader(
    "Selecciona un archivo Excel",
    type=["xlsx", "xls"],
    help="El archivo debe contener columnas: Icono, Nombre y Precio.",
)

if archivo is not None:
    st.info(f"Archivo cargado: {archivo.name}")

col_cargar, col_limpiar = st.columns([1, 1])
with col_cargar:
    if st.button("Cargar catálogo"):
        if archivo is None:
            st.error("Debes seleccionar un archivo Excel antes de cargar el catálogo.")
        else:
            try:
                cargar_catalogo_desde_excel(archivo)
                st.success(st.session_state.productos_catalogo_exito)
            except ValueError as exc:
                st.session_state.productos_catalogo_error = str(exc)
                st.error(str(exc))

with col_limpiar:
    if st.button("Limpiar catálogo actual"):
        st.session_state.productos_catalogo = []
        st.session_state.productos_catalogo_error = ""
        st.session_state.productos_catalogo_exito = "Catálogo vacío."
        st.warning("Se eliminó el catálogo actualmente cargado.")

if st.session_state.get("productos_catalogo_error"):
    st.error(st.session_state.productos_catalogo_error)

if st.session_state.get("productos_catalogo_exito") and not st.session_state.get("productos_catalogo_error"):
    st.success(st.session_state.productos_catalogo_exito)

catalogo_actual = st.session_state.get("productos_catalogo", [])
if not catalogo_actual:
    st.info("Todavía no hay productos cargados. Carga un Excel para comenzar.")
else:
    st.subheader("Catálogo actual")
    df_catalogo = pd.DataFrame(catalogo_actual, columns=["ID", "Codigo_Producto", "Icono", "Nombre", "Precio"])
    st.dataframe(df_catalogo, hide_index=True, width="stretch")
