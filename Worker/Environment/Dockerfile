FROM ubuntu:16.10
COPY eval-all.sh
USER useradd -ms /bin/bash contestant
RUN apt-get update
RUN apt-get install -y gcc g++ python3 ghc java-1.8.0-openjdk java-1.8.0-openjdk-devel
RUN mkdir -p /home/contestant/workspace
WORKDIR /home/contestant/workspace
RUN mkdir ./tests
RUN mkdir ./sources
VOLUME /home/contestant/sources
ENTRYPOINT ['/eval-all.sh']
