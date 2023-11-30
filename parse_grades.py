from bs4 import BeautifulSoup

def parse_grades(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    
    grades_title = soup.find('h3', string='Ihre letzten Noten')
    
    grades_list = []

    if grades_title:
        grades_table = grades_title.find_next('table', class_='mdl-data-table')
        
        if grades_table:
            rows = grades_table.find_all('tr', class_='mdl-table--row-dense')
            for row in rows:
                columns = row.find_all('td', class_='mdl-data-table__cell--non-numeric')
                grade = tuple(column.text.strip() for column in columns)
                grades_list.append(grade)

    return grades_list
