FROM agrigorev/zoomcamp-model:mlops-2024-3.10.13-slim

RUN pip install pipenv==2024.0.1

COPY requirements.txt ./
RUN pipenv install -r requirements.txt

# To avoid reinstalling if only changing in script
COPY batch_inference.py ./

ENTRYPOINT ["pipenv", "run", "python","batch_inference.py"]