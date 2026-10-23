import dlt
from ingesta.recursos import obtener_paises, obtener_clima


@dlt.source(name="monitoreo_clima")
def fuente_clima():
    """Agrupa los recursos y transformadores bajo una misma fuente lógica."""
    return obtener_paises, obtener_clima
