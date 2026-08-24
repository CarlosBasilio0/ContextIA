from django.shortcuts import render
from .models import Analisis

import re
import unicodedata

import spacy

from .motor_semantico import calcular_similitud_semantica
from .conocimiento_semantico import buscar_concepto_por_palabra


# =========================================================
# MODELO DE PROCESAMIENTO DE LENGUAJE NATURAL
# =========================================================

try:
    nlp = spacy.load("es_core_news_sm")
except Exception as error:
    print("Advertencia: no se pudo cargar spaCy:", error)
    nlp = None


# =========================================================
# FUNCIONES AUXILIARES
# =========================================================

def normalizar_texto(texto):
    """
    Convierte el texto a minúsculas, elimina espacios
    innecesarios y elimina las tildes.
    """

    if not texto:
        return ""

    texto = str(texto).lower().strip()

    texto = unicodedata.normalize("NFD", texto)

    texto = "".join(
        caracter
        for caracter in texto
        if unicodedata.category(caracter) != "Mn"
    )

    return texto


def obtener_doc(texto):
    """
    Procesa el texto utilizando spaCy.
    """

    if nlp is None:
        return None

    try:
        return nlp(texto)

    except Exception as error:
        print("Error procesando texto con spaCy:", error)
        return None


# =========================================================
# BASE DE CONOCIMIENTO - MODISMOS
# =========================================================

MODISMOS = {

    "ser un teso": {
        "variantes": [
            "ser un teso",
            "un teso",
            "es un teso",
            "eres un teso",
            "soy un teso"
        ],
        "significado": (
            "Ser una persona muy talentosa, habilidosa "
            "o destacada en una actividad."
        ),
        "contextos": [
            "Académico",
            "Laboral",
            "Deportivo",
            "Social",
            "General"
        ]
    },

    "ser un crack": {
        "variantes": [
            "ser un crack",
            "un crack",
            "es un crack",
            "eres un crack",
            "soy un crack"
        ],
        "significado": (
            "Ser una persona muy talentosa, habilidosa "
            "o destacada en una actividad."
        ),
        "contextos": [
            "Académico",
            "Laboral",
            "Deportivo",
            "Social",
            "General"
        ]
    },

    "estar volando": {
        "variantes": [
            "estar volando",
            "esta volando",
            "está volando",
            "estoy volando",
            "están volando"
        ],
        "significado": (
            "Expresión que puede tener un significado literal "
            "relacionado con desplazarse por el aire o un "
            "significado figurado relacionado con realizar "
            "algo muy bien, rápidamente o con eficiencia."
        ),
        "contextos": [
            "Deportivo",
            "Académico",
            "Laboral",
            "Transporte",
            "General"
        ]
    },

    "dar papaya": {
        "variantes": [
            "dar papaya",
            "dando papaya",
            "da papaya",
            "dio papaya",
            "di papaya"
        ],
        "significado": (
            "Dar una oportunidad o facilitar que otra "
            "persona aproveche una situación."
        ),
        "contextos": [
            "General",
            "Social"
        ]
    },

    "estar pilas": {
        "variantes": [
            "estar pilas",
            "está pilas",
            "esta pilas",
            "estoy pilas",
            "estar muy pilas"
        ],
        "significado": (
            "Estar atento, concentrado o preparado "
            "ante una situación."
        ),
        "contextos": [
            "General",
            "Académico",
            "Laboral"
        ]
    },

    "poner las pilas": {
        "variantes": [
            "poner las pilas",
            "ponerse las pilas",
            "pon las pilas",
            "ponte las pilas",
            "póngase las pilas"
        ],
        "significado": (
            "Empezar a actuar con mayor atención, energía "
            "o responsabilidad."
        ),
        "contextos": [
            "General",
            "Académico",
            "Laboral"
        ]
    },

    "estar en las nubes": {
        "variantes": [
            "estar en las nubes",
            "está en las nubes",
            "esta en las nubes"
        ],
        "significado": (
            "Estar distraído, desconcentrado o pensando "
            "en otra cosa."
        ),
        "contextos": [
            "General",
            "Académico"
        ]
    },

    "meter la pata": {
        "variantes": [
            "meter la pata",
            "metió la pata",
            "metio la pata",
            "metiendo la pata"
        ],
        "significado": (
            "Cometer un error o equivocarse en una situación."
        ),
        "contextos": [
            "General",
            "Social",
            "Laboral"
        ]
    },

    "echar una mano": {
        "variantes": [
            "echar una mano",
            "échame una mano",
            "echame una mano",
            "echarle una mano"
        ],
        "significado": (
            "Ayudar a otra persona en una situación."
        ),
        "contextos": [
            "General",
            "Social",
            "Laboral"
        ]
    },

    "estar al tanto": {
        "variantes": [
            "estar al tanto",
            "está al tanto",
            "esta al tanto"
        ],
        "significado": (
            "Estar informado o conocer lo que está sucediendo."
        ),
        "contextos": [
            "General",
            "Laboral",
            "Académico"
        ]
    },

    "hacerle frente": {
        "variantes": [
            "hacerle frente",
            "hacer frente",
            "hacerle frente a"
        ],
        "significado": (
            "Enfrentar o afrontar una situación o dificultad."
        ),
        "contextos": [
            "General",
            "Laboral",
            "Social"
        ]
    },

    "romperla": {
        "variantes": [
            "romperla",
            "la rompió",
            "la rompio",
            "romperla en"
        ],
        "significado": (
            "Tener un desempeño excelente o destacar "
            "mucho en una actividad."
        ),
        "contextos": [
            "General",
            "Deportivo",
            "Académico",
            "Laboral"
        ]
    },

    "estar duro": {
        "variantes": [
            "estar duro",
            "está duro",
            "esta duro",
            "estoy duro"
        ],
        "significado": (
            "Ser muy competente, fuerte o destacado "
            "en determinada actividad."
        ),
        "contextos": [
            "Deportivo",
            "Laboral",
            "General"
        ]
    },

    "ser una máquina": {
        "variantes": [
            "ser una máquina",
            "ser una maquina",
            "una máquina",
            "una maquina",
            "es una máquina",
            "es una maquina"
        ],
        "significado": (
            "Describir figuradamente a una persona que "
            "destaca por su capacidad, rendimiento "
            "o eficiencia."
        ),
        "contextos": [
            "Deportivo",
            "Académico",
            "Laboral",
            "General"
        ]
    }
}


