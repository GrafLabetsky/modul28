Тестирование протестировать новый интерфейс авторизации в личном кабинете от заказчика Ростелеком Информационные Технологии.

В проект использовались: PageObject, Selenium и PyTest.

В корневой папке находятся файлы chromedriver.exe для запуска тестов с браузером google chrome, requirements.txt для установки необходимых для тестирования библиотек, settings.py с тестовыми данными.

Папка tests содержит файл для запуска автотестов: test

Папка pages содержит следующие файлы: base_page.py - базовая страница, от которой унаследованы все остальные классы, auth_page.py - содержит класс для страницы авторизация, registr_page.py - содержит класс для страницы регистрация 
locators.py - список локаторов на веб страницах, 

Для запуска тестов необходимо установить библиотеки командой:
- pip install -r requirements.txt

Запуск тестов при помощи команд в консоли:

- python -m pytest -v --driver Chrome --driver-path chromedriver.exe tests/test.py

Ссылка на тест кейсы: https://docs.google.com/spreadsheets/d/1_Ijgn-lrIk70E9vSyNRXjH20IRuU19qvDXzVrQU0c-M/edit?usp=sharing

P.S. Из-за появляющейся капчи не все тесты могут пройти коректно.