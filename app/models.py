from django.db import models

# Create your models here.
class Busbooking(models.Model):
    CSID =models.AutoField(primary_key=True)
    NAME = models.CharField(max_length=50)
    EMAIL = models.EmailField()
    PH_NO = models.CharField(max_length=50)
    USERNAME = models.CharField(max_length=50)
    PASSWORD = models.CharField(max_length=50)
    class Meta:
	    verbose_name = "Busbooking"
	    verbose_name_plural = "Busbookings"

class BusDetails(models.Model):
	BID = models.AutoField(primary_key=True)
	FROM = models.CharField( max_length=50)
	TO = models.CharField(max_length=50)
	BUSNAME = models.CharField(max_length=50)
	BUSTIME = models.TimeField()
	FARE = models.IntegerField()
	TOTAL_SEATS = models.IntegerField(default=50)
	class Meta:
		verbose_name = "BusDetails"
		verbose_name_plural = "BusDetailss"

class Register(models.Model):
	RID  = models.IntegerField()
	DATE = models.DateField(auto_now_add=True)
	TIME = models.TimeField(auto_now_add=True)
	CSID= models.ForeignKey(Busbooking, default=None, verbose_name="Busbooking", on_delete=models.SET_DEFAULT)
	BID= models.ForeignKey(BusDetails, default=None, verbose_name="BusDetails", on_delete=models.SET_DEFAULT)
	Num_seats = models.IntegerField(default=0)
	Total_Fare = models.FloatField(default=0)
	class Meta:
		verbose_name = "Register"
		verbose_name_plural = "Registers"

    
    