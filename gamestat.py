class GameStats():
    def __init__(self, st):
        self.st = st;
        self.rest_stats();
        self.game_active = False;



    def rest_stats(self):
        self.ships_left = self.st.ship_limit;
        self.score =0;