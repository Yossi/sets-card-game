import sys
import sets
import pygame

MUTE, CHEAT = False, False
if 'mute' in sys.argv:
    MUTE = True
if 'cheat' in sys.argv:
    CHEAT = True

BGCOLOR = (0, 0, 0)
WIN_COLOR = (0, 200, 50)
PERSISTANT_HIGHLIGHT = (200, 0, 0)
TEMPORARY_HIGHLIGHT = (255, 255, 50)

SPACE_BETWEEN_CARDS = 7
COLUMNS = 4
ROWS = 4
FONT_SIZE = 30

def show_table(screen, table):
    for i, card in enumerate(table):
        x = (i % COLUMNS)  * (card.size[0] + SPACE_BETWEEN_CARDS) + SPACE_BETWEEN_CARDS
        y = (i // COLUMNS) * (card.size[1] + SPACE_BETWEEN_CARDS) + SPACE_BETWEEN_CARDS
        card.position = x, y
        screen.blit(pygame.image.load(card.draw()), (x, y))

def select_card(game, mouse_x, mouse_y):
    if mouse_x:
        for card in game.table:
            lower_x, upper_x = (card.position[0], card.position[0] + card.size[0])
            lower_y, upper_y = (card.position[1], card.position[1] + card.size[1])

            if lower_x < mouse_x < upper_x:
                if lower_y < mouse_y < upper_y:
                    return card

def toggle_selection(game, card):
    if card not in game.selected_cards:
        game.selected_cards.append(card)
    else:
        game.selected_cards.remove(card)

def show_scorecard(scorecard, game, my_font):
    score = my_font.render('Score: %s' % game.score, True, WIN_COLOR, BGCOLOR)
    num_sets = my_font.render('Possible sets: %s' % game.num_sets, True, WIN_COLOR, BGCOLOR)
    cards_left = my_font.render('Cards left in deck: %s' % len(game.deck), True, WIN_COLOR, BGCOLOR)
    scorecard.blit(score, (0, FONT_SIZE))
    scorecard.blit(num_sets, (0, FONT_SIZE*2))
    scorecard.blit(cards_left, (0, FONT_SIZE*3))

def cheat(game, screen):
    if game.num_sets:
        for card in game.find_sets()[0]:
            position = (card.position[0] + SPACE_BETWEEN_CARDS * 2,
                        card.position[1] + SPACE_BETWEEN_CARDS * 2)
            pygame.draw.circle(screen, PERSISTANT_HIGHLIGHT, position, SPACE_BETWEEN_CARDS)

def main():
    game = sets.Game()
    while not game.num_sets and game.is_more_deck():
        game.deal()

    card_size = sets.Card().size

    screen_size_x = (card_size[0] + SPACE_BETWEEN_CARDS) * COLUMNS + SPACE_BETWEEN_CARDS
    screen_size_y = (card_size[1] + SPACE_BETWEEN_CARDS) * ROWS + SPACE_BETWEEN_CARDS

    pygame.init()
    #logo = pygame.image.load("logo32x32.png")
    #pygame.display.set_icon(logo)
    my_font = pygame.font.Font('Comfortaa-Bold.ttf', FONT_SIZE)
    ding = pygame.mixer.Sound('ding.ogg')

    screen = pygame.display.set_mode((screen_size_x, screen_size_y))
    scorecard = screen.subsurface(pygame.Rect((screen_size_x - (card_size[0] + SPACE_BETWEEN_CARDS), screen_size_y - (card_size[1] + SPACE_BETWEEN_CARDS)), card_size))
    set_found = False
    game_is_running = True
    while game_is_running:
        screen.fill(BGCOLOR)

        show_table(screen, game.table)
        show_scorecard(scorecard, game, my_font)
        if CHEAT:
            cheat(game, screen)

        mouse_x, mouse_y = pygame.mouse.get_pos()
        active_card = select_card(game, mouse_x, mouse_y)

        if active_card:
            pygame.draw.rect(screen, TEMPORARY_HIGHLIGHT, (active_card.position[0], active_card.position[1], card_size[0], card_size[1]), SPACE_BETWEEN_CARDS*2)
        for card in game.selected_cards:
            pygame.draw.rect(screen, PERSISTANT_HIGHLIGHT, (card.position[0], card.position[1], card_size[0], card_size[1]), SPACE_BETWEEN_CARDS*2)

        if set_found:
            win_text = my_font.render('SET!', True, WIN_COLOR)
            for card in game.selected_cards:
                pygame.draw.rect(screen, WIN_COLOR, (card.position[0], card.position[1], card_size[0], card_size[1]), SPACE_BETWEEN_CARDS*2)
            screen.blit(win_text, (screen_size_x - (card_size[0] + SPACE_BETWEEN_CARDS), screen_size_y - (card_size[1] + SPACE_BETWEEN_CARDS)))
            pygame.display.update()
            if not MUTE:
                ding.play()
            pygame.time.delay(750)

            set_found = False
            game.remove_win_set()

            if len(game.table) < 12:
                game.deal()
            else:
                game.num_sets = len(game.find_sets())
            while not game.num_sets and game.is_more_deck():
                game.deal()

        if game.game_over():
            game_over = my_font.render('Game Over!', True, WIN_COLOR)
            scorecard.blit(game_over, (0, 0))

        pygame.display.update()

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                game_is_running = False
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONUP:
                if active_card:
                    toggle_selection(game, active_card)
                    set_found = game.is_score()


if __name__ == '__main__':
    main()
