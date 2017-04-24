# impact package
import requests
from bs4 import BeautifulSoup
from tidylib import tidy_document
import json
import googlemaps
import csv

record = []


def collectInfo(links, gmaps):
    info = []
    for l in links:
        temp = {}

        temp['category'] = "Nights"

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

        temp['geocode'] = geocode_result[0]['geometry']['location']
        temp['lat'] = geocode_result[0]['geometry']['location']['lat']
        temp['lng'] = geocode_result[0]['geometry']['location']['lng']
        try:
            temp['rate'] = soup.find_all("span", class_="rate sprite-rating_rr rating_rr")[0].img['content']
        except IndexError:
            temp['rate'] = "no rate"
        except IndexError:
            temp['isimage'] = "No"

        try:
            if soup.find_all("div", class_="details_wrapper")[0].get_text().strip().startswith(
                    "Recommended length of visit"):
                temp['Recommended length of visit'] = soup.find_all("div", class_="details_wrapper")[
                                                          0].get_text().strip('\n')[28:].strip().encode("utf8")
            else:
                temp['Recommended length of visit'] = "no info"
        except IndexError:
            temp['Recommended length of visit'] = "no info"

        try:
            # import pdb; pdb.set_trace()
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
    links = {
    "https://www.tripadvisor.com/Attraction_Review-g53449-d7097692-Reviews-Grist_House_Brewery-Pittsburgh_Pennsylvania.html",
"https://www.tripadvisor.com/Attraction_Review-g53449-d6701414-Reviews-Wigle_Whiskey_Garden_and_Barrel_House-Pittsburgh_Pennsylvania.html",
"https://www.tripadvisor.com/Attraction_Review-g53449-d4558019-Reviews-Arsenal_Cider_House_Wine_Cellar-Pittsburgh_Pennsylvania.html",
"https://www.tripadvisor.com/Attraction_Review-g53449-d8567972-Reviews-Pittsburgh_Party_Pedaler-Pittsburgh_Pennsylvania.html",
"https://www.tripadvisor.com/Attraction_Review-g53449-d8646494-Reviews-Howl_at_the_moon-Pittsburgh_Pennsylvania.html",
"https://www.tripadvisor.com/Attraction_Review-g53449-d5847536-Reviews-Butterjoint-Pittsburgh_Pennsylvania.html",
"https://www.tripadvisor.com/Attraction_Review-g53449-d8126775-Reviews-Hard_Rock_Cafe_Pittsburgh-Pittsburgh_Pennsylvania.html",
"https://www.tripadvisor.com/Attraction_Review-g53449-d6750924-Reviews-Roundabout_Brewery-Pittsburgh_Pennsylvania.html",
"https://www.tripadvisor.com/Attraction_Review-g53449-d3381871-Reviews-Altar_Bar-Pittsburgh_Pennsylvania.html",
"https://www.tripadvisor.com/Attraction_Review-g53449-d6198075-Reviews-Jack_s_Bar_Southside-Pittsburgh_Pennsylvania.html",
"https://www.tripadvisor.com/Attraction_Review-g53449-d8077766-Reviews-Maggie_s_Farm_Rum_Distillery-Pittsburgh_Pennsylvania.html",
"https://www.tripadvisor.com/Attraction_Review-g53449-d5845551-Reviews-Club_Cafe-Pittsburgh_Pennsylvania.html",
"https://www.tripadvisor.com/Attraction_Review-g53449-d4263780-Reviews-OTB_Bicylce_Cafe-Pittsburgh_Pennsylvania.html",
"https://www.tripadvisor.com/Attraction_Review-g53449-d7212358-Reviews-Arcade_Comedy_Theater-Pittsburgh_Pennsylvania.html",
"https://www.tripadvisor.com/Attraction_Review-g53449-d5841845-Reviews-Blue_Dust-Pittsburgh_Pennsylvania.html",
"https://www.tripadvisor.com/Attraction_Review-g53449-d6199152-Reviews-Tiki_Lounge-Pittsburgh_Pennsylvania.html",
"https://www.tripadvisor.com/Attraction_Review-g53449-d5830407-Reviews-Fox_and_Hound_Pittsburgh-Pittsburgh_Pennsylvania.html",
"https://www.tripadvisor.com/Attraction_Review-g53449-d5841244-Reviews-All_Star_Sports_Bar_Grill-Pittsburgh_Pennsylvania.html",
"https://www.tripadvisor.com/Attraction_Review-g53449-d5836980-Reviews-Jamison_s_On_West_Liberty-Pittsburgh_Pennsylvania.html",
"https://www.tripadvisor.com/Attraction_Review-g53449-d5835286-Reviews-Mario_s_East_Side_Saloon-Pittsburgh_Pennsylvania.html",
"https://www.tripadvisor.com/Attraction_Review-g53449-d5845128-Reviews-The_Monkey_Bar_Pittsburgh-Pittsburgh_Pennsylvania.html",
"https://www.tripadvisor.com/Attraction_Review-g53449-d5842504-Reviews-The_Smiling_Moose-Pittsburgh_Pennsylvania.html",
"https://www.tripadvisor.com/Attraction_Review-g53449-d8639480-Reviews-Rex_Theater-Pittsburgh_Pennsylvania.html",
"https://www.tripadvisor.com/Attraction_Review-g53449-d5845372-Reviews-Bobby_s_Lounge-Pittsburgh_Pennsylvania.html",
"https://www.tripadvisor.com/Attraction_Review-g53449-d274092-Reviews-Gooski_s-Pittsburgh_Pennsylvania.html",
"https://www.tripadvisor.com/Attraction_Review-g53449-d5845601-Reviews-The_Library_Pittsburgh-Pittsburgh_Pennsylvania.html",
"https://www.tripadvisor.com/Attraction_Review-g53449-d5845585-Reviews-Local_Bar_Kitchen-Pittsburgh_Pennsylvania.html",
"https://www.tripadvisor.com/Attraction_Review-g53449-d5841857-Reviews-Skybar_Pittsburgh-Pittsburgh_Pennsylvania.html",
"https://www.tripadvisor.com/Attraction_Review-g53449-d5831033-Reviews-Doubledays_Burgers-Pittsburgh_Pennsylvania.html",
"https://www.tripadvisor.com/Attraction_Review-g53449-d6197637-Reviews-The_Allegheny_Wine_Mixer_Inc-Pittsburgh_Pennsylvania.html"

    }

    collectInfo(links, gmaps)
    writetocsv()


if __name__ == "__main__":
    main()