# =========================================================
# CONTEXTOS
# =========================================================

CONTEXTOS = {

    "Académico": [
        "profesor", "profesora", "docente",
        "estudiante", "alumno", "alumna",
        "universidad", "colegio", "escuela",
        "clase", "examen", "tarea", "materia",
        "curso", "semestre", "nota", "calificación",
        "aprendizaje", "investigación",
        "compañero", "compañera",
        "biblioteca", "libro", "estudiar",
        "estudio", "taller", "parcial",
        "facultad", "carrera", "ingeniería",
        "universitario", "universitaria",
        "programación"
    ],

    "Deportivo": [
        "jugador", "jugadora", "fútbol", "futbol",
        "partido", "equipo", "gol", "cancha",
        "entrenador", "entrenamiento",
        "competencia", "torneo", "deporte",
        "marcador", "liga", "delantero",
        "defensa", "portero", "balón", "pelota",
        "atleta", "basquetbol", "baloncesto",
        "voleibol", "correr", "ciclista",
        "carrera", "medalla", "campeonato"
    ],

    "Laboral": [
        "trabajo", "trabajador", "trabajadora",
        "empresa", "jefe", "jefa",
        "empleado", "empleada", "oficina",
        "proyecto", "reunión", "cliente",
        "negocio", "profesional", "empleo",
        "laboral", "programador",
        "programadora", "desarrollador",
        "desarrolladora", "gerente",
        "salario", "contrato", "reporte",
        "jornada", "programación", "software"
    ],

    "Transporte": [
        "avión", "avion", "aeropuerto", "vuelo",
        "piloto", "helicóptero", "helicoptero",
        "aeronave", "viaje", "aire",
        "avioneta", "pasajero", "pasajera",
        "equipaje", "aterrizaje", "despegue",
        "terminal", "bus", "autobús", "taxi",
        "carro", "vehículo", "vehiculo",
        "tren", "metro", "motocicleta"
    ],

    "Social": [
        "amigo", "amiga", "familia", "fiesta",
        "persona", "vecino", "vecina",
        "comunidad", "reunión", "grupo",
        "pareja", "hermano", "hermana",
        "mamá", "mama", "papá", "papa",
        "padre", "madre", "conocido",
        "conocida", "compañero", "compañera",
        "amigos", "amistad", "social",
        "conversación", "conversacion"
    ],

    "Tecnología": [
        "computadora", "computador", "ordenador",
        "laptop", "portátil", "portatil",
        "tecnología", "tecnologia",
        "informática", "informatica",
        "internet", "red", "software",
        "hardware", "programa", "programación",
        "programacion", "aplicación",
        "aplicacion", "sistema", "sistemas",
        "web", "página", "pagina", "servidor",
        "base", "datos", "código", "codigo",
        "python", "django", "javascript",
        "computación", "computacion",
        "procesador", "memoria", "archivo",
        "teclado", "pantalla", "celular",
        "móvil", "movil"
    ]
}


# =========================================================
# PALABRAS AMBIGUAS
# =========================================================

