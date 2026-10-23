import duckdb

DB = "datos.duckdb"
DATASET = "clima_raw"


def verificar_base_datos():
    con = duckdb.connect(DB, read_only=True)

    print("=== Tablas Creadas ===")
    
    tablas = con.execute(
        "SELECT table_name FROM information_schema.tables "
        "WHERE table_schema = ? AND table_name NOT LIKE '\\_dlt\\_%' ESCAPE '\\'",
        [DATASET],
    ).fetchall()

    for tabla in tablas:
        print(f"- {tabla[0]}")

    print("\n=== Conteo de Registros ===")
    conteo_pais = con.execute(f"SELECT COUNT(*) FROM {DATASET}.paises").fetchone()[0]
    print(f"Total de países cargados: {conteo_pais}")

    conteo_clima = con.execute(f"SELECT COUNT(*) FROM {DATASET}.clima_capitales").fetchone()[0]
    print(f"Total de mediciones de clima: {conteo_clima}")

    print("\n=== Última medición por capital ===")
    for fila in con.execute(
        f"SELECT codigo_iso, capital, temperatura_actual, unidad_temperatura, fecha_hora_medicion "
        f"FROM {DATASET}.clima_capitales "
        f"QUALIFY ROW_NUMBER() OVER (PARTITION BY codigo_iso ORDER BY fecha_hora_medicion DESC) = 1"
    ).fetchall():
        print(fila)

    con.close()


if __name__ == "__main__":
    verificar_base_datos()