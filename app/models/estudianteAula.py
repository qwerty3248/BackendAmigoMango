from app.extensiones import db

class EstudianteAula(db.Model):
    __tablename__ = "estudiante_aula"
    id_estudiante = db.Column(db.Integer, db.ForeignKey('estudiante.id_estudiante', ondelete='CASCADE'), primary_key=True)
    id_aula = db.Column(db.Integer, db.ForeignKey('aula.id_aula', ondelete='CASCADE'), primary_key=True)

