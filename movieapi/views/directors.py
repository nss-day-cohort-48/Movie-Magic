"""View module for handling requests about directors"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from movieapi.models import Director


class DirectorView(ViewSet):
    """Movie Server directors"""

    def destroy(self, request, pk=None):
        """
        [summary]

        Args:
            request ([type]): [description]
            pk ([type], optional): [description]. Defaults to None.
        """
        try:
            genre = Director.objects.get(pk=pk)
            genre.delete()
            return Response({}, status=status.HTTP_204_NO_CONTENT)
        except Director.DoesNotExist as ex:
            return Response({'message': ex.args[0]})

    def retrieve(self, request, pk=None):
        """Handle GET requests for single director

        Returns:
            Response -- JSON serialized director
        """
        try:
            director = Director.objects.get(pk=pk)
            serializer = DirectorSerializer(director, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        """Handle GET requests to get all directors

        Returns:
            Response -- JSON serialized list of directors
        """
        directors = Director.objects.all()

        # Note the additional `many=True` argument to the
        # serializer. It's needed when you are serializing
        # a list of objects instead of a single object.
        serializer = DirectorSerializer(
            directors, many=True, context={'request': request})
        return Response(serializer.data)

class DirectorSerializer(serializers.ModelSerializer):
    """JSON serializer for directors

    Arguments:
        serializers
    """
    class Meta:
        model = Director
        fields = ('id', 'full_name')
