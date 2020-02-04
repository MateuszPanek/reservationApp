from reservationAppConfig import db, ma
from flask import jsonify


class Train(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    source = db.Column(db.String(80), unique=False, nullable=False)
    destination = db.Column(db.String(80), unique=False, nullable=False)
    date = db.Column(db.DateTime, unique=False, nullable=False)
    price = db.Column(db.Float, unique=False, nullable=False)


    def __repr__(self):
        return f"{self.id}: {self.source}-{self.destination} ({self.date}), {self.price}$"

    @staticmethod
    def get_all_as_json():
        train_schema = TrainSchema(many=True)
        return jsonify(train_schema.dump(Train.query.all()))


class TrainSchema(ma.ModelSchema):
    class Meta:
        model = Train


class Ticket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    paid = db.Column(db.Boolean, unique=False, nullable=False)
    seats = db.Column(db.Integer)
    train_id = db.Column(db.Integer, db.ForeignKey('train.id'),nullable=False)
    train = db.relationship('Train')

    def __repr__(self):
        return f"{self.id}: Train: {self.train_id}, Paid: {self.paid}, Seats={self.seats}"

    @staticmethod
    def get_all_as_json():
        ticket_schema = TicketSchema(many=True)
        return jsonify()


class TicketSchema(ma.ModelSchema):
    class Meta:
        model = Ticket
    train = ma.Nested(TrainSchema)