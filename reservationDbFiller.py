from reservationAppConfig import *
from reservationAppModels import Train, Ticket
from datetime import datetime

with app.app_context():
    db.create_all() #Tworzy się baza danych - na podstawie wszystkich modeli
    for table in reversed(db.metadata.sorted_tables):
        db.session.execute(table.delete())  ####Kasowanie poprzednich rekordów z bazy dancyh
    db.session.commit()

    trains = [
        ("Krakow", "Gdynia", datetime(2020, 2, 10, 12, 0), 200),
        ("Bydgoszcz", "Warszawa", datetime(2020, 2, 10, 14, 25), 100),
        ("Warszawa", "Olsztyn", datetime(2020, 2, 10, 13, 15), 120),
        ("Szczecin", "Lublin", datetime(2020, 2, 10, 11, 27), 400),
        ("Gdynia", 'Lębork', datetime(2020, 2, 3, 14, 50), 120)
    ]
    for train in trains:
        db.session.add(Train(source=train[0], destination=train[1], date=train[2], price=train[3]))
        db.session.commit()

    db.session.add(Ticket(paid=False, train_id=1, seats=1))
    db.session.add(Ticket(paid=True, train_id=2, seats=2))

    sosnowiec_walbrzych = Train(source='Sosnowiec', destination='Walbrzych', date=datetime(2020, 2, 10, 11, 27), price=5)
    sonowiec_walbrzych_ticket = Ticket(paid=True, train=sosnowiec_walbrzych)
    db.session.add(sonowiec_walbrzych_ticket)
    db.session.commit()

    print(Train.query.all())
    print(Ticket.query.all())