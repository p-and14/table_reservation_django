from django.db import models


class Table(models.Model):
    class Meta:
        verbose_name = "Стол"
        verbose_name_plural = "Столы"
        ordering = ["id"]
    
    def __str__(self):
        return self.name
    
    name = models.CharField(verbose_name="Название", max_length=255, unique=True)
    seats = models.PositiveSmallIntegerField(verbose_name="Количество мест", db_index=True)
    location = models.CharField(verbose_name="Расположение", max_length=255)


class Reservation(models.Model):
    class Meta:
        verbose_name = "Бронь"
        verbose_name_plural = "Брони"
        ordering = ["table", "reservation_time"]

    customer_name = models.CharField(verbose_name="Имя клиента", max_length=255)
    table = models.ForeignKey(
        Table, verbose_name="Стол",
        on_delete=models.CASCADE,
        db_index=True,
        related_name="reservations")
    reservation_time = models.DateTimeField(verbose_name="Время брони")
    duration_minutes = models.PositiveIntegerField(verbose_name="Длительность в минутах")
