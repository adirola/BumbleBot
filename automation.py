from bs4 import BeautifulSoup
from selenium import webdriver;
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
import time

path = 'path to chrome driver'
service = Service(executable_path=path)
web = 'https://bumble.com/app'


options = Options()
options.add_experimental_option("debuggerAddress", "localhost:9222")
driver = webdriver.Chrome(service=service, options=options)

driver.get(web);
time.sleep(3)



gpt_promt_final = """
ChatGPT-4, I need your help to generate a follow-up message with a girl named {} on a dating application. I will provide you with relevant information about the person.

Bio Information:
{}

Beliefs:
{}

Previous Chat History:
{}

Based on this information, please generate a flirty and engaging follow-up message in more than 20 words.
"""


chat_window = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//div[@class='contact__notifications']//div[@class='contact__move-label']//span[text()='Your Move']")))
driver.execute_script("arguments[0].click();", chat_window)
time.sleep(5)

profile_element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//div[@class="profile__about"]//div[@class="p-1"]')))
bio = profile_element.text


profile_answer_element = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//div[@class="profile__section profile__section--answer"]//div')))

profile_qoute = ""

if len(profile_answer_element)>0:
    individual_element = profile_answer_element[0]
    profile_question_element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//div[@class="profile-answer"]//div[@class="profile-answer__title"]//h3')))
    profile_question_answer_element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//div[@class="profile-answer"]//div[@class="profile-answer__text"]//p')))
    profile_qoute = profile_question_element.text + profile_question_answer_element.text

html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')
parent_div = soup.find('div', {'class': 'messages-list__conversation'})
name_div_container = soup.find('div',{'class':'messages-header__name is-clickable'})
name = name_div_container.find('div').get_text();
all_divs = parent_div.find_all('div')

segrated_chat = []

for div in all_divs:
    if 'message--in' in div.get('class', []):
        child_span = div.find('span',{})
        fina_children_text = "her:"+child_span.get_text() 
        segrated_chat.append(fina_children_text)
    elif 'message--out' in div.get('class', []):
        child_span = div.find('span',{})
        fina_children_text = "me:"+child_span.get_text() 
        segrated_chat.append(fina_children_text)

fina_gpt_prompt = gpt_promt_final.format(name,bio, profile_qoute,"\n".join(segrated_chat))


driver.execute_script("window.open('');")
driver.switch_to.window(driver.window_handles[1])
driver.get("https://chat.openai.com/")
time.sleep(3)

prompt_window = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//div[@class="relative flex h-full flex-1 items-stretch md:flex-col"]//div//textarea')))
prompt_submit_button = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//div[@class="relative flex h-full flex-1 items-stretch md:flex-col"]//div//button')))
script = """
        var elm = arguments[0], txt = arguments[1];
        elm.value += txt;
        elm.dispatchEvent(new Event('keydown', {bubbles: true}));
        elm.dispatchEvent(new Event('keypress', {bubbles: true}));
        elm.dispatchEvent(new Event('input', {bubbles: true}));
        elm.dispatchEvent(new Event('keyup', {bubbles: true}));
        """       
driver.execute_script(script,prompt_window,fina_gpt_prompt)
time.sleep(5);
driver.execute_script("arguments[0].click();", prompt_submit_button)
time.sleep(5);
prompt_result_screen = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//div[@class="flex justify-between lg:block"]//div//button[@class="flex ml-auto gap-2 rounded-md p-1 hover:bg-gray-100 hover:text-gray-700 dark:text-gray-400 dark:hover:bg-gray-700 dark:hover:text-gray-200 disabled:dark:hover:text-gray-400"]')))
prompt_result_element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//div[@class="markdown prose w-full break-words dark:prose-invert light"]//p')))
prompt_result = prompt_result_element.text;


driver.switch_to.window(driver.window_handles[0])

text_area = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//div[@data-qa-role="chat-input"]//div[@class="textarea__inner"]//textarea[@class="textarea__input"]')))

actions = ActionChains(driver)
actions.move_to_element(text_area).click().send_keys(prompt_result)
actions.perform()


text_area_ghost = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//div[@data-qa-role="chat-input"]//div[@class="textarea__inner"]//textarea[@class="textarea__ghost"]')))

send_button = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//button[@class="message-field__send"]')))
# driver.execute_script("arguments[0].click();", send_button) enable to send automatic text







