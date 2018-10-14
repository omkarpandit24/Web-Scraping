from bs4 import BeautifulSoup
from selenium import webdriver
from time import sleep
from xlsxwriter import Workbook
import os
import requests
import shutil


class App:
    def __init__(self, username='abc', password='xyz', target_username='pqr',
                 path='/Desktop/instaPhotos'):
        self.username = username
        self.password = password
        self.target_username = target_username
        self.path = path
        self.driver = webdriver.Chrome()
        self.error = False
        self.main_url = 'https://www.instagram.com'
        self.driver.get(self.main_url)
        sleep(3)
        self.log_in()
        if self.error is False:
            self.close_dialog_box()
            self.open_target_profile()
        if self.error is False:
            self.scroll_down()
        if self.error is False:
            if not os.path.exists(path):
                os.mkdir(path)
            self.downloading_images()
        sleep(3)
        self.driver.close()

    def write_captions_to_excel_file(self, images, caption_path):
        print('writing to excel')
        #workbook = Workbook(caption_path + '/captions.xlsx')
        workbook = Workbook(os.path.join(caption_path, 'captions.xlsx'))
        worksheet = workbook.add_worksheet()
        row = 0
        worksheet.write(row, 0, 'Image name')       # 3 --> row number, column number, value
        worksheet.write(row, 1, 'Caption')
        row += 1
        for index, image in enumerate(images):
            filename = 'image_' + str(index) + '.jpg'
            try:
                caption = image['alt']
            except KeyError:
                caption = 'No caption exists'
            worksheet.write(row, 0, filename)
            worksheet.write(row, 1, caption)
            row += 1
        workbook.close()

    def download_captions(self, images):
        captions_folder_path = os.path.join(self.path, 'captions')
        if not os.path.exists(captions_folder_path):
            os.mkdir(captions_folder_path)
        self.write_captions_to_excel_file(images, captions_folder_path)
        '''for index, image in enumerate(images):
            try:
                caption = image['alt']
            except KeyError:
                caption = 'No caption exists for this image'
            file_name = 'caption_' + str(index) + '.txt'
            file_path = os.path.join(captions_folder_path, file_name)
            link = image['src']
            with open(file_path, 'wb') as file:
                file.write(str('link:' + str(link) + '\n' + 'caption:' + caption).encode())'''


    def downloading_images(self):
        soup = BeautifulSoup(self.driver.page_source, 'lxml')
        all_images = soup.find_all('img')
        self.download_captions(all_images)
        print('Length of all images', len(all_images))
        for index, image in enumerate(all_images):
            filename = 'image_' + str(index) + '.jpg'
            image_path = os.path.join(self.path, filename)
            link = image['src']
            print('Downloading image', index)
            response = requests.get(link, stream=True)
            try:
                with open(image_path, 'wb') as file:
                    shutil.copyfileobj(response.raw, file)  # source -  destination
            except Exception as e:
                print(e)
                print('Could not download image number ', index)
                print('Image link -->', link)

    def scroll_down(self):
        try:
            no_of_posts = self.driver.find_element_by_xpath('//span[@class="_fd86t"]')
            no_of_posts = str(no_of_posts.text).replace(',', '')  # 15,483 --> 15483
            self.no_of_posts = int(no_of_posts)
            if self.no_of_posts > 12:
                no_of_scrolls = int(self.no_of_posts/12) + 3
                try:
                    for value in range(no_of_scrolls):
                        self.driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
                        sleep(2)
                except Exception as e:
                    self.error = True
                    print(e)
                    print('Some error occurred while trying to scroll down')
            sleep(10)
        except Exception:
            print('Could not find no of posts while trying to scroll down')
            self.error = True


    def open_target_profile(self):
        try:
            search_bar = self.driver.find_element_by_xpath('//input[@class="_avvq0 _o716c"]')
            search_bar.send_keys(self.target_username)
            target_profile_url = self.main_url + '/' + self.target_username + '/'
            self.driver.get(target_profile_url)
            sleep(3)
        except Exception:
            self.error = True
            print('Could not find search bar')

    def close_dialog_box(self):
        try:
            sleep(10)
            close_btn = self.driver.find_element_by_xpath('//button[@class="_dbnr9"]')
            close_btn.click()
            sleep(1)
        except Exception:
            pass

    def close_settings_window_if_there(self):
        try:
            self.driver.switch_to.window(self.driver.window_handles[1])
            self.driver.close()
            self.driver.switch_to.window(self.driver.window_handles[0])
        except Exception as e:
            pass

    def log_in(self, ):
        try:
            log_in_button = self.driver.find_element_by_xpath('//p[@class="_76e0u"]/a[@class="_msxj2"]')
            log_in_button.click()
            try:
                user_name_input = self.driver.find_element_by_xpath('//input[@placeholder="Phone number, username, or email"]')
                user_name_input.send_keys(self.username)
                password_input = self.driver.find_element_by_xpath('//input[@placeholder="Password"]')
                password_input.send_keys(self.password)
                user_name_input.submit()
                self.close_settings_window_if_there()
            except Exception:
                print('Some exception occurred while trying to find username or password field')
                self.error = True
        except Exception:
            self.error = True
            print('Unable to find login button')


if __name__ == '__main__':
    app = App()
