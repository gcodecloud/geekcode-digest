FROM python:3.10.7-buster

WORKDIR /app
COPY . /app

#ENV WECHAT_APP_ID=your_wechat_app_id
#ENV WECHAT_APP_SECRET=your_wechat_app_secret

RUN pip install -r requirements.txt

CMD ["make", "start"]