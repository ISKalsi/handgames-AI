from random import randint
from cv2 import VideoCapture
from handgames.detection import detect_number


class Player:
    def __init__(self, name, video_capture: VideoCapture = None):
        self.name = name
        self.video_feed = video_capture

    def next_move(self):
        if self.video_feed is None:
            yield randint(1, 10)
        else:
            for num in detect_number(self.video_feed):
                yield num


class Innings:
    def __init__(self, number: int, batter: Player, bowler: Player):
        self.number = number
        self.batter = batter
        self.bowler = bowler
        self.runs = 0
        self.moves = []

    @property
    def last_move(self):
        return self.moves[-1] if len(self.moves) != 0 else None


class Match:
    def __init__(self, is_batting_first: bool, video_capture: VideoCapture):
        player = Player("Player", video_capture)
        cpu = Player("CPU")

        if is_batting_first:
            first_innings = Innings(1, batter=player, bowler=cpu)
        else:
            first_innings = Innings(1, batter=cpu, bowler=player)

        self.innings: list[Innings] = [first_innings]
        self.players: tuple[Player, Player] = (player, cpu)
        self.winner: Player = None

    @property
    def current_innings(self):
        return self.innings[-1]

    @property
    def previous_innings(self):
        return self.innings[-2]

    @property
    def is_second_innings(self) -> bool:
        return self.current_innings.number == 2

    @property
    def did_achieve_target(self) -> bool:
        return self.current_innings.runs >= self.previous_innings.runs

    @staticmethod
    def is_number_valid(num: int) -> bool:
        return 1 <= num <= 10

    def start_match(self) -> bool:
        while True:
            bat = -1
            for num in self.current_innings.batter.next_move():
                if num is not None:
                    bat = num
                yield False
            ball = -1
            for num in self.current_innings.bowler.next_move():
                if num is not None:
                    ball = num
                else:
                    yield False

            if bat == ball:
                self.hit_wicket(ball)
                if self.is_second_innings:
                    self.winner = self.current_innings.bowler
                    break
                else:
                    self.proceedToNextInnings()
            else:
                self.play_ball(bat, ball)
                if self.is_second_innings and self.did_achieve_target:
                    self.winner = self.current_innings.batter
                    break

            yield True
        yield True

    def play_ball(self, bat: int, ball: int):
        if not (Match.is_number_valid(bat) or Match.is_number_valid(ball)):
            raise Exception("Invalid number: " + str(bat) + " or " + str(ball))
        self.current_innings.runs += bat
        self.current_innings.moves.append((bat, ball))

    def hit_wicket(self, ball: int):
        self.current_innings.moves.append((ball, ball))

    def proceedToNextInnings(self):
        newInnings = Innings(number=self.current_innings.number+1,
                             batter=self.current_innings.bowler,
                             bowler=self.current_innings.batter)
        self.innings.append(newInnings)
