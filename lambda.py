from urllib.request import urlretrieve
from pathlib import Path

from audio_program_generator import apg

BUCKET = (
    ("https://pb-audio-generator.s3.us-east-2"
     ".amazonaws.com"))
DEFAULT_PHRASE_FILE = f"{BUCKET}/phrase_file.txt"
DEFAULT_SOUND_FILE = f"{BUCKET}/birds.wav"
TMP = Path("/tmp")


def lambda_handler(event, context):
    phrase_file = event.get("phrase_file", DEFAULT_PHRASE_FILE)
    local_phrase_file = TMP / "phrase_file"
    if not local_phrase_file.exists():
        urlretrieve(phrase_file, local_phrase_file)

    sound_file = event.get("sound_file", DEFAULT_SOUND_FILE)
    local_sound_file = TMP / "sound_file"
    if not local_sound_file.exists():
        urlretrieve(sound_file, local_sound_file)

    to_mix = event.get("to_mix", True)
    attenuation = event.get("attenuation", 10)

    audio_gen = apg.AudioProgramGenerator(
        local_phrase_file,
        to_mix,
        local_sound_file,
        attenuation,
    )
    audio_gen.invoke()

    return {
        'statusCode': 200,
        'result_file': audio_gen.save_file
    }


if __name__ == "__main__":
    ret = lambda_handler({}, None)
    print(ret)
