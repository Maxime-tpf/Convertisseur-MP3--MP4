import subprocess
import json

def has_audio_stream(file_path: str) -> bool:
    # On execute ffprobe pour obtenir les infos des flux
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
        return False

if not has_audio_stream(input_file):
    st.error("Le fichier ne contient aucune piste audio.")
    st.stop()
