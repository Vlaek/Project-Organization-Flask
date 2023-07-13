# Flask - Project Organization

## Описание

**Project Organization** - это графический интерфейс на основе фреймворка **Flask** для БД "Проектные организации". В качестве БД используется MySQL. Для реализации запросов в БД был выбран модуль PyMySQL. ER-диаграмма БД представлена ниже.

![ER-диаграмма БД](https://i.imgur.com/KvaWXwi.jpg "ER-диаграмма БД")

В данном проекте использовались следующие сущности:
* **Contracts** - таблица договоры (название, клиент);
* **ContractProject** - связующая таблица между Contracts и Projects;
* **Projects** - таблица проекты (название, дата начала, дата окончания, стоимость, руководитель);
* **Workers** - таблица сотрудники (фамилия, имя, дата рождения, специальность, должность);
* **Executors** - связующая таблица между Workers и Projects;
* **Groups** - таблица с должностями сотрудников.

Ниже представлены скриншоты интерфейса.

![Скриншот главной страницы](https://i.imgur.com/olaJWIP.jpg "Скриншот главной страницы")

![Скриншот страницы 'Сотрудники'](https://i.imgur.com/WJG8AQz.jpg "Скриншот страницы 'Сотрудники'")

![Скриншот модального окна 'Добавление сотрудника'](https://i.imgur.com/NkuKS4I.jpg "Скриншот модального окна 'Добавление сотрудника'")

![Скриншот страницы 'Проекты'](https://i.imgur.com/1qNOA6o.jpg "Скриншот страницы 'Проекты'")

![Скриншот страницы 'Договоры'](https://i.imgur.com/0EmwMw8.jpg "Скриншот страницы 'Договоры'")
