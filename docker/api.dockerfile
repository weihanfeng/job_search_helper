FROM python:3.9-slim-buster

ARG USER=app
ARG ID=1000
ARG HOME_DIR="/home/$USER"
ARG REQUIREMENTS_TXT="requirements.txt"

RUN groupadd -g $ID $USER && useradd -g $ID -m -u $ID -s /bin/bash $USER

WORKDIR $HOME_DIR
USER $USER

COPY --chown=$ID:$ID $REQUIREMENTS_TXT .
RUN pip3 install --no-cache-dir -r $REQUIREMENTS_TXT

COPY --chown=$ID:$ID src/ ./src

EXPOSE 5000

CMD ["python3", "src/app.py"]