import streamlit as st

if "cuentas" not in st.session_state:
    st.session_state.cuentas = []

if "cuenta_seleccionada" not in st.session_state:
    st.session_state.cuenta_seleccionada = None


def volver_a_cuenta():
    st.switch_page("pages/GestionarCuenta.py")


indice_cuenta = st.session_state.get("cuenta_seleccionada")
if indice_cuenta is None or indice_cuenta >= len(st.session_state.cuentas):
    st.warning("No hay una cuenta seleccionada.")
    if st.button("Volver a cuentas"):
        st.session_state.cuenta_seleccionada = None
        st.switch_page("app.py")
    st.stop()

cuenta = st.session_state.cuentas[indice_cuenta]
cuenta.setdefault("estado", "Abierta")
cuenta.setdefault("total_base", cuenta.get("total", 0))
cuenta_pedidos = cuenta.get("pedidos", [])

st.markdown("<style> .stButton > button { width: 100%; } </style>", unsafe_allow_html=True)

if st.button("← Volver"):
    volver_a_cuenta()

st.markdown("### Cobrar cuenta")

panel = st.container(border=True)
with panel:
    izquierda, derecha = st.columns([1.4, 1])

    with izquierda:
        col_titulo, col_estado = st.columns([2, 1])
        with col_titulo:
            st.markdown(f"<span style='color:#0b6623; font-weight:bold; font-size:18px;'>● {cuenta['cancha']}</span>", unsafe_allow_html=True)
        with col_estado:
            st.markdown(f"<div style='text-align:right; color:#28a745; font-weight:bold; text-transform:uppercase;'>{cuenta.get('estado', 'ABIERTA')}</div>", unsafe_allow_html=True)

        st.markdown(f"Responsable: {cuenta['responsable']}")
        st.markdown(f"📅 {cuenta['fecha']}")
        st.markdown(f"🕒 {cuenta['hora_inicio']} - {cuenta['hora_fin']}")

        st.markdown("---")
        total_productos = 0
        for item in cuenta_pedidos:
            subtotal = item.get("precio", 0) * item.get("cantidad", 0)
            total_productos += subtotal
            st.markdown(f"{item['cantidad']} x {item['nombre']}  •  ${subtotal:,.0f}")

        st.markdown("---")
        st.markdown(
            f"<div style='display:flex; justify-content:space-between; font-size:1.1rem;'><span>Base de cancha</span><strong>${cuenta.get('total_base', 0):,.0f}</strong></div>",
            unsafe_allow_html=True,
        )
        st.markdown(
            f"<div style='display:flex; justify-content:space-between; font-size:1.1rem;'><span>Productos</span><strong>${total_productos:,.0f}</strong></div>",
            unsafe_allow_html=True,
        )
        st.markdown("---")
        st.markdown(f"<div style='display:flex; justify-content:space-between; font-size:1.1rem; font-weight:bold;'><span>TOTAL</span><span>${cuenta.get('total', 0):,.0f}</span></div>", unsafe_allow_html=True)

    with derecha:
        st.markdown("### Medio de pago")
        metodo_pago = st.radio(
            "",
            ["Efectivo", "Débito", "Transferencia"],
            index=0,
            label_visibility="collapsed",
        )

if st.button("Confirmar cobro", type="primary", use_container_width=True):
    st.session_state.cuentas[indice_cuenta]["estado"] = "COBRADA"
    st.session_state.cuentas[indice_cuenta]["metodo_pago"] = metodo_pago
    st.session_state.cuenta_seleccionada = None
    st.success("¡Cuenta pagada correctamente!")
    st.info("La cuota ha sido registrada y ya no aparece en cuentas abiertas.")
    if st.button("Volver a cuentas"):
        st.switch_page("app.py")
    st.stop()
