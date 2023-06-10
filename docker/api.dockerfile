# FROM python:3.9-slim-buster

# ARG USER=app
# ARG ID=1000
# ARG HOME_DIR="/home/$USER"
# ARG REQUIREMENTS_TXT="requirements.txt"

# RUN groupadd -g $ID $USER && useradd -g $ID -m -u $ID -s /bin/bash $USER

# # install system dependencies
# RUN apt-get update \
#     && apt-get -y install gcc make \
#     && rm -rf /var/lib/apt/lists/*s
# # install google chrome
# RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
# RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
# RUN apt-get -y update
# RUN apt-get install -y google-chrome-stable
# # install chromedriver
# RUN apt-get install -yqq unzip
# RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip
# RUN unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/

# WORKDIR $HOME_DIR
# USER $USER

# COPY --chown=$ID:$ID $REQUIREMENTS_TXT .
# RUN pip3 install --no-cache-dir -r $REQUIREMENTS_TXT

# COPY --chown=$ID:$ID src/ ./src

# EXPOSE 5000

# CMD ["python3", "src/app.py"]


FROM python:3.9

ARG HOME_DIR="/home/app"
ARG REQUIREMENTS_TXT="requirements.txt"

# install system dependencies
RUN apt-get update \
    && apt-get -y install gcc make \
    && rm -rf /var/lib/apt/lists/*s
# install google chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
RUN apt-get -y update
RUN apt-get install -y google-chrome-stable
# install chromedriver
RUN apt-get install -yqq unzip
RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip
RUN unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/

WORKDIR $HOME_DIR

COPY $REQUIREMENTS_TXT .
RUN pip3 install --no-cache-dir -r $REQUIREMENTS_TXT

COPY src/ ./src

EXPOSE $PORT

WORKDIR /src

CMD gunicorn --workers=4 --bind 0.0.0.0:$PORT src.app:app
# EXPOSE 5000

# CMD ["python3", "src/app.py"]