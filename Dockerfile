# Base docker image
FROM python:3.12

ADD --chmod=755 https://astral.sh/uv/install.sh /install.sh
RUN /install.sh && rm /install.sh

# the docker container working directory to this newly created directory
WORKDIR /vizro_demo_app


# Copy requirements file, add extra packages to requirements.txt if needed
COPY ./requirements.txt .
# Copy all extra packages that are supposed to be installed
#COPY ./packages ./packages

RUN /root/.cargo/bin/uv pip install --system --no-cache -r requirements.txt

# Copy all the files from the working directory where the command to trigger is file is run from
COPY ./src ./src

# Set the working directory to the location of the dashboard which is to be run in the step below
WORKDIR /vizro_demo_app/src
# Specify the port on which app is listen
EXPOSE 5010

# Run gunicorn with 4 worker process
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5010", "app:server"]

# OR run Flask server (not recommended for production)
# CMD ["python", "app.py"]
