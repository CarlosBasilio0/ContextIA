# =========================================================
# MOTOR SEMÁNTICO DE CONTEXTIA
# =========================================================

from sentence_transformers import SentenceTransformer
from sentence_transformers.util import cos_sim


# =========================================================
# CARGAR MODELO SEMÁNTICO
# =========================================================

modelo_semantico = SentenceTransformer(
    "paraphrase-multilingual-MiniLM-L12-v2"
)


# =========================================================
# GENERAR REPRESENTACIÓN SEMÁNTICA
# =========================================================

def generar_embedding(texto):
    """
    Convierte un texto en una representación numérica
    que permite comparar su significado semántico.
    """

    if not texto or not texto.strip():
        return None

    try:
        embedding = modelo_semantico.encode(
            texto,
            convert_to_tensor=True
        )

        return embedding

    except Exception as error:
        print(
            "Error generando embedding:",
            error
        )

        return None


# =========================================================
# CALCULAR SIMILITUD
# =========================================================

def calcular_similitud(texto1, texto2):
    """
    Compara semánticamente dos textos.

    Devuelve un valor entre 0 y 1.
    """

    if not texto1 or not texto2:
        return 0.0

    embedding1 = generar_embedding(texto1)
    embedding2 = generar_embedding(texto2)

    if embedding1 is None or embedding2 is None:
        return 0.0

    try:

        similitud = cos_sim(
            embedding1,
            embedding2
        )

        resultado = float(
            similitud.item()
        )

        # Mantener el resultado entre 0 y 1
        resultado = max(
            0.0,
            min(1.0, resultado)
        )

        return resultado

    except Exception as error:

        print(
            "Error calculando similitud:",
            error
        )

        return 0.0


# =========================================================
# CALCULAR SIMILITUD SEMÁNTICA
# =========================================================

def calcular_similitud_semantica(
    texto1,
    texto2
):
    """
    Función principal utilizada por ContextIA.

    Compara dos textos teniendo en cuenta su significado
    semántico y no solamente las palabras exactas.

    Devuelve un valor entre 0 y 1.
    """

    return calcular_similitud(
        texto1,
        texto2
    )


# =========================================================
# PORCENTAJE DE SIMILITUD
# =========================================================

def porcentaje_similitud(
    texto1,
    texto2
):
    """
    Convierte la similitud semántica en porcentaje.
    """

    similitud = calcular_similitud_semantica(
        texto1,
        texto2
    )

    porcentaje = similitud * 100

    return round(
        porcentaje,
        2
    )


# =========================================================
# PRUEBA DEL MOTOR SEMÁNTICO
# =========================================================

if __name__ == "__main__":

    texto1 = (
        "El profesor está cansado"
    )

    texto2 = (
        "El docente está agotado"
    )

    resultado = porcentaje_similitud(
        texto1,
        texto2
    )

    print(
        f"Similitud semántica: {resultado}%"
    )