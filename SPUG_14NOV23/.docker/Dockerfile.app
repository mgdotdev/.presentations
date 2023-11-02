FROM node:alpine3.17

RUN adduser --disabled-password --gecos '' user

WORKDIR /home/user/code

COPY --chown=user ./app ./app

WORKDIR /home/user/code/app

USER user

RUN npm install

CMD ["npm", "run", "dev", "--", "--port", "3000", "--host"]
