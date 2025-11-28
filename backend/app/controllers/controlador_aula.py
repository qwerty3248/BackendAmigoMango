from flask import request, jsonify
from app.models import Aula, Multimedia, EstudianteAula
from app.extensiones import db

def crear_aula():
    try:
        data = request.get_json()
        nombre = data.get("nombre")
        descripcion = data.get("descripcion")
        ruta_multimedia = data.get("ruta_multimedia")

        if not nombre:
            return jsonify({"error": "El nombre del aula es obligatorio"}), 400

        if Aula.query.filter_by(nombre=nombre).first():
            return jsonify({"error": "Ya existe un aula con ese nombre"}), 400

        multimedia = Multimedia(tipo="imagen", nombre=f"Imagen {nombre}", ruta=ruta_multimedia)
        db.session.add(multimedia)
        db.session.commit()  

        aula = Aula(nombre=nombre, descripcion=descripcion, id_multimedia=multimedia.id_multimedia)
        db.session.add(aula)
        db.session.commit()

        return jsonify({"success": True, "id_aula": aula.id_aula})

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

def anadir_estudiante_aula():
    try:
        data = request.get_json()
        nombre_aula = data.get("nombre_aula")
        id_estudiante = data.get("id_estudiante")

        if not nombre_aula or not id_estudiante:
            return jsonify({"error": "Faltan datos"}), 400

        aula = Aula.query.filter_by(nombre=nombre_aula).first()
        if not aula:
            return jsonify({"error": "Aula no encontrada"}), 404

        # Verifica si ya existe la relación
        existe = EstudianteAula.query.filter_by(id_aula=aula.id_aula, id_estudiante=id_estudiante).first()
        if existe:
             return jsonify({"message": "El estudiante ya está en el aula"}), 200

        nueva_relacion = EstudianteAula(id_aula=aula.id_aula, id_estudiante=id_estudiante)
        db.session.add(nueva_relacion)
        db.session.commit()

        return jsonify({"message": "Estudiante añadido correctamente"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
