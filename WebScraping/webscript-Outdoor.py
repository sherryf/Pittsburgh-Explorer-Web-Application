
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

        temp['category'] = "Outdoor"


        r = requests.get(l)  # use requests library to scrape the master website
        tidy, errors = tidy_document(r.text)

        soup = BeautifulSoup(tidy, 'html.parser')

        temp["name"] = soup.find("div", class_="heading_height").h1.text.strip()

        temp["imgae"] = ""
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
    links = {"https://www.tripadvisor.com/Attraction_Review-g53449-d272390-Reviews-National_Aviary-Pittsburgh_Pennsylvania.html",
"https://www.tripadvisor.com/Attraction_Review-g53449-d2169478-Reviews-Gateway_Clipper_Fleet-Pittsburgh_Pennsylvania.html",
"https://www.tripadvisor.com/Attraction_Review-g53449-d272389-Reviews-Pittsburgh_Zoo_PPG_Aquarium-Pittsburgh_Pennsylvania.html",
"https://www.tripadvisor.com/Attraction_Review-g53449-d667745-Reviews-Just_Ducky_Tours_Inc-Pittsburgh_Pennsylvania.html",
"https://www.tripadvisor.com/Attraction_Review-g53449-d5567751-Reviews-Golden_Triangle_Bike_Rental-Pittsburgh_Pennsylvania.html",
"https://www.tripadvisor.com/Attraction_Review-g53449-d7225296-Reviews-Pittsburgh_Water_Limo-Pittsburgh_Pennsylvania.html",
"https://www.tripadvisor.com/Attraction_Review-g53449-d8129753-Reviews-Bike_The_Burgh_Tours-Pittsburgh_Pennsylvania.html",
"https://www.tripadvisor.com/Attraction_Review-g53449-d2015137-Reviews-Bike_the_GAP_Bicycle_Tours-Pittsburgh_Pennsylvania.html",
"https://www.tripadvisor.com/Attraction_Review-g53449-d2258331-Reviews-SurfSUP_Adventures-Pittsburgh_Pennsylvania.html",
"https://www.tripadvisor.com/Attraction_Review-g53449-d1141639-Reviews-Kayak_Pittsburgh-Pittsburgh_Pennsylvania.html",
"https://www.tripadvisor.com/Attraction_Review-g53449-d2415268-Reviews-Three_Rivers_Heritage_Trail-Pittsburgh_Pennsylvania.html",
"https://www.tripadvisor.com/Attraction_Review-g53449-d8567972-Reviews-Pittsburgh_Party_Pedaler-Pittsburgh_Pennsylvania.html",
"https://www.tripadvisor.com/Attraction_Review-g53449-d519340-Reviews-Western_Pennsylvania_Sports_Museum-Pittsburgh_Pennsylvania.html",
"https://www.tripadvisor.com/Attraction_Review-g53449-d4328186-Reviews-The_Wheel_Mill-Pittsburgh_Pennsylvania.html",
"https://www.tripadvisor.com/Attraction_Review-g53449-d10826491-Reviews-Pittsburgh_Running_Tours-Pittsburgh_Pennsylvania.html",
"https://www.tripadvisor.com/Attraction_Review-g53449-d7676130-Reviews-Boat_Pittsburgh-Pittsburgh_Pennsylvania.html",
"https://www.tripadvisor.com/Attraction_Review-g53449-d4475396-Reviews-Pittsburgh_Riverhounds-Pittsburgh_Pennsylvania.html",
"https://www.tripadvisor.com/Attraction_Review-g53449-d10063302-Reviews-Nocturnal_Addiction_Bowfishing-Pittsburgh_Pennsylvania.html",
"https://www.tripadvisor.com/Attraction_Review-g53449-d8414234-Reviews-Rush_Hour_Boat_Charters-Pittsburgh_Pennsylvania.html",
"https://www.tripadvisor.com/Attraction_Review-g53449-d7093152-Reviews-Wake_Up_Pittsburgh-Pittsburgh_Pennsylvania.html",
"https://www.tripadvisor.com/Attraction_Review-g53449-d6991691-Reviews-Mellon_Green-Pittsburgh_Pennsylvania.html",
"https://www.tripadvisor.com/Attraction_Review-g53449-d8595365-Reviews-Pedal_Power_Tours-Pittsburgh_Pennsylvania.html",
"https://www.tripadvisor.com/Attraction_Review-g53449-d10168512-Reviews-Surf_Pittsburgh-Pittsburgh_Pennsylvania.html"}
    collectInfo(links,gmaps)
    writetocsv()



if __name__ == "__main__":
    main()