AMBIGUEDADES = {

    "teso": {
        "literal": (
            "Persona que tiene gran fortaleza, dureza "
            "o habilidad en determinada situación."
        ),
        "figurado": (
            "Persona muy talentosa, habilidosa "
            "o destacada en una actividad."
        )
    },

    "volando": {
        "literal": (
            "Desplazarse o encontrarse en el aire."
        ),
        "figurado": (
            "Realizar algo muy bien, con gran rapidez "
            "o destacar notablemente."
        )
    },

    "maquina": {
        "literal": (
            "Objeto o dispositivo creado para "
            "realizar una función."
        ),
        "figurado": (
            "Persona que destaca mucho por su "
            "habilidad o rendimiento."
        )
    },

    "duro": {
        "literal": (
            "Algo que tiene gran resistencia "
            "y poca facilidad para deformarse."
        ),
        "figurado": (
            "Persona muy competente, fuerte "
            "o destacada en una actividad."
        )
    },

    "crack": {
        "literal": (
            "Palabra utilizada originalmente para "
            "referirse a una grieta o ruptura."
        ),
        "figurado": (
            "Persona muy talentosa o destacada "
            "en una actividad."
        )
    },

    "pilas": {
        "literal": (
            "Dispositivos que almacenan energía "
            "para alimentar aparatos eléctricos."
        ),
        "figurado": (
            "Estar atento, concentrado o preparado "
            "ante una situación."
        )
    },

    "banco": {
        "literal": (
            "Asiento utilizado para sentarse."
        ),
        "figurado": (
            "Entidad financiera donde se realizan "
            "operaciones económicas."
        )
    },

    "planta": {
        "literal": (
            "Ser vivo vegetal que crece en la tierra."
        ),
        "figurado": (
            "Instalación o lugar donde se desarrolla "
            "una actividad industrial."
        )
    },

    "vela": {
        "literal": (
            "Objeto que puede utilizarse para producir luz."
        ),
        "figurado": (
            "Elemento utilizado para impulsar una "
            "embarcación mediante el viento."
        )
    }
}


# =========================================================
# DETECTAR CONTEXTOS
# =========================================================

def detectar_contextos(doc):

    resultados = {}

    if doc is None:
        return resultados

    palabras_contexto = {
        contexto: {
            normalizar_texto(palabra)
            for palabra in palabras
        }
        for contexto, palabras in CONTEXTOS.items()
    }

    for token in doc:

        if token.is_space or token.is_punct:
            continue

        palabra = normalizar_texto(token.text)

        if not palabra:
            continue

        for contexto, palabras in palabras_contexto.items():

            if palabra in palabras:

                if contexto not in resultados:
                    resultados[contexto] = []

                palabras_existentes = {
                    normalizar_texto(p)
                    for p in resultados[contexto]
                }

                if palabra not in palabras_existentes:
                    resultados[contexto].append(token.text)

    return resultados


# =========================================================
# DETECTAR MODISMOS
# =========================================================

def detectar_modismos(texto):

    texto_normalizado = normalizar_texto(texto)

    encontrados = []

    for expresion, informacion in MODISMOS.items():

        for variante in informacion["variantes"]:

            variante_normalizada = normalizar_texto(variante)

            patron = (
                r"(?<!\w)"
                + re.escape(variante_normalizada)
                + r"(?!\w)"
            )

            if re.search(
                patron,
                texto_normalizado
            ):

                encontrados.append({
                    "nombre": expresion,
                    "significado": informacion["significado"],
                    "contextos": informacion["contextos"]
                })

                break

    return encontrados


# =========================================================
# DETECTAR AMBIGÜEDADES
# =========================================================

def detectar_ambiguedades(doc):

    encontrados = []
    palabras_detectadas = set()

    if doc is None:
        return encontrados

    for token in doc:

        if token.is_space or token.is_punct:
            continue

        palabra = normalizar_texto(token.text)

        if palabra in AMBIGUEDADES:

            if palabra in palabras_detectadas:
                continue

            palabras_detectadas.add(palabra)

            informacion = AMBIGUEDADES[palabra]

            encontrados.append({
                "palabra": token.text,
                "literal": informacion["literal"],
                "figurado": informacion["figurado"]
            })

    return encontrados


# =========================================================
# ANÁLISIS SEMÁNTICO
# =========================================================

def analizar_semantica(doc):

    resultados = []

    if doc is None:
        return resultados

    palabras_procesadas = set()

    for token in doc:

        if token.is_space or token.is_punct:
            continue

        palabra_original = token.text

        palabra = normalizar_texto(
            palabra_original
        )

        if not palabra:
            continue

        if palabra in palabras_procesadas:
            continue

        palabras_procesadas.add(palabra)

        try:

            concepto = buscar_concepto_por_palabra(
                palabra
            )

            if concepto:

                resultados.append({
                    "palabra": palabra_original,

                    "concepto": concepto.get(
                        "concepto",
                        ""
                    ),

                    "descripcion": concepto.get(
                        "descripcion",
                        ""
                    ),

                    "contextos": concepto.get(
                        "contextos",
                        []
                    ),

                    "palabras_relacionadas": concepto.get(
                        "palabras_relacionadas",
                        []
                    )
                })

        except Exception as error:

            print(
                "Error en análisis semántico:",
                error
            )

    return resultados


# =========================================================
# CONTEXTO PRINCIPAL
# =========================================================

