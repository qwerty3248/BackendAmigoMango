from flask import Blueprint, request, jsonify
from app.controllers.controlador_profesor import registrar_profesor, iniciar_profesor
from app.controllers.controlador_estudiante import registrar_estudiante, iniciar_sesion_perfil_alumno, editar_perfil_estudiante, listar_alumnos_por_aula, listar_todos_alumnos, obtener_alumnos_de_aula, obtener_alumno, anadir_contrasena_estudiante, editar_datos_estudiante, editar_config_estudiante, obtener_config_alumno
from app.controllers.controlador_juegos import anadir_repeticion, finalizar_partida, traer_configuracion , crear_iniciar_partida, get_juegos
from app.controllers.controlador_aula import crear_aula, anadir_estudiante_aula
from app.controllers.controlador_multimedia import listar_multimedia, get_multimedia, crear_multimedia, actualizar_multimedia, eliminar_multimedia

api = Blueprint('api', __name__)

@api.route('/health')
def health():
    return jsonify({"status": "ok"})

@api.route('/estudiante/registro', methods=['POST'])
def registrar_estudiante_route():
    return registrar_estudiante()

@api.route('/estudiante/inicio_sesion', methods=['POST'])
def iniciar_sesion_perfil_alumno_route():
    return iniciar_sesion_perfil_alumno()

@api.route('/estudiante/editar_perfil', methods=['POST'])
def editar_perfil_estudiante_route():
    return editar_perfil_estudiante()

@api.route("/aulas/alumnos", methods=["GET"])
def listar_alumnos_por_aula_route():
    return listar_alumnos_por_aula()

@api.route("/estudiantes", methods=["GET"])
def listar_todos_alumnos_route():
    return listar_todos_alumnos()

@api.route("/aulas/anadir_estudiante", methods=["POST"])
def anadir_estudiante_aula_route():
    return anadir_estudiante_aula()

@api.route("/profesores/registro", methods=["POST"])
def registrar_profesor_route():
    return registrar_profesor()

@api.route("/profesores/inicio_sesion", methods=["POST"])
def login():
    return iniciar_profesor()

@api.route('/juegos', methods=['GET'])
def get_juegos_route():
    return get_juegos()

@api.route('/juegos/finalizar', methods=['POST'])
def finalizar_partida_route():
    return finalizar_partida()

@api.route('/juegos/configuracion/<int:id_juego>/<int:id_estudiante>', methods=['GET'])
def traer_configuracion_route(id_juego, id_estudiante):
    return traer_configuracion(id_juego, id_estudiante)

@api.route('/juegos/anadir_repeticion', methods=['POST'])
def anadir_repeticion_route():
    return anadir_repeticion()

@api.route('/juegos/iniciar_partida', methods=['POST'])
def crear_iniciar_partida_route():
    return crear_iniciar_partida()

@api.route("/aulas", methods=["POST"])
def crear_aula_route():
    return crear_aula()
    
@api.route("/aulas/alumnos/<int:id_aula>", methods=["GET"])
def obtener_alumnos_de_aula_route(id_aula):
    return obtener_alumnos_de_aula(id_aula)
    
@api.route("/estudiante/<int:id_estudiante>", methods=["GET"])
def obtener_alumno_route(id_estudiante):
    return obtener_alumno(id_estudiante)

@api.route("/estudiante/config/<int:id_estudiante>", methods=["GET"])
def obtener_config_alumno_route(id_estudiante):
    return obtener_config_alumno(id_estudiante)

@api.route("/estudiante/anadir_contrasena", methods=["POST"])
def anadir_contrasena_estudiante_route():
    return anadir_contrasena_estudiante()

@api.route("/estudiante/editar_datos", methods=["POST"])
def editar_datos_estudiante_route():
    return editar_datos_estudiante()

@api.route("/estudiante/editar_config", methods=["POST"])
def editar_config_estudiante_route():
    return editar_config_estudiante()

@api.route("/multimedia", methods=["GET"])
def listar_multimedia_route():
    return listar_multimedia()

@api.route("/multimedia/<int:id_multimedia>", methods=["GET"])
def obtener_multimedia_route(id_multimedia):
    return get_multimedia(id_multimedia)

@api.route("/multimedia", methods=["POST"])
def crear_multimedia_route():
    return crear_multimedia()

@api.route("/multimedia/<int:id_multimedia>", methods=["PUT"])
def actualizar_multimedia_route(id_multimedia):
    return actualizar_multimedia(id_multimedia)

@api.route("/multimedia/<int:id_multimedia>", methods=["DELETE"])
def eliminar_multimedia_route(id_multimedia):
    return eliminar_multimedia(id_multimedia)
