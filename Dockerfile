FROM continuumio/miniconda3:4.9.2-alpine

WORKDIR /app

# Create the environment:
COPY environment.yml .
RUN conda env create -f environment.yml

# Make RUN commands use the new environment:
SHELL ["conda", "run", "-n", "myenv", "/bin/sh", "-c"]

# Make sure the environment is activated:
RUN echo "Make sure flask is installed:"
RUN python -c "import flask"

# The code to run when container is started:
COPY . .
#ENTRYPOINT ["conda", "run", "--no-capture-output", "-n", "myenv", "python", "app.py"]
ENTRYPOINT ["conda", "run", "--no-capture-output", "-n", "myenv", "python", "tests/eye_detector.test.py"]
