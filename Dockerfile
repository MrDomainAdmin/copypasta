FROM python:3.12-slim-bookworm

ADD requirements.txt /srv/requirements.txt

EXPOSE 8080

WORKDIR "/srv/"
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

ADD copypasta.py /srv/copypasta.py
CMD ["python3", "/srv/copypasta.py"]