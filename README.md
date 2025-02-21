## How to use it

- Always first git pull --rebase for new result files
## Entry file
  - productUrl.json
  Add all the urls of the new products in here and remove the urls for products that has been run out.

## Output file
- resultado_HOUR-MIN_DAY_MONTH_YEAR.json
  This will be created after run the script and display the list of products urls for each provider grouped by availabiity in web.
  NOTE: remove from the productUrl.json file the ones that appears as "agotados" in here.

## Run the script
- python3 scrapperProductsJSON.py
