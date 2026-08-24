from google import genai
import os

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("ERROR: No se encontró la API Key.")
    exit()

client = genai.Client(api_key=api_key)

respuesta = client.models.generate_content(
    model="gemini-3.6-flash",
    contents="Explica brevemente qué significa la frase 'Ese man está volando' en Colombia."
)

print("\nRESPUESTA DE GEMINI:\n")
print(respuesta.text)