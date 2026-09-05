# pyright: reportMissingImports=false
import streamlit as st

from pages.AbrirCuenta import mostrar_formulario_cuenta


# 1. Configuración de la página (¡Debe ser la primera línea!)
st.set_page_config(page_title="PadelCenter", layout="wide")


# 2. Inicializar el estado de las cuentas si no existe
if "cuentas" not in st.session_state:
    st.session_state.cuentas = []
    st.write("No hay Cuentas Agregadas")



# Estilos CSS para los botones dentro de las tarjetas
st.markdown(
    """
    <style>
        .stButton > button {
            width: auto;
            margin-top: 12px;
            background-color: #f0fdfa;
            color: #0f766e;
            border: 1px solid #99f6e4;
            border-radius: 8px;
            padding: 10px 14px;
            font-weight: 600;
        }
        .stButton > button:hover {
            border-color: #5eead4;
            background-color: #ccfbf1;
        }

        main div[data-testid="stHorizontalBlock"] {
            justify-content: center !important;
        }

        main div[data-testid="stHorizontalBlock"] > div {
            flex: 0 0 420px !important;
            max-width: 420px !important;
        }

        main [data-testid="stVerticalBlockBorderWrapper"] {
            padding: 0.45rem 0.7rem 0.3rem !important;
            width: 100% !important;
            max-width: 420px !important;
            margin: 0 auto !important;
        }

        section[data-testid="stSidebar"] div[data-testid="stHorizontalBlock"] {
            display: flex !important;
        }

        section[data-testid="stSidebar"] div[data-testid="stHorizontalBlock"] > div {
            flex: 1 1 0 !important;
            max-width: none !important;
        }

        div[data-testid="stVerticalBlock"] > div {
            gap: 0.18rem !important;
        }

        .stMarkdown {
            margin: 0 !important;
        }

        .stMarkdown p {
            margin: 0.12rem 0 !important;
            line-height: 1.35 !important;
        }

        hr {
            margin: 0.3rem 0 !important;
        }
    </style>
    """,
    unsafe_allow_html=True,
)



# 3. Construcción del menú en la barra lateral
with st.sidebar:
    # Encabezado con título del sistema
    st.title("🎾 PadelCenter")
    st.markdown("<p style='margin-top:-5px; color:#a0aec0; font-size:14px;'>Gestión de Cuentas</p>", unsafe_allow_html=True)
    st.write("---") # Línea divisoria discreta
    mostrar_formulario_cuenta()

    st.divider()
    st.subheader("Navegación")
    st.page_link("pages/Productos.py", label="Productos", icon="🥤")
    st.page_link("pages/HistorialCuentasCobradas.py", label="Historial de cuentas cobradas", icon="📙")


# 4. Creamos filas dinámicas usando st.columns (3 tarjetas por fila)
cols = st.columns(3)

cuentas_activas = [
    (index, cuenta)
    for index, cuenta in enumerate(st.session_state.cuentas)
    if cuenta.get("estado", "Abierta") != "COBRADA"
]

for index, cuenta in cuentas_activas:
    estado = cuenta.get('estado', 'Abierta')
    color = '#28a745' if estado == 'Abierta' else '#dc3545'
    pedidos = cuenta.get('pedidos', [])

    if pedidos:
        vista_pedidos = "\n".join(
            f"• {item.get('cantidad', 0)}x {item.get('nombre', '')}"
            for item in pedidos[:3]
        )
        if len(pedidos) > 3:
            vista_pedidos += f"\n+{len(pedidos) - 3} más"
    else:
        vista_pedidos = "Sin pedidos"

    with cols[index % 3]:
        card = st.container(border=True)
        with card:
            col_titulo, col_estado = st.columns([4, 1])
            with col_titulo:
                st.markdown(f"<span style='color:{color}; font-size: 16px; font-weight: bold;'>●</span> <span style='color:#0b6623; font-weight: bold;'>{cuenta['cancha']}</span>", unsafe_allow_html=True)
            with col_estado:
                st.markdown(f"<div style='text-align:right; color:{color}; font-size:11px; font-weight:bold; text-transform:uppercase;'>{estado}</div>", unsafe_allow_html=True)

            st.markdown(f"🙎🏻 {cuenta['responsable']}")
            st.markdown(f"🕒 {cuenta['hora_inicio']} - {cuenta['hora_fin']}")
            st.markdown(f"📅 {cuenta['fecha']}")

            st.markdown("---")
            st.markdown(f"<div style='font-size:12px; color:#4a5568; min-height:52px;'>{vista_pedidos.replace(chr(10), '<br>')}</div>", unsafe_allow_html=True)
            st.markdown(f"<div style='font-size:22px; font-weight:bold; color:#0b6623; margin-top:8px;'>${cuenta.get('total', 0):,}</div>", unsafe_allow_html=True)

            if st.button("Ver cuenta", key=f"btn_{index}", width="stretch"):
                st.session_state.cuenta_seleccionada = index
                st.switch_page("pages/GestionarCuenta.py")