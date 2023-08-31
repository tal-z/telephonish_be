from django import forms
from django.http import JsonResponse

from rest_framework.views import APIView

from telephonish_be.game.models.drawing import Drawing
from telephonish_be.game.models.story import Story
from telephonish_be.game.models.poem import Poem
from telephonish_be.game.models.player import Player


class PoemForm(forms.ModelForm):
    class Meta:
        model = Poem
        fields = ["player", "room", "round_number", "poem"]


class SubmitPoemView(APIView):

    def post(self, request):
        form = PoemForm(request.data)

        if form.is_valid():
            form.save()
            return JsonResponse({"message": "Poem submitted successfully."})

        return JsonResponse({"errors": form.errors}, status=400)


class GetPoemView(APIView):

    def get(self, request):
        player_id = request.GET.get("player")
        room = request.GET.get("room")
        round_number = request.GET.get("round_number")

        try:
            poem = Poem.objects.get(player_id=player_id, room=room, round_number=round_number)
            data = {
                "poem_id": poem.id,
                "story_player_id": poem.player.id,
                "room_id": poem.room.id,
                "story_round_number": poem.round_number,
                "poem_text": poem.poem,
            }
            return JsonResponse(data)
        except Story.DoesNotExist:
            return JsonResponse({"error": "Story not found."}, status=404)
        except Player.DoesNotExist:
            return JsonResponse({"error": "Story Player not found."}, status=404)


class StoryForm(forms.ModelForm):
    class Meta:
        model = Story
        fields = ["player", "room", "round_number", "story"]


class SubmitStoryView(APIView):

    def post(self, request):
        form = StoryForm(request.data)

        if form.is_valid():
            form.save()
            return JsonResponse({"message": "Story submitted successfully."})

        return JsonResponse({"errors": form.errors}, status=400)


class GetStoryView(APIView):

    def get(self, request):
        player_id = request.GET.get("player")
        room = request.GET.get("room")
        round_number = request.GET.get("round_number")

        try:
            story = Story.objects.get(player_id=player_id, room=room, round_number=round_number)
            data = {
                "story_id": story.id,
                "story_player_id": story.player.id,
                "room_id": story.room.id,
                "story_round_number": story.round_number,
                "story_text": story.story,
            }
            return JsonResponse(data)
        except Story.DoesNotExist:
            return JsonResponse({"error": "Story not found."}, status=404)
        except Player.DoesNotExist:
            return JsonResponse({"error": "Story Player not found."}, status=404)


class DrawingForm(forms.ModelForm):
    class Meta:
        model = Drawing
        fields = ["player", "room", "round_number", "dataUrl", "prompt"]


class SubmitDrawingView(APIView):

    def post(self, request):
        form = DrawingForm(request.data)

        if form.is_valid():
            form.save()
            return JsonResponse({"message": "Drawing submitted successfully."})

        return JsonResponse({"errors": form.errors}, status=400)


class GetDrawingView(APIView):

    def get(self, request):
        player = request.GET.get("player")
        room = request.GET.get("room")
        round_number = request.GET.get("round_number")

        try:
            drawing = Drawing.objects.get(player=player, room=room, round_number=round_number)
            data = {
                "id": drawing.id,
                "player_id": drawing.player.id,
                "room_id": drawing.room.id,
                "round_number": drawing.round_number,
                "dataUrl": drawing.dataUrl,
                "prompt": drawing.prompt,
            }
            return JsonResponse(data)
        except Drawing.DoesNotExist:
            return JsonResponse({"error": "Drawing not found."}, status=404)
