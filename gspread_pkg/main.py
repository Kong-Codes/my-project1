import logging
import gspread
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException
import os
from dotenv import load_dotenv

load_dotenv()
KEY = os.getenv("PROJECT_1202")
PATH = os.getenv("FILE_PATH")

link = "https://www.lusha.com/company-search/accounting/10/canada/193/page/2/"


def chrome_driver():
    option = webdriver.ChromeOptions()
    option.add_argument('--headless')
    drivers = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=option)
    return drivers


gc = gspread.service_account(PATH)


def open_spreadsheet(sheet_name):
    """
    This opens a spreadsheet already created on Google sheet
    """
    if isinstance(sheet_name, str):
        sh = gc.open(sheet_name)
        logging.info("spreadsheet opened")
        return sh
    else:
        raise ValueError("The sheet name expected a string object")


def create_spreadsheet(sheet_name):
    """
    This creates a new spreadsheet file in a Google sheet
    """
    if isinstance(sheet_name, str):
        sh = gc.create(sheet_name)
        logging.info("Spreadsheet created")
        return sh
    else:
        raise ValueError("The sheet name expected a string object")


def select_spreadsheet(filename, sheet_name):
    """
    This function  selects the preferred worksheet
    :param filename: This is the name of the spreadsheet
    :param sheet_name: This is the name of the desired worksheet in str format
    """
    if isinstance(filename, str) and isinstance(sheet_name, str):
        worksheets = open_spreadsheet(filename).worksheet(sheet_name)
        logging.info(f"Worksheet {sheet_name} has been loaded")
        return worksheets
    else:
        raise ValueError("The input expected a string object")


def spreadsheet_format(filename, sheet_name, first_column, second_column):
    """
    This functon is for the formatting of the spreadsheet
    :param sheet_name: Name of current worksheet
    :param filename: Name of spreadsheet
    :param first_column: This is the name of the start column in the range in str format
    :param second_column: This is the name of the end column in the range in str format
    """
    if (isinstance(filename, str) and isinstance(sheet_name, str)
            and isinstance(first_column, str) and isinstance(second_column, str)):
        formats = (select_spreadsheet(filename, sheet_name).format
                   (f"{first_column}:{second_column}", {'textFormat': {'bold': True}}))
        logging.info("Worksheet columns format has been set")
        return formats
    else:
        raise ValueError("The input expected a string object e.g 'A1' for the cols and rows input."
                         "Wrong input expected a string object.")


def new_worksheet(filename, new_name, rows, columns):
    """
    This function creates a new worksheet within the spreadsheet.
    :param filename: This is the name of the spreadsheet file
    :param new_name: Name of the new worksheet
    :param rows: Number of desired rows
    :param columns: Number of desired columns
    """

    if (isinstance(rows, int) and isinstance(columns, int) and
            isinstance(filename, str) and isinstance(new_name, str)):
        open_s = open_spreadsheet(filename)
        sheet_names = [s.title for s in open_s.worksheets()]
        if new_name not in sheet_names:
            open_spreadsheet(filename).add_worksheet(new_name, rows, columns)
            logging.info("Worksheet created")
        else:
            raise FileExistsError("This worksheet already exists")
    else:
        raise ValueError("The input expected a number/integer for the "
                         "rows ands cols input, other inputs are strings")


if __name__ == "__main__":
    driver = chrome_driver()
    driver.get(link)
    open_spreadsheet("project 1202")
    worksheet = select_spreadsheet("project 1202", "Sheet1")
    spreadsheet_format("project 1202", "Sheet1", "A1", "C1")
    worksheet.clear()
    worksheet.update("A1", "Company Name")
    worksheet.update("B1", "Company Link")
    worksheet.update("C1", "Company LinkedIn")

    num = 1
    linked = []
    links = driver.find_elements(By.CSS_SELECTOR, value='.directory-content-box-inner a')
    for link in links:
        linked.append(link.get_attribute('href'))
    for links in linked:
        num += 1
        driver.get(links)
        company_name = None
        while not company_name:
            try:
                txt = driver.find_element(By.TAG_NAME, value='h1')
                company_name = txt.text
            except NoSuchElementException:
                company_name = "None"
        company_link = None
        while not company_link:
            try:
                linke = driver.find_element(By.XPATH, value='/html/body/main/div[1]/div/section[1]/div/div[1]'
                                                            '/div/div[2]/a')
                company_link = linke.get_attribute('href')
            except NoSuchElementException:
                company_link = "None"
        linkedin = None
        while not linkedin:
            try:
                texts = driver.find_element(By.CSS_SELECTOR, value='.company-details-socials a')
                linkedin = texts.get_attribute('href')
            except NoSuchElementException:
                linkedin = "None"

        worksheet.update(f"A{num}", company_name)
        worksheet.update(f"B{num}", company_link)
        worksheet.update(f"C{num}", linkedin)
