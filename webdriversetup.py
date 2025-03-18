from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd

# Path to your Edge WebDriver
driver_path = 'C:/Users/ilham/Downloads/edgedriver_win64/msedgedriver.exe'  # Modify path

# Set up Selenium WebDriver (Edge in this case)
driver = webdriver.Edge(executable_path=driver_path)

# Open the login page
login_url = "https://plateforme.smit.gov.ma/moovapps/easysite/workplace"
driver.get(login_url)

# Wait for page to load
time.sleep(3)  # You can also use WebDriverWait here for better handling

# Find username and password fields, and login
username = driver.find_element(By.NAME, "username")  # Update with correct field name
password = driver.find_element(By.NAME, "password")  # Update with correct field name

# Send login credentials
username.send_keys("IncubateurAZ@sdratlastourismebmk.ma")
password.send_keys("azi2030")
password.send_keys(Keys.RETURN)  # Press Enter after filling in password

# Wait for login to complete (adjust as needed)
time.sleep(5)

# After login, navigate to the protected page
url = "https://plateforme.smit.gov.ma/moovapps/easysite/workplace/applications/application-programme-d-accompagnement-tpmet-0/index"
driver.get(url)

# Wait for page to load
time.sleep(5)

# Extract the data (adjust the selector for the table)
data = []
rows = driver.find_elements(By.XPATH, "//table//tr")  # Modify XPath if needed

for row in rows:
    cols = row.find_elements(By.TAG_NAME, "td")
    if cols:
        data.append([col.text.strip() for col in cols])

# Save data to Excel
if data:
    df = pd.DataFrame(data, columns=["Column1", "Column2", "Column3"])  # Update column names
    df.to_excel("scraped_data.xlsx", index=False)
    print("Data scraped and saved!")
else:
    print("No data found.")

# Close the browser
driver.quit()
