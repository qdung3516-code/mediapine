import random

WIDTH, HEIGHT = 960, 720
BASKET_Y = 640
BASKET_WIDTH = 150
HOLD_FRAMES = 15
NO_HAND_FRAMES = 45
WIN_SCORE = 1500
POWER_COST = 5


class Game:
    def __init__(self):
        self.state = "MENU"
        self.best = 0
        self.fingers = None
        self.hold = 0
        self.new_game()

    def new_game(self):
        self.score = 0
        self.lives = 3
        self.energy = 4
        self.basket_x = WIDTH / 2
        self.things = []
        self.frame = 0
        self.slow = 0
        self.big = 0
        self.shield = False
        self.won = False

    def level(self):
        return self.score // 300 + 1

    def basket_width(self):
        return BASKET_WIDTH * 2 if self.big > 0 else BASKET_WIDTH

    def see_fingers(self, fingers):
        if fingers == self.fingers:
            self.hold += 1
        else:
            self.fingers = fingers
            self.hold = 1

        if fingers is None and self.hold == NO_HAND_FRAMES and self.state == "PLAY":
            self.state = "PAUSE"
        if fingers is not None and self.hold == HOLD_FRAMES:
            self.gesture(fingers)

    def gesture(self, fingers):
        if self.state == "MENU" and fingers == 5:
            self.new_game()
            self.state = "PLAY"
        elif self.state == "PLAY" and fingers == 0:
            self.state = "PAUSE"
        elif self.state == "PLAY" and 1 <= fingers <= 4:
            self.use_power(fingers)
        elif self.state == "PAUSE" and fingers in (0, 5):
            self.state = "PLAY"
        elif self.state == "OVER" and fingers == 5:
            self.state = "MENU"

    def use_power(self, fingers):
        if self.energy < POWER_COST:
            return False
        self.energy -= POWER_COST
        if fingers == 1:
            self.slow = 150
        elif fingers == 2:
            self.big = 180
        elif fingers == 3:
            self.shield = True
        elif fingers == 4:
            self.things = [t for t in self.things if t["kind"] != "bomb"]
        return True

    def update(self, hand_x):
        if self.state != "PLAY":
            return
        self.frame += 1
        self.slow = max(0, self.slow - 1)
        self.big = max(0, self.big - 1)

        if hand_x is not None:
            self.basket_x += (hand_x - self.basket_x) / 3
        half = self.basket_width() / 2
        self.basket_x = min(max(self.basket_x, half), WIDTH - half)

        gap = max(12, 36 - 3 * self.level())
        if self.frame % gap == 0:
            self.add_thing()

        speed = 5 + self.level()
        if self.slow > 0:
            speed = speed / 2

        for thing in self.things[:]:
            thing["y"] += speed
            if thing["y"] >= BASKET_Y:
                self.things.remove(thing)
                if abs(thing["x"] - self.basket_x) <= half:
                    self.catch(thing["kind"])
                else:
                    self.miss(thing["kind"])

        if self.lives <= 0 or self.score >= WIN_SCORE:
            self.won = self.score >= WIN_SCORE
            self.best = max(self.best, self.score)
            self.things = []
            self.state = "OVER"

    def add_thing(self):
        r = random.random()
        if r < 0.2:
            kind = "bomb"
        elif r < 0.27:
            kind = "star"
        else:
            kind = "fruit"
        self.things.append({"kind": kind, "x": random.randint(40, WIDTH - 40), "y": 0})

    def catch(self, kind):
        if kind == "fruit":
            self.score += 10
            self.energy = min(10, self.energy + 1)
        elif kind == "star":
            self.score += 50
            self.energy = min(10, self.energy + 3)
        else:
            self.lose_life()

    def miss(self, kind):
        if kind == "fruit":
            self.lose_life()

    def lose_life(self):
        if self.shield:
            self.shield = False
        else:
            self.lives -= 1
