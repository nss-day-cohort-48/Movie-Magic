"""View module for handling requests about movies"""
from django.http import HttpResponseServerError
from django.core.exceptions import ValidationError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from movieapi.models import Movie, Genre, Director


class MovieView(ViewSet):
    """Movie Server movies"""

    def create(self, request):
        """
        [summary]

        Args:
            request ([type]): [description]
        """
        movie = Movie()

        movie.title = request.data["movieTitle"]
        movie.duration = request.data["movieDuration"]
        movie.genre = Genre.objects.get(pk=request.data["genreId"])
        movie.director = Director.objects.get(pk=request.data["directorId"])

        # get the list of actor ids from request

        actors = request.data["actorIds"]

        try:
            movie.save()

            movie.actors.set(actors)
            # creates relationships between all actors in actors list and the movie we just created

            serializer = MovieSerializer(movie, context={'request': request})
            return Response(serializer.data)

        except ValidationError as ex:
            return Response({'reason': ex.message})

    def update(self, request, pk=None):
        """
        [summary]

        Args:
            request ([type]): [description]
            pk ([type], optional): [description]. Defaults to None.
        """

        movie = Movie.objects.get(pk=pk)

        movie.title = request.data["movieTitle"]
        movie.duration = request.data["movieDuration"]
        movie.genre = Genre.objects.get(pk=request.data["genreId"])
        movie.director = Director.objects.get(pk=request.data["directorId"])

        actors = request.data["actorIds"]

        movie.actors.set(actors)

        try:
            movie.save()
            return Response({}, status=status.HTTP_204_NO_CONTENT)
        except ValidationError as ex:
            return Response({'reason': ex.message})

    def retrieve(self, request, pk=None):
        """Handle GET requests for single movie

        Returns:
            Response -- JSON serialized movie
        """
        try:
            movie = Movie.objects.get(pk=pk)
            serializer = MovieSerializer(
                movie, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        """Handle GET requests to get all movies

        Returns:
            Response -- JSON serialized list of movies
        """
        movies = Movie.objects.all()

        # Note the additional `many=True` argument to the
        # serializer. It's needed when you are serializing
        # a list of objects instead of a single object.
        serializer = MovieSerializer(
            movies, many=True, context={'request': request})
        return Response(serializer.data)


class MovieSerializer(serializers.ModelSerializer):
    """JSON serializer for movies

    Arguments:
        serializers
    """
    class Meta:
        model = Movie
        fields = ('id', 'title', 'duration', 'genre_name', 'director', 'actors')
        depth = 1
