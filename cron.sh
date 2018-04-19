#! /bin/sh                                                                                                                                            

export PATH=$PATH:/usr/local/bin

source /home/yue/Desktop/NJ_HousePriceCrawler/venv/bin/activate

cd /home/yue/Desktop/NJ_HousePriceCrawler/venv/bin

now=`date +%F`

clean=`mongo test --eval "db.data.remove({})"`

scrapy=`nohup ./python3.5 scrapy crawl Lianjia >> /home/yue/Desktop/NJ_HousePriceCrawler/log/$now.log 2>&1 &`

mongoexport -d NJ_HousePrice -c data -csv -f price,name,lng,lat,location,when -o ~/Desktop/NJ_HousePriceCrawler/csv/$now.csv

