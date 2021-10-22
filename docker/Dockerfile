###
### Ubuntu 2004 with default Python 3.9
###

# -- Base --

FROM ubuntu:20.04 AS base

RUN apt-get update -y \
  && apt-get install --yes --no-upgrade --no-install-recommends \
    python3.9 \
    python3-pip \
  && apt-get clean \
  && rm -rf \
    /tmp/* \
    /usr/share/doc/* \
    /var/cache/apt/* \
    /var/lib/apt/lists/* \
    /var/tmp/*

# -- Build --

FROM base AS build

RUN apt-get update -y \
  && apt-get install --yes --no-upgrade --no-install-recommends \
    gcc \
    python3.9-dev \
  && apt-get clean \
  && rm -rf \
    /tmp/* \
    /usr/share/doc/* \
    /var/cache/apt/* \
    /var/lib/apt/lists/* \
    /var/tmp/*

WORKDIR /srv/voyagesapi-plotly

RUN python3.9 -m pip install --user --no-cache-dir --upgrade \
    pip \
    setuptools \
    wheel

COPY src/requirements.txt .
RUN python3.9 -m pip install --user --no-cache-dir -r ./requirements.txt

# -- Release --

FROM base AS release

WORKDIR /srv/voyagesapi-plotly

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PATH=/root/.local/bin:$PATH

COPY --from=build /root/.local /root/.local
COPY . .

ENTRYPOINT ["python3.9"]
CMD ["app_router.py"]
