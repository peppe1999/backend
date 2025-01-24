from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from datetime import date

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Booking(BaseModel):
    id: int
    name: str
    date: date
    time: str
    guests: int

bookings: List[Booking] = []

@app.get("/api/bookings", response_model=List[Booking])
def get_bookings():
    return bookings

@app.get("/api/bookings/{booking_id}", response_model=Booking)
def get_booking(booking_id: int):
    for booking in bookings:
        if booking.id == booking_id:
            return booking
    raise HTTPException(status_code=404, detail="Prenotazione non trovata.")

@app.post("/api/bookings", response_model=Booking)
def create_booking(booking: Booking):
    for existing_booking in bookings:
        if existing_booking.date == booking.date and existing_booking.time == booking.time:
            raise HTTPException(status_code=400, detail="Orario già occupato!")

    bookings.append(booking)
    return booking

@app.put("/api/bookings/{booking_id}", response_model=Booking)
def update_booking(booking_id: int, updated_booking: Booking):
    for booking in bookings:
        if booking.id == booking_id:
            for existing_booking in bookings:
                if (
                    existing_booking.id != booking_id
                    and existing_booking.date == updated_booking.date
                    and existing_booking.time == updated_booking.time
                ):
                    raise HTTPException(status_code=400, detail="Orario già occupato!")

            # Aggiorna la prenotazione
            booking.date = updated_booking.date
            booking.time = updated_booking.time
            booking.guests = updated_booking.guests
            return booking

    raise HTTPException(status_code=404, detail="Prenotazione non trovata.")

@app.delete("/api/bookings/{booking_id}")
def delete_booking(booking_id: int):
    """Elimina una prenotazione."""
    for booking in bookings:
        if booking.id == booking_id:
            bookings.remove(booking)
            return {"message": f"Prenotazione con ID {booking_id} eliminata con successo."}

    raise HTTPException(status_code=404, detail="Prenotazione non trovata.")
