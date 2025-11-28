from app.extensiones import db
from flask import jsonify, request
from app.models.partida import Partida
from app.models.configJuego import ConfigJuego
from app.models.repeticion import Repeticion
from app.models.juego import Juego
from datetime import timedelta

def finalizar_partida():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Se requiere JSON válido"}), 400

    id_partida = data.get('id_partida')
    if id_partida is None:
        return jsonify({"error": "Se requiere id_partida"}), 400

    partida = Partida.query.get(id_partida)
    
    if not partida:
        return jsonify({"error": "Partida no encontrada"}), 404

    if partida.en_progreso is False:
        return jsonify({"message": "La partida ya está finalizada", "id_partida": partida.id_partida}), 200

    partida.en_progreso = False
    db.session.commit()

    return jsonify({
            "message": "Partida finalizada correctamente",
            "id_partida": partida.id_partida,
            "id_juego": partida.id_juego,
            "id_estudiante": partida.id_estudiante
        }), 200

def traer_configuracion(id_juego, id_estudiante):

    if id_juego is None or id_estudiante is None:
        return jsonify({"error": "Se requieren id_juego e id_estudiante"}), 400

    config = ConfigJuego.query.filter_by(
        id_juego=id_juego,
        id_estudiante=id_estudiante
    ).first()

    if not config:
        return jsonify({"error": "Configuración no encontrada"}), 404

    return jsonify({
        "num_contenedores": config.num_contenedores,
        "color_contenedores": config.color_contenedores,
        "contiene_suma": config.contiene_suma,
        "contiene_resta": config.contiene_resta,
        "contiene_comparacion": config.contiene_comparacion,
        "formato_numeros": config.formato_numeros,
        "rango_maximo": config.rango_maximo
    }), 200

def anadir_repeticion():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Se requiere JSON válido"}), 400
    
    tiempo = data.get('tiempo')
    tiempo_delta = timedelta(seconds=tiempo)
    
    nueva_repeticion = Repeticion(
        id_partida=data.get('id_partida'),
        num_repeticion=data.get('num_repeticion'),
        aciertos=data.get('aciertos', 0),
        fallos=data.get('fallos', 0),
        tiempo=tiempo_delta
    )

    db.session.add(nueva_repeticion)
    db.session.commit()

    return jsonify({
        "message": "Repetición añadida con éxito",
        "id_repeticion": nueva_repeticion.id_repeticion
    }), 201

def crear_iniciar_partida():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Se requiere JSON válido"}), 400

    id_juego = data.get('id_juego')
    id_estudiante = data.get('id_estudiante')
    dificultad = data.get('dificultad')

    if id_juego is None or id_estudiante is None or dificultad is None:
        return jsonify({"error": "Se requieren id_juego, id_estudiante y dificultad"}), 400

    partida_en_curso = Partida.query.filter_by(
        id_juego=id_juego,
        id_estudiante=id_estudiante,
        en_progreso=True
    ).first()

    if partida_en_curso:
        ultima_rep = Repeticion.query.filter_by(id_partida=partida_en_curso.id_partida).order_by(Repeticion.num_repeticion.desc()).first()

        ultima_ronda = ultima_rep.num_repeticion if ultima_rep else 0

        return jsonify({
            "message": "Partida en curso encontrada",
            "id_partida": partida_en_curso.id_partida,
            "es_nueva": False,
            "ultima_ronda": ultima_ronda
        }), 200

    nueva_partida = Partida(
        id_juego=id_juego,
        id_estudiante=id_estudiante,
        dificultad=dificultad,
        en_progreso=True
    )

    db.session.add(nueva_partida)
    db.session.commit()

    return jsonify({
        "message": "Nueva partida creada correctamente",
        "id_partida": nueva_partida.id_partida,
        "es_nueva": True
    }), 201

def get_juegos():
    try:
        juegos = Juego.query.all()
        
        if not juegos:
            return jsonify({"message": "No se encontraron juegos disponibles"}), 404

        juegos_list = []
        for juego in juegos:
            juegos_list.append({
                "id_juego": juego.id_juego,
                "nombre": juego.nombre,
                "descripcion": juego.descripcion
            })
        
        return jsonify(juegos_list), 200
        
    except Exception as e:
        return jsonify({"error": f"Error interno del servidor al obtener los juegos: {str(e)}"}), 500