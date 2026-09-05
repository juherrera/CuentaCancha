import pandas as pd
import streamlit as st


st.set_page_config(page_title="Historial Cuentas Cobradas", layout="wide")


def obtener_cuentas_cobradas():
    return [
        (indice, cuenta)
        for indice, cuenta in enumerate(st.session_state.get("cuentas", []))
        if cuenta.get("estado") == "COBRADA"
    ]


def construir_dataframe(cuentas_cobradas):
    filas = []
    for indice, cuenta in cuentas_cobradas:
        filas.append(
            {
                "ID": indice,
                "Cancha": cuenta.get("cancha", ""),
                "Representante": cuenta.get("responsable", ""),
                "Fecha": cuenta.get("fecha", ""),
                "Hora Inicio": cuenta.get("hora_inicio", ""),
                "Hora Fin": cuenta.get("hora_fin", ""),
                "Cuenta Total": cuenta.get("total", 0),
                "Medio de pago": cuenta.get("metodo_pago", "No registrado"),
                "Acción": "Ver detalle",
            }
        )

    return pd.DataFrame(
        filas,
        columns=[
            "ID",
            "Cancha",
            "Representante",
            "Fecha",
            "Hora Inicio",
            "Hora Fin",
            "Cuenta Total",
            "Medio de pago",
            "Acción",
        ],
    )


def obtener_pedidos(indice, cuenta):
    pedidos = cuenta.get("pedidos")
    if pedidos is not None:
        return pedidos
    return st.session_state.get("pedidos", {}).get(indice, [])


@st.dialog("Detalle de la cuenta")
def mostrar_detalle(indice, cuenta):
    st.markdown(f"**Cancha:** {cuenta.get('cancha', '')}")
    st.markdown(f"**Representante:** {cuenta.get('responsable', '')}")
    st.markdown(f"**Fecha:** {cuenta.get('fecha', '')}")
    st.markdown(
        f"**Horario:** {cuenta.get('hora_inicio', '')} - "
        f"{cuenta.get('hora_fin', '')}"
    )

    pedidos = obtener_pedidos(indice, cuenta)
    if not pedidos:
        st.info("Esta cuenta no tiene pedidos asociados.")
        return

    detalle = []
    for pedido in pedidos:
        cantidad = pedido.get("cantidad", 0)
        precio = pedido.get("precio", 0)
        detalle.append(
            {
                "Producto": pedido.get("nombre", ""),
                "Cantidad": cantidad,
                "Precio": precio,
                "Subtotal": cantidad * precio,
            }
        )

    st.dataframe(pd.DataFrame(detalle), hide_index=True, use_container_width=True)
    st.markdown(f"**Total de la cuenta:** ${cuenta.get('total', 0):,.0f}")


def preparar_exportacion(df):
    columnas_exportables = [
        "ID",
        "Cancha",
        "Representante",
        "Fecha",
        "Hora Inicio",
        "Hora Fin",
        "Cuenta Total",
        "Medio de pago",
    ]
    return df[columnas_exportables].to_csv(index=False).encode("utf-8-sig")


if st.button("← Volver a cuentas"):
    st.switch_page("app.py")

st.markdown(
    """
    <style>
    div[data-testid="stHorizontalBlock"] {
        gap: 0.05rem;
        align-items: center;
    }
    .stDivider {
        margin-top: 0.18rem !important;
        margin-bottom: 0.18rem !important;
        border-top: 1px solid rgba(49, 51, 63, 0.3) !important;
    }
    [data-testid="stVerticalBlock"] > div:has(> div[data-testid="stHorizontalBlock"]) {
        margin-bottom: 0 !important;
    }
    div[data-testid="stHorizontalBlock"] > div {
        padding-top: 0.08rem !important;
        padding-bottom: 0.08rem !important;
        display: flex !important;
        align-items: center !important;
    }
    div[data-testid="stHorizontalBlock"] > div:last-child {
        padding-top: 0.18rem !important;
        padding-bottom: 0.12rem !important;
        justify-content: center !important;
    }
    div[data-testid="stHorizontalBlock"] > div > p,
    div[data-testid="stHorizontalBlock"] > div > div,
    div[data-testid="stHorizontalBlock"] > div > span {
        margin: 0 !important;
        line-height: 1.2 !important;
    }
    div[data-testid="stHorizontalBlock"] > div:last-child .stButton > button {
        height: 2.25rem;
        min-height: 2.25rem;
        padding-top: 0.3rem !important;
        padding-bottom: 0.3rem !important;
        margin-top: 0.02rem !important;
        margin-bottom: 0.06rem !important;
        width: 82%;
        max-width: 140px;
        min-width: 110px;
    }
    .st-emotion-cache-1r6slb0, .st-emotion-cache-1r6slb0 p {
        margin: 0 !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("📙 Historial de Cuentas Cobradas")

cuentas_cobradas = obtener_cuentas_cobradas()
df = construir_dataframe(cuentas_cobradas)

if df.empty:
    st.info("No hay cuentas cobradas para mostrar.")
    st.stop()

columna_orden, sentido_orden = st.columns(2)
with columna_orden:
    columna_seleccionada = st.selectbox(
        "Ordenar por",
        ["Fecha", "Cancha", "Representante", "Hora Inicio", "Hora Fin", "Cuenta Total"],
    )
with sentido_orden:
    orden_descendente = st.checkbox("Orden descendente")

df = df.sort_values(
    by=columna_seleccionada,
    ascending=not orden_descendente,
    kind="stable",
)

st.subheader("Cuentas cobradas")
encabezados = st.columns([0.5, 1, 1.8, 1, 1, 1, 1, 1.2, 1])
for columna, encabezado in zip(
    encabezados,
    [
        "ID",
        "Cancha",
        "Representante",
        "Fecha",
        "Hora Inicio",
        "Hora Fin",
        "Cuenta Total",
        "Medio de pago",
        "Acción",
    ],
):
    columna.markdown(f"**{encabezado}**")

cuentas_por_id = dict(cuentas_cobradas)
for fila in df.to_dict("records"):
    columnas = st.columns([0.5, 1, 1.8, 1, 1, 1, 1, 1.2, 1])
    columnas[0].write(fila["ID"])
    columnas[1].write(fila["Cancha"])
    columnas[2].write(fila["Representante"])
    columnas[3].write(fila["Fecha"])
    columnas[4].write(fila["Hora Inicio"])
    columnas[5].write(fila["Hora Fin"])
    columnas[6].write(f"${fila['Cuenta Total']:,.0f}")
    columnas[7].write(fila["Medio de pago"])
    if columnas[8].button(
        "Ver detalle",
        key=f"detalle_cuenta_{fila['ID']}",
        use_container_width=True,
    ):
        mostrar_detalle(fila["ID"], cuentas_por_id[fila["ID"]])
    st.divider()

st.download_button(
    "Descargar historial CSV",
    data=preparar_exportacion(df),
    file_name="historial_cuentas_cobradas.csv",
    mime="text/csv",
)