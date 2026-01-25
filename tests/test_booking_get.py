"""
Tests for GET /booking and GET /booking/:id endpoints
"""
from datetime import date, timedelta

import pytest
from requests.exceptions import HTTPError

from src.clients.facades.booking_client import BookingClient
from src.models.booking.bookings_models import (
    BookingDates,
    BookingModel,
    BookingRequest,
    BookingResponse,
    generate_fake_booking_model,
)
from src.models.http_response import HttpResponse


# ============================================
# GET /booking - Get all booking IDs
# ============================================

def test_get_all_booking_ids_success(initialize_booking_client: BookingClient):
    """Test that GET /booking returns a successful response"""
    # Act - Need to add get_all_booking_ids() method to BookingClient
    booking_ids: list[int] = initialize_booking_client.get_all_booking_ids()
    
    # Assert
    assert booking_ids is not None
    assert isinstance(booking_ids, list)


def test_get_all_booking_ids_not_empty(initialize_booking_client: BookingClient):
    """Test that GET /booking returns a non-empty list"""
    # Arrange - Create a booking first to ensure list is not empty
    fake_booking: BookingModel = generate_fake_booking_model()
    initialize_booking_client.create_booking(booking_model=fake_booking)
    
    # Act
    booking_ids: list[int] = initialize_booking_client.get_all_booking_ids()
    
    # Assert
    assert len(booking_ids) > 0, "Booking list should not be empty"


def test_get_all_booking_ids_valid_structure(initialize_booking_client: BookingClient):
    """Test that each item in GET /booking response has valid structure"""
    # Act
    booking_ids: list[int] = initialize_booking_client.get_all_booking_ids()
    
    # Assert - Each ID should be a positive integer
    for booking_id in booking_ids:
        assert isinstance(booking_id, int), f"Booking ID should be int, got {type(booking_id)}"
        assert booking_id > 0, f"Booking ID should be positive, got {booking_id}"


# ============================================
# GET /booking/:id - Get booking by ID
# ============================================

def test_get_booking_by_id_success(initialize_booking_client: BookingClient):
    """Test that GET /booking/:id returns a successful response"""
    # Arrange - Create a booking first
    fake_booking: BookingModel = generate_fake_booking_model()
    booking_response: BookingResponse = initialize_booking_client.create_booking(
        booking_model=fake_booking
    )
    booking_id = booking_response.bookingid
    
    # Act
    retrieved_booking: BookingModel = initialize_booking_client.get_booking(booking_id=booking_id)
    
    # Assert
    assert retrieved_booking is not None
    assert isinstance(retrieved_booking, BookingModel)


def test_get_booking_by_id_valid_structure(initialize_booking_client: BookingClient):
    """Test that GET /booking/:id returns all required fields"""
    # Arrange - Create a booking first
    fake_booking: BookingModel = generate_fake_booking_model()
    booking_response: BookingResponse = initialize_booking_client.create_booking(
        booking_model=fake_booking
    )
    booking_id = booking_response.bookingid
    
    # Act
    retrieved_booking: BookingModel = initialize_booking_client.get_booking(booking_id=booking_id)
    
    # Assert - All required fields are present and have correct types
    assert hasattr(retrieved_booking, 'firstname')
    assert hasattr(retrieved_booking, 'lastname')
    assert hasattr(retrieved_booking, 'totalprice')
    assert hasattr(retrieved_booking, 'depositpaid')
    assert hasattr(retrieved_booking, 'bookingdates')
    assert hasattr(retrieved_booking, 'additionalneeds')
    
    assert isinstance(retrieved_booking.firstname, str)
    assert isinstance(retrieved_booking.lastname, str)
    assert isinstance(retrieved_booking.totalprice, int)
    assert isinstance(retrieved_booking.depositpaid, bool)
    assert isinstance(retrieved_booking.bookingdates, BookingDates)


def test_get_booking_by_id_returns_correct_data(initialize_booking_client: BookingClient):
    """Test that GET /booking/:id returns the correct booking data"""
    # Arrange - Create a booking first
    fake_booking: BookingModel = generate_fake_booking_model()
    booking_response: BookingResponse = initialize_booking_client.create_booking(
        booking_model=fake_booking
    )
    booking_id = booking_response.bookingid
    
    # Act
    retrieved_booking: BookingModel = initialize_booking_client.get_booking(booking_id=booking_id)
    
    # Assert - Data matches what was created
    assert retrieved_booking.firstname == fake_booking.firstname
    assert retrieved_booking.lastname == fake_booking.lastname
    assert retrieved_booking.totalprice == fake_booking.totalprice
    assert retrieved_booking.depositpaid == fake_booking.depositpaid
    assert retrieved_booking.additionalneeds == fake_booking.additionalneeds
    assert retrieved_booking.bookingdates.checkin == fake_booking.bookingdates.checkin
    assert retrieved_booking.bookingdates.checkout == fake_booking.bookingdates.checkout


def test_get_booking_invalid_id(initialize_booking_client: BookingClient):
    """Test that GET /booking/:id returns 404 for non-existent booking"""
    # Arrange - Use an ID that doesn't exist
    invalid_booking_id = 99999999
    
    # Act & Assert - Should raise HTTPError for 404
    with pytest.raises(HTTPError) as exc_info:
        initialize_booking_client.get_booking(booking_id=invalid_booking_id)
    
    # Verify it's a 404 error
    assert exc_info.value.response.status_code == 404


