from app.extensiones import db

class Juego(db.Model):
    __tablename__ = "juego"
    id_juego = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text)
