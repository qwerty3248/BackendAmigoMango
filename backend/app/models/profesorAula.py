from app.extensiones import db

class ProfesorAula(db.Model):
    __tablename__ = "profesor_aula"
    id_profesor = db.Column(db.Integer, db.ForeignKey('profesor.id_profesor', ondelete='CASCADE'), primary_key=True)
    id_aula = db.Column(db.Integer, db.ForeignKey('aula.id_aula', ondelete='CASCADE'), primary_key=True)
