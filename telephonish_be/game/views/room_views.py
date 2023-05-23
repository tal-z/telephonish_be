from django.http import JsonResponse

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import APIException

from telephonish_be.game.serializers import RoomSerializer
from telephonish_be.game.models.room import Room
from telephonish_be.game.models.player import Player

class RoomAlreadyExistsError(APIException):
    status_code = 403
    default_detail = 'room_already_exists'


class RoomDoesNotExistError(APIException):
    status_code = 403
    default_detail = 'room_does_not_exist'


class InvalidPasswordError(APIException):
    status_code = 403
    default_detail = 'invalid_password_provided'



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


class RoomJoinView(APIView):
    """Deprecated"""
    def post(self, request):
        data = request.data
        room_name = data.get("game_room_name")
        player_name = data.get("player_name")
        provided_password = data.get("password")
        try:
            room = Room.objects.get(room_name=room_name)
            if not room.provided_password_is_valid(provided_password):
                raise InvalidPasswordError

            is_spectator = room.current_round_number > 0
            new_player = Player.objects.create(
                name=player_name,
                emoji="🛸",
                room=room,
                is_spectator=is_spectator,

            )
            return JsonResponse(
                {
                    'player_added': True,
                    'new_player': {
                        "player_id": new_player.id,
                        "player_name": new_player.name,
                        "is_spectator": new_player.is_spectator,
                    },
                    "room_name": room_name,
                    "room_id": room.id,
                }
            )

        except Room.DoesNotExist:
            raise RoomDoesNotExistError



class GetRoomDataView(APIView):
    def get(self, request, room_name):
        try:
            room_instance = Room.objects.get(room_name=room_name)
            room_players = Player.objects.filter(room=room_instance).values("id", "name", "is_spectator")
        except Room.DoesNotExist:
            return JsonResponse({'error': 'Room does not exist'})

        data = {
            "room_data": {
                "room_id": room_instance.id,
                "room_name": room_instance.room_name,
                "current_round_number": room_instance.current_round_number,
                "one_sentence_story_round": room_instance.one_sentence_story_round,
                "drawing_round": room_instance.drawing_round,
                "poem_round": room_instance.poem_round,
                "dramatic_reading_round": room_instance.dramatic_reading_round,
                "password_required": room_instance.password_required,
            },
            "player_data": {
                player["id"]: {"name": player["name"], "id": player["id"]}
                for player in room_players
            }
        }

        return JsonResponse(data)

class CheckPasswordRequirementView(APIView):
    def get(self, request, room_name):
        try:
            room_instance = Room.objects.get(room_name=room_name)
            return JsonResponse({"password_required": room_instance.password_required})

        except Room.DoesNotExist:
            return JsonResponse({'error': 'Room does not exist'})



