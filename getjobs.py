#!/usr/bin/env python3

import json
import requests

from bs4 import BeautifulSoup
from collections import OrderedDict
from multiprocessing import Pool
from subprocess import Popen, PIPE


JSON_PATH = "/home/ayush/Projects/client/data/json/"
MARKUP_PATH = "/home/ayush/Projects/client/data/markup/"

_content_pre = """<div class="row"><div class="ten columns"><p>"""
_content_mid = """</p></div><div class="two columns apply-btn"><a href=\""""
_content_end = """\" target="_blank" rel="noreferrer" class="apply-btn-link"><code><strong>APPLY</strong></code></a></div></div>"""
_count_pre = """<div class="row"><div class="ten columns"><h5>Available Jobs: """
_count_end = """</h5></div></div><br>"""
_empty = """<div class="row"><div class="ten columns"><h5 class="no-jobs">No job listings found! Check back later.</h5></div></div>"""


#MERCEDES
def mercedes():
    merc_dict = OrderedDict()
    merc_pre_url = "http://careers.mercedesamgf1.com"
    merc_url = merc_pre_url + "/vacancies/?s_keywords="

    try:
        r = requests.get(merc_url)
    except requests.exceptions.RequestException as e:
        print("An exception occured while connecting to MERCEDES")
        print(e)

    soup = BeautifulSoup(r.content, 'html.parser')
    tag = soup.find_all("div", class_ = "job-item")

    for merc in tag:
        merc_dict[merc.a.text] = merc_pre_url + merc.a.get('href')

    with open(JSON_PATH + "MER.json", "w") as merc_fo:
        json.dump(merc_dict, merc_fo)
    if(merc_dict):
        with open(MARKUP_PATH + "MER", "w") as merc_mkp_fo:
            merc_mkp_fo.write(_count_pre + str(len(merc_dict)) + _count_end + "\n\n")
            for k in merc_dict:
                merc_mkp_fo.write(_content_pre + k + _content_mid + merc_dict[k] + _content_end)
                merc_mkp_fo.write("\n\n")
    else:
        with open(MARKUP_PATH + "MER", "w") as merc_mkp_fo:
            merc_mkp_fo.write(_empty + "\n\n")


