FROM ubuntu:latest
MAINTAINER Alex Quin

RUN apt-get update && apt-get -y install cron python3 python3-pip

# Copy /src to /home/src
ADD src /src

RUN pip install --upgrade pip && pip install -r /src/requirements.txt

# RUN python3 /src/main.py
RUN apt-get -y install rsyslog

# Give execution rights on the cron job
RUN chmod 0644 /src/iss-cron

RUN chmod +x /src/run_script.sh

# Apply cron job
RUN crontab /src/iss-cron

RUN touch /cron.log

# Run the command on container startup
CMD cron && tail -f /cron.log