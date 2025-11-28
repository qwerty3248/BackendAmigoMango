from app.models.estudiante import Estudiante
from app.extensiones import db, bcrypt
from app.models.configAccesibilidad import ConfigAccesibilidad
from app.models.estudianteAula import EstudianteAula
from app.models.aula import Aula
from app.models.configJuego import ConfigJuego
from flask import jsonify, request   
import re

from app.models.multimedia import Multimedia

def limpiar_texto(texto):
    if not isinstance(texto, str):
        return texto
    # Elimina caracteres no alfanuméricos excepto espacios, guiones y guiones bajos
    texto = re.sub(r"[^\w\s\-]", "", texto)
    # Elimina espacios extra
    texto = re.sub(r"\s+", " ", texto).strip()
    return texto

def registrar_estudiante():
    data = request.get_json()
    
    campos = ['nombre', 'usuario', 'genero', 'contrasena']
    for campo in campos:
        if campo not in data:
            return jsonify({"error": f"Falta el campo {campo}"}), 400
        
    nuevo_estudiante = Estudiante(
        nombre = limpiar_texto(data.get('nombre')),
        contrasena = limpiar_texto(data.get('contrasena')),
        usuario = limpiar_texto(data.get('usuario')),
        genero = limpiar_texto(data.get('genero')),
    )

    db.session.add(nuevo_estudiante)
    db.session.flush()

    # Crear configuración de accesibilidad por defecto
    nuevo_estudiante.config_accesibilidad = ConfigAccesibilidad(
        id_estudiante=nuevo_estudiante.id_estudiante,
        tamaño_letra=12,
        tipo_letra="Arial",
        color_letra="#000000",
        color_fondo="#FFFFFF",
        color_contraste=False,
        representacion_numerica="numero",
        modo_acceso="pantalla_táctil",
        modo_discapacidad="otro"
    )

    # Crear configuración juegos por defecto
    for id_juego in range(0, 4): 
        config_juego = ConfigJuego(
            id_juego=id_juego,
            id_estudiante=nuevo_estudiante.id_estudiante,
            num_contenedores=2,
            color_contenedores="#000000",
            contiene_suma=True,
            contiene_resta=False,
            contiene_comparacion=False,
            formato_numeros="digito",
            rango_maximo=10
        )
        db.session.add(config_juego)

    db.session.commit()

    return jsonify({
        "message": "Estudiante registrado con éxito",
        "datos_enviados": {
            "nombre": nuevo_estudiante.nombre,
            "usuario": nuevo_estudiante.usuario,
            "genero": nuevo_estudiante.genero,
            "config_accesibilidad": {
                "tamano_letra": nuevo_estudiante.config_accesibilidad.tamaño_letra,
                "tipo_letra": nuevo_estudiante.config_accesibilidad.tipo_letra,
                "color_letra": nuevo_estudiante.config_accesibilidad.color_letra,
                "color_fondo": nuevo_estudiante.config_accesibilidad.color_fondo,
                "color_contraste": nuevo_estudiante.config_accesibilidad.color_contraste,
                "representacion_numerica": nuevo_estudiante.config_accesibilidad.representacion_numerica,
                "modo_acceso": nuevo_estudiante.config_accesibilidad.modo_acceso,
                "modo_discapacidad": nuevo_estudiante.config_accesibilidad.modo_discapacidad
            }
        }
    }), 201

