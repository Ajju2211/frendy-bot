FROM ubuntu:18.04
ENTRYPOINT []
# RUN apt-get update && apt-get install -y python3 python3-pip && python3 -m pip install --no-cache --upgrade pip && pip3 install --no-cache rasa==1.10.8 && pip3 install --no-cache rasa[transformers] && pip3 install --no-cache pandas==1.1.0
RUN apt-get update && apt-get install -y python3 python3-pip && python3 -m pip install --no-cache --upgrade pip && pip3 install --no-cache rasa==1.10.14 \
    && pip3 install --no-cache rasa[spacy] && python3 -m spacy download en_core_web_md  && python3 -m spacy link en_core_web_md en \
    &&  pip3 install firebase-admin==4.4.0 

# ADD . /app/

COPY . /app/

WORKDIR /app

EXPOSE 5005

ENV PYTHONPATH "${PYTHONPATH}:${PWD}"

RUN echo current path $(pwd)
# RUN cd app/

# CMD cd app/

RUN rasa train

RUN chmod +x /app/start_services.sh
# CMD /app/start_services.sh

CMD /app/start_services.sh
