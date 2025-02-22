FROM debian:bookworm
RUN apt-get update
RUN apt-get upgrade --yes
RUN apt-get install python3 --yes
RUN apt-get install python3-pytest --yes
RUN apt-get install python3-matplotlib --yes
RUN mkdir /meta_magical_garden
WORKDIR /meta_magical_garden
COPY . .
CMD ["./launch.sh"]
