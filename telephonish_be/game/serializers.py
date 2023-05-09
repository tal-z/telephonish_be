from rest_framework import serializers
from .models.room import Room


class RoomSerializer(serializers.ModelSerializer):
    one_sentence_story_round = serializers.BooleanField(required=False)
    drawing_round = serializers.BooleanField(required=False)
    poem_round = serializers.BooleanField(required=False)
    dramatic_reading_round = serializers.BooleanField(required=False)
    password = serializers.CharField(required=False, allow_blank=True, trim_whitespace=True)
    class Meta:
        model = Room
        fields = ['id', 'room_name', 'current_round_number', 'one_sentence_story_round', 'drawing_round', 'poem_round', 'dramatic_reading_round', 'password']
        read_only_fields = ['id']

