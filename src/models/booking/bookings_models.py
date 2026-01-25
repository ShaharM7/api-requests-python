from datetime import date
from pydantic import BaseModel
from faker import Faker
from faker_food import FoodProvider

from src.models import booking

class BookingRequest(BaseModel):
    """Optional query parameters for GET /booking"""
    firstname: str | None = None
    lastname: str | None = None
    checkin: date | None = None
    checkout: date | None = None

class BookingDates(BaseModel):
    """Nested dates object"""
    checkin: date
    checkout: date

class BookingModel(BaseModel):
    """Full booking object (for Get /booking/:id, Post /booking etc)"""
    firstname: str
    lastname: str
    totalprice: int
    depositpaid: bool
    bookingdates: BookingDates
    additionalneeds: str

class BookingResponse(BaseModel):
    """Single booking ID from GET /booking response"""
    bookingid: int
    booking: BookingModel # Nested booking object
    

def generate_fake_booking_model() -> BookingModel: 
    """Returns fake booking data"""
    fake = Faker()
    fake.add_provider(FoodProvider) # for fun ;)


    checkin = fake.date_object()

    from datetime import timedelta
    checkout = checkin + timedelta(days=fake.random_int(min=1, max=7))

    booking_model = BookingModel(firstname=fake.first_name(), 
            lastname=fake.last_name(),
            totalprice=fake.random_int(min=100, max=1000),
            depositpaid=fake.boolean(),
            bookingdates=BookingDates(
                checkin=checkin,
                checkout=checkout
            ),
            additionalneeds=f"I want to eat for Breakfast {fake.dish()}")

    return booking_model

    
