# Локальный поисковик (версия 3)
Приложение для мгновенного поиска файлов в локальной сети предприятия.
Приложение постоянно сканирует каталоги в локальной сети.
Приложение предоставляет интерфейс для пользователей в виде веб-сервера для поиска файлов.
Приложение реализовано на технологии Docker.

# Предыдущие разработки
Локальный поисковик (версия 2). 
Неудачная попытка организовать поиск по файлам локальной сети. 
См. https://github.com/prog815/loc-index-2

# Установка и запуск

## 1. Скачиваем проект к себе

```
git clone https://github.com/prog815/lindex3.git
cd lindex3/
```

## 2. Сборка образа
```
docker build --pull --rm -f "Dockerfile" -t lindex3:latest .
```

## 3. Переносим образ в локальную сеть

## 4. Каталог с файлами для индексирования.

В локальной сети в каталог ./files примонтировать каталоги для индексирования.

## 5. Запуск контейнера
```
docker run -d -p80:5000 --mount type=bind,source=./files,target=/app/static/files,readonly --name lindex3 lindex3
```

## 6. Работаем с программой

http://server

# Обслуживание

```
docker container ls
docker rm -f lindex3
docker exec -it lindex3 /bin/sh
docker image ls 
docker image prune
docker ps -s
```