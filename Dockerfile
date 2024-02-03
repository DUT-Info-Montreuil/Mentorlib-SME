FROM python:3.10

WORKDIR /usr/src/app

#Set arguments
ARG FLASK_DEBUG

# Set environment variables, maybe for specific variables we can move them to the docker-compose file
ENV FLASK_DEBUG=$FLASK_DEBUG 

# Copy pyproject.toml first to avoid reinstalling dependencies when code changes
COPY pyproject.toml . 

COPY . .

RUN pip install -e .

# Set timezone to Paris, France
ENV TZ=Europe/Paris
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

EXPOSE 5050

ENTRYPOINT [ "python3" ]

CMD ["serveur/run.py"]