#FERRARI
def ferrari():
    fer_dict = OrderedDict()
    cookielist=[]
    fer_job_url = "http://corporate.ferrari.com/en/career/career-opportunities"
    
    def get_ferrari_jobs(r):
        soup = BeautifulSoup(r.content, 'html.parser')
        tag = soup.find_all("span", class_="rs_lab_prsearch")
        for fer in tag:
            if(fer.div.text.startswith("Ferrari F1 Team")):
                fer_dict[fer.div.text] = fer_job_url

    process = Popen(['phantomjs', 'getcookies.js'],
                    stdout=PIPE, 
                    stderr=PIPE)

    for cookie in process.stdout:
        cookielist.append(cookie.decode("utf-8").rstrip())
    errc = process.returncode

    fer_url = "https://hr.ferrari.com/cvo3ferrari/jsp/repeatbody.jsp?jkcptlva"

    cookies = {
        'spcookie': cookielist[0],
        'JSESSIONID': cookielist[1]
        }

    data_chunk_one = [
        ('m_cParameterCache', 'mgprgdtjgr'),
        ('portlet', 'hvse_psearch_portlet.jsp'),
        ('query', 'hvse_qapplopensearch'),
        ('IdPortlet', 'wwomk'),
        ('name', 'Repeat1'),
        ('fields',
        'DSAPPLIC,DSRULE,DSJOBAREA,CPROWNUM,DSGEOAREA,IDCODREFF,FLVISJOBAREA,FLVISJOBRULE,FLSEARCH,DSRECJOB,DSRECSEC,DTSTARTVL1,DTENDVL1,TIPO,FLCUSTFIELD,TEAPPLIC'
        ),
        ('parameters',
        'GSEPARAM=PARADEING,GIDLANGUAGE=ENG,GSECOMPANY=000000,IDBRAND=,IDJOBAREA=,IDJOBFUNC=,DTSTARTVL=,IDCODREF=,IDSTATE=,IDGEOAREA=,IDRECSEC=,IDRECJOB=,IDCOMPORG=,IDDEPENDEN=,TEMPFLCV=N,OrderBy=9   DESC'
        ),
        ('parmstype', 'C,C,C,C,C,C,D,C,C,C,C,C,C,C,C,C'),
        ('vars', ''),
        ('varlist', ''),
        ('n_row', '10'),
        ('n_col', '1'),
        ('max_rec', '-1'),
        ('page', '1'),
        ('npage_next', '5'),
        ('navbar', 'top'),
        ('floating', 'false'),
        ('portlet_check', 'e07936ce30ace95114a4d26910cc1851')
        ]

    data_chunk_two = [
        ('m_cParameterCache', 'mgprgdtjgr'),
        ('portlet', 'hvse_psearch_portlet.jsp'),
        ('query', 'hvse_qapplopensearch'),
        ('IdPortlet', 'wwomk'),
        ('name', 'Repeat1'),
        ('fields',
        'DSAPPLIC,DSRULE,DSJOBAREA,CPROWNUM,DSGEOAREA,IDCODREFF,FLVISJOBAREA,FLVISJOBRULE,FLSEARCH,DSRECJOB,DSRECSEC,DTSTARTVL1,DTENDVL1,TIPO,FLCUSTFIELD,TEAPPLIC'
        ),
        ('parameters',
        'GSEPARAM=PARADEING,GIDLANGUAGE=ENG,GSECOMPANY=000000,IDBRAND=,IDJOBAREA=,IDJOBFUNC=,DTSTARTVL=,IDCODREF=,IDSTATE=,IDGEOAREA=,IDRECSEC=,IDRECJOB=,IDCOMPORG=,IDDEPENDEN=,TEMPFLCV=,OrderBy=10 DESC'
        ),
        ('parmstype', 'C,C,C,C,C,C,D,C,C,C,C,C,C,C,C,C'),
        ('vars', ''),
        ('varlist', ''),
        ('n_row', '10'),
        ('n_col', '1'),
        ('max_rec', '-1'),
        ('page', '1'),
        ('npage_next', '5'),
        ('navbar', 'top'),
        ('floating', 'false'),
        ('portlet_check', 'e07936ce30ace95114a4d26910cc1851')
        ]

    data_chunks = [data_chunk_one, data_chunk_two]
    for dc in data_chunks:
        try:
            get_ferrari_jobs(requests.post(fer_url, cookies=cookies, data=dc))
        except requests.exceptions.RequestException as e:
            print("An exception occured while connecting to FERRARI")
            print(e)

    with open(JSON_PATH + "FER.json", "w") as fer_fo:
        json.dump(fer_dict, fer_fo)
    if(fer_dict):
        with open(MARKUP_PATH + "FER", "w") as fer_mkp_fo:
            fer_mkp_fo.write(_count_pre + str(len(fer_dict)) + _count_end + "\n\n")
            for k in fer_dict:
                fer_mkp_fo.write(_content_pre + k + _content_mid + fer_dict[k] + _content_end)
                fer_mkp_fo.write("\n\n")
    else:
        with open(MARKUP_PATH + "FER", "w") as fer_mkp_fo:
            fer_mkp_fo.write(_empty + "\n\n")


#HAAS
def haas():
    haas_dict = OrderedDict()
    haas_pre_url = "https://haasf1team.applytojob.com"
    haas_url = haas_pre_url + "/apply/jobs/"

    try:
        r = requests.get(haas_url)
    except requests.exceptions.RequestException as e:
        print("An exception occured while connecting to HAAS")
        print(e)

    soup = BeautifulSoup(r.content, 'html.parser')
    tag = soup.find_all("a", class_ = "job_title_link")

    for has in tag:
        haas_dict[has.text] = haas_pre_url + has.get('href')
    
    with open(JSON_PATH + "HAS.json", "w") as haas_fo:
        json.dump(haas_dict, haas_fo)
    if(haas_dict):
        with open(MARKUP_PATH + "HAS", "w") as haas_mkp_fo:
            haas_mkp_fo.write(_count_pre + str(len(haas_dict)) + _count_end + "\n\n")
            for k in haas_dict:
                haas_mkp_fo.write(_content_pre + k + _content_mid + haas_dict[k] + _content_end)
                haas_mkp_fo.write("\n\n")
    else:
        with open(MARKUP_PATH + "HAS", "w") as haas_mkp_fo:
            haas_mkp_fo.write(_empty + "\n\n")


