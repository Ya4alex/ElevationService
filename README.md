# ElevationService

Задание 2 для практики в НИИТП

## **Сервис высот (elevation service)**

> Необходимо разработать веб-сервер с одной функцией (пока что):
> по запросу типа
`http://[ip-адрес]:[порт]/elevation?wkt={wkt}`
> возвращать ту же геометрию в формате wkt, но с данными о высоте.

В качестве фреймвокра для веб-сервера рекомендую использовать flask.

- [Про WKT](https://ru.wikipedia.org/wiki/WKT)
- [Получение](https://gis.stackexchange.com/questions/228920/getting-elevation-at-particular-coordinate-lat-lon-programmatically-but-offli)
  значения высоты из файла с данными
- Это [данные](https://drive.google.com/open?id=1CbXJCnGHTxH-5djAwEuWiCKi6z2nUCEE) на вулканы Камчатки (55-56 с.ш. и
  160-161 в.д.)

## Настройки и Развертывание
### Фронтенд
#### Настройка
- создать файл `./frontend/.env`
  ```dotenv
  VITE_API_URL_BASE="http://localhost:5050" # <- Your URL
  VITE_API_PATH_GET_ELEVATION="/elevation"
  ```
  
#### Развертка
- необходимо иметь `npm` (рекомендуемая версия `10.8.1+`)
  ```shell
  npm i
  npm run build
  ```
  
### Бэкенд
#### Настройка
- Настроить `.env` файл:
  ```dotenv
  SECRET_KEY="123145532"
  HOST="localhost"
  PORT=5050
  ```
- в `./config.py` указать ваш `ENV_FILE` и убедится, что `config = ProdConfig`

#### Развертывание
> Python 3.10+ Желательно создать новую среду `venv`
- `pip install -r ./requirements.txt`
- `python main.py`
