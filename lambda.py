from base64 import b64encode
from pathlib import Path
from urllib.request import urlretrieve

from audio_program_generator import apg

TMP = Path("/tmp")


def lambda_handler(event, context):
    phrase_file = event["phrase_file"]
    sound_file = event.get("sound_file", None)

    local_phrase_file = TMP / "phrase_file"
    local_sound_file = TMP / "sound_file"

    if not local_phrase_file.exists():
        urlretrieve(phrase_file, local_phrase_file)

    if sound_file:
        if not local_sound_file.exists():
            urlretrieve(sound_file, local_sound_file)

    slow = event.get("slow", False)
    attenuation = event.get("attenuation", 10)
    kwargs = dict(
        slow=slow,
        attenuation=attenuation)

    pfile, sfile = None, None
    try:
        pfile = open(local_phrase_file)
        sfile = open(local_sound_file, 'rb') if sound_file else None

        audio_gen = apg.AudioProgramGenerator(pfile, sfile, **kwargs)

        out_file = audio_gen.invoke()
        out_file_encoded = b64encode(out_file.read()).decode('utf-8')

        return {
            'status_code': 200,
            'result_file': out_file_encoded
        }
    except Exception as exc:
        return {
            'status_code': 400,
            'exception': str(exc)
        }
    finally:
        if pfile is not None:
            pfile.close()
        if sfile is not None:
            sfile.close()


def encode(file):
    with open(file, 'rb') as f:
        return b64encode(f.read()).decode('utf-8')


if __name__ == "__main__":
    bucket = (
        ("https://pb-audio-generator.s3.us-east-2"
         ".amazonaws.com"))
    payload = dict(
        phrase_file=f"{bucket}/phrase_file.txt",
        sound_file=f"{bucket}/birds.wav"
    )
    ret = lambda_handler(payload, None)
    print(ret)
