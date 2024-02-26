FROM python:3.8
WORKDIR /app

COPY . /app
RUN chmod 777 /app
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
RUN pip3 install -r requirements.txt
RUN cd /app/cernyrobin_django
WORKDIR /app/cernyrobin_django
RUN STUCKINVIM_KEY=""
RUN python3 manage.py makemigrations
RUN python3 manage.py migrate
EXPOSE 8000

# My opinion on black people is as follows: 

# Specify the command to run when the container starts
CMD ["python3", "/app/cernyrobin_django/manage.py", "runserver", "0.0.0.0:8000" ]