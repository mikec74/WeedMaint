from flask import Flask, render_template, redirect, url_for, flash, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
import os


app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY")
Bootstrap(app)


# CONNECT TO DB
# The current version of SQLAlchemy uses a URI of "postgresql://" when accessing a PostgreSQL database.
# Heroku uses a URI of "postgres://". Because of this difference, when running at Heroku, the system
# crashes because SQLAlchemy cannot connect to a URI of "postgres://". I added the replace() call to change
# the environment variable returned from Heroku into a URI that can be used by SQLAlchemy. If Heroku ever
# changes to use "postgresql://" like SQLAlchemy does, then this code should still work since the replace()
# call will not change the URI. If Heroku ever makes this change, you can remove the call to replace().
# This code was suggested by a post on StackOverflow:
#     https://stackoverflow.com/questions/66690321/flask-and-heroku-sqlalchemy-exc-nosuchmoduleerror-cant-load-plugin-sqlalchemy
#
# Running the program on my local computer uses a SQLite database. I want to continue to be able to run the
# program on my computer for development while it is also running on Heroku. This is accomplished by including
# the DATABASE_URL in an environment variable. The call to replace() has no effect on this URL because the
# URL on the local computer does not contain "postgres://".
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    "DATABASE_URL",
).replace("postgres://", "postgresql://", 1)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class PageHeader(db.Model):
    __tablename__ = "page_headers"
    id = db.Column(db.Integer, primary_key=True)
    image_url = db.Column(db.String(250), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    subtitle = db.Column(db.String(100), nullable=False)
    announcement = db.Column(db.Text, nullable=True)


class Weed(db.Model):
    __tablename__ = "weeds"
    id = db.Column(db.Integer, primary_key=True)
    scientific_name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    removal_method = db.Column(db.Text, nullable=False)
    comments = db.Column(db.Text, nullable=False)
    location_desc = db.Column(db.Text, nullable=False)
    location_map = db.Column(db.String(200), nullable=False)
    display_order = db.Column(db.Integer, nullable=False)


class WeedCommonName(db.Model):
    __tablename__ = "weed_common_names"
    id = db.Column(db.Integer, primary_key=True)
    common_name = db.Column(db.String(250), nullable=False)
    is_primary = db.Column(db.Boolean, nullable=False)
    weed_id = db.Column(db.Integer, db.ForeignKey("weeds.id"), nullable=False)

    weed = db.relationship("Weed", backref=db.backref("weed_common_names", lazy=True))


class WeedPhoto(db.Model):
    __tablename__ = "weed_photos"
    id = db.Column(db.Integer, primary_key=True)
    photo_url = db.Column(db.String(200), nullable=False)
    caption = db.Column(db.String(250), nullable=False)
    display_order = db.Column(db.Integer, nullable=False)
    weed_id = db.Column(db.Integer, db.ForeignKey("weeds.id"), nullable=False)

    weed = db.relationship("Weed", backref=db.backref("weed_photos"), lazy=True)


# Delete all rows from all tables.
# I tried using db.drop_all() but it always crashed when the application was being deployed.
WeedPhoto.query.delete()
WeedCommonName.query.delete()
Weed.query.delete()
PageHeader.query.delete()

db.session.commit()


# db.create_all()


@app.route('/')
def show_page():
    page_header = PageHeader(
        image_url="https://images.unsplash.com/photo-1631163468569-b5265125d578?ixlib=rb-1.2.1"\
                  "&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1470&q=80",
        title="Weed of the Week",
        subtitle="These invasives have to go!",
        announcement=None
    )
    db.session.add(page_header)

    weed1 = Weed(
        scientific_name="Leucanthemum vulgare",
        description="This plant has the typical daisy appearance with white petals and a yellow center. It grows "
                    "to a height of 1 to 3 feet.",
        removal_method="Pull the plant out by the roots. This "
                       "plant has a shallow root system, so you usually can pull out "
                       "all of the roots. However, it spreads by rhizomes, so some of the rhizomes may snap "
                       "when you pull the plant out of the ground. You may have more luck pulling out more "
                       "roots when the soil is moist "
                       "after a rain. When you pull the plant, make sure you put "
                       "the entire plant in a yard waste bag and remove the bag from the premises.",
        comments="This is a perennial from Eurasia. It is highly invasive and is regulated as an invasive "
                 "species in 13 states. Each flower can produce up to 200 seeds.",
        location_desc="Along the western edge of the ditch on the northern part of the property. Also, there "
                      "are some isolated plants at the south end of the ditch.",
        location_map="images/OxeyeDaisy-20220313.png",
        display_order=1
    )
    oxeye_daisy = WeedCommonName(
        common_name="oxeye daisy",
        is_primary=True
    )
    weed1.weed_common_names.append(oxeye_daisy)

    ox_eye_daisy = WeedCommonName(
        common_name="ox-eye daisy",
        is_primary=False
    )
    weed1.weed_common_names.append(ox_eye_daisy)

    dog_daisy = WeedCommonName(
        common_name="dog daisy",
        is_primary=False
    )
    weed1.weed_common_names.append(dog_daisy)

    marguerite = WeedCommonName(
        common_name="marguerite",
        is_primary=False
    )
    weed1.weed_common_names.append(marguerite)

    bull_daisy = WeedCommonName(
        common_name="bull daisy",
        is_primary=False
    )
    weed1.weed_common_names.append(bull_daisy)

    button_daisy = WeedCommonName(
        common_name="button daisy",
        is_primary=False
    )
    weed1.weed_common_names.append(button_daisy)

    field_daisy = WeedCommonName(
        common_name="field daisy",
        is_primary=False
    )
    weed1.weed_common_names.append(field_daisy)

    photo3 = WeedPhoto(
        photo_url="images/OxeyeDaisy-2.jpg",
        caption="Oxeye daisy stem has very small leaves",
        display_order=2
    )
    weed1.weed_photos.append(photo3)

    photo4 = WeedPhoto(
        photo_url="images/OxeyeDaisy-1.jpg",
        caption="The classic daisy look",
        display_order=1
    )
    weed1.weed_photos.append(photo4)

    db.session.add(weed1)
    db.session.commit()

    return render_template("index.html")


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
