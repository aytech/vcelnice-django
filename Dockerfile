FROM python:3.12-slim
WORKDIR /app

ENV VIRTUAL_ENV=/opt/venv
RUN python -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Install build software
RUN apt update
RUN apt -y upgrade
RUN apt install -y zip
RUN apt install -y curl
RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash - && apt install -y nodejs
RUN corepack enable
RUN npm install -g @angular/cli

# Install dependencies
RUN python -m pip install --upgrade pip
COPY ./requirements.txt ./requirements.txt
RUN pip install -r ./requirements.txt

CMD [ "./build.sh" ]