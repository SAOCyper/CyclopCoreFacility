
#See https://www.wikidata.org/wiki/Special:ListProperties/wikibase-item for properties

class WikiDataProperties():

    def init(self):
        pass
    def create_property_list(self):
        self.property_type_item_list = {
            "head of government":"P6",
            "transport network":"P16",
            "country":"P17",
            "place of birth":"P19",
            "place of death":"P20",
            "sex or gender":"P21",
            "father":"P22",
            "mother":"P25",
            "spouse":"P26",
            "citizenship":"P27",
            "continent":"P30",
            "instance of":"P31",
            "capital":"P36",
            "official language":"P37",
            "currency":"P38",
            "position held":"P39",
            "child":"P40",
            "shares border with":"P47",
            "author":"P50",
            "family":"P53",
            "member of sports team":"P54",
            "director":"P57",
            "inventor":"P61",
            "educated at":"P69",
            "architect":"P84",
            "anthem":"P85",
            "composer":"P86",
            "commissioned by":"P88",
            "noble title":"P97",
            "editor":"P98",
            "field of work":"P101",
            "native language":"P103",
            "occupation":"P106",
            "employer":"P108",
            "illustrator":"P110",
            "measured physical quantity":"P111",
            "founded by":"P112",
            "place of burial":"P119",
            "publisher":"P123",
            "maintained by":"P126",
            "owned by":"P127",
            "genre":"P136",
            "named after":"P138",
            "religion":"P140",
            "killed by":"P157",
            "cast member":"P161",
            "creator":"P170",
            "ethnic group":"P172",
            "manufacturer":"P176",
            "developer":"P178",
            "part of the series":"P179",
            "stated in":"P248",
            "official residence":"P263",
            "production company":"P272",
            "copyright license":"P275",
            "location":"P276",
            "programmed in":"P277",
            "operating system":"P306",
            "discography":"P358",
            "part of":"P361",
            "military rank":"P410",
            "color":"P462",
            "input device":"P479",
            "cause of death":"P509",
            "academic degree":"P512",
            "participant":"P710"
        }
        self.property_type_geographiccoord_list = {
            "coordinate location":"P625",
            "coordinates of point of view":"P1259",
            "coordinates of northernmost point":"P1332",
            "coordinates of southernmost point":"P1333",
            "coordinates of easternmost point":"P1334",
            "coordinates of westernmost point":"P1335"
        }
        self.property_type_time_list = {
            "point in time":"P585",
            "birth date": "P569",
            "death date": "P570"
        }
        return self.property_type_item_list , self.property_type_geographiccoord_list , self.property_type_time_list
    

