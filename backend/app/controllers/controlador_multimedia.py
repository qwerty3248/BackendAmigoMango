from flask import Blueprint, request, jsonify
from app.extensiones import db
from app.models.multimedia import Multimedia
import re

multimedia_bp = Blueprint('multimedia', __name__)

def limpiar_texto(texto):
    if not isinstance(texto, str):
        return texto
    texto = re.sub(r"[^\w\s\-\.\/]", "", texto) 
    texto = re.sub(r"\s+", " ", texto).strip()
    return texto


def listar_multimedia():
    try:
        archivos = Multimedia.query.all()

        resultado = [
            {
                "id_multimedia": a.id_multimedia,
                "tipo": a.tipo,
                "nombre": a.nombre,
                "ruta": a.ruta
            }
            for a in archivos
        ]

        return jsonify(resultado), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


def get_multimedia(id_multimedia):
    try:
        archivo = Multimedia.query.get(id_multimedia)
        if not archivo:
            return jsonify({"error": "Multimedia no encontrado"}), 404

        return jsonify({
            "id_multimedia": archivo.id_multimedia,
            "tipo": archivo.tipo,
            "nombre": archivo.nombre,
            "ruta": archivo.ruta
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


def crear_multimedia():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "JSON inválido"}), 400

        campos_obligatorios = ["ruta"]
        for campo in campos_obligatorios:
            if campo not in data:
                return jsonify({"error": f"Falta el campo obligatorio: {campo}"}), 400

        nuevo = Multimedia(
            tipo=limpiar_texto(data.get("tipo")),
            nombre=limpiar_texto(data.get("nombre")),
            ruta=limpiar_texto(data.get("ruta"))
        )

        db.session.add(nuevo)
        db.session.commit()

        return jsonify({
            "mensaje": "Archivo multimedia creado con éxito",
            "multimedia": {
                "id_multimedia": nuevo.id_multimedia,
                "tipo": nuevo.tipo,
                "nombre": nuevo.nombre,
                "ruta": nuevo.ruta
            }
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


def actualizar_multimedia(id_multimedia):
    try:
        archivo = Multimedia.query.get(id_multimedia)
        if not archivo:
            return jsonify({"error": "Multimedia no encontrado"}), 404

        data = request.get_json()
        if not data:
            return jsonify({"error": "JSON inválido"}), 400

        campos = ["tipo", "nombre", "ruta"]
        for campo in campos:
            if campo in data:
                setattr(archivo, campo, limpiar_texto(data[campo]))

        db.session.commit()

        return jsonify({
            "mensaje": "Multimedia actualizado correctamente",
            "multimedia": {
                "id_multimedia": archivo.id_multimedia,
                "tipo": archivo.tipo,
                "nombre": archivo.nombre,
                "ruta": archivo.ruta
            }
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


def eliminar_multimedia(id_multimedia):
    try:
        archivo = Multimedia.query.get(id_multimedia)
        if not archivo:
            return jsonify({"error": "Multimedia no encontrado"}), 404

        db.session.delete(archivo)
        db.session.commit()

        return jsonify({"mensaje": "Multimedia eliminado correctamente"}), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
