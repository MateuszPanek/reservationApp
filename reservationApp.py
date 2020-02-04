from reservationAppConfig import *
from reservationAppModels import TrainSchema, Train, Ticket, TicketSchema
from reservationControllers import buy_ticket
from flask import request, redirect

@app.route('/relations')
def relations():
    return Train.get_all_as_json()

@app.route('/ticket/<ticket_id>')
def ticket(ticket_id):
    ticket = Ticket.query.filter_by(id=ticket_id).one_or_none()
    ticket_schema = TicketSchema()
    return ticket_schema.dump(ticket)

@app.route('/buy/<train_id>', methods=["POST"])
def buy(train_id):
    if request.json is None:
        return {"message": f"Invalid request type."}, 400
    app.logger.info(f"buy/{train_id} called with data: {request.json}")

    if "number_of_tickets" not in request.json:
        return {"message": f"Missing number of tickets."}, 400

    # Odwołujemy się do funkcji buy_ticket z reservationControllers, przekazując jej wartość pod kluczem
    # number_of tickets (wydobywając ją z przetworzonego w json obiektu response)
    buy_ticket_info = buy_ticket(train_id, request.json["number_of_tickets"])

    # Przekierowujemy klienta na adres podany w zwrotce przez bank (otrzymany w reservationControllers.buy_ticket)
    return redirect(buy_ticket_info)

@app.route('/paid/<int:ticket_id>', methods=["POST"])
def mark_as_paid(ticket_id):
    # Tutaj trafi zwrotka z banku z potwierdzeniem opłacenia biletu. Funkcja mark_as_paid zrobi update biletu w bazie dancyh
    # i przestawi wartość paid jako True
    status = Ticket.query.filter_by(id=ticket_id).first()
    status.paid = True
    app.logger.info(f'payment_id:{status.id}  paid :{status.paid}')
    db.session.commit()
    return "OK"


if __name__ == "__main__":
    app.run(port=5001, debug=True)
