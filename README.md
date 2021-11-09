# Voyages Plotly Visualizations

A companion piece to https://github.com/rice-crc/voyagesapi_plotly

Specifically, it hits the dataframe endpoint, which was built for this purpose.

This repository contains several interactive visualizations of the Voyages dataset, rendered in Python Dash: https://dash.plotly.com/deployment

## Local Deployment

Be sure you have a local deployment of the Voyages API running at http://127.0.0.1:8000/.

Build and run the apps container.

```bash
host:~/Projects/voyagesapi_plotly$ docker-compose up
```

Run specific apps by pointing at their paths, as given in app_router.py

http://127.0.0.1:3000/apps/sunburst_app_nomemory
http://127.0.0.1:3000/apps/scatter_app_nomemory

View container logs.

```bash
host:~/Projects/voyagesapi_plotly$ docker logs voyagesapi-plotly
```

Note the following project resources:

* Plotly Apps: http://127.0.0.1:3000/

## Cleanup

```bash
host:~/Projects/voyagesapi_plotly$ docker-compose down

host:~/Projects/voyagesapi_plotly$ docker container prune
host:~/Projects/voyagesapi_plotly$ docker image prune
host:~/Projects/voyagesapi_plotly$ docker volume prune
host:~/Projects/voyagesapi_plotly$ docker network prune
```

## General Methods

### Metadata and variables

Each graph type (scatter, sunburst...) currently has its own variables defined in an appropriately-named ..._vars.py file. I don't see a way around hard-coding those.

However, every dashboard also, on load, hits the options endpoint built into the new api. Right now I'm only using this to fetch human-readable variable labels, but it shows how we could offload some textual choices, maybe data validation, maybe even value selection array population, off to the main API.

### no-memory targeted dataframe fetching

Dataframes do get large enough to really slow the show down, and this is especially true for text-heavy dataframes.

So, I'm trying only fetching the data we need to render the graph. The upside is that it really, really speeds up the queries in some cases. The downside is that every button you press, the graph goes out and fetches it all over again.

#### compromise positions down the line?

We could do creative callbacks, in theory, that might get us the best of both worlds.

1. Have a quasi-async fetch for large dataframe pulls, that requests, say, five years at a time, and updates the graph as these come back. This would actually look amazing if we could hack it -- the x axis growing over time as it tracks the query's targeted historical facet.
1. More generally than that, we could, upon making a new request, take a look at the dataframe we've got, and see what it has of what we need, in order to make the least-expensive request possible. This, however, would involve programming a lot of logic into the front-end that could make the apps super susceptible to breaking changes on the API side.
