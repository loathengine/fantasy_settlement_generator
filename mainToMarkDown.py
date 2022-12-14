
# TODO:add functionality
# shop number and quality
# government and guards
# religion and stuff
# name generator
# tavern generator
# npc generator

import random
import string
import numpy
import uuid
import xml.etree.ElementTree as ElementTree

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

def write_mark_down(webout, seed):
    filename = "web/cities/" + seed + ".txt"
    file = open(filename, "w")
    file.writelines(webout)
    file.close()


# Path to xml file
xml_file_path = 'data/monolith.xml'

# Get highest level called env
settlement_env = weighted_element_list(xml_file_path, "./ENV")
# Get second level called biome
settlement_env_biome = weighted_element_list(xml_file_path, "./ENV/BIOME")
# Get third level called topography
settlement_env_biome_topography = weighted_element_list(xml_file_path, "./ENV/BIOME[@name='" +
                                                        settlement_env_biome[0] + "']/TOPOGRAPHY")
# Get fourth level for raw materials called raw
settlement_env_biome_topography_raw = weighted_element_list(xml_file_path, "./ENV/BIOME[@name='" +
                                                            settlement_env_biome[0] + "']/TOPOGRAPHY[@name='" +
                                                            settlement_env_biome_topography[0] + "']/RAW")

env_biome_topo_raw = "./ENV/BIOME[@name='" + settlement_env_biome[0] + "']/TOPOGRAPHY[@name='" + \
                     settlement_env_biome_topography[0] + "']/RAW[@name='" + \
                     settlement_env_biome_topography_raw[0] + "']"


settlement_population = int(abs(numpy.random.normal(loc=0, scale=5000)))
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


mark_down = ""


mark_down += '# ' + settlement_name + '\n'
mark_down += background_flavor + '\n\n\n'
mark_down += '### Settlement Features \n'
mark_down += settlement_features + '\n\n'
mark_down += '### Demographics \n'
mark_down += '**Name:** ::  ' + settlement_name + '\n'
mark_down += '**Size:** ::  ' + string.capwords(settlement_label) + '\n'
mark_down += '**Real population:** ::  ' + str(settlement_population) + '\n'
mark_down += '**Population Density:** ::  ' + str(settlement_density) + '\n'
mark_down += '**Number by race:** ::  '
for x, y in settlement_races.items():
    mark_down += string.capwords(x) + ' ' + y[0] + ', '
mark_down += '\n'
mark_down += '**Wealth:** ::  ' + str(settlement_wealth[2]) + '\n'
mark_down += '**Age:** ::' + string.capwords(settlement_age[0]) + '\n'
mark_down += '**Alignment:** ::' + str(settlement_alignment[2]) + '\n'
mark_down += '**Government Type:** ::' + string.capwords(settlement_government[0]) + ' - ' + settlement_government[2] + '\n'
mark_down += '**Settlement Trait:** ::' + settlement_trait[0] + '\n'
mark_down += '**Number Of Wards:** ::' + str(settlement_wards) + '\n'
mark_down += '**Number of Districts:** ::' + str(settlement_district_number) + '\n\n'
mark_down += '### Industry and Economy \n'
mark_down += '**Primary Raw Materials:** ::' + string.capwords(settlement_env_biome_topography_raw[0]) + '\n'
mark_down += '**Shops of Note:** ::'
for x in settlement_shops.keys():
    if x == list(settlement_shops.keys())[-1]:
        mark_down += x + "."
    else:
        mark_down += x + ", "
mark_down += '\n'
mark_down += '**Number of Inns/Taverns:** ::' + str(len(settlement_taverns)) + '\n'
mark_down += '**Inns/Taverns of Note:** ::'
for x in settlement_tavern_names.keys():
    if x == list(settlement_tavern_names.keys())[-1]:
        mark_down += x + "."
    else:
        mark_down += x + ", "
mark_down += '\n\n'
mark_down += '### Districts \n'
for x, y in zip(settlement_district_info.items(), settlement_district_trait.items()):
    mark_down += '**' + x[0] + '** ::'
    z = y[1]
    mark_down += y[0] + ': ' + z[1] + '\n'
mark_down += '\n'
mark_down += '### Taverns / Inns \n'
for x, y in settlement_taverns.items():
    mark_down += '#### ' + x + '\n'
    mark_down += '**Location** :: ' + y[0] + '\n'
    mark_down += '**Description** :: ' + y[1] + '\n'
    mark_down += '**Innkeeper** :: ' + y[2] + '\n'
    mark_down += '##### Menu\n'
    mark_down += '* ' + y[3] + '\n'
    mark_down += '* ' + y[4] + '\n' 
    mark_down += '* ' + y[5] + '\n'
    mark_down += '* ' + y[6] + '\n'
    mark_down += '* ' + y[7] + '\n'
    mark_down += '\n\n'
write_mark_down(mark_down, uuid)