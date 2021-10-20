# Voyages Plotly Visualizations

A companion piece to https://github.com/JohnMulligan/voyagesapi

Specifically, it hits the dataframe endpoint, which was built for this purpose.

This repository contains several interactive visualizations of the Voyages dataset, rendered in Python Dash: https://dash.plotly.com/deployment

## To install

	python3 -m venv venv
	source venv/bin/activate
	pip3 install -r requirements.txt

Then you'll have to make sure you've got the new voyages api (referenced above) running at 127.0.0.1:8000

## General Methods

### Metadata and variables

Each graph type (scatter, sunburst...) currently has its own variables defined in an appropriately-named ..._vars.py file. I don't see a way around hard-coding those.

However, every dashboard also, on load, hits the options endpoint built into the new api. Right now I'm only using this to fetch human-readable variable labels, but it shows how we could offload some textual choices, maybe data validation, maybe even value selection array population, off to the main API.

### Memory

There are two methods currently being used here:

#### in-memory dataframe fetching & faceting

An advantage (_the advantage?_) of dataframes is that they have a lot of data in them that can be looked at this way and that. The disadvantage, of course .... :)

One method we use, then, is to use the dash store component to first fetch a large dataframe and then make it available for faceting: https://dash.plotly.com/dash-core-components/store

This means that the initial fetch (that is, API query) is pretty slow, but every non-query operation after that is very, very fast.

Current apps that use this:

1. scatter_app.py
1. sunburst_app.py

#### no-memory targeted dataframe fetching

However, dataframes do get large enough to really slow the show down, and this is especially true for text-heavy dataframes.

So, another method we're trying out here is only fetching the data we need to render the graph. The upside is that it really, really speeds up the queries in some cases. The downside is that every button you press, the graph goes out and fetches it all over again.

#### compromise positions down the line?

We could do creative callbacks, in theory, that might get us the best of both worlds.

1. Have a quasi-async fetch for large dataframe pulls, that requests, say, five years at a time, and updates the graph as these come back. This would actually look amazing if we could hack it -- the x axis growing over time as it tracks the query's targeted historical facet.
1. More generally than that, we could, upon making a new request, take a look at the dataframe we've got, and see what it has of what we need, in order to make the least-expensive request possible. This, however, would involve programming a lot of logic into the front-end that could make the apps super susceptible to breaking changes on the API side.