from datetime import date

import pytest

from src.clients.facades.booking_client import BookingClient
from src.models.booking.bookings_models import BookingDates, BookingModel, BookingResponse, generate_fake_booking_model
from src.models.http_response import HttpResponse

@pytest.mark.create
class TestCreateBooking:
    """Tests for CREATE /booking/:id"""

    def test_create_booking_success(self, initialize_booking_client: BookingClient):
        """Test that a booking can be created successfully"""
        fake_booking_model: BookingModel = generate_fake_booking_model()
        booking_response: BookingResponse = initialize_booking_client.create_booking(booking_model=fake_booking_model)

        assert booking_response.bookingid > 0
        assert booking_response.booking.firstname == fake_booking_model.firstname
        assert booking_response.booking.lastname == fake_booking_model.lastname
        assert isinstance(booking_response.booking.bookingdates.checkin, date)

    def test_create_booking_returns_correct_data(self, initialize_booking_client: BookingClient):
        """Test that the created booking matches the request data"""
        fake_booking_model: BookingModel = generate_fake_booking_model()

        booking_response: BookingResponse = initialize_booking_client.create_booking(
            booking_model=fake_booking_model
        )

        # Verify all fields match
        assert booking_response.booking.firstname == fake_booking_model.firstname
        assert booking_response.booking.lastname == fake_booking_model.lastname
        assert booking_response.booking.totalprice == fake_booking_model.totalprice
        assert booking_response.booking.depositpaid == fake_booking_model.depositpaid
        assert booking_response.booking.additionalneeds == fake_booking_model.additionalneeds
        assert booking_response.booking.bookingdates.checkin == fake_booking_model.bookingdates.checkin
        assert booking_response.booking.bookingdates.checkout == fake_booking_model.bookingdates.checkout

    def test_create_booking_generates_unique_id(self, initialize_booking_client: BookingClient):
        """Test that each booking gets a unique ID"""
        fake_booking_1: BookingModel = generate_fake_booking_model()
        fake_booking_2: BookingModel = generate_fake_booking_model()

        response_1: BookingResponse = initialize_booking_client.create_booking(booking_model=fake_booking_1)
        response_2: BookingResponse = initialize_booking_client.create_booking(booking_model=fake_booking_2)

        # IDs should be positive integers
        assert response_1.bookingid > 0
        assert response_2.bookingid > 0

        # IDs should be unique
        assert response_1.bookingid != response_2.bookingid

    def test_create_booking_verify_persisted(self, initialize_booking_client: BookingClient):
        """Test that created booking can be retrieved via GET"""
        fake_booking_model: BookingModel = generate_fake_booking_model()

        # Create booking
        booking_response: BookingResponse = initialize_booking_client.create_booking(
            booking_model=fake_booking_model
        )
        booking_id = str(booking_response.bookingid)

        retrieved_booking: BookingModel = initialize_booking_client.get_booking(booking_id=booking_id)

        # Verify data matches
        assert retrieved_booking.firstname == fake_booking_model.firstname
        assert retrieved_booking.lastname == fake_booking_model.lastname
        assert retrieved_booking.totalprice == fake_booking_model.totalprice

    def test_create_booking_with_additionalneeds(self, initialize_booking_client: BookingClient):
        """Test that booking with additionalneeds is created correctly"""
        fake_booking_model: BookingModel = generate_fake_booking_model()
        # additionalneeds is already set by generate_fake_booking_model()

        booking_response: BookingResponse = initialize_booking_client.create_booking(
            booking_model=fake_booking_model
        )

        assert booking_response.booking.additionalneeds == fake_booking_model.additionalneeds
        assert len(booking_response.booking.additionalneeds) > 0

    def test_create_booking_with_minimum_data(self, initialize_booking_client: BookingClient):
        """Test booking creation with minimum required data"""
        from datetime import timedelta

        checkin = date.today()
        checkout = checkin + timedelta(days=1)

        minimal_booking = BookingModel(
            firstname="John",
            lastname="Doe",
            totalprice=100,
            depositpaid=True,
            bookingdates=BookingDates(checkin=checkin, checkout=checkout),
            additionalneeds=""  # Empty string for optional field
        )

        booking_response: BookingResponse = initialize_booking_client.create_booking(
            booking_model=minimal_booking
        )

        assert booking_response.bookingid > 0
        assert booking_response.booking.firstname == "John"
        assert booking_response.booking.lastname == "Doe"

    def test_create_booking_with_special_characters(self, initialize_booking_client: BookingClient):
        """Test booking creation with special characters in names"""
        from datetime import timedelta

        checkin = date.today()
        checkout = checkin + timedelta(days=1)

        booking_with_special_chars = BookingModel(
            firstname="José-María",
            lastname="O'Connor",
            totalprice=150,
            depositpaid=False,
            bookingdates=BookingDates(checkin=checkin, checkout=checkout),
            additionalneeds="Special request: gluten-free"
        )

        booking_response: BookingResponse = initialize_booking_client.create_booking(
            booking_model=booking_with_special_chars
        )

        assert booking_response.bookingid > 0
        assert booking_response.booking.firstname == "José-María"
        assert booking_response.booking.lastname == "O'Connor"

    def test_create_booking_depositpaid_true(self, initialize_booking_client: BookingClient):
        """Test booking creation with depositpaid=True"""
        from datetime import timedelta

        checkin = date.today()
        checkout = checkin + timedelta(days=2)

        booking = BookingModel(
            firstname="Test",
            lastname="User",
            totalprice=200,
            depositpaid=True,  # Explicitly True
            bookingdates=BookingDates(checkin=checkin, checkout=checkout),
            additionalneeds=""
        )

        booking_response: BookingResponse = initialize_booking_client.create_booking(booking_model=booking)

        assert booking_response.booking.depositpaid is True

    def test_create_booking_depositpaid_false(self, initialize_booking_client: BookingClient):
        """Test booking creation with depositpaid=False"""
        from datetime import timedelta

        checkin = date.today()
        checkout = checkin + timedelta(days=2)

        booking = BookingModel(
            firstname="Test",
            lastname="User",
            totalprice=200,
            depositpaid=False,  # Explicitly False
            bookingdates=BookingDates(checkin=checkin, checkout=checkout),
            additionalneeds=""
        )

        booking_response: BookingResponse = initialize_booking_client.create_booking(booking_model=booking)

        assert booking_response.booking.depositpaid is False

    @pytest.mark.parametrize("price", [0, 1, 100, 999, 10000])
    def test_create_booking_various_prices(self, initialize_booking_client: BookingClient, price: int):
        """Test booking creation with various price values"""
        from datetime import timedelta

        checkin = date.today()
        checkout = checkin + timedelta(days=1)

        booking = BookingModel(
            firstname="Test",
            lastname="Price",
            totalprice=price,
            depositpaid=True,
            bookingdates=BookingDates(checkin=checkin, checkout=checkout),
            additionalneeds=""
        )

        booking_response: BookingResponse = initialize_booking_client.create_booking(booking_model=booking)

        assert booking_response.bookingid > 0
        assert booking_response.booking.totalprice == price

    def test_create_booking_missing_required_field(self, initialize_booking_client: BookingClient):
        from datetime import timedelta

        checkin = date.today()
        checkout = checkin + timedelta(days=1)

        # create valid bookign dict
        valid_booking = BookingModel(
            firstname="Negativ",
            lastname="Case",
            totalprice=100,
            depositpaid=True,
            bookingdates=BookingDates(checkin=checkin, checkout=checkout),
            additionalneeds=""  # Empty string for optional field
        )

        # Remove requierd field
        invalid_dict: dict = valid_booking.model_dump(mode="json")
        del invalid_dict["totalprice"]

        http_response: HttpResponse = initialize_booking_client.create_booking_raw(booking_dict=invalid_dict)

        assert http_response.status_code in [400, 500], \
            f"Expected 400/500 but got {http_response.status_code}. Response: {http_response.text}"
