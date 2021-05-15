
# TODO:add functionality
# shop number and quality
# government and guards
# religion and stuff
# name generator
# tavern generator
# npc generator

import time
import random
import string
import numpy
import uuid
import xml.etree.ElementTree as ElementTree



firefoxbinary = "/usr/lib/firefox/firefox"
geckodriverpath = '/home/loathengine/PycharmProjects/fantasy_settlement_generator/web/driver/'

#randomseed = random.randint(10000000, 99999999)


randomseed = 37433863
uuid = str(uuid.uuid4())
random.seed(uuid)


def weighted_element_list(xml_file, element_root):
    """Takes a file and an element name and returns a weighted random result"""
    tree = ElementTree.parse(xml_file)
    root = tree.getroot()
    weighted_list = []
    for e in root.findall(element_root):
        name = e.get('name')
        weight = e.get('weight')
        description = e.get('desc')
        i = int(weight)
        while i > 0:
            weighted_list.append([name, weight, description])
            i -= 1
    return random.choice(weighted_list)


def all_unique_element_dict(xml_file, element_root):
    """Takes a file and an element name and returns a dict of every unique instance of that element."""
    """Format: key, [weight, description]"""
    tree = ElementTree.parse(xml_file)
    root = tree.getroot()
    dictionary = {}
    for e in root.findall(element_root):
        name = e.get('name')
        weight = e.get('weight')
        description = e.get('desc')
        dictionary[name] = [weight, description]
    return dictionary


def count_unique_element_dict(xml_file, element_root, count):
    """Takes a file and an element name and a count and returns a unique dict of size count of that element."""
    dictionary = {}
    while count > 0:
        results = weighted_element_list(xml_file, element_root)
        if results[0] not in dictionary:
            dictionary[results[0]] = [results[1], results[2]]
            count -= 1
    return dictionary


def all_unique_element_list(xml_file, element, attribute):
    """Takes a file and an element name and returns a list of every unique instance of that element."""
    tree = ElementTree.parse(xml_file)
    root = tree.getroot()
    xml_list = []
    for e in root.iter(element):
        xml_list.append(e.get(attribute))
    xml_set = set(xml_list)
    unique_xml_list = list(xml_set)
    return unique_xml_list


def count_unique_element_list(xml_file, element, attribute, count):
    """Takes a file and an element name and returns a unique list of or size count for that element."""
    tree = ElementTree.parse(xml_file)
    root = tree.getroot()
    xml_list = []
    for e in root.iter(element):
        xml_list.append(e.get(attribute))
    xml_set = set(xml_list)
    unique_xml_list = list(xml_set)
    return random.sample(unique_xml_list, count)


def get_settlement_shops(xml_file, element_root, ssn):
    shop_dict = {}
    while ssn > 0:
        ssn -= 1
        shop_results = weighted_element_list(xml_file, element_root)
        if shop_results[0] in shop_dict:
            shop_dict[shop_results[0]] += 1
        else:
            shop_dict[shop_results[0]] = 1
    return shop_dict


def get_settlement_label(xml_file, element_root, settlement_pop):
    # TODO: Need to sort data before doing the size checks
    tree = ElementTree.parse(xml_file)
    root = tree.getroot()
    settlement_list = ""
    for e in root.findall(element_root):
        name = e.get('name')
        ceiling = e.get('ceiling')
        i = int(ceiling)
        if i < settlement_pop:
            settlement_list = name
    return settlement_list


def npc_generator():
    npc_names = weighted_element_list(xml_file_path, "./STATS/NPC_NAMES")
    return npc_names[0]


def get_settlement_tavern(t_n, t_l):
    # TODO: Name=settlement_tavern_name, Location=district_info, Description, Innkeeper, Menu, Patrons
    xml_dict = {}
    for name in t_n:
        tavern_name = name
        tavern_location = random.choice(list(t_l))
        tavern_description = weighted_element_list('data/monolith.xml', "./STATS/TAVERN_DESC")
        tavern_innkeeper = npc_generator()
        tavern_menu = list(count_unique_element_dict('data/monolith.xml', "./STATS/TAVERN_MENU", 5))
        xml_dict[tavern_name] = [tavern_location, tavern_description[0], tavern_innkeeper, tavern_menu[0],
                                 tavern_menu[1], tavern_menu[2], tavern_menu[3], tavern_menu[4]]
    return xml_dict

