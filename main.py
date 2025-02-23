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
    """
    _summary_: Visualizza tutte le prenotazioni disponibili

    Returns:
        List[Booking]: Una lista di tutte le prenotazioni esistenti
    """
    return bookings




@app.get("/api/bookings/{booking_id}", response_model=Booking)
def get_booking(booking_id: int):
    """
    _summary_: Ottiene una prenotazione specifica in base all'ID

    Args:
        booking_id (int):  L'ID della prenotazione richiesta

    Raises:
        HTTPException: Se la prenotazione non viene trovata restituisce un errore 404

    Returns:
        Booking: L'oggetto prenotazione corrispondente all'ID specificato
    """
    for booking in bookings:
        if booking.id == booking_id:
            return booking
    raise HTTPException(status_code=404, detail="Prenotazione non trovata")




@app.post("/api/bookings", response_model=Booking)
def create_booking(booking: Booking):
    """_summary_: Crea una nuova prenotazione

    Args:
        booking (Booking): I dettagli della prenotazione da creare

    Raises:
        HTTPException: Se l'orario è già occupato restituisce un errore 400

    Returns:
        Booking: L'oggetto prenotazione appena creato
    """
    for existing_booking in bookings:
        if existing_booking.date == booking.date and existing_booking.time == booking.time:
            raise HTTPException(status_code=400, detail="Orario già occupato")

    bookings.append(booking)
    return booking




@app.put("/api/bookings/{booking_id}", response_model=Booking)
def update_booking(booking_id: int, updated_booking: Booking):
    """_summary_: Aggiorna una prenotazione esistente

    Args:
        booking_id (int): L'ID della prenotazione da aggiornare
        updated_booking (Booking): I nuovi dettagli della prenotazione

    Raises:
        HTTPException: Se l'orario è già occupato da un'altra prenotazione restituisce un errore 400
        HTTPException: Se la prenotazione non viene trovata restituisce un errore 404

    Returns:
         Booking: L'oggetto prenotazione aggiornato
    """
    for booking in bookings:
        if booking.id == booking_id:
            for existing_booking in bookings:
                if (
                    existing_booking.id != booking_id
                    and existing_booking.date == updated_booking.date
                    and existing_booking.time == updated_booking.time
                ):
                    raise HTTPException(status_code=400, detail="Orario già occupato")

            booking.date = updated_booking.date
            booking.time = updated_booking.time
            booking.guests = updated_booking.guests
            return booking

    raise HTTPException(status_code=404, detail="Prenotazione non trovata")
    




@app.delete("/api/bookings/{booking_id}")
def delete_booking(booking_id: int):
    """_summary_: Elimina una prenotazione esistente

    Args:
        booking_id (int): L'ID della prenotazione da eliminare

    Raises:
        HTTPException: Se la prenotazione non viene trovata restituisce un errore 404.

    Returns:
        dict: Messaggio di conferma dell'eliminazione
    """
    for booking in bookings:
        if booking.id == booking_id:
            bookings.remove(booking)
            return {"message": f"Prenotazione numero: {booking_id} eliminata con successo"}

    raise HTTPException(status_code=404, detail="Prenotazione non trovata")
