# Pokemon.com Scrapy Project

This project is configured to be hosted on [Scrapy Cloud](https://www.zyte.com/scrapy-cloud/).  

It uses [Zyte Smart Proxy Manager](https://scrapinghub.com/?rfsn=4170080.0597ad) as proxy service.  

The dataset can be found [here](https://www.kaggle.com/datasets/patkle/over-13k-cards-from-the-pokmon-trading-card-game).  
A Jupyter Notebook detailing how I plan to become Pokémon master can be found [here](https://www.kaggle.com/code/patkle/becoming-pok-mon-trading-card-master).

## TCG

The spider can be ran with
```zsh
python3 -m scrapy crawl tcg -a pages=5 -O tcg.csv
```

### Arguments

With `-a` you can specify arguments for the spider.  

|argument   |type  |description   | 
|---|---|---|
|pages   |int   |number of pages to scrape   |


## Setting up locally
  
When setting up this project locally you must create a **.env** file with the following data:  

|setting   |description   |  
|---|---|
|ZYTE_SMARTPROXY_APIKEY   |your smart proxy manager api key   |
  

## Deploy to Scrapy Cloud
There's a shortcut in the Makefile, just running `make deploy` will deploy the project to Scrapy Cloud (given that you provided the project ID in `scrapinghub.yml`).Don't forget to add the following settings in your cloud project's settings:
|setting   |description   | 
|---|---|
|ZYTE_SMARTPROXY_APIKEY   |your smart proxy manager api key   |
  
## Also, 
you could [buy me a coffe](https://www.buymeacoffee.com/kleinp) if you wanted to. I'd really appreciate that.  