import asyncio
import json
import time
from selenium.webdriver.common.by import By as Selector
import undetected_chromedriver as uc
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from typing import Generator, Dict, List, Any

RUNNING_DIR = "." if __name__ == "__main__" else "bing"

with open(RUNNING_DIR + '/executor.js', 'r') as fp:
    executor = fp.read()

with open(RUNNING_DIR + '/detector.js', 'r') as fp:
    detector = fp.read()


async def handle_request(content: str, cookies: List[Dict[str, Any]], max_timeout: int = 60 * 10)\
        -> Generator[str, None, None]:
    script = executor.replace("{{content}}", content)
    buffer = ""

    try:
        options = webdriver.EdgeOptions()

        driver = webdriver.Edge(options=options)
        driver.get('https://www.bing.com/search?form=MY0291&OCID=MY0291&q=Bing+AI&showconv=1')

        await asyncio.sleep(2)

        # set cookies
        for cookie in cookies:
            cookie['sameSite'] = 'None'
            driver.add_cookie(cookie)

        await asyncio.sleep(10)

        # execute javascript
        driver.execute_script(script)
        driver.execute_script(detector)

        stamp = time.time()
        started = time.time()
        while time.time() - started < max_timeout:
            await asyncio.sleep(0.1)
            resp = driver.execute_script("return getText()")
            if resp is None:
                continue

            if resp == content and len(buffer) == 0:
                continue

            if resp and len(resp.strip()) > 0 and time.time() - stamp > 10:
                break

            if resp is not None and resp != buffer:
                offset = resp[len(buffer):]
                buffer = resp
                stamp = time.time()
                yield offset

        driver.quit()
    except Exception as e:
        print(str(e))
        if len(buffer.strip()) == 0:
            yield str(e)
