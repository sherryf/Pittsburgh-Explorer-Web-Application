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

        temp['category'] = "Workshops"

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
    links = {
    "https://www.tripadvisor.com/Attraction_Review-g53449-d3438093-Reviews-Copper_Kettle_Brewing_Company-Pittsburgh_Pennsylvania.html",
    "https://www.tripadvisor.com/Attraction_Review-g53449-d7226985-Reviews-Painting_With_a_Twist_Pittsburgh_West-Pittsburgh_Pennsylvania.html",
    "https://www.tripadvisor.com/Attraction_Review-g53449-d519340-Reviews-Western_Pennsylvania_Sports_Museum-Pittsburgh_Pennsylvania.html",
    "https://www.tripadvisor.com/Attraction_Review-g53449-d8447756-Reviews-Painting_with_a_Twist-Pittsburgh_Pennsylvania.html",
    "https://www.tripadvisor.com/Attraction_Review-g53449-d4060360-Reviews-Paint_Monkey-Pittsburgh_Pennsylvania.html",
    "https://www.tripadvisor.com/Attraction_Review-g53449-d2547247-Reviews-Chop_WOK_Talk-Pittsburgh_Pennsylvania.html",
    "https://www.tripadvisor.com/Attraction_Review-g53449-d6784560-Reviews-Kiln_N_Time-Pittsburgh_Pennsylvania.html",
    "https://www.tripadvisor.com/Attraction_Review-g53449-d11837586-Reviews-Become_Better_Sport_Performance_and_Personal_Training-Pittsburgh_Pennsylvania.html",
    "https://www.tripadvisor.com/Attraction_Review-g53449-d10464261-Reviews-Steel_City_Fiber_Collective-Pittsburgh_Pennsylvania.html"
    }
    collectInfo(links, gmaps)
    writetocsv()


if __name__ == "__main__":
    main()