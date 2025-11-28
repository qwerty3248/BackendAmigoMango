from app.extensiones import db

class Multimedia(db.Model):
    __tablename__ = "multimedia"

    id_multimedia = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tipo = db.Column(db.String(20), nullable=True)
    nombre = db.Column(db.String(40), nullable=True)
    ruta = db.Column(db.Text, nullable=False)
