from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True)

    def __str__(self):
        return self.name
class Product(models.Model):
    title = models.CharField( max_length=100)
    price = models.DecimalField( max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products")
    image = models.ImageField( upload_to='photos/')
    rating = models.DecimalField(default=0, max_digits=5, decimal_places=2)
    trending = models.BooleanField(default=False)

    def __str__(self):
        return self.title
    