=CONCAT("<t><s>",SUBSTITUTE(A1,"-","</s><s>"),"</s></t>")
=FILTERXML(A1,"//s[1]")
=FILTERXML(CONCAT("<t><s>",SUBSTITUTE(A1,"-","</s><s>"),"</s></t>"), "//s[1]")

**1) All Elements:**
=FILTERXML(<XML>,"//s")
Returns: ABC, 123, DEF, 456, XY-1A, ZY-2F, XY-3F, XY-4f, xyz and 123 (all nodes)
**2) Elements by position:**
=FILTERXML(<XML>,"//s[position()=4]")
Or:
=FILTERXML(<XML>,"//s[4]")
Returns: 456 (node on index 4)†
=FILTERXML(<XML>,"//s[position()<4]")
Returns: ABC, 123 and DEF (nodes on index < 4)
=FILTERXML(<XML>,"//s[position()=2 or position()>5]")
Returns: 123, ZY-2F, XY-3F, XY-4f, xyz and 123 (nodes on index 2 or > 5)
=FILTERXML(<XML>,"//s[last()]")
Returns: 123 (node on last index)
=FILTERXML(<XML>,"//s[position() mod 2 = 1]")
Returns: ABC, DEF, XY-1A, XY-3F and xyz (odd nodes)
=FILTERXML(<XML>,"//s[position() mod 2 = 0]")
Returns: 123, 456, ZF-2F, XY-4f and 123 (even nodes)
**3) (Non) numeric elements:**
=FILTERXML(<XML>,"//s[number()=.]")
Or:
=FILTERXML(<XML>,"//s[.*0=0]")
Returns: 123, 456, and 123 (numeric nodes)
=FILTERXML(<XML>,"//s[not(number()=.)]")
Or:
=FILTERXML(<XML>,"//s[.*0!=0)]")
Returns: ABC, DEF, XY-1A, ZY-2F, XY-3F, XY-4f and xyz (non-numeric nodes)
**4) Elements that (not) contain:**
=FILTERXML(<XML>,"//s[contains(., 'Y')]")
Returns: XY-1A, ZY-2F, XY-3F and XY-4f (containing 'Y', notice XPATH is case sensitive, exclusing xyz)
=FILTERXML(<XML>,"//s[not(contains(., 'Y'))]")
Returns: ABC, 123, DEF, 456, xyz and 123 (not containing 'Y', notice XPATH is case sensitive, including xyz)
**5) Elements that (not) start or/and end with:**
=FILTERXML(<XML>,"//s[starts-with(., 'XY')]")
Returns: XY-1A, XY-3F and XY-4f (starting with 'XY')
=FILTERXML(<XML>,"//s[not(starts-with(., 'XY'))]")
Returns: ABC, 123, DEF, 456, ZY-2F, xyz and 123 (don't start with 'XY')
=FILTERXML(<XML>,"//s[substring(., string-length(.) - string-length('F') +1) = 'F']")
Returns: DEF, ZY-2F and XY-3F (end with 'F', notice XPATH 1.0 does not support ends-with)
=FILTERXML(<XML>,"//s[not(substring(., string-length(.) - string-length('F') +1) = 'F')]")
Returns: ABC, 123, 456, XY-1A, XY-4f, xyz and 123 (don't end with 'F')
=FILTERXML(<XML>,"//s[starts-with(., 'X') and substring(., string-length(.) - string-length('A') +1) = 'A']")
Returns: XY-1A (start with 'X' and end with 'A')
**6) Elements that are upper- or lowercase:**
=FILTERXML(<XML>,"//s[translate(.,'abcdefghijklmnopqrstuvwxyz','ABCDEFGHIJKLMNOPQRSTUVWXYZ')=.]")
Returns: ABC, 123, DEF, 456, XY-1A, ZY-2F, XY-3F and 123 (uppercase nodes)
=FILTERXML(<XML>,"//s[translate(.,'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz')=.]")
Returns: 123, 456, xyz and 123 (lowercase nodes)
NOTE: Unfortunately XPATH 1.0 does not support upper-case() nor lower-case() so the above is a workaround. Add special characters if need be.
**7) Elements that (not) contain any number:**
=FILTERXML(<XML>,"//s[translate(.,'1234567890','')!=.]")
Returns: 123, 456, XY-1A, ZY-2F, XY-3F, XY-4f and 123 (contain any digit)
=FILTERXML(<XML>,"//s[translate(.,'1234567890','')=.]")
Returns: ABC, DEF and xyz (don't contain any digit)
=FILTERXML(<XML>,"//s[translate(.,'1234567890','')!=. and .*0!=0]")
Returns: XY-1A, ZY-2F, XY-3F and XY-4f (holding digits but not a a number on it's own)
**8) Unique elements or duplicates:**
=FILTERXML(<XML>,"//s[preceding::*=.]")
Returns: 123 (duplicate nodes)
=FILTERXML(<XML>,"//s[not(preceding::*=.)]")
Returns: ABC, 123, DEF, 456, XY-1A, ZY-2F, XY-3F, XY-4f and xyz (unique nodes)
=FILTERXML(<XML>,"//s[not(following::*=. or preceding::*=.)]")
Returns: ABC, DEF, 456, XY-1A, ZY-2F, XY-3F and XY-4f (nodes that have no similar sibling)
**9) Elements of certain length:**
=FILTERXML(<XML>,"//s[string-length()=5]")
Returns: XY-1A, ZY-2F, XY-3F and XY-4f (5 characters long)
=FILTERXML(<XML>,"//s[string-length()<4]")
Returns: ABC, 123, DEF, 456, xyz and 123 (shorter than 4 characters)
**10) Elements based on preceding/following:**
=FILTERXML(<XML>,"//s[preceding::*[1]='456']")
Returns: XY-1A (previous node equals '456')
=FILTERXML(<XML>,"//s[starts-with(preceding::*[1],'XY')]")
Returns: ZY-2F, XY-4f, and xyz (previous node starts with 'XY')
=FILTERXML(<XML>,"//s[following::*[1]='123']")
Returns: ABC, and xyz (following node equals '123')
=FILTERXML(<XML>,"//s[contains(following::*[1],'1')]")
Returns: ABC, 456, and xyz (following node contains '1')
=FILTERXML(<XML>,"//s[preceding::*='ABC' and following::*='XY-3F']")
Or:
=FILTERXML(<XML>,"//s[.='ABC']/following::s[following::s='XY-3F']")    
Returns: 123, DEF, 456, XY-1A and ZY-2F (everything between 'ABC' and 'XY-3F')
**11) Elements based on sub-strings:**
=FILTERXML(<XML>,"//s[substring-after(., '-') = '3F']")
Returns: XY-3F (nodes ending with '3F' after hyphen)
=FILTERXML(<XML>,"//s[contains(substring-after(., '-') , 'F')]")
Returns: ZY-2F and XY-3F (nodes containing 'F' after hyphen)
=FILTERXML(<XML>,"//s[substring-before(., '-') = 'ZY']")
Returns: ZY-2F (nodes starting with 'ZY' before hyphen)
=FILTERXML(<XML>,"//s[contains(substring-before(., '-'), 'Y')]")
Returns: XY-1A, ZY-2F, XY-3F and XY-4f (nodes containing 'Y' before hyphen)
**12) Elements based on concatenation:**
=FILTERXML(<XML>,"//s[concat(., '|', following::*[1])='ZY-2F|XY-3F']")
Returns: ZY-2F (nodes when concatenated with '|' and following sibling equals 'ZY-2F|XY-3F')
=FILTERXML(<XML>,"//s[contains(concat(., preceding::*[2]), 'FA')]")
Returns: DEF (nodes when concatenated with sibling two indices to the left contains 'FA')
**13) Empty vs. Non-empty:**
=FILTERXML(<XML>,"//s[count(node())>0]")
Or:
=FILTERXML(<XML>,"//s[node()]")
Returns: ABC, 123, DEF, 456, XY-1A, ZY-2F, XY-3F, XY-4f, xyz and 123 (all nodes that are not empty)
=FILTERXML(<XML>,"//s[count(node())=0]")
Or:
=FILTERXML(<XML>,"//s[not(node())]")
Returns: None (all nodes that are empty)
**14) Preceding or Following:**
=FILTERXML(<XML>,"//s[substring(., string-length(.) - string-length('F') +1) = 'F'][last()]/following::*")
Returns: XY-4f, xyz and 123 (all nodes to the right of the last node that ends with an uppercase 'F')
=FILTERXML(<XML>,"//s[substring(., string-length(.) - string-length('F') +1) = 'F'][1]/preceding::*")
Returns: ABC and 123 (all nodes to the left of the first node that ends with an uppercase 'F')
**15) (Preceding or Following) and self:**
=FILTERXML(<XML>,"(//s[.*0!=0][last()]|//s[.*0!=0][last()]/preceding::*)")
Returns: ABC, 123, DEF, 456, XY-1A, ZY-2F, XY-3F, XY-4f and xyz (trim all numeric nodes from the right)††
=FILTERXML(<XML>,"(//s[.*0=0][1]|//s[.*0=0][1]/following::*)")
Returns: 123, DEF, 456, XY-1A, ZY-2F, XY-3F, XY-4f, xyz and 123 (trim all non-numeric nodes from the left)
**16) Maximum or Minimum:**
=FILTERXML(<XML>,"(//s[.*0=0][not(.<//s)])[1]")
Returns: 456 (The maximum value looking at numeric nodes)
=FILTERXML(<XML>,"(//s[.*0=0][not(.>//s)])[1]")
Returns: 123 (The minimum value looking at numeric nodes)
NOTE: This is the equivalent to returning all numeric nodes as per #3 and post-process the array using Excel's MIN() and MAX() functions.
