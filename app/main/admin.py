from django.contrib import admin
import main.models

admin.site.register(main.models.Customer)
admin.site.register(main.models.Activity)
admin.site.register(main.models.VehicleType)
admin.site.register(main.models.Vehicle)
admin.site.register(main.models.WorkerActivity)
