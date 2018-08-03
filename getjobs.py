#!/usr/bin/env python3

import json
import requests
import time

from bs4 import BeautifulSoup
from multiprocessing import Pool
from subprocess import Popen, PIPE


#MERCEDES
def mercedes():
    merc_dict = {}
    merc_pre_url = "http://careers.mercedesamgf1.com"
    merc_url = merc_pre_url + "/vacancies/?s_keywords="

    r = requests.get(merc_url)
    soup = BeautifulSoup(r.content, 'html.parser')
    tag = soup.find_all("div", class_ = "job-item")

    for merc in tag:
        merc_dict[merc.a.text] = merc_pre_url + merc.a.get('href')
    with open("MER.json", "w") as merc_fo:
        json.dump(merc_dict, merc_fo)


#FERRARI
def ferrari():
    fer_dict = {}
    cookielist=[]
    fer_job_url = "http://corporate.ferrari.com/en/career/career-opportunities"
    
    def get_ferrari_jobs(r):
        soup = BeautifulSoup(r.content, 'html.parser')
        tag = soup.find_all("span", class_="rs_lab_prsearch")
        for fer in tag:
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
        get_ferrari_jobs(requests.post(fer_url, cookies=cookies, data=dc))

    with open("FER.json", "w") as fer_fo:
        json.dump(fer_dict, fer_fo)


#HAAS
def haas():
    haas_dict = {}
    haas_pre_url = "https://haasf1team.applytojob.com"
    haas_url = haas_pre_url + "/apply/jobs/"

    r = requests.get(haas_url)
    soup = BeautifulSoup(r.content, 'html.parser')
    tag = soup.find_all("a", class_ = "job_title_link")

    for has in tag:
        haas_dict[has.text] = haas_pre_url + has.get('href')

    with open("HAS.json", "w") as haas_fo:
        json.dump(haas_dict, haas_fo)


#RENAULT
def renault():
    renault_dict = {}
    renault_pre_url = "https://www.renaultsport.com/"
    renault_url = renault_pre_url + "-Emplois-.html"

    r = requests.get(renault_url)
    soup = BeautifulSoup(r.content, 'html.parser')
    tag = soup.find_all("h1", class_ = "h4")

    for ren in tag:
        renault_dict[ren.text] = renault_pre_url + ren.parent.parent.get('href')

    with open("REN.json", "w") as renault_fo:
        json.dump(renault_dict, renault_fo)


#REDBULL
def redbull():
    rbr_dict = {}
    rbr_url = "http://redbullracing.redbull.com/careerslisting"

    r = requests.get(rbr_url)
    soup = BeautifulSoup(r.content, 'html.parser')

    tag = soup.find_all("span", class_ = "jobslist_listing_item_title_text")
    tag_ext = soup.select('a.button.button--primary.button--square.jobslist_listing_item_apply')

    for rbr, rbr_jobs_url in zip(tag, tag_ext):
        rbr_dict[rbr.text] = rbr_jobs_url.get('href')

    with open("RBR.json", "w") as rbr_fo:
        json.dump(rbr_dict, rbr_fo)


#SAUBER
def sauber():
    sauber_dict = {}
    sauber_url = "https://www.sauberf1team.com/jobs"

    r = requests.get(sauber_url)
    soup = BeautifulSoup(r.content, 'html.parser')
    tag = soup.find_all("div", class_ = "jobs_single_listing")

    for sau in tag:
        sauber_dict[sau.span.text] = sau.a.get('href')

    with open("SAU.json", "w") as sauber_fo:
        json.dump(sauber_dict, sauber_fo)


#MCLAREN
def mclaren():
    mc_dict = {}
    mc_pre_url = "https://careers.mclaren.com"
    mc_url = mc_pre_url + "/go/Racing/724201/?utm_source=careersite"

    r = requests.get(mc_url)
    soup = BeautifulSoup(r.content, 'html.parser')
    tag = soup.find_all("a", class_ = "jobTitle-link")

    for mc in tag:
        mc_dict[mc.text] = mc_pre_url + mc.get('href')

    with open("MCL.json", "w") as mc_fo:
        json.dump(mc_dict, mc_fo)


#WILLIAMS
def williams():
    williams_dict = {}
    williams_pre_url = "http://www.williamsf1.com"
    williams_url = williams_pre_url + "/pages/careers/WMR"
    williams_url_ajl = williams_pre_url + "/pages/careers/WAE"

    def get_williams_jobs(r):
        soup = BeautifulSoup(r.content, 'html.parser')
        tag = soup.find_all("div", class_ = "job-title")
        for wil in tag:
            try:
                williams_dict[wil.a.text[1:]] = williams_pre_url + wil.a.get('href')
            except AttributeError:
                pass

    r = requests.get(williams_url)
    r_ajl = requests.get(williams_url_ajl)

    wil_categories = [r, r_ajl]
    for wc in wil_categories:
        get_williams_jobs(wc)

    with open("WIL.json", "w") as williams_fo:
        json.dump(williams_dict, williams_fo)


#TOROROSSO
def toro():
    toro_dict = {}
    toro_url = "https://portal.tororosso.com/Jobs/SitePages/ViewJobOpportunities.aspx"

    r = requests.get(toro_url)
    soup = BeautifulSoup(r.content, 'html.parser')
    tag = soup.find_all("td", class_ = "ms-vb-title")

    for tor in tag:
        toro_dict[tor.a.text] = tor.a.get('href').replace("&amp", "&")

    with open("TOR.json", "w") as toro_fo:
        json.dump(toro_dict, toro_fo)


def main():

    start = time.time()
    pool = Pool(processes=16)

    constructors = [ferrari, haas, redbull, sauber, renault, mercedes, mclaren, williams, toro]
    for i in constructors:
        pool.apply_async(i)

    pool.close()
    pool.join()
    print (time.time() - start)


if __name__ == '__main__':
    main()
