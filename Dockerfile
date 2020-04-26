FROM python:3.7



WORKDIR ~/project/project-SoundCloud/

COPY requirements.txt requirements.txt
COPY soundcloud soundcloud

RUN pip3 install --upgrade pip

RUN pip3 install -r requirements.txt
 

COPY run.py ./ 
ENV FLASK_APP run.py





EXPOSE 8000

# ENTRYPOINT  ["./boot.sh"]
