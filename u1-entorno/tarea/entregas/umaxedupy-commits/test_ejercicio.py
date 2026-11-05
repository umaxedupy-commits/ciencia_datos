import pytest
from datetime import date

from ejercicio import (
    parse_fecha,
    descripcion_venta,
    separar_nombre_id
)


@pytest.mark.parametrize(
    "valor_texto, valor_esperado",
    [
        ("01/01/2026", date(2026,1,1)),
        ("10/03/2026", date(2026,10,3)),
        ("08/15/2026", date(2026,8,15))
    ],
)
def test_parser_fecha_valida(valor_texto, valor_esperado):
    assert parse_fecha(valor_texto) == valor_esperado


@pytest.mark.parametrize(
        "valor_texto",
        [
            "15/01/2026",
            "02/31/2026",
            "04/31/2026"
        ],
)
def test_parser_fecha_invalido(valor_texto):
    with pytest.raises(ValueError):
        parse_fecha(valor_texto)


@pytest.mark.parametrize(
        "valor_texto, nombre_esperado, id_esperado",
        [
            ("Jorge Bogado 123", "Jorge Bogado", 123),
            ("Pedro 25", "Pedro", 25),
            ("Marta Maria 859", "Marta Maria", 859)
        ],
)
def test_separado_nombres(valor_texto, nombre_esperado, id_esperado):
    assert separar_nombre_id(valor_texto) == (
        nombre_esperado,
        id_esperado
    )

@pytest.mark.parametrize(
        "venta, esperado",
        [
            (
                {
                    "car_make": "Toyota",
                    "car_model": "Starlet",
                    "sale_price": "1500000"
                },
                "Venta registrada: Toyota Starlet por $1500000.0",
            ),
            (
                {
                    "car_make": "Honda",
                    "car_model": "Focus",
                    "sale_price": "2500000"
                },
                "Venta registrada: Honda Focus por $2500000.0",
            )
        ]
)
def test_descripcion_ventas(venta, esperado):
    assert descripcion_venta(venta) == esperado