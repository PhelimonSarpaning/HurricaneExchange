from django.db import models

# Create your models here.
# class Users(models.Model):
#     first_name = models.CharField(max_length=30)
#     last_name = models.CharField(max_length=30)
#     email = models.EmailField()
#     password = models.CharField(max_length=100)
#     created_at = models.DateTimeField(auto_now_add=True)

# # class Trading_Account(models.Model):
# #     user_id = models.ForeignKey('Users', on_delete=models.CASCADE)
# #     amount = models.FloatField(default=1000000)

# # class Stock_Amount(models.Model):
# #     trading_id = models.ForeignKey('Trading_Account', on_delete=models.CASCADE)
# #     stock_name = models.CharField(max_length=100)
# #     stock_amount = models.FloatField()
