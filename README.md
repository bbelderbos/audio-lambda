# Audio lambda

Project to process audio on lambda

Steps taken:

1. Create a virtual environment

2. Pip install requirements as per file

3. Zip it up:

		cd venv/lib/python3.9/site-packages
		zip -r9 lambda.pkg.zip *
		mv lambda.pkg.zip ../../../../
		cd ../../../..
		zip -g lambda.pkg.zip lambda.py

4. Create a lambda and upload the generated zip file

5. Add [this _ffmpeg_ layer](https://github.com/serverlesspub/ffmpeg-aws-lambda-layer) via [this option](https://serverlessrepo.aws.amazon.com/applications/arn:aws:serverlessrepo:us-east-1:145266761615:applications~ffmpeg-lambda-layer). This got me this ARN: `arn:aws:lambda:us-east-2:825951402381:layer:ffmpeg:1`

6. When doing so you also need to set `PYTHONPATH` to `$PYTHONPATH:/opt/python` under Lambda _Configuration_ > _Env variables_ (I also gave it 256 MB and a timeout of 2 minutes, and changed _Handler_ to `lambda.lambda_handler` under _Runtime settings_).

7. Run a test event on Lambda. No need for payload, `lambda.py` just defaults to static input files if nothing is provided.
