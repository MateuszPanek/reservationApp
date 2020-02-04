from reservationAppModels import Train, Ticket
from reservationAppConfig import db
import requests
BANK_URL = "http://127.0.0.1:5001"

def buy_ticket(train_id, number_of_tickets):
    train = Train.query.filter_by(id=train_id).first()
    if train is None:
        raise ValueError(f"Train {train_id} not found.")

    ticket = Ticket(train_id=train_id, paid=False, seats=number_of_tickets)
    db.session.add(ticket)
    db.session.commit()

    amount = number_of_tickets * train.price
    request_body = {'amount': amount,
                    'client_callback': f'http://127.0.0.1:5001/ticket/{ticket.id}',
                    'paid_callback': f'http://127.0.0.1:5001/paid/{ticket.id}'}

    payment_start = requests.post(url='http://127.0.0.1:5002/pay', json=request_body)
    link = payment_start.json()['redirect_to']
    return link
