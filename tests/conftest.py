import pytest


@pytest.fixture(autouse=True)
def token(monkeypatch):
    monkeypatch.setenv("REST_COUNTRIES_TOKEN", "token-de-prueba")


@pytest.fixture
def pais_v5():
    """Fábrica de objetos país con el formato de REST Countries v5."""

    def _crear(codigo, nombre, capital=None, lat=None, lng=None, poblacion=1000):
        pais = {
            "codes": {"alpha_3": codigo},
            "names": {"common": nombre},
            "population": poblacion,
        }
        if capital is not None:
            pais["capitals"] = [{
                "name": capital,
                "attributes": {"primary": True},
                "coordinates": {"lat": lat, "lng": lng},
            }]
        return pais

    return _crear