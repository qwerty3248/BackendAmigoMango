from app.extensiones import db

class ConfigAccesibilidad(db.Model):
    __tablename__ = "config_accesibilidad"
    id_estudiante = db.Column(db.Integer, db.ForeignKey('estudiante.id_estudiante', ondelete='CASCADE'), primary_key=True)
    tamaño_letra = db.Column(db.SmallInteger, default=16)
    tipo_letra = db.Column(db.String(50), default='Arial')
    color_letra = db.Column(db.String(7), default='#000000')
    color_fondo = db.Column(db.String(7), default='#FFFFFF')
    color_contraste = db.Column(db.String(7), default='#FFFF00')
    representacion_numerica = db.Column(db.String(20), default='numero')
    modo_acceso = db.Column(db.String(20), default='pantalla_táctil')
    modo_discapacidad = db.Column(db.String(20), default='otro')
