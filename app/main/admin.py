from django.contrib import admin
import main.models


class ActivityAdmin(admin.ModelAdmin):

    list_display = (
        'description', 'customer', 'start', 'finish', 'status_name')
    list_filter = ('status',)

    search_fields = ('description', 'customer__name')
    ordering = ('-start',)


class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'identification', 'is_active')
    # list_filter = ('name', 'identificacion')

    search_fields = ('name', 'identificacion')
    ordering = ('-created',)


class ContractAdmin(admin.ModelAdmin):

    list_display = ('customer', 'identification',
                    'description', 'start', 'finish', 'is_active')
    # list_filter = ('status',)

    search_fields = ('description', 'customer__name')
    ordering = ('-start',)


class VehicleAdmin(admin.ModelAdmin):

    list_display = ('plate', 'type',
                    'brand', 'model', 'is_active')
    list_filter = ('type',)

    search_fields = ('plate', 'brand')
    # ordering = ('-start',)


admin.site.register(main.models.Activity, ActivityAdmin)
admin.site.register(main.models.Customer, CustomerAdmin)
admin.site.register(main.models.VehicleType)
admin.site.register(main.models.Vehicle, VehicleAdmin)
admin.site.register(main.models.WorkerActivity)
admin.site.register(main.models.ActivityLog)
admin.site.register(main.models.Contract, ContractAdmin)
