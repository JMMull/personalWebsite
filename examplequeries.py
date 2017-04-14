__author__ = "Joseph Mullen"


class examples():
    def __init__(self):
        self.all = []
        self.prefixes = (
        "PREFIX rdfs:  <http://www.w3.org/2000/01/rdf-schema#>\nPREFIX drenin:  <http://drenin.ncl.ac.uk/Terms#>\nPREFIX drugbank:  <http://identifiers.org/drugbank#>\nPREFIX uniprot:  <http://identifiers.org/uniprot#>\nPREFIX hgnc.symbol:  <http://identifiers.org/hgnc.symbol#>\nPREFIX string:  <http://identifiers.org/string#>\nPREFIX go:  <http://identifiers.org/go#>\nPREFIX goa:  <http://identifiers.org/goa#>\nPREFIX ORDO:  <http://www.orpha.net/ORDO/>\nPREFIX MeSH:  <http://id.nlm.nih.gov/mesh/2015/>\nPREFIX ClinicalTrials.gov:  <https://ClinicalTrials.gov/show/>\nPREFIX wp:  <http://identifiers.org/wikipathways/>\n");

    def getquery(self):
        one = self.individual('1', 'Return all proteins that interact with proteinX (uniprot:Q13444)', self.prefixes +
                              "\nSELECT ?Protein WHERE  {\n"
                              + "\t{\n"
                              + "\tuniprot:Q13444 drenin:hasPpi ?Protein .\n"
                              + "} UNION {\n"
                              + "\t?Protein drenin:hasPpi uniprot:Q13444 .\n"
                              + "\t}\n"
                              + "}\n"
                              + "LIMIT 20")
        self.all.append(one)

        two = self.individual('2', 'Return all indications for drugX (drugbank:DB00203)',
                              self.prefixes + "\nSELECT ?disease ?type ?name WHERE  {\n"
                              + "\tdrugbank:DB00203 drenin:hasIndication ?disease .\n"
                              + "\t?disease a ?type .\n"
                              + "\t?type rdfs:subClassOf drenin:Disease .\n"
                              + "\t?disease drenin:MeSHHeader ?name .\n"
                              + "}\n"
                              + "LIMIT 20")
        self.all.append(two)

        three = self.individual('3', 'Return all completed Phase 4 clinical trials involving drugX (drugbank:DB00203)',
                                self.prefixes + "\nSELECT ?Trial ?Title WHERE  {\n"
                                + "\t?Trial drenin:drugInTrial drugbank:DB00203 .\n"
                                + "\t?Trial drenin:Phase \"Phase 4\" .\n"
                                + "\t?Trial drenin:Status \"Completed\" .\n"
                                + "\t?Trial drenin:Title ?Title .\n"
                                + "}\n"
                                + "LIMIT 20")
        self.all.append(three)

        four = self.individual('4', 'Return all druggable targets associated with rarediseaseX (ORDO:Orphanet_2764)',
                               self.prefixes + "\nSELECT ?drug ?target ?gene WHERE  {\n"
                               + "\t?drug drenin:bindsTo ?target .\n"
                               + "\t?target drenin:isEncodedBy ?gene .\n"
                               + "\t?gene drenin:involvedInRareDisease ORDO:Orphanet_2764 .\n"
                               + "}\n"
                               + "LIMIT 20")
        self.all.append(four)

        five = self.individual('5',
                               'Return all targets that drugX (drugbank:DB00203) potently binds to and the rare diseases associated to these targets. Do not include diseases drugX is marketed to treat or are known off-target effects of the drug',
                               self.prefixes + "\nSELECT DISTINCT ?Protein ?PossInd ?PossIndName WHERE  {\n"
                               + "  ?t rdf:subject drugbank:DB00203 .\n"
                               + "  ?t rdf:predicate drenin:bindsTo .\n"
                               + "  ?t rdf:object ?Protein .\n"
                               + "  ?t drenin:ActivityType \"Ki\" .\n"
                               + "  ?t drenin:ActivityValue ?KiValue .\n"
                               + "  FILTER (?KiValue < \"10.0\")\n"
                               + "   ?Protein drenin:isEncodedBy ?gene .\n"
                               + "   ?gene drenin:involvedInRareDisease ?PossInd .\n"
                               + "   ?PossInd drenin:MeSHHeader ?PossIndName .\n"
                               + "   MINUS {drugbank:DB00203 drenin:hasIndication ?PossInd .}\n"
                               + "   MINUS {drugbank:DB00203 drenin:hasSideEffect ?PossInd .}\n"
                               + "}\n"
                               + "LIMIT 20"
                               )
        self.all.append(five)

        six = self.individual('6',
                              'Return the title, phase and status of clinical trials that involve drugY (drugbank:DB00203) and diseaseX (drenin:D008171)',
                              self.prefixes + "\nSELECT ?Trial ?Title ?Phase ?Status WHERE  {\n"
                              + "	?Trial drenin:drugInTrial drugbank:DB00203 .\n"
                              + "	?Trial drenin:diseaseInTrial drenin:D008171 .\n"
                              + "	?Trial drenin:Phase ?Phase .\n"
                              + "	?Trial drenin:Status ?Status .\n"
                              + "	?Trial drenin:Title ?Title .\n"
                              + "}\n"
                              + "LIMIT 20")
        self.all.append(six)

        seven = self.individual('7',
                                'Return all rare diseases for which there are currently no marketed drugs but have known genetic associations that can potentially be targeted',
                                self.prefixes + "\nSELECT DISTINCT ?Disease ?MeSH WHERE  {\n"
                                + "   ?Disease a drenin:RareDisease .\n"
                                + "   ?Disease drenin:MeSHHeader ?MeSH .\n"
                                + "   ?Gene drenin:involvedInRareDisease ?Disease .\n"
                                + "      MINUS { \n"
                                + "              ?drug drenin:hasIndication ?Disease .\n"
                                + "              ?drug a ?type.\n"
                                + "              ?type rdfs:subClassOf drenin:Drug . \n"
                                + "             }\n"
                                + "}\n"
                                + "LIMIT 20")
        self.all.append(seven)

        return self.all

    class individual():
        def __init__(self, uid, description, SPARQL):
            self.uid = uid
            self.description = description
            self.SPARQL = SPARQL
