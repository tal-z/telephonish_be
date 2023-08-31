
def get_round_order_for_room(room):
    """
    Currently returns a hard-coded list of round order,
    but eventually will use form data to determine round order.
    """

    rounds = [
        "one-sentence-story",
        "drawing",
        "poem",
        "drawing",
        "poem",
        "drawing",
        "poem",
        "drawing",
        "end",
    ]

    return rounds

def get_player_series_for_room(room, num_rounds=8):
    players = list(
        room.players.values("id", "name", "is_spectator").order_by("id").all()
    )
    player_series = {}

    for idx, player in enumerate(players):
        remaining_players = players[idx+1:] + players[:idx]
        get_prompt_from_players = remaining_players * (num_rounds // (len(remaining_players) or 1))
        get_prompt_from_players = get_prompt_from_players[:num_rounds]

        player_series[player["name"]] = get_prompt_from_players

    return player_series
