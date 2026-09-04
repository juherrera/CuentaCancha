import streamlit as st  # type: ignore[import-not-found]

productos_disponibles = [
    {"nombre": "Bebida", "precio": 2000, "icono": "🥤"},
    {"nombre": "Kit de pelotas", "precio": 8000, "icono": "🏓"},
    {"nombre": "Agua", "precio": 1500, "icono": "💧"},
]

if "cuentas" not in st.session_state:
    st.session_state.cuentas = []

if "pedidos" not in st.session_state:
    st.session_state.pedidos = {}

if "cuenta_seleccionada" not in st.session_state:
    st.session_state.cuenta_seleccionada = None


def calcular_total_cuenta(cuenta_actual, pedidos_actuales):
    base = cuenta_actual.get("total_base", cuenta_actual.get("total", 0))
    total_pedidos = sum(item.get("precio", 0) * item.get("cantidad", 0) for item in pedidos_actuales)
    return base + total_pedidos


def guardar_total_cuenta(indice, pedidos_actuales):
    cuenta_actual = st.session_state.cuentas[indice]
    cuenta_actual["pedidos"] = pedidos_actuales
    cuenta_actual["total"] = calcular_total_cuenta(cuenta_actual, pedidos_actuales)


def volver_a_cuentas():
    st.session_state.cuenta_seleccionada = None
    st.switch_page("app.py")


indice_cuenta = st.session_state.get("cuenta_seleccionada")
cuenta = None

if indice_cuenta is None or indice_cuenta >= len(st.session_state.cuentas):
    st.warning("No hay una cuenta seleccionada.")
    if st.button("Volver a cuentas"):
        st.session_state.cuenta_seleccionada = None
        st.switch_page("app.py")
    st.stop()

cuenta = st.session_state.cuentas[indice_cuenta]
cuenta.setdefault("estado", "Abierta")
cuenta.setdefault("total_base", cuenta.get("total", 0))
cuenta_pedidos = st.session_state.pedidos.setdefault(indice_cuenta, cuenta.get("pedidos", []))

if st.button("← Volver"):
    st.session_state.cuenta_seleccionada = None
    st.switch_page("app.py")
col_izquierda, col_derecha = st.columns([1.4, 1])

with col_izquierda:
    st.subheader("Agregar productos")

    for producto in productos_disponibles:
        nombre = producto["nombre"]
        precio = producto["precio"]
        icono = producto["icono"]

        with st.container():
            col_prod, col_precio, col_cantidad, col_boton = st.columns([2.2, 1, 1, 1])

            with col_prod:
                st.markdown(f"{icono} {nombre}")

            with col_precio:
                st.markdown(f"${precio:,.0f}")

            with col_cantidad:
                cantidad = st.number_input(
                    "Cantidad",
                    min_value=0,
                    max_value=20,
                    value=0,
                    step=1,
                    key=f"qty_{indice_cuenta}_{nombre}",
                    label_visibility="collapsed",
                )

            with col_boton:
                if st.button("Agregar", key=f"add_{indice_cuenta}_{nombre}"):
                    if cantidad > 0:
                        item_existente = next((item for item in cuenta_pedidos if item["nombre"] == nombre), None)
                        if item_existente:
                            item_existente["cantidad"] += cantidad
                        else:
                            cuenta_pedidos.append({
                                "nombre": nombre,
                                "precio": precio,
                                "cantidad": cantidad,
                            })

                        guardar_total_cuenta(indice_cuenta, cuenta_pedidos)
                        st.success(f"{cantidad} {nombre} agregado(s)")
                        st.rerun()

with col_derecha:
    col_guardar, col_cobrar = st.columns(2)
    with col_guardar:
        if st.button("Guardar cambios"):
            guardar_total_cuenta(indice_cuenta, cuenta_pedidos)
            st.success("Cambios guardados")

    with col_cobrar:
        if st.button("Cobrar cuenta"):
            st.session_state.cuenta_seleccionada = indice_cuenta
            st.switch_page("pages/Cobrar.py")

    if st.session_state.cuentas[indice_cuenta].get("estado") in ["Cobrada", "COBRADA"]:
        st.info("Esta cuenta ya fue cobrada.")

    st.subheader("Detalle de la cuenta")
    st.markdown(f"**Cancha:** {cuenta['cancha']}", help=None)
    st.markdown(f"**Responsable:** {cuenta['responsable']}", help=None)
    st.markdown(f"**Fecha:** {cuenta['fecha']}", help=None)
    st.markdown(f"**Horario:** {cuenta['hora_inicio']} - {cuenta['hora_fin']}", help=None)
    st.markdown(
        "<style>div[data-testid='stMarkdownContainer'] p { margin: 0.15rem 0 !important; line-height: 1.3 !important; }</style>",
        unsafe_allow_html=True,
    )

    base_court = st.number_input(
        "Base de cancha",
        min_value=0,
        value=cuenta.get("total_base", 0),
        step=500,
        key=f"base_court_{indice_cuenta}",
    )
    if base_court != cuenta.get("total_base", 0):
        cuenta["total_base"] = base_court
        guardar_total_cuenta(indice_cuenta, cuenta_pedidos)

    if not cuenta_pedidos:
        st.info("Aún no hay productos agregados.")
    else:
        subtotal_productos = 0
        for item in cuenta_pedidos:
            subtotal = item["precio"] * item["cantidad"]
            subtotal_productos += subtotal
            col_item, col_precio, col_eliminar = st.columns([3, 1.2, 0.7])
            with col_item:
                st.markdown(f"{item['nombre']} x{item['cantidad']}", help=None)
            with col_precio:
                st.markdown(f"${subtotal:,.0f}", help=None)
            with col_eliminar:
                if st.button("✕", key=f"del_{indice_cuenta}_{item['nombre']}"):
                    cuenta_pedidos.remove(item)
                    guardar_total_cuenta(indice_cuenta, cuenta_pedidos)
                    st.rerun()

        st.markdown("---")
        total_final = calcular_total_cuenta(cuenta, cuenta_pedidos)
        st.markdown(
            f"<div style='display:flex; justify-content:space-between; font-size:1.1rem;'><span>Base de cancha</span><strong>${cuenta.get('total_base', 0):,.0f}</strong></div>",
            unsafe_allow_html=True,
        )
        st.markdown(
            f"<div style='display:flex; justify-content:space-between; font-size:1.1rem;'><span>Productos</span><strong>${subtotal_productos:,.0f}</strong></div>",
            unsafe_allow_html=True,
        )
        st.markdown("---")
        st.markdown(f"<h3 style='text-align: right;'>TOTAL ${total_final:,.0f}</h3>", unsafe_allow_html=True)

