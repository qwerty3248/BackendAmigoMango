from app.models.profesor import Profesor
from app.extensiones import db, bcrypt
from flask import jsonify, request

def registrar_profesor():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Se requiere JSON válido"}), 400

        nombre = data.get('nombre')
        usuario = data.get('usuario')
        contrasena = data.get('contrasena')
        correo = data.get('correo')
        telefono = data.get('telefono')
        es_admin = data.get('es_admin', False)

        if not nombre or not usuario or not contrasena or not correo:
            return jsonify({"error": "Faltan datos obligatorios"}), 400

        if Profesor.query.filter((Profesor.usuario == usuario) | (Profesor.correo == correo)).first():
            return jsonify({"error": "El usuario o correo ya existe"}), 409

        contrasena_hash = bcrypt.generate_password_hash(contrasena).decode('utf-8')

        nuevo_profesor = Profesor(
            nombre=nombre,
            usuario=usuario,
            contrasena=contrasena_hash,
            correo=correo,
            telefono=telefono,
            es_admin=es_admin
        )

        db.session.add(nuevo_profesor)
        db.session.commit()

        return jsonify({"mensaje": "Profesor registrado correctamente"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

def iniciar_profesor():
    data = request.get_json()
    usuario = data.get('usuario')
    contrasena = data.get('contrasena')

    if not usuario or not contrasena:
        return jsonify({"error":"Usuario y contraseña requeridos"}), 400
    
    profesor = Profesor.query.filter_by(usuario=usuario).first()

    if not profesor or not bcrypt.check_password_hash(profesor.contrasena, contrasena):
        return jsonify({"Error": "Usuario o contraseña incorrectos"}), 401
   
    return jsonify({
        "mensaje": "Inicio de sesion exitoso",
        "profesor": {
            "id": profesor.id_profesor,
            "nombre": profesor.nombre,
            "usuario": profesor.usuario,
            "correo": profesor.correo,
            "es_admin": profesor.es_admin
        }
    }), 200