from datetime import datetime


def formatear_fecha(valor_fecha: str) : 
    fecha = datetime.strftime(valor_fecha.strip(), "%m/%s/%d")
    return fecha.date()

