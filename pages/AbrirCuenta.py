import streamlit as st # type: ignore[import-not-found]
from datetime import time

canchas_disponibles = ['Cancha 1','Cancha 2','Cancha 3','Cancha 4','Cancha 5']

def mostrar_formulario_cuenta():
    """Muestra el formulario 'Crear Cuenta' y agrega la transaccion al session_state cuando se envia."""
    st.title("➕ Abrir Cuenta")

    with st.form("nueva_cuenta"):
        cancha = st.selectbox("Selecciona Cancha", canchas_disponibles)
        responsable = st.text_input("Responsable", placeholder="Nombre del representante del grupo")
        fecha = st.date_input("Fecha")

        col_hora_inicio, col_hora_fin = st.columns(2)
        with col_hora_inicio:
            hora_inicio = st.time_input("Hora Inicio", value=time(9, 0), step=1800)
        with col_hora_fin:
            hora_fin = st.time_input("Hora Fin", value=time(10, 0), step=1800)

        enviado = st.form_submit_button("Agregar Cuenta", use_container_width=True)

    if enviado:
        if responsable.strip() and hora_inicio and hora_fin:
            if hora_inicio >= hora_fin:
                st.error("La hora de inicio debe ser anterior a la hora de fin.")
            elif any(
                cuenta.get("cancha") == cancha
                and cuenta.get("estado", "Abierta") == "Abierta"
                for cuenta in st.session_state.cuentas
            ):
                st.error(
                    "La cancha seleccionada ya tiene una cuenta abierta. "
                    "Debes cerrar la cuenta existente antes de abrir una nueva."
                )
            else:
                st.session_state.cuentas.append({
                    "cancha": cancha,
                    "fecha": fecha,
                    "hora_inicio": hora_inicio.strftime("%H:%M"),
                    "hora_fin": hora_fin.strftime("%H:%M"),
                    "responsable": responsable,
                    "total": 0,
                    "total_base": 0
                })

                st.success("Asignación agregada exitosamente!")
                st.rerun() #recarga la pantalla para mostrar los cambios
        else:
            st.error("Por favor, rellena todos los campos")