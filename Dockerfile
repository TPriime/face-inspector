FROM continuumio/miniconda3:4.9.2-alpine as build

WORKDIR /app

# Create the environment:
COPY environment.yml .
COPY requirements.txt .
RUN conda env create -f environment.yml

# Install conda-pack:
RUN conda install -c conda-forge conda-pack

# Use conda-pack to create a standalone enviornment
# in /venv:
RUN conda-pack -n myenv -o /tmp/env.tar && \
  mkdir /venv && cd /venv && tar xf /tmp/env.tar && \
  rm /tmp/env.tar

# We've put venv in same path it'll be in final image,
# so now fix up paths:
RUN /venv/bin/conda-unpack


# The runtime-stage image; we can use Debian as the
# base image since the Conda env also includes Python
# for us.
FROM debian:buster AS runtime

# Copy /venv from the previous stage:
COPY --from=build /venv /venv

# Make sure the environment is activated:
#RUN echo "Make sure flask is installed:"
#RUN python -c "import flask"

# The code to run when container is started:
COPY . .

# When image is run, run the code with the environment
# activated:
SHELL ["/bin/bash", "-c"]
# Run tests
RUN source /venv/bin/activate && python tests/eye_detector.test.py

EXPOSE 5000
ENTRYPOINT ["source", "/venv/bin/activate", "&&", "python", "app.py"]
