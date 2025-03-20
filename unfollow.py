from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time

options = webdriver.FirefoxOptions()
options.add_argument('--window-size=1920,1080')
options.add_argument(
    '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
)
options.binary_location = '/nix/store/pkqh0pddz268mvh55p8x3snpjz3ia8gk-firefox-127.0/bin/firefox'
options.set_preference("dom.webdriver.enabled", False)
options.set_preference('useAutomationExtension', False)

service = webdriver.firefox.service.Service(
    '/nix/store/kxz4y57xlv70567x1zbvarmn5ry2asx4-geckodriver-0.34.0/bin/geckodriver'
)
driver = webdriver.Firefox(options=options, service=service)

try:
    print("Starting Instagram automation...")
    driver.get("https://www.instagram.com/")
    time.sleep(15)  # Extended initial wait

    # Try multiple selectors for username field
    username_selectors = [
        "input[name='username']",
        "input[aria-label='Phone number, username, or email']",
        "//input[@aria-label='Phone number, username, or email']"
    ]

    username_field = None
    for selector in username_selectors:
        try:
            if selector.startswith("//"):
                username_field = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, selector)))
            else:
                username_field = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located(
                        (By.CSS_SELECTOR, selector)))
            if username_field:
                break
        except:
            continue

    if not username_field:
        raise Exception("Could not find username field")

    print("Found username field, entering credentials...")
    username_field.clear()
    username_field.send_keys("INSTAGRAM_USERNAME") #Replace your instagram username
    time.sleep(3)

    # Similar approach for password field
    password_selectors = [
        "input[name='password']", "input[aria-label='Password']",
        "//input[@aria-label='Password']"
    ]

    password_field = None
    for selector in password_selectors:
        try:
            if selector.startswith("//"):
                password_field = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, selector)))
            else:
                password_field = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located(
                        (By.CSS_SELECTOR, selector)))
            if password_field:
                break
        except:
            continue

    if not password_field:
        raise Exception("Could not find password field")

    password_field.clear()
    password_field.send_keys("INSTAGRAM_PASSWORD")  # Replace with ur Instagram Password
    time.sleep(3)

    # Multiple login button selectors
    login_selectors = [
        "button[type='submit']", "//button[@type='submit']",
        "//button[contains(text(), 'Log in')]",
        "//div[contains(text(), 'Log in')]/parent::button"
    ]

    login_button = None
    for selector in login_selectors:
        try:
            if selector.startswith("//"):
                login_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, selector)))
            else:
                login_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, selector)))
            if login_button:
                break
        except:
            continue

    if not login_button:
        raise Exception("Could not find login button")

    print("Attempting to log in...")
    login_button.click()
    input("Please complete 2FA verification manually and press Enter to continue...")
    time.sleep(5)  # Short wait after 2FA

    print("Navigating to profile...")
    # First navigate to home page to ensure we're properly logged in
    driver.get("https://www.instagram.com")
    time.sleep(10)

    # Then navigate to profile
    profile_url = "https://www.instagram.com/INSTAGRAM_USERNAME/" # Replace with your username
    driver.get(profile_url)
    time.sleep(20)

    # Verify we're on the right page
    current_url = driver.current_url
    if "login" in current_url.lower():
        print("Redirected to login, attempting to navigate again...")
        driver.get(profile_url)
        time.sleep(20)

    # Try multiple ways to verify we're on the profile page
    profile_indicators = [
        "//h2[contains(text(), 'INSTAGRAM_USERNAME')]", # Replace with your username
        "//*[contains(@class, 'profile')]//h2", "//section//h2",
        "//*[contains(@class, 'profile-page')]"
    ]

    profile_loaded = False
    for indicator in profile_indicators:
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, indicator)))
            profile_loaded = True
            break
        except:
            continue

    if not profile_loaded:
        print("Attempting alternative profile navigation...")
        try:
            # Try clicking profile icon
            profile_buttons = [
                "//a[contains(@href, '/INSTAGRAM_USERNAME')]", # Replace with your username
                "//a[contains(@href, '/profile')]",
                "//nav//a[contains(@role, 'link')]"
            ]
            for button in profile_buttons:
                try:
                    profile_link = WebDriverWait(driver, 5).until(
                        EC.element_to_be_clickable((By.XPATH, button)))
                    profile_link.click()
                    time.sleep(10)
                    break
                except:
                    continue
        except Exception as e:
            print(f"Profile navigation alternative method failed: {e}")

    # Save page source for debugging
    with open("page_source.html", "w", encoding="utf-8") as f:
        f.write(driver.page_source)

    print("Looking for following button...")
    time.sleep(5)  # Additional wait before profile verification

    # First ensure we're on the correct profile page
    profile_selectors = [
        "//h2[text()='INSTAGRAM_USERNAME']", "//span[text()='INSTAGRAM_USERNAME']",
        "//*[@class='x1lliihq x1plvlek xryxfnj x1n2onr6 x193iq5w xeuugli x1fj9vlw x13faqbe x1vvkbs x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x x1i0vuye xvs91rp xo1l8bm x5n08af x10wh9bi x1wdrske x8viiok x18hxmgj'][text()='INSTAGRAM_USERNAME']"
    ]

    profile_found = False
    for selector in profile_selectors:
        try:
            profile_name = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, selector)))
            print("Profile found, looking for following count...")
            profile_found = True
            break
        except:
            continue

    if not profile_found:
        print("Profile verification failed, continuing anyway...")

    following_selectors = [
        "//a[contains(@href, '/following') and contains(@role, 'link')]",
        "//a[contains(@href, '/following') and @tabindex='0']",
        "//div[contains(@class, '_aacl')]//a[contains(@href, '/following')]",
        "//span[contains(text(), ' following')]/ancestor::a",
        "//div[@class='_ab8w _ab94 _ab97 _ab9f _ab9k _ab9p _abcm']/a[contains(@href, '/following')]",
        "//section//div//a[contains(@href, '/following')]"
    ]

    print("Trying to find following link...")
    try:
        # Direct navigation to following page
        driver.get("https://www.instagram.com/INSTAGRAM_USERNAME/following/")
        time.sleep(10)
    except Exception as e:
        print(f"Direct navigation failed: {e}")

    print("Waiting for page to fully load...")
    time.sleep(20)  # Extended wait for page load

    following_button = None
    for selector in following_selectors:
        try:
            following_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, selector)))
            print(f"Found following button with selector: {selector}")
            break
        except:
            continue

    if not following_button:
        print("Attempting alternative method to find following button...")
        try:
            # Try to find any clickable links with numbers (following count)
            links = driver.find_elements(By.TAG_NAME, "a")
            for link in links:
                try:
                    href = link.get_attribute('href')
                    if href and 'following' in href.lower():
                        following_button = link
                        break
                except:
                    continue
        except Exception as e:
            print(f"Alternative method failed: {e}")

    if not following_button:
        raise Exception("Could not find following button")

    try:
        following_button.click()
    except:
        driver.execute_script("arguments[0].click();", following_button)
    time.sleep(15)  # Extended wait after clicking

    print("Finding unfollow buttons...")
    unfollow_selectors = [
        "//button[contains(@class, '_acan')]",
        "//button[contains(text(), 'Following')]",
        "//div[contains(text(), 'Following')]/ancestor::button",
        "//button[@type='button' and contains(., 'Following')]"
    ]

    for selector in unfollow_selectors:
        try:
            unfollow_buttons = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.XPATH, selector)))

            count = 0
            target = 1500
            print(f"Found {len(unfollow_buttons)} unfollow buttons")

            while count < target:
                try:
                    for button in unfollow_buttons:
                        try:
                            driver.execute_script("arguments[0].click();", button)
                            time.sleep(2)

                            # Try multiple selectors for confirm button
                            confirm_selectors = [
                                "//button[text()='Unfollow']",
                                "//button[contains(@class, '_a9--') and contains(@class, '_a9_1')]",
                                "//div[@role='dialog']//button[contains(text(), 'Unfollow')]"
                            ]

                            confirm_button = None
                            for selector in confirm_selectors:
                                try:
                                    confirm_button = WebDriverWait(driver, 5).until(
                                        EC.element_to_be_clickable((By.XPATH, selector)))
                                    if confirm_button:
                                        break
                                except:
                                    continue

                            if confirm_button:
                                confirm_button.click()
                                count += 1
                                print(f"Unfollowed {count} accounts")
                                time.sleep(3)

                            if count >= target:
                                break
                        except Exception as e:
                            print(f"Failed to unfollow one account: {e}")
                            continue
                    # Scroll to load more buttons if needed
                    if count < target:
                        driver.execute_script(
                            "window.scrollTo(0, document.body.scrollHeight);")
                        time.sleep(2)
                        unfollow_buttons = WebDriverWait(driver, 10).until(
                            EC.presence_of_all_elements_located(
                                (By.XPATH, selector)))

                except Exception as e:
                    print(f"Error unfollowing: {e}")
                    time.sleep(5)  # Wait longer if error occurs
                    continue
            break
        except Exception as e:
            print(f"Error with selector {selector}: {e}")
            continue

except Exception as e:
    print(f"Error occurred: {e}")
    driver.save_screenshot("error_debug.png")
finally:
    driver.quit()
