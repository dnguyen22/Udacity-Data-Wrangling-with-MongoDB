from bs4 import BeautifulSoup

html_page = "options.html"


def extract_carriers(page):
    data = []

    with open(page, "r") as html:
        soup = BeautifulSoup(html, "lxml")
        carrier_list = soup.find(id="CarrierList")

        for carrier in carrier_list.find_all('option'):
            if len(carrier['value']) == 2:
                data.append(carrier['value'])

    return data


def make_request(data):
    eventvalidation = data["eventvalidation"]
    viewstate = data["viewstate"]
    airport = data["airport"]
    carrier = data["carrier"]

    r = s.post("https://www.transtats.bts.gov/Data_Elements.aspx?Data=2",
               data=(("__EVENTTARGET", ""),
                     ("__EVENTARGUMENT", ""),
                     ("__VIEWSTATE", viewstate),
                     ("__VIEWSTATEGENERATOR", viewstategenerator),
                     ("__EVENTVALIDATION", eventvalidation),
                     ("CarrierList", carrier),
                     ("AirportList", airport),
                     ("Submit", "Submit")))

    return r.text


def extract_airports(page):
    data = []
    with open(page, "r") as html:
        soup = BeautifulSoup(html, "lxml")
        airport_list = soup.find(id='AirportList')

        for airport in airport_list.find_all('option'):
            if len(airport['value']) == 3 and airport['value'] != 'All':
                data.append(airport['value'])

    return data


def test_extract_airports():
    data = extract_airports(html_page)
    assert len(data) == 15
    assert "ATL" in data
    assert "ABR" in data


def test_extract_carriers():
    data = extract_carriers(html_page)
    assert len(data) == 16
    assert "FL" in data
    assert "NK" in data


if __name__ == "__main__":
    test_extract_carriers()
    test_extract_airports()