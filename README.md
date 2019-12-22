# Email processing 

Установка зависимостей 

pip install -r requirements.txt

## Pipline workflow

1. Сначала мы разбираем tar.gz архивы и конвертируем mailbox в .eml файлы
```
cd src
python extract_mailbox.py --path yourPathFolder
```

2. Составим xlsx файл 
```
python create_table.py --path yourPathFolder
```
#### TODO:
- [ ] Исправить ошибку Error parsing date 
- [ ] Проверить парсинг to_name в файлах list.txt


3. Сделать xlsx файл с фильтрацией по email
