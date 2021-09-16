from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

app = Flask(__name__)



basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.sqlite')
db = SQLAlchemy(app)
ma = Marshmallow(app)

class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(144), unique=False)
    url = db.Column(db.String(144), unique=False)

    def __init__(self, description, url):
        self.description = description
        self.url = url

class ImageSchema(ma.Schema):
    class Meta:
        fields = ('description', 'url')


image_schema = ImageSchema()
images_schema = ImageSchema(many=True)

@app.route('/image', methods=["POST"])
def add_image():

    description = request.json['description']
    url = request.json['url']

    new_image = Image(description, url)

    db.session.add(new_image)
    db.session.commit()

    image = Image.query.get(new_image.id)

    return image_schema.jsonify(image)


@app.route("/images", methods=["GET"])
def get_images():
    all_images = Image.query.all()
    result = images_schema.dump(all_images)
    return jsonify(result)


@app.route("/image/<id>", methods=["GET"])
def get_image(id):
    image = Image.query.get(id)
    return image_schema.jsonify(image)


@app.route("/image/<id>", methods=["PUT"])
def image_update(id):
    image = Image.query.get(id)
    description = request.json['description']
    url = request.json['url']

    image.description = description
    image.url = url

    db.session.commit()
    return image_schema.jsonify(image)


@app.route("/image/<id>", methods=["DELETE"])
def image_delete(id):
    image = Image.query.get(id)
    db.session.delete(image)
    db.session.commit()

    return "Image was successfully deleted"

if __name__ == '__main__':
    app.run(debug=True)
