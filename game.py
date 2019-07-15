from pprint import pprint
import pygame
import sets


BLACK = (0, 0, 0)
GREEN = (0, 200, 50)
RED = (255, 0, 0)
BLUE = (0, 50, 150)
PURPLE = (255, 0, 255)
YELLOW = (255, 255, 0)

SPACE_BETWEEN_CARDS = 7
COLUMNS = 4
ROWS = 4
FONT_SIZE = 30

def show_table(screen, table):
    for i, card in enumerate(table):
        x = (i % COLUMNS)    * (card.size[0] + SPACE_BETWEEN_CARDS) + SPACE_BETWEEN_CARDS
        y = (i // COLUMNS) * (card.size[1] + SPACE_BETWEEN_CARDS) + SPACE_BETWEEN_CARDS
        card.position = x, y
        screen.blit(pygame.image.load(card.draw()), (x, y))

def select_card(game, mouse_x, mouse_y):
    if mouse_x:
        for card in game.table:
            lower_x, upper_x = (card.position[0], card.position[0] + card.size[0])
            lower_y, upper_y = (card.position[1], card.position[1] + card.size[1])

            if mouse_x > lower_x and mouse_x < upper_x:
                if mouse_y > lower_y and mouse_y < upper_y:
                    if card not in game.selected_cards:
                        game.selected_cards.append(card)
                    else:
                        game.selected_cards.remove(card)
                    return


def main():
    pygame.init()
    pygame.font.init()
    #logo = pygame.image.load("logo32x32.png")
    #pygame.display.set_icon(logo)

    game = sets.Game()
    ###REMOVE: CHEAT###
    print(game.find_sets())
    ###################

    my_font = pygame.font.SysFont('Times New Roman', FONT_SIZE)

    card_size = sets.Card().size

    screen_size_x = (card_size[0] + SPACE_BETWEEN_CARDS) * COLUMNS + SPACE_BETWEEN_CARDS
    screen_size_y = (card_size[1] + SPACE_BETWEEN_CARDS) * ROWS + SPACE_BETWEEN_CARDS

    screen = pygame.display.set_mode((screen_size_x, screen_size_y))

    set_found = False
    game_is_running = True
    while game_is_running:
        screen.fill(BLACK)

        mouse_x, mouse_y = None, None
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                game_is_running = False
                quit()
            if event.type == pygame.MOUSEBUTTONUP:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                select_card(game, mouse_x, mouse_y)
                set_found = game.is_selected_set()

        for card in game.selected_cards:
            pygame.draw.rect(screen, RED, (card.position[0], card.position[1], card_size[0], card_size[1]), SPACE_BETWEEN_CARDS*2)

        if set_found:
            textsurface = my_font.render('SET!', False, GREEN)
            screen.blit(textsurface, (screen_size_x - (card_size[0] + SPACE_BETWEEN_CARDS), screen_size_y - (card_size[1] + SPACE_BETWEEN_CARDS)))

        show_table(screen, game.table)

        pygame.display.update()

if __name__ == '__main__':
    main()
