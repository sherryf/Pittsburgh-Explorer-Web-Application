
# impact package
import requests
from bs4 import BeautifulSoup
from tidylib import tidy_document
import json
import googlemaps
import csv

record=[]


def collectInfo(links, gmaps):
    info = []
    for l in links:
        temp = {}

        temp['category'] = "Parks"


        r = requests.get(l)  # use requests library to scrape the master website
        tidy, errors = tidy_document(r.text)

        soup = BeautifulSoup(tidy, 'html.parser')

        temp["name"] = soup.find("div", class_="heading_height").h1.text.strip()

        for scr in list(soup.findAll('script')):
            if "lazyImgs" in scr.string:
                index = scr.string.find("{")
                new = scr.string[index:].split("\n    ,   ")
                for e in new:
                    if "HERO_PHOTO" in e:
                        ustr_to_load = unicode(e)
                        temp["imgae"] = json.loads(ustr_to_load)['data']
                        break
                break

        address = soup.find_all("span", class_="format_address")[0]
        temp['address'] = address.get_text()[9:]
        geocode_result = gmaps.geocode(address.get_text()[9:])

        try:
            temp['geocode'] = geocode_result[0]['geometry']['location']
            temp['lat'] = geocode_result[0]['geometry']['location']['lat']
            temp['lng'] = geocode_result[0]['geometry']['location']['lng']
        except IndexError:
            temp['geocode'] = ""
            temp['lat'] =""
            temp['lng'] =""


        try:
            temp['rate'] = soup.find_all("span", class_="rate sprite-rating_rr rating_rr")[0].img['content']
        except IndexError:
            temp['rate'] = "no rate"

        try:
            if soup.find_all("div", class_="details_wrapper")[0].get_text().strip().startswith(
                "Recommended length of visit"):
                temp['Recommended length of visit'] = soup.find_all("div", class_="details_wrapper")[0].get_text().strip('\n')[28:].strip().encode("utf8")
            else:
                temp['Recommended length of visit'] = "no info"
        except IndexError:
            temp['Recommended length of visit'] = "no info"

        try:
            #import pdb; pdb.set_trace()
            temp['detail'] = soup.find_all("div", class_="listing_details")[0].get_text().strip().encode("utf8")
        except IndexError:
            try:
                temp['detail'] = soup.find_all("div", class_="details_wrapper")[0].get_text().encode("utf8").rstrip()
            except IndexError:
                temp['detail'] = "no info"

        print temp
        record.append(temp)


def writetocsv():
    keys = record[0].keys()
    print(keys)
    with open('Attractions.csv', 'a') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(record)

def main():
    print("start")
    gmaps = googlemaps.Client(key='AIzaSyAn-6XiiENx0RGqGcI8_BjKzTUUQAiI7T8')
    links = {"https://www.tripadvisor.com/Attraction_Review-g53449-d209225-Reviews-Phipps_Conservatory-Pittsburgh_Pennsylvania.html",
"https://www.tripadvisor.com/Attraction_Review-g53449-d272285-Reviews-Mount_Washington-Pittsburgh_Pennsylvania.html",
"https://www.tripadvisor.com/Attraction_Review-g53449-d272390-Reviews-National_Aviary-Pittsburgh_Pennsylvania.html",
"https://www.tripadvisor.com/Attraction_Review-g53449-d258386-Reviews-Point_State_Park-Pittsburgh_Pennsylvania.html",
"https://www.tripadvisor.com/Attraction_Review-g53449-d272389-Reviews-Pittsburgh_Zoo_PPG_Aquarium-Pittsburgh_Pennsylvania.html",
"https://www.tripadvisor.com/Attraction_Review-g53449-d531834-Reviews-Schenley_Park-Pittsburgh_Pennsylvania.html",
"https://www.tripadvisor.com/Attraction_Review-g53449-d2233179-Reviews-Frick_Park-Pittsburgh_Pennsylvania.html",
"https://www.tripadvisor.com/Attraction_Review-g53449-d6540931-Reviews-West_End_Elliot_Overlook_Park-Pittsburgh_Pennsylvania.html",
"https://www.tripadvisor.com/Attraction_Review-g53449-d2415268-Reviews-Three_Rivers_Heritage_Trail-Pittsburgh_Pennsylvania.html",
"https://www.tripadvisor.com/Attraction_Review-g53449-d10941111-Reviews-August_Wilson_Park-Pittsburgh_Pennsylvania.html",
"https://www.tripadvisor.com/Attraction_Review-g53449-d11890982-Reviews-Emerald_View_Park-Pittsburgh_Pennsylvania.html"}
    collectInfo(links,gmaps)
    writetocsv()



if __name__ == "__main__":
    main()