import requests
import random
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


def add_new_booking(booking_id, name, date, time):
    query = {
        "booking_id": str(booking_id),
        "name": str(name),
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


if __name__ == "__main__":

    input_prompt = None
    while not input_prompt:
        input_prompt = print_start_screen()
    if input_prompt["action"] == options_menu[0]:
        # Request new booking
        name = get_name()
        date = get_date()
        time = get_time()
        # generate booking ID
        bookings = get_bookings()
        booking_id = generate_booking_id(bookings)
        add_new_booking(booking_id, name, date, time)
    elif input_prompt["action"] == options_menu[1]:
        # View existing booking details
        booking_id = get_booking_id()
        # Some sort of name authentication
        display_booking(booking_id)
    elif input_prompt["action"] == options_menu[2]:
        # Modify existing booking
        booking_id = get_booking_id()
        new_date = get_date()
        new_time = get_time()
        update_booking(booking_id, new_date, new_time)
    elif input_prompt["action"] == options_menu[3]:
        # Delete existing booking
        booking_id = get_booking_id()
        delete_booking(booking_id)
