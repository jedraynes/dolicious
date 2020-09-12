# dolicious

### Description
Unadjusted non-farm minimum wage by location by year 1988-2019. This is my first, real attempt at scraping an html table, wrangling the data, and visualizng it.

### Source Data
Source data was taken via the US DOL [here](https://www.dol.gov/agencies/whd/state/minimum-wage/history).

### Tableau Visualization
See my visualization on Tableau Public [here](https://public.tableau.com/views/Dolicious/DoliciousDashboard?:language=en&:display_count=y&:origin=viz_share_link).

### Required Packages
	import requests
	from bs4 import BeautifulSoup
	import pandas as pd
	import sys
