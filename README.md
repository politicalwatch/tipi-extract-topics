# tipi-extract-topics

This project extracts topics from Google Sheets (One topic, one Sheet) and saves the content on a JSON file ready to import into MongoDB database. It also evaluate all regular expressions each topic has.

## Configuration

* Create a Google Drive Service Account. Yo can follow [this guide](https://pygsheets.readthedocs.io/en/latest/authorization.html)
* Create a credentials.json file into a project directory with your Google Drive Service Account.
* Create a data reference file such as data/data.json.example
* Share with your Google Service Account (it is an email) all Sheets you want to extract.
* Create and install requirements.txt on a python virtualenv.

## Run

```
python app.py data_reference_name.json
```

## Test

```
python -m unittest
```
