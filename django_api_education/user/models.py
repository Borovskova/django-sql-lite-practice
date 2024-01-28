from django.db import models

from car.models import Car


class User(models.Model):
    email = models.EmailField(max_length=50, default="default@example.com")
    password = models.TextField(max_length=50, default="password")
    name = models.CharField(max_length=50, blank=True, null=True, default="Guest")
    age = models.IntegerField(blank=True, null=True, default=0)
    cars = models.ManyToManyField(Car, related_name="owners", blank=True)

    def save(self, *args, **kwargs):
        if not self.name:
            self.name = "Guest"

        super(User, self).save(*args, **kwargs)

    def to_dict(self):
        return {
            "id": self.id,
            "email": self.email,
            "password": self.password,
            "name": self.name,
            "age": self.age,
            "cars": [car.to_dict() for car in self.cars.all()],
        }