def iniciar_sesion_perfil_alumno():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Se requiere JSON válido"}), 400

        id_estudiante = data.get('id_estudiante')
        if not id_estudiante:
            return jsonify({"error": "Se requiere el id del estudiante"}), 400

        estudiante = Estudiante.query.filter_by(id=id_estudiante).first()
        if not estudiante:
            return jsonify({"error": "Estudiante no encontrado"}), 404

        return jsonify({
            "mensaje": "Estudiante encontrado",
            "estudiante": {
                "id": estudiante.id_estudiante,
                "nombre": estudiante.nombre,
                "usuario": estudiante.usuario,
                "sexo": estudiante.sexo,
                "fecha_nacimiento": str(estudiante.fecha_nacimiento),
                "correo": estudiante.correo,
                "telefono": estudiante.telefono
            }
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

def editar_perfil_estudiante():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Se requiere JSON válido"}), 400

        id_estudiante = data.get("id_estudiante")
        if not id_estudiante:
            return jsonify({"error": "Se requiere el id del estudiante"}), 400

        estudiante = Estudiante.query.get(id_estudiante)
        if not estudiante:
            return jsonify({"error": "Estudiante no encontrado"}), 404

        campos_actualizables = ["nombre", "sexo", "correo", "telefono", "fecha_nacimiento"]
        for campo in campos_actualizables:
            if campo in data:
                setattr(estudiante, campo, data[campo])

        config = data.get("config_accesibilidad")
        if config:
            if not estudiante.config_accesibilidad:
                # Crear configuración si no existe
                estudiante.config_accesibilidad = ConfigAccesibilidad(id_estudiante=estudiante.id_estudiante)

            campos_config = [
                "tamano_letra", "tipo_letra", "color_letra", "color_fondo",
                "color_contraste", "representacion_numerica", "modo_acceso", "modo_discapacidad"
            ]
            for campo in campos_config:
                if campo in config:
                    setattr(estudiante.config_accesibilidad, campo, config[campo])

        db.session.commit()

        return jsonify({
            "mensaje": "Perfil actualizado correctamente",
            "estudiante": {
                "id_estudiante": estudiante.id_estudiante,
                "nombre": estudiante.nombre,
                "sexo": estudiante.sexo,
                "correo": estudiante.correo,
                "telefono": estudiante.telefono,
                "fecha_nacimiento": str(estudiante.fecha_nacimiento) if estudiante.fecha_nacimiento else None,
                "config_accesibilidad": {
                    "tamano_letra": estudiante.config_accesibilidad.tamano_letra,
                    "tipo_letra": estudiante.config_accesibilidad.tipo_letra,
                    "color_letra": estudiante.config_accesibilidad.color_letra,
                    "color_fondo": estudiante.config_accesibilidad.color_fondo,
                    "color_contraste": estudiante.config_accesibilidad.color_contraste,
                    "representacion_numerica": estudiante.config_accesibilidad.representacion_numerica,
                    "modo_acceso": estudiante.config_accesibilidad.modo_acceso,
                    "modo_discapacidad": estudiante.config_accesibilidad.modo_discapacidad
                } if estudiante.config_accesibilidad else {}
            }
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


def editar_datos_estudiante():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Se requiere JSON válido"}), 400

        id_estudiante = data.get("id_estudiante")
        if not id_estudiante:
            return jsonify({"error": "Se requiere el id del estudiante"}), 400

        estudiante = Estudiante.query.get(id_estudiante)
        if not estudiante:
            return jsonify({"error": "Estudiante no encontrado"}), 404

        campos_actualizables = ["nombre"]
        for campo in campos_actualizables:
            if campo in data:
                setattr(estudiante, campo, data[campo])

        db.session.commit()

        return jsonify({
            "mensaje": "Datos del estudiante actualizados correctamente",
            "estudiante": {
                "id_estudiante": estudiante.id_estudiante,
                "nombre": estudiante.nombre,
            }
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

def editar_config_estudiante():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Se requiere JSON válido"}), 400

        id_estudiante = data.get("id_estudiante")
        if not id_estudiante:
            return jsonify({"error": "Se requiere el id del estudiante"}), 400

        estudiante = Estudiante.query.get(id_estudiante)
        if not estudiante:
            return jsonify({"error": "Estudiante no encontrado"}), 404

        config_data = data.get("config_accesibilidad")
        if not config_data:
            return jsonify({"error": "Se requiere el objeto 'config_accesibilidad'"}), 400

        # Crear config si no existía
        if not estudiante.config_accesibilidad:
            estudiante.config_accesibilidad = ConfigAccesibilidad(
                id_estudiante=estudiante.id_estudiante
            )

        campos_config = [
            "tamaño_letra", "tipo_letra", "color_letra", "color_fondo",
            "color_contraste", "representacion_numerica",
            "modo_acceso", "modo_discapacidad"
        ]

        for campo in campos_config:
            if campo in config_data:
                setattr(estudiante.config_accesibilidad, campo, config_data[campo])

        db.session.commit()

        config = estudiante.config_accesibilidad

        return jsonify({
            "mensaje": "Configuración de accesibilidad actualizada correctamente",
            "config_accesibilidad": {
                "tamano_letra": config.tamaño_letra,
                "tipo_letra": config.tipo_letra,
                "color_letra": config.color_letra,
                "color_fondo": config.color_fondo,
                "color_contraste": config.color_contraste,
                "representacion_numerica": config.representacion_numerica,
                "modo_acceso": config.modo_acceso,
                "modo_discapacidad": config.modo_discapacidad,
            }
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

def listar_alumnos_por_aula():
    try:
        resultados = (
            db.session.query(
                Aula.nombre,
                Aula.id_aula,
                Estudiante.nombre,
                Estudiante.id_estudiante,
                Multimedia.ruta
            )
            .outerjoin(EstudianteAula, Aula.id_aula == EstudianteAula.id_aula)
            .outerjoin(Estudiante, Estudiante.id_estudiante == EstudianteAula.id_estudiante)
            .outerjoin(Multimedia, Aula.id_multimedia == Multimedia.id_multimedia)
            .order_by(Aula.nombre, Estudiante.nombre)
            .all()
        )

        aulas_dict = {}

        for nombre_aula, id_aula, nombre_estudiante, id_estudiante, ruta_icono in resultados:
            if id_aula not in aulas_dict:
                aulas_dict[id_aula] = {
                    "nombre": nombre_aula,
                    "alumnos": [],
                    "icono": ruta_icono if ruta_icono else "flor"
                }

            if nombre_estudiante:
                aulas_dict[id_aula]["alumnos"].append({
                    "id_estudiante": id_estudiante,
                    "nombre": nombre_estudiante
                })

        return jsonify(aulas_dict), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

def listar_todos_alumnos():
    try:
        nombre_aula = request.args.get('aula')
        
        if nombre_aula:
            aula = Aula.query.filter_by(nombre=nombre_aula).first()
            if not aula:
                return jsonify({"error": "Aula no encontrada"}), 404
            
            subquery = db.session.query(EstudianteAula.id_estudiante).filter_by(id_aula=aula.id_aula)
            estudiantes = Estudiante.query.filter(Estudiante.id_estudiante.notin_(subquery)).all()
        else:
            estudiantes = Estudiante.query.all()

        lista_estudiantes = []
        for estudiante in estudiantes:
            lista_estudiantes.append({
                "id_estudiante": estudiante.id_estudiante,
                "nombre": estudiante.nombre,
                "usuario": estudiante.usuario,
                "genero": estudiante.genero,
                "fecha_nacimiento": str(estudiante.fecha_nacimiento) if estudiante.fecha_nacimiento else None,
                "correo": estudiante.correo,
                "telefono": estudiante.telefono
            })
        return jsonify(lista_estudiantes), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def obtener_alumnos_de_aula(id_aula):
    try:
        resultados = (
            db.session.query(
                Estudiante.id_estudiante,
                Estudiante.nombre,
            )
            .join(EstudianteAula, Estudiante.id_estudiante == EstudianteAula.id_estudiante)
            .filter(EstudianteAula.id_aula == id_aula)
            .order_by(Estudiante.nombre)
            .all()
        )

        alumnos = []
        for id_estudiante, nombre in resultados:
            alumnos.append({
                "id": id_estudiante,
                "nombre": nombre,
            })

        return jsonify(alumnos), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

def obtener_alumno(id_estudiante):
    
    try:
        estudiante = Estudiante.query.get(id_estudiante)
        if not estudiante:
            return None

        return {
            "id_estudiante": estudiante.id_estudiante,
            "nombre": estudiante.nombre,
            "contrasena": estudiante.contrasena,
        }
    except Exception as e:
        return None

def obtener_config_alumno(id_estudiante):
    try:
        estudiante = Estudiante.query.get(id_estudiante)
        if not estudiante or not estudiante.config_accesibilidad:
            return None
        config = estudiante.config_accesibilidad
        return {
            "tamano_letra": getattr(config, "tamaño_letra"),
            "tipo_letra": config.tipo_letra,
            "color_letra": config.color_letra,
            "color_fondo": config.color_fondo,
            "color_contraste": config.color_contraste,
            "representacion_numerica": config.representacion_numerica,
            "modo_acceso": config.modo_acceso,
            "modo_discapacidad": config.modo_discapacidad,
        }
    except Exception as e:
        return None
def anadir_contrasena_estudiante():
    try:
        data = request.get_json() or {}
        id_estudiante = data.get("id_estudiante")
        contrasena = data.get("contrasena")
        estudiante = Estudiante.query.get(id_estudiante)
        if not estudiante:
            return None

        estudiante.contrasena = contrasena
        db.session.commit()
        return {
            "id_estudiante": estudiante.id_estudiante,
            "nombre": estudiante.nombre,
            "contrasena": estudiante.contrasena,
        }
    except Exception as e:
        return None