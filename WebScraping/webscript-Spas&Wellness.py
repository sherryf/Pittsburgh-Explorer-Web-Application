
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

        temp['category'] = "Spas"


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
    links = {"https://www.tripadvisor.com/Attraction_Review-g53449-d4834136-Reviews-Esspa_Kozmetika_Organic_Skincare-Pittsburgh_Pennsylvania.html",
"https://www.tripadvisor.com/Attraction_Review-g53449-d1569929-Reviews-Spa_Jema-Pittsburgh_Pennsylvania.html",
"https://www.tripadvisor.com/Attraction_Review-g53449-d7070901-Reviews-Evolve_Wellness_Spa-Pittsburgh_Pennsylvania.html",
"https://www.tripadvisor.com/Attraction_Review-g53449-d3396840-Reviews-Massage_Envy-Pittsburgh_Pennsylvania.html",
"https://www.tripadvisor.com/Attraction_Review-g53449-d6692196-Reviews-Massage_Heights-Pittsburgh_Pennsylvania.html",
"https://www.tripadvisor.com/Attraction_Review-g53449-d6429208-Reviews-Peace_Love_Zen-Pittsburgh_Pennsylvania.html",
"https://www.tripadvisor.com/Attraction_Review-g53449-d3440474-Reviews-LaVida_Massage_of_Shadyside-Pittsburgh_Pennsylvania.html",
"https://www.tripadvisor.com/Attraction_Review-g53449-d11948782-Reviews-Centre_Ave_Massage_Spa-Pittsburgh_Pennsylvania.html",
"https://www.tripadvisor.com/Attraction_Review-g53449-d8671577-Reviews-Happy_Feet_Relexology-Pittsburgh_Pennsylvania.html",
"https://www.tripadvisor.com/Attraction_Review-g53449-d12146911-Reviews-Pure_Skin_Care_Center_Beauty_Lounge-Pittsburgh_Pennsylvania.html",
"https://www.tripadvisor.com/Attraction_Review-g53449-d12104911-Reviews-Evolve_Massage_and_Wellness_Center-Pittsburgh_Pennsylvania.html",
"https://www.tripadvisor.com/Attraction_Review-g53449-d4493438-Reviews-Golden_Fingers_Spa-Pittsburgh_Pennsylvania.html",
"https://www.tripadvisor.com/Attraction_Review-g53449-d11929715-Reviews-Verve_360-Pittsburgh_Pennsylvania.html",
"https://www.tripadvisor.com/Attraction_Review-g53449-d9559803-Reviews-Glo_Skincare_Studio_Day_Spa-Pittsburgh_Pennsylvania.html",
"https://www.tripadvisor.com/Attraction_Review-g53449-d8762213-Reviews-Amazing_Yoga-Pittsburgh_Pennsylvania.html",
"https://www.tripadvisor.com/Attraction_Review-g53449-d4502486-Reviews-Rdlfitness-Pittsburgh_Pennsylvania.html"}
    collectInfo(links,gmaps)
    writetocsv()



if __name__ == "__main__":
    main()