def obtener_contexto_principal(
    contextos,
    modismos=None
):
    """
    Determina el contexto principal.

    Si existe un modismo, se priorizan los contextos
    compatibles con dicho modismo. Esto evita que una
    palabra secundaria como 'amigo' haga que una oración
    deportiva sea clasificada como Social.
    """

    if not contextos:
        return None

    # -----------------------------------------------------
    # SI EXISTEN MODISMOS
    # -----------------------------------------------------

    if modismos:

        candidatos = {}

        for modismo in modismos:

            contextos_modismo = set(
                modismo.get("contextos", [])
            )

            for contexto, palabras in contextos.items():

                if contexto in contextos_modismo:

                    candidatos[contexto] = len(palabras)

        if candidatos:

            # En caso de empate se utiliza este orden.
            prioridad = [
                "Deportivo",
                "Académico",
                "Laboral",
                "Transporte",
                "Tecnología",
                "Social",
                "General"
            ]

            return max(
                candidatos,
                key=lambda contexto: (
                    candidatos[contexto],
                    -prioridad.index(contexto)
                    if contexto in prioridad
                    else -999
                )
            )

    # -----------------------------------------------------
    # CONTEXTO NORMAL
    # -----------------------------------------------------

    prioridad_general = [
        "Deportivo",
        "Académico",
        "Laboral",
        "Transporte",
        "Tecnología",
        "Social",
        "General"
    ]

    return max(
        contextos,
        key=lambda contexto: (
            len(contextos[contexto]),
            -prioridad_general.index(contexto)
            if contexto in prioridad_general
            else -999
        )
    )


# =========================================================
# PALABRAS RELEVANTES
# =========================================================

def detectar_palabras_relevantes(doc):

    relevantes = []

    if doc is None:
        return relevantes

    categorias_relevantes = {
        "NOUN",
        "VERB",
        "ADJ",
        "ADV",
        "PROPN"
    }

    palabras_excluir = {
        "ser",
        "estar",
        "haber",
        "tener",
        "hacer",
        "ir",
        "y",
        "o",
        "a",
        "de",
        "en"
    }

    for token in doc:

        if token.is_space or token.is_punct:
            continue

        palabra = normalizar_texto(token.text)
        lema = normalizar_texto(token.lemma_)

        if (
            token.pos_ in categorias_relevantes
            and palabra not in palabras_excluir
            and lema not in palabras_excluir
        ):

            if token.text not in relevantes:

                relevantes.append(
                    token.text
                )

    return relevantes


# =========================================================
# INTERPRETACIÓN DE VOLANDO
# =========================================================

def interpretar_volando(contexto):

    if contexto == "Transporte":

        return {
            "contexto": "Transporte",
            "expresion": "Volando",
            "tipo": "Literal",
            "significado": (
                "En este contexto, 'volando' indica que "
                "una persona o aeronave se encuentra "
                "desplazándose por el aire."
            )
        }

    if contexto in {
        "Deportivo",
        "Académico",
        "Laboral"
    }:

        return {
            "contexto": contexto,
            "expresion": "Volando",
            "tipo": "Figurado",
            "significado": (
                "En este contexto, 'volando' expresa que "
                "una persona realiza una actividad con "
                "gran rapidez, eficiencia o buen desempeño."
            )
        }

    return {
        "contexto": "General",
        "expresion": "Volando",
        "tipo": "Ambiguo",
        "significado": (
            "'Volando' puede interpretarse literalmente "
            "como desplazarse por el aire o figuradamente "
            "como realizar algo con gran rapidez."
        )
    }


# =========================================================
# INTERPRETACIÓN CONTEXTUAL
# =========================================================

