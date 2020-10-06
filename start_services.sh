cd app/
# Start rasa server with nlu model

# rasa run --model models --enable-api \
#         --endpoints endpoints.yml \
#         --credentials credentials.yml \
#         -p $PORT
# rasa train -c spacy_config.yml && \
rasa train && \
rasa run --model models --enable-api  --endpoints prod_endpoints.yml --cors "*" --debug \
         -p $PORT
