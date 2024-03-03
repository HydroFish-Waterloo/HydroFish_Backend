FROM python:3
COPY requirements.txt /tmp/requirements.txt
RUN apt-get update \
    && apt-get upgrade -y \
    && rm -rf /var/lib/apt/lists/*
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r /tmp/requirements.txt \
    && rm -rf /tmp/requirements.txt \
    && useradd -U developer

USER developer:developer
WORKDIR /backend

COPY --chown=developer:developer . .
RUN chmod +x ./entrypoint.sh  
ENTRYPOINT [ "./entrypoint.sh" ]
CMD ["python", "./manage.py", "runserver", "0.0.0.0:8000"]