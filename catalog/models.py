from django.db import models
from django.urls import reverse

class Category(models.Model):
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse("catalog:category_detail", kwargs={"slug": self.slug})
    

class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    bio = models.TextField(blank=True)
    photo = models.ImageField(blank=True, upload_to="authors/")
    slug = models.SlugField(unique=True)

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        ordering = ["last_name"]
        verbose_name = "Автор"
        verbose_name_plural = "Авторы"


    def __str__(self):
        return self.full_name
    
    def get_absolute_url(self):
        return reverse("catalog:author_detail", kwargs={"slug": self.slug})
    
class Book(models.Model):
    title = models.CharField(max_length=300)   
    slug = models.SlugField(unique=True)
    authors = models.ManyToManyField(Author)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="books")
    description = models.TextField(blank=True)
    cover = models.ImageField(blank=True, upload_to="covers/")
    price = models.DecimalField(max_digits=8, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    available = models.BooleanField(default=True)
    created_at= models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["title"]    
        verbose_name = "Книга"
        verbose_name_plural = "Книги"
        indexes = [
            models.Index(fields=["price"])
        ]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("catalog:book_detail", kwargs={"slug": self.slug})
    