import streamlit as st
import subprocess
import json
import tempfile
import os

def has_audio_stream(file_path: str) -> bool:
    """Utilise ffprobe pour vérifier si le fichier possède une piste audio."""
    command = [
       'ffprobe', '-v', 'error',
       '-select_streams', 'a',
       '-show_entries', 'stream=codec_type',
       '-of', 'json', file_path
    ]
    try:
       result = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
       output = json.loads(result.stdout)
       return len(output.get("streams", [])) > 0
    except Exception as e:
       st.error("Erreur lors de la vérification du flux audio.")
       st.error(e)
       return False

st.title("Conversion MP4 → MP3 avec FFmpeg")
st.write("Uploader votre fichier MP4 pour extraire l'audio.")

# Uploader le fichier MP4
uploaded_file = st.file_uploader("Fichier MP4", type=["mp4"])

if uploaded_file is not None:
    # Créer un fichier temporaire pour le fichier d'entrée
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp_input:
        tmp_input.write(uploaded_file.read())
        input_file = tmp_input.name

    st.write("Fichier uploadé avec succès.")

    # Vérifier que le fichier contient une piste audio
    if not has_audio_stream(input_file):
        st.error("Le fichier ne contient aucune piste audio.")
        os.remove(input_file)
        st.stop()

    # Créer un fichier temporaire pour la sortie MP3
    tmp_output = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    output_file = tmp_output.name
    tmp_output.close()

    st.write("Conversion en cours...")

    command = [
        'ffmpeg',
        '-y',              # Forcer l'écrasement du fichier de sortie existant
        '-i', input_file,
        '-vn',             # Désactiver la composante vidéo
        '-ar', '44100',    # Fréquence d'échantillonnage audio
        '-ac', '2',        # Nombre de canaux audio (stéréo)
        '-b:a', '192k',    # Débit audio
        output_file
    ]

    try:
        result = subprocess.run(
            command, check=True,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )
        st.success("Conversion terminée !")
        with open(output_file, "rb") as f:
            st.download_button("Télécharger le MP3", f, file_name="converted.mp3", mime="audio/mp3")
    except subprocess.CalledProcessError as e:
        st.error("Une erreur est survenue lors de la conversion.")
        st.error(e.stderr)
    finally:
        os.remove(input_file)
        os.remove(output_file)
