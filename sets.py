import os
from random import shuffle, choice
import Image, ImageOps
from bmps.sprites import *

class Card(object):
    def __init__(self, **kw):
        self.number = kw['number']
        self.color = kw['color']
        self.shade = kw['shade']
        self.shape = kw['shape']
        
    def __repr__(self):
        return '(%s %s %s %s)' % (self.number.center(len(max(Deck.numbers, key=len))),
                                  self.color.center(len(max(Deck.colors, key=len))),
                                  self.shade.center(len(max(Deck.shades, key=len))), 
                                  self.shape.center(len(max(Deck.shapes, key=len))))
    def draw(self):
        shape_size = 50, 90
        space = shape_size[0]//3
        margin = 10
        
        if not os.path.isfile('shapes.png') \
           or Image.open('shapes.png').size != (shape_size[0]*3, shape_size[1]*3):
            print "regenerating shapes.png... please stand by"
            create('shapes.png', shape_size)
        
        number = Deck.numbers.index(self.number) + 1
        x1 = Deck.shades.index(self.shade) * shape_size[0]
        x2 = x1 + shape_size[0]
        y1 = Deck.shapes.index(self.shape) * shape_size[1]
        y2 = y1 + shape_size[1]

        shapes = Image.open('shapes.png')
        shape = shapes.crop( (x1,y1,x2,y2) )
        
        im = Image.new( 'L', (number*(shape_size[0]+space)-space, shape_size[1]), 'white' )
        for n in xrange(number):
            a = (shape_size[0]+space) * n
            b = a + shape_size[0]
            box = (a, 0, b, shape_size[1])
            im.paste(shape, box)
        im = ImageOps.colorize(im, self.color, 'white')

        card = Image.new( 'RGB', ((shape_size[0]*3)+((margin+space)*2),
                                 shape_size[1]   + (margin * 2)    ), 'white' )
        card.paste(im, center(im, card.size))
        card.show()        

class Deck(object):
    numbers = ('one', 'two', 'three')
    colors  = ('green', 'red', 'purple')
    shades  = ('filled', 'shaded', 'empty')
    shapes  = ('squiggle', 'diamond', 'oval')
    
    def __init__(self):
        self.cards = []

        for number in Deck.numbers:
            for color in Deck.colors:
                for shade in Deck.shades:
                    for shape in Deck.shapes:
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
            for i in xrange(n[0]):
                ret.extend(self.next())
            return ret
        return self.next() 

def find_sets(table):
    ret = []
    end = len(table)
    for x in xrange(0, end):
        for y in xrange(x+1, end):
            for z in xrange(y+1, end):
                A, B, C = table[x], table[y], table[z]
                if is_set(A, B, C):
                    ret.append([A, B, C])
    return ret
              
def is_set(*s):
    return all([len(set([c.number for c in s])) != 2,
                len(set([c.color for c in s])) != 2,
                len(set([c.shade for c in s])) != 2,
                len(set([c.shape for c in s])) != 2])
    
def play():
    deck = Deck()
    table = deck.deal(4)
    while len(deck):
        print '-----------', len(table), '-----------'
        print table
        sets = find_sets(table)
        if sets:
            s = choice(sets)
            print 'Found ', len(sets), ' ->', s
            [table.remove(card) for card in s]
            if len(table) < 12:
                table.extend(deck.deal())
        else:    
            table.extend(deck.deal())
            
if __name__ == '__main__':
    #play()
    a = Card( number='three', color='red', shade='filled', shape='oval' )
    a.draw()
    b = Card( number='two', color='green', shade='shaded', shape='squiggle' )
    b.draw()
    c = Card( number='one', color='purple', shade='empty', shape='diamond' )
    c.draw()
