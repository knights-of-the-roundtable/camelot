class Player:
    """A simple player class"""
    def __init__(self, first, last, email, id):
        self._firstname = first
        self._lastname = last
        self._email = email
        self._id = id
        self._score = 0

    def get_id(self):
        return self._id

    def get_first(self):
        return self._firstname

    def get_last(self):
        return self._lastname

    def get_name(self):
        return '{}{}'.format(self._firstname,self._lastname)

    def get_email(self):
        return self._email

    def get_score(self):
        return self._score

    def increment_score(self):
        self._score += 1

    def decrement_score(self):
        self._score -= 1

class Score:
    """A class that stores score for a player"""
    def __init__(self, id, name, points):
        self._player_id = id
        self._player_name = name
        self._player_score = points

class Players:
    """A class that stores all players"""
    def __init__(self):
        self._players = {}
        self._players_count = 0

    def addPlayer(self, first, last, email, id):
        self._players[id] = Player(first, last, email, id)
        self._players_count += 1

    def get_players(self):
        return self._players

    def get_num_players(self):
        return self._players_count

    def get_player_names(self):
        name_list = []
        for player in self._players:
            name_list.append(player.get_name)

    def get_scores(self):
        scores = []
        for player in self._players:
            scores.append(Score(player.get_id, player.get_name, player.get_score))
        return scores


class Outcome:
    """A class that stores attributes of an outcome for a game of Avalon"""
    def __init__(self, id, name):
        self._outcome_id = id
        self._outcome_name = name

    def get_outcome_id(self):
        return self._outcome_id

    def get_outcome_name(self):
        return self._outcome_name


class Outcomes:
    """A class that stores all outcomes possible for a game of Avalon"""
    def __init__(self):
        self._outcomes = {}

    def add_outcome(self, id, name):
        self._outcomes[id] = Outcome(id, name)

    def get_outcomes(self):
        return self._outcomes


class Role:
    """A class that stores attributes of a role"""
    def __init__(self, id, name):
        self._role_id = id
        self._role_name = name

    def get_role_id(self):
        return self._role_id

    def get_role_name(self):
        return self._role_name


class Roles:
    """A class that stores attributes of a role"""
    def __init__(self):
        self_roles = {}

    def add_role(self, id, name):
        self._roles[id] = Role(id, name)

    def get_roles(self):
        return self._roles


class Game:
    """A class that store attributes of an Avalon Game"""
    def __init__(self, id, mvp, lvp, outcome, date):
        self._game_id = id
        self._mvp_id = mvp
        self._lvp_id = lvp
        self._outcome = outcome
        self._player_role_map = {}
        self._date = date

    def add_player(self, roleid, playerid):
        self._player_role_map[roleid] = playerid

    def get_id(self):
        return self._game_id

    def get_date(self):
        return self._date

    def get_mvp(self):
        return self._mvp_id

    def get_lvp(self):
        return self._lvp_id

    def get_outcome(self):
        return self._outcome

    def get_players(self):
        return self._player_role_map

    def get_player_for_role(self, role):
        return self._player_role_map[role._role_id]


class Games:
    """A class that stores all games"""
    def __init__(self):
        self._games = {}
        self._games_count = 0

    def addGame(self, mvp, lvp, outcome, id, date):
        self._games[id] = Game(mvp, lvp, outcome, id, date)
        self._games_count += 1

    def get_games(self):
        return self._games

    def get_game(self, id):
        return self._games[id]

