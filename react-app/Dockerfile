FROM node

RUN mkdir /frontend
WORKDIR /frontend
ADD package.json /frontend/
RUN npm install
ADD . /frontend

EXPOSE 3000
CMD ["npm", "start"]
