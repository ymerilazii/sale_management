from django.db import models

class Total(models.Model):
    date = models.DateField()
    cashbox = models.DecimalField(max_digits=9,decimal_places=2)
    withdraw = models.DecimalField(max_digits=9, decimal_places=2)
    remain = models.DecimalField(max_digits=9, decimal_places=2)
    sale = models.DecimalField(max_digits=9, decimal_places=2)
    profit = models.DecimalField(max_digits=9, decimal_places=2)
    neto = models.DecimalField(max_digits=9, decimal_places=2)
    expense = models.DecimalField(max_digits=9, decimal_places=2)


class Budget(models.Model):
    budget = models.DecimalField(max_digits=9, decimal_places=2)
    total_sale = models.DecimalField(max_digits=9, decimal_places=2)
    total_profit = models.DecimalField(max_digits=9, decimal_places=2)
    total_neto = models.DecimalField(max_digits=9, decimal_places=2)
    total_expense = models.DecimalField(max_digits=9, decimal_places=2)