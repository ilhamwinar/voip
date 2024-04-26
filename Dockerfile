FROM python:3.9-slim-bullseye
#FROM python:3.7
ENV TZ="Asia/Jakarta"
RUN python -m pip install --upgrade pip
RUN pip install pygame
RUN pip install fastapi
RUN pip install uvicorn
RUN pip install pydantic
RUN pip install requests 
RUN pip install python-multipart

workdir ./voip
RUN ls
RUN pwd

EXPOSE 8200:8200
CMD ["uvicorn", "main:app","--host","0.0.0.0","--port", "8200"]