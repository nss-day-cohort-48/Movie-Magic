from django.db import models

class MovieActor(models.Model):
    movie = models.ForeignKey("Movie", on_delete=models.CASCADE)
    actor = models.ForeignKey("Actor", on_delete=models.CASCADE)
