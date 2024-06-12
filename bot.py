from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager  # pip install webdriver-manager
from selenium.webdriver.common.by import By
import time

PREFS = {"profile.default_content_setting_values.notifications": 2}
COLUMNS = ["Ordine", "SerialN", "Tipologia", "Indirizzo", "FasciaOraria", "Nominativo", "TeleLetto", "Pod", "NumTelef"]
IREN_URL = "https://iren-ii.fs.ocs.oraclecloud.com/"
# Without specifying the path
CHROME_DRIVER_PATH = ChromeDriverManager().install()


class Bot:
    def __init__(self):
        # TODO: Dati da prendere forse con un dict e non una lista: controllare documentazione
        self.data = []
        self.data.append(COLUMNS)
        self.chrome_options = webdriver.ChromeOptions()

        # For maintain open chrome
        self.chrome_options.add_experimental_option(name="detach", value=True)
        # For disable chrome notifications pop up
        self.chrome_options.add_experimental_option("prefs", PREFS)

        self.service = ChromeService(executable_path=CHROME_DRIVER_PATH)
        self.driver = webdriver.Chrome(service=self.service, options=self.chrome_options)
        self.actions = ActionChains(self.driver)

        self.driver.get(IREN_URL)

    def log_in(self, username: str, password: str):
        self.driver.find_element(By.ID, "username").send_keys(username)
        self.driver.find_element(By.ID, "password").send_keys(password)
        self.driver.find_element(By.ID, "sign-in").click()

        # If maximum sessions are exceeded
        try:
            self.driver.implicitly_wait(1)
            self.driver.find_element(By.ID, "delsession").click()
        except NoSuchElementException:
            pass
        else:
            self.driver.find_element(By.ID, "password").send_keys(password)
            self.driver.find_element(By.ID, "sign-in").click()

    def go_to_activity(self):
        self.driver.implicitly_wait(5)
        self.driver.find_element(By.CLASS_NAME, "jbf-form-item").send_keys("Zolfaroli David")
        self.driver.find_element(By.CLASS_NAME, "search-results-list").click()

        # Make element visible
        element = self.driver.find_element(By.CLASS_NAME, "effective-list-item")
        self.driver.execute_script("arguments[0].style.visibility = 'visible';", element)

        self.driver.find_element(By.CLASS_NAME, "effective-list-item").click()
        self.driver.find_element(By.CLASS_NAME, "icon-route").click()
        self.driver.implicitly_wait(2)

        self.driver.find_element(By.XPATH, '//*[@id="dashboard-content"]/div[2]/div/div[3]').click()

    def get_data(self):
        def get_single_data(xpath: str):
            data = self.driver.find_element(By.XPATH, xpath).text
            self.row.append(data)

        # Make visible all the rows
        while True:
            try:
                self.driver.find_element(By.CLASS_NAME, "btn-pagination-button").click()
            except NoSuchElementException:
                break

        activities = self.driver.find_element(
            By.XPATH,
            '//*[@id="predefined-layout"]/div[5]/div/div/section/div'
        ).find_elements(By.CLASS_NAME, "grid-row")

        for n in range(len(activities)):
            self.row = []

            # To be reviewed
            activity = self.driver.find_element(
                By.XPATH,
                '//*[@id="predefined-layout"]/div[5]/div/div/section/div'
            ).find_elements(By.CLASS_NAME, "grid-row")[n]

            activity.click()

            get_single_data('//*[@id="id_index_27"]')  # Ordine di lavoro
            get_single_data('//*[@id="id_index_30"]')  # Serial number
            get_single_data('//*[@id="id_index_39"]')  # Tipologia attività
            get_single_data('//*[@id="id_index_48"]')  # Indirizzo
            get_single_data('//*[@id="id_index_1308"]')  # Fascia oraria
            get_single_data('//*[@id="id_index_44"]')  # Nominativo
            get_single_data('//*[@id="id_index_130"]')  # Regolarmente teleletto
            get_single_data('//*[@id="id_index_118"]')  # Pom
            # get_single_data(activity, '')  # Numero di telefono

            self.data.append(self.row)

            self.driver.back()

        return self.data
