from unittest.mock import MagicMock, patch

import dlt

from ingesta.fuentes import fuente_clima


def _crear_respuesta_falsa(paises_por_codigo):
    """Devuelve un side_effect que simula REST Countries v5 y Open-Meteo."""

    def _respuesta(url, **kwargs):
        resp = MagicMock()
        if "open-meteo" in url:
            resp.json.return_value = {
                "current": {"temperature_2m": 21.5, "time": "2026-10-23T12:00"},
                "current_units": {"temperature_2m": "°C"},
            }
        else:
            codigo = url.rsplit("/", 1)[-1]
            resp.json.return_value = {
                "data": {"objects": [paises_por_codigo[codigo]]}
            }
        return resp

    return _respuesta


def _pipeline(tmp_path):
    return dlt.pipeline(
        pipeline_name="test_clima_pipeline",
        destination=dlt.destinations.duckdb(str(tmp_path / "test.duckdb")),
        dataset_name="test_clima_raw",
        pipelines_dir=str(tmp_path / "pipelines"),
    )


@patch("ingesta.recursos.CODIGOS_ISO", ["PRY"])
@patch("ingesta.recursos.requests.get")
def test_pipeline_carga_paises_y_clima(mock_get, tmp_path, pais_v5):
    mock_get.side_effect = _crear_respuesta_falsa({
        "PRY": pais_v5("PRY", "Paraguay", "Asunción", -25.28, -57.57, 6109644),
    })
    pipeline = _pipeline(tmp_path)

    info = pipeline.run(fuente_clima())

    assert not info.has_failed_jobs
    with pipeline.sql_client() as client:
        with client.execute_query(
            "SELECT codigo_iso, nombre_pais, capital FROM paises"
        ) as cur:
            assert cur.fetchall() == [("PRY", "Paraguay", "Asunción")]
        with client.execute_query(
            "SELECT codigo_iso, temperatura_actual, unidad_temperatura "
            "FROM clima_capitales"
        ) as cur:
            assert cur.fetchall() == [("PRY", 21.5, "°C")]


@patch("ingesta.recursos.CODIGOS_ISO", ["PRY", "ARG"])
@patch("ingesta.recursos.requests.get")
def test_pipeline_omite_clima_de_paises_sin_coordenadas(mock_get, tmp_path, pais_v5):
    mock_get.side_effect = _crear_respuesta_falsa({
        "PRY": pais_v5("PRY", "Paraguay", "Asunción", -25.28, -57.57),
        "ARG": pais_v5("ARG", "Argentina"),  # sin capital ni coordenadas
    })
    pipeline = _pipeline(tmp_path)

    info = pipeline.run(fuente_clima())

    assert not info.has_failed_jobs
    with pipeline.sql_client() as client:
        with client.execute_query("SELECT COUNT(*) FROM paises") as cur:
            assert cur.fetchone()[0] == 2
        with client.execute_query(
            "SELECT codigo_iso FROM clima_capitales"
        ) as cur:
            assert cur.fetchall() == [("PRY",)]


@patch("ingesta.recursos.CODIGOS_ISO", ["PRY"])
@patch("ingesta.recursos.requests.get")
def test_pipeline_paises_replace_y_clima_append(mock_get, tmp_path, pais_v5):
    mock_get.side_effect = _crear_respuesta_falsa({
        "PRY": pais_v5("PRY", "Paraguay", "Asunción", -25.28, -57.57),
    })
    pipeline = _pipeline(tmp_path)

    pipeline.run(fuente_clima())
    pipeline.run(fuente_clima())

    with pipeline.sql_client() as client:
        with client.execute_query("SELECT COUNT(*) FROM paises") as cur:
            assert cur.fetchone()[0] == 1   # replace
        with client.execute_query("SELECT COUNT(*) FROM clima_capitales") as cur:
            assert cur.fetchone()[0] == 2   # append
