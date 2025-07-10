from flask import Flask, render_template, request, redirect, flash, abort
from flask_sqlalchemy import SQLAlchemy
import json
from sqlalchemy.ext.declarative import DeclarativeMeta

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///main.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = '49ad7504707fd3944eb0df3294c00376'
db = SQLAlchemy(app)


class AlchemyEncoder(json.JSONEncoder):

  def default(self, obj):
    if isinstance(obj.__class__, DeclarativeMeta):
      # an SQLAlchemy class
      fields = {}
      for field in [
          x for x in dir(obj) if not x.startswith('_') and x != 'metadata'
      ]:
        data = obj.__getattribute__(field)
        try:
          json.dumps(
            data)  # this will fail on non-encodable values, like other classes
          fields[field] = data
        except TypeError:
          fields[field] = None
      # a json-encodable dict
      return fields

    return json.JSONEncoder.default(self, obj)


class car(db.Model):
  id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
  brand = db.Column(db.String)
  model = db.Column(db.String)
  year = db.Column(db.Integer)
  price = db.Column(db.Integer)
  sales = db.Column(db.Integer)
  wear = db.Column(db.String)
  color = db.Column(db.String)
  datereleased = db.Column(db.Date)
  filename = db.Column(db.String)


class question(db.Model):
  id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
  name = db.Column(db.String)
  email = db.Column(db.String)
  text = db.Column(db.Text)


@app.route('/')
def index():
  #return "hi"
  #cars = car.query.all()
  topcars = car.query.order_by(car.sales.desc()).all()
  carsnew = car.query.order_by(car.price).all()
  brands = db.session.query(car.brand).distinct().all()
  return render_template('index.html',
                         carsnew=carsnew,
                         topcars=topcars,
                         brands=brands)


@app.route('/search')
def search():
  return render_template('search.html')


@app.route('/car/<int:id>')
def cardetail(id):
  cartoreturn = car.query.get_or_404(id)
  try:
    carssuggested = car.query.filter_by(brand=cartoreturn.brand).all()[:10]
  except:
    carssuggested = car.query.filter_by(brand=cartoreturn.brand).all()
  return render_template('cardetail.html',
                         car=cartoreturn,
                         carssuggested=carssuggested)


@app.route('/aboutus', methods=["POST", "GET"])
def aboutus():
  if request.method == "POST":
    name = request.form["name"]
    email = request.form["email"]
    message = request.form["message"]
    nuquestion = question(name=name, email=email, text=message)
    try:
      db.session.add(nuquestion)
      db.session.commit()
      flash("Success!")
      return redirect('/')
    except:
      return "error on POST"
  return render_template('about.html')


@app.route('/brands/<string:brand>')
def brands(brand):
  brandcars = car.query.filter_by(brand=brand).all()
  if len(brandcars) == 0:
    return abort(404)
  return render_template('brandpage.html', brandcars=brandcars, brand=brand)


@app.route('/sources')
def sources():
  return render_template('sources.html')


@app.route('/team')
def team():
  return render_template('team.html')
  

@app.route('/working', methods=["POST", "GET"])
def working():
  if request.method == "POST":
    print(request.get_data())
    jsonarr = json.loads(request.get_data())

    querys = db.session.query(car).filter(
      car.brand.in_(jsonarr["brand"]), car.color.in_(jsonarr["color"]),
      car.wear.in_(jsonarr["wear"]),
      car.price.between(0, int(jsonarr["maxPrice"])),
      car.year.is_(jsonarr["year"])).all()

    jsontoreturn = json.dumps(querys, cls=AlchemyEncoder)
    jsontoreturn += '\n'
    return jsontoreturn

with app.app_context():
  db.create_all()
if __name__ == "__main__":
  #app.run()
  app.run(host='0.0.0.0')
