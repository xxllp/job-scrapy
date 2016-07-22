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
kaggle[userLocation%chin%c("Russia/The Netherlands","Russian Federation","RU"),userLocation:="Russia"]
kaggle[userLocation%chin%c("india","INDIA","IN"),userLocation:="India"]
kaggle[userLocation%chin%c("PL"),userLocation:="Poland"]
kaggle[userLocation%chin%c("United States","US" ,"USA","USA/Portugal","San Francisco, CA","California, United States"),userLocation:="Unite States"]
kaggle[userLocation%chin%c("Germany & Hungary","DE"),userLocation:="Germany"]
kaggle[userLocation%chin%c("CN","China, P. R.","tencent"  ),userLocation:="China"]
kaggle[userLocation%chin%c("CA" ),userLocation:="Canada" ]
kaggle[userLocation%chin%c("BR" ),userLocation:="Brazil" ]
kaggle[userLocation%chin%c("London","GB","England" ,"UK"),userLocation:="United Kingdom"]
kaggle[userLocation%chin%c("Australia", "Australiua","AU" ),userLocation:="Austria" ]
kaggle[userLocation%chin%c("NZ","The Netherlands"  ),userLocation:="New Zealand"  ]
kaggle[userLocation%chin%c("MX" ),userLocation:="Mexico"   ]
kaggle[userLocation%chin%c("South Italy","IT" ),userLocation:="Italy"   ]
kaggle[userLocation%chin%c("switzerland" ),userLocation:="Switzerland"   ]
kaggle[userLocation%chin%c("HK" ),userLocation:="Hong Kong"   ]
kaggle[userLocation%chin%c("Bilbao, Basque Country, Spain","Girona-Spain" ),userLocation:="Spain"   ]
kaggle[userLocation%chin%c("UA" ),userLocation:="Ukraine"    ]
kaggle[userLocation%chin%c("GR" ),userLocation:="Greece"   ]
kaggle[userLocation%chin%c("UAE" ),userLocation:="United Arab Emirates"  ]
kaggle$totalGoldMedals<-as.numeric(kaggle$totalGoldMedals)
kaggle$totalSilverMedals<-as.numeric(kaggle$totalSilverMedals)
kaggle$totalBronzeMedals<-as.numeric(kaggle$totalBronzeMedals)


###统计人数和获得的名次人数，发现前几名分别为美，俄，英国，印度，中国暂时排在第六。。。香港台湾也有进入
df<-kaggle[,.(cnt=.N,gcnt=sum(totalGoldMedals),scnt=sum(totalSilverMedals),bcnt=sum(totalBronzeMedals)),by=userLocation]

p <- ggplot(data = df, mapping = aes(x = 'Content', y = cnt, fill = userLocation)) + geom_bar(stat = 'identity', position = 'stack', width = 1)  
p  

label_value <- paste('(', round(df$cnt/sum(df$cnt) * 100, 1), '%)', sep = '')  
label_value  
label <- paste(df$userLocation, label_value, sep = '')  
label  
p + coord_polar(theta = 'y') + labs(x = '', y = '', title = '') + theme(axis.text = element_blank()) + theme(axis.ticks = element_blank()) + 
  theme(legend.position = "none") + 
  geom_text(aes(y = df$cnt/2 + c(0, cumsum(df$cnt)[-length(df$cnt)]), x = sum(df$cnt)/1800, label = label)) 

p + coord_polar(theta = 'y') + labs(x = '', y = '', title = '') + theme(axis.text = element_blank()) + 
  theme(axis.ticks = element_blank()) + scale_fill_discrete(labels = label)  

###看了下排名，中国排名前500的才10人，占比%2，高端的厚度还是比较浅
hist(kaggle[userLocation=="China"]$currentRanking)

###专业未知