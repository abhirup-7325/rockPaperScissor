"""
ROCK, PAPER, SCISSORS

This file aims to create a GUI-based single-player game of rock, paper,scissors using pygame.

CREATED BY Abhirup Pal.
"""

# --------------------------------------Imports and Initialisations-----------------------------------------------------
import random
import pygame as p
import sys
import functools

p.init()

# --------------------------------------CONSTANTS-----------------------------------------------------------------------

# Dimension related
WIDTH = 700
HEIGHT = 600
DIMENSIONS = (WIDTH, HEIGHT)

# Color related
BG_COLOR = 0xc9aa88  # Peach color
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
SQUARE_COLOR = p.Color('Blue')

# Size related
BUTTON_SIZES = (WIDTH / 7, HEIGHT / 10)
ROCK_LOCATION = (WIDTH / 7, 2 * HEIGHT / 3)
PAPER_LOCATION = (3*WIDTH / 7, 2 * HEIGHT / 3)
SCISSOR_LOCATION = (5*WIDTH / 7, 2 * HEIGHT / 3)

# TODO -- Some size values are hard-coded in Window.draw_layout() method.


# ---------------------------------------------Class Definitions--------------------------------------------------------
class Window:
    """
    This class aims at drawing the screen and its contents.
    """
    def __init__(self, dim, bg_color, caption="~ Abhirup Pal"):
        p.init()
        self.screen = p.display.set_mode(dim)
        self.screen.fill(bg_color)
        p.display.set_caption(caption)

    def draw_rect_buttons_or_placeholders(self, color, location: tuple, size: tuple = (0, 0), text: str = None,
                                          text_color=WHITE, text_size=28):
        """
        For placeholder skip some of the parameters
        """
        p.draw.rect(self.screen, color, p.Rect(location[0], location[1], size[0], size[1]))
        self.screen.blit(p.font.SysFont('Arial', text_size).render(text, True, text_color),
                         (location[0] + 15, location[1]+15))

    def draw_layout(self):
        self.draw_rect_buttons_or_placeholders(color=SQUARE_COLOR, location=ROCK_LOCATION, size=BUTTON_SIZES,
                                               text="Rock")
        self.draw_rect_buttons_or_placeholders(color=SQUARE_COLOR, location=PAPER_LOCATION, size=BUTTON_SIZES,
                                               text="Paper")
        self.draw_rect_buttons_or_placeholders(color=SQUARE_COLOR, location=SCISSOR_LOCATION, size=BUTTON_SIZES,
                                               text="Scissor")
        self.draw_rect_buttons_or_placeholders(color=BG_COLOR, location=(180, 130), text="Rock, Paper, Scissors!",
                                               text_size=36)
        if len(MoveProcessing.move_Log) != 0 and len(MoveProcessing.generated_move_Log) != 0:
            self.draw_rect_buttons_or_placeholders(color=BG_COLOR, location=(100, 200), size=(1000, BUTTON_SIZES[1]))
            self.draw_rect_buttons_or_placeholders(color=BG_COLOR, location=(100, 200),
                                                   text="Your move is: " + MoveProcessing.move_Log[-1].move)
            self.draw_rect_buttons_or_placeholders(color=BG_COLOR, location=(100, 250), size=(1000, BUTTON_SIZES[1]))
            self.draw_rect_buttons_or_placeholders(color=BG_COLOR, location=(100, 250),
                                                   text="AI move is: " + MoveProcessing.generated_move_Log[-1].move,
                                                   text_color=BLACK)
            self.draw_rect_buttons_or_placeholders(color=BG_COLOR, location=(0, 0), size=(1000, BUTTON_SIZES[1]))
            self.draw_rect_buttons_or_placeholders(color=BG_COLOR, location=(0, 0),
                                                   text="Round: " + str(MoveProcessing.rounds_played),
                                                   text_color=BLACK)
            self.draw_rect_buttons_or_placeholders(color=BG_COLOR, location=(WIDTH - 250, 0),
                                                   size=(1000, BUTTON_SIZES[1]))
            self.draw_rect_buttons_or_placeholders(color=BG_COLOR, location=(WIDTH - 250, 0),
                                                   text="Your Score: " + str(MoveProcessing.my_score))
            self.draw_rect_buttons_or_placeholders(color=BG_COLOR, location=(WIDTH - 250, 60),
                                                   size=(1000, BUTTON_SIZES[1]))
            self.draw_rect_buttons_or_placeholders(color=BG_COLOR, location=(WIDTH - 250, 60),
                                                   text="Opponent Score: " + str(MoveProcessing.opp_score),
                                                   text_color=BLACK)


class MoveProcessing:
    """
    This class performs the operations and processing required by Move object. It also serves as a database to log the
    rounds, scores, valid moves and move logs.
    """
    moves = ["rock", "paper", "scissor"]
    rounds_played = 0
    my_score = 0
    opp_score = 0
    move_Log = []
    generated_move_Log = []

    @staticmethod
    def generate_move():
        generated_move = random.choices(MoveProcessing.moves)[0]
        return generated_move


@functools.total_ordering
class Move(MoveProcessing):
    """
    This class creates a new move and defines its properties.
    """
    def __init__(self, move):
        if move in super().moves:  # Valid move checking
            self.move = move
            super().move_Log.append(self)
        elif move == "null":
            self.move = MoveProcessing.generate_move()
            super().generated_move_Log.append(self)
        else:
            print("Invalid input")
            del self

    def __eq__(self, other):
        if isinstance(other, Move):
            if self.move == other.move:
                return True
            return False
        return NotImplemented

    def __lt__(self, other):
        if isinstance(other, Move):
            if self.move == "rock":
                if other.move == "paper":
                    return True
                return False
            elif self.move == "paper":
                if other.move == "scissor":
                    return True
                return False
            elif self.move == "scissor":
                if other.move == "rock":
                    return True
                return False


# ------------------------------------------main function---------------------------------------------------------------


def main():
    # Screen surface
    screen = Window(dim=DIMENSIONS, bg_color=BG_COLOR)
    screen.draw_layout()
    move = None
    while True:
        for event in p.event.get():
            if event.type == p.QUIT:
                p.quit()
                sys.exit()
            if event.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos()
                if (ROCK_LOCATION[0] <= location[0] <= ROCK_LOCATION[0]+BUTTON_SIZES[0] and
                        ROCK_LOCATION[1] <= location[1] <= ROCK_LOCATION[1] + BUTTON_SIZES[1]):
                    move = Move('rock')
                elif (PAPER_LOCATION[0] <= location[0] <= PAPER_LOCATION[0]+BUTTON_SIZES[0] and
                        PAPER_LOCATION[1] <= location[1] <= PAPER_LOCATION[1] + BUTTON_SIZES[1]):
                    move = Move('paper')
                elif (SCISSOR_LOCATION[0] <= location[0] <= SCISSOR_LOCATION[0]+BUTTON_SIZES[0] and
                        SCISSOR_LOCATION[1] <= location[1] <= SCISSOR_LOCATION[1] + BUTTON_SIZES[1]):
                    move = Move("scissor")

        if move:
            generated_move = Move("null")
            MoveProcessing.rounds_played += 1
            if move == generated_move:
                print("Draw")
            elif move > generated_move:
                MoveProcessing.my_score += 1
                print("Win")
            elif move < generated_move:
                MoveProcessing.opp_score += 1
                print("Loss")
            screen.draw_layout()
            move = None

        p.display.flip()


if __name__ == "__main__":
    main()
