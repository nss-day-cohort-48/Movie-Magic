from django.db import models


class Movie(models.Model):
    title = models.CharField(max_length=75)
    duration = models.IntegerField(blank=True, null=True)
    #  CASCADE = if director is deleted, also delete the movie
    #  SET_NULL = if director is deleted, set the director to NULL

    director = models.ForeignKey("Director",
                                 on_delete=models.SET_NULL,
                                 null=True)

    #  SET_DEFAULT = if genre is deleted, set the genre to default value (1)

    genre = models.ForeignKey("Genre",
                              on_delete=models.SET_DEFAULT,
                              default=1)

    actors = models.ManyToManyField("Actor",
                                    through="MovieActor",
                                    related_name="movies")

    @property
    def genre_name(self):
        return self.genre.label
