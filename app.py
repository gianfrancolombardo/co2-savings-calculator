import math
import streamlit as st
import pandas as pd

# Array de equivalencias con ID, coeficientes y textos
equivalences_array_final = [
    {"id": 1, "coefficient": 0.2, "text": "Conducir un coche de gasolina por {value} km", "emoji": "🚗"},  
    {"id": 2, "coefficient": 27.0, "text": "La producción de {value} kg de carne de res", "emoji": "🥩"},  
    {"id": 3, "coefficient": 11.0, "text": "La producción de {value} kg de carne de pollo", "emoji": "🍗"},  
    {"id": 5, "coefficient": 3.16, "text": "{value} minutos de agua caliente en la ducha", "emoji": "🚿"}, 
    {"id": 6, "coefficient": 219.85, "text": "Cargar un teléfono móvil {value} veces", "emoji": "📱"}, 
    {"id": 7, "coefficient": 10.0, "text": "Fabricar {value} jeans de mezclilla", "emoji": "👖"},  
    {"id": 8, "coefficient": 0.2, "text": "Reciclar {value} kg de papel", "emoji": "♻️"},  
    {"id": 4, "coefficient": 3.5, "text": "El uso de {value} kWh de electricidad (red Europea)", "emoji": "💡"}, 
    {"id": 9, "coefficient": 12.5, "text": "El uso de {value} kWh de electricidad (red EEUU)", "emoji": "💡"},  
    {"id": 10, "coefficient": 3.68, "text": "Tomar {value} tazas de café caliente", "emoji": "☕"} 
]

# Función para calcular las equivalencias y devolver un DataFrame
def calculate_equivalences_df(co2_kg):
    equivalences_list = []
    for item in equivalences_array_final:
        value = math.ceil(co2_kg * item["coefficient"])
        equivalences_list.append({
            "Icono": item["emoji"],
            "Texto": item["text"].format(value=math.ceil(value)),
            # text = item["text"].format(value=round(value, 0))
            # text = item["text"].format(value=int(value))
            "Coefficiente (por kg)": item["coefficient"]
        })
    
    # Convertir la lista de equivalencias en un DataFrame
    df = pd.DataFrame(equivalences_list)
    return df

st.set_page_config(
    page_title="CO₂e ahorrado", 
    page_icon="🌍", 
)

# Crear la interfaz con Streamlit
st.title("🌍 ¡Mira cuánto CO₂e has ahorrado!")

# Entrada de CO₂ en kilogramos
co2_input = st.number_input("Ingresa cuánto CO₂e (en kg) has ahorrado:", min_value=0, value=10)

if co2_input > 0:
    st.subheader(f"🎉 Tu ahorro de **{co2_input} kg** de CO₂e equivale a:")
    # Calcular las equivalencias y mostrarlas en un DataFrame
    df_equivalences = calculate_equivalences_df(co2_input)
    st.dataframe(df_equivalences, use_container_width=True)
