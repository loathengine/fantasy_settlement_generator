import csv


def import_csv(file):

    with open(file) as csvfile:
        reader = csv.DictReader(csvfile, delimiter="|", restval=3)
        return list(reader)


size_label = import_csv('data/size_label.txt')
primary_biome = import_csv('data/primary_biome.txt')
primary_topography = import_csv('data/primary_topography.txt')
industry_raw = import_csv('data/industry_raw.txt')
industry_shop = import_csv('data/industry_shop.txt')
industry_services = import_csv('data/industry_services.txt')
settlement_name = import_csv('data/settlement_name.txt')
settlement_government = import_csv('data/settlement_government.txt')
settlement_trait = import_csv('data/settlement_trait.txt')
race_percentage = import_csv('data/race_percentage.txt')
settle_age = import_csv('data/settlement_age.txt')
district_names = import_csv('data/district_names.txt')
district_trait = import_csv('data/district_trait.txt')
tavern_names = import_csv('data/tavern_names.txt')
tavern_description = import_csv('data/tavern_description.txt')
tavern_menu = import_csv('data/tavern_menu.txt')
background_flavor = import_csv('data/background_flavor.txt')
settlement_density = import_csv('data/settlement_density.txt')
settlement_wealth = import_csv('data/settlement_wealth.txt')
settlement_alignment = import_csv('data/settlement_alignment.txt')
npc_names = import_csv('data/npc_names.txt')


def write_xml(file):
    print('<?xml version="1.0" encoding="UTF-8"?>', file=file)
    print('<UNIVERSE>', file=file)
    print('  <ENV name="DEFAULT" weight="3" desc="The default environment for your universe." >', file=file)
    for p_b in primary_biome:
        print('    <BIOME name="' + str(p_b['key']) + '" weight="' + str(p_b['weight']) + '" desc="' + str(p_b['desc']) + '" >', file=file)
        for p_t in primary_topography:
            print('      <TOPOGRAPHY name="' + str(p_t['key']) + '" weight="' + str(p_t['weight']) + '" desc="' + str(p_t['desc']) + '" >', file=file)
            for r_i in industry_raw:
                print('        <RAW name="' + str(r_i['key']) + '" weight="' + str(r_i['weight']) + '" desc="' + str(r_i['desc']) + '" >', file=file)
                for i_s in industry_shop:
                    print('          <SHOP name="' + str(i_s['key']) + '" weight="' + str(i_s['weight']) + '" desc="' + str(i_s['desc']) + '" />', file=file)
                for d_n in district_names:
                    print('          <DISTRICT name="' + str(d_n['key']) + '" weight="' + str(d_n['weight']) + '" desc="' + str(d_n['desc']) + '" />', file=file)
                print('        </RAW>', file=file)
            print('      </TOPOGRAPHY>', file=file)
        print('    </BIOME>', file=file)
    print('  </ENV>', file=file)

    print('  <STATS>', file=file)
    for x in settlement_name:
        print('    <SETTLEMENT_NAME name="' + str(x['key']) + '" weight="' + str(x['weight']) + '" desc="' + str(x['desc']) + '" />', file=file)
    for x in background_flavor:
        print('    <FLAVOR name="' + str(x['key']) + '" weight="' + str(x['weight']) + '" desc="' + str(x['desc']) + '" />', file=file)
    for x in race_percentage:
        print('    <RACE name="' + str(x['key']) + '" weight="' + str(x['weight']) + '" desc="' + str(x['desc']) + '" />', file=file)
    for x in settle_age:
        print('    <AGE name="' + str(x['key']) + '" weight="' + str(x['weight']) + '" desc="' + str(x['desc']) + '" />', file=file)
    for x in settlement_government:
        print('    <GOVERNMENT name="' + str(x['key']) + '" weight="' + str(x['weight']) + '" desc="' + str(x['desc']) + '" />', file=file)
    for x in settlement_trait:
        print('    <TRAIT name="' + str(x['key']) + '" weight="' + str(x['weight']) + '" desc="' + str(x['desc']) + '" />', file=file)
    for x in district_trait:
        print('    <DISTRICT_TRAIT name="' + str(x['key']) + '" weight="' + str(x['weight']) + '" desc="' + str(x['desc']) + '" />', file=file)
    for x in tavern_menu:
        print('    <TAVERN_MENU name="' + str(x['key']) + '" weight="' + str(x['weight']) + '" desc="' + str(x['desc']) + '" />', file=file)
    for x in tavern_description:
        print('    <TAVERN_DESC name="' + str(x['key']) + '" weight="' + str(x['weight']) + '" desc="' + str(x['desc']) + '" />', file=file)
    for x in tavern_names:
        print('    <TAVERN_NAME name="' + str(x['key']) + '" weight="' + str(x['weight']) + '" desc="' + str(x['desc']) + '" />', file=file)
    for x in size_label:
        print('    <LABEL name="' + str(x['key']) + '" ceiling="' + str(x['weight']) + '" desc="' + str(x['desc']) + '" />', file=file)
    for x in settlement_density:
        print('    <DENSITY name="' + str(x['key']) + '" weight="' + str(x['weight']) + '" desc="' + str(x['desc']) + '" />', file=file)
    for x in settlement_wealth:
        print('    <WEALTH name="' + str(x['key']) + '" weight="' + str(x['weight']) + '" desc="' + str(x['desc']) + '" />', file=file)
    for x in settlement_alignment:
        print('    <ALIGNMENT name="' + str(x['key']) + '" weight="' + str(x['weight']) + '" desc="' + str(x['desc']) + '" />', file=file)
    for x in npc_names:
        print('    <NPC_NAMES name="' + str(x['key']) + '" weight="' + str(x['weight']) + '" desc="' + str(x['desc']) + '" />', file=file)
    print('  </STATS>', file=file)

    print('  <IND>', file=file)
    print('  </IND>', file=file)

    print('</UNIVERSE>', file=file)

with open("data/monolith.xml", "w") as m:
    write_xml(m)