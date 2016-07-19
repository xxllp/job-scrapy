#coding=utf-8
#爬取kaggle上的用户数据 https://www.kaggle.com/rankings 和每个用户的信息
##需要得到的信息，用户国家，教育和职业分布，可以得到获得冠军的一些有用的成长之路更好哈。需要从其关联的帐号（linkin，github等）得到很多有用的数据
###用户主页基本都是js渲染上去的，数据也都嵌在js里面
import requests,json,re,time
import pyquery as pq

# user_competition_url="https://www.kaggle.com/stasg7/competitions.json?sortBy=best&page=2&group=null"
# data=json.loads(requests.get(user_competition_url,headers=head).content)
# for competition in data.get("competitions"):
#     print competition

#ReactDOM.render(React.createElement(KaggleReactComponents.ProfileContainerReact, {"userId":3230,"displayName":"Naokazu Mizuta","userLocation":"Japan","gitHubUserName":"naokazumizuta","twitterUserName":null,"linkedInUrl":null,"websiteUrl":null,"occupation":null,"organization":null,"bio":"Ph.D, Mathematics","userLastActive":"2016-07-15T22:53:52.45Z","userJoinDate":"2010-10-10T13:01:16Z","performanceTier":"grandmaster","performanceTierCategory":"competitions","userUrl":"/naokazumizuta","userAvatarUrl":"https://secure.gravatar.com/avatar/1a99fa69a72463665158d2bd49b97725.jpg?r=pg\u0026s=400\u0026d=https%3a%2f%2fkaggle2.blob.core.windows.net%2favatars%2fthumbnails%2fdefault-thumb.png","activityUrl":"/naokazumizuta/activity.json","genieUrl":null,"canEdit":false,"canCreateDatasets":false,"userName":"naokazumizuta","activePane":"home","totalDatasets":0,"competitionsSummary":{"tier":"grandmaster","totalResults":50,"rankPercentage":0.0008108743,"rankOutOf":46863,"rankCurrent":38,"rankHighest":2,"totalGoldMedals":14,"totalSilverMedals":12,"totalBronzeMedals":8,"highlights":[{"title":"Event Recommendation Engine Challenge","date":"2013-02-20T23:59:00Z","medal":"gold","score":2,"scoreOutOf":223,"url":"/c/event-recommendation-engine-challenge","thumbnailUrl":"https://kaggle2.blob.core.windows.net/competitions/kaggle/3288/logos/thumb76_76.png"},{"title":"Cervical Cancer Screening","date":"2016-02-01T23:59:00Z","medal":"gold","score":3,"scoreOutOf":40,"url":"/c/cervical-cancer-screening","thumbnailUrl":"https://kaggle2.blob.core.windows.net/competitions/kaggle/4494/logos/thumb76_76.png"},{"title":"Caterpillar Tube Pricing","date":"2015-08-31T23:59:00Z","medal":"gold","score":3,"scoreOutOf":1323,"url":"/c/caterpillar-tube-pricing","thumbnailUrl":"https://kaggle2.blob.core.windows.net/competitions/kaggle/4467/logos/thumb76_76.png"}],"summaryType":"competitions"},"scriptsSummary":{"tier":"contributor","totalResults":0,"rankPercentage":0.129708052,"rankOutOf":8974,"rankCurrent":null,"rankHighest":null,"totalGoldMedals":0,"totalSilverMedals":0,"totalBronzeMedals":0,"highlights":[],"summaryType":"kernels"},"discussionsSummary":{"tier":"contributor","totalResults":46,"rankPercentage":0.0174412057,"rankOutOf":17774,"rankCurrent":null,"rankHighest":null,"totalGoldMedals":1,"totalSilverMedals":1,"totalBronzeMedals":20,"highlights":[{"title":"After shock, Let\u0027s talk about solutions","date":"2014-09-03T12:27:29.93Z","medal":"gold","score":14,"scoreOutOf":0,"url":"/c/liberty-mutual-fire-peril/forums/t/10194/after-shock-let-s-talk-about-solutions/53027#post53027","thumbnailUrl":null},{"title":"#1 Dexter\u0027s Lab winning solution","date":"2016-04-19T14:29:05.863Z","medal":"silver","score":5,"scoreOutOf":0,"url":"/c/bnp-paribas-cardif-claims-management/forums/t/20247/1-dexter-s-lab-winning-solution/115656#post115656","thumbnailUrl":null},{"title":"being smart about loading data","date":"2016-02-03T02:35:31.59Z","medal":"bronze","score":4,"scoreOutOf":0,"url":"/c/cervical-cancer-screening/forums/t/18693/being-smart-about-loading-data/106663#post106663","thumbnailUrl":null}],"summaryType":"discussion"},"achievement":null,"pageMessages":[]}), document.getElementById("react-ProfileContainerReact-1"));

