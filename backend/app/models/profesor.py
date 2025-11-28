from app.extensiones import db
from .profesorAula import ProfesorAula

class Profesor(db.Model):
    __tablename__ = "profesor"
    id_profesor = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    usuario = db.Column(db.String(50), unique=True, nullable=False)
    contrasena = db.Column(db.String(255), nullable=False)
    correo = db.Column(db.String(100), unique=True, nullable=False)
    telefono = db.Column(db.String(20))
    es_admin = db.Column(db.Boolean, default=False)

    aulas = db.relationship('Aula', secondary=ProfesorAula.__table__, primaryjoin='Profesor.id_profesor==ProfesorAula.id_profesor',
        secondaryjoin='Aula.id_aula==ProfesorAula.id_aula', backref='profesores')

