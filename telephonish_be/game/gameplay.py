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
    rounds = rounds * int(8 / len(rounds))

    return rounds


def get_player_series_for_room(room, num_rounds=8):
    players = list(room.players.values("id", "name", "is_spectator").all())
    player_series = {}

    for idx, player in enumerate(players):
        remaining_players = players[idx+1:] + players[:idx]
        get_prompt_from_players = []
        while len(get_prompt_from_players) < num_rounds:
            get_prompt_from_players += remaining_players

        player_series[player["name"]] = get_prompt_from_players[:num_rounds]

    return player_series







