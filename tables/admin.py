from django.contrib import admin

from tables.models import Table, Reservation


admin.site.register((Table, Reservation))