def web_get_city(size, seed, name):
    from selenium import webdriver
    from selenium.webdriver.firefox.options import Options
    from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
    options = Options()
    options.binary = FirefoxBinary('web/browser/firefox/firefox')
    options.headless = True
    driver = webdriver.Firefox(executable_path='web/driver/geckodriver', options=options)
    driver.set_window_position(0, 0)
    driver.set_window_size(1024, 1098)
    driver.get('http://0.0.0.0:8000/MFCG.html?size=' + str(size) + '&seed=' + str(seed) + '&name=' + name)
    print("Headless Firefox Initialized")
    time.sleep(8)
    screenshot = driver.save_screenshot('web/cities/' + str(seed) + '.png')
    driver.get("http://google.com/")
    driver.quit()
#    driver.get('http://fantasycities.watabou.ru/?size=' + str(size) + '&seed=' + str(seed) + '&name=' + name)


def write_web_page(webout, seed):
    filename = "web/cities/" + seed + ".html"
    file = open(filename, "w")
    file.writelines(webout)
    file.close()


xml_file_path = 'data/monolith.xml'


settlement_env = weighted_element_list(xml_file_path, "./ENV")
settlement_env_biome = weighted_element_list(xml_file_path, "./ENV/BIOME")
settlement_env_biome_topography = weighted_element_list(xml_file_path, "./ENV/BIOME[@name='" +
                                                        settlement_env_biome[0] + "']/TOPOGRAPHY")
settlement_env_biome_topography_raw = weighted_element_list(xml_file_path, "./ENV/BIOME[@name='" +
                                                            settlement_env_biome[0] + "']/TOPOGRAPHY[@name='" +
                                                            settlement_env_biome_topography[0] + "']/RAW")

env_biome_topo_raw = "./ENV/BIOME[@name='" + settlement_env_biome[0] + "']/TOPOGRAPHY[@name='" + \
                     settlement_env_biome_topography[0] + "']/RAW[@name='" + \
                     settlement_env_biome_topography_raw[0] + "']"



