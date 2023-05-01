# Stage 0, "build-stage", based on Node.js, to build and compile the frontend
FROM node:16-alpine as build-stage

WORKDIR /app

COPY package*.json /app/

RUN npm install

COPY ./ /app/

RUN npm run build

FROM busybox:uclibc
COPY --from=build-stage /app/build /app