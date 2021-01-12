import pygame

from constants import Player, BLACK, GRAY, WHITE

IMAGE_PATH = 'ui_data/'

BOARD_WIDTH = 500
BOARD_HEIGHT = 500
MESSAGE_BOX_HEIGHT = 100
MARGIN = 27
CELL = (BOARD_WIDTH - 2 * MARGIN) / 10
PIECE = 40
BUTTON_WIDTH = 190
BUTTON_HEIGHT = 40


class GameRenderer:
    def __init__(self, game):
        self._game = game

        # initialize pygame
        pygame.init()

        self.__font = pygame.font.Font(r'ui_data/cmu.ttf', 24)

        self.__screen = pygame.display.set_mode([BOARD_WIDTH, BOARD_HEIGHT + MESSAGE_BOX_HEIGHT])
        pygame.display.set_caption('Gomokai')

        self.__game_over_message_box = GameInfoBox(pygame.Rect(0, BOARD_HEIGHT, BOARD_WIDTH, MESSAGE_BOX_HEIGHT),
                                                   self.__font)
        self.__game_over_message_box.draw_empty(self.__screen)
        self.__game_over_message_box.draw_replay_button(self.__screen)

        self.__ui_chessboard = pygame.image.load(IMAGE_PATH + '11_board_dark.png').convert()
        self.__ui_chessboard = pygame.transform.scale(self.__ui_chessboard, (BOARD_WIDTH, BOARD_HEIGHT))
        self.__ui_piece_black = pygame.image.load(IMAGE_PATH + 'piece_black.png').convert_alpha()
        self.__ui_piece_black = pygame.transform.smoothscale(self.__ui_piece_black, (PIECE, PIECE))
        self.__ui_piece_white = pygame.image.load(IMAGE_PATH + 'piece_white.png').convert_alpha()
        self.__ui_piece_white = pygame.transform.smoothscale(self.__ui_piece_white, (PIECE, PIECE))

    @staticmethod
    def coordinate_transform_map2pixel(row, column):
        return MARGIN + column * CELL - PIECE / 2, MARGIN + row * CELL - PIECE / 2

    def coordinate_transform_pixel2map(self, x, y):
        (row, column) = (int(y // CELL), int(x // CELL))

        if row < 0 or row >= self._game.board.board_size or column < 0 or column >= self._game.board.board_size:
            return None, None
        else:
            return row, column

    def draw_board(self):
        self.__screen.blit(self.__ui_chessboard, (0, 0))

    def place_piece_at_cell(self, row, column, player):
        x_coordinate, y_coordinate = self.coordinate_transform_map2pixel(row, column)
        self.place_piece_at_coordinates(x_coordinate, y_coordinate, player)

    def place_piece_at_coordinates(self, x_coordinate, y_coordinate, player):
        if player == Player.BLACK:
            self.__screen.blit(self.__ui_piece_black, (x_coordinate, y_coordinate))
        elif player == Player.WHITE:
            self.__screen.blit(self.__ui_piece_white, (x_coordinate, y_coordinate))

    def draw_message(self, message, game_over=False):
        self.__game_over_message_box.draw_message(self.__screen, message)

        if game_over:
            self.__game_over_message_box.draw_replay_button(self.__screen)

    def was_play_again_pressed(self):
        return self.__game_over_message_box.was_pressed()


class GameInfoBox:
    def __init__(self, rectangle, font):
        self.__rectangle = rectangle
        self.__font = font
        self.__background_colour = pygame.Color(GRAY)
        self.__text_colour = pygame.Color(WHITE)

        self.done_button = UIImageButton([self.__rectangle[0] + (self.__rectangle[2] / 2) - BUTTON_WIDTH // 2,
                                          self.__rectangle[1] + self.__rectangle[3] - BUTTON_HEIGHT - 10,
                                          BUTTON_WIDTH, BUTTON_HEIGHT], 'play_again.png')

    def was_pressed(self):
        return self.done_button.was_pressed()

    def is_inside(self, screen_position):
        is_inside = False
        if self.__rectangle[0] <= screen_position[0] <= self.__rectangle[0] + self.__rectangle[2]:
            if self.__rectangle[1] <= screen_position[1] <= self.__rectangle[1] + self.__rectangle[3]:
                is_inside = True
        return is_inside

    def draw_empty(self, screen):
        pygame.draw.rect(screen, self.__background_colour, pygame.Rect(self.__rectangle[0], self.__rectangle[1],
                                                                       self.__rectangle[2], self.__rectangle[3]), 0)

    def draw_message(self, screen, message):
        self.draw_empty(screen)

        message_text_render = self.__font.render(message, True, self.__text_colour)

        screen.blit(message_text_render,
                    message_text_render.get_rect(centerx=self.__rectangle.centerx,
                                                 centery=self.__rectangle[1] + 20))

    def draw_replay_button(self, screen):
        self.done_button.draw(screen)


class UIImageButton:
    def __init__(self, rectangle, path_to_image):
        self.__image = pygame.transform.scale(pygame.image.load(IMAGE_PATH + path_to_image).convert_alpha(),
                                              (rectangle[2], rectangle[3]))
        self.__rectangle = pygame.Rect(rectangle)

    def was_pressed(self):
        mouse_position = pygame.mouse.get_pos()
        return self.__rectangle.collidepoint(mouse_position)

    def draw(self, screen):
        pygame.Surface.blit(screen, self.__image, self.__rectangle)
