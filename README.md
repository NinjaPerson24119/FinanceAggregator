# Finance Aggregator

Aggregates financial CSVs from multiple sources into a single transaction record.

Supports simple preprocessing and postprocessing steps such as:
- Adding missing headers
- Combining in/out columns to a single column with positive and negative values
- Negating transaction amounts (i.e. for credit cards)
- Filtering by date range
- Removing records matching a list of names
- Adding categories based on transaction description
- Prefilling notes based on transaction description

Each source is configured in a `config.json` file. See `config_example/config_example.json` for an example.

## Usage

```
python3 app.py --config config_example/config_example.json

# Output
Loading Some Bank...
	Preprocessing with AddMissingHeader...
	Preprocessing with CombineInOutColumns...
	Postprocessing with FilterByDate...
	Postprocessing with FilterByName...
	Postprocessing with WithCategories...


	Postprocessing with WithNotes...


Saved to /.../output.csv
```

### Example CSV

Input
```
01-Jan-2023,AMAZON,,50
02-Jan-2023,UBERTRIP,,15
04-Jan-2023,IKEA,,269.72
20-Jan-2023,INTERAC e-Transfer From Human,200,
07-Feb-2023,spotify,,11.59
```

Output
```
date,name,amount,source,category,notes
2023-01-01,AMAZON,-50.0,Some Bank,amazon,What did you buy? Pick a better category. 
2023-01-02,UBERTRIP,-15.0,Some Bank,transportation,
2023-01-04,IKEA,-269.72,Some Bank,furniture,
2023-01-20,INTERAC e-Transfer From Human,200.0,Some Bank,deposit,
```

## Configuration
| Option | Description |
| --- | --- |
|--config|Path to config file|
|--work-dir|Path to working directory|

## Environment Setup

```
# Ubuntu
sudo apt install python3-venv

pip3 install virtualenv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
