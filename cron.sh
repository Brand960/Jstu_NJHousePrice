#!/bin/bash                                                                                                                                            

export PATH=$PATH:/usr/local/bin
# source /home/NJ_HousePriceCrawler/venv/bin/activate
cd /home/NJ_HousePriceCrawler/log
now=`date +%F`
clean=`mongo test --eval "db.data.remove({})"`
# scrapy=`nohup /usr/local/bin/scrapy crawl Lianjia >> /home/NJ_HousePriceCrawler/log/$now.log 2>&1 &`
/usr/local/bin/scrapy crawl Lianjia > /home/NJ_HousePriceCrawler/log/$now.log
mongoexport -d test -c data -csv -f price,name,lng,lat,location,when -o /home/NJ_HousePriceCrawler/csv/$now.csv

