#
#     USAGE var_code/util/test_website url verbose=True/False
#
#  Would like to make this work on a directory with files containing links as well as the website
import urllib2
import re
import os
from types import StringType 



def test_website(url, verbose=False):
    debug = False
    nlinks_tried  = 0 
    nlinks_failed = 0


    if debug:
        print "==========================================================="
        print "args to test_website ",url," verbose = ",verbose,type(verbose)
    if type(verbose) == StringType:
        if verbose == 'False':
            verbose = False
        elif verbose == 'True':
            verbose = True
        else: 
            print "ERROR: ",__file__," received verbose argument = ",verbose
            print "       verbose must = True or False"
            return False
 
    if not urllib2.urlparse.urlparse(url).netloc:
        return False

    website = urllib2.urlopen(url)
    html = website.read()
    
    if website.code != 200 :
        return False

    dirname = os.path.dirname(url)

    # Get all the links from the file. Brute forcing case insensitivity
    # Should be able to do [href|HREF] but then I lose the rest of the string
    # IGNORECASE chould work too
#    print("received line: ",html)

    linklist = re.findall('href=.*', html)
#    linklist.extend(re.findall("HREF=.*[png,gif,ps]", html))
    linklist.extend(re.findall("HREF=.*>",html))
 
#OLD    linklist = re.findall('".*"', html)
#       print linklist
#    return False  #quit out

    if debug:
        print "LINKLIST"
        print "found linklist ",linklist
    for link in linklist:


        test = re.split("=",link)
        if len(test) > 2:
            test3 = [test[0],"=".join(test[1:])]
            if (debug): 
                print "WARNING there are multiple = in the path"
                print "test3 ",test3
            test = test3
                     
        test2 = re.split(">",test[1])
        if debug: 
            print "test ",test
            print "test2 ",test2

        newlink = test2[0].replace('"','').strip()
        newlink = newlink.replace('HREF=','').strip()
        newlink = newlink.replace('href=','').strip()

        # Deal with relative links by keying off of 'html'
        if "html" not in newlink.lower():
            fullpath = dirname +"/"+ newlink
            url = fullpath

#        if debug:
#            print "Testing link ",url
 
       # I'm not sure what this does
        if not urllib2.urlparse.urlparse(url).netloc:
            return False

        try:
            nlinks_tried = nlinks_tried + 1
            website = urllib2.urlopen(url)
            if (debug):
                print "Found link : ",url
        except:
            nlinks_failed = nlinks_failed + 1
            if (verbose | debug ):
                print "Missing link ",url
                
        finally:
            if website.code != 200:
                if (verbose):
                    print "Failed link w/o exception: ", url
                nlinks_failed = nlinks_failed + 1

#            print nlinks_failed," fail out of ",nlinks_tried," tried"


    if nlinks_failed == 0:
        return True,nlinks_tried,nlinks_failed
    else:
        return False,nlinks_tried,nlinks_failed



# ======================================================================
# MAIN
# ======================================================================
#test = test_website("http://www.cgd.ucar.edu/cms/bundy/Projects/diagnostics/mdtf/mdtf_figures/MDTF_QBOi.EXP1.AMIP.001/MJO_suite/MJO_suite.html",True)

import sys

verbose = False
try:
#    print __file__,"received args ",sys.argv," of type ",type(sys.argv)
#
#    nb. sys.argv[0] = __file__
#
    if len(sys.argv) <= 1:
        print "USAGE ",__file__," url [check_all_links True/False]"
        
    else:
        url = sys.argv[1]
        if len(sys.argv) == 2:
            isgood,nlinks,nmissing = test_website(url,verbose=verbose)
        elif len(sys.argv) == 3:
            isgood,nlinks,nmissing = test_website(url,sys.argv[2],verbose=verbose)

    if isgood:
        print "All",nlinks,"links good on",url
    else:
        print "Missing",nmissing,"of",nlinks,"links on",url


except Exception, e:
    print "ERROR: ",e


