from functools import wraps

from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func


app = Flask(__name__)
app.config["SECRET_KEY"] = "dev-secret-key-change-for-production"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///pet_adoption.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class Staff(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    full_name = db.Column(db.String(120), nullable=False)


class Pet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    species = db.Column(db.String(80), nullable=False)
    breed = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(30), nullable=False, default="Available")
    adoption_fee = db.Column(db.Float, nullable=False, default=0)

    applications = db.relationship("Application", back_populates="pet", cascade="all, delete-orphan")
    adoptions = db.relationship("Adoption", back_populates="pet")


class Adopter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(30), nullable=False)
    address = db.Column(db.String(200), nullable=False)

    applications = db.relationship("Application", back_populates="adopter", cascade="all, delete-orphan")
    adoptions = db.relationship("Adoption", back_populates="adopter")

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"


class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pet_id = db.Column(db.Integer, db.ForeignKey("pet.id"), nullable=False)
    adopter_id = db.Column(db.Integer, db.ForeignKey("adopter.id"), nullable=False)
    status = db.Column(db.String(30), nullable=False, default="Pending")
    notes = db.Column(db.Text, nullable=False)

    pet = db.relationship("Pet", back_populates="applications")
    adopter = db.relationship("Adopter", back_populates="applications")
    adoption = db.relationship("Adoption", back_populates="application", uselist=False)


class Adoption(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pet_id = db.Column(db.Integer, db.ForeignKey("pet.id"), nullable=False)
    adopter_id = db.Column(db.Integer, db.ForeignKey("adopter.id"), nullable=False)
    application_id = db.Column(db.Integer, db.ForeignKey("application.id"), nullable=False, unique=True)
    adoption_date = db.Column(db.Date, nullable=False, server_default=func.current_date())
    fee_paid = db.Column(db.Float, nullable=False)

    pet = db.relationship("Pet", back_populates="adoptions")
    adopter = db.relationship("Adopter", back_populates="adoptions")
    application = db.relationship("Application", back_populates="adoption")


def login_required(view):
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        if "staff_id" not in session:
            flash("Please log in to continue.", "info")
            return redirect(url_for("login"))
        return view(*args, **kwargs)

    return wrapped_view


def is_blank(value):
    return value is None or value.strip() == ""


def validate_required(form, fields):
    errors = []
    for field, label in fields:
        if is_blank(form.get(field)):
            errors.append(f"{label} is required. Please enter a value before saving.")
    return errors


def validate_pet_form(form):
    errors = validate_required(
        form,
        [
            ("name", "Name"),
            ("species", "Species"),
            ("breed", "Breed"),
            ("age", "Age"),
            ("status", "Status"),
            ("adoption_fee", "Adoption fee"),
        ],
    )
    try:
        age = int(form.get("age", ""))
        if age < 0:
            errors.append("Pet age cannot be negative. Enter 0 or a positive whole number.")
    except ValueError:
        errors.append("Pet age must be a whole number, such as 0, 2, or 5.")

    try:
        adoption_fee = float(form.get("adoption_fee", ""))
        if adoption_fee < 0:
            errors.append("Adoption fee cannot be negative. Enter 0.00 or a positive amount.")
    except ValueError:
        errors.append("Adoption fee must be a valid number, such as 75 or 125.50.")

    return errors


def validate_adopter_form(form):
    errors = validate_required(
        form,
        [
            ("first_name", "First name"),
            ("last_name", "Last name"),
            ("email", "Email"),
            ("phone", "Phone"),
            ("address", "Address"),
        ],
    )
    if not is_blank(form.get("email")) and "@" not in form.get("email"):
        errors.append("Email address is invalid. Please include @, such as name@example.com.")
    return errors


def validate_application_form(form):
    return validate_required(
        form,
        [
            ("pet_id", "Pet"),
            ("adopter_id", "Adopter"),
            ("status", "Status"),
            ("notes", "Notes"),
        ],
    )


@app.route("/")
def index():
    if "staff_id" in session:
        return redirect(url_for("dashboard"))
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()
        staff = Staff.query.filter_by(username=username, password=password).first()
        if staff:
            session["staff_id"] = staff.id
            session["staff_name"] = staff.full_name
            flash("Logged in successfully.", "success")
            return redirect(url_for("dashboard"))
        flash("Invalid username or password.", "danger")
    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for("login"))


@app.route("/dashboard")
@login_required
def dashboard():
    total_pets = Pet.query.count()
    available_pets = Pet.query.filter_by(status="Available").count()
    adopted_pets = Pet.query.filter_by(status="Adopted").count()
    total_applications = Application.query.count()
    total_fees = db.session.query(func.coalesce(func.sum(Adoption.fee_paid), 0)).scalar()
    average_fee = db.session.query(func.coalesce(func.avg(Adoption.fee_paid), 0)).scalar()
    recent_applications = Application.query.order_by(Application.id.desc()).limit(5).all()
    recent_adoptions = Adoption.query.order_by(Adoption.id.desc()).limit(5).all()

    return render_template(
        "dashboard.html",
        total_pets=total_pets,
        available_pets=available_pets,
        adopted_pets=adopted_pets,
        total_applications=total_applications,
        total_fees=total_fees,
        average_fee=average_fee,
        recent_applications=recent_applications,
        recent_adoptions=recent_adoptions,
    )


@app.route("/pets")
@login_required
def pets():
    return render_template("pets/list.html", pets=Pet.query.order_by(Pet.name).all())


@app.route("/pets/new", methods=["GET", "POST"])
@login_required
def new_pet():
    if request.method == "POST":
        errors = validate_pet_form(request.form)
        if errors:
            for error in errors:
                flash(error, "danger")
        else:
            pet = Pet(
                name=request.form["name"].strip(),
                species=request.form["species"].strip(),
                breed=request.form["breed"].strip(),
                age=int(request.form["age"]),
                status=request.form["status"],
                adoption_fee=float(request.form["adoption_fee"]),
            )
            db.session.add(pet)
            db.session.commit()
            flash("Pet added successfully.", "success")
            return redirect(url_for("pets"))
    return render_template("pets/form.html", pet=None)


@app.route("/pets/<int:pet_id>/edit", methods=["GET", "POST"])
@login_required
def edit_pet(pet_id):
    pet = Pet.query.get_or_404(pet_id)
    if request.method == "POST":
        errors = validate_pet_form(request.form)
        if errors:
            for error in errors:
                flash(error, "danger")
        else:
            pet.name = request.form["name"].strip()
            pet.species = request.form["species"].strip()
            pet.breed = request.form["breed"].strip()
            pet.age = int(request.form["age"])
            pet.status = request.form["status"]
            pet.adoption_fee = float(request.form["adoption_fee"])
            db.session.commit()
            flash("Pet updated successfully.", "success")
            return redirect(url_for("pets"))
    return render_template("pets/form.html", pet=pet)


@app.route("/pets/<int:pet_id>/delete", methods=["POST"])
@login_required
def delete_pet(pet_id):
    pet = Pet.query.get_or_404(pet_id)
    db.session.delete(pet)
    db.session.commit()
    flash("Pet deleted successfully.", "success")
    return redirect(url_for("pets"))


@app.route("/adopters")
@login_required
def adopters():
    return render_template("adopters/list.html", adopters=Adopter.query.order_by(Adopter.last_name).all())


@app.route("/adopters/new", methods=["GET", "POST"])
@login_required
def new_adopter():
    if request.method == "POST":
        errors = validate_adopter_form(request.form)
        if errors:
            for error in errors:
                flash(error, "danger")
        else:
            adopter = Adopter(
                first_name=request.form["first_name"].strip(),
                last_name=request.form["last_name"].strip(),
                email=request.form["email"].strip(),
                phone=request.form["phone"].strip(),
                address=request.form["address"].strip(),
            )
            db.session.add(adopter)
            db.session.commit()
            flash("Adopter added successfully.", "success")
            return redirect(url_for("adopters"))
    return render_template("adopters/form.html", adopter=None)


@app.route("/adopters/<int:adopter_id>/edit", methods=["GET", "POST"])
@login_required
def edit_adopter(adopter_id):
    adopter = Adopter.query.get_or_404(adopter_id)
    if request.method == "POST":
        errors = validate_adopter_form(request.form)
        if errors:
            for error in errors:
                flash(error, "danger")
        else:
            adopter.first_name = request.form["first_name"].strip()
            adopter.last_name = request.form["last_name"].strip()
            adopter.email = request.form["email"].strip()
            adopter.phone = request.form["phone"].strip()
            adopter.address = request.form["address"].strip()
            db.session.commit()
            flash("Adopter updated successfully.", "success")
            return redirect(url_for("adopters"))
    return render_template("adopters/form.html", adopter=adopter)


@app.route("/adopters/<int:adopter_id>/delete", methods=["POST"])
@login_required
def delete_adopter(adopter_id):
    adopter = Adopter.query.get_or_404(adopter_id)
    db.session.delete(adopter)
    db.session.commit()
    flash("Adopter deleted successfully.", "success")
    return redirect(url_for("adopters"))


@app.route("/applications")
@login_required
def applications():
    all_applications = Application.query.order_by(Application.id.desc()).all()
    return render_template("applications/list.html", applications=all_applications)


@app.route("/applications/new", methods=["GET", "POST"])
@login_required
def new_application():
    if request.method == "POST":
        errors = validate_application_form(request.form)
        if errors:
            for error in errors:
                flash(error, "danger")
        else:
            application = Application(
                pet_id=int(request.form["pet_id"]),
                adopter_id=int(request.form["adopter_id"]),
                status=request.form["status"],
                notes=request.form["notes"].strip(),
            )
            db.session.add(application)
            db.session.commit()
            flash("Application added successfully.", "success")
            return redirect(url_for("applications"))

    pets = Pet.query.order_by(Pet.name).all()
    adopters = Adopter.query.order_by(Adopter.last_name).all()
    return render_template("applications/form.html", application=None, pets=pets, adopters=adopters)


@app.route("/applications/<int:application_id>/edit", methods=["GET", "POST"])
@login_required
def edit_application(application_id):
    application = Application.query.get_or_404(application_id)
    if request.method == "POST":
        errors = validate_application_form(request.form)
        if errors:
            for error in errors:
                flash(error, "danger")
        else:
            application.pet_id = int(request.form["pet_id"])
            application.adopter_id = int(request.form["adopter_id"])
            application.status = request.form["status"]
            application.notes = request.form["notes"].strip()
            db.session.commit()
            flash("Application updated successfully.", "success")
            return redirect(url_for("applications"))

    pets = Pet.query.order_by(Pet.name).all()
    adopters = Adopter.query.order_by(Adopter.last_name).all()
    return render_template("applications/form.html", application=application, pets=pets, adopters=adopters)


@app.route("/applications/<int:application_id>/delete", methods=["POST"])
@login_required
def delete_application(application_id):
    application = Application.query.get_or_404(application_id)
    db.session.delete(application)
    db.session.commit()
    flash("Application deleted successfully.", "success")
    return redirect(url_for("applications"))


@app.route("/applications/<int:application_id>/finalize", methods=["POST"])
@login_required
def finalize_adoption(application_id):
    application = Application.query.get_or_404(application_id)

    if application.adoption:
        flash("This application already has a finalized adoption.", "warning")
        return redirect(url_for("applications"))
    if application.pet.status == "Adopted":
        flash("This pet is already marked as adopted.", "danger")
        return redirect(url_for("applications"))

    try:
        adoption = Adoption(
            pet_id=application.pet_id,
            adopter_id=application.adopter_id,
            application_id=application.id,
            fee_paid=application.pet.adoption_fee,
        )
        db.session.add(adoption)
        application.pet.status = "Adopted"
        application.status = "Approved"
        db.session.commit()
        flash("Adoption finalized successfully.", "success")
    except Exception:
        db.session.rollback()
        flash("Adoption transaction failed and was rolled back.", "danger")

    return redirect(url_for("applications"))


@app.route("/adoptions")
@login_required
def adoptions():
    return render_template("adoptions/list.html", adoptions=Adoption.query.order_by(Adoption.id.desc()).all())


@app.route("/relationships")
@login_required
def relationships():
    return render_template(
        "relationships.html",
        pets=Pet.query.order_by(Pet.name).all(),
        adopters=Adopter.query.order_by(Adopter.last_name).all(),
        applications=Application.query.order_by(Application.id.desc()).all(),
        adoptions=Adoption.query.order_by(Adoption.id.desc()).all(),
    )


def seed_data():
    if Staff.query.count() == 0:
        db.session.add(Staff(username="admin", password="admin123", full_name="Admin Staff"))

    if Pet.query.count() == 0:
        db.session.add_all(
            [
                Pet(name="Luna", species="Cat", breed="Domestic Shorthair", age=2, status="Available", adoption_fee=75),
                Pet(name="Milo", species="Dog", breed="Beagle Mix", age=4, status="Available", adoption_fee=125),
                Pet(name="Nova", species="Rabbit", breed="Mini Rex", age=1, status="Available", adoption_fee=50),
            ]
        )

    if Adopter.query.count() == 0:
        db.session.add_all(
            [
                Adopter(
                    first_name="Jordan",
                    last_name="Lee",
                    email="jordan@example.com",
                    phone="555-0101",
                    address="120 Bluebird Lane",
                ),
                Adopter(
                    first_name="Taylor",
                    last_name="Morgan",
                    email="taylor@example.com",
                    phone="555-0102",
                    address="48 Slate Street",
                ),
            ]
        )
    db.session.commit()

    if Application.query.count() == 0:
        luna = Pet.query.filter_by(name="Luna").first()
        jordan = Adopter.query.filter_by(email="jordan@example.com").first()
        if luna and jordan:
            db.session.add(Application(pet_id=luna.id, adopter_id=jordan.id, status="Pending", notes="Good match."))
            db.session.commit()


with app.app_context():
    db.create_all()
    seed_data()


if __name__ == "__main__":
    app.run(debug=True)
