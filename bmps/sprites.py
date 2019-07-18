from PIL import Image, ImageEnhance
import glob, os

def center(im, background):
    ix, iy = im.size
    sx, sy = background
    x = ( sx - ix ) // 2
    y = ( sy - iy ) // 2
    return x, y

def create(filename, shape_size):
    output = Image.new('RGB', tuple(map(lambda x: x*3, shape_size)), 'white')
        
    for infile in glob.iglob("bmps/*.bmp"):
        n = os.path.split(infile)[-1]
        name, ext = os.path.splitext(n)
        x_scale = ('solid', 'open', 'striped').index(name.split('_')[0])
        y_scale = ('squiggle', 'diamond', 'oval').index(name.split('_')[1])
        im = Image.open(infile)
        im.thumbnail(shape_size, Image.ANTIALIAS) # thumbnail rather than resize to keep aspect ratio
        shape = Image.new('L', shape_size, 'white')
        shape.paste(im, center(im, shape_size))
        shape = ImageEnhance.Color(shape).enhance(0.0)
        shape = shape.point(lambda x: 255 if x >= 230 else x)
        shape = shape.point(lambda x: 0 if x <= 25 else x)
        output.paste( shape, (shape.size[0]*x_scale, shape.size[1]*y_scale,
                              shape.size[0]*(x_scale+1), shape.size[1]*(y_scale+1)) )
    output.save(filename)
