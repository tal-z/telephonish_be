from collections import defaultdict

def get_round_order_for_room(room):
    story = room.one_sentence_story_round
    drawing = room.drawing_round
    poem = room.poem_round

    rounds = []

    if story:
        rounds.append("story")
    if drawing:
        rounds.append("drawing")
    if poem:
        rounds.append("poem")
        rounds.append("drawing")

    # always play eight rounds
    num_rounds = 8
    rounds = (round for round in rounds for _ in range(num_rounds // len(rounds)))

    return list(rounds)

def get_player_series_for_room(room, num_rounds=8):
    players = list(room.players.values("id", "name", "is_spectator").all())
    player_series = {}

    for idx, player in enumerate(players):
        remaining_players = players[idx+1:] + players[:idx]
        get_prompt_from_players = remaining_players * (num_rounds // len(remaining_players) + 1)
        get_prompt_from_players = get_prompt_from_players[:num_rounds]

        player_series[player["name"]] = get_prompt_from_players

    return player_series
