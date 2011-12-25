import os
import Image, ImageOps
from bmps.sprites import *
import cStringIO
from sets import Card

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
        print e
    #card.show()
    ret = cStringIO.StringIO()
    card.save(ret, 'PNG')
    return ret
    
    
