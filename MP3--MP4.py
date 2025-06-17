import streamlit as st
import vlc
import time
import tempfile
import os

st.title("Conversion MP4 → MP3")
st.write("Uploader votre fichier MP4 pour extraire l'audio.")

uploaded_file = st.file_uploader("Fichier MP4", type=["mp4"])

if uploaded_file is not None:
    # Créer un fichier temporaire pour le fichier d'entrée
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_input:
        temp_input.write(uploaded_file.read())
        input_file = temp_input.name

    st.write("Fichier uploadé avec succès.")

    # Définir un fichier temporaire pour la sortie MP3
    output_temp = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    output_file = output_temp.name
    output_temp.close()

    # Définir la chaîne d'options pour VLC (désactivation de la vidéo, choix de l'encodeur MP3 et autres paramètres)
    sout = (
        '#transcode{vcodec=none,'
        'acodec=mp3,'
        'ab=192,'
        'channels=2,'
        'samplerate=44100}'
        ':std{access=file,'
        'mux=raw,'
        'dst=' + output_file + '}'
    )

    st.write("Conversion en cours...")

    # Créer l'instance VLC avec l'option pour conserver la chaîne de sortie
    instance = vlc.Instance('--sout-keep')
    media = instance.media_new(input_file, f':sout={sout}', ':sout-keep')
    player = instance.media_player_new()
    player.set_media(media)
    
    # Lancer la conversion
    player.play()

    # Attente active jusqu'à la fin de la conversion
    conversion_in_progress = True
    while conversion_in_progress:
        state = player.get_state()
        if state in (vlc.State.Ended, vlc.State.Stopped, vlc.State.Error):
            conversion_in_progress = False
        time.sleep(1)
    
    player.stop()
    st.success("Conversion terminée !")

    # Proposer le téléchargement du fichier converti
    with open(output_file, "rb") as f:
        st.download_button("Télécharger le MP3", f, file_name="converted.mp3", mime="audio/mp3")

    # Nettoyer les fichiers temporaires
    os.remove(input_file)
    os.remove(output_file)
