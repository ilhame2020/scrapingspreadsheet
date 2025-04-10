from playwright.sync_api import sync_playwright
import pandas as pd
import time


# Login credentials
LOGIN_URL = "https://plateforme.smit.gov.ma/moovapps/easysite/workplace"
BASE_URL =  "https://plateforme.smit.gov.ma"
SCRAPE_URL = "https://plateforme.smit.gov.ma/moovapps/easysite/workplace/applications/application-programme-d-accompagnement-tpmet-0/index"
USERNAME = "IncubateurAZ@sdratlastourismebmk.ma"
PASSWORD = "azi2030"

with sync_playwright() as p:
    # Launch browser
    browser = p.chromium.launch()  # Change to True for headless mode
    page = browser.new_page()

    # Open login page
    page.goto(LOGIN_URL, timeout=60000)

        # Fill in login details (adjust selectors if necessary)
    page.fill('input[type="text"]', USERNAME)  # Update selector if needed
    page.fill('input[type="password"]', PASSWORD)  # Update selector if needed
    page.click('button[title="Connexion"]')  # Adjust if login button is different

    # Wait for login to complete
    page.wait_for_load_state("networkidle")

    # Navigate to the target page
    page.goto(SCRAPE_URL)
    page.wait_for_load_state("networkidle")  

     # Click on the "Show 200 rows" option
    try:
        page.click('.itemsperpage a')  # Adjust selector to match the actual button
        print("dod")
        page.click('a:has(span:text("250"))')  # Adjust selector if it's inside a dropdown
       
        page.wait_for_function("document.querySelectorAll('table tr').length >= 250")

  # Wait for data to load
    except:
        print("Could not find the 'Show 200 rows' option.")
    # Initialize storage for scraped data
    data = []
    rows = page.query_selector_all("table tr")  # Adjust selector if necessary
    if len(rows) >= 500:
        print("✅ 250 rows successfully loaded!")
    else:
        print(f"⚠️ Only {len(rows)} rows loaded.")
    
    links_to_visit = []  # Pour stocker les liens à visiter après

    for i, row in enumerate(rows):
        cols = row.query_selector_all("td")
        row_data = []

        for j, col in enumerate(cols):
            try:
                text = col.inner_text().strip()
            except Exception as e:
                print(f"⚠️ Couldn't read a column: {e}")
                text = ""

            # Si on est à partir de la 3e ligne et 2e colonne
            if i >= 2 and j == 1:
                print(text)
                a_tag = col.query_selector("a.postaction")
                if a_tag:
                    href = a_tag.get_attribute("href")
                    if href:
                        link = href if href.startswith("http") else BASE_URL + href
                        links_to_visit.append(link)
        if row_data:
            data.append(row_data)

    # 🧭 Ensuite, visiter les liens collectés
    for link in links_to_visit:
        print(f"🔗 Visiting: {link}")
        try:
            page.goto(link)
            page.wait_for_load_state("load")
            time.sleep(1)

            elements = page.query_selector_all(".readonly-field")

            ref = page.inner_text("span.document-label-reference")
            phase = page.inner_text("span.document-label-task")
            structureJuridique = elements[0] if elements else None
            catégorieDuProjet = elements[1] if elements else None
            domaineDactivité = elements[3] if elements else None
            genre = elements[4] if elements else None
            nomPrénom = elements[5] if elements else None
            dateDeNaissance = elements[6] if elements else None
            numéroCNIE = elements[8] if elements else None
            numéroDeTéléphone = elements[9] if elements else None
            nomDuProjet= elements[14] if elements else None
            commune = elements[16] if elements else None
            phaseDavancementDuProjet = elements[17] if elements else None
            coûtDuProjetEnDH =elements[21] if elements else None



            data.append([ref, phase, structureJuridique, catégorieDuProjet, domaineDactivité,
                          genre, nomPrénom, dateDeNaissance, numéroCNIE, numéroDeTéléphone, 
                          nomDuProjet, commune, phaseDavancementDuProjet, coûtDuProjetEnDH])

            page.go_back()
            page.wait_for_load_state("networkidle")
            time.sleep(1)

        except Exception as e:
            print(f"⚠️ Failed to scrape {link}: {e}")

                # links = [col.query_selector(".postaction").get_attribute("href") for col in cols if col.query_selector(".postaction")]
                # print(f"Found {len(links)} links to scrape.")
                # for link in links:
                #     # Open the reference page in the same tab
              
          

    # Save data to Excel
    if data:
        df = pd.DataFrame(data, columns=[
                "ref",
    "phase",
    "structureJuridique",
    "catégorieDuProjet",
    "domaineDactivité",
    "genre",
    "nomPrénom",
    "dateDeNaissance",
    "numéroCNIE",
    "numéroDeTéléphone",
    "nomDuProjet",
    "commune",
    "phaseDavancementDuProjet",
    "coûtDuProjetEnDH",
    "link",
    "title",
    "description"])
             # Update column names
        df.to_excel("scraped_data.xlsx", index=False)
        print("All pages scraped and data saved!")
    else:
        print("No data found.")

    # Close browser
    browser.close()


      