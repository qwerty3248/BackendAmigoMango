from app.extensiones import db

class Aula(db.Model):
    __tablename__ = "aula"
    id_aula = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text)
    id_multimedia = db.Column(
        db.Integer,
        db.ForeignKey("multimedia.id_multimedia"),
        nullable=True
    )
    multimedia = db.relationship("Multimedia", backref="aulas", lazy=True)
