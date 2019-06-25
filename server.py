from sets import Card
from flask import render_template, url_for, Blueprint, Flask, send_file
app = Blueprint('sets', __name__, url_prefix='/sets')

@app.route('/<attributes>.png')
def card(attributes):
    attr = {}
    for attribute in attributes.split('_'):
        if attribute in Card().numbers:
            attr['number'] = attribute
        if attribute in Card().colors:
            attr['color'] = attribute
        if attribute in Card().shades:
            attr['shade'] = attribute
        if attribute in Card().shapes:
            attr['shape'] = attribute
        
    c = Card(**attr)

    return send_file(c.draw(), 
                      attachment_filename=c.filename(),
                      mimetype='image/png')

if __name__ == '__main__':
    a = Flask(__name__)
    a.register_blueprint(app)
    a.run(host='0.0.0.0', debug=True)