#RENAULT
def renault():
    renault_dict = OrderedDict()
    renault_pre_url = "https://www.renaultsport.com/"
    renault_url = renault_pre_url + "-Emplois-.html"

    try:
        r = requests.get(renault_url)
    except requests.exceptions.RequestException as e:
        print("An exception occured while connecting to HAAS")
        print(e)

    soup = BeautifulSoup(r.content, 'html.parser')
    tag = soup.find_all("h1", class_ = "h4")

    for ren in tag:
        renault_dict[ren.text] = renault_pre_url + ren.parent.parent.get('href')

    with open(JSON_PATH + "REN.json", "w") as renault_fo:
        json.dump(renault_dict, renault_fo)
    if(renault_dict):
        with open(MARKUP_PATH + "REN", "w") as renault_mkp_fo:
            renault_mkp_fo.write(_count_pre + str(len(renault_dict)) + _count_end + "\n\n")
            for k in renault_dict:
                renault_mkp_fo.write(_content_pre + k + _content_mid + renault_dict[k] + _content_end)
                renault_mkp_fo.write("\n\n")
    else:
        with open(MARKUP_PATH + "REN", "w") as renault_mkp_fo:
            renault_mkp_fo.write(_empty + "\n\n")


#REDBULL
def redbull():
    rbr_dict = OrderedDict()
    rbr_url = "http://redbullracing.redbull.com/careerslisting"

    try:
        r = requests.get(rbr_url)
    except requests.exceptions.RequestException as e:
        print("An exception occured while connecting to RED BULL")
        print(e)

    soup = BeautifulSoup(r.content, 'html.parser')

    tag = soup.find_all("span", class_ = "jobslist_listing_item_title_text")
    tag_ext = soup.select('a.button.button--primary.button--square.jobslist_listing_item_apply')

    for rbr, rbr_jobs_url in zip(tag, tag_ext):
        rbr_dict[rbr.text] = rbr_jobs_url.get('href')

    with open(JSON_PATH + "RBR.json", "w") as rbr_fo:
        json.dump(rbr_dict, rbr_fo)
    if(rbr_dict):
        with open(MARKUP_PATH + "RBR", "w") as rbr_mkp_fo:
            rbr_mkp_fo.write(_count_pre + str(len(rbr_dict)) + _count_end + "\n\n")
            for k in rbr_dict:
                rbr_mkp_fo.write(_content_pre + k + _content_mid + rbr_dict[k] + _content_end)
                rbr_mkp_fo.write("\n\n")
    else:
        with open(MARKUP_PATH + "RBR", "w") as rbr_mkp_fo:
            rbr_mkp_fo.write(_empty + "\n\n")


#SAUBER
def sauber():
    sauber_dict = OrderedDict()
    sauber_url = "https://www.sauberf1team.com/jobs"

    try:
        r = requests.get(sauber_url)
    except requests.exceptions.RequestException as e:
        print("An exception occured while connecting to SAUBER")
        print(e)

    soup = BeautifulSoup(r.content, 'html.parser')
    tag = soup.find_all("div", class_ = "jobs_single_listing")

    for sau in tag:
        sauber_dict[sau.span.text] = sau.a.get('href')

    with open(JSON_PATH + "SAU.json", "w") as sauber_fo:
        json.dump(sauber_dict, sauber_fo)
    if(sauber_dict):
        with open(MARKUP_PATH + "SAU", "w") as sauber_mkp_fo:
            sauber_mkp_fo.write(_count_pre + str(len(sauber_dict)) + _count_end + "\n\n")
            for k in sauber_dict:
                sauber_mkp_fo.write(_content_pre + k + _content_mid + sauber_dict[k] + _content_end)
                sauber_mkp_fo.write("\n\n")
    else:
        with open(MARKUP_PATH + "SAU", "w") as sauber_mkp_fo:
            sauber_mkp_fo.write(_empty + "\n\n")


