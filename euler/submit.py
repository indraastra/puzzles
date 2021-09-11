from datetime import datetime
import json
import os
import sys
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


_SESSION_FILE = '.euler-session.json'


class BadSessionException(Exception):
    pass


def load_session():
    with open(_SESSION_FILE, 'rt') as session_file:
        return json.loads(session_file.read())


def save_session(session):
    with open(_SESSION_FILE, 'wt') as session_file:
        session_file.write(json.dumps(session))


def drive_login(password=None):
    if password is None:
        password = input('euler password > ')
    browser = webdriver.Chrome()
    browser.get('https://projecteuler.net/sign_in')
    browser.find_element_by_id('username').send_keys('indraastra')
    browser.find_element_by_id('password').send_keys(password)
    browser.find_element_by_id('remember_me').click()
    browser.find_element_by_id('captcha').click()

    # Wait until login has completed.
    print('Awaiting login...')
    wait = WebDriverWait(browser, 10)
    wait.until(EC.url_changes(browser.current_url))
    print('Login completed!')

    session = {
        'password': password,
        'cookies': browser.get_cookies()
    }
    for cookie in browser.get_cookies():
        if 'expiry' in cookie:
            session['expiry'] = cookie['expiry']
            #session['cookies'] = [cookie]

    browser.quit()
    return session


def restore_session():
    if not os.path.exists(_SESSION_FILE):
        print(f'{_SESSION_FILE} not found; login required!')
        session = drive_login()
        save_session(session)

    session = load_session()

    expiry = datetime.fromtimestamp(session.get('expiry', 0))
    if not expiry or datetime.now() >= expiry:
        print(f'Session expired at {expiry}; login required!')
        session = drive_login(session['password'])
        save_session(session)

    print('Session loaded!')
    return session


def drive_submit(session, problem, solution):
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    browser = webdriver.Chrome(options=chrome_options)
    browser.get(f'https://projecteuler.net/')
    browser.delete_all_cookies()
    for cookie in session['cookies']:
        browser.add_cookie(cookie)
    browser.get(f'https://projecteuler.net/problem={problem}')
    browser.find_element_by_id('guess').send_keys(solution)
    browser.find_element_by_xpath('//input[@type="submit"]').click()

    # Wait until submit has completed.
    print('Awaiting submission...')
    wait = WebDriverWait(browser, 30)
    wait.until(EC.text_to_be_present_in_element(
        (By.ID, 'content'), 'answer'))
    print('>>>', browser.find_element_by_id('content').text)
    browser.quit()


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage: submit.py <problem> <solution>')
        sys.exit(1)

    session = restore_session()
    drive_submit(session, sys.argv[1], sys.argv[2])
