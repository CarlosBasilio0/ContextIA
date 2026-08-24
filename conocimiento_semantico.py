# =========================================================
# BASE DE CONOCIMIENTO SEMÁNTICO - CONTEXTIA
# =========================================================

CONOCIMIENTO_SEMANTICO = {

    # =====================================================
    # ÁMBITO ACADÉMICO
    # =====================================================

    "profesor": {
        "concepto": "persona que enseña",
        "palabras": [
            "profesor",
            "profesora",
            "docente",
            "maestro",
            "maestra",
            "educador",
            "educadora"
        ],
        "contextos": [
            "Académico"
        ]
    },

    "estudiante": {
        "concepto": "persona que estudia",
        "palabras": [
            "estudiante",
            "alumno",
            "alumna",
            "aprendiz",
            "universitario",
            "universitaria"
        ],
        "contextos": [
            "Académico"
        ]
    },

    "estudio": {
        "concepto": "actividad de aprendizaje",
        "palabras": [
            "estudio",
            "estudiar",
            "aprendizaje",
            "aprender",
            "investigar",
            "investigación"
        ],
        "contextos": [
            "Académico"
        ]
    },

    # =====================================================
    # ESTADOS Y CARACTERÍSTICAS
    # =====================================================

    "cansancio": {
        "concepto": "estado de fatiga o agotamiento",
        "palabras": [
            "cansado",
            "cansada",
            "agotado",
            "agotada",
            "fatigado",
            "fatigada",
            "exhausto",
            "exhausta"
        ],
        "contextos": [
            "General",
            "Laboral",
            "Académico",
            "Deportivo"
        ]
    },

    "felicidad": {
        "concepto": "estado de alegría o satisfacción",
        "palabras": [
            "feliz",
            "felices",
            "alegre",
            "alegres",
            "contento",
            "contenta",
            "satisfecho",
            "satisfecha"
        ],
        "contextos": [
            "General",
            "Social"
        ]
    },

    "tristeza": {
        "concepto": "estado emocional de tristeza",
        "palabras": [
            "triste",
            "tristeza",
            "deprimido",
            "deprimida",
            "melancólico",
            "melancólica"
        ],
        "contextos": [
            "General",
            "Social"
        ]
    },

    # =====================================================
    # ÁMBITO LABORAL
    # =====================================================

    "trabajador": {
        "concepto": "persona que realiza una actividad laboral",
        "palabras": [
            "trabajador",
            "trabajadora",
            "empleado",
            "empleada",
            "profesional",
            "colaborador",
            "colaboradora"
        ],
        "contextos": [
            "Laboral"
        ]
    },

    "trabajo": {
        "concepto": "actividad laboral o profesional",
        "palabras": [
            "trabajo",
            "trabajar",
            "empleo",
            "labor",
            "ocupación",
            "actividad laboral"
        ],
        "contextos": [
            "Laboral"
        ]
    },

    # =====================================================
    # TECNOLOGÍA
    # =====================================================

    "computadora": {
        "concepto": "dispositivo electrónico para procesar información",
        "palabras": [
            "computadora",
            "computador",
            "ordenador",
            "pc",
            "laptop",
            "portátil"
        ],
        "contextos": [
            "Tecnología"
        ]
    },

    "programacion": {
        "concepto": "actividad de crear software mediante código",
        "palabras": [
            "programación",
            "programacion",
            "programar",
            "desarrollo",
            "desarrollar",
            "codigo",
            "código"
        ],
        "contextos": [
            "Tecnología",
            "Académico",
            "Laboral"
        ]
    },

    "software": {
        "concepto": "conjunto de programas informáticos",
        "palabras": [
            "software",
            "programa",
            "aplicación",
            "aplicacion",
            "sistema",
            "plataforma"
        ],
        "contextos": [
            "Tecnología"
        ]
    },

    # =====================================================
    # DEPORTES
    # =====================================================

    "deportista": {
        "concepto": "persona que practica un deporte",
        "palabras": [
            "deportista",
            "atleta",
            "jugador",
            "jugadora",
            "competidor",
            "competidora"
        ],
        "contextos": [
            "Deportivo"
        ]
    },

    "competencia": {
        "concepto": "actividad deportiva en la que participan competidores",
        "palabras": [
            "competencia",
            "competición",
            "torneo",
            "campeonato",
            "partido",
            "encuentro"
        ],
        "contextos": [
            "Deportivo"
        ]
    },

    # =====================================================
    # MOVIMIENTO Y TRANSPORTE
    # =====================================================

    "viaje": {
        "concepto": "desplazamiento de un lugar a otro",
        "palabras": [
            "viaje",
            "viajar",
            "desplazamiento",
            "traslado",
            "recorrido"
        ],
        "contextos": [
            "Transporte",
            "General"
        ]
    },

    "avion": {
        "concepto": "medio de transporte aéreo",
        "palabras": [
            "avión",
            "avion",
            "aeronave",
            "avioneta"
        ],
        "contextos": [
            "Transporte"
        ]
    },

    # =====================================================
    # RELACIONES SOCIALES
    # =====================================================

    "amistad": {
        "concepto": "relación afectiva entre personas",
        "palabras": [
            "amigo",
            "amiga",
            "amistad",
            "compañero",
            "compañera",
            "conocido",
            "conocida"
        ],
        "contextos": [
            "Social"
        ]
    },

    "familia": {
        "concepto": "grupo de personas relacionadas familiarmente",
        "palabras": [
            "familia",
            "familiares",
            "padre",
            "madre",
            "mamá",
            "papá",
            "hermano",
            "hermana",
            "hijo",
            "hija"
        ],
        "contextos": [
            "Social"
        ]
    }
}


# =========================================================
# BUSCAR CONCEPTO POR PALABRA
# =========================================================

def buscar_concepto_por_palabra(palabra):

    palabra = palabra.lower().strip()

    for nombre, informacion in CONOCIMIENTO_SEMANTICO.items():

        palabras = [
            p.lower()
            for p in informacion["palabras"]
        ]

        if palabra in palabras:

            return {
                "concepto": nombre,
                "descripcion": informacion["concepto"],
                "contextos": informacion["contextos"],
                "palabras_relacionadas": informacion["palabras"]
            }

    return None


# =========================================================
# OBTENER TODAS LAS PALABRAS DE LA BASE
# =========================================================

def obtener_palabras_conocimiento():

    palabras = []

    for informacion in CONOCIMIENTO_SEMANTICO.values():

        palabras.extend(
            informacion["palabras"]
        )

    return list(set(palabras))