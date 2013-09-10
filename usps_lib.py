import urllib, urllib2, sys
from bs4 import BeautifulSoup

def FindAddress(input_st_name, input_st_num, input_city, input_zip):
    streetAddressSpaces = str(input_st_num) + ' ' + str(input_st_name)
    streetAddress = streetAddressSpaces.replace(' ','+')
    city = input_city
    zipcode = str(input_zip)
    url = "https://tools.usps.com/go/ZipLookupResultsAction!input.action?resultMode=0&companyName=&address1=" + streetAddress + "&address2=&city=" + city + "&state=Select&urbanCode=&postalCode=&zip=" + zipcode
    results = urllib.urlopen(url)
    
    #create file object with response HTML
    with open("results_test.html", "w") as f:
        f.write(results.read())
    
    #extract resulting street address, city, state, and zipcode
    if sys.platform == 'win32':
        soup = BeautifulSoup(open("C:/Documents and Settings/schristensen/My Documents/Python/Address_Validation/results_test.html"))
    else:
        soup = BeautifulSoup(open("/var/www/DjangoProjects/WebMap/scripts/results_test.html"))
    
    #extract street address
    streetAddressResultTag = soup.find("span", class_="address1 range")
    if str(streetAddressResultTag) == 'None':
        streetAddressResult = 'None'
    else:
        streetAddressResult = str(streetAddressResultTag.string.strip())
    
    #extract city
    cityResultTag = soup.find("span", class_="city range")
    if str(cityResultTag) == 'None':
        cityResult = 'None'
    else:
        cityResult = str(cityResultTag.string.strip())
    
    #extract state
    stateResultTag = soup.find("span", class_="state range")
    if str(stateResultTag) == 'None':
        stateResult = 'None'
    else:
        stateResult = str(stateResultTag.string.strip())

    #extract zipcode
    zipResultTag = soup.find("span", class_="zip")
    if str(zipResultTag) == 'None':
        zipResult = 'None'
    else:
        zipResult = str(zipResultTag.string.strip())

    if (streetAddressSpaces.upper() == streetAddressResult) and (zipcode == zipResult):
        isAccurate = True
    else:
        isAccurate = False
    
    if streetAddressResult == 'None':
        recommendation = False
    elif isAccurate == True:
        recommendation = False
    elif len(streetAddress) > 0:
        recommendation = True
    else:
        recommendation = False
    
    dict = {'isAccurate': isAccurate, 'recommendation': recommendation, 'uspsAddress': streetAddressResult, 'uspsCity': cityResult, 'uspsState': stateResult, 'uspsZip': zipResult }

    return dict
