require(data.table)
require(ggplot2)
kaggle<-fread("C:/Users/Administrator/PycharmProjects/留影/job-scrapy/User/kaggledata.csv",colClasses="character")
names(kaggle)<-c('userId','userJoinDate','userLastActive','linkedInUrl','occupation','userLocation','currentRanking','tier',
                 'totalGoldMedals','totalSilverMedals','totalBronzeMedals','bio')
kaggle$userLastActiveYear<-substr(kaggle$userLastActive,1,4)
kaggle$userJoinYear<-substr(kaggle$userJoinDate,1,4)
###地区等字段需要整理下
kaggle[userLocation%chin%c("FR","France","france","France  Metropolitan","France, Metropolitan"),userLocation:="France"]
kaggle[userLocation%chin%c("JP"),userLocation:="Japan"]
kaggle[userLocation%chin%c("Russia/The Netherlands","Russian Federation"),userLocation:="Russia"]
kaggle[userLocation%chin%c("india","INDIA","IN"),userLocation:="India"]
kaggle[userLocation%chin%c("PL"),userLocation:="Poland"]
kaggle[userLocation%chin%c("United States","US" ,"USA","USA/Portugal","San Francisco, CA","California, United States"),userLocation:="Unite States"]
kaggle[userLocation%chin%c("Germany & Hungary","DE"),userLocation:="Germany"]
kaggle[userLocation%chin%c("CN","China, P. R.","tencent"  ),userLocation:="China"]
kaggle[userLocation%chin%c("CA" ),userLocation:="Canada" ]
kaggle[userLocation%chin%c("BR" ),userLocation:="Brazil" ]
kaggle[userLocation%chin%c("London","GB","England" ),userLocation:="United Kingdom"]
kaggle[userLocation%chin%c("Australia", "Australiua","AU" ),userLocation:="Austria" ]
kaggle[userLocation%chin%c("NZ","The Netherlands"  ),userLocation:="New Zealand"  ]
kaggle[userLocation%chin%c("MX" ),userLocation:="Mexico"   ]
kaggle$totalGoldMedals<-as.numeric(kaggle$totalGoldMedals)
kaggle$totalSilverMedals<-as.numeric(kaggle$totalSilverMedals)
kaggle$totalBronzeMedals<-as.numeric(kaggle$totalBronzeMedals)
View(kaggle[,.(.N,sum(totalGoldMedals),sum(totalSilverMedals),sum(totalBronzeMedals)),by=userLocation])