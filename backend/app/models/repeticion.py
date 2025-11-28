from app.extensiones import db

class Repeticion(db.Model):
    __tablename__ = "repeticion"
    id_repeticion = db.Column(db.Integer, primary_key=True)
    id_partida = db.Column(db.Integer, db.ForeignKey('partida.id_partida', ondelete='CASCADE'))
    num_repeticion = db.Column(db.SmallInteger)
    aciertos = db.Column(db.Integer, default=0)
    fallos = db.Column(db.Integer, default=0)
    tiempo = db.Column(db.Interval)