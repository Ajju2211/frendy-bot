# Start rasa actions server 
# rasa run actions --actions app.actions --enable-api --cors "*" --debug \
#          -p $PORT
cd app/
rasa run actions --actions actionserver.actions  --cors "*" --debug -p $PORT
