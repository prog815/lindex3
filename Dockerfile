FROM python:3.8-alpine

WORKDIR /app

COPY . /app

RUN pip3 install -r requirements.txt
# RUN python ./init_db.py

# RUN touch /app/update.log
# RUN echo "2 */6 * * * cd /app; /bin/sh ./update.sh >> ./update.log 2>&1" > /app/crontab
# RUN crontab /app/crontab

CMD crond && python ./app.py