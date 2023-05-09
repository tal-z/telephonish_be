from django.http import JsonResponse
from django.core import serializers

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import APIException

from telephonish_be.game.serializers import RoomSerializer
from telephonish_be.game.models.room import Room

class RoomAlreadyExistsError(APIException):
    status_code = 403
    default_detail = 'room_already_exists'


class RoomCreateView(APIView):

    def post(self, request):
        serializer = RoomSerializer(data=request.data)
        if serializer.is_valid():
            selected_values = request.data.get('selected_values', {})
            one_sentence_story_round = selected_values.get('oneSentenceStory', None)
            drawing_round = selected_values.get('drawing', None)
            poem_round = selected_values.get('poem', None)
            dramatic_reading_round = selected_values.get('dramaticReading', None)
            password = request.data.get('password', None) or None

            serializer.save(
                one_sentence_story_round=one_sentence_story_round,
                drawing_round=drawing_round,
                poem_round=poem_round,
                dramatic_reading_round=dramatic_reading_round,
                password=password,
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        if 'room_name' in serializer.errors:
            if serializer.errors['room_name'][0].code == 'unique':
                raise RoomAlreadyExistsError
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetRoomDataView(APIView):
    def get(self, request, room_name):
        try:
            room_instance = Room.objects.get(room_name=room_name)
        except Room.DoesNotExist:
            return JsonResponse({'error': 'Room does not exist'})

        data = {
            "room_name": room_instance.room_name,
            "current_round_number": room_instance.current_round_number,
            "one_sentence_story_round": room_instance.one_sentence_story_round,
            "drawing_round": room_instance.drawing_round,
            "poem_round": room_instance.poem_round,
            "dramatic_reading_round": room_instance.dramatic_reading_round,
        }

        return JsonResponse(data)

class CheckPasswordRequirementView(APIView):
    def get(self, request, room_name):
        try:
            room_instance = Room.objects.get(room_name=room_name)
        except Room.DoesNotExist:
            return JsonResponse({'error': 'Room does not exist'})

        password_required = bool(room_instance.password)

        return JsonResponse({"password_required": password_required})


