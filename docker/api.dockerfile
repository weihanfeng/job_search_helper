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

WORKDIR $HOME_DIR/src

CMD gunicorn --workers=4 --bind 0.0.0.0:$PORT --timeout 600 app:app