# doi2notion
https://qiita.com/130n/items/ee8b89e87f992ee5b7cf

# Setup
## Notion
1. Create integration
2. Create database
    - Add connections to the integration
    - Add following properties
        - Authors (Multi-select)
        - Year (Number)
        - Journal (Select)
        - Subject (Multi-select)
        - DOI (Text)
        - Type (Select)
        - Bibtex (Text)
        - Title (Text)
        - Abstract (Text)

## Python
Install packages.

```
pip install -r requirements.txt
```

# Run
Execute doi2notion.py with arguments Notion API key, Database ID, and DOI.

```
python3 doi2notion.py secret_ABCdef123 a1b2c3 10.1063/1.4961149
```
