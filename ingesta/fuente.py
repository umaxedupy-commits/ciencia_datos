
import csv
import dlt
import logging

from pathlib import Path
from date_util import formatear_fecha
from typing import Iterator


RUTA_CSV = Path(__file__).resolve().parents[1] / "data"/ "car_sales.csv"

# logging.basicConfig(level=logging.debug, format="%(levelname)s: %(message)s")

def leer_csv(ruta: Path): 
    with open(ruta, encoding="utf-8", newline="") as archivo:
        yield from csv.DictReader(archivo)


@dlt.resource(name="car_sales", write_disposition="append")
def ventas(ruta: Path = RUTA_CSV) -> Iterator[dict]:
    for fila in leer_csv(ruta):
        yield fila

@dlt.source(name="ventas_ejemplo")
def fuente_ventas(ruta_cvs: Path = RUTA_CSV):
    print(RUTA_CSV)
    return [ventas(ruta_cvs)]

