from django.contrib import admin
from .models import Client,Tables,Order,Snacks,Payment,Contact,Otp
# Register your models here.
admin.site.register(Client)
admin.site.register(Tables)
admin.site.register(Order)
admin.site.register(Snacks)
admin.site.register(Payment)
admin.site.register(Contact)
admin.site.register(Otp)



