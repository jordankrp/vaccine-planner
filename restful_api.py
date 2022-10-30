from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from datetime import datetime

app = Flask(__name__)
api = Api(app)

bookings = [
    {"booking_id": "1021", "name": "Miles Davis", "date": "01-11-2022", "time": "10"}
]

parser = reqparse.RequestParser()

opening_times = [str(hour) for hour in range(9, 18)]


class BookingsList(Resource):
    def get(self):
        return bookings

    def post(self):
        # TODO Check for clashes with other users
        parser.add_argument("booking_id", type=str)
        parser.add_argument("name", type=str)
        parser.add_argument("date", type=str)
        parser.add_argument("time", type=str)
        args = parser.parse_args()

        # Check if all arguments have been provided
        if (
            args["booking_id"] is None
            or args["name"] is None
            or args["date"] is None
            or args["time"] is None
        ):
            return "Please provide a booking ID, name, date and time.", 404

        # Check if name or booking ID already exists
        else:
            for booking in bookings:
                if (
                    args["name"] == booking["name"]
                    or args["booking_id"] == booking["booking_id"]
                ):
                    return f"Booking ID or name already exists.", 404

        # Check if date is in correct format (DD-MM-YYYY)
        try:
            datetime.strptime(args["date"], "%d-%m-%Y")
        except ValueError:
            return "Wrong date format, must be in the form dd-mm-yyyy", 404
        else:
            if args["time"] in opening_times:
                # Time given by user is within opening times
                new_booking = {
                    "booking_id": args["booking_id"],
                    "name": args["name"],
                    "date": args["date"],
                    "time": args["time"],
                }
                bookings.append(new_booking)
                return request.get_json(), 201
            else:
                return (
                    "Time selected is not within opening times, please enter an integer from 9 to 17",
                    404,
                )


class Booking(Resource):
    def get(self, booking_id):
        for booking in bookings:
            if booking["booking_id"] == booking_id:
                return booking
        return "Booking ID does not exist", 404

    # Update an existing booking.
    # Restrict date format to dd-mm-yyyy
    def put(self, booking_id):
        parser.add_argument("date", type=str)
        parser.add_argument("time", type=str)
        args = parser.parse_args()
        for booking in bookings:
            if booking["booking_id"] == booking_id:
                # Date and time will be overwritten
                # Check date format
                try:
                    datetime.strptime(args["date"], "%d-%m-%Y")
                except ValueError:
                    return "Wrong date format, must be in the form dd-mm-yyyy", 404
                else:
                    if args["time"] in opening_times:
                        booking["date"] = args["date"]
                        booking["time"] = args["time"]
                        return booking, 200
                    else:
                        return (
                            "Time selected is not within opening times, please enter an integer from 9 to 17",
                            404,
                        )
        return "Booking ID does not exist", 404

    def delete(self, booking_id):
        for booking in bookings:
            if booking["booking_id"] == booking_id:
                bookings.remove(booking)
                return "", 204
        return "Booking ID not found", 404


api.add_resource(BookingsList, "/bookings")
api.add_resource(Booking, "/bookings/<booking_id>")

if __name__ == "__main__":
    app.run(debug=True)
