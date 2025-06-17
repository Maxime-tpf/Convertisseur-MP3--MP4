import streamlit as st
import subprocess
import tempfile
import os

st.title("Conversion MP4 → MP3 avec FFmpeg")
st.write("Uploader votre fichier MP4 pour extraire l'audio.")

# Vérifier que FFmpeg est présent
try:
    subprocess.run(["ffmpeg", "-version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
except FileNotFoundError:
    st.error("FFmpeg n'est pas installé dans l'environnement d'exécution ! Assurez-vous que le fichier `packages.txt` inclut 'ffmpeg'.")
    st.stop()

uploaded_file = st.file_uploader("Fichier MP4", type=["mp4"])

if uploaded_file is not None:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp_input:
        tmp_input.write(uploaded_file.read())
        input_file = tmp_input.name

    st.write("Fichier uploadé avec succès.")

    tmp_output = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    output_file = tmp_output.name
    tmp_output.close()

    st.write("Conversion en cours...")

    command = [
        'ffmpeg',
        '-i', input_file,
        '-vn',
        '-ar', '44100',
        '-ac', '2',
        '-b:a', '192k',
        output_file
    ]

    try:
        subprocess.run(command, check=True)
        st.success("Conversion terminée !")
        with open(output_file, "rb") as f:
            st.download_button("Télécharger le MP3", f, file_name="converted.mp3", mime="audio/mp3")
    except subprocess.CalledProcessError as e:
        st.error("Une erreur est survenue lors de la conversion.")
        st.error(e)
    finally:
        os.remove(input_file)
        os.remove(output_file)
