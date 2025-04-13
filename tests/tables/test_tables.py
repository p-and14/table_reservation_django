import pytest

from rest_framework.exceptions import ErrorDetail

from tables import serializers
from tables.models import Table, Reservation


@pytest.mark.django_db
@pytest.mark.usefixtures("table_data")
@pytest.mark.parametrize(
    "data, status_code, res_data, create_table", [
        ("table_data", 201, "table_data", False),
        ({}, 400, {key: [ErrorDetail("Обязательное поле.", "required")] for key in ("name", "seats", "location")}, False),
        ("table_data", 400, {"name": [ErrorDetail("Стол с таким Название уже существует.", "unique")]}, True),
    ]
)
def test_table_create(client, table_factory, data, status_code, res_data, create_table, request):
    data = request.getfixturevalue(data) if data in request.fixturenames else data
    res_data = request.getfixturevalue(res_data) if res_data in request.fixturenames else res_data

    if create_table:
        table_factory.create()

    response = client.post("/tables/", data=data)

    assert response.status_code == status_code
    for k in res_data.keys():
        assert response.data[k] == res_data[k]


@pytest.mark.django_db
def test_table_list(client, table_factory):
    tables = table_factory.create_batch(2)
    expected_response = serializers.TableSerializer(tables, many=True).data
    
    response = client.get("/tables/")

    assert response.status_code == 200
    assert response.data["results"] == expected_response
    assert len(response.data["results"]) == 2


@pytest.mark.django_db
def test_table_delete(client, table_factory, reservation_factory):
    table = table_factory.create()
    reservation_factory.create_batch(2, table=table)
    
    response = client.delete(f"/tables/{table.pk}")

    assert response.status_code == 204
    assert len(Table.objects.all()) == 0
    assert len(Reservation.objects.all()) == 0

    response = client.delete(f"/tables/{table.pk}")

    assert response.status_code == 404
    assert response.data["detail"] == ErrorDetail("No Table matches the given query.", "not_found")


@pytest.mark.django_db
@pytest.mark.usefixtures("reservation_data", "reservation_data_overlap")
@pytest.mark.parametrize(
    "data, status_code, res_data, create_reservation", [
        ("reservation_data", 201, "reservation_data", False),
        ("reservation_data", 400, "reservation_data_overlap", True)
    ]
)
def test_reservation_create(
    client, data, status_code, res_data, create_reservation,
    table_factory, reservation_factory, request
):
    table = table_factory.create()
    if create_reservation:
        reservation_factory.create(table=table)

    if data in request.fixturenames:
        data = request.getfixturevalue(data)
    
        if callable(data):
            data = data(table)

    if res_data in request.fixturenames:
        res_data = request.getfixturevalue(res_data)
        if callable(res_data):
            res_data = res_data(table)

    response = client.post("/reservations/", data=data)

    assert response.status_code == status_code
    for k in res_data.keys():
        assert response.data[k] == res_data[k]


@pytest.mark.django_db
def test_reservation_delete(client, table_factory, reservation_factory):
    table = table_factory.create()
    reservation = reservation_factory.create(table=table)
    
    response = client.delete(f"/reservations/{reservation.pk}")

    assert response.status_code == 204
    assert len(Reservation.objects.all()) == 0

    response = client.delete(f"/reservations/{reservation.pk}")

    assert response.status_code == 404
    assert response.data["detail"] == ErrorDetail("No Reservation matches the given query.", "not_found")
