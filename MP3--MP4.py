import streamlit as st
import subprocess
import tempfile
import os

st.title("Conversion MP4 → MP3 avec FFmpeg")
st.write("Uploader votre fichier MP4 pour extraire l'audio.")

uploaded_file = st.file_uploader("Fichier MP4", type=["mp4"])

if uploaded_file is not None:
    # Créer un fichier temporaire pour le fichier d'entrée 
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp_input:
        tmp_input.write(uploaded_file.read())
        input_file = tmp_input.name

    st.write("Fichier uploadé avec succès.")

    # Créer un fichier temporaire pour la sortie MP3
    tmp_output = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    output_file = tmp_output.name
    tmp_output.close()

    st.write("Conversion en cours...")

    # Commande FFmpeg pour extraire l'audio
    command = [
        'ffmpeg',
        '-i', input_file,     # Entrée
        '-vn',                # Désactiver la composante vidéo
        '-ar', '44100',       # Fréquence d'échantillonnage audio
        '-ac', '2',           # Nombre de canaux audio (stéréo)
        '-b:a', '192k',       # Débit audio
        output_file
    ]

    try:
        subprocess.run(command, check=True)
        st.success("Conversion terminée !")

        # Proposer le téléchargement
        with open(output_file, "rb") as f:
            st.download_button("Télécharger le MP3", f, file_name="converted.mp3", mime="audio/mp3")
    except subprocess.CalledProcessError as e:
        st.error("Une erreur est survenue lors de la conversion.")
        st.error(e)
    finally:
        # Nettoyer les fichiers temporaires
        os.remove(input_file)
        os.remove(output_file)
