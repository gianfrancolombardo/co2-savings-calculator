import math
import streamlit as st
import pandas as pd

# Array de equivalencias con ID, coeficientes y textos
"""
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
"""

# Updated CO₂ equivalence conversions (value = kg CO₂ saved × coefficient)
equivalences_array_final = [
  {
    "id": 1,
    "coefficient": 5.0, # 1 km de coche de gasolina emite ~0.2 kg CO₂ (1/0.2 = 5 km/kg)
    "text": "Conducir un coche de gasolina por {value} km",
    "emoji": "🚗"
  },
  {
    "id": 2,
    "coefficient": 0.037, # 1 kg de carne de res ≈27 kg CO₂, 1/27 ≈ 0.037 kg de res por kg CO₂
    "text": "La producción de {value} kg de carne de res",
    "emoji": "🥩"
  },
  {
    "id": 3,
    "coefficient": 0.145, # 1 kg de carne de pollo ≈6.9 kg CO₂, 1/6.9 ≈ 0.145 kg de pollo por kg CO₂
    "text": "La producción de {value} kg de carne de pollo",
    "emoji": "🍗"
  },
  {
    "id": 5,
    "coefficient": 10.75, # Si un minuto de ducha usa ~0.093 kg CO₂, 1/0.093 ≈ 10.75 minutos por kg CO₂
    "text": "{value} minutos de agua caliente en la ducha",
    "emoji": "🚿"
  },
  {
    "id": 6,
    "coefficient": 66.67, # Asumiendo ~15 g (0.015 kg) CO₂ por carga, 1/0.015 ≈ 66.67 cargas por kg CO₂
    "text": "Cargar un teléfono móvil {value} veces",
    "emoji": "📱"
  },
  {
    "id": 7,
    "coefficient": 0.077, # Si una producción de jeans genera ~13 kg CO₂, 1/13 ≈ 0.077 jeans por kg CO₂
    "text": "Fabricar {value} jeans de mezclilla",
    "emoji": "👖"
  },
  {
    "id": 8,
    "coefficient": 0.67, # Suponiendo que reciclar 1 kg de papel evita ~1.5 kg CO₂, 1/1.5 ≈ 0.67 kg de papel por kg CO₂
    "text": "Reciclar {value} kg de papel",
    "emoji": "♻️"
  },
  {
    "id": 4,
    "coefficient": 4.0, # En red europea: 1 kWh ≈0.25 kg CO₂, 1/0.25 = 4 kWh por kg CO₂
    "text": "El uso de {value} kWh de electricidad (red Europea)",
    "emoji": "💡"
  },
  {
    "id": 9,
    "coefficient": 2.54, # En red EEUU: 1 kWh ≈0.394 kg CO₂, 1/0.394 ≈2.54 kWh por kg CO₂
    "text": "El uso de {value} kWh de electricidad (red EEUU)",
    "emoji": "💡"
  },
  {
    "id": 10,
    "coefficient": 41.67, # Suponiendo ~0.024 kg CO₂ por taza de café, 1/0.024 ≈41.67 tazas por kg CO₂
    "text": "Tomar {value} tazas de café caliente",
    "emoji": "☕"
  },
  {
    "id": 11,
    "coefficient": 4.17, # En un vuelo comercial corto: 1 km ≈0.24 kg CO₂, 1/0.24 ≈4.17 km por kg CO₂
    "text": "Volar en un avión comercial durante {value} km",
    "emoji": "✈️"
  },
  {
    "id": 12,
    "coefficient": 1.0, # Asumiendo que un ciclo de secadora emite ~1 kg CO₂
    "text": "Realizar {value} ciclos de secado en secadora",
    "emoji": "🌀"
  },
  {
    "id": 13,
    "coefficient": 40.0, # Una bombilla incandescente de 100W durante 1 hora ≈0.025 kg CO₂, 1/0.025 = 40 horas por kg CO₂
    "text": "Encender una bombilla incandescente durante {value} horas",
    "emoji": "💡"
  },
  {
    "id": 14,
    "coefficient": 0.05, # Si un árbol absorbe ~20 kg CO₂ al año, 1/20 = 0.05 árboles por kg CO₂
    "text": "Plantar {value} árboles (promedio anual absorbido)",
    "emoji": "🌳"
  }
];


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