def interpretar_contexto(
    doc,
    contextos,
    ambiguedades,
    modismos
):

    comparaciones = []

    contexto_principal = obtener_contexto_principal(
        contextos,
        modismos
    )

    palabras = set()

    if doc is not None:

        palabras = {
            normalizar_texto(token.text)
            for token in doc
            if not token.is_space
            and not token.is_punct
        }

    # -----------------------------------------------------
    # VOLANDO
    # -----------------------------------------------------

    if "volando" in palabras:

        comparaciones.append(
            interpretar_volando(
                contexto_principal
            )
        )

    # -----------------------------------------------------
    # TESO
    # -----------------------------------------------------

    if "teso" in palabras:

        if contexto_principal == "Deportivo":

            significado = (
                "En el contexto deportivo, 'teso' indica "
                "que el jugador es muy talentoso, habilidoso "
                "y destaca por su rendimiento."
            )

        elif contexto_principal == "Académico":

            significado = (
                "En el contexto académico, 'teso' indica "
                "que la persona tiene grandes conocimientos, "
                "habilidades o un excelente desempeño."
            )

        elif contexto_principal == "Laboral":

            significado = (
                "En el contexto laboral, 'teso' indica "
                "que la persona es muy competente, "
                "habilidosa y sobresale en su trabajo."
            )

        else:

            significado = (
                "'Teso' se utiliza para describir a una "
                "persona muy talentosa, habilidosa "
                "o destacada."
            )

        comparaciones.append({
            "contexto": contexto_principal or "General",
            "expresion": "Teso",
            "tipo": "Figurado",
            "significado": significado
        })

    # -----------------------------------------------------
    # CRACK
    # -----------------------------------------------------

    if "crack" in palabras:

        if contexto_principal == "Deportivo":

            significado = (
                "En el contexto deportivo, 'crack' indica "
                "que el deportista es muy talentoso y "
                "destaca por su rendimiento."
            )

        elif contexto_principal == "Académico":

            significado = (
                "En el contexto académico, 'crack' indica "
                "que el estudiante destaca por su "
                "conocimiento o desempeño."
            )

        elif contexto_principal == "Laboral":

            significado = (
                "En el contexto laboral, 'crack' indica "
                "que la persona posee un alto nivel "
                "de habilidad o competencia."
            )

        else:

            significado = (
                "'Crack' se utiliza para describir a una "
                "persona muy talentosa o destacada."
            )

        comparaciones.append({
            "contexto": contexto_principal or "General",
            "expresion": "Crack",
            "tipo": "Figurado",
            "significado": significado
        })

    # -----------------------------------------------------
    # DURO
    # -----------------------------------------------------

    if "duro" in palabras:

        if contexto_principal == "Deportivo":

            significado = (
                "En este contexto, la persona es fuerte, "
                "competitiva o difícil de superar."
            )

        elif contexto_principal == "Laboral":

            significado = (
                "En este contexto, 'duro' puede indicar "
                "que una persona trabaja con mucha "
                "exigencia y esfuerzo."
            )

        else:

            significado = (
                "'Duro' puede referirse literalmente a algo "
                "resistente o figuradamente a una persona "
                "fuerte, competente o destacada."
            )

        comparaciones.append({
            "contexto": contexto_principal or "General",
            "expresion": "Duro",
            "tipo": "Figurado",
            "significado": significado
        })

    # -----------------------------------------------------
    # MÁQUINA
    # -----------------------------------------------------

    if "maquina" in palabras:

        comparaciones.append({
            "contexto": contexto_principal or "General",
            "expresion": "Máquina",
            "tipo": "Figurado",
            "significado": (
                "En este contexto, 'máquina' puede utilizarse "
                "de manera figurada para indicar que una "
                "persona destaca por su capacidad, habilidad "
                "o rendimiento."
            )
        })

    # -----------------------------------------------------
    # PILAS
    # -----------------------------------------------------

    if "pilas" in palabras:

        comparaciones.append({
            "contexto": contexto_principal or "General",
            "expresion": "Pilas",
            "tipo": "Figurado",
            "significado": (
                "'Pilas' puede utilizarse figuradamente "
                "para indicar que una persona debe estar "
                "atenta, concentrada o preparada."
            )
        })

    # -----------------------------------------------------
    # MODISMOS
    # -----------------------------------------------------

    expresiones_ya_procesadas = {
        normalizar_texto(
            comparacion["expresion"]
        )
        for comparacion in comparaciones
    }

    for modismo in modismos:

        nombre = modismo["nombre"]

        if normalizar_texto(nombre) in expresiones_ya_procesadas:
            continue

        contextos_modismo = modismo.get(
            "contextos",
            []
        )

        if contexto_principal in contextos_modismo:
            contexto = contexto_principal
        else:
            contexto = "General"

        comparaciones.append({
            "contexto": contexto,
            "expresion": nombre,
            "tipo": "Figurado",
            "significado": modismo["significado"]
        })

    return comparaciones


# =========================================================
# SIGNIFICADO GENERAL
# =========================================================

