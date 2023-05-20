"""
Updates the chatbot webhook_url credentials attribute to the
new dynamic URL from the ngrok log file
"""
import re
import yaml
from yaml.loader import SafeLoader

LOG_PATH = './ngrok/ngrok.log'
CREDENTIALS_PATH = './bot/credentials.yml'
REGEX = r'https://.*ngrok-free.app'
WEBHOOK = '/webhooks/telegram/webhook'

print(f'\n[START] Updating webhook_url from {LOG_PATH} file '\
      f'to {CREDENTIALS_PATH} credentials.')

with open(LOG_PATH, 'r', encoding='utf-8') as file:
    log = file.read()

matches = re.findall(REGEX, log)
if matches:
    url = matches[0] + WEBHOOK

    with open(CREDENTIALS_PATH, 'r', encoding='utf-8') as file:
        credentials = yaml.load(file, Loader=SafeLoader)
        credentials['telegram']['webhook_url'] = url

    with open(CREDENTIALS_PATH, 'w', encoding='utf-8') as file:
        yaml.dump(credentials, file)

    print('\n[SUCCESS] Credentials successfully updated.\n'\
          f'---> webhook_url: {url}\n')
else:
    print('\n[FAIL] Credentials not updated. No URL found in the ngrok log file.\n')
