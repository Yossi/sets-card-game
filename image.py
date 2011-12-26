import os
import traceback
import cStringIO
import Image, ImageOps, ImageDraw
from sets import Card
from bmps.sprites import create, center

def draw(**kw):
    shape_size = 50, 90
    space = shape_size[0]//3
    margin = 10
    
    card = Image.new( 'RGB', ((shape_size[0]*3)+((margin+space)*2),
                               shape_size[1]   + (margin * 2)    ), 'white' )    
    
    if not os.path.isfile('shapes.png') \
       or Image.open('shapes.png').size != (shape_size[0]*3, shape_size[1]*3):
        #print "regenerating shapes.png... please stand by"
        create('shapes.png', shape_size)
    
    try:
        number = Card.numbers.index(kw['number']) + 1
        x1 = Card.shades.index(kw['shade']) * shape_size[0]
        x2 = x1 + shape_size[0]
        y1 = Card.shapes.index(kw['shape']) * shape_size[1]
        y2 = y1 + shape_size[1]

        shapes = Image.open('shapes.png')
        shape = shapes.crop( (x1,y1,x2,y2) )
        
        im = Image.new( 'L', (number*(shape_size[0]+space)-space, shape_size[1]), 'white' )
        for n in xrange(number):
            a = (shape_size[0]+space) * n
            b = a + shape_size[0]
            box = (a, 0, b, shape_size[1])
            im.paste(shape, box)
        im = ImageOps.colorize(im, kw['color'], 'white')

        card.paste(im, center(im, card.size))
    except Exception as e:
        draw = ImageDraw.Draw(card)
        error = traceback.format_exc()
        attributes = ' '.join(kw.values())
        for n, errLine in enumerate([attributes] + error.split('\n')):
            draw.text((0,15*n), errLine, fill='black')
    #card.show()
    
    ret = cStringIO.StringIO()
    card.save(ret, 'PNG')
    return ret
    
if __name__ == '__main__':
    # testing code follows. not expected to be left in working order
    c = draw(number='one', color='lue', shade='filled', shape='oval')

