FROM python:alpine

RUN pip install Flask
RUN pip install vtt_to_srt3
RUN pip install --upgrade youtube_dl
RUN pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
RUN pip install -U flask-cors

WORKDIR app

CMD ["python", "main.py"]
