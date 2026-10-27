import cv2

from game import BASKET_Y, HEIGHT, WIDTH, Game
from hand import Hand, count_fingers

WHITE = (255, 255, 255)
COLORS = {"fruit": (40, 40, 220), "star": (0, 220, 255), "bomb": (200, 60, 160)}


def write(img, text, x, y, size=0.8, color=WHITE):
    cv2.putText(img, text, (x, y), cv2.FONT_HERSHEY_SIMPLEX, size, (0, 0, 0), 5)
    cv2.putText(img, text, (x, y), cv2.FONT_HERSHEY_SIMPLEX, size, color, 2)


def draw(img, game, points, fingers):
    for thing in game.things:
        cv2.circle(img, (int(thing["x"]), int(thing["y"])), 22, COLORS[thing["kind"]], -1)
    half = int(game.basket_width() / 2)
    x = int(game.basket_x)
    color = (255, 200, 0) if game.shield else (40, 90, 150)
    cv2.rectangle(img, (x - half, BASKET_Y), (x + half, BASKET_Y + 25), color, -1)

    if points:
        for px, py in points:
            cv2.circle(img, (int(px), int(py)), 4, (80, 220, 80), -1)
        write(img, f"Fingers: {fingers}", 20, HEIGHT - 20)

    if game.state == "MENU":
        write(img, "HAND CATCH", 330, 250, 1.6, (0, 220, 255))
        write(img, "Open hand (5 fingers) = start", 260, 330)
        write(img, "Fist = pause   1-4 fingers = powers", 220, 380)
    elif game.state == "PLAY":
        write(img, f"Score {game.score}  Lives {game.lives}  Energy {game.energy}", 20, 40)
        write(img, "1 Slow  2 Big  3 Shield  4 No bombs (cost 5)", 20, 80, 0.6)
    elif game.state == "PAUSE":
        write(img, "PAUSED - open hand to play", 260, 330, 1.0)
    else:
        write(img, "YOU WIN!" if game.won else "GAME OVER", 340, 280, 1.6)
        write(img, f"Score {game.score}  Best {game.best}", 330, 340)
        write(img, "Open hand = menu", 360, 390)


def main():
    camera = cv2.VideoCapture(0)
    hand = Hand()
    game = Game()
    while True:
        ok, frame = camera.read()
        if not ok:
            break
        frame = cv2.flip(cv2.resize(frame, (WIDTH, HEIGHT)), 1)

        points = hand.find(frame)
        if points:
            fingers = count_fingers(points)
            hand_x = points[9][0]
        else:
            fingers = None
            hand_x = None

        game.see_fingers(fingers)
        game.update(hand_x)

        draw(frame, game, points, fingers)
        cv2.imshow("Hand Catch", frame)
        if cv2.waitKey(1) & 0xFF in (27, ord("q")):
            break
    camera.release()
    hand.detector.close()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
