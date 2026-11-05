from unittest.mock import MagicMock, patch

from ingesta.recursos import _consultar_clima, _transformar_pais


def test_transformar_pais():
    raw = {
        "codes": {"alpha_3": "PRY"},
        "names": {"common": "Paraguay"},
        "capitals": [{
            "name": "Asunción",
            "attributes": {"primary": True},
            "coordinates": {"lat": -25.28, "lng": -57.57},
        }],
        "population": 6109644,
    }

    pais = _transformar_pais(raw)

    assert pais["codigo_iso"] == "PRY"
    assert pais["nombre_pais"] == "Paraguay"
    assert pais["capital"] == "Asunción"
    assert pais["latitud_capital"] == -25.28


@patch("ingesta.recursos.requests.get")
def test_clima_sin_coordenadas(mock_get):
    pais = {"codigo_iso": "XXX", "capital": None,
            "latitud_capital": None, "longitud_capital": None}

    assert _consultar_clima(pais) is None
    mock_get.assert_not_called()


@patch("ingesta.recursos.requests.get")
def test_clima_con_coordenadas(mock_get):
    mock_get.return_value = MagicMock(json=lambda: {
        "current": {"temperature_2m": 21.5, "time": "2026-10-23T12:00"},
        "current_units": {"temperature_2m": "°C"},
    })
    pais = {"codigo_iso": "PRY", "capital": "Asunción",
            "latitud_capital": -25.28, "longitud_capital": -57.57}

    clima = _consultar_clima(pais)

    assert clima["temperatura_actual"] == 21.5
    assert clima["codigo_iso"] == "PRY"