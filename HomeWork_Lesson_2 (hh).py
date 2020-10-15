import pandas as pd
from bs4 import BeautifulSoup as bs
import requests


vacancy_input = input('Введите название вакансии: ')  #Тестировал на Разработчик Python
vacancies = []
pages_input = input('Введите количество анализируемых страниц: ') #Тестировал на 15 страницах

for page in range(int(pages_input)):
    main_link = 'https://hh.ru/search/vacancy'
    params = {'text': vacancy_input,
              'page': page}
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                            'Chrome/86.0.4240.75 Safari/537.36',
              'Authorization': '*/*'}
    response = requests.get(main_link, headers=header, params=params)

    soup = bs(response.text, 'html.parser')
    vacancy_block = soup.find('div', {'class': 'vacancy-serp'})
    vacancy_list = vacancy_block.findChildren('div', {'class': 'vacancy-serp-item'}, recursive=False)

    for vacancy in vacancy_list:
        vacancy_data = {}
        vacancy_link = vacancy.find('div', {'class': 'vacancy-serp-item__info'}).find('a', {'class': 'bloko-link HH-LinkModifier'})['href']
        vacancy_name = vacancy.find('div', {'class': 'vacancy-serp-item__info'}).find('a').getText()
        vacancy_salary = vacancy.find('div', {'class': 'vacancy-serp-item__sidebar'}).getText()
        vacancy_company = vacancy.find('div', {'class': 'vacancy-serp-item__meta-info'}).find('a').getText()

        vacancy_data['name'] = vacancy_name
        vacancy_data['link'] = vacancy_link
        vacancy_data['company'] = vacancy_company
        vacancy_salary_list = vacancy_salary.split()

        if len(vacancy_salary) > 1:
            if vacancy_salary_list[0] == 'от':
                vacancy_data['salary_min'] = int(vacancy_salary_list[1] + vacancy_salary_list[2])
                vacancy_data['salary_max'] = 'NaN'
                vacancy_data['currency'] = vacancy_salary_list[3]
            elif vacancy_salary_list[0] == 'до':
                vacancy_data['salary_min'] = 'NaN'
                vacancy_data['salary_max'] = int(vacancy_salary_list[1] + vacancy_salary_list[2])
                vacancy_data['currency'] = vacancy_salary_list[3]
            elif vacancy_salary.find('-') & len(vacancy_salary) > 3:
                vacancy_data['salary_min'] = int(vacancy_salary_list[0] + vacancy_salary_list[1][:3])
                vacancy_data['salary_max'] = int(vacancy_salary_list[1][4:] + vacancy_salary_list[2])
                vacancy_data['currency'] = vacancy_salary_list[3]
        else:
            vacancy_data['salary_min'] = 'NaN'
            vacancy_data['salary_max'] = 'NaN'
            vacancy_data['currency'] = 'NaN'
        vacancy_data['source'] = main_link[8:13]
        vacancies.append(vacancy_data)


    params2 = {'text': vacancy_input,
              'page': page + 1}
    if requests.get(main_link, headers=header, params=params2).ok == False:
        break


df_vacancies = pd.DataFrame(vacancies)
df_vacancies.to_csv(f'df_vacancies_hh_{vacancy_input}.csv', encoding='utf-8')