def generar_significado_general(
    texto,
    doc,
    contextos,
    modismos,
    ambiguedades,
    palabras_relevantes
):

    if not texto.strip():

        return (
            "No se ingresó suficiente información para "
            "generar una interpretación."
        )

    contexto_principal = obtener_contexto_principal(
        contextos,
        modismos
    )

    # =====================================================
    # MODISMOS
    # =====================================================

    if modismos:

        modismo = modismos[0]

        sujeto = None

        if doc is not None:

            for token in doc:

                if token.dep_ in {
                    "nsubj",
                    "nsubj:pass",
                    "csubj"
                }:

                    sujeto = token.text
                    break

        if sujeto:

            if (
                contexto_principal
                and contexto_principal != "General"
            ):

                return (
                    f"La oración indica que "
                    f"{sujeto.lower()} presenta un comportamiento "
                    f"o desempeño destacado dentro del contexto "
                    f"{contexto_principal.lower()}. "
                    f"La expresión '{modismo['nombre']}' "
                    f"se utiliza de manera figurada "
                    f"para expresar esa idea."
                )

            return (
                f"La oración indica que "
                f"{sujeto.lower()} presenta un desempeño "
                f"destacado o realiza una acción de manera "
                f"eficiente. La expresión "
                f"'{modismo['nombre']}' se utiliza con "
                f"un sentido figurado."
            )

        return (
            f"El texto contiene la expresión "
            f"'{modismo['nombre']}', utilizada para expresar "
            f"{modismo['significado'].lower()}"
        )

    # =====================================================
    # AMBIGÜEDADES
    # =====================================================

    if ambiguedades:

        ambiguedad = ambiguedades[0]

        return (
            f"La palabra '{ambiguedad['palabra']}' "
            f"presenta más de una posible interpretación. "
            f"En sentido literal puede significar "
            f"{ambiguedad['literal'].lower()} "
            f"Mientras que en sentido figurado puede "
            f"expresar {ambiguedad['figurado'].lower()}"
        )

    # =====================================================
    # ANÁLISIS CON SPACY
    # =====================================================

    if doc is not None:

        sujeto = None
        verbo_principal = None
        auxiliar = None

        adjetivos = []
        adverbios = []
        sustantivos = []

        for token in doc:

            if token.is_space or token.is_punct:
                continue

            if token.dep_ in {
                "nsubj",
                "nsubj:pass",
                "csubj"
            }:

                if sujeto is None:
                    sujeto = token.text

            if token.pos_ == "AUX":

                if auxiliar is None:
                    auxiliar = normalizar_texto(
                        token.lemma_
                    )

            if token.pos_ == "VERB":

                if verbo_principal is None:
                    verbo_principal = normalizar_texto(
                        token.lemma_
                    )

            if token.pos_ in {
                "NOUN",
                "PROPN"
            }:

                sustantivos.append(
                    token.text
                )

            if token.pos_ == "ADJ":

                adjetivos.append(
                    token.text
                )

            if token.pos_ == "ADV":

                adverbios.append(
                    token.text
                )

        # -------------------------------------------------
        # SUJETO + ESTAR + ADJETIVO
        # -------------------------------------------------

        if sujeto and auxiliar == "estar" and adjetivos:

            estado = adjetivos[0]

            estados = {

                "cansado":
                    "se encuentra en un estado de cansancio",

                "cansada":
                    "se encuentra en un estado de cansancio",

                "feliz":
                    "se encuentra en un estado de felicidad",

                "triste":
                    "se encuentra en un estado de tristeza",

                "enfermo":
                    "se encuentra en un estado de enfermedad",

                "enferma":
                    "se encuentra en un estado de enfermedad",

                "preocupado":
                    "presenta un estado de preocupación",

                "preocupada":
                    "presenta un estado de preocupación",

                "contento":
                    "se encuentra en un estado de satisfacción",

                "contenta":
                    "se encuentra en un estado de satisfacción",

                "enojado":
                    "se encuentra en un estado de enojo",

                "enojada":
                    "se encuentra en un estado de enojo",

                "nervioso":
                    "presenta un estado de nerviosismo",

                "nerviosa":
                    "presenta un estado de nerviosismo",

                "emocionado":
                    "presenta un estado de emoción",

                "emocionada":
                    "presenta un estado de emoción",

                "ocupado":
                    "se encuentra realizando alguna actividad",

                "ocupada":
                    "se encuentra realizando alguna actividad"
            }

            estado_normalizado = normalizar_texto(
                estado
            )

            interpretacion_estado = estados.get(
                estado_normalizado,
                f"presenta la característica "
                f"'{estado.lower()}'"
            )

            significado = (
                f"La oración indica que "
                f"{sujeto.lower()} "
                f"{interpretacion_estado}."
            )

            if (
                contexto_principal
                and contexto_principal != "General"
            ):

                significado += (
                    f" Debido a la presencia de elementos "
                    f"relacionados con el contexto "
                    f"{contexto_principal.lower()}, "
                    f"la situación se puede interpretar "
                    f"dentro de ese ámbito."
                )

            return significado

        # -------------------------------------------------
        # SUJETO + VERBO
        # -------------------------------------------------

        if sujeto and verbo_principal:

            significado = (
                f"La oración indica que "
                f"{sujeto.lower()} realiza o participa "
                f"en una acción relacionada con "
                f"'{verbo_principal}'."
            )

            if adjetivos:

                significado += (
                    f" Además, se describe al sujeto "
                    f"mediante la característica "
                    f"'{adjetivos[0].lower()}'."
                )

            if adverbios:

                significado += (
                    f" El adverbio "
                    f"'{adverbios[0].lower()}' aporta "
                    f"información adicional sobre la "
                    f"manera o circunstancia de la acción."
                )

            if (
                contexto_principal
                and contexto_principal != "General"
            ):

                significado += (
                    f" La presencia de palabras relacionadas "
                    f"con el ámbito "
                    f"{contexto_principal.lower()} "
                    f"permite asociar la situación "
                    f"con ese contexto."
                )

            return significado

        # -------------------------------------------------
        # SUSTANTIVO + ADJETIVO
        # -------------------------------------------------

        if sustantivos and adjetivos:

            significado = (
                f"La oración relaciona el concepto "
                f"'{sustantivos[0]}' con la característica "
                f"'{adjetivos[0]}'."
            )

            if (
                contexto_principal
                and contexto_principal != "General"
            ):

                significado += (
                    f" El contexto identificado corresponde "
                    f"al ámbito "
                    f"{contexto_principal.lower()}."
                )

            return significado

        # -------------------------------------------------
        # SUSTANTIVOS
        # -------------------------------------------------

        if sustantivos:

            significado = (
                "La oración presenta información "
                f"relacionada con "
                f"{', '.join(sustantivos[:3])}."
            )

            if (
                contexto_principal
                and contexto_principal != "General"
            ):

                significado += (
                    f" Los términos utilizados permiten "
                    f"relacionar el texto con el contexto "
                    f"{contexto_principal.lower()}."
                )

            return significado

    # =====================================================
    # CONTEXTO
    # =====================================================

    if contexto_principal:

        return (
            "La oración presenta una situación "
            f"relacionada con el ámbito "
            f"{contexto_principal.lower()}."
        )

    # =====================================================
    # PALABRAS RELEVANTES
    # =====================================================

    if palabras_relevantes:

        palabras = ", ".join(
            palabras_relevantes[:4]
        )

        return (
            f"La oración comunica una idea relacionada "
            f"con las palabras principales: {palabras}. "
            f"Su significado se interpreta de manera "
            f"descriptiva a partir de la estructura "
            f"lingüística."
        )

    # =====================================================
    # RESPALDO
    # =====================================================

    return (
        "La oración presenta un significado descriptivo "
        "basado en las palabras y estructuras lingüísticas "
        "identificadas."
    )


