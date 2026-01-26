import pytest
from requests import HTTPError

from src.clients.facades.booking_client import BookingClient
from src.models.booking.bookings_models import BookingModel, BookingResponse, generate_fake_booking_model
from src.models.http_response import HttpResponse

@pytest.mark.delete
class TestDeleteBooking:
    """Tests for DELETE /booking/:id"""

    def test_delete_booking_success(self, initialize_booking_client: BookingClient):
        """Test that a booking can be deleted successfully"""
        # Create a booking first
        booking: BookingModel = generate_fake_booking_model()
        create_response: BookingResponse = initialize_booking_client.create_booking(
            booking_model=booking
        )
        booking_id = create_response.bookingid

        # Delete the booking
        delete_response: HttpResponse = initialize_booking_client.delete_booking(
            booking_id=booking_id
        )

        # API returns 201 for successful delete (as per docs)
        assert delete_response.status_code == 201, \
            f"Expected 201 but got {delete_response.status_code}"

    def test_delete_booking_no_longer_exists(self, initialize_booking_client: BookingClient):
        """Test that deleted booking cannot be retrieved"""
        # Create a booking
        booking: BookingModel = generate_fake_booking_model()
        create_response: BookingResponse = initialize_booking_client.create_booking(
            booking_model=booking
        )
        booking_id = create_response.bookingid

        # Delete the booking
        initialize_booking_client.delete_booking(booking_id=booking_id)

        # Try to retrieve - should fail with 404
        with pytest.raises(HTTPError) as exc_info:
            initialize_booking_client.get_booking(booking_id=str(booking_id))

        assert exc_info.value.response.status_code == 404

    def test_delete_nonexistent_booking(self, initialize_booking_client: BookingClient):
        """Test deleting a non-existent booking returns error"""
        non_existent_id = 999999999

        http_response: HttpResponse = initialize_booking_client.delete_booking_raw(
            booking_id=non_existent_id
        )

        assert http_response.status_code in [404, 405], \
            f"Expected 404/405 but got {http_response.status_code}"

    def test_delete_already_deleted_booking(self, initialize_booking_client: BookingClient):
        """Test that deleting an already deleted booking returns error"""
        # Create a booking
        booking: BookingModel = generate_fake_booking_model()
        create_response: BookingResponse = initialize_booking_client.create_booking(
            booking_model=booking
        )
        booking_id = create_response.bookingid

        # Delete the booking first time
        initialize_booking_client.delete_booking(booking_id=booking_id)

        # Try to delete again - should fail
        http_response: HttpResponse = initialize_booking_client.delete_booking_raw(
            booking_id=booking_id
        )

        assert http_response.status_code in [404, 405], \
            f"Expected 404/405 but got {http_response.status_code}"
