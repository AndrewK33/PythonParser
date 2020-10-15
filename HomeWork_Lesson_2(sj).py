import pandas as pd
from bs4 import BeautifulSoup as bs
import requests

vacancy_input = input('Введите название вакансии: ')  #Тестировал на Python
vacancies = []
pages_input = input('Введите количество анализируемых страниц: ') #Тестировал на 2 страницах


for page in range(int(pages_input)):
    main_link = 'https://superjob.ru'
    params = {'keywords': vacancy_input,
              'page': page}
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                            'Chrome/86.0.4240.75 Safari/537.36',
              'Authorization': '*/*'}
    response = requests.get(main_link + '/vacancy/search/', headers=header, params=params)

    soup = bs(response.text, 'html.parser')
    vacancy_list = soup.findAll('div', {'class': 'Fo44F QiY08 LvoDO'})

    for vacancy in vacancy_list:
        vacancy_data = {}
        vacancy_link = main_link + vacancy.find('div', {'class': '_3zucV undefined _3SGgo'}).find('a')['href']   #Время от времени здесь возникает проблема: эти замудренные название классов у дивов иногда меняются.
        vacancy_name = vacancy.find('div', {'class': '_3mfro CuJz5 PlM3e _2JVkc _3LJqf'}).getText()
        vacancy_salary = vacancy.find('span', {'class': '_3mfro _2Wp8I _1qw9T f-test-text-company-item-salary PlM3e _2JVkc _2VHxz'}).getText()
        if vacancy.find('span', {'class': '_3mfro _3Fsn4 f-test-text-vacancy-item-company-name _9fXTd _2JVkc _2VHxz _15msI'}):
            vacancy_company = vacancy.find('span', {'class': '_3mfro _3Fsn4 f-test-text-vacancy-item-company-name _9fXTd _2JVkc _2VHxz _15msI'}).find('a').getText()
        else:
            vacancy_company = 'NaN'
        vacancy_data['name'] = vacancy_name
        vacancy_data['link'] = vacancy_link
        vacancy_data['company'] = vacancy_company
        vacancy_salary_list = vacancy_salary.split( )

        if vacancy_salary_list[0] == 'от':
            vacancy_data['salary_min'] = int(vacancy_salary_list[1] + vacancy_salary_list[2])
            vacancy_data['salary_max'] = 'NaN'
            vacancy_data['currency'] = vacancy_salary_list[3]
        elif vacancy_salary_list[0] == 'до':
            vacancy_data['salary_min'] = 'NaN'
            vacancy_data['salary_max'] = int(vacancy_salary_list[1] + vacancy_salary_list[2])
            vacancy_data['currency'] = vacancy_salary_list[3]
        elif vacancy_salary_list[0] == 'По':
            vacancy_data['salary_min'] = 'NaN'
            vacancy_data['salary_max'] = 'NaN'
            vacancy_data['currency'] = 'NaN'
        elif vacancy_salary.find('-') & len(vacancy_salary_list) > 4:
            vacancy_data['salary_min'] = int(vacancy_salary_list[0] + vacancy_salary_list[1])
            vacancy_data['salary_max'] = int(vacancy_salary_list[3] + vacancy_salary_list[4])
            vacancy_data['currency'] = vacancy_salary_list[4]
        else:
            vacancy_data['salary_min'] = int(vacancy_salary_list[0] + vacancy_salary_list[1])
            vacancy_data['salary_max'] = int(vacancy_salary_list[0] + vacancy_salary_list[1])
            vacancy_data['currency'] = vacancy_salary_list[2]

        vacancy_data['source'] = main_link[15:]
        vacancies.append(vacancy_data)


    if not soup.find('a', {'class': 'icMQ_ _1_Cht _3ze9n f-test-button-dalshe f-test-link-Dalshe'}):
        break


df_vacancies = pd.DataFrame(vacancies)
df_vacancies.to_csv(f'df_vacancies_sj_{vacancy_input}.csv', encoding='utf-8')