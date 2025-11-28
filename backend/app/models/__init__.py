from app.extensiones import db

# Importa los modelos para que Flask los registre correctamente
from .profesor import Profesor
from .aula import Aula
from .estudiante import Estudiante
from .profesorAula import ProfesorAula       
from .estudianteAula import EstudianteAula   
from .configAccesibilidad import ConfigAccesibilidad
from .configJuego import ConfigJuego
from .juego import Juego
from .partida import Partida
from .repeticion import Repeticion
from .multimedia import Multimedia


