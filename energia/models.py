from django.db import models


class Energy(models.Model):
    produced_energy_in_watt = models.IntegerField()
    consumed_energy_in_watt = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    hash = models.CharField(max_length=32, default=None, null=True)
    txId = models.CharField(max_length=66, default=None, null=True)

    class Meta:
        app_label = 'energia'


class AdminLog(models.Model):
    admin_user = models.CharField(max_length=200)
    last_ip_address = models.CharField(max_length=20)
    login_time = models.DateTimeField(auto_now_add=True)



