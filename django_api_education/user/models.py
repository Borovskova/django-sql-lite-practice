from django.db import models
 
class User(models.Model):
    email = models.EmailField(max_length = 50, default='default@example.com')
    password = models.TextField(max_length = 50, default='password')
    name = models.CharField(max_length=50, blank=True, null=True, default='Guest')
    age = models.IntegerField(blank=True, null=True, default=0)

    def save(self, *args, **kwargs):
        if not self.name:
            self.name = 'Guest'
        super(User, self).save(*args, **kwargs)

    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'password': self.password,
            'name': self.name,
            'age': self.age,
        }