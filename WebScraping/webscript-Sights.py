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

        temp['category'] = "Sights"

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
        "https://www.tripadvisor.com/Attraction_Review-g53449-d272117-Reviews-PNC_Park-Pittsburgh_Pennsylvania.html",
        "https://www.tripadvisor.com/Attraction_Review-g53449-d209225-Reviews-Phipps_Conservatory-Pittsburgh_Pennsylvania.html",
        "https://www.tripadvisor.com/Attraction_Review-g53449-d272285-Reviews-Mount_Washington-Pittsburgh_Pennsylvania.html",
        "https://www.tripadvisor.com/Attraction_Review-g53449-d272116-Reviews-Heinz_Field-Pittsburgh_Pennsylvania.html",
        "https://www.tripadvisor.com/Attraction_Review-g53449-d220084-Reviews-The_Strip_District-Pittsburgh_Pennsylvania.html",
        "https://www.tripadvisor.com/Attraction_Review-g53449-d2689690-Reviews-PPG_Paints_Arena-Pittsburgh_Pennsylvania.html",
        "https://www.tripadvisor.com/Attraction_Review-g53449-d258386-Reviews-Point_State_Park-Pittsburgh_Pennsylvania.html",
        "https://www.tripadvisor.com/Attraction_Review-g53449-d272372-Reviews-Monongahela_Incline-Pittsburgh_Pennsylvania.html",
        "https://www.tripadvisor.com/Attraction_Review-g53449-d668029-Reviews-Roberto_Clemente_Bridge_Sixth_Street_Bridge-Pittsburgh_Pennsylvania.html",
        "https://www.tripadvisor.com/Attraction_Review-g53449-d3793029-Reviews-Market_Square-Pittsburgh_Pennsylvania.html",
        "https://www.tripadvisor.com/Attraction_Review-g53449-d1383642-Reviews-Heinz_Memorial_Chapel-Pittsburgh_Pennsylvania.html",
        "https://www.tripadvisor.com/Attraction_Review-g53449-d527273-Reviews-University_of_Pittsburgh-Pittsburgh_Pennsylvania.html",
        "https://www.tripadvisor.com/Attraction_Review-g53449-d532081-Reviews-PPG_Place-Pittsburgh_Pennsylvania.html",
        "https://www.tripadvisor.com/Attraction_Review-g53449-d272375-Reviews-South_Side-Pittsburgh_Pennsylvania.html",
        "https://www.tripadvisor.com/Attraction_Review-g53449-d294409-Reviews-USS_Requin-Pittsburgh_Pennsylvania.html",
        "https://www.tripadvisor.com/Attraction_Review-g53449-d2173285-Reviews-Saint_Anthony_Chapel-Pittsburgh_Pennsylvania.html",
        "https://www.tripadvisor.com/Attraction_Review-g53449-d4701662-Reviews-Carnegie_Mellon_University-Pittsburgh_Pennsylvania.html",
        "https://www.tripadvisor.com/Attraction_Review-g53449-d272387-Reviews-Shadyside-Pittsburgh_Pennsylvania.html",
        "https://www.tripadvisor.com/Attraction_Review-g53449-d272386-Reviews-Allegheny_Cemetery-Pittsburgh_Pennsylvania.html",
        "https://www.tripadvisor.com/Attraction_Review-g53449-d7043545-Reviews-Sri_Venkateswara_Temple-Pittsburgh_Pennsylvania.html",
        "https://www.tripadvisor.com/Attraction_Review-g53449-d4045967-Reviews-Fort_Pitt_Block_House-Pittsburgh_Pennsylvania.html",
        "https://www.tripadvisor.com/Attraction_Review-g53449-d3398395-Reviews-Stage_AE-Pittsburgh_Pennsylvania.html",
        "https://www.tripadvisor.com/Attraction_Review-g53449-d272388-Reviews-Squirrel_Hill-Pittsburgh_Pennsylvania.html",
        "https://www.tripadvisor.com/Attraction_Review-g53449-d3474630-Reviews-Pittsburgh_Water_Steps-Pittsburgh_Pennsylvania.html",
        "https://www.tripadvisor.com/Attraction_Review-g53449-d4112198-Reviews-Mr_Rogers_Memorial_Statue-Pittsburgh_Pennsylvania.html",
        "https://www.tripadvisor.com/Attraction_Review-g53449-d7798879-Reviews-St_Paul_Cathedral-Pittsburgh_Pennsylvania.html",
        "https://www.tripadvisor.com/Attraction_Review-g53449-d2253864-Reviews-Homewood_Cemetery-Pittsburgh_Pennsylvania.html",
        "https://www.tripadvisor.com/Attraction_Review-g53449-d531836-Reviews-Allegheny_County_Courthouse-Pittsburgh_Pennsylvania.html",
        "https://www.tripadvisor.com/Attraction_Review-g53449-d294371-Reviews-Forbes_Field-Pittsburgh_Pennsylvania.html",
        "https://www.tripadvisor.com/Attraction_Review-g53449-d4131516-Reviews-Highmark_Stadium-Pittsburgh_Pennsylvania.html"
    }

    collectInfo(links, gmaps)
    writetocsv()


if __name__ == "__main__":
    main()
