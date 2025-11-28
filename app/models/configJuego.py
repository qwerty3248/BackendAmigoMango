from app.extensiones import db
class ConfigJuego(db.Model):
    __tablename__ = "config_juego"
    id_juego = db.Column(db.Integer, db.ForeignKey('juego.id_juego', ondelete='CASCADE'), primary_key=True)
    id_estudiante = db.Column(db.Integer, db.ForeignKey('estudiante.id_estudiante', ondelete='CASCADE'), primary_key=True)
    num_contenedores = db.Column(db.SmallInteger, default=3)
    color_contenedores = db.Column(db.String(7), default='#FF0000')
    contiene_suma = db.Column(db.Boolean, default=True)
    contiene_resta = db.Column(db.Boolean, default=True)
    contiene_comparacion = db.Column(db.Boolean, default=False)
    formato_numeros = db.Column(db.String(20), default='digito')
    rango_maximo = db.Column(db.SmallInteger, default=1)