# =========================================================
# ANÁLISIS PLN
# =========================================================

def analizar_pln(doc, texto):

    palabras = []
    entidades = []

    if doc is None:

        tokens = texto.split()

        palabras = [
            {
                "texto": token,
                "categoria": "N/D",
                "lema": normalizar_texto(token)
            }
            for token in tokens
        ]

        numero_oraciones = (
            len(re.findall(r"[.!?]+", texto))
            if texto.strip()
            else 0
        )

        if numero_oraciones == 0 and texto.strip():
            numero_oraciones = 1

        return {
            "numero_palabras": len(tokens),
            "numero_oraciones": numero_oraciones,
            "palabras": palabras,
            "entidades": entidades
        }

    for token in doc:

        if token.is_space or token.is_punct:
            continue

        palabras.append({
            "texto": token.text,
            "categoria": token.pos_,
            "lema": token.lemma_
        })

    for entidad in doc.ents:

        entidades.append({
            "texto": entidad.text,
            "tipo": entidad.label_
        })

    oraciones = list(doc.sents)

    return {
        "numero_palabras": len(palabras),
        "numero_oraciones": len(oraciones),
        "palabras": palabras,
        "entidades": entidades
    }


# =========================================================
# RESUMEN GENERAL
# =========================================================

def generar_resumen_general(
    pln,
    contextos,
    modismos,
    ambiguedades,
    significado_general,
    palabras_relevantes,
    tipo_interpretacion
):

    hallazgos = []

    if modismos:

        hallazgos.append(
            f"Se detectaron {len(modismos)} "
            f"expresión(es) registrada(s)."
        )

    if ambiguedades:

        hallazgos.append(
            f"Se detectaron {len(ambiguedades)} "
            f"palabra(s) con posibles interpretaciones."
        )

    if contextos:

        nombres = ", ".join(
            contextos.keys()
        )

        hallazgos.append(
            "El texto presenta indicadores relacionados "
            f"con los contextos: {nombres}."
        )

    if palabras_relevantes:

        hallazgos.append(
            "Se identificaron palabras relevantes "
            "para comprender el contenido del texto."
        )

    if not hallazgos:

        hallazgos.append(
            "No se encontraron expresiones, "
            "ambigüedades o contextos especializados "
            "registrados."
        )

    return {

        "mensaje": (
            "El texto fue procesado mediante técnicas "
            "de Procesamiento de Lenguaje Natural."
        ),

        "hallazgos": hallazgos,

        "significado_general": significado_general,

        "palabras_relevantes": palabras_relevantes,

        "palabras": pln["numero_palabras"],

        "oraciones": pln["numero_oraciones"],

        "tipo_interpretacion": tipo_interpretacion
    }


# =========================================================
# FUNCIÓN PRINCIPAL DE ANÁLISIS
# =========================================================

