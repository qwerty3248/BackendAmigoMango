from app.extensiones import db
from .estudianteAula import EstudianteAula
from .aula import Aula
class Estudiante(db.Model):
    __tablename__ = "estudiante"
    id_estudiante = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    usuario = db.Column(db.String(50), unique=True, nullable=False)
    genero = db.Column(db.String(40), nullable=False)  # M, F, O
    contrasena = db.Column(db.String(255), nullable=False)
    fecha_nacimiento = db.Column(db.Date)
    correo = db.Column(db.String(100), unique=True)
    telefono = db.Column(db.String(20))

    aulas = db.relationship('Aula', secondary=EstudianteAula.__table__, primaryjoin=id_estudiante == EstudianteAula.id_estudiante,
        secondaryjoin=Aula.id_aula == EstudianteAula.id_aula, backref='estudiantes')
    config_accesibilidad = db.relationship('ConfigAccesibilidad', uselist=False, backref='estudiante')