#MCLAREN
def mclaren():
    mc_dict = OrderedDict()
    mc_pre_url = "https://careers.mclaren.com"
    mc_url = mc_pre_url + "/go/Racing/724201/?utm_source=careersite"

    try:
        r = requests.get(mc_url)
    except requests.exceptions.RequestException as e:
        print("An exception occured while connecting to McLAREN")
        print(e)
    
    soup = BeautifulSoup(r.content, 'html.parser')
    tag = soup.find_all("a", class_ = "jobTitle-link")

    for mc in tag:
        mc_dict[mc.text] = mc_pre_url + mc.get('href')

    with open(JSON_PATH + "MCL.json", "w") as mc_fo:
        json.dump(mc_dict, mc_fo)
    if(mc_dict):
        with open(MARKUP_PATH + "MCL", "w") as mc_mkp_fo:
            mc_mkp_fo.write(_count_pre + str(len(mc_dict)) + _count_end + "\n\n")
            for k in mc_dict:
                mc_mkp_fo.write(_content_pre + k + _content_mid + mc_dict[k] + _content_end)
                mc_mkp_fo.write("\n\n")
    else:
        with open(MARKUP_PATH + "MCL", "w") as mc_mkp_fo:
            mc_mkp_fo.write(_empty + "\n\n")


#WILLIAMS
def williams():
    williams_dict = OrderedDict()
    williams_pre_url = "http://www.williamsf1.com"
    williams_url = williams_pre_url + "/pages/careers/WMR"

    try:
        r = requests.get(williams_url)
    except requests.exceptions.RequestException as e:
        print("An exception occured while connecting to WILLIAMS WMR")
        print(e)

    soup = BeautifulSoup(r.content, 'html.parser')
    tag = soup.find_all("div", class_ = "job-title")
    
    for wil in tag:
        try:
            williams_dict[wil.a.text[1:]] = williams_pre_url + wil.a.get('href')
        except AttributeError:
            pass

    with open(JSON_PATH + "WIL.json", "w") as williams_fo:
        json.dump(williams_dict, williams_fo)
    if(williams_dict):
        with open(MARKUP_PATH + "WIL", "w") as williams_mkp_fo:
            williams_mkp_fo.write(_count_pre + str(len(williams_dict)) + _count_end + "\n\n")
            for k in williams_dict:
                williams_mkp_fo.write(_content_pre + k + _content_mid + williams_dict[k] + _content_end)
                williams_mkp_fo.write("\n\n")
    else:
        with open(MARKUP_PATH + "WIL", "w") as williams_mkp_fo:
            williams_mkp_fo.write(_empty + "\n\n")


#TOROROSSO
def toro():
    toro_dict = OrderedDict()
    toro_url = "https://portal.tororosso.com/Jobs/SitePages/ViewJobOpportunities.aspx"

    try:
        r = requests.get(toro_url)
    except requests.exceptions.RequestException as e:
        print("An exception occured while connecting to TORO ROSSO")
        print(e)

    soup = BeautifulSoup(r.content, 'html.parser')
    tag = soup.find_all("td", class_ = "ms-vb-title")

    for tor in tag:
        toro_dict[tor.a.text] = tor.a.get('href').replace("&amp", "&")

    with open(JSON_PATH + "TOR.json", "w") as toro_fo:
        json.dump(toro_dict, toro_fo)
    if(toro_dict):
        with open(MARKUP_PATH + "TOR", "w") as toro_mkp_fo:
            toro_mkp_fo.write(_count_pre + str(len(toro_dict)) + _count_end + "\n\n")
            for k in toro_dict:
                toro_mkp_fo.write(_content_pre + k + _content_mid + toro_dict[k] + _content_end)
                toro_mkp_fo.write("\n\n")
    else:
        with open(MARKUP_PATH + "TOR", "w") as toro_mkp_fo:
            toro_mkp_fo.write(_empty + "\n\n")

#MAIN
def main():

    pool = Pool(processes=16)

    constructors = [ferrari, haas, redbull, sauber, renault, mercedes, mclaren, williams, toro]
    for i in constructors:
        pool.apply_async(i)

    pool.close()
    pool.join()


if __name__ == '__main__':
    main()
