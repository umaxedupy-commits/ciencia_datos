import dlt
from fuente import  fuente_ventas


def build_pipeline() -> dlt.Pipeline:
    return dlt.pipeline(
        pipeline_name="car_sales",
        destination="duckdb",
        dataset_name="raw_carsales"
    )


def main() -> None: 
    pipe = build_pipeline()
    info = pipe.run(fuente_ventas)
    print(info)


if __name__ == "__main__":
    main()