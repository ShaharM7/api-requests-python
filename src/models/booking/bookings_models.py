from datetime import date
from pydantic import BaseModel
from faker import Faker
from faker_food import FoodProvider

class BookingsRequest(BaseModel):
    """Optional query parameters for GET /booking"""
    firstname: str | None = None
    lastname: str | None = None
    checkin: date | None = None
    checkout: date | None = None

class BookingsResponse(BaseModel):
    """Single booking ID from GET /booking response"""
    bookingid: int

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
    
def generate_booking_data() -> BookingModel: 
    """Returns fake booking data"""
    fake = Faker()
    fake.add_provider(FoodProvider) # for fun ;)
    return BookingModel(firstname=fake.first_name(), 
            lastname=fake.last_name(),
            totalprice=fake.random_number(),
            depositpaid=fake.boolean(),
            bookingdates=BookingDates(checkin=fake.date_object(), checkout=fake.date_object()),
            additionalneeds=f"I want to eat for Breakfast {fake.dish()}")