def analizar_texto(texto):

    texto = texto.strip()

    if not texto:
        return None

    # -----------------------------------------------------
    # PROCESAMIENTO CON SPACY
    # -----------------------------------------------------

    doc = obtener_doc(texto)

    # -----------------------------------------------------
    # MODISMOS
    # -----------------------------------------------------

    modismos = detectar_modismos(texto)

    # -----------------------------------------------------
    # AMBIGÜEDADES
    # -----------------------------------------------------

    ambiguedades = detectar_ambiguedades(doc)

    # -----------------------------------------------------
    # CONTEXTOS
    # -----------------------------------------------------

    contextos_detectados = detectar_contextos(doc)

    # -----------------------------------------------------
    # ANÁLISIS PLN
    # -----------------------------------------------------

    pln = analizar_pln(
        doc,
        texto
    )

    # -----------------------------------------------------
    # ANÁLISIS SEMÁNTICO
    # -----------------------------------------------------

    analisis_semantico = analizar_semantica(doc)

    # -----------------------------------------------------
    # PALABRAS RELEVANTES
    # -----------------------------------------------------

    palabras_relevantes = detectar_palabras_relevantes(
        doc
    )

    # -----------------------------------------------------
    # SIMILITUD SEMÁNTICA
    # -----------------------------------------------------

    similitudes_semanticas = []

    for concepto in analisis_semantico:

        palabras_relacionadas = concepto.get(
            "palabras_relacionadas",
            []
        )

        for palabra_relacionada in palabras_relacionadas:

            try:

                similitud = calcular_similitud_semantica(
                    texto,
                    palabra_relacionada
                )

                similitudes_semanticas.append({
                    "palabra": concepto.get(
                        "palabra",
                        ""
                    ),

                    "concepto": concepto.get(
                        "concepto",
                        ""
                    ),

                    "relacion": palabra_relacionada,

                    "similitud": round(
                        similitud * 100,
                        2
                    )
                })

            except Exception as error:

                print(
                    "Error calculando similitud semántica:",
                    error
                )

    # -----------------------------------------------------
    # INTERPRETACIÓN CONTEXTUAL
    # -----------------------------------------------------

    comparaciones = interpretar_contexto(
        doc,
        contextos_detectados,
        ambiguedades,
        modismos
    )

    # -----------------------------------------------------
    # SIGNIFICADO GENERAL
    # -----------------------------------------------------

    significado_general = generar_significado_general(
        texto,
        doc,
        contextos_detectados,
        modismos,
        ambiguedades,
        palabras_relevantes
    )

    # -----------------------------------------------------
    # TIPO DE INTERPRETACIÓN
    # -----------------------------------------------------

    if modismos:

        tipo_interpretacion = "Figurada"

    elif ambiguedades:

        tipo_interpretacion = "Ambigua / contextual"

    elif analisis_semantico:

        tipo_interpretacion = "Semántica / contextual"

    else:

        tipo_interpretacion = "Literal / descriptiva"

    # -----------------------------------------------------
    # FORMATEAR CONTEXTOS
    # -----------------------------------------------------

    contextos = []

    for nombre, palabras in contextos_detectados.items():

        contextos.append({
            "nombre": nombre,
            "palabras": palabras
        })

    # -----------------------------------------------------
    # RESUMEN GENERAL
    # -----------------------------------------------------

    resumen_general = generar_resumen_general(
        pln,
        contextos_detectados,
        modismos,
        ambiguedades,
        significado_general,
        palabras_relevantes,
        tipo_interpretacion
    )

    # -----------------------------------------------------
    # RESULTADO
    # -----------------------------------------------------

    return {

        "texto": texto,

        "conceptos_semanticos":
            analisis_semantico,

        "similitudes_semanticas":
            similitudes_semanticas,

        "modismos":
            modismos,

        "ambiguedades":
            ambiguedades,

        "contextos":
            contextos,

        "comparaciones":
            comparaciones,

        "palabras_relevantes":
            palabras_relevantes,

        "analisis_semantico":
            analisis_semantico,

        "significado_general":
            significado_general,

        "tipo_interpretacion":
            tipo_interpretacion,

        "pln":
            pln,

        "resumen_general":
            resumen_general
    }


# =========================================================
# VISTA PRINCIPAL
# =========================================================

def inicio(request):

    resultado = None

    if request.method == "POST":

        texto = request.POST.get(
            "texto",
            ""
        ).strip()

        if texto:

            try:

                resultado = analizar_texto(
                    texto
                )

                # -----------------------------------------
                # GUARDAR EN BASE DE DATOS
                # -----------------------------------------

                try:

                    Analisis.objects.create(
                        texto=texto,
                        resultado=resultado[
                            "significado_general"
                        ]
                    )

                except Exception as error_bd:

                    print(
                        "Advertencia al guardar en BD:",
                        error_bd
                    )

            except Exception as error:

                print(
                    "Error durante el análisis:",
                    error
                )

                numero_palabras = len(
                    texto.split()
                )

                resultado = {

                    "texto": texto,

                    "conceptos_semanticos": [],

                    "similitudes_semanticas": [],

                    "modismos": [],

                    "ambiguedades": [],

                    "contextos": [],

                    "comparaciones": [],

                    "palabras_relevantes": [],

                    "analisis_semantico": [],

                    "significado_general": (
                        "No fue posible generar el "
                        "significado automáticamente. "
                        "El texto fue recibido correctamente "
                        "y puede realizarse un análisis básico."
                    ),

                    "tipo_interpretacion":
                        "Literal / descriptiva",

                    "pln": {

                        "numero_palabras":
                            numero_palabras,

                        "numero_oraciones":
                            1 if texto else 0,

                        "palabras": [],

                        "entidades": []
                    },

                    "resumen_general": {

                        "mensaje":
                            "El texto fue recibido correctamente.",

                        "hallazgos": [
                            "El sistema realizó un "
                            "análisis básico del texto."
                        ],

                        "significado_general": (
                            "No fue posible generar el "
                            "significado automáticamente."
                        ),

                        "palabras_relevantes": [],

                        "palabras":
                            numero_palabras,

                        "oraciones":
                            1 if texto else 0,

                        "tipo_interpretacion":
                            "Literal / descriptiva"
                    }
                }

    return render(
        request,
        "inicio.html",
        {
            "resultado": resultado
        }
    )