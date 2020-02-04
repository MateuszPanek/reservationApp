from reservationAppModels import Train, Ticket
from reservationAppConfig import db
import requests
BANK_URL = "http://127.0.0.1:5001"

def buy_ticket(train_id, number_of_tickets):
    train = Train.query.filter_by(id=train_id).first()
    if train is None:
        raise ValueError(f"Train {train_id} not found.")

    # W tym momencie w bazie danych PKP tworzony jest bilet ze statusem płatnośći = nieopłacony (False)
    ticket = Ticket(train_id=train_id, paid=False, seats=number_of_tickets)
    db.session.add(ticket)
    db.session.commit()

    amount = number_of_tickets * train.price
    # Request body - przygotowuje słownik który zostanie przekazany do banku i zapisany w jego bazie danych
    # Callbacki zostaną potem zwrócone - paid_callback trafi do pkp, z informacją o opłaceniu biletu
    # Client callback będzie użyty do przekierowania klienta na stronę do pobrania biletu
    request_body = {'amount': amount,
                    'client_callback': f'http://127.0.0.1:5001/ticket/{ticket.id}',
                    'paid_callback': f'http://127.0.0.1:5001/paid/{ticket.id}'}

    # request.post wysyła pod podany url request z metodą post - w którym przekazuje słownik powyżej w formacie json
    # Podstawienie requesta pod zmienną służy zapisaniu pod nią odpowiedz którą zwróci bank (Patrz bankApp endopoint /pay)
    a = requests.post(url='http://127.0.0.1:5002/pay', json=request_body)
    # Zwrócona od banku odpowiedź (obiekt Response) zostaje przekształcona w jsona i za pomocą klucza odpakowujemy z niej link
    # Na który należy przekierować klienta (w celu dokonania płatności) - PATRZ reservationAPP/buy/<int:trainid>
    link = a.json()['redirect_to']
    return link
