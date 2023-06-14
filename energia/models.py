from django.db import models


# The Energy model, representing the energy data
class Energy(models.Model):
    # The amount of produced energy, represented as an integer field
    produced_energy_in_watt = models.IntegerField()
    # The amount of consumed energy, represented as an integer field
    consumed_energy_in_watt = models.IntegerField()
    # The timestamp when the record was created, set automatically when the object is created
    created_at = models.DateTimeField(auto_now_add=True)
    # The hash value, represented as a string field with a maximum length of 32
    # It's set as optional with default value as None
    hash = models.CharField(max_length=32, default=None, null=True)
    # The transaction ID, represented as a string field with a maximum length of 66
    # It's set as optional with default value as None
    txId = models.CharField(max_length=66, default=None, null=True)

    class Meta:
        # Set the application label for this model to 'energia'
        app_label = 'energia'


# The AdminLog model, representing the admin login logs
class AdminLog(models.Model):
    # The username of the admin user, represented as a string field with a maximum length of 200
    admin_user = models.CharField(max_length=200)
    # The last IP address from which the admin user logged in, represented as a string field with a maximum length of 20
    last_ip_address = models.CharField(max_length=20)
    # The timestamp when the admin user logged in, set automatically when the object is created
    login_time = models.DateTimeField(auto_now_add=True)




