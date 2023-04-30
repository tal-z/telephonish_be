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
            # Get the new field values from the request data
            one_sentence_story_round = request.data.get('selected_values', {}).get('oneSentenceStory', None)
            drawing_round = request.data.get('selected_values', {}).get('drawing', None)
            poem_round = request.data.get('selected_values', {}).get('poem', None)
            dramatic_reading_round = request.data.get('selected_values', {}).get('dramaticReading', None)

            # Call serializer.save() with the new field values
            serializer.save(
                one_sentence_story_round=one_sentence_story_round,
                drawing_round=drawing_round,
                poem_round=poem_round,
                dramatic_reading_round=dramatic_reading_round
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        if 'room_name' in serializer.errors:
            if serializer.errors['room_name'][0].code == 'unique':
                raise RoomAlreadyExistsError
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

