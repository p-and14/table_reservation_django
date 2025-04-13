import pytest
from pytest_factoryboy import register

from rest_framework.exceptions import ErrorDetail

from tests import factories


register(factories.TableFactory)
register(factories.ReservationFactory)


@pytest.fixture
def table_data():
    return {"name": "Table 0", "seats": 5, "location": "Location 0"}


@pytest.fixture
def reservation_data():
    def _add_table(table):
        return {
            "customer_name": "Ivan",
            "table": table.pk,
            "reservation_time": "2025-04-10T15:30:00+03:00",
            "duration_minutes": 60,
        }
    return _add_table


@pytest.fixture
def reservation_data_overlap():
    return {
        "reservation_time": [ErrorDetail("Время занято. Попробуйте изменить длительность брони", "invalid")],
        "duration_minutes": [ErrorDetail("Время занято. Попробуйте изменить время брони", "invalid")]
    }
