from django.db import models
from django.conf import settings

from main.managers.activities import ActivityManager
from main.managers.customers import CustomerManager
from main.utils.models import BaseModel


class Customer(BaseModel):
    """ Customer entity """
    objects = CustomerManager()
    name = models.CharField(max_length=50)
    identification = models.CharField(max_length=20, null=True)
    address = models.CharField(max_length=100, null=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        on_delete=models.SET_NULL,
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Customers"
        ordering = ['-created']


class VehicleType(BaseModel):
    """ VehicleType Entity """
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Vehicle(BaseModel):
    """ Vehicle Entity """
    brand = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    plate = models.CharField(max_length=10)
    type = models.ForeignKey(
        VehicleType,
        null=True,
        on_delete=models.SET_NULL
    )

    def __str__(self):
        return f"{self.brand} {self.model} {self.plate}"


class Activity(BaseModel):
    """ Activity Entity """
    objects = ActivityManager()
    description = models.TextField()
    detail = models.TextField()
    status = models.CharField(max_length=2, default="R")
    start = models.DateField()
    finish = models.DateField()
    customer = models.ForeignKey(
        Customer,
        null=True,
        on_delete=models.SET_NULL)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        on_delete=models.SET_NULL)
    workers = models.ManyToManyField(
        'users.User', through='WorkerActivity',
        related_name='activities'
    )

    vehicles = models.ManyToManyField(
        Vehicle, through='VehicleActivity',
        related_name='activities'
    )

    def __str__(self) -> str:
        return f"{self.description}"

    class Meta:
        verbose_name_plural = "Activities"
        ordering = ['-created']


class WorkerActivity(BaseModel):
    """ Worker activity Entity """
    activity = models.ForeignKey(
        Activity,
        on_delete=models.CASCADE)
    worker = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE)
    role = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural = "Workers of activities"
        ordering = ['-created']


class VehicleActivity(BaseModel):
    """ Vehicle activity Entity """
    activity = models.ForeignKey(
        Activity,
        on_delete=models.CASCADE)
    vehicle = models.ForeignKey(
        Vehicle,
        on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Vehicles of activities"
        ordering = ['-created']
