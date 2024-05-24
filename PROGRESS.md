# Current state of the project

Here is a doc that can be used as an overview of the project. One should thus be able to see what exactly needs working on at this current time. The main benefit lies in the simplicity of this documentation process.

### Scraping and downloading data

Currently, there are a few areas to work on regarding scraping and downloading data.

- Savings, Capacity and Sentiment are targeted only by a specific URL, which should be improved (using some element type for xpath etc.) ⛔
- GrossWage and MedianWage are targeted only by a specific URL, which should be improved (using some element type for xpath etc.) ⛔

### Processing the data

Below are the specific subsections of the code that need to be addressed with their current state.

- Grouping and ordering the input files ✅
- Wages ✅
- Unemployment ✅
- Household debt ✅
- Household disposable income ✅
- Employment potential ✅
- Commodities (Gas.py and Electricity.py) ✅
- Savings ✅
- Retail ✅
- Industrial evolution ✅
- Foreign trade ✅
- Capacity utilization 🟡 - explore use of Eurostat data https://data.europa.eu/data/datasets/vhn6fvebcxzpdj4uwqeslw?locale=en 
- Outline the next steps in terms of the data that still need to be transformed 🟡
- Prepare the processing scripts for those and move on to the standardization 🟡
- Standardizing the time dimensions for the whole project ⛔
- Optimizing the code ⛔