def test_get_booking_invalid_id_raw(initialize_booking_client: BookingClient):
    """Test that GET /booking/:id returns 404 for non-existent booking (raw check)"""
    # Arrange - Use an ID that doesn't exist
    invalid_booking_id = 99999999
    
    # Act - Use raw client to check status code directly
    http_response: HttpResponse = initialize_booking_client.client.get(
        endpoint=f"{initialize_booking_client.booking_endpoint}/{invalid_booking_id}"
    )
    
    # Assert
    assert http_response.status_code == 404, \
        f"Expected 404 but got {http_response.status_code}. Response: {http_response.text}"


# ============================================
# GET /booking with filters
# ============================================

def test_get_booking_ids_filter_by_firstname(initialize_booking_client: BookingClient):
    """Test filtering bookings by firstname"""
    # Arrange - Create a booking with specific firstname
    checkin = date.today()
    checkout = checkin + timedelta(days=2)
    
    unique_firstname = "UniqueFirstName123"
    booking = BookingModel(
        firstname=unique_firstname,
        lastname="TestLastName",
        totalprice=100,
        depositpaid=True,
        bookingdates=BookingDates(checkin=checkin, checkout=checkout),
        additionalneeds=""
    )
    
    booking_response: BookingResponse = initialize_booking_client.create_booking(booking_model=booking)
    created_booking_id = booking_response.bookingid
    
    filters = BookingRequest(firstname=unique_firstname)
    filtered_ids: list[int] = initialize_booking_client.get_booking_ids_by_filter(filters=filters)
    
    # Assert
    assert created_booking_id in filtered_ids, \
        f"Created booking ID {created_booking_id} should be in filtered results"


def test_get_booking_ids_filter_by_lastname(initialize_booking_client: BookingClient):
    """Test filtering bookings by lastname"""
    # Arrange - Create a booking with specific lastname
    checkin = date.today()
    checkout = checkin + timedelta(days=2)
    
    unique_lastname = "UniqueLastName456"
    booking = BookingModel(
        firstname="TestFirstName",
        lastname=unique_lastname,
        totalprice=200,
        depositpaid=False,
        bookingdates=BookingDates(checkin=checkin, checkout=checkout),
        additionalneeds=""
    )
    
    booking_response: BookingResponse = initialize_booking_client.create_booking(booking_model=booking)
    created_booking_id = booking_response.bookingid
    
    # Act - Filter by lastname
    filters = BookingRequest(lastname=unique_lastname)
    filtered_ids: list[int] = initialize_booking_client.get_booking_ids_by_filter(filters=filters)
    
    # Assert
    assert created_booking_id in filtered_ids, \
        f"Created booking ID {created_booking_id} should be in filtered results"


def test_get_booking_ids_filter_by_dates(initialize_booking_client: BookingClient):
    """Test filtering bookings by checkin/checkout dates"""
    # Arrange - Create a booking with specific dates
    checkin = date.today() + timedelta(days=100)  # Use future date to make it unique
    checkout = checkin + timedelta(days=5)
    
    booking = BookingModel(
        firstname="DateFilter",
        lastname="Test",
        totalprice=300,
        depositpaid=True,
        bookingdates=BookingDates(checkin=checkin, checkout=checkout),
        additionalneeds=""
    )
    
    booking_response: BookingResponse = initialize_booking_client.create_booking(booking_model=booking)
    created_booking_id = booking_response.bookingid
    
    # Act - Filter by checkin date
    filters = BookingRequest(checkin=checkin)
    filtered_ids: list[int] = initialize_booking_client.get_booking_ids_by_filter(filters=filters)
    
    # Assert
    assert created_booking_id in filtered_ids, \
        f"Created booking ID {created_booking_id} should be in filtered results"


def test_get_booking_ids_filter_combination(initialize_booking_client: BookingClient):
    """Test filtering bookings by multiple filters (firstname + lastname)"""
    # Arrange - Create a booking with specific firstname and lastname
    checkin = date.today()
    checkout = checkin + timedelta(days=2)
    
    unique_firstname = "ComboFirst789"
    unique_lastname = "ComboLast789"
    
    booking = BookingModel(
        firstname=unique_firstname,
        lastname=unique_lastname,
        totalprice=400,
        depositpaid=True,
        bookingdates=BookingDates(checkin=checkin, checkout=checkout),
        additionalneeds=""
    )
    
    booking_response: BookingResponse = initialize_booking_client.create_booking(booking_model=booking)
    created_booking_id = booking_response.bookingid
    
    # Act - Filter by both firstname and lastname
    filters = BookingRequest(firstname=unique_firstname, lastname=unique_lastname)
    filtered_ids: list[int] = initialize_booking_client.get_booking_ids_by_filter(filters=filters)
    
    # Assert
    assert created_booking_id in filtered_ids, \
        f"Created booking ID {created_booking_id} should be in filtered results"


def test_get_booking_ids_filter_no_results(initialize_booking_client: BookingClient):
    """Test filtering bookings returns empty list when no matches"""
    # Act - Filter by non-existent name
    filters = BookingRequest(firstname="NonExistentName99999")
    filtered_ids: list[int] = initialize_booking_client.get_booking_ids_by_filter(filters=filters)
    
    # Assert - Should return empty list
    assert filtered_ids == [], f"Expected empty list but got {filtered_ids}"
