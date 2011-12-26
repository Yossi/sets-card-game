from random import shuffle, choice

class Card(object):
    numbers = ('one', 'two', 'three')
    colors  = ('green', 'red', 'purple')
    shades  = ('filled', 'shaded', 'empty')
    shapes  = ('squiggle', 'diamond', 'oval')
    
    def __init__(self, **attributes):
        self.attributes = attributes
        
    def __repr__(self):
        return '(%s %s %s %s)' % (self.attributes['number'].center(len(max(self.numbers, key=len))),
                                  self.attributes['color'].center(len(max(self.colors, key=len))),
                                  self.attributes['shade'].center(len(max(self.shades, key=len))),
                                  self.attributes['shape'].center(len(max(self.shapes, key=len))))

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
    return all([len(set([c.attributes['number'] for c in s])) != 2,
                len(set([c.attributes['color'] for c in s])) != 2,
                len(set([c.attributes['shade'] for c in s])) != 2,
                len(set([c.attributes['shape'] for c in s])) != 2]) and len(s) == 3
    
def play():
    deck = Deck()
    table = deck.deal(4)
    while len(deck) or (len(table) and find_sets(table)):
        print '-----------', len(table), '-----------'
        print table
        sets = find_sets(table)
        if sets:
            s = choice(sets)
            print 'Found', len(sets), '->', s
            [table.remove(card) for card in s]
            if len(table) < 12 and len(deck):
                table.extend(deck.deal())
        else:
            table.extend(deck.deal())
            
if __name__ == '__main__':
    play()
    #a = Card( number='three', color='red', shade='filled', shape='oval' )
    #a.draw()
    #b = Card( number='two', color='green', shade='shaded', shape='squiggle' )
    #b.draw()
    #c = Card( number='one', color='purple', shade='empty', shape='diamond' )
    #c.draw()
