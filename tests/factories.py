from datetime import datetime, timezone, timedelta
import factory

from tables.models import Table, Reservation


class TableFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Table
    
    name = factory.Sequence(lambda n : "Table {}".format(n))
    seats = 5
    location = factory.Sequence(lambda n : "Location {}".format(n))


class ReservationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Reservation

    customer_name = factory.Faker("first_name")
    table = factory.SubFactory(TableFactory)
    reservation_time = datetime(2025, 4, 10, 15, 0, 0, 0, timezone(timedelta(hours=3)))
    duration_minutes = 60
