
from flask import request, session
from flask_restful import Resource
from config import app, db, api
from models import User, House, Booking, Review, Favorite
from functools import wraps

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user_id = session.get('user_id')
        if not user_id:
            return {"error": "Unauthorized"}, 401

        user = User.query.get(user_id)
        if not user or user.role.name != "Admin":
            return {"error": "Admin access required"}, 403

        return f(*args, **kwargs)
    return decorated_function


class Signup(Resource):
    def post(self):
        data = request.get_json()

        try:
            new_user = User(
                username=data.get('username'),
                email=data.get('email'),
                role_id=2  
            )
            new_user.password_hash = data.get('password')

            db.session.add(new_user)
            db.session.commit()

            session['user_id'] = new_user.id
            return new_user.to_dict(), 201

        except Exception as e:
            return {"errors": [str(e)]}, 422


class Login(Resource):
    def post(self):
        data = request.get_json()
        user = User.query.filter_by(username=data.get('username')).first()

        if user and user.authenticate(data.get('password')):
            session['user_id'] = user.id
            return user.to_dict(), 200

        return {"error": "Invalid username or password"}, 401


class Logout(Resource):
    def delete(self):  
        session['user_id'] = None
        return {}, 204


class CheckSession(Resource):
    def get(self):
        user_id = session.get('user_id')
        if user_id:
            user = User.query.get(user_id)
            return user.to_dict(), 200
        return {"error": "Not logged in"}, 401


class HouseList(Resource):
    def get(self):
        location = request.args.get('location')
        house_type = request.args.get('type')
        min_rating = request.args.get('rating')

        query = House.query

        if location:
            query = query.filter(House.location.ilike(f"%{location}%"))

        if house_type:
            query = query.filter(House.house_type == house_type)

        houses = query.all()

        if min_rating:
            houses = [h for h in houses if (h.average_rating or 0) >= float(min_rating)]  
        return [h.to_dict(rules=('-bookings', '-reviews')) for h in houses], 200

    @admin_required
    def post(self):
        data = request.get_json()

        new_house = House(
            location=data['location'],
            price_per_night=data['price_per_night'],
            house_type=data['house_type'],
            image_url=data['image_url'],
            description=data['description'],
            average_rating=0.0
        )

        db.session.add(new_house)
        db.session.commit()
        return new_house.to_dict(), 201


class HouseByID(Resource):
    def get(self, id):
        house = House.query.get_or_404(id)
        return house.to_dict(), 200
    @admin_required
    def patch(self, id):
        house = House.query.get_or_404(id)
        data = request.get_json()

        for attr, value in data.items():
            setattr(house, attr, value)

        db.session.commit()
        return house.to_dict(), 200

    @admin_required
    def delete(self, id):
        house = House.query.get_or_404(id)
        db.session.delete(house)
        db.session.commit()
        return {}, 204



class BookingList(Resource):
    def post(self):
        user_id = session.get('user_id')
        if not user_id:
            return {"error": "Must be logged in"}, 401

        data = request.get_json()

        booking = Booking(
            user_id=user_id,
            house_id=data['house_id'],
            start_date=data['start_date'],
            end_date=data['end_date'],
            status="Pending"
        )

        db.session.add(booking)
        db.session.commit()
        return booking.to_dict(), 201

    @admin_required
    def get(self):
        bookings = Booking.query.all()
        return [b.to_dict() for b in bookings], 200


class ApproveBooking(Resource):
    @admin_required
    def patch(self, id):
        booking = Booking.query.get_or_404(id)
        booking.status = "Approved"
        db.session.commit()
        return booking.to_dict(), 200


class UserBookings(Resource):
    def get(self):
        user_id = session.get('user_id')
        if not user_id:
            return {"error": "Unauthorized"}, 401

        user = User.query.get(user_id)
        return [b.to_dict() for b in user.bookings], 200



class FavoriteResource(Resource):
    def get(self):
        user_id = session.get('user_id')
        if not user_id:
            return {"error": "Unauthorized"}, 401
        user_favorites = Favorite.query.filter_by(user_id=user_id).all()
        return [f.to_dict() for f in user_favorites], 200

    def post(self):
        user_id = session.get('user_id')
        if not user_id:
            return {"error": "Unauthorized"}, 401

        data = request.get_json()

        existing = Favorite.query.filter_by(
            user_id=user_id,
            house_id=data['house_id']
        ).first()

        if existing:
            db.session.delete(existing)
            db.session.commit()
            return {"message": "Removed from favorites"}, 200

        favorite = Favorite(
            user_id=user_id,
            house_id=data['house_id']
        )

        db.session.add(favorite)
        db.session.commit()
        return favorite.to_dict(), 201



class ReviewResource(Resource):
    def post(self):
        user_id = session.get('user_id')
        if not user_id:
            return {"error": "Unauthorized"}, 401

        data = request.get_json()

        review = Review(
            user_id=user_id,
            house_id=data['house_id'],
            rating=data['rating'],
            comment=data['comment']
        )

        db.session.add(review)
        db.session.commit()
        return review.to_dict(), 201



class UserList(Resource):
    @admin_required
    def get(self):
        users = User.query.all()
        return [u.to_dict() for u in users], 200



api.add_resource(Signup, '/signup')
api.add_resource(Login, '/login')
api.add_resource(Logout, '/logout')
api.add_resource(CheckSession, '/check_session')

api.add_resource(HouseList, '/houses')
api.add_resource(HouseByID, '/houses/<int:id>')

api.add_resource(BookingList, '/bookings')
api.add_resource(ApproveBooking, '/bookings/<int:id>/approve')
api.add_resource(UserBookings, '/my-bookings')

api.add_resource(FavoriteResource, '/favorites')
api.add_resource(ReviewResource, '/reviews')

api.add_resource(UserList, '/users')



if __name__ == '__main__':
    app.run(port=5555, debug=True)
