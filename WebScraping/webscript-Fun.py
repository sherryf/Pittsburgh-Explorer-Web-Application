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

        temp['category'] = "Fun & Games"

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

        temp['geocode'] = geocode_result[0]['geometry']['location']
        temp['lat'] = geocode_result[0]['geometry']['location']['lat']
        temp['lng'] = geocode_result[0]['geometry']['location']['lng']

        try:
            temp['rate'] = soup.find_all("span", class_="rate sprite-rating_rr rating_rr")[0].img['content']
        except IndexError:
            temp['rate'] = "no rate"

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
    links = {"https://www.tripadvisor.com/Attraction_Review-g53449-d7248286-Reviews-Escape_Room_Pittsburgh-Pittsburgh_Pennsylvania.html",
            "https://www.tripadvisor.com/Attraction_Review-g53449-d10454939-Reviews-The_Great_Escape_Room-Pittsburgh_Pennsylvania.html",
            "https://www.tripadvisor.com/Attraction_Review-g53449-d10721826-Reviews-Questburgh-Pittsburgh_Pennsylvania.html",
            "https://www.tripadvisor.com/Attraction_Review-g53449-d8522207-Reviews-Escape_the_Room_PA-Pittsburgh_Pennsylvania.html",
            "https://www.tripadvisor.com/Attraction_Review-g53449-d2212884-Reviews-Rivers_Casino-Pittsburgh_Pennsylvania.html",
            "https://www.tripadvisor.com/Attraction_Review-g53449-d11760522-Reviews-The_Haunted_Dollhouse-Pittsburgh_Pennsylvania.html",
            "https://www.tripadvisor.com/Attraction_Review-g53449-d8791531-Reviews-Daring_Escapes-Pittsburgh_Pennsylvania.html",
            "https://www.tripadvisor.com/Attraction_Review-g53449-d7212358-Reviews-Arcade_Comedy_Theater-Pittsburgh_Pennsylvania.html",
            "https://www.tripadvisor.com/Attraction_Review-g53449-d8447756-Reviews-Painting_with_a_Twist-Pittsburgh_Pennsylvania.html",
            "https://www.tripadvisor.com/Attraction_Review-g53449-d7797977-Reviews-The_John_M_and_Gertrude_E_Petersen_Events_Center-Pittsburgh_Pennsylvania.html",
            "https://www.tripadvisor.com/Attraction_Review-g53449-d5975736-Reviews-Southside_Works_Cinema-Pittsburgh_Pennsylvania.html",
            "https://www.tripadvisor.com/Attraction_Review-g53449-d8639480-Reviews-Rex_Theater-Pittsburgh_Pennsylvania.html",
            "https://www.tripadvisor.com/Attraction_Review-g53449-d12012459-Reviews-Zone_28-Pittsburgh_Pennsylvania.html",
            "https://www.tripadvisor.com/Attraction_Review-g53449-d7379228-Reviews-Arsenal_Bowl-Pittsburgh_Pennsylvania.html",
            "https://www.tripadvisor.com/Attraction_Review-g53449-d11636235-Reviews-Mystery_Key_Escape_Room-Pittsburgh_Pennsylvania.html",
            "https://www.tripadvisor.com/Attraction_Review-g53449-d12188624-Reviews-Colony_Cafe-Pittsburgh_Pennsylvania.html",
            "https://www.tripadvisor.com/Attraction_Review-g53449-d12098333-Reviews-Main_Event_Entertainment-Pittsburgh_Pennsylvania.html",
            "https://www.tripadvisor.com/Attraction_Review-g53449-d10513323-Reviews-The_Dinner_Detective-Pittsburgh_Pennsylvania.html"
    }
    collectInfo(links, gmaps)
    writetocsv()


if __name__ == "__main__":
    main()