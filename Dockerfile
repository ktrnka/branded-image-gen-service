FROM python:3.10

# Set the working directory inside the container
WORKDIR /app

# Copy everything
# TODO: Copy just the backend and pipfiles
COPY Pipfile Pipfile.lock ./

# Install Pipenv
RUN pip install pipenv

# Install dependencies using Pipenv
RUN pipenv install --system --deploy --verbose

# Temporarily run the embedding index to download the embeddings into the image
# Run local API instance to cache models in container
RUN python3 -c "from txtai.embeddings import Embeddings; Embeddings(path='BAAI/bge-small-en-v1.5')"

COPY local_backend ./local_backend

# Use python3 instead of pipenv due to --system
CMD python3 -m local_backend.slack_app