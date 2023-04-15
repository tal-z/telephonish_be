from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import RoomSerializer
from rest_framework.exceptions import APIException

class RoomAlreadyExistsError(APIException):
    status_code = 403
    default_detail = 'room_already_exists'

class RoomCreateView(APIView):

    def post(self, request):
        serializer = RoomSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        if 'room_name' in serializer.errors:
            if serializer.errors['room_name'][0].code == 'unique':
                raise RoomAlreadyExistsError
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

