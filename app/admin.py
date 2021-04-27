from django.contrib import admin
from app.models import * 
# Register your models here.
class BusbookingAdmin(admin.ModelAdmin):
    '''
        Admin View for Busbooking
    '''
    list_display = ('CSID','NAME','EMAIL','PH_NO','USERNAME','PASSWORD')

admin.site.register(Busbooking, BusbookingAdmin)

class BusDetailsAdmin(admin.ModelAdmin):
    '''
        Admin View for BusDetails
    '''
    list_display = ('BID','FROM','TO','BUSNAME','BUSTIME','FARE','TOTAL_SEATS')

admin.site.register(BusDetails, BusDetailsAdmin)

class RegisterAdmin(admin.ModelAdmin):
    '''
        Admin View for 
    '''
    list_display = ('CSID','BID','Num_seats','Total_Fare')

admin.site.register(Register,RegisterAdmin)
