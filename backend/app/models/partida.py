from app.extensiones import db

class Partida(db.Model):
    __tablename__ = "partida"
    id_partida = db.Column(db.Integer, primary_key=True)
    id_juego = db.Column(db.Integer, db.ForeignKey('juego.id_juego', ondelete='CASCADE'))
    id_estudiante = db.Column(db.Integer, db.ForeignKey('estudiante.id_estudiante', ondelete='CASCADE'))
    dificultad = db.Column(db.SmallInteger)
    fecha = db.Column(db.DateTime, server_default=db.func.now())
    observaciones = db.Column(db.Text)
    en_progreso = db.Column(db.Boolean, default=True)

    repeticiones = db.relationship('Repeticion', backref='partida', cascade='all, delete-orphan')
