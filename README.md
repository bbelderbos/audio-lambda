# Audio lambda

Project to process audio files with [Audio Program Generator](https://pypi.org/project/audio-program-generator/) on AWS lambda.

Steps taken:

1. Create a virtual environment: `python3.9 -m venv venv && source venv/bin/activate`.

2. Pip install requirements as per file: `pip install -r requirements.txt`.

3. Zip the env up for upload to lambda:

		cd venv/lib/python3.9/site-packages
		zip -r9 lambda.pkg.zip *
		mv lambda.pkg.zip ../../../../
		cd ../../../..

	And add the actual lambda script:

		zip -g lambda.pkg.zip lambda.py

4. Now create the lambda function on AWS uploading the generated `lambda.pkg.zip` file.

5. Add [this _ffmpeg_ layer](https://github.com/serverlesspub/ffmpeg-aws-lambda-layer) via [this option](https://serverlessrepo.aws.amazon.com/applications/arn:aws:serverlessrepo:us-east-1:145266761615:applications~ffmpeg-lambda-layer). This got me this ARN: `arn:aws:lambda:us-east-2:825951402381:layer:ffmpeg:1`

6. When doing so you also need to set `PYTHONPATH` to `$PYTHONPATH:/opt/python` so `ffprobe` gets detected, that is under Lambda _Configuration_ > _Env variables_

	I also gave the lambda 256 MB and a timeout of 2 minutes, and changed _Handler_ to `lambda.lambda_handler` under _Runtime settings_ because my script module is `lambda.py`.

7. Run a test event on Lambda. No need for payload, `lambda.py` just defaults to static input files if nothing is provided.

		(venv) $ python lambda.py
		100%|███████████████████████████████████████████████████████████████████████████████| 3/3 [00:00<00:00, 10.22it/s]
		{'statusCode': 200, 'result_file': 'SUQzBAAAAAAAI1RTU0UA......'}

---

TODO: run it through API gateway
