import unittest

from game import BASKET_Y, HOLD_FRAMES, NO_HAND_FRAMES, Game
from hand import count_fingers


def fake_hand(up):
    points = [(0, 0)] * 21
    points[0] = (300, 400)
    for name, tip, joint, x in [("index", 8, 6, 275), ("middle", 12, 10, 300),
                                ("ring", 16, 14, 322), ("pinky", 20, 18, 342)]:
        points[joint] = (x, 260)
        points[tip] = (x, 200) if name in up else (x, 310)
    points[17] = (342, 310)
    points[3] = (220, 325)
    points[4] = (185, 295) if "thumb" in up else (290, 320)
    return points


def show(game, fingers):
    for _ in range(HOLD_FRAMES):
        game.see_fingers(fingers)


def playing_game():
    game = Game()
    show(game, 5)
    return game


def drop(game, kind, x):
    game.things = [{"kind": kind, "x": x, "y": BASKET_Y - 1}]
    game.frame = 1
    game.update(None)


class TestFingers(unittest.TestCase):
    def test_count(self):
        self.assertEqual(count_fingers(fake_hand([])), 0)
        self.assertEqual(count_fingers(fake_hand(["index"])), 1)
        self.assertEqual(count_fingers(fake_hand(["index", "middle"])), 2)
        self.assertEqual(count_fingers(fake_hand(["thumb", "index", "middle"])), 3)
        self.assertEqual(count_fingers(fake_hand(["index", "middle", "ring", "pinky"])), 4)
        self.assertEqual(count_fingers(fake_hand(["thumb", "index", "middle", "ring", "pinky"])), 5)


class TestGame(unittest.TestCase):
    def test_open_hand_starts(self):
        game = Game()
        self.assertEqual(game.state, "MENU")
        show(game, 5)
        self.assertEqual(game.state, "PLAY")

    def test_must_hold(self):
        game = Game()
        for _ in range(HOLD_FRAMES - 1):
            game.see_fingers(5)
        self.assertEqual(game.state, "MENU")

    def test_fist_pauses_and_open_hand_resumes(self):
        game = playing_game()
        show(game, 0)
        self.assertEqual(game.state, "PAUSE")
        show(game, 5)
        self.assertEqual(game.state, "PLAY")

    def test_no_hand_pauses(self):
        game = playing_game()
        for _ in range(NO_HAND_FRAMES):
            game.see_fingers(None)
        self.assertEqual(game.state, "PAUSE")

    def test_catch_fruit_and_star(self):
        game = playing_game()
        drop(game, "fruit", game.basket_x)
        drop(game, "star", game.basket_x)
        self.assertEqual(game.score, 60)

    def test_miss_fruit_loses_life(self):
        game = playing_game()
        drop(game, "fruit", 900)
        self.assertEqual(game.lives, 2)

    def test_bomb(self):
        game = playing_game()
        drop(game, "bomb", 900)
        self.assertEqual(game.lives, 3)
        drop(game, "bomb", game.basket_x)
        self.assertEqual(game.lives, 2)

    def test_power_needs_energy(self):
        game = playing_game()
        game.energy = 4
        show(game, 1)
        self.assertEqual(game.slow, 0)
        game.energy = 10
        show(game, 2)
        self.assertGreater(game.big, 0)
        self.assertEqual(game.energy, 5)

    def test_slow_and_big(self):
        game = playing_game()
        game.energy = 10
        game.use_power(1)
        game.use_power(2)
        game.things = [{"kind": "fruit", "x": 100, "y": 0}]
        game.frame = 1
        game.update(None)
        self.assertEqual(game.things[0]["y"], (5 + 1) / 2)
        self.assertEqual(game.basket_width(), 300)

    def test_shield(self):
        game = playing_game()
        game.energy = 10
        show(game, 3)
        drop(game, "bomb", game.basket_x)
        self.assertEqual(game.lives, 3)
        drop(game, "bomb", game.basket_x)
        self.assertEqual(game.lives, 2)

    def test_clear_bombs(self):
        game = playing_game()
        game.energy = 10
        game.things = [{"kind": "bomb", "x": 100, "y": 50}, {"kind": "fruit", "x": 200, "y": 50}]
        show(game, 4)
        self.assertEqual([t["kind"] for t in game.things], ["fruit"])

    def test_win_and_lose(self):
        game = playing_game()
        game.score = 1490
        drop(game, "fruit", game.basket_x)
        self.assertEqual(game.state, "OVER")
        self.assertTrue(game.won)
        game = playing_game()
        game.lives = 1
        drop(game, "fruit", 900)
        self.assertEqual(game.state, "OVER")
        self.assertFalse(game.won)


if __name__ == "__main__":
    unittest.main()
