FROM python:3.9-slim
RUN mkdir /Translate-from-image
WORKDIR /Translate-from-image
COPY ./requirements.txt /Translate-from-image
RUN pip install --no-cache-dir -r /Translate-from-image/requirements.txt
RUN gdown --folder "https://drive.google.com/drive/folders/1mh3rzYTAUs-lcCuzqLlX8zMP4MyvMhzd?usp=sharing"
ADD . /Translate-from-image
CMD ["uvicorn", "my_api:app", "--host", "0.0.0.0", "--port", "80"]

