from datetime import date, timedelta

import pytest

from src.clients.facades.booking_client import BookingClient
from src.models.booking.bookings_models import BookingDates, BookingModel, BookingResponse, generate_fake_booking_model
from src.models.http_response import HttpResponse

@pytest.mark.update
class TestUpdateBookingPut:
    """Tests for PUT /booking/:id - Full update"""

    def test_update_booking_success(self, initialize_booking_client: BookingClient):
        """Test that a booking can be fully updated"""
        # Create a booking first
        original_booking: BookingModel = generate_fake_booking_model()
        create_response: BookingResponse = initialize_booking_client.create_booking(
            booking_model=original_booking
        )
        booking_id = create_response.bookingid

        # Create updated booking data
        updated_booking: BookingModel = generate_fake_booking_model()

        # Perform update
        result: BookingModel = initialize_booking_client.update_booking(
            booking_id=booking_id,
            booking_model=updated_booking
        )

        # Verify update was successful
        assert result.firstname == updated_booking.firstname
        assert result.lastname == updated_booking.lastname
        assert result.totalprice == updated_booking.totalprice
        assert result.depositpaid == updated_booking.depositpaid

    def test_update_booking_persists(self, initialize_booking_client: BookingClient):
        """Test that updated data persists when retrieved"""
        # Create a booking
        original_booking: BookingModel = generate_fake_booking_model()
        create_response: BookingResponse = initialize_booking_client.create_booking(
            booking_model=original_booking
        )
        booking_id = create_response.bookingid

        # Update with new data
        updated_booking: BookingModel = generate_fake_booking_model()
        initialize_booking_client.update_booking(
            booking_id=booking_id,
            booking_model=updated_booking
        )

        # Retrieve and verify
        retrieved: BookingModel = initialize_booking_client.get_booking(booking_id=str(booking_id))

        assert retrieved.firstname == updated_booking.firstname
        assert retrieved.lastname == updated_booking.lastname
        assert retrieved.totalprice == updated_booking.totalprice

    def test_update_nonexistent_booking(self, initialize_booking_client: BookingClient):
        """Test updating a non-existent booking returns error"""
        fake_booking: BookingModel = generate_fake_booking_model()
        non_existent_id = 999999999

        http_response: HttpResponse = initialize_booking_client.update_booking_raw(
            booking_id=non_existent_id,
            payload=fake_booking.model_dump(mode="json")
        )

        assert http_response.status_code in [404, 405], \
            f"Expected 404/405 but got {http_response.status_code}"

    def test_update_dates_only(self, initialize_booking_client: BookingClient):
        """Test updating only the dates of a booking"""
        # Create booking
        original_booking: BookingModel = generate_fake_booking_model()
        create_response: BookingResponse = initialize_booking_client.create_booking(
            booking_model=original_booking
        )
        booking_id = create_response.bookingid

        # Update with new dates but same other data
        new_checkin = date.today() + timedelta(days=30)
        new_checkout = new_checkin + timedelta(days=5)

        updated_booking = BookingModel(
            firstname=original_booking.firstname,
            lastname=original_booking.lastname,
            totalprice=original_booking.totalprice,
            depositpaid=original_booking.depositpaid,
            bookingdates=BookingDates(checkin=new_checkin, checkout=new_checkout),
            additionalneeds=original_booking.additionalneeds
        )

        result: BookingModel = initialize_booking_client.update_booking(
            booking_id=booking_id,
            booking_model=updated_booking
        )

        assert result.bookingdates.checkin == new_checkin
        assert result.bookingdates.checkout == new_checkout
        assert result.firstname == original_booking.firstname

    def test_update_price_only(self, initialize_booking_client: BookingClient):
        """Test updating only the price of a booking"""
        # Create booking
        original_booking: BookingModel = generate_fake_booking_model()
        create_response: BookingResponse = initialize_booking_client.create_booking(
            booking_model=original_booking
        )
        booking_id = create_response.bookingid

        # Update with new price
        new_price = 9999

        updated_booking = BookingModel(
            firstname=original_booking.firstname,
            lastname=original_booking.lastname,
            totalprice=new_price,
            depositpaid=original_booking.depositpaid,
            bookingdates=original_booking.bookingdates,
            additionalneeds=original_booking.additionalneeds
        )

        result: BookingModel = initialize_booking_client.update_booking(
            booking_id=booking_id,
            booking_model=updated_booking
        )

        assert result.totalprice == new_price
        assert result.firstname == original_booking.firstname


class TestPartialUpdateBookingPatch:
    """Tests for PATCH /booking/:id - Partial update"""

    def test_partial_update_firstname(self, initialize_booking_client: BookingClient):
        """Test partial update of firstname only"""
        # Create booking
        original_booking: BookingModel = generate_fake_booking_model()
        create_response: BookingResponse = initialize_booking_client.create_booking(
            booking_model=original_booking
        )
        booking_id = create_response.bookingid

        # Partial update - only firstname
        new_firstname = "UpdatedFirstName"
        result: BookingModel = initialize_booking_client.partial_update_booking(
            booking_id=booking_id,
            updates={"firstname": new_firstname}
        )

        assert result.firstname == new_firstname
        assert result.lastname == original_booking.lastname  # Unchanged
        assert result.totalprice == original_booking.totalprice  # Unchanged

    def test_partial_update_multiple_fields(self, initialize_booking_client: BookingClient):
        """Test partial update of multiple fields"""
        # Create booking
        original_booking: BookingModel = generate_fake_booking_model()
        create_response: BookingResponse = initialize_booking_client.create_booking(
            booking_model=original_booking
        )
        booking_id = create_response.bookingid

        # Partial update - firstname and totalprice
        updates = {
            "firstname": "NewFirst",
            "lastname": "NewLast",
            "totalprice": 5555
        }

        result: BookingModel = initialize_booking_client.partial_update_booking(
            booking_id=booking_id,
            updates=updates
        )

        assert result.firstname == "NewFirst"
        assert result.lastname == "NewLast"
        assert result.totalprice == 5555
        assert result.depositpaid == original_booking.depositpaid  # Unchanged

    def test_partial_update_nonexistent_booking(self, initialize_booking_client: BookingClient):
        """Test partial update of non-existent booking returns error"""
        non_existent_id = 999999999

        http_response: HttpResponse = initialize_booking_client.partial_update_booking_raw(
            booking_id=non_existent_id,
            payload={"firstname": "Test"}
        )

        assert http_response.status_code in [404, 405], \
            f"Expected 404/405 but got {http_response.status_code}"

    def test_partial_update_depositpaid(self, initialize_booking_client: BookingClient):
        """Test partial update of depositpaid field"""
        # Create booking with depositpaid=False
        checkin = date.today()
        checkout = checkin + timedelta(days=2)

        original_booking = BookingModel(
            firstname="Test",
            lastname="User",
            totalprice=100,
            depositpaid=False,
            bookingdates=BookingDates(checkin=checkin, checkout=checkout),
            additionalneeds=""
        )

        create_response: BookingResponse = initialize_booking_client.create_booking(
            booking_model=original_booking
        )
        booking_id = create_response.bookingid

        # Partial update - change depositpaid to True
        result: BookingModel = initialize_booking_client.partial_update_booking(
            booking_id=booking_id,
            updates={"depositpaid": True}
        )

        assert result.depositpaid is True
        assert result.firstname == original_booking.firstname  # Unchanged
