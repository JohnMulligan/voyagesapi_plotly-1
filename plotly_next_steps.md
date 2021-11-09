1. Labels (and maybe a few datatypes?) on the api options.json file need to be corrected.
2. Discard the dcc.mem apps with callbacks -- it appears that these dataframes are simply too large?
3. Remove the hard-coding of the vars in scatter_app and sunburst_app and rely entirely on scatter_vars and sunburst_vars
4. Build a non-factorized version of both graphs -- in other words, don't fetch the nation or the port of departure -- just numerical x var (like year) vs numerical y var (like estimated mortality) and see how much that speeds it up
5. Add a search option on text vars (move this up the priority list?)
6. Consider how we might offer drop-down options on certain text vars with limited values (e.g. geographic vars)
7. Sankey diagrams
8. Maps
9. Pivot tables