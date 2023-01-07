# python -m pytest -v --driver Chrome --driver-path chromedriver.exe tests/test_auth_page.py
import pytest
from pages.auth_page import AuthPage
from pages.registr_page import RegistrPage
from pages.locators import AuthLocators
from settings import *

def test_autoriz_valid_email_pass(selenium):
    """RT-001 Тест авторизации с валидными значениями e-mail и паролем."""
    page = AuthPage(selenium)
    page.email.send_keys(Settings.valid_email)
    page.email.clear()
    page.pass_eml.send_keys(Settings.valid_password)
    page.pass_eml.clear()
    page.btn_enter.click()

    try:
        assert page.get_relative_link() == '/account_b2c/page'
    except AssertionError:
        assert 'Неверно введен текст с картинки' in page.find_other_element(*AuthLocators.error_message).text

@pytest.mark.parametrize("incor_email", [Settings.invalid_email, Settings.empty_email],
                         ids=['invalid_email', 'empty'])
@pytest.mark.parametrize("incor_passw", [Settings.invalid_password, Settings.empty_password],
                         ids=['invalid_password', 'empty'])

def test_autoriz_invalid_email_pass(selenium, incor_email, incor_passw):
    """RT-002, RT-003 "Проверка аутентификации пользователя с невалидным email и паролем:
    связка Почта+Пароль валидна, но пользователь с такими данными не зарегистрирован в системе;
    пустые значения."""
    page = AuthPage(selenium)
    page.email.send_keys(incor_email)
    page.email.clear()
    page.pass_eml.send_keys(incor_passw)
    page.pass_eml.clear()
    page.btn_enter.click()

    assert page.get_relative_link() != '/account_b2c/page'


def test_elements_of_autoriz(selenium):
    """RT-004 Проверка Формы "Авторизация" на наличие основных элементов."""
    page = AuthPage(selenium)

    assert page.menu_tub.text in page.card_of_auth.text
    assert page.email.text in page.card_of_auth.text
    assert page.pass_eml.text in page.card_of_auth.text
    assert page.btn_enter.text in page.card_of_auth.text
    assert page.forgot_password_link.text in page.card_of_auth.text
    assert page.register_link.text in page.card_of_auth.text


def test_menu_type_autoriz(selenium):
    """RT-005 Проверка названия табов в меню выбора типа авторизации."""
    try:
        page = AuthPage(selenium)
        menu = [page.tub_phone.text, page.tub_email.text, page.tub_login.text, page.tub_ls.text]
        for i in range(len(menu)):
            assert "Номер" in menu
            assert 'Почта' in menu
            assert 'Логин' in menu
            assert 'Лицевой счёт' in menu
    except AssertionError:
        print('Ошибка в имени таба Меню типа аутентификации')


def test_menu_of_type_active_autoriz(selenium):
    """RT-006 Проверка выбора таба по умолчанию в Меню выбора типа авторизации."""
    page = AuthPage(selenium)

    assert page.active_tub_phone.text == Settings.menu_type_auth[0]


def test_placeholder_name_swap(selenium):
    """RT-007 Тест смены полей ввода при смене типа авторизации."""
    page = AuthPage(selenium)
    page.tub_phone.click()

    assert page.placeholder_name.text in Settings.placeholder_name
    page.tub_email.click()
    assert page.placeholder_name.text in Settings.placeholder_name
    page.tub_login.click()
    assert page.placeholder_name.text in Settings.placeholder_name
    page.tub_ls.click()
    assert page.placeholder_name.text in Settings.placeholder_name

def test_forgot_password_link(selenium):
    """RT-008 Тест перехода к форме "восстановление пароля"."""
    page = AuthPage(selenium)
    page.driver.execute_script("arguments[0].click();", page.forgot_password_link)

    assert page.find_other_element(*AuthLocators.password_recovery).text == 'Восстановление пароля'

def test_registration_link(selenium):
    """RT-009 Тест перехода к форме "Регистрация"."""
    page = AuthPage(selenium)
    page.register_link.click()

    assert page.find_other_element(*AuthLocators.registration).text == 'Регистрация'

def test_page_logo_registration(selenium):
    """RT-010 Проверка блока с продуктовым слоганом компании на странице "Регистрация"."""
    try:
        page_reg = RegistrPage(selenium)
        assert page_reg.page_left_registration.text != ''
    except AssertionError:
        print('Элемент отсутствует в левой части формы')


def test_elements_registration(selenium):
    """RT-011 Проверка Формы "Регистрация" на наличие основных элементов."""
    try:
        page_reg = RegistrPage(selenium)
        card_of_reg = [page_reg.first_name, page_reg.last_name, page_reg.address_registration,
                       page_reg.email_registration, page_reg.password_registration,
                       page_reg.password_registration_confirm, page_reg.registration_btn]
        for i in range(len(card_of_reg)):
            assert page_reg.first_name in card_of_reg
            assert page_reg.last_name in card_of_reg
            assert page_reg.email_registration in card_of_reg
            assert page_reg.address_registration in card_of_reg
            assert page_reg.password_registration in card_of_reg
            assert page_reg.password_registration_confirm in card_of_reg
            assert page_reg.registration_btn in card_of_reg
    except AssertionError:
        print('Элемент отсутствует в форме «Регистрация»')


def test_names_elements_registration(selenium):
    """RT-012 Проверка Формы "Регистрация" на соответствие названий элементов блока требованию."""
    try:
        page_reg = RegistrPage(selenium)
        assert 'Имя' in page_reg.card_of_registration.text
        assert 'Фамилия' in page_reg.card_of_registration.text
        assert 'Регион' in page_reg.card_of_registration.text
        assert 'E-mail или мобильный телефон' in page_reg.card_of_registration.text
        assert 'Пароль' in page_reg.card_of_registration.text
        assert 'Подтверждение пароля' in page_reg.card_of_registration.text
        assert 'Продолжить' in page_reg.card_of_registration.text
    except AssertionError:
        print('Название элемента в форме «Регистрация» не соответствует Требованию')


def test_registration_valid_data(selenium):
    """RT-013 Проверка Регистрации пользователя с валидными данными: "Имя" и "Фамилия" написанных кириллицей."""
    page_reg = RegistrPage(selenium)
    page_reg.first_name.send_keys(Settings.first_name)
    page_reg.first_name.clear()
    page_reg.last_name.send_keys(Settings.last_name)
    page_reg.last_name.clear()
    page_reg.email_registration.send_keys(Settings.valid_email_reg)
    page_reg.email_registration.clear()
    page_reg.password_registration.send_keys(Settings.valid_password)
    page_reg.password_registration.clear()
    page_reg.password_registration_confirm.send_keys(Settings.valid_password)
    page_reg.password_registration_confirm.clear()
    page_reg.registration_btn.click()

    assert page_reg.find_other_element(*AuthLocators.email_confirm).text == 'Подтверждение email'

def test_registration_invalid_data(selenium):
    """RT-014 Проверка на уникальность введенного e-mail в форме "Регистрация"."""
    page_reg = RegistrPage(selenium)
    page_reg.first_name.send_keys(Settings.first_name)
    page_reg.first_name.clear()
    page_reg.last_name.send_keys(Settings.last_name)
    page_reg.last_name.clear()
    page_reg.email_registration.send_keys(Settings.valid_email)
    page_reg.email_registration.clear()
    page_reg.password_registration.send_keys(Settings.valid_password)
    page_reg.password_registration.clear()
    page_reg.password_registration_confirm.send_keys(Settings.valid_password)
    page_reg.password_registration_confirm.clear()
    page_reg.registration_btn.click()

    assert "Учётная запись уже существует" in page_reg.find_other_element(*AuthLocators.error_account_exists).text

def test_registration_and_redir_auth(selenium):
    """RT-015 Тест формы "Авторизация" после нажатия кнопки "Войти" при регистрации пользователя e-mail,
    который уже был использован ранее для регистрации. """
    page_reg = RegistrPage(selenium)
    page_reg.first_name.send_keys(Settings.first_name)
    page_reg.first_name.clear()
    page_reg.last_name.send_keys(Settings.last_name)
    page_reg.last_name.clear()
    page_reg.email_registration.send_keys(Settings.valid_email)
    page_reg.email_registration.clear()
    page_reg.password_registration.send_keys(Settings.valid_password)
    page_reg.password_registration.clear()
    page_reg.password_registration_confirm.send_keys(Settings.valid_password)
    page_reg.password_registration_confirm.clear()
    page_reg.registration_btn.click()
    page_reg.find_other_element(*AuthLocators.redirect_auth).click()

    assert 'Авторизация' in page_reg.find_other_element(*AuthLocators.authorization).text

@pytest.mark.parametrize("valid_first_name",
                         [
                             (Settings.russian_generate_string) * 2
                             , (Settings.russian_generate_string) * 3
                             , (Settings.russian_generate_string) * 15
                             , (Settings.russian_generate_string) * 29
                             , (Settings.russian_generate_string) * 30
                         ],
                         ids=
                         [
                             'russ_symbols=2', 'russ_symbols=3', 'russ_symbols=15',
                             'russ_symbols=29', 'russ_symbols=30'
                         ])
def test_first_name_by_valid_data(selenium, valid_first_name):
    """RT-016 Тест поля ввода "Имя" формы "Регистрация" допустимыми валидными значениями:
    буквы кириллицы в количестве 2 ; 3 ; 15 ; 29 ; 30 ."""
    page_reg = RegistrPage(selenium)
    page_reg.first_name.send_keys(valid_first_name)
    page_reg.first_name.clear()
    page_reg.registration_btn.click()

    assert 'Необходимо заполнить поле кириллицей. От 2 до 30 символов.' not in page_reg.container_first_name.text

@pytest.mark.parametrize("invalid_first_name",
                         [
                             (Settings.russian_generate_string) * 1
                             , (Settings.russian_generate_string) * 100
                             , (Settings.russian_generate_string) * 256
                             , (Settings.empty), (Settings.numbers)
                             , (Settings.latin_generate_string)
                             , (Settings.chinese_chars), (Settings.special_chars)
                         ],
                         ids=
                         [
                             'russ_symbols=1', 'russ_symbols=100', 'russ_symbols=256',
                             'empty', 'numbers', 'latin_symbols', 'chinese_symbols', 'special_symbols'
                         ])

def test_first_name_invalid_data(selenium, invalid_first_name):
    """RT-017 Тест поля ввода "Имя" формы "Регистрация" невалидными значениями:
    пустое значение;
    буквы кириллицы в количестве 1 ; 100 ; 256 ;
    латиницы буквы; китайские иероглифы; спецсимволы; числа."""
    page_reg = RegistrPage(selenium)
    page_reg.first_name.send_keys(invalid_first_name)
    page_reg.first_name.clear()
    page_reg.registration_btn.click()

    assert 'Необходимо заполнить поле кириллицей. От 2 до 30 символов.' in \
           page_reg.find_other_element(*AuthLocators.error_first_name).text


@pytest.mark.parametrize("valid_password",
                         [(Settings.passw1), (Settings.passw2), (Settings.passw3)],
                         ids=['valid_symbols=8', 'valid_symbols=15', 'valid_symbols=20'])
def test_last_name_valid_data(selenium, valid_password):
    """RT-018 Тест поля ввода "Пароль" формы "Регистрация" валидными значениями.:
    символы из букв латиницы прописью и строчные+числа в количестве 8 ; 15 ; 20 ."""
    page_reg = RegistrPage(selenium)
    page_reg.password_registration.send_keys(valid_password)
    page_reg.password_registration.clear()
    page_reg.registration_btn.click()

    assert 'Длина пароля должна быть не менее 8 символов' and \
           'Длина пароля должна быть не более 20 символов' and \
           'Пароль должен содержать хотя бы одну заглавную букву' and \
           'Пароль должен содержать хотя бы одну прописную букву' and \
           'Пароль должен содержать хотя бы 1 спецсимвол или хотя бы одну цифру' not in \
           page_reg.password_registration.text


def test_registration_confirm_password_valid_data(selenium):
    """RT-019 Тест поля ввода "Пароль" и "Подтвердить пароль" формы «Регистрация»
     валидными значениями(пароли совпадают)."""
    page_reg = RegistrPage(selenium)
    page_reg.password_registration.send_keys(Settings.passw1)
    page_reg.password_registration.clear()
    page_reg.password_registration_confirm.send_keys(Settings.passw1)
    page_reg.password_registration_confirm.clear()
    page_reg.registration_btn.click()

    assert 'Пароли не совпадают' not in page_reg.container_password_confirm.text


def test_registration_confirm_password_invalid_data(selenium):
    """RT-020 Тест поля ввода "Пароль" и "Подтвердить пароль" формы «Регистрация»
    невалидными значениями(пароли не совпадают)."""
    page_reg = RegistrPage(selenium)
    page_reg.password_registration.send_keys(Settings.passw1)
    page_reg.password_registration.clear()
    page_reg.password_registration_confirm.send_keys(Settings.passw2)
    page_reg.password_registration_confirm.clear()
    page_reg.registration_btn.click()

    assert 'Пароли не совпадают' in page_reg.find_other_element(*AuthLocators.error_password_confirm).text

