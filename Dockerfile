FROM public.ecr.aws/lambda/python:3.9
COPY app.py   ./
RUN pip install --upgrade pip
RUN pip install requests
RUN pip install line-bot-sdk
RUN pip install openai
CMD ["app.handler"]  
