# Tregex_Based_Parsing

Mainly follows the algorithm of : http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.453.4005&rep=rep1&type=pdf
1. Intially divide the sentences into three main chunks based on POS: NP-VP-NP
	<subject, verb, object>

## Subject Finding:

Firstly  we  intend  to  find  the  subject  of  the  sentence.  In  order  to  find  it,  we  are  going  to  search  in  the  NP  subtree.  The  subject  will  be  found  by  performing  breadth  first  search  and  selecting  the  first  descendent  of  NP  that  is  a  noun.

## VERB Finding:

Secondly,  for  determining  the  predicate  of  the  sentence,  a  search  will  be  performed  in  the  VP  subtree.  The  deepest  verb  descendent  of  the  verb  phrase  will  give  the  second  element  of  the  triplet

## OBJECT Finding:

Thirdly,  we  look  for  objects.  These  can  be  found  in  three  different subtrees, all siblings of the VP subtree containing the  predicate.  The  subtrees  are:  PP  (prepositional  phrase),  NP (noun phrase) and  ADJP  (adjective  phrase).  In  NP  and  PP  we  search  for the first noun, while in ADJP we find the first adjective

Moreover, for each of the element in the triplet, we also take a look into its modifiers, which mostly consists of adjectives (for nouns) and adverbs for the adjectives (for adjectives).


