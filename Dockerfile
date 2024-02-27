FROM python:3.8
WORKDIR /app

COPY . /app
RUN chmod -R 777 /app
#Update repos
RUN apt-get update && apt-get install -y 
#Install ffmpeg dependency
RUN apt install ffmpeg -y
#Install python3 and pip3
# RUN apt-get install -y python3 python3-pip python3-venv
#Create a virtual python environment
# RUN python3 -m venv /app/venv 
#Activate the virtual environment
# RUN source /app/venv/bin/activate
#Install the requirements into the virtual environment

#Setup virtual display    
# RUN apt-get install xvfb libglib2.0-0=2.50.3-2 libnss3=2:3.26.2-1.1+deb9u1 libgconf-2-4=3.2.6-4+b1 libfontconfig1=2.11.0-6.7+b1 -y
RUN apt-get install xvfb libnss3 libgconf-2-4 chromium -y

RUN Xvfb :99 -ac &
RUN export DISPLAY=:99  


RUN pip3 install -r requirements.txt
RUN cd /app/cernyrobin_django
WORKDIR /app/cernyrobin_django
RUN STUCKINVIM_KEY=""
RUN python3 manage.py makemigrations
RUN python3 manage.py migrate
EXPOSE 8000

# Specify the command to run when the container starts
CMD ["python3", "/app/cernyrobin_django/manage.py", "runserver", "0.0.0.0:8000" ]