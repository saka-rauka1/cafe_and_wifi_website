import os
from flask import Flask, render_template, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, Boolean
from flask_bootstrap import Bootstrap5
from forms import CafeForm, DeleteForm


# Create DB
class Base(DeclarativeBase):
    pass


# Create Table
class Cafe(Base):
    __tablename__ = "cafe"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(250), unique=True)
    map_url: Mapped[str] = mapped_column(String(500))
    img_url: Mapped[str] = mapped_column(String(500))
    location: Mapped[str] = mapped_column(String(250))
    has_sockets: Mapped[bool] = mapped_column(Boolean)
    has_toilet: Mapped[bool] = mapped_column(Boolean)
    has_wifi: Mapped[bool] = mapped_column(Boolean)
    can_take_calls: Mapped[bool] = mapped_column(Boolean)
    seats: Mapped[str] = mapped_column(String(250), nullable=True)
    coffee_price: Mapped[str] = mapped_column(String(250), nullable=True)

    def __repr__(self):
        return f"id: {self.id} name: {self.name}"


# Initialize app
app = Flask(__name__)
app.secret_key = os.environ.get("secret_key")
Bootstrap5(app)

# Initialize database
db = SQLAlchemy(model_class=Base)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///cafes.db"
db.init_app(app)

with app.app_context():
    db.create_all()

# todo Handle non unique names with database entry
# todo Handle invalid db requests
# todo Could replace the delete form with a button by each cafe entry


# Create Routes
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/cafes")
def cafes():
    column_headers = [column.name for column in Cafe.__table__.columns]
    cafes_list = db.session.execute(db.select(Cafe)).scalars()
    return render_template("cafes.html", column_headers=column_headers, cafes=cafes_list)


@app.route("/add", methods=["GET", "POST"])
def add_cafe():
    cafe_form = CafeForm()
    if cafe_form.validate_on_submit():
        new_cafe = Cafe(
            name=cafe_form.name.data,
            map_url=cafe_form.map_url.data,
            img_url=cafe_form.img_url.data,
            location=cafe_form.location.data,
            has_sockets=cafe_form.has_sockets.data,
            has_toilet=cafe_form.has_toilet.data,
            has_wifi=cafe_form.has_wifi.data,
            can_take_calls=cafe_form.can_take_calls.data,
            seats=cafe_form.seats.data,
            coffee_price=cafe_form.coffee_price.data,
        )
        db.session.add(new_cafe)
        db.session.commit()

        return redirect("/cafes")

    return render_template("add.html", form=cafe_form)


@app.route("/delete", methods=["GET", "POST"])
def delete_cafe():
    delete_form = DeleteForm()
    if delete_form.validate_on_submit():
        cafe_name = delete_form.name.data
        cafe = db.session.execute(db.select(Cafe).filter_by(name=cafe_name)).scalar_one()
        db.session.delete(cafe)
        db.session.commit()

        return redirect("/cafes")

    return render_template("delete.html", form=delete_form)


if __name__ == '__main__':
    app.run(debug=True)