###获取kaggeler的主页详细信息
def getmainpage(username):
  main_page="https://www.kaggle.com%s"%(username)
  content=requests.get(main_page).content
  #content='ReactDOM.render(React.createElement(KaggleReactComponents.ProfileContainerReact, {"userId":3230,"displayName":"Naokazu Mizuta","userLocation":"Japan","gitHubUserName":"naokazumizuta","twitterUserName":null,"linkedInUrl":null,"websiteUrl":null,"occupation":null,"organization":null,"bio":"Ph.D, Mathematics","userLastActive":"2016-07-15T22:53:52.45Z","userJoinDate":"2010-10-10T13:01:16Z","performanceTier":"grandmaster","performanceTierCategory":"competitions","userUrl":"/naokazumizuta","userAvatarUrl":"https://secure.gravatar.com/avatar/1a99fa69a72463665158d2bd49b97725.jpg?r=pg\u0026s=400\u0026d=https%3a%2f%2fkaggle2.blob.core.windows.net%2favatars%2fthumbnails%2fdefault-thumb.png","activityUrl":"/naokazumizuta/activity.json","genieUrl":null,"canEdit":false,"canCreateDatasets":false,"userName":"naokazumizuta","activePane":"home","totalDatasets":0,"competitionsSummary":{"tier":"grandmaster","totalResults":50,"rankPercentage":0.0008108743,"rankOutOf":46863,"rankCurrent":38,"rankHighest":2,"totalGoldMedals":14,"totalSilverMedals":12,"totalBronzeMedals":8,"highlights":[{"title":"Event Recommendation Engine Challenge","date":"2013-02-20T23:59:00Z","medal":"gold","score":2,"scoreOutOf":223,"url":"/c/event-recommendation-engine-challenge","thumbnailUrl":"https://kaggle2.blob.core.windows.net/competitions/kaggle/3288/logos/thumb76_76.png"},{"title":"Cervical Cancer Screening","date":"2016-02-01T23:59:00Z","medal":"gold","score":3,"scoreOutOf":40,"url":"/c/cervical-cancer-screening","thumbnailUrl":"https://kaggle2.blob.core.windows.net/competitions/kaggle/4494/logos/thumb76_76.png"},{"title":"Caterpillar Tube Pricing","date":"2015-08-31T23:59:00Z","medal":"gold","score":3,"scoreOutOf":1323,"url":"/c/caterpillar-tube-pricing","thumbnailUrl":"https://kaggle2.blob.core.windows.net/competitions/kaggle/4467/logos/thumb76_76.png"}],"summaryType":"competitions"},"scriptsSummary":{"tier":"contributor","totalResults":0,"rankPercentage":0.1296936,"rankOutOf":8975,"rankCurrent":null,"rankHighest":null,"totalGoldMedals":0,"totalSilverMedals":0,"totalBronzeMedals":0,"highlights":[],"summaryType":"kernels"},"discussionsSummary":{"tier":"contributor","totalResults":46,"rankPercentage":0.0174412057,"rankOutOf":17774,"rankCurrent":null,"rankHighest":null,"totalGoldMedals":1,"totalSilverMedals":1,"totalBronzeMedals":20,"highlights":[{"title":"After shock, Let\u0027s talk about solutions","date":"2014-09-03T12:27:29.93Z","medal":"gold","score":14,"scoreOutOf":0,"url":"/c/liberty-mutual-fire-peril/forums/t/10194/after-shock-let-s-talk-about-solutions/53027#post53027","thumbnailUrl":null},{"title":"#1 Dexter\u0027s Lab winning solution","date":"2016-04-19T14:29:05.863Z","medal":"silver","score":5,"scoreOutOf":0,"url":"/c/bnp-paribas-cardif-claims-management/forums/t/20247/1-dexter-s-lab-winning-solution/115656#post115656","thumbnailUrl":null},{"title":"being smart about loading data","date":"2016-02-03T02:35:31.59Z","medal":"bronze","score":4,"scoreOutOf":0,"url":"/c/cervical-cancer-screening/forums/t/18693/being-smart-about-loading-data/106663#post106663","thumbnailUrl":null}],"summaryType":"discussion"},"achievement":null,"pageMessages":[]}), document.getElementById("react-ProfileContainerReact-1"));'
  data= json.loads(re.findall('KaggleReactComponents.ProfileContainerReact,(.*)\), document',content)[0])
  return data

def get_user():
  head = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.130 Safari/537.36'
}
  f=open("kaggle_user.csv","a")
  for i in range(530,1000):
   url="https://www.kaggle.com/rankings.json?sortBy=null&page=%d&group=competitions"%(i)
   time.sleep(2)
   data=json.loads(requests.get(url,headers=head).content)
   for user in data.get("list"):
       print user
       url=user.get("userUrl")
       try :
        main_data=getmainpage(url)
        print dict(user, **main_data)
        f.write(json.dumps(dict(user, **main_data))+"\n")
       except Exception as e:
         print e

  f.close()
if __name__ == '__main__':
     get_user()