settlement_population = int(abs(numpy.random.normal(loc = 0, scale = 5000)))
settlement_shops_num = 1 + (settlement_population // 1500)
settlement_shops = get_settlement_shops(xml_file_path, env_biome_topo_raw + "/SHOP", settlement_shops_num)
settlement_district_number = 1 + (settlement_population // 1000)
settlement_wards = 6 + settlement_population // 100
settlement_tavern_num = (2 + settlement_population // 500)



settlement_density = weighted_element_list(xml_file_path, "./STATS/DENSITY")[2]
settlement_district_info = count_unique_element_dict(xml_file_path, env_biome_topo_raw + "/DISTRICT", settlement_district_number)
settlement_name = weighted_element_list(xml_file_path, "./STATS/SETTLEMENT_NAME")[0]
settlement_label = get_settlement_label(xml_file_path, "./STATS/LABEL", settlement_population)
settlement_wealth = weighted_element_list(xml_file_path, "./STATS/WEALTH")
settlement_age = weighted_element_list(xml_file_path, "./STATS/AGE")
background_flavor = weighted_element_list(xml_file_path, "./STATS/FLAVOR")[2]
settlement_alignment = weighted_element_list(xml_file_path, "./STATS/ALIGNMENT")
settlement_government = weighted_element_list(xml_file_path, "./STATS/GOVERNMENT")
settlement_trait = weighted_element_list(xml_file_path, "./STATS/TRAIT")
settlement_races = all_unique_element_dict(xml_file_path, "./STATS/RACE")
settlement_district_trait = count_unique_element_dict(xml_file_path, "./STATS/DISTRICT_TRAIT", settlement_district_number)
settlement_tavern_names = count_unique_element_dict(xml_file_path, "./STATS/TAVERN_NAME", settlement_tavern_num)
settlement_taverns = get_settlement_tavern(settlement_tavern_names, settlement_district_info)

settlement_features = (settlement_name + " is a " + settlement_label + " located in the " +
                       settlement_env_biome_topography[0] + " region of the areas " + "greater " +
                       settlement_env_biome[0] + ".  The settlement seems to be " +
                       settlement_age[0] + ".  " + settlement_name +
                       " and the local surroundings are under the control of " + settlement_government[0] + ".")

page_number = 0
page_iterator = 0
web_page = ""

web_page = web_page + '<!DOCTYPE html> \n'
web_page = web_page + '<!-- saved from url=(0065)https://homebrewery.naturalcrit.com/print?dialog=true&local=print --> \n'
web_page = web_page + '<html> \n'
web_page = web_page + '   <head> \n'
web_page = web_page + '      <meta http-equiv="Content-Type" content="text/html; charset=UTF-8"> \n'
web_page = web_page + '      <link href="../markup_files/font-awesome.min.css" rel="stylesheet"> \n'
web_page = web_page + '      <link href="../markup_files/css" rel="stylesheet" type="text/css"> \n'
web_page = web_page + '      <title>Fantasy Settlement Generator</title> \n'
web_page = web_page + '      <link rel="stylesheet" type="text/css" href="../markup_files/bundle.css"> \n'
web_page = web_page + '      <style class="crddr-fonts" type="text/css">@import url(https://fonts.googleapis.com/css?family=Bitter:bold);</style> \n'
web_page = web_page + '      <style class="crddr-fonts" type="text/css">@font-face {font-family: "Helvetica Neue For Number"; src: local("Helvetica Neue"); unicode-range: U+30-39; } \n'
web_page = web_page + "         @font-face {font-family: 'anticon'; src: url('https://at.alicdn.com/t/font_148784_v4ggb6wrjmkotj4i.eot'); /* IE9*/ src: url('https://at.alicdn.com/t/font_148784_v4ggb6wrjmkotj4i.eot?#iefix') format('embedded-opentype'), /* chrome, firefox */ url('https://at.alicdn.com/t/font_148784_v4ggb6wrjmkotj4i.woff') format('woff'), /* chrome, firefox, opera, Safari, Android, iOS 4.2+*/ url('https://at.alicdn.com/t/font_148784_v4ggb6wrjmkotj4i.ttf') format('truetype'), /* iOS 4.1- */ url('https://at.alicdn.com/t/font_148784_v4ggb6wrjmkotj4i.svg#iconfont') format('svg'); } /* \n"
web_page = web_page + "         @font-face {font-family: 'ReviewIcons'; src: local('ReviewIcons'), url('.../assets/ReviewIcons.woff') format('woff'); } */ \n"
web_page = web_page + '      </style> \n'
web_page = web_page + '   </head> \n'
web_page = web_page + '<body> \n'
web_page = web_page + '<main> \n'
web_page = web_page + '<div> \n'

# Page title

web_page = web_page + '<div class="phb" id="p1"> \n'
web_page = web_page + '<style> \n'
web_page = web_page + '.phb#p1{ text-align:center; } \n'
web_page = web_page + '.phb#p1:after{ display:none; } \n'
web_page = web_page + '</style> \n'
web_page = web_page + '<div style="margin-top:450px;">  </div> \n'
web_page = web_page + '<h1 id="' + settlement_name + '">' + settlement_name + ' </h1> \n'
web_page = web_page + '<div style="margin-top:25px"> \n'
web_page = web_page + '<p></p> \n'
web_page = web_page + '</div> \n'
web_page = web_page + '<p></p> \n'
web_page = web_page + '<p></p> \n'
web_page = web_page + '<div class="wide"> \n'
web_page = web_page + '<p></p> \n'
web_page = web_page + '<h5 id="a-mystical-settlement-in-a-fantastical-world">A mystical settlement in a fantastical world</h5> \n'
web_page = web_page + '</div> \n'
web_page = web_page + '</div> \n'

# Page one
page_number += 1
web_page = web_page + '<div class="phb" id="p2"> \n'
web_page = web_page + '<div class="wide"><p><img src="image.png" style="width:700px"></p></div> \n'
web_page = web_page + '<h3 id="background">Background Flavor</h3>'
web_page = web_page + '<p>' + background_flavor + '</p>'
web_page = web_page + '<div class="pageNumber"><p>' + str(
    page_number) + '</p></div><p></p><p></p><div class="footnote">PAGE ' + str(
    page_number) + '| ' + settlement_name + '<p></p></div>'
web_page = web_page + '</div> \n'

# Page two
page_number += 1
web_page = web_page + '<div class="phb" id="p3"> \n'
web_page = web_page + '<h2 id="settlement-features">Settlement Features</h2>'
web_page = web_page + '<p>' + settlement_features + '</p>'
web_page = web_page + '<h4 id="demographics">Demographics</h4>'
web_page = web_page + '<hr>'
web_page = web_page + '<ul>'
web_page = web_page + '<li><strong>Name: </strong>' + settlement_name + '</li>'
web_page = web_page + '<li><strong>Size: </strong>' + string.capwords(settlement_label) + '</li>'
web_page = web_page + '<li><strong>Real population: </strong>' + str(settlement_population) + '</li>'
web_page = web_page + '<li><strong>Population Density: </strong>' + str(settlement_density) + '</li>'
web_page = web_page + '<li><strong>Number by race: </strong>'
for x, y in settlement_races.items():
    web_page = web_page + string.capwords(x) + " " + y[0] + "%, "
web_page = web_page + '</li>'
web_page = web_page + '<li><strong>Wealth: </strong>' + str(settlement_wealth[2]) + '</li>'
web_page = web_page + '<li><strong>Age: </strong>' + string.capwords(settlement_age[0]) + '</li>'
web_page = web_page + '<li><strong>Alignment: </strong>' + str(settlement_alignment[2]) + '</li>'
web_page = web_page + "<li><strong>Government Type: </strong>" + string.capwords(settlement_government[0]) + " - " + \
           settlement_government[2] + "</li>"
web_page = web_page + '<li><strong>Settlement Trait: </strong>' + settlement_trait[0] + '</li>'
web_page = web_page + '<li><strong>Number Of Wards: </strong>' + str(settlement_wards) + '</li>'
web_page = web_page + '<li><strong>Number of Districts: </strong>' + str(settlement_district_number) + '</li>'
web_page = web_page + '</ul>'
web_page = web_page + '<h4 id="industry-and-economy">Industry and Economy</h4>'
web_page = web_page + '<hr>'
web_page = web_page + '<ul>'
web_page = web_page + '<li><strong>Primary Raw Materials: </strong>' + string.capwords(settlement_env_biome_topography_raw[0]) + '</li>'
web_page = web_page + '<li><strong>Shops of Note: </strong>'
for x in settlement_shops.keys():
    if x == list(settlement_shops.keys())[-1]:
        web_page = web_page + x + "."
    else:
        web_page = web_page + x + ", "
web_page = web_page + '</li>'
web_page = web_page + '<li><strong>Number Of Inns/Taverns: </strong>' + str(len(settlement_taverns)) + '</li>'
web_page = web_page + '<li><strong>Inns/Taverns of Note: </strong>'
for x in settlement_tavern_names.keys():
    if x == list(settlement_tavern_names.keys())[-1]:
        web_page = web_page + x + "."
    else:
        web_page = web_page + x + ", "
web_page = web_page + '</li>'
web_page = web_page + '</ul>'
web_page = web_page + '<h4 id="districts">Districts</h4>'
for x, y in zip(settlement_district_info.items(), settlement_district_trait.items()):
    web_page = web_page + '<h5 id="' + x[0] + '">' + x[0] + '</h5>'
    z = y[1]
    web_page = web_page + '<p>' + y[0] + ': ' + z[1] + '</p>'
web_page = web_page + '<h3 id="districts">Taverns / Inns</h3>'
for x, y in settlement_taverns.items():
    web_page = web_page + '<h2 id="' + x + '">' + x + '</h2>'
    web_page = web_page + '<h5 id="location">Location</h5>'
    web_page = web_page + '<p>' + y[0] + '</p>'
    web_page = web_page + '<h5 id="description">Description</h5>'
    web_page = web_page + '<p>' + y[1] + '</p>'
    web_page = web_page + '<h5 id="innkeeper">Innkeeper</h5>'
    web_page = web_page + '<p>' + y[2] + '</p>'
    web_page = web_page + '<h5 id="menu">Menu</h5>'
    web_page = web_page + '<ul>'
    web_page = web_page + '<li>' + y[3] + '</li>'
    web_page = web_page + '<li>' + y[4] + '</li>'
    web_page = web_page + '<li>' + y[5] + '</li>'
    web_page = web_page + '<li>' + y[6] + '</li>'
    web_page = web_page + '<li>' + y[7] + '</li>'
    web_page = web_page + '</ul>'
    web_page = web_page + '<hr>'
    page_iterator += 1
    if page_iterator == 3 or page_iterator == 9:
        web_page = web_page + '<div class="pageNumber"><p>' + str(
            page_number) + '</p></div><p></p><p></p><div class="footnote">PAGE ' + str(
            page_number) + '| ' + settlement_name + '<p></p></div>'
        web_page = web_page + '</div> \n'
        web_page = web_page + '<div class="phb" id="p4"> \n'
        page_number += 1

web_page = web_page + '<div class="pageNumber"><p>' + str(
    page_number) + '</p></div><p></p><p></p><div class="footnote">PAGE ' + str(
    page_number) + ' | ' + settlement_name + '<p></p></div>'
web_page = web_page + '</div>'
# footer
web_page = web_page + '</div></main></body></html>'

write_web_page(web_page, uuid)

#web_get_city(str(settlement_wards), str(randomseed), settlement_name)