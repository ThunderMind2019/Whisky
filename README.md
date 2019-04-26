# whisky auction scrapers

## Setup

### install virtual environment

```
sudo apt-get install python3-venv

python3 -m venv .venv
```

### Activate virtual environment

```
source /path/to/venv/bin/activate
```

### Install requirements

```
pip install -r requirements.txt
```

### Run command

```

scrapy crawl whiskyhammer_current_spider    # `Whisky Hammer` For current auction (if any)
scrapy crawl whiskyhammer_past_spider    # `Whisky hammer` For past auction (all)

```
### output in json file

```

scrapy crawl whiskyhammer_current_spider -o filename.json    # For current auction (if any)
scrapy crawl whiskyhammer_past_spider -o filename.json    # For past auction (all)

```
