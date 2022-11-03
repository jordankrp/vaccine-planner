import requests
import random
import sys
from blessed import Terminal
from PyInquirer import prompt

options_menu = [
    "Request new booking",
    "Display existing booking",
    "Modify existing booking",
    "Delete booking",
]

term = Terminal()


def print_start_screen():
    print(term.home + term.clear)

    print(term.center(term.bold(("Welcome to the COVID-19 vaccination scheduler!"))))

    print("\n\n")

    input_prompt = prompt(
        {
            "name": "action",
            "type": "list",
            "message": "Choose an action to continue",
            "required": True,
            "choices": options_menu,
        }
    )
    print("\n")
    return input_prompt


def get_booking_id():
    print()
    print(term.underline("Please type in the booking ID"))
    answer = prompt({"type": "input", "name": "booking_id", "message": "Booking ID:"})
    return str(answer["booking_id"])


def get_name():
    print()
    print(term.underline("Please type in your Name and Surname"))
    answer = prompt({"type": "input", "name": "name", "message": "Name and Surname:"})
    return str(answer["name"])


def get_email():
    print()
    print(term.underline("Please type in your email address"))
    answer = prompt({"type": "input", "name": "email", "message": "Email address:"})
    return str(answer["email"])


def get_date():
    print()
    print(term.underline("Please type in the booking date"))
    answer = prompt({"type": "input", "name": "date", "message": "Booking date:"})
    return str(answer["date"])


def get_time():
    print()
    print(term.underline("Please type in the booking time"))
    answer = prompt({"type": "input", "name": "time", "message": "Booking time:"})
    return str(answer["time"])


def get_bookings():
    get_req = requests.get("http://localhost:5000/bookings")
    if get_req.status_code == 200:
        bookings = get_req.json()
        return bookings
    else:
        return get_req.text


def generate_booking_id(bookings):
    existing_ids = []
    for booking in bookings:
        existing_ids.append(booking["booking_id"])
    booking_id = random.choice([i for i in range(0, 9999) if i not in existing_ids])
    return booking_id


def name_auth(bookings, booking_id, name):
    auth = False
    for booking in bookings:
        if booking["booking_id"] == booking_id:
            if booking["name"] == name:
                auth = True
    return auth


def date_modify_zeros(date):
    day = date.split("-")[0]
    month = date.split("-")[1]
    year = date.split("-")[2]
    if len(day) == 1:
        day = "0" + day
    if len(month) == 1:
        month = "0" + month
    return "-".join([day, month, year])


def booking_clash(bookings, date, time):
    clash = False
    for booking in bookings:
        # TODO Need to account for 01-11 and 1-11
        date = date_modify_zeros(date)
        if booking["date"] == date:
            if booking["time"] == time:
                print("Selected time is already taken on this date")
                clash = True
    return clash


def display_booking(booking_id):
    get_req = requests.get(f"http://localhost:5000/bookings/{booking_id}")
    if get_req.status_code == 200:
        booking = get_req.json()
        print(f"Name: {booking['name']}")
        print(f"Booking ID: {booking['booking_id']}")
        print(f"Date: {booking['date']}")
        print(f"Time: {booking['time']}")
        print("\n")
    else:
        print(get_req.text)


def add_new_booking(booking_id, name, email, date, time):
    query = {
        "booking_id": str(booking_id),
        "name": str(name),
        "email": str(email),
        "date": str(date),
        "time": str(time),
    }
    post_req = requests.post("http://localhost:5000/bookings", json=query)
    if post_req.status_code == 201:
        print()
        print("New booking added successfully")
        display_booking(booking_id)
    else:
        print(post_req.text)


def update_booking(booking_id, date, time):
    query = {"date": date, "time": time}
    put_req = requests.put(f"http://localhost:5000/bookings/{booking_id}", json=query)
    if put_req.status_code == 200:
        print()
        print(f"Booking with ID {booking_id} updated successfully")
        display_booking(booking_id)
    else:
        print(put_req.text)


def delete_booking(booking_id):
    delete_req = requests.delete(f"http://localhost:5000/bookings/{booking_id}")
    if delete_req.status_code == 204:
        print()
        print(f"Booking with ID {booking_id} deleted successfully")
    else:
        print(delete_req.text)


def request_new_booking(bookings):
    name = get_name()
    email = get_email()
    date = get_date()
    time = get_time()
    # Check if there is a date / time clash
    if booking_clash(bookings, date, time):
        sys.exit()
    # generate booking ID
    booking_id = generate_booking_id(bookings)
    add_new_booking(booking_id, name, email, date, time)
    # TODO Send email confirmation to user (using Flask mail or similar)


def view_booking_details(bookings):
    booking_id = get_booking_id()
    name = get_name()
    if name_auth(bookings, booking_id, name):
        display_booking(booking_id)
    else:
        print("Name does not match with booking ID")


def modify_booking(bookings):
    booking_id = get_booking_id()
    name = get_name()
    new_date = get_date()
    new_time = get_time()
    # Check if there is a date / time clash
    if booking_clash(bookings, new_date, new_time):
        sys.exit()
    if name_auth(bookings, booking_id, name):
        update_booking(booking_id, new_date, new_time)
    else:
        print("Name does not match with booking ID")


def remove_booking(bookings):
    booking_id = get_booking_id()
    name = get_name()
    if name_auth(bookings, booking_id, name):
        delete_booking(booking_id)
    else:
        print("Name does not match with booking ID")


if __name__ == "__main__":

    input_prompt = None
    bookings = get_bookings()
    while not input_prompt:
        input_prompt = print_start_screen()
    if input_prompt["action"] == options_menu[0]:
        # Request new booking
        request_new_booking(bookings)
    elif input_prompt["action"] == options_menu[1]:
        # View existing booking details
        view_booking_details(bookings)
    elif input_prompt["action"] == options_menu[2]:
        # Modify existing booking
        modify_booking(bookings)
    elif input_prompt["action"] == options_menu[3]:
        # Delete existing booking
        remove_booking(bookings)
