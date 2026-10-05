import os
import pandas as pd

def analizar_sensores():
    data_path = os.path.join("data", "sensores_industriales.csv")
    output_dir = "resultados"
    output_path = os.path.join(output_dir, "alertas.csv")

    if not os.path.exists(data_path):
        print(f"Error: No se encontró el archivo en {data_path}")
        return

    print("=== ANÁLISIS DE SENSORES INDUSTRIALES ===\n")
    df = pd.read_csv(data_path)

    # 1. Registros y sensores distintos
    print(f"1. Total registros: {len(df):,}")
    print(f"   Sensores distintos: {df['id_sensor'].nunique()}\n")

    # 2. Temp promedio por planta
    print("2. Temperatura promedio por planta:")
    for planta, temp in df.groupby('planta')['temperatura_c'].mean().items():
        print(f"   - {planta}: {temp:.2f} °C")
    print()

    # 3. Temp máxima, sensor y fecha
    max_temp = df['temperatura_c'].max()
    registros_max = df[df['temperatura_c'] == max_temp]
    print(f"3. Temperatura máxima: {max_temp} °C")
    for _, row in registros_max.iterrows():
        print(f"   - Sensor: {row['id_sensor']} | Fecha: {row['fecha_hora']} | Planta: {row['planta']}")
    print()

    # 4. Lecturas > 85 °C
    df_alertas = df[df['temperatura_c'] > 85]
    print(f"4. Lecturas con alerta (> 85 °C): {len(df_alertas):,}\n")

    # 5. Planta con más alertas
    print("5. Planta(s) con más alertas:")
    alertas_por_planta = df_alertas['planta'].value_counts()
    if not alertas_por_planta.empty:
        max_a = alertas_por_planta.max()
        for planta, conteo in alertas_por_planta[alertas_por_planta == max_a].items():
            print(f"   - {planta}: {conteo:,} alertas")
    print()

    # 6. Exportar alertas
    os.makedirs(output_dir, exist_ok=True)
    df_alertas.to_csv(output_path, index=False)
    print(f"6. Alertas exportadas exitosamente en {output_path}")

if __name__ == "__main__":
    analizar_sensores()