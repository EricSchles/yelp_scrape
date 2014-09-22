import grequests
import lxml.html
import unidecode

#set up

base_url = "http://www.yelp.com/search?find_desc=chain+restaurants&find_loc=New+York%2C+NY#"

#iterate

urls =[]
for i in xrange(10,110,10):
    urls.append(base_url+"start="+str(i))

rs = (grequests.get(u) for u in urls)

#grab
responses = grequests.map(rs)

all_links = []
for r in responses:
    html = lxml.html.fromstring(r.text)
    links = html.xpath("//a")
    biz_links = []
    for link in links:
        if len(link.values()) >= 2:
            if "/biz/" in link.values()[1]:
                name = link.text_content()
                url = link.values()[1]
                biz_links.append([name,url])
    all_links += biz_links

data = []
for link in all_links:
    url = "http://www.yelp.com"+link[1]
    name = link[0].encode("ascii","ignore")
    data.append([name,url])

with open("chains.csv","w") as f:
    f.write("name,url\n")
    for datum in data:
        f.write(datum[0]+","+datum[1]+"\n")


        
