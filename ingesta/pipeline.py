import dlt
from ingesta.fuentes import fuente_clima


def ejecutar():
    pipeline = dlt.pipeline(
        pipeline_name="pipeline_modular_clima",
        destination=dlt.destinations.duckdb("datos.duckdb"),
        dataset_name="clima_raw"
    )

    info = pipeline.run(fuente_clima())
    print(info)


if __name__ == "__main__":
    ejecutar()
