from random import shuffle, choice
from PIL import Image, ImageOps, ImageDraw
import os
import traceback
import io
from bmps.sprites import create, center
from pprint import pprint
# rules of the game http://www.setgame.com/set/index.html

class Card(object):
    numbers = ('one', 'two', 'three')
    colors  = ('green', 'red', 'purple')
    shades  = ('solid', 'open', 'striped')
    shapes  = ('squiggle', 'diamond', 'oval')
    
    def __init__(self, **attributes):
        self.attributes = attributes

    def __repr__(self):
        return '(%s %s %s %s)' % (self.attributes['number'].center(len(max(self.numbers, key=len))),
                                  self.attributes['color'].center(len(max(self.colors, key=len))),
                                  self.attributes['shade'].center(len(max(self.shades, key=len))),
                                  self.attributes['shape'].center(len(max(self.shapes, key=len))))

    def filename(self):
        return '%s_%s_%s_%s.png' % (self.attributes['number'], self.attributes['color'],
                                    self.attributes['shade'],  self.attributes['shape'])

    def draw(self):
        shape_size = (50, 90)
        space = shape_size[0]//3
        margin = 10

        card = Image.new( 'RGB', ((shape_size[0]*3)+((margin+space)*2),
                                shape_size[1]   + (margin * 2)    ), 'white' )
        
        if not os.path.isfile('shapes.png') \
        or Image.open('shapes.png').size != (shape_size[0]*3, shape_size[1]*3):
            print("regenerating shapes.png... please stand by")
            create('shapes.png', shape_size)
        
        try:
            number = Card.numbers.index(self.attributes['number']) + 1
            x1 = Card.shades.index(self.attributes['shade']) * shape_size[0]
            x2 = x1 + shape_size[0]
            y1 = Card.shapes.index(self.attributes['shape']) * shape_size[1]
            y2 = y1 + shape_size[1]

            shapes = Image.open('shapes.png')
            shape = shapes.crop( (x1,y1,x2,y2) )
            
            im = Image.new( 'L', (number*(shape_size[0]+space)-space, shape_size[1]), 'white' )
            for n in range(number):
                a = (shape_size[0]+space) * n
                b = a + shape_size[0]
                box = (a, 0, b, shape_size[1])
                im.paste(shape, box)
            im = ImageOps.colorize(im, self.attributes['color'], 'white')

            card.paste(im, center(im, card.size))
        except Exception:
            draw = ImageDraw.Draw(card)
            error = traceback.format_exc()
            for n, errLine in enumerate([self.attributes] + error.split('\n')):
                draw.text((0,15*n), errLine, fill='black')
        
        #card.show()
        ret = io.BytesIO()
        card.save(ret, 'PNG')
        ret.seek(0, 0)
        return ret


class Deck(object):
    def __init__(self):
        self.cards = []

        for number in Card.numbers:
            for color in Card.colors:
                for shade in Card.shades:
                    for shape in Card.shapes:
                        self.cards.append( Card(number=number, color=color, shade=shade, shape=shape) )

        shuffle(self.cards)
    
    def __len__(self):
        return len(self.cards)
    
    def __iter__(self):
        return self
        
    def next(self):
        if len(self.cards) >= 3:
            return [self.cards.pop(), self.cards.pop(), self.cards.pop()]
        raise StopIteration
    
    def deal(self, *n):
        if n and isinstance(n[0], int) and n[0] > 1:
            ret = []
            for i in range(n[0]):
                ret.extend(self.next())
            return ret
        return self.next()

def find_sets(table):
    ret = []
    end = len(table)
    for x in range(0, end):
        for y in range(x+1, end):
            for z in range(y+1, end):
                A, B, C = table[x], table[y], table[z]
                if is_set(A, B, C):
                    ret.append([A, B, C])
    return ret
              
def is_set(*s):
    return all([len(set([c.attributes['number'] for c in s])) != 2,
                len(set([c.attributes['color'] for c in s])) != 2,
                len(set([c.attributes['shade'] for c in s])) != 2,
                len(set([c.attributes['shape'] for c in s])) != 2]) and len(s) == 3
    
def play():
    deck = Deck()
    table = deck.deal(4)
    while len(deck) or (len(table) and find_sets(table)):
        print('-----------', len(table), '-----------')
        pprint(table)
        sets = find_sets(table)
        if sets:
            s = choice(sets)
            print('Found', len(sets), '->', s)
            [table.remove(card) for card in s]
            if len(table) < 12 and len(deck):
                table.extend(deck.deal())
        else:
            table.extend(deck.deal())
            
if __name__ == '__main__':
    play()
    #a = Card( number='three', color='red', shade='solid', shape='oval' )
    #a.draw()
    #b = Card( number='two', color='green', shade='striped', shape='squiggle' )
    #b.draw()
    #c = Card( number='one', color='purple', shade='open', shape='diamond' )
    #c.draw()
