
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

        temp['category'] = "Shopping"


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
    links = {"https://www.tripadvisor.com/Attraction_Review-g53449-d272371-Reviews-Station_Square-Pittsburgh_Pennsylvania.html",
"https://www.tripadvisor.com/Attraction_Review-g53449-d6450962-Reviews-Pennsylvania_Macaroni_Company-Pittsburgh_Pennsylvania.html",
"https://www.tripadvisor.com/Attraction_Review-g53449-d2561564-Reviews-Pittsburgh_Public_Market_in_the_Strip-Pittsburgh_Pennsylvania.html",
"https://www.tripadvisor.com/Attraction_Review-g53449-d2484939-Reviews-The_Society_for_Contemporary_Craft-Pittsburgh_Pennsylvania.html",
"https://www.tripadvisor.com/Attraction_Review-g53449-d2643393-Reviews-Pittsburgh_Glass_Center_Studios-Pittsburgh_Pennsylvania.html",
"https://www.tripadvisor.com/Attraction_Review-g53449-d1592770-Reviews-ToonSeum-Pittsburgh_Pennsylvania.html",
"https://www.tripadvisor.com/Attraction_Review-g53449-d2484891-Reviews-Pittsburgh_Center_for_the_Arts-Pittsburgh_Pennsylvania.html",
"https://www.tripadvisor.com/Attraction_Review-g53449-d7907980-Reviews-Larrimor_s-Pittsburgh_Pennsylvania.html",
"https://www.tripadvisor.com/Attraction_Review-g53449-d3511440-Reviews-Artifacts-Pittsburgh_Pennsylvania.html",
"https://www.tripadvisor.com/Attraction_Review-g53449-d2422998-Reviews-James_Gallery-Pittsburgh_Pennsylvania.html",
"https://www.tripadvisor.com/Attraction_Review-g53449-d4306793-Reviews-Caliban_Book_Shop-Pittsburgh_Pennsylvania.html",
"https://www.tripadvisor.com/Attraction_Review-g53449-d7806619-Reviews-Grandpa_Joe_s_Candy_Shop-Pittsburgh_Pennsylvania.html",
"https://www.tripadvisor.com/Attraction_Review-g53449-d7762359-Reviews-Olive_Marlowe-Pittsburgh_Pennsylvania.html",
"https://www.tripadvisor.com/Attraction_Review-g53449-d2514612-Reviews-Wild_Card-Pittsburgh_Pennsylvania.html",
"https://www.tripadvisor.com/Attraction_Review-g53449-d9718758-Reviews-Hart_s-Pittsburgh_Pennsylvania.html",
"https://www.tripadvisor.com/Attraction_Review-g53449-d7705833-Reviews-House_of_the_Dead-Pittsburgh_Pennsylvania.html",
"https://www.tripadvisor.com/Attraction_Review-g53449-d8834020-Reviews-Four_Winds_Gallery-Pittsburgh_Pennsylvania.html",
"https://www.tripadvisor.com/Attraction_Review-g53449-d7984595-Reviews-Gallery_G_Glass-Pittsburgh_Pennsylvania.html",
"https://www.tripadvisor.com/Attraction_Review-g53449-d9800830-Reviews-Mahla_Co_Antiques-Pittsburgh_Pennsylvania.html",
"https://www.tripadvisor.com/Attraction_Review-g53449-d10547738-Reviews-The_Pittsburgh_Fan-Pittsburgh_Pennsylvania.html",
"https://www.tripadvisor.com/Attraction_Review-g53449-d10499868-Reviews-5th_Avenue_Place-Pittsburgh_Pennsylvania.html",
"https://www.tripadvisor.com/Attraction_Review-g53449-d7698083-Reviews-Gallerie_CHIZ-Pittsburgh_Pennsylvania.html",
"https://www.tripadvisor.com/Attraction_Review-g53449-d7594895-Reviews-Art_of_steel-Pittsburgh_Pennsylvania.html",
"https://www.tripadvisor.com/Attraction_Review-g53449-d11727525-Reviews-Candy_Cigar-Pittsburgh_Pennsylvania.html",
"https://www.tripadvisor.com/Attraction_Review-g53449-d11695884-Reviews-Classic_Lines_Books-Pittsburgh_Pennsylvania.html",
"https://www.tripadvisor.com/Attraction_Review-g53449-d12033471-Reviews-Lily_Val_Flagship_Store-Pittsburgh_Pennsylvania.html",
"https://www.tripadvisor.com/Attraction_Review-g53449-d10494072-Reviews-Neu_Kirche_Contemporary_Art_Center-Pittsburgh_Pennsylvania.html",
"https://www.tripadvisor.com/Attraction_Review-g53449-d274091-Reviews-Scrap_Metals-Pittsburgh_Pennsylvania.html"}
    collectInfo(links,gmaps)
    writetocsv()



if __name__ == "__main__":
    main()