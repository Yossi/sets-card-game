# rules of the game https://www.setgame.com/file/set-english
from random import shuffle, choice
from PIL import Image, ImageOps, ImageDraw
import os
import traceback
import io
from bmps.sprites import create, center
from pprint import pprint
from collections import deque

class Card():
    numbers = ('one', 'two', 'three')
    colors = ('green', 'red', 'purple')
    shades = ('solid', 'open', 'striped')
    shapes = ('squiggle', 'diamond', 'stadium')
    
    # adjustable numbers to tweak cards' look
    multiplier = 2
    shape_size = (50 * multiplier, 90 * multiplier)
    space = shape_size[0]//3
    margin = 10 * multiplier
    
    size = (shape_size[0]*3)+((margin+space)*2), shape_size[1]+(margin*2)

    def __init__(self, **attributes):
        self.attributes = attributes
        self.valid = self.is_valid()

    def __repr__(self):
        if self.valid:
            return '(%s %s %s %s)' % (self.attributes['number'].center(len(max(self.numbers, key=len))),
                                      self.attributes['color'].center(len(max(self.colors, key=len))),
                                      self.attributes['shade'].center(len(max(self.shades, key=len))),
                                      self.attributes['shape'].center(len(max(self.shapes, key=len))))
        return 'invalid card: %s' % self.attributes

    def is_valid(self):
        return all((self.attributes.get('number', None) in self.numbers,
                    self.attributes.get('color', None) in self.colors,
                    self.attributes.get('shade', None) in self.shades,
                    self.attributes.get('shape', None) in self.shapes))

    def filename(self):
        if self.valid:
            return '%s_%s_%s_%s.png' % (self.attributes['number'], self.attributes['color'],
                                        self.attributes['shade'],  self.attributes['shape'])
        else:
            return 'invalid.png'

    def draw(self):
        '''returns filelike object'''

        card = Image.new('RGB', self.size, 'white')

        if not os.path.isfile('shapes.png') or Image.open('shapes.png').size != (self.shape_size[0]*3, self.shape_size[1]*3):
            print("regenerating shapes.png... please stand by")
            create('shapes.png', self.shape_size)

        try:
            number = Card.numbers.index(self.attributes['number']) + 1
            x1 = Card.shades.index(self.attributes['shade']) * self.shape_size[0]
            x2 = x1 + self.shape_size[0]
            y1 = Card.shapes.index(self.attributes['shape']) * self.shape_size[1]
            y2 = y1 + self.shape_size[1]

            shapes = Image.open('shapes.png')
            shape = shapes.crop((x1, y1, x2, y2))

            im = Image.new('L', (number*(self.shape_size[0]+self.space)-self.space, self.shape_size[1]), 'white')
            for n in range(number):
                a = (self.shape_size[0]+self.space) * n
                b = a + self.shape_size[0]
                box = (a, 0, b, self.shape_size[1])
                im.paste(shape, box)
            im = ImageOps.colorize(im, self.attributes['color'], 'white')

            card.paste(im, center(im, card.size))
        except Exception:
            draw = ImageDraw.Draw(card)
            error = traceback.format_exc()
            for n, errLine in enumerate([self.attributes] + error.split('\n')):
                draw.text((0, 15 * n), errLine, fill='black')

        #card.show()
        ret = io.BytesIO()
        card.save(ret, 'PNG')
        ret.seek(0, 0)
        return ret


class Deck():
    def __init__(self):
        self.cards = []

        for number in Card.numbers:
            for color in Card.colors:
                for shade in Card.shades:
                    for shape in Card.shapes:
                        self.cards.append(Card(number=number, color=color, shade=shade, shape=shape))

        shuffle(self.cards)

    def __len__(self):
        return len(self.cards)

    def __iter__(self):
        return iter(self)

    def next(self):
        if len(self.cards) >= 3:
            return [self.cards.pop(), self.cards.pop(), self.cards.pop()]
        raise StopIteration

    def deal(self, *n):
        if n and isinstance(n[0], int) and n[0] > 1:
            ret = []
            for _ in range(n[0]):
                ret.extend(self.next())
            return ret
        return self.next()


class Game():
    def is_set(*s):
        # only look at 3 cards at a time. each attribute must be all different (len(3)) or all the same (len(1))
        return len(s) == 3 and \
               all({c.valid for c in s}) and \
               all([len({c.attributes['number'] for c in s}) != 2,
                    len({c.attributes['color'] for c in s}) != 2,
                    len({c.attributes['shade'] for c in s}) != 2,
                    len({c.attributes['shape'] for c in s}) != 2])

    def __init__(self):
        self.deck = Deck()
        self.table = self.deck.deal(4)
        self.selected_cards = deque([], 3)
        self.score = 0
        self.num_sets = len(self.find_sets())

    def is_more_deck(self):
        return bool(len(self.deck))

    def remove_set(self, s):
        for card in s:
            self.table.remove(card)

    def remove_win_set(self):
        self.remove_set(self.selected_cards)
        self.selected_cards.clear()
        self.score += 1

    def find_sets(self, table=None):
        '''returns list of ALL sets on table'''
        if table is None:
            table = self.table
        ret = []
        end = len(table)
        for x in range(0, end):
            for y in range(x+1, end):
                for z in range(y+1, end):
                    A, B, C = table[x], table[y], table[z]
                    if Game.is_set(A, B, C):
                        ret.append([A, B, C])
        return ret

    def deal(self):
        try:
            self.table.extend(self.deck.deal())
        except StopIteration:
            pass
        finally:
            self.num_sets = len(self.find_sets())

    def is_score(self):
        return Game.is_set(*self.selected_cards)


def play():
    game = Game()
    while game.is_more_deck() or (len(game.table) and game.find_sets()):
        print('-----------', len(game.table), '-----------')
        pprint(game.table)
        sets = game.find_sets()
        if sets:
            s = choice(sets)
            print('Found', len(sets), '->', s)
            game.remove_set(s)
            if len(game.table) < 12 and game.is_more_deck():
                game.deal()
        else:
            game.deal()

if __name__ == '__main__':
    play()
    #a = Card( number='three', color='red', shade='solid', shape='stadium' )
    #a.draw()
    #b = Card( number='two', color='green', shade='striped', shape='squiggle' )
    #b.draw()
    #c = Card( number='one', color='purple', shade='open', shape='diamond' )
    #c.draw()
