from base64 import b64encode
from pathlib import Path
from urllib.request import urlretrieve

from audio_program_generator import apg

TMP = Path("/tmp")


def lambda_handler(event, context):
    phrase_file = event["phrase_file"]
    sound_file = event["sound_file"]
    mix = event.get("to_mix", False)
    to_mix = str(mix).lower() == "true"  # convert JSON to bool
    attenuation = event.get("attenuation", 0)

    local_phrase_file = TMP / "phrase_file"
    if not local_phrase_file.exists():
        urlretrieve(phrase_file, local_phrase_file)

    local_sound_file = TMP / "sound_file"
    if not local_sound_file.exists():
        urlretrieve(sound_file, local_sound_file)

    try:
        audio_gen = apg.AudioProgramGenerator(
            local_phrase_file,
            to_mix,
            local_sound_file,
            attenuation,
        )
        audio_gen.invoke()
        return {
            'statusCode': 200,
            'result_file': encode(audio_gen.save_file)
        }
    except Exception as exc:
        return {
            'statusCode': 400,
            'exception': str(exc)
        }


def encode(file):
    with open(file, 'rb') as f:
        return b64encode(f.read()).decode('utf-8')


if __name__ == "__main__":
    ret = lambda_handler({}, None)
    print(ret)
