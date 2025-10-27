from django.db import models

class User(models.Model):
    email = models.EmailField(unique=True)
    fam = models.CharField(max_length=128)
    name = models.CharField(max_length=128)
    otc = models.CharField(max_length=128)
    phone = models.CharField(max_length=32)

    def __str__(self):
        return f"{self.name} {self.fam}"

class Coords(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()
    height = models.IntegerField()

    def __str__(self):
        return f"{self.latitude}, {self.longitude}, {self.height}m"

class Pereval(models.Model):
    STATUS_CHOICES = [
        ('new', 'New'),
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]

    beauty_title = models.CharField(max_length=32, default="пер.")
    title = models.CharField(max_length=256)
    other_titles = models.CharField(max_length=256, blank=True)
    connect = models.TextField(blank=True)
    add_time = models.DateTimeField()
    status = models.CharField(max_length=16, choices=STATUS_CHOICES, default='new')

    # Внешние ключи
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='perevals')
    coords = models.ForeignKey(Coords, on_delete=models.CASCADE, null=True, blank=True)

    # Уровни сложности
    winter = models.CharField(max_length=16, blank=True)
    summer = models.CharField(max_length=16, blank=True)
    autumn = models.CharField(max_length=16, blank=True)
    spring = models.CharField(max_length=16, blank=True)

    def __str__(self):
        return self.title

class Image(models.Model):
    title = models.CharField(max_length=256)
    path = models.CharField(max_length=512)

    def __str__(self):
        return self.title

class PerevalImage(models.Model):
    pereval = models.ForeignKey(Pereval, on_delete=models.CASCADE, related_name='images')
    image = models.ForeignKey(Image, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('pereval', 'image')
    def __str__(self):
        return f"{self.pereval.title} - {self.image.title}"