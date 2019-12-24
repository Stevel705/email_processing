# Email processing 

Установка зависимостей 

pip install -r requirements.txt

## Pipline workflow

0. 
```
git clone https://github.com/Stevel705/email_processing.git
cd email_processing
```
1. Сначала мы разбираем tar.gz архивы и конвертируем mailbox в .eml файлы
```
cd src
python extract_mailbox.py --path yourPathFolder
```

2. Составим xlsx файл из файлов .eml
```
cd src
python create_table.py --path yourPathFolder
```



3. Делаем xlsx файл с фильтрацией по email в столбцах "from_", "to_", "cc"
```
cd src
python filter_email.py --email example@example.com
```



#### TODO:
- [ ] Исправить ошибку Error parsing date 
- [ ] Проверить парсинг to_name в файлах list.txt
- [ ] Сделать обработку hyperlink
- [ ] Добавить Логгер