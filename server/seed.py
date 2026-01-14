from config import app, db
from models import User, Role, House, Review, Booking
from faker import Faker
import random
from datetime import datetime, timedelta

fake = Faker()

with app.app_context():

    print("🧹 Clearing database...")
    Booking.query.delete()
    Review.query.delete()
    House.query.delete()
    User.query.delete()
    Role.query.delete()
    db.session.commit()

    # --------------------
    # ROLES
    # --------------------
    print("👥 Creating roles...")
    admin_role = Role(name="Admin")
    user_role = Role(name="User")
    db.session.add_all([admin_role, user_role])
    db.session.commit()

    # --------------------
    # USERS
    # --------------------
    print("🙋 Creating users...")
    users = []

    admin = User(
        username="admin",
        email="admin@glamjam.com",
        role=admin_role
    )
    admin.password_hash = "admin123"
    users.append(admin)

    for _ in range(5):
        user = User(
            username=fake.user_name(),
            email=fake.unique.email(),
            role=user_role
        )
        user.password_hash = "password123"
        users.append(user)

    db.session.add_all(users)
    db.session.commit()

    # --------------------
    # HOUSES
    # --------------------
    print("🏠 Creating houses...")
    house_types = ["Villa", "Apartment", "Cottage", "Beach House"]

    houses = []
    for _ in range(8):
        house = House(
            location=f"{fake.city()}, Kenya",
            price_per_night=random.randint(80, 400),
            house_type=random.choice(house_types),
            image_url="https://source.unsplash.com/800x600/?house",
            description=fake.paragraph(nb_sentences=3),
            average_rating=round(random.uniform(3.5, 5.0), 1)
        )
        houses.append(house)

    db.session.add_all(houses)
    db.session.commit()

    # --------------------
    # BOOKINGS
    # --------------------
    print("📅 Creating bookings...")
    bookings = []

    for _ in range(10):
        start_date = fake.date_time_between(start_date="-30d", end_date="+10d")
        end_date = start_date + timedelta(days=random.randint(1, 7))

        booking = Booking(
            user=random.choice(users),
            house=random.choice(houses),
            status=random.choice(["Pending", "Approved", "Denied"]),
            start_date=start_date,
            end_date=end_date
        )
        bookings.append(booking)

    db.session.add_all(bookings)
    db.session.commit()

    # --------------------
    # REVIEWS
    # --------------------
    print("⭐ Creating reviews...")
    reviews = []

    for _ in range(12):
        review = Review(
            user=random.choice(users),
            house=random.choice(houses),
            rating=random.randint(1, 5),
            comment=fake.sentence(nb_words=12)
        )
        reviews.append(review)

    db.session.add_all(reviews)
    db.session.commit()

    print("✅ Database seeded successfully 🚀")
