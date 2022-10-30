import requests
import unittest


class TestAPI(unittest.TestCase):

    BASE = "http://127.0.0.1:5000/"
    BOOKINGS = BASE + "bookings"

    booking_1021 = {
        "booking_id": "1021",
        "name": "Miles Davis",
        "date": "01-11-2022",
        "time": "10",
    }

    new_booking = {
        "booking_id": "1022",
        "name": "Joe Pass",
        "date": "15-11-2022",
        "time": "13",
    }

    update_booking = {"date": "30-11-2022", "time": "12"}
    update_booking_original = {"date": "01-11-2022", "time": "10"}

    updated_booking_1021 = {
        "booking_id": "1021",
        "name": "Miles Davis",
        "date": "30-11-2022",
        "time": "12",
    }

    wrong_booking_time = {"date": "30-11-2022", "time": "19"}

    updated_booking_1012 = {
        "booking_id": "1012",
        "name": "Dizzy Gillespie",
        "date": "29-06-2022",
        "time": "12",
    }

    booking_wrong_date = {
        "booking_id": "1018",
        "name": "Oscar Peterson",
        "date": "2022-08-07",
        "time": "11",
    }

    def test_1_get_all_bookings(self):
        resp = requests.get(self.BOOKINGS)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.json()), 1)
        print("Test 1 completed")

    def test_2_get_booking_1021(self):
        resp = requests.get(self.BOOKINGS + "/1021")
        self.assertEqual(resp.status_code, 200)
        self.assertDictEqual(resp.json(), self.booking_1021)
        print("Test 2 completed")

    def test_3_post_booking(self):
        resp = requests.post(self.BOOKINGS, json=self.new_booking)
        self.assertEqual(resp.status_code, 201)
        print("Test 3 completed")

    def test_4_delete_booking(self):
        resp = requests.delete(self.BOOKINGS + "/1022")
        self.assertEqual(resp.status_code, 204)
        print("Test 4 completed")

    def test_5_update_booking(self):
        resp = requests.put(self.BOOKINGS + "/1021", json=self.update_booking)
        self.assertDictEqual(resp.json(), self.updated_booking_1021)
        print("Test 5 completed")

    def test_6_wrong_booking_id(self):
        resp = requests.get(self.BOOKINGS + "/1090")
        self.assertEqual(resp.status_code, 404)
        self.assertEqual(resp.json(), "Booking ID does not exist")
        print("Test 6 completed")

    def test_7_update_wrong_booking_time(self):
        resp = requests.put(self.BOOKINGS + "/1021", json=self.wrong_booking_time)
        self.assertEqual(resp.status_code, 404)
        self.assertEqual(
            resp.json(),
            "Time selected is not within opening times, please enter an integer from 9 to 17",
        )
        print("Test 7 completed")

    def test_8_post_wrong_date_format(self):
        resp = requests.post(self.BOOKINGS, json=self.booking_wrong_date)
        self.assertEqual(resp.status_code, 404)
        self.assertEqual(
            resp.json(), "Wrong date format, must be in the form dd-mm-yyyy"
        )
        print("Test 8 completed")
    
    def test_9_update_booking_back(self):
        resp = requests.put(self.BOOKINGS + "/1021", json=self.update_booking_original)
        self.assertDictEqual(resp.json(), self.booking_1021)
        print("Test 9 completed")


if __name__ == "__main__":
    tester = TestAPI()

    tester.test_1_get_all_bookings()
    tester.test_2_get_booking_1021()
    tester.test_3_post_booking()
    tester.test_4_delete_booking()
    tester.test_5_update_booking()
    tester.test_6_wrong_booking_id()
    tester.test_7_update_wrong_booking_time()
    tester.test_8_post_wrong_date_format()
    tester.test_9_update_booking_back()
