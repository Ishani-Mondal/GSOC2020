# GSOC2020

### src/dep_tregex Folder:

Tregex_Obama_DBpedia.ipynb : Contains implementation of the Tregex-based Triple Prediction on the Barrack Obama Abstracts

Mainly follows the algorithm of : http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.453.4005&rep=rep1&type=pdf

Intially divide the sentences into three main chunks based on POS: NP-VP-NP
	<subject, verb, object>

## Subject Finding:

Firstly  we  intend  to  find  the  subject  of  the  sentence.  In  order  to  find  it,  we  are  going  to  search  in  the  NP  subtree.  The  subject  will  be  found  by  performing  breadth  first  search  and  selecting  the  first  descendent  of  NP  that  is  a  noun.

## VERB Finding:

Secondly,  for  determining  the  predicate  of  the  sentence,  a  search  will  be  performed  in  the  VP  subtree.  The  deepest  verb  descendent  of  the  verb  phrase  will  give  the  second  element  of  the  triplet

## OBJECT Finding:

Thirdly,  we  look  for  objects.  These  can  be  found  in  three  different subtrees, all siblings of the VP subtree containing the  predicate.  The  subtrees  are:  PP  (prepositional  phrase),  NP (noun phrase) and  ADJP  (adjective  phrase).  In  NP  and  PP  we  search  for the first noun, while in ADJP we find the first adjective

Moreover, for each of the element in the triplet, we also take a look into its modifiers, which mostly consists of adjectives (for nouns) and adverbs for the adjectives (for adjectives).



### src/pyclausie Folder : 
Paper: http://resources.mpi-inf.mpg.de/d5/clausie/clausie-www13.pdf
Clause_IE_Predictions.ipynb : Contains implementation of the ClauseIE based Triple Prediction on the Barrack Obama Abstracts


====================================Mapping=============================================

### src/mapping Folder : 

#### Using DBpedia Spotlight API:

curl -X GET "https://api.dbpedia-spotlight.org/en/annotate?text=Barack%20Hussein%20Obama%20II%20is%20an%20American%20politician%20who%20is%20the%2044th%20and%20current%20President%20of%20the%20United%20States.%20He%20is%20the%20first%20African%20American%20to%20hold%20the%20office%20and%20the%20first%20president%20born%20outside%20the%20continental%20United%20States.%20Born%20in%20Honolulu%2C%20Hawaii%2C%20Obama%20is%20a%20graduate%20of%20Columbia%20University%20and%20Harvard%20Law%20School%2C%20where%20he%20was%20president%20of%20the%20Harvard%20Law%20Review.%20He%20was%20a%20community%20organizer%20in%20Chicago%20before%20earning%20his%20law%20degree.%20He%20worked%20as%20a%20civil%20rights%20attorney%20and%20taught%20constitutional%20law%20at%20the%20University%20of%20Chicago%20Law%20School%20between%201992%20and%202004.%20While%20serving%20three%20terms%20representing%20the%2013th%20District%20in%20the%20Illinois%20Senate%20from%201997%20to%202004%2C%20he%20ran%20unsuccessfully%20in%20the%20Democratic%20primary%20for%20the%20United%20States%20Hou" -H  "accept: application/json"

Used to map the triples from text to resources and classes (ontologies)

Intermediate JSON Files: input_data/Obama_Json.json
Result of mapping is in : triple_extraction_results/Mapped_ClauseIE_results
