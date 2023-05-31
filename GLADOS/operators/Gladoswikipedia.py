import wikipedia,json,requests
from datetime import datetime
from dateutil import parser
from wikidata.datavalue import Decoder
from wikidata.client import Client
from qwikidata.entity import WikidataItem, WikidataLexeme, WikidataProperty
from qwikidata.linked_data_interface import get_entity_dict_from_api
from qwikidata.json_dump import WikidataJsonDump
from qwikidata.utils import dump_entities_to_json
from WikiDataProperties import WikiDataProperties

class Glados_knowlodge:
    def __init__(self,language="en"):
        self.language=language
        wikipedia.set_lang(self.language)
        properties = WikiDataProperties()
        self.property_type_item_list , self.property_type_geographiccoord_list,self.property_type_time_list= properties.create_property_list()
    def id_for_page(self,page):
        """Uses the wikipedia api to find the wikidata id for a page"""
        api = "https://en.wikipedia.org/w/api.php"
        query = "?action=query&prop=pageprops&titles=%s&format=json"
        slug = page.split('/')[-1]

        response = json.loads(requests.get(api + query % slug).content)
        
        # Assume we got 1 page result and it is correct.
        page_info = list(response['query']['pages'].values())[0]
        print(page_info)
        if "pageprops" in page_info :
            if "wikibase_item" in page_info['pageprops'] :
                return  page_info['pageprops']['wikibase_item']
            else : 
                return None
        else : 
                return None
    def get_claim_as_time(self,claims, claim_id,parser_info=None):
        """Helper function to work with data returned from wikidata api"""
        try:
            claim = claims[claim_id][0]['mainsnak']['datavalue']
            assert claim['type'] == 'time', "Expecting time data type"
            str1 = claim['value']['time'][1:]
            if str1[5:7] == "00" : 
                list1 = list(claim['value']['time'][1:])
                list1[5:7]="01"
                str1 = ''.join(list1)
            if str1[8:10] == "00":
                list1 = list(str1)
                list1[8:10]="01"
                str1 = ''.join(list1)
            # dateparser chokes on leading '+', thanks wikidata.
            return parser.parse(str1,parserinfo=parser_info)
        except KeyError as e:
            print(e)
            return None
    def get_claim_as_string(self,claims, claim_id,parser_info=None):
        try:
            claim = claims[claim_id][0]['mainsnak']['datavalue']
            assert claim["type"] == 'wikibase-entityid' , "Expecting string data type"
            return claim
        except KeyError as e:
            return None
    def get_claim_as_geographic(self,claims, claim_id,parser_info=None):
        try:
            claim = claims[claim_id][0]['mainsnak']['datavalue']
            assert claim["type"] == 'globecoordinate' , "Expecting globe-coordinate data type"
            return claim
        except KeyError as e:
            return None
    def lifespan_for_id(self,wikidata_id,parser_info=None):
        """Uses the wikidata API to retrieve wikidata for the given id."""
        data_url = "https://www.wikidata.org/wiki/Special:EntityData/%s.json"
        page = json.loads(requests.get(data_url % wikidata_id).content)

        claims = list(page['entities'].values())[0]['claims']
        # P569 (birth) and P570 (death) ... not everyone has died yet.
        return [self.get_claim_as_time(claims, cid,parser_info) for cid in ['P585','P569', 'P570']]
    def all_for_id(self,wikidata_id,parser_info=None):
        data_url = "https://www.wikidata.org/wiki/Special:EntityData/%s.json"
        page = json.loads(requests.get(data_url % wikidata_id).content)
        claim_list = []
        claims = list(page['entities'].values())[0]['claims']
        keys_list = []
        ind = 0
        for a in self.property_type_item_list.keys():
            keys_list.append(a)
        for cid in self.property_type_item_list.values():
            claim_list.append([self.get_claim_as_string(claims, cid,parser_info),keys_list[ind]])
            ind += 1
        return claim_list
    def geographic_for_id(self,wikidata_id,parser_info=None):
        data_url = "https://www.wikidata.org/wiki/Special:EntityData/%s.json"
        page = json.loads(requests.get(data_url % wikidata_id).content)
        claim_list = []
        claims = list(page['entities'].values())[0]['claims']
        keys_list = []
        ind = 0
        """ print("claims:",claims) """
        for a in self.property_type_geographiccoord_list.keys():
            keys_list.append(a)
        for cid in self.property_type_geographiccoord_list.values():
            claim_list.append([self.get_claim_as_geographic(claims, cid,parser_info),keys_list[ind]])
            ind += 1
        return claim_list
    def FetchTimeRelevantData(self,person):
        person = person.replace(' ', '_')
        page = 'https://en.wikipedia.org/wiki/{}'.format(person)
        # 1. use the wikipedia api to find the wikidata id for this page
        wikidata_id = self.id_for_page(page)
        # 2. use the wikidata id to get the birth and death dates
        span = self.lifespan_for_id(wikidata_id)

        for label, dt in zip(["point in time" ,"birth", "death"], span):
            if dt != None:
                print(label, " = ", datetime.strftime(dt, "%b %d, %Y"))
    def FetchRelevantDataPerson(self,person):
        person = person.replace(' ', '_')
        page = 'https://en.wikipedia.org/wiki/{}'.format(person)
        # 1. use the wikipedia api to find the wikidata id for this page
        wikidata_id = self.id_for_page(page)
        if wikidata_id != None:
            # 2. use the wikidata id to get the birth and death dates
            span_all  = self.all_for_id(wikidata_id)
            for dt in span_all:
                if dt[0] != None:
                    entity=get_entity_dict_from_api(dt[0]["value"]["id"])
                    entity = WikidataItem(entity)
                    print(dt[1]," = ",entity.get_label())
    def FetchGeographicRelevantData(self,context):
        context = context.replace(' ', '_')
        page = 'https://en.wikipedia.org/wiki/{}'.format(context)
        # 1. use the wikipedia api to find the wikidata id for this page
        wikidata_id = self.id_for_page(page)
        if wikidata_id != None:
            # 2. use the wikidata id to get the birth and death dates
            span_all  = self.geographic_for_id(wikidata_id)
            print(span_all)
            for dt in span_all:
                if dt[0] != None:
                    print(dt[1],"Latitude"," = ",dt[0]["value"]["latitude"],"Longitude"," = ",dt[0]["value"]["longitude"],"Altitude"," = ",dt[0]["value"]["altitude"])                  
    def FetchSummary(self,context):
        self.context = context
        result = wikipedia.search(context)
        page=wikipedia.page(result[0])
        title = page.title
        categories = page.categories
        content = page.content
        links = page.links
        references = page.references
        summary = page.summary
        print("Page title:", title, "\n")
        print("Summary:", summary, "\n")
    
wiki = Glados_knowlodge()
""" wiki.FetchRelevantDataPerson("Battle of Ankara") 
wiki.FetchTimeRelevantData("Battle of Ankara")
wiki.FetchGeographicRelevantData("Turkey")
wiki.FetchSummary("Operating System")  """
