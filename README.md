 <p align="center">
  <img width="250px" src="https://github.com/NekoSilverFox/NekoSilverfox/blob/master/icons/logo_building_spbstu.png?raw=true" align="center" alt="ogo_building_spbstu" />
  </br>
  </br>
  <b><b>Санкт-Петербургский государственный политехнический университет</b></br></b>
  <b>Институт компьютерных наук и технологий</b>
  </br></br>
</p>


<div align=left>
<!-- SPbSTU 最后一行 -->
<p align="right">
 <b>Мэн Цзянин</br></b>
 <b>3530904/90102</b>
</p>


[toc]



# Лабораторная работа No.1

## Лабораторная работа No.1.1

### Постановка задачи

Практическое задание связано с проектированием схемы базы данных для работы приложения. Каждый индивидуальный вариант содержит предметную область, из которой должна быть проектируемая база данных. Задачей студента является решить, для чего будет использоваться создаваемая база данных, и, исходя из этого, построить её концептуальную схему. Результатом данного практического задания является схема базы данных (в виде ER-диаграммы, содержащей таблицы и связи между ними, без уточнения типов столбцов). При сдаче задания студент должен обосновать соответствие созданной схемы поставленной задаче.



**Темы для проработки**

- Модель "сущность-связь" (ER-модель).

- Первичные и внешние ключи.

- Типы связей и их моделирование.

- Нормальные формы и нормализация.

    

**Требования к схеме**
Схема должна соответствовать поставленной задаче.

Связи между сущностями должны быть правильно смоделированы.

Таблицы должны удовлетворять, по крайней мере, третьей нормальной форме (т.е. каждая таблица должна состоять из ключа и других взаимно независимых атрибутов).

Желательно придерживаться какой-либо системы в именовании таблиц и столбцов.



**Вариант №20**

Предметная область для практических заданий No1.* No2.*: **Судоходство**

Пример схемы для задания No1.1,

<img src="doc/pic/README/image-20220516203429227.png" alt="image-20220516203429227" style="zoom:50%;" />



### Реализация

ER-диаграмма, полученная с помощью DataGrip:

![ER 图](doc/pic/README/ER 图.png)



## Лабораторная работа No.1.2

### Постановка задачи





### Реализация



## Лабораторная работа No.1.3

### Постановка задачи





### Реализация



## Лабораторная работа No.1.4



### Постановка задачи





### Реализация



## 【lab 1.4】 Контроль целостности данных

### Постановка задачи





### Реализация



### Результат

| **Контроль целостности данных** | грязные чтении | неповторяющиеся чтении | Потерянные изменении | фантом | **Аномалия сериализации** |
| ------------------------------- | -------------- | ---------------------- | -------------------- | ------ | ------------------------- |
| `serializable`                  | -              | -                      | -                    | -      | -                         |
| `repeatable read`               | -              | -                      | -                    | -      | +                         |
| `read commited`                 | -              | +                      | -                    | +      | +                         |
| `read uncommited`               | -              | +                      | -                    | +      | +                         |



### Аномалия сериализации

We can conclude that Postgres uses a `dependencies detection` mechanism to detect potential `read phenomena` and stop them by throwing out an error.

> Dan R. K. Ports and Kevin Grittner. 2012. Serializable Snapshot Isolation in PostgreSQL. Proceedings of the VLDB Endowment vol. 5 (12) , August 2012 
> ————————————————
>
> https://arxiv.org/pdf/1208.4179.pdf
>
> https://postgrespro.ru/docs/postgrespro/14/transaction-iso
>
> https://dev.to/techschoolguru/understand-isolation-levels-read-phenomena-in-mysql-postgres-c2e#isolation-levels-in-postgres
>
> https://blog.csdn.net/gp_community/article/details/109772336

<img src="doc/pic/README/image-20220323225542601.png" alt="image-20220323225542601" style="zoom:50%;" />







---



## READ UNCOMMITTED

- **[-] грязные чтении & [+] неповторяющиеся чтении**

    | **Параллельный сеанс** 1                                     | **Параллельный сеанс** 2                                     |
    | ------------------------------------------------------------ | ------------------------------------------------------------ |
    | `BEGIN TRANSACTION ISOLATION LEVEL READ UNCOMMITTED;`<br />`SHOW TRANSACTION_ISOLATION;`<br /><br />>>><br />*read uncommitted* |                                                              |
    |                                                              | `BEGIN TRANSACTION ISOLATION LEVEL READ UNCOMMITTED;`<br />`SHOW TRANSACTION_ISOLATION;`<br /><br />>>><br />*read uncommitted* |
    | `SELECT price FROM tb_ports WHERE nameport='baku';`<br /><br />>>><br />1000 |                                                              |
    |                                                              | `UPDATE tb_ports SET price=2000 WHERE nameport='baku';`      |
    |                                                              | `SELECT price FROM tb_ports WHERE nameport='baku';`<br /><br />>>><br />2000 |
    | `SELECT price FROM tb_ports WHERE nameport='baku';`<br /><br />>>>==[-] грязные чтении==<br />1000 |                                                              |
    |                                                              | `COMMIT;`                                                    |
    | `SELECT price FROM tb_ports WHERE nameport='baku';`<br /><br />>>>==[-] неповторяющиеся чтении==<br />2000 |                                                              |
    | `COMMIT;`                                                    |                                                              |



- **[-] Потерянные изменении**

  - **[-] Потерянные изменении | Lost update**
  
  - | **Параллельный сеанс** 1                                     | **Параллельный сеанс** 2                                     |
      | ------------------------------------------------------------ | ------------------------------------------------------------ |
      | `BEGIN TRANSACTION ISOLATION LEVEL READ UNCOMMITTED;`<br />`SHOW TRANSACTION_ISOLATION;`<br /><br />>>><br />*read uncommitted* |                                                              |
      |                                                              | `BEGIN TRANSACTION ISOLATION LEVEL READ UNCOMMITTED;`<br />`SHOW TRANSACTION_ISOLATION;`<br /><br />>>><br />*read uncommitted* |
      | `SELECT price FROM tb_ports WHERE nameport='baku';`<br /><br />>>><br />1000 |                                                              |
      |                                                              | `UPDATE tb_ports SET price=price-100 WHERE nameport='baku';` |
      |                                                              | `SELECT price FROM tb_ports WHERE nameport='baku';`<br /><br />>>><br />900 |
      |                                                              | `COMMIT;`                                                    |
      | `UPDATE tb_ports SET price=price+100 WHERE nameport='baku';` |                                                              |
      | `ROLLBACK;`                                                  |                                                              |
      |                                                              | `SELECT price FROM tb_ports WHERE nameport='baku';`<br /><br />>>>==[-] Потерянные изменении \| Second lost update==<br />900 |
  
      **[-] Потерянные изменении | Second lost update**
  
      | **Параллельный сеанс** 1                                     | **Параллельный сеанс** 2                                     |
      | ------------------------------------------------------------ | ------------------------------------------------------------ |
      | `BEGIN TRANSACTION ISOLATION LEVEL READ UNCOMMITTED;`<br />`SHOW TRANSACTION_ISOLATION;`<br /><br />>>><br />*read uncommitted* |                                                              |
      |                                                              | `BEGIN TRANSACTION ISOLATION LEVEL READ UNCOMMITTED;`<br />`SHOW TRANSACTION_ISOLATION;`<br /><br />>>><br />*read uncommitted* |
      | `SELECT price FROM tb_ports WHERE nameport='baku';`<br /><br />>>><br />1000 |                                                              |
      |                                                              | `UPDATE tb_ports SET price=price-100 WHERE nameport='baku';` |
      |                                                              | `SELECT price FROM tb_ports WHERE nameport='baku';`<br /><br />>>><br />900 |
      | `UPDATE tb_ports SET price=price+100 WHERE nameport='baku';`<br /><br />>>> <br />БЛОКИРУЕТСЯ |                                                              |
      |                                                              | `COMMIT;`                                                    |
      | `COMMIT;`                                                    |                                                              |
      |                                                              | `SELECT price FROM tb_ports WHERE nameport='baku';`<br /><br />>>>==[-] Потерянные изменении \| Second lost update==<br />1000 |
  





- **[+] Фантом**

    | **Параллельный сеанс** 1                                     | **Параллельный сеанс** 2                                     |
    | ------------------------------------------------------------ | ------------------------------------------------------------ |
    | `BEGIN TRANSACTION ISOLATION LEVEL READ UNCOMMITTED;`<br />`SHOW TRANSACTION_ISOLATION;`<br /><br />>>><br />*read uncommitted* |                                                              |
    |                                                              | `BEGIN TRANSACTION ISOLATION LEVEL READ UNCOMMITTED;`<br />`SHOW TRANSACTION_ISOLATION;`<br /><br />>>><br />*read uncommitted* |
    | `SELECT price FROM tb_ports WHERE nameport='baku2';`<br /><br />>>><br />(0 rows) |                                                              |
    |                                                              | `INSERT INTO tb_Ports(Country, NamePort, Price, LevelID)`<br />` VALUES('Azerbaijan', 'baku2', 2222, 3);` |
    | `SELECT price FROM tb_ports WHERE nameport='baku2';`<br /><br />>>><br />(0 rows) |                                                              |
    |                                                              | `COMMIT;`                                                    |
    | `SELECT price FROM tb_ports WHERE nameport='baku2';`<br /><br />>>>==[+] Фантом==<br />2222 |                                                              |
    | `DELETE FROM tb_ports WHERE nameport='baku2';`               |                                                              |
    | `COMMIT;`                                                    |                                                              |





- **[+] Аномалия сериализации**

    | **Параллельный сеанс** 1                                     | **Параллельный сеанс** 2                                     |
    | ------------------------------------------------------------ | ------------------------------------------------------------ |
    | `BEGIN TRANSACTION ISOLATION LEVEL READ UNCOMMITTED;`<br />`SHOW TRANSACTION_ISOLATION;`<br /><br />>>><br />*read uncommitted* |                                                              |
    |                                                              | `BEGIN TRANSACTION ISOLATION LEVEL READ UNCOMMITTED;`<br />`SHOW TRANSACTION_ISOLATION;`<br /><br />>>><br />*read uncommitted* |
    | `UPDATE tb_ports SET price=2000 WHERE nameport='baku';`      |                                                              |
    |                                                              | `UPDATE tb_ports SET price=9000 WHERE nameport='ShangHai';`  |
    | `COMMIT;`                                                    |                                                              |
    |                                                              | `COMMIT;`<br />>>>==[+] Аномалия сериализации==              |

    






---





## READ COMMITTED

- **[-] Грязные чтении & [+] Неповторяющиеся чтении**

    | **Параллельный сеанс** 1                                     | **Параллельный сеанс** 2                                     |
    | ------------------------------------------------------------ | ------------------------------------------------------------ |
    | `BEGIN TRANSACTION ISOLATION LEVEL READ COMMITTED;`<br />`SHOW TRANSACTION_ISOLATION;`<br /><br />>>><br />*read committed* |                                                              |
    |                                                              | `BEGIN TRANSACTION ISOLATION LEVEL READ COMMITTED;`<br />`SHOW TRANSACTION_ISOLATION;`<br /><br />>>><br />*read committed* |
    | `SELECT price FROM tb_ports WHERE nameport='baku';`<br /><br />>>><br />1000 |                                                              |
    |                                                              | `UPDATE tb_ports SET price=2000 WHERE nameport='baku';`      |
    |                                                              | `SELECT price FROM tb_ports WHERE nameport='baku';`<br /><br />>>><br />2000 |
    | `SELECT price FROM tb_ports WHERE nameport='baku';`<br /><br />>>>==[-] Грязные чтении==<br />1000 |                                                              |
    |                                                              | `COMMIT;`                                                    |
    | `SELECT price FROM tb_ports WHERE nameport='baku';`<br /><br />>>>==[+] Неповторяющиеся чтении==<br />2000 |                                                              |
    | `COMMIT;`                                                    |                                                              |





- **[-] Потерянные изменении**

    - **[-] Потерянные изменении | Lost update**

    - | **Параллельный сеанс** 1                                     | **Параллельный сеанс** 2                                     |
        | ------------------------------------------------------------ | ------------------------------------------------------------ |
        | `BEGIN TRANSACTION ISOLATION LEVEL READ COMMITTED;`<br />`SHOW TRANSACTION_ISOLATION;`<br /><br />>>><br />*read committed* |                                                              |
        |                                                              | `BEGIN TRANSACTION ISOLATION LEVEL READ COMMITTED;`<br />`SHOW TRANSACTION_ISOLATION;`<br /><br />>>><br />*read committed* |
        | `SELECT price FROM tb_ports WHERE nameport='baku';`<br /><br />>>><br />1000 |                                                              |
        |                                                              | `UPDATE tb_ports SET price=price-100 WHERE nameport='baku';` |
        |                                                              | `SELECT price FROM tb_ports WHERE nameport='baku';`<br /><br />>>><br />900 |
        |                                                              | `COMMIT;`                                                    |
        | `UPDATE tb_ports SET price=price+100 WHERE nameport='baku';` |                                                              |
        | `ROLLBACK;`                                                  |                                                              |
        |                                                              | `SELECT price FROM tb_ports WHERE nameport='baku';`<br /><br />>>>==[-] Потерянные изменении \| Second lost update==<br />900 |

        **[-] Потерянные изменении | Second lost update**

        | **Параллельный сеанс** 1                                     | **Параллельный сеанс** 2                                     |
        | ------------------------------------------------------------ | ------------------------------------------------------------ |
        | `BEGIN TRANSACTION ISOLATION LEVEL READ COMMITTED;`<br />`SHOW TRANSACTION_ISOLATION;`<br /><br />>>><br />*read committed* |                                                              |
        |                                                              | `BEGIN TRANSACTION ISOLATION LEVEL READ COMMITTED;`<br />`SHOW TRANSACTION_ISOLATION;`<br /><br />>>><br />*read committed* |
        | `SELECT price FROM tb_ports WHERE nameport='baku';`<br /><br />>>><br />1000 |                                                              |
        |                                                              | `UPDATE tb_ports SET price=price-100 WHERE nameport='baku';` |
        |                                                              | `SELECT price FROM tb_ports WHERE nameport='baku';`<br /><br />>>><br />900 |
        | `UPDATE tb_ports SET price=price+100 WHERE nameport='baku';`<br /><br />>>> <br />БЛОКИРУЕТСЯ |                                                              |
        |                                                              | `COMMIT;`                                                    |
        | `COMMIT;`                                                    |                                                              |
        |                                                              | `SELECT price FROM tb_ports WHERE nameport='baku';`<br /><br />>>>==[-] Потерянные изменении \| Second lost update==<br />1000 |





- **[+] Фантом**

    | **Параллельный сеанс** 1                                     | **Параллельный сеанс** 2                                     |
    | ------------------------------------------------------------ | ------------------------------------------------------------ |
    | `BEGIN TRANSACTION ISOLATION LEVEL READ COMMITTED;`<br />`SHOW TRANSACTION_ISOLATION;`<br /><br />>>><br />*read committed* |                                                              |
    |                                                              | `BEGIN TRANSACTION ISOLATION LEVEL READ COMMITTED;`<br />`SHOW TRANSACTION_ISOLATION;`<br /><br />>>><br />*read committed* |
    | `SELECT price FROM tb_ports WHERE nameport='baku2';`<br /><br />>>><br />(0 rows) |                                                              |
    |                                                              | `INSERT INTO tb_Ports(Country, NamePort, Price, LevelID)`<br />` VALUES('Azerbaijan', 'baku2', 2222, 3);` |
    | `SELECT price FROM tb_ports WHERE nameport='baku2';`<br /><br />>>><br />(0 rows) |                                                              |
    |                                                              | `COMMIT;`                                                    |
    | `SELECT price FROM tb_ports WHERE nameport='baku2';`<br /><br />>>>==[+] Фантом==<br />2222 |                                                              |
    | `DELETE FROM tb_ports WHERE nameport='baku2';`               |                                                              |
    | `COMMIT;`                                                    |                                                              |





- **[+] Аномалия сериализации**

    | **Параллельный сеанс** 1                                     | **Параллельный сеанс** 2                                     |
    | ------------------------------------------------------------ | ------------------------------------------------------------ |
    | `BEGIN TRANSACTION ISOLATION LEVEL READ COMMITTED;`<br />`SHOW TRANSACTION_ISOLATION;`<br /><br />>>><br />*read committed* |                                                              |
    |                                                              | `BEGIN TRANSACTION ISOLATION LEVEL READ COMMITTED;`<br />`SHOW TRANSACTION_ISOLATION;`<br /><br />>>><br />*read committed* |
    | `UPDATE tb_ports SET price=2000 WHERE nameport='baku';`      |                                                              |
    |                                                              | `UPDATE tb_ports SET price=9000 WHERE nameport='ShangHai';`  |
    | `COMMIT;`                                                    |                                                              |
    |                                                              | `COMMIT;`<br />>>>==[+] Аномалия сериализации==              |

    





---



## REPEATABLE READ

- **[-] Грязные чтении & [-] Неповторяющиеся чтении**

    | **Параллельный сеанс** 1                                     | **Параллельный сеанс** 2                                     |
    | ------------------------------------------------------------ | ------------------------------------------------------------ |
    | `BEGIN TRANSACTION ISOLATION LEVEL REPEATABLE READ;`<br />`SHOW TRANSACTION_ISOLATION;`<br /><br />>>><br />*repeatable read* |                                                              |
    |                                                              | `BEGIN TRANSACTION ISOLATION LEVEL REPEATABLE READ;`<br />`SHOW TRANSACTION_ISOLATION;`<br /><br />>>><br />*repeatable read* |
    | `SELECT price FROM tb_ports WHERE nameport='baku';`<br /><br />>>><br />1000 |                                                              |
    |                                                              | `UPDATE tb_ports SET price=2000 WHERE nameport='baku';`      |
    |                                                              | `SELECT price FROM tb_ports WHERE nameport='baku';`<br /><br />>>><br />2000 |
    | `SELECT price FROM tb_ports WHERE nameport='baku';`<br /><br />>>>==[-] Грязные чтении==<br />1000 |                                                              |
    |                                                              | `COMMIT;`                                                    |
    | `SELECT price FROM tb_ports WHERE nameport='baku';`<br /><br />>>>==[-] Неповторяющиеся чтении==<br />1000 |                                                              |
    | `COMMIT;`                                                    |                                                              |





- **[-] Потерянные изменении**

    - **[-] Потерянные изменении | Lost update**

    - | **Параллельный сеанс** 1                                     | **Параллельный сеанс** 2                                     |
        | ------------------------------------------------------------ | ------------------------------------------------------------ |
        | `BEGIN TRANSACTION ISOLATION LEVEL REPEATABLE READ;`<br />`SHOW TRANSACTION_ISOLATION;`<br /><br />>>><br />*repeatable read* |                                                              |
        |                                                              | `BEGIN TRANSACTION ISOLATION LEVEL REPEATABLE READ;`<br />`SHOW TRANSACTION_ISOLATION;`<br /><br />>>><br />*repeatable read* |
        | `SELECT price FROM tb_ports WHERE nameport='baku';`<br /><br />>>><br />1000 |                                                              |
        |                                                              | `UPDATE tb_ports SET price=price-100 WHERE nameport='baku';` |
        |                                                              | `SELECT price FROM tb_ports WHERE nameport='baku';`<br /><br />>>><br />900 |
        |                                                              | `COMMIT;`                                                    |
        | `UPDATE tb_ports SET price=price+100 WHERE nameport='baku';`<br /><br />>>> <br />ERROR:  could not serialize access due to concurrent update |                                                              |
        | `ROLLBACK;`                                                  |                                                              |
        |                                                              | `SELECT price FROM tb_ports WHERE nameport='baku';`<br /><br />>>>==[-] Потерянные изменении \| Second lost update==<br />900 |

        **[-] Потерянные изменении | Second lost update**

        | **Параллельный сеанс** 1                                     | **Параллельный сеанс** 2                                     |
        | ------------------------------------------------------------ | ------------------------------------------------------------ |
        | `BEGIN TRANSACTION ISOLATION LEVEL REPEATABLE READ;`<br />`SHOW TRANSACTION_ISOLATION;`<br /><br />>>><br />*repeatable read* |                                                              |
        |                                                              | `BEGIN TRANSACTION ISOLATION LEVEL REPEATABLE READ;`<br />`SHOW TRANSACTION_ISOLATION;`<br /><br />>>><br />*repeatable read* |
        | `SELECT price FROM tb_ports WHERE nameport='baku';`<br /><br />>>><br />1000 |                                                              |
        |                                                              | `UPDATE tb_ports SET price=price-100 WHERE nameport='baku';` |
        |                                                              | `SELECT price FROM tb_ports WHERE nameport='baku';`<br /><br />>>><br />900 |
        | `UPDATE tb_ports SET price=price+100 WHERE nameport='baku';`<br /><br />>>> <br />БЛОКИРУЕТСЯ |                                                              |
        |                                                              | `COMMIT;`                                                    |
        | >>><br />ERROR:  could not serialize access due to concurrent update |                                                              |
        | `COMMIT;`<br /><br />>>><br />ROLLBACK                       |                                                              |
        |                                                              | `SELECT price FROM tb_ports WHERE nameport='baku';`<br /><br />>>>==[-] Потерянные изменении \| Second lost update==<br />900 |





- **[-] Фантом**

    | **Параллельный сеанс** 1                                     | **Параллельный сеанс** 2                                     |
    | ------------------------------------------------------------ | ------------------------------------------------------------ |
    | `BEGIN TRANSACTION ISOLATION LEVEL REPEATABLE READ;`<br />`SHOW TRANSACTION_ISOLATION;`<br /><br />>>><br />*repeatable read* |                                                              |
    |                                                              | `BEGIN TRANSACTION ISOLATION LEVEL REPEATABLE READ;`<br />`SHOW TRANSACTION_ISOLATION;`<br /><br />>>><br />*repeatable read* |
    | `SELECT price FROM tb_ports WHERE nameport='baku2';`<br /><br />>>><br />(0 rows) |                                                              |
    |                                                              | `INSERT INTO tb_Ports(Country, NamePort, Price, LevelID)`<br />` VALUES('Azerbaijan', 'baku2', 2222, 3);` |
    | `SELECT price FROM tb_ports WHERE nameport='baku2';`<br /><br />>>><br />(0 rows) |                                                              |
    |                                                              | `COMMIT;`                                                    |
    | `SELECT price FROM tb_ports WHERE nameport='baku2';`<br /><br />>>>==[-] Фантом==<br />(0 rows) |                                                              |
    | `DELETE FROM tb_ports WHERE nameport='baku2';`               |                                                              |
    | `COMMIT;`                                                    |                                                              |



- **[+] Аномалия сериализации**

    | **Параллельный сеанс** 1                                     | **Параллельный сеанс** 2                                     |
    | ------------------------------------------------------------ | ------------------------------------------------------------ |
    | `BEGIN TRANSACTION ISOLATION LEVEL REPEATABLE READ;`<br />`SHOW TRANSACTION_ISOLATION;`<br /><br />>>><br />*repeatable read* |                                                              |
    |                                                              | `BEGIN TRANSACTION ISOLATION LEVEL REPEATABLE READ;`<br />`SHOW TRANSACTION_ISOLATION;`<br /><br />>>><br />*repeatable read* |
    | `UPDATE tb_ports SET price=2000 WHERE nameport='baku';`      |                                                              |
    |                                                              | `UPDATE tb_ports SET price=9000 WHERE nameport='ShangHai';`  |
    | `COMMIT;`                                                    |                                                              |
    |                                                              | `COMMIT;`<br />>>>==[+] Аномалия сериализации==              |

    



---



## SERIALIZABLE

- **[-] Грязные чтении & [-] Неповторяющиеся чтении**

    | **Параллельный сеанс** 1                                     | **Параллельный сеанс** 2                                     |
    | ------------------------------------------------------------ | ------------------------------------------------------------ |
    | `BEGIN TRANSACTION ISOLATION LEVEL SERIALIZABLE;`<br />`SHOW TRANSACTION_ISOLATION;`<br /><br />>>><br />*serializable* |                                                              |
    |                                                              | `BEGIN TRANSACTION ISOLATION LEVEL SERIALIZABLE;`<br />`SHOW TRANSACTION_ISOLATION;`<br /><br />>>><br />*serializable* |
    | `SELECT price FROM tb_ports WHERE nameport='baku';`<br /><br />>>><br />1000 |                                                              |
    |                                                              | `UPDATE tb_ports SET price=2000 WHERE nameport='baku';`      |
    |                                                              | `SELECT price FROM tb_ports WHERE nameport='baku';`<br /><br />>>><br />2000 |
    | `SELECT price FROM tb_ports WHERE nameport='baku';`<br /><br />>>>==[-] Грязные чтении==<br />1000 |                                                              |
    |                                                              | `COMMIT;`                                                    |
    | `SELECT price FROM tb_ports WHERE nameport='baku';`<br /><br />>>>==[-] Неповторяющиеся чтении==<br />1000 |                                                              |
    | `COMMIT;`                                                    |                                                              |





- **[-] Потерянные изменении**

    - **[-] Потерянные изменении | Lost update**

    - | **Параллельный сеанс** 1                                     | **Параллельный сеанс** 2                                     |
        | ------------------------------------------------------------ | ------------------------------------------------------------ |
        | `BEGIN TRANSACTION ISOLATION LEVEL SERIALIZABLE;`<br />`SHOW TRANSACTION_ISOLATION;`<br /><br />>>><br />*serializable* |                                                              |
        |                                                              | `BEGIN TRANSACTION ISOLATION LEVEL SERIALIZABLE;`<br />`SHOW TRANSACTION_ISOLATION;`<br /><br />>>><br />*serializable* |
        | `SELECT price FROM tb_ports WHERE nameport='baku';`<br /><br />>>><br />1000 |                                                              |
        |                                                              | `UPDATE tb_ports SET price=price-100 WHERE nameport='baku';` |
        |                                                              | `SELECT price FROM tb_ports WHERE nameport='baku';`<br /><br />>>><br />900 |
        |                                                              | `COMMIT;`                                                    |
        | `UPDATE tb_ports SET price=price+100 WHERE nameport='baku';`<br /><br />>>> <br />ERROR:  could not serialize access due to concurrent update |                                                              |
        | `ROLLBACK;`                                                  |                                                              |
        |                                                              | `SELECT price FROM tb_ports WHERE nameport='baku';`<br /><br />>>>==[-] Потерянные изменении \| Second lost update==<br />900 |

        **[-] Потерянные изменении | Second lost update**

        | **Параллельный сеанс** 1                                     | **Параллельный сеанс** 2                                     |
        | ------------------------------------------------------------ | ------------------------------------------------------------ |
        | `BEGIN TRANSACTION ISOLATION LEVEL SERIALIZABLE;`<br />`SHOW TRANSACTION_ISOLATION;`<br /><br />>>><br />*serializable* |                                                              |
        |                                                              | `BEGIN TRANSACTION ISOLATION LEVEL SERIALIZABLE;`<br />`SHOW TRANSACTION_ISOLATION;`<br /><br />>>><br />*serializable* |
        | `SELECT price FROM tb_ports WHERE nameport='baku';`<br /><br />>>><br />1000 |                                                              |
        |                                                              | `UPDATE tb_ports SET price=price-100 WHERE nameport='baku';` |
        |                                                              | `SELECT price FROM tb_ports WHERE nameport='baku';`<br /><br />>>><br />900 |
        | `UPDATE tb_ports SET price=price+100 WHERE nameport='baku';`<br /><br />>>> <br />БЛОКИРУЕТСЯ |                                                              |
        |                                                              | `COMMIT;`                                                    |
        | >>><br />ERROR:  could not serialize access due to concurrent update |                                                              |
        | `COMMIT;`<br /><br />>>><br />ROLLBACK                       |                                                              |
        |                                                              | `SELECT price FROM tb_ports WHERE nameport='baku';`<br /><br />>>>==[-] Потерянные изменении \| Second lost update==<br />900 |





- **[-] Фантом**

    | **Параллельный сеанс** 1                                     | **Параллельный сеанс** 2                                     |
    | ------------------------------------------------------------ | ------------------------------------------------------------ |
    | `BEGIN TRANSACTION ISOLATION LEVEL SERIALIZABLE;`<br />`SHOW TRANSACTION_ISOLATION;`<br /><br />>>><br />*serializable* |                                                              |
    |                                                              | `BEGIN TRANSACTION ISOLATION LEVEL SERIALIZABLE;`<br />`SHOW TRANSACTION_ISOLATION;`<br /><br />>>><br />*serializable* |
    | `SELECT price FROM tb_ports WHERE nameport='baku2';`<br /><br />>>><br />(0 rows) |                                                              |
    |                                                              | `INSERT INTO tb_Ports(Country, NamePort, Price, LevelID)`<br />` VALUES('Azerbaijan', 'baku2', 2222, 3);` |
    | `SELECT price FROM tb_ports WHERE nameport='baku2';`<br /><br />>>><br />(0 rows) |                                                              |
    |                                                              | `COMMIT;`                                                    |
    | `SELECT price FROM tb_ports WHERE nameport='baku2';`<br /><br />>>>==[-] Фантом==<br />(0 rows) |                                                              |
    | `DELETE FROM tb_ports WHERE nameport='baku2';`               |                                                              |
    | `COMMIT;`                                                    |                                                              |



- **[-] Аномалия сериализации**

    | **Параллельный сеанс** 1                                     | **Параллельный сеанс** 2                                     |
    | ------------------------------------------------------------ | ------------------------------------------------------------ |
    | `BEGIN TRANSACTION ISOLATION LEVEL SERIALIZABLE;`<br />`SHOW TRANSACTION_ISOLATION;`<br /><br />>>><br />*serializable* |                                                              |
    |                                                              | `BEGIN TRANSACTION ISOLATION LEVEL SERIALIZABLE;`<br />`SHOW TRANSACTION_ISOLATION;`<br /><br />>>><br />*serializable* |
    | `UPDATE tb_ports SET price=2000 WHERE nameport='baku';`      |                                                              |
    |                                                              | `UPDATE tb_ports SET price=9000 WHERE nameport='ShangHai';`  |
    | `COMMIT;`                                                    |                                                              |
    |                                                              | `COMMIT;`<br />>>>==[-] Аномалия сериализации==<br />ERROR:  could not serialize access due to read/write dependencies among transactions<br/>DETAIL:  Reason code: Canceled on identification as a pivot, during commit attempt.<br/>HINT:  The transaction might succeed if retried. |
    
    





---

# lab 2



## 【lab】2.1

1. **Создать пользователя test** 

```sql
-- CREATE USER fox;
CREATE ROLE test;
ALTER ROLE test PASSWORD '123';
```

<img src="doc/pic/README/image-20220324211259582.png" alt="image-20220324211259582" style="zoom: 50%;" />



2. **Добавление привилегий для входа в базу данных**

    ```sql
    ALTER ROLE test LOGIN;
    ```

    <img src="doc/pic/README/image-20220324211432812.png" alt="image-20220324211432812" style="zoom: 50%;" />

    

3. **Выдать ему доступ к базе данных**

    - Присваиваются права `SELECT`, `INSERT`, `UPDATE`

        ```sql
        GRANT SELECT, INSERT, UPDATE ON tb_portlevels TO test;
        ```

        - ![image-20220324214127593](doc/pic/README/image-20220324214127593.png)

        

        - ![image-20220324215214166](doc/pic/README/image-20220324215214166.png)

            

        - ![image-20220324214054583](doc/pic/README/image-20220324214054583.png)

            

        - ![image-20220324215341921](doc/pic/README/image-20220324215341921-8148027.png)

        

        

        

        

        

    - Присваиваются права `SELECT` и `UPDATE `

        ```sql
        GRANT SELECT, UPDATE ON tb_typeseacraft TO test;
        ```

        - ![image-20220324215447762](doc/pic/README/image-20220324215447762.png)
        - ![image-20220324215736741](doc/pic/README/image-20220324215736741.png)
        - ![image-20220324215830246](doc/pic/README/image-20220324215830246.png)
        - ![image-20220324215853702](doc/pic/README/image-20220324215853702.png)

        

    - Присваивается только право `SELECT`

        ```sql
        GRANT SELECT ON tb_ports TO test;
        ```

        

    - Присвоить новому пользователю право доступа (`SELECT`) к одному из представлений

        ```sql
        -- Вывод списка подробной информации о порте
        CREATE OR REPLACE VIEW VW_Ports
        AS
        SELECT IDPort, Country, NamePort, NameLevel, Price, COUNT(IDPort) AS NumArrivals
        	FROM tb_arrivals
        		INNER JOIN tb_ports ON tb_ports.idport=tb_arrivals.portid
        		INNER JOIN tb_portlevels ON tb_ports.levelid=tb_portlevels.idlevel
        	GROUP BY IDPort, Country, NamePort, NameLevel, Price 
        	ORDER BY IDPort ASC;
        
        GRANT SELECT ON VW_Ports TO test;
        ```

        <img src="doc/pic/README/image-20220324232945852.png" alt="image-20220324232945852" style="zoom:50%;" />

        <img src="doc/pic/README/image-20220324233025589.png" alt="image-20220324233025589" style="zoom:50%;" />
        
    - Создать стандартную роль уровня базы данных, присвоить ей право доступа (`UPDATE` на некоторые столбцы) к одному из представлений, назначить новому пользователю созданную роль.

        ```sql
        CREATE ROLE update_vw_test;
        GRANT UPDATE (NameSeacraft) ON vw_seacrafts TO update_vw_test;
        GRANT update_vw_test TO test;
        ```

        <img src="doc/pic/README/image-20220324235621158.png" alt="image-20220324235621158" style="zoom:50%;" />

        <img src="doc/pic/README/image-20220325000112121.png" alt="image-20220325000112121" style="zoom:50%;" />

        

4. Удалите все разрешения у пользователя и удалите пользователя

    ```sql
    REVOKE ALL ON DATABASE db_port from test;
    DROP ROLE test;
    ```





---





# lab 3

## lab 3.1

> **第 46 章 PL/Python — Python 过程语言**：
>
> http://www.postgres.cn/docs/14/plpython-funcs.html（向后几页都是）
>
> https://www.cnblogs.com/whitebai/p/12924270.html
>
> http://www.postgres.cn/docs/14/performance-tips.html
>
> https://juejin.cn/post/6960674004969455623



### Постановка задачи

Седьмое практическое задание связано с проектированием схемы базы данных для аналитики. Будем исходить из того, что приложение, для которого была сделана база данных в задании стала очень популярной и по ней каждый день можно собирать большой объем статистической информации. Результатом данного практического задания являются: **скрипты создания базы данных, хранимая процедура (генератор) для ее заполнения**, **анализ плана выполнения запроса**.



**Требования к БД**

- Как минимум одна таблица должна содержать не меньше 10 млн. записей, которые со временем теряют актуальность.

- Другая таблица, связанная с первой, должна содержать не меньше 1 млн. записей.

- В одной из таблиц с количество записей больше 1 млн. должна быть колонка с текстом, по

    которой будет необходимо настроить полнотекстовый поиск.



### ER диаграммы

![ER-图](doc/pic/README/ER-图.png)



### Хранимая процедура (генератор)

```sql
CREATE EXTENSION plpython3u;

------------------------------------------------------------------------------------------------------
-- 向 tb_arrivals 中插入 10000 0000 条随机数据记录
-- Вставьте 100 000 000 случайных записей данных в tb_arrivals
CREATE OR REPLACE FUNCTION fc_InsertArrivals()
	RETURNS TEXT
	AS $$
import random
import datetime


COL_NUM = 100000000


def get_random_text():
    """
    生成一段随机 `text`
    Сгенерируйте случайный `текст`.
    
    :return: text -> string
    """
    text = ''
    num_word = random.randint(1, 20)
    for i in range(num_word):
        len_word = random.randint(1, 10)
        word = ''.join(random.sample('zyxwvutsrqponmlkjihgfedcba', len_word))
        text += (word + ' ')

    return "'" + text + "'"


def get_random_start_end_time():
    """
    获取一个随机开始时间 `start_time_str` 和随机结束时间 `end_time_str` 合并之后的字符串
    Получить строку со случайным начальным временем `start_time_str` и случайным конечным временем `end_time_str`, 
    объединенными вместе
    
    :return: string -> start time and end time
    """
    start = '1900-01-01 00:00:00'
    end = '2022-04-15 00:00:00'
    frmt = '%Y-%m-%d %H:%M:%S'
    num_hour = random.randint(12, 7 * 24)
    stime = datetime.datetime.strptime(start, frmt)
    etime = datetime.datetime.strptime(end, frmt)
    time_datetime = random.random() * (etime - stime) + stime
    start_time_str = time_datetime.strftime(frmt)
    end_time_str = (time_datetime + datetime.timedelta(hours=num_hour)).strftime(frmt)

    return "'" + start_time_str + "', '" + end_time_str + "'"


if __name__ == '__main__':
    try:
        num_port = plpy.execute("SELECT COUNT(*) FROM tb_ports")[0]['count']
        num_seacraft = plpy.execute("SELECT COUNT(*) FROM tb_seacrafts")[0]['count']
        # return str(num_port)
            
        for i in range(COL_NUM):
            portid = random.randint(1, num_port)
            seacraftid = random.randint(1, num_seacraft)
            purpose = get_random_text()
            arrival_leave_time = get_random_start_end_time()
            command = 'INSERT INTO tb_Arrivals (PortID, SeacraftID, Purpose, ArrivalTime, LeaveTime) VALUES ('
            command = command + str(portid) + ', ' + str(seacraftid) + ', ' + purpose + ', ' + arrival_leave_time + ');'
            # return command
            plpy.execute(command)

    except plpy.SPIError as e:
        return "[ERROR] %s" % e.sqlstate

    else:
        return "[Info] Successful insert"
        
$$ LANGUAGE plpython3u;

----------------------------------------------------------

TRUNCATE TABLE tb_arrivals CASCADE;
SELECT fc_InsertArrivals();  -- 运行时间 13040 秒


SELECT COUNT(*) FROM tb_arrivals; -- 运行时间 26.195 秒

```



```python

------------------------------------------------------------------------------------------------------
-- 向 tb_seacraft 中插入 1000000 条随机数据记录
-- Вставьте 1 000 000 случайных записей данных в tb_arrivals
CREATE OR REPLACE FUNCTION fc_InsertSeacrafts()
	RETURNS TEXT
	AS $$
import random
import datetime


COL_NUM = 1000000


def get_random_name():
    """
    生成一段随机 `name`
    Сгенерируйте случайный `name`.
    
    :return: text -> string
    """
    len_word = random.randint(1, 10)
    word = ''.join(random.sample('zyxwvutsrqponmlkjihgfedcba', len_word))

    return word


if __name__ == '__main__':
    try:
        num_captain = plpy.execute("SELECT COUNT(*) FROM tb_captains")[0]['count']
        num_port = plpy.execute("SELECT COUNT(*) FROM tb_ports")[0]['count']
        num_type = plpy.execute("SELECT COUNT(*) FROM tb_portlevels")[0]['count']
            
        for i in range(COL_NUM):
            regportid = random.randint(1, num_port)
            captainid = random.randint(1, num_captain)
            typeid = random.randint(1, num_type)
            displacement = random.randint(10000, 1000000)
            nameseacraft = get_random_word()

            command = 'INSERT INTO tb_seacraft(NameSeacraft, Displacement, RegPortID, TypeID, CaptainID) VALUES ('
            command = command + str(nameseacraft) + ', ' + str(displacement) + ', ' + str(regportid) + ', ' + str(typeid) + str(captainid) + ');'
            # return command
            plpy.execute(command)

    except plpy.SPIError as e:
        return "[ERROR] %s" % e.sqlstate

    else:
        return "[Info] Successful insert"
        
$$ LANGUAGE plpython3u;

----------------------------------------------------------
```



### Анализ плана выполнения запроса

> http://www.postgres.cn/docs/14/performance-tips.html
>
> http://www.postgres.cn/docs/14/using-explain.html#USING-EXPLAIN-BASICS
>
> http://www.postgres.cn/docs/14/runtime-config-query.html#RUNTIME-CONFIG-QUERY-CONSTANTS
>
> https://blog.csdn.net/kmblack1/article/details/80761647



****

**Константы стоимости для планировщика**

| Константы                              | Описание                                                     | Значение по умолчанию (стоимость) |
| -------------------------------------- | ------------------------------------------------------------ | --------------------------------- |
| `cpu_tuple_cost(floating point)`       | Задаёт приблизительную стоимость обработки ==каждой строки== при выполнении запроса | 0.01                              |
| `cpu_index_tuple_cost(floating point)` | Задаёт приблизительную стоимость обработки ==каждой записи индекса== при сканировании индекса | 0.005                             |
| `cpu_operator_cost(floating point)`    | Задаёт приблизительную стоимость обработки ==оператора или функции== при выполнении запроса | 0.0025                            |



- ==[1]== **Запрос к одной таблице, содержащий фильтрацию по нескольким полям.**

  ​    

    1. Получить план выполнения запроса **без использования индексов** (удаление индекса или отключение его использования в плане запроса).

        ```sql
        SELECT * FROM tb_arrivals WHERE ArrivalTime BETWEEN '2000-01-01 00:00:00'::TIMESTAMP AND '2001-01-01 00:00:00' AND PortID > 1000;
        
        DROP INDEX IX_ArriverTime;
        DROP INDEX IX_PortID;
        ```

        

    2. Получить статистику (IO и Time) выполнения запроса **без использования индексов**.

        ```sql
        db_port=# EXPLAIN ANALYZE SELECT * FROM tb_arrivals WHERE ArrivalTime BETWEEN '2000-01-01 00:00:00'::TIMESTAMP AND '2001-01-01 00:00:00' AND PortID > 1000;
                                                                                            QUERY PLAN
        -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
         Gather  (cost=1000.00..2348941.17 rows=326215 width=97) (actual time=1.252..27359.813 rows=332165 loops=1)
           Workers Planned: 2
           Workers Launched: 2
           ->  Parallel Seq Scan on tb_arrivals  (cost=0.00..2315319.67 rows=135923 width=97) (actual time=0.427..27321.096 rows=110722 loops=3)
                 Filter: ((arrivaltime >= '2000-01-01 00:00:00'::timestamp without time zone) AND (arrivaltime <= '2001-01-01 00:00:00'::timestamp without time zone) AND (portid > 1000))
                 Rows Removed by Filter: 33222612
         Planning Time: 3.485 ms
         Execution Time: 27368.246 ms
        (8 rows)
        ```

         

    3. Создать нужные индексы, позволяющие ускорить запрос.

        ```sql
        CREATE INDEX IX_ArriverTime ON tb_arrivals(ArrivalTime);
        CREATE INDEX IX_PortID ON tb_arrivals(PortID);
        ```

        

        Получить план выполнения запроса с использованием индексов и сравнить с первоначальным планом.

        ```sql
        db_port=# EXPLAIN ANALYZE SELECT * FROM tb_arrivals WHERE ArrivalTime BETWEEN '2000-01-01 00:00:00'::TIMESTAMP AND '2001-01-01 00:00:00' AND PortID > 1000;
                                                                                               QUERY PLAN
        -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
         Gather  (cost=459271.16..1940524.67 rows=326215 width=97) (actual time=557.093..23659.834 rows=332165 loops=1)
           Workers Planned: 2
           Workers Launched: 2
           ->  Parallel Bitmap Heap Scan on tb_arrivals  (cost=458271.16..1906903.17 rows=135923 width=97) (actual time=537.187..23605.583 rows=110722 loops=3)
                 Recheck Cond: ((arrivaltime >= '2000-01-01 00:00:00'::timestamp without time zone) AND (arrivaltime <= '2001-01-01 00:00:00'::timestamp without time zone) AND (portid > 1000))
                 Rows Removed by Index Recheck: 12492294
                 Heap Blocks: exact=14079 lossy=199261
                 ->  BitmapAnd  (cost=458271.16..458271.16 rows=326215 width=0) (actual time=551.432..551.432 rows=0 loops=1)
                       ->  Bitmap Index Scan on ix_arrivertime  (cost=0.00..16861.76 rows=804919 width=0) (actual time=96.028..96.028 rows=818208 loops=1)
                             Index Cond: ((arrivaltime >= '2000-01-01 00:00:00'::timestamp without time zone) AND (arrivaltime <= '2001-01-01 00:00:00'::timestamp without time zone))
                       ->  Bitmap Index Scan on ix_portid  (cost=0.00..441246.04 rows=40527663 width=0) (actual time=448.839..448.839 rows=40516196 loops=1)
                             Index Cond: (portid > 1000)
         Planning Time: 0.142 ms
         Execution Time: 23671.716 ms
        (14 rows)
        ```

        

    5. Получить статистику выполнения запроса с использованием индексов и сравнить с первоначальной статистикой.

        |                                | **cost**              | **actual time**    | **Planning Time** | **Execution Time** |
        | ------------------------------ | --------------------- | ------------------ | ----------------- | ------------------ |
        | **без использования индексов** | 1000.00..2348941.17   | 1.252..27359.813   | 3.485 ms          | 27368.246 ms       |
        | **с использованием индексов**  | 459271.16..1940524.67 | 557.093..23659.834 | 0.142 ms          | 23671.716 ms       |
        | **Разница**                    | -866687.6599          | -4255.82           | -3.343 ms         | -3696.5299 ms      |

        

    6. Оценить эффективность выполнения оптимизированного запроса.

        После использования индекса ==приблизительная стоимость запуска(cost)== значительно увеличилась, однако ==приблизительная общая стоимость (cost)== и ==фактическое время (Execution Time)== значительно уменьшились. ==Фактическое время (Execution Time)== сократилось на 13,506%



---



- ==[2]== **Запрос к нескольким связанным таблицам, содержащий фильтрацию по нескольким полям**

  ​    

    1. Получить план выполнения запроса **без использования индексов** (удаление индекса или отключение его использования в плане запроса).

        ```sql
        SELECT * FROM tb_arrivals INNER JOIN tb_seacrafts ON tb_arrivals.seacraftID=tb_seacrafts.IDSeacraft INNER JOIN tb_ports ON tb_arrivals.portID=tb_ports.IDPort WHERE NameSeacraft='cmari' AND NamePort='St Petersburg';
        
        DROP INDEX IX_NameSeacraft;
        DROP INDEX IX_NamePort;
        ```

        

    2. Получить статистику (IO и Time) выполнения запроса **без использования индексов**.

        ```sql
        db_port=# EXPLAIN ANALYZE SELECT * FROM tb_arrivals INNER JOIN tb_seacrafts ON tb_arrivals.seacraftID=tb_seacrafts.IDSeacraft INNER JOIN tb_ports ON tb_arrivals.portID=tb_ports.IDPort WHERE NameSeacraft='cmari' AND NamePort='St Petersburg';
                                                                               QUERY PLAN
        ---------------------------------------------------------------------------------------------------------------------------------------------------------
         Nested Loop  (cost=1008.31..2140204.13 rows=1 width=161) (actual time=698.274..29483.075 rows=6 loops=1)
           Join Filter: (tb_arrivals.seacraftid = tb_seacrafts.idseacraft)
           Rows Removed by Join Filter: 59539
           ->  Seq Scan on tb_seacrafts  (cost=0.00..20033.00 rows=1 width=29) (actual time=0.177..55.336 rows=1 loops=1)
                 Filter: ((nameseacraft)::text = 'cmari'::text)
                 Rows Removed by Filter: 999999
           ->  Gather  (cost=1008.31..2119427.53 rows=59488 width=132) (actual time=4.875..29424.577 rows=59545 loops=1)
                 Workers Planned: 2
                 Workers Launched: 2
                 ->  Hash Join  (cost=8.31..2112478.73 rows=24787 width=132) (actual time=6.244..29400.751 rows=19848 loops=3)
                       Hash Cond: (tb_arrivals.portid = tb_ports.idport)
                       ->  Parallel Seq Scan on tb_arrivals  (cost=0.00..2002819.67 rows=41666667 width=97) (actual time=0.345..27659.885 rows=33333333 loops=3)
                       ->  Hash  (cost=8.29..8.29 rows=1 width=35) (actual time=0.165..0.165 rows=1 loops=3)
                             Buckets: 1024  Batches: 1  Memory Usage: 9kB
                             ->  Index Scan using uq_ports_nameport on tb_ports  (cost=0.28..8.29 rows=1 width=35) (actual time=0.118..0.119 rows=1 loops=3)
                                   Index Cond: ((nameport)::text = 'St Petersburg'::text)
         Planning Time: 7.004 ms
         Execution Time: 29483.181 ms
        (18 rows)
        ```

         

    3. Создать нужные индексы, позволяющие ускорить запрос.

        ```sql
        CREATE INDEX IX_NameSeacraft ON tb_seacrafts(NameSeacraft);
        CREATE INDEX IX_NamePort ON tb_ports(NamePort);
        ```

        

        Получить план выполнения запроса с использованием индексов и сравнить с первоначальным планом.

        ```sql
        db_port=# EXPLAIN ANALYZE SELECT * FROM tb_arrivals INNER JOIN tb_seacrafts ON tb_arrivals.seacraftID=tb_seacrafts.IDSeacraft INNER JOIN tb_ports ON tb_arrivals.portID=tb_ports.IDPort WHERE NameSeacraft='cmari' AND NamePort='St Petersburg';
                                                                               QUERY PLAN
        ---------------------------------------------------------------------------------------------------------------------------------------------------------
         Gather  (cost=1016.76..2113212.11 rows=1 width=161) (actual time=9437.606..29046.762 rows=6 loops=1)
           Workers Planned: 2
           Workers Launched: 2
           ->  Hash Join  (cost=16.76..2112212.01 rows=1 width=161) (actual time=6601.278..29032.137 rows=2 loops=3)
                 Hash Cond: (tb_arrivals.portid = tb_ports.idport)
                 ->  Hash Join  (cost=8.46..2112203.59 rows=42 width=126) (actual time=6.039..29030.866 rows=3333 loops=3)
                       Hash Cond: (tb_arrivals.seacraftid = tb_seacrafts.idseacraft)
                       ->  Parallel Seq Scan on tb_arrivals  (cost=0.00..2002819.67 rows=41666667 width=97) (actual time=0.461..27245.982 rows=33333333 loops=3)
                       ->  Hash  (cost=8.44..8.44 rows=1 width=29) (actual time=0.353..0.356 rows=1 loops=3)
                             Buckets: 1024  Batches: 1  Memory Usage: 9kB
                             ->  Index Scan using ix_nameseacraft on tb_seacrafts  (cost=0.42..8.44 rows=1 width=29) (actual time=0.349..0.350 rows=1 loops=3)
                                   Index Cond: ((nameseacraft)::text = 'cmari'::text)
                 ->  Hash  (cost=8.29..8.29 rows=1 width=35) (actual time=0.222..0.223 rows=1 loops=3)
                       Buckets: 1024  Batches: 1  Memory Usage: 9kB
                       ->  Index Scan using ix_nameport on tb_ports  (cost=0.28..8.29 rows=1 width=35) (actual time=0.215..0.215 rows=1 loops=3)
                             Index Cond: ((nameport)::text = 'St Petersburg'::text)
         Planning Time: 3.746 ms
         Execution Time: 29047.011 ms
        (18 rows)
        ```

        

        ---

        

    4. Создать нужные индексы, позволяющие ускорить запрос.

        ```sql
        CREATE EXTENSION pg_trgm;
        CREATE INDEX IX_NameSeacraft ON tb_seacrafts USING GIN(NameSeacraft gin_trgm_ops);
        CREATE INDEX IX_NamePort ON tb_ports USING GIN(NamePort gin_trgm_ops);
        ```

        
  
        Получить план выполнения запроса с использованием индексов и сравнить с первоначальным планом.
  
        ```sql
        db_port=# EXPLAIN ANALYZE SELECT * FROM tb_arrivals INNER JOIN tb_seacrafts ON tb_arrivals.seacraftID=tb_seacrafts.IDSeacraft INNER JOIN tb_ports ON tb_arrivals.portID=tb_ports.IDPort WHERE NameSeacraft='cmari' AND NamePort='St Petersburg';
                                                                                         QUERY PLAN
        -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
         Gather  (cost=1088.34..2321635.00 rows=1 width=161) (actual time=11391.572..35022.070 rows=6 loops=1)
           Workers Planned: 2
           Workers Launched: 2
           ->  Hash Join  (cost=88.34..2320634.90 rows=1 width=161) (actual time=12996.658..35002.537 rows=2 loops=3)
                 Hash Cond: (tb_arrivals.portid = tb_ports.idport)
                 ->  Hash Join  (cost=80.03..2320626.48 rows=42 width=126) (actual time=10.302..34999.074 rows=3333 loops=3)
                       Hash Cond: (tb_arrivals.seacraftid = tb_seacrafts.idseacraft)
                       ->  Parallel Append  (cost=0.00..2211170.01 rows=41667034 width=97) (actual time=1.530..32921.062 rows=33333333 loops=3)
                             ->  Parallel Seq Scan on tb_arrivals tb_arrivals_1  (cost=0.00..2002819.67 rows=41666667 width=97) (actual time=1.517..31469.568 rows=33333333 loops=3)
                             ->  Parallel Seq Scan on tb_child_arrivals tb_arrivals_2  (cost=0.00..15.18 rows=518 width=60) (actual time=0.001..0.001 rows=0 loops=1)
                       ->  Hash  (cost=80.02..80.02 rows=1 width=29) (actual time=1.348..1.349 rows=1 loops=3)
                             Buckets: 1024  Batches: 1  Memory Usage: 9kB
                             ->  Bitmap Heap Scan on tb_seacrafts  (cost=76.01..80.02 rows=1 width=29) (actual time=1.346..1.347 rows=1 loops=3)
                                   Recheck Cond: ((nameseacraft)::text = 'cmari'::text)
                                   Heap Blocks: exact=1
                                   ->  Bitmap Index Scan on ix_nameseacraft  (cost=0.00..76.01 rows=1 width=0) (actual time=1.339..1.339 rows=1 loops=3)
                                         Index Cond: ((nameseacraft)::text = 'cmari'::text)
                 ->  Hash  (cost=8.29..8.29 rows=1 width=35) (actual time=0.151..0.152 rows=1 loops=3)
                       Buckets: 1024  Batches: 1  Memory Usage: 9kB
                       ->  Index Scan using uq_ports_nameport on tb_ports  (cost=0.28..8.29 rows=1 width=35) (actual time=0.083..0.084 rows=1 loops=3)
                             Index Cond: ((nameport)::text = 'St Petersburg'::text)
         Planning Time: 1.025 ms
         Execution Time: 35022.279 ms
        (23 rows)
        ```
  
        
  
    5. Получить статистику выполнения запроса с использованием индексов и сравнить с первоначальной статистикой.
  
        |                                     | **cost**            | **actual time**      | **Planning Time** | **Execution Time** | **Разница Execution Time с неиспользуемыми индексами** |
        | ----------------------------------- | ------------------- | -------------------- | ----------------- | ------------------ | ------------------------------------------------------ |
        | **без использования индексов**      | 1008.31..2140204.13 | 698.274..29483.075   | 7.004 ms          | 29483.181 ms       |                                                        |
        | **==с использованием индексов==**   | 1016.76..2113212.11 | 9437.606..29046.762  | 3.746 ms          | 29047.011 ms       | -436.17 ms                                             |
        | **с использованием индексов (GIN)** | 1088.34..2321635.00 | 11180.878..35380.249 | 1.025             | 35022.279 ms       | +5539.09 ms                                            |
        
        
        
    6. Оценить эффективность выполнения оптимизированного запроса.
  
        При добавлении индексов к двум полям `varchar` подтаблицы значительного улучшения **в скорости запросов не наблюдается.** GIN-индексирование в этом случае вместо того, чтобы ускорить запрос, делает его медленнее.
  
        

---





- ==[3]== **Также необходимо продемонстрировать полезность индексов для организации полнотекстового поиска.**

  ​    

    1. Получить план выполнения запроса **без использования индексов** (удаление индекса или отключение его использования в плане запроса).

        ```sql
        SELECT * FROM tb_arrivals WHERE Purpose LIKE '%at%';
        
        DROP INDEX IX_Purpose;
        ```

        

    2. Получить статистику (IO и Time) выполнения запроса **без использования индексов**.

        ```sql
        db_port=# EXPLAIN ANALYZE SELECT * FROM tb_arrivals WHERE Purpose LIKE '% at %';
                                                                      QUERY PLAN
        --------------------------------------------------------------------------------------------------------------------------------------
         Gather  (cost=1000.00..2108981.63 rows=9953 width=97) (actual time=2.708..35207.244 rows=145614 loops=1)
           Workers Planned: 2
           Workers Launched: 2
           ->  Parallel Seq Scan on tb_arrivals  (cost=0.00..2106986.33 rows=4147 width=97) (actual time=2.798..35181.150 rows=48538 loops=3)
                 Filter: (purpose ~~ '% at %'::text)
                 Rows Removed by Filter: 33284795
         Planning Time: 0.337 ms
         Execution Time: 35212.464 ms
        (8 rows)
        ```

         

    3. Создать нужные индексы, позволяющие ускорить запрос.

        ```sql
        CREATE INDEX IX_Purpose ON tb_arrivals(Purpose);
        ```

        

        Получить план выполнения запроса с использованием индексов и сравнить с первоначальным планом.

        ```sql
        db_port=# EXPLAIN ANALYZE SELECT * FROM tb_arrivals WHERE Purpose LIKE '% at %';
                                                                      QUERY PLAN
        --------------------------------------------------------------------------------------------------------------------------------------
         Gather  (cost=1000.00..2108981.63 rows=9953 width=97) (actual time=3.036..36736.283 rows=145614 loops=1)
           Workers Planned: 2
           Workers Launched: 2
           ->  Parallel Seq Scan on tb_arrivals  (cost=0.00..2106986.33 rows=4147 width=97) (actual time=0.982..36713.617 rows=48538 loops=3)
                 Filter: (purpose ~~ '% at %'::text)
                 Rows Removed by Filter: 33284795
         Planning Time: 5.599 ms
         Execution Time: 36741.591 ms
        (8 rows)
        ```

        

    4. Создать нужные индексы (GIN), позволяющие ускорить запрос.

        ```sql
        CREATE INDEX IX_Purpose ON tb_arrivals USING GIN(Purpose gin_trgm_ops);
        ```

        

        Получить план выполнения запроса с использованием индексов и сравнить с первоначальным планом.
  
        ```sql
        db_port=# EXPLAIN ANALYZE SELECT * FROM tb_arrivals WHERE Purpose LIKE '% at %';
                                                                              QUERY PLAN
        -------------------------------------------------------------------------------------------------------------------------------------------------------
         Append  (cost=1277.14..38806.13 rows=9960 width=97) (actual time=711.662..21840.648 rows=145614 loops=1)
           ->  Bitmap Heap Scan on tb_arrivals tb_arrivals_1  (cost=1277.14..38735.33 rows=9953 width=97) (actual time=711.661..21829.443 rows=145614 loops=1)
                 Recheck Cond: (purpose ~~ '% at %'::text)
                 Rows Removed by Index Recheck: 8520120
                 Heap Blocks: exact=33655 lossy=137020
                 ->  Bitmap Index Scan on ix_purpose  (cost=0.00..1274.65 rows=9953 width=0) (actual time=706.322..706.322 rows=180530 loops=1)
                       Index Cond: (purpose ~~ '% at %'::text)
           ->  Seq Scan on tb_child_arrivals tb_arrivals_2  (cost=0.00..21.00 rows=7 width=60) (actual time=0.062..0.062 rows=0 loops=1)
                 Filter: (purpose ~~ '% at %'::text)
         Planning Time: 27.951 ms
         Execution Time: 21846.879 ms
        (11 rows)
        ```

        

        

    5. Получить статистику выполнения запроса с использованием индексов и сравнить с первоначальной статистикой.
  
        |                                | **cost**            | **actual time**  | **Planning Time** | **Execution Time** |
        | ------------------------------ | ------------------- | ---------------- | ----------------- | ------------------ |
        | **без использования индексов** | 1000.00..2108981.63 | 2.708..35207.244 | 0.337 ms          | 35212.464 ms       |
        | **с использованием индексов**  | 1000.00..2108981.63 | 3.032..36313.774 | 4.645 ms          | 36319.114 ms       |
        | с использованием индексов(GIN) |                     |                  | 27.951 ms         | 21846.879 ms       |
        | **Разница**                    | 0                   | 1106.2059        | 4.308 ms          | 1106.65 ms         |

        

    6. Оценить эффективность выполнения оптимизированного запроса.

        Несмотря на то, что для текстового поля создан индекс, база данных **не использует его для запросов**
  
        

---



- ==[4]== **Также необходимо продемонстрировать полезность индексов для организации полнотекстового поиска.**

  ​    

    1. Получить план выполнения запроса **без использования индексов** (удаление индекса или отключение его использования в плане запроса).

        ```sql
        SELECT * FROM tb_arrivals WHERE char_length(Purpose) > 20;
        
        DROP INDEX IX_Purpose;
        ```

        

    2. Получить статистику (IO и Time) выполнения запроса **без использования индексов**.

        ```sql
        db_port=*# EXPLAIN ANALYZE SELECT * FROM tb_arrivals WHERE char_length(Purpose) > 20;
                                                                            QUERY PLAN
        --------------------------------------------------------------------------------------------------------------------------------------------------
         Append  (cost=0.00..3252844.33 rows=33333626 width=97) (actual time=0.522..22543.607 rows=86235207 loops=1)
           ->  Seq Scan on tb_arrivals tb_arrivals_1  (cost=0.00..3086153.00 rows=33333333 width=97) (actual time=0.521..19450.968 rows=86235207 loops=1)
                 Filter: (char_length(purpose) > 20)
                 Rows Removed by Filter: 13764793
           ->  Seq Scan on tb_child_arrivals tb_arrivals_2  (cost=0.00..23.20 rows=293 width=60) (actual time=0.026..0.026 rows=0 loops=1)
                 Filter: (char_length(purpose) > 20)
         Planning Time: 2.516 ms
         Execution Time: 24233.586 ms
        (8 rows)
        ```

         

    3. Получить план выполнения запроса с использованием индексов и сравнить с первоначальным планом.

        ```sql
        CREATE INDEX IX_Purpose ON tb_arrivals USING GIN(Purpose gin_trgm_ops);
        ```

        

        Получить план выполнения запроса с использованием индексов и сравнить с первоначальным планом.
  
        ```sql
        db_port=# EXPLAIN ANALYZE SELECT * FROM tb_arrivals WHERE char_length(Purpose) > 20;
                                                                            QUERY PLAN
        --------------------------------------------------------------------------------------------------------------------------------------------------
         Append  (cost=0.00..3252844.33 rows=33333626 width=97) (actual time=0.514..23314.352 rows=86235207 loops=1)
           ->  Seq Scan on tb_arrivals tb_arrivals_1  (cost=0.00..3086153.00 rows=33333333 width=97) (actual time=0.513..20128.237 rows=86235207 loops=1)
                 Filter: (char_length(purpose) > 20)
                 Rows Removed by Filter: 13764793
           ->  Seq Scan on tb_child_arrivals tb_arrivals_2  (cost=0.00..23.20 rows=293 width=60) (actual time=0.042..0.042 rows=0 loops=1)
                 Filter: (char_length(purpose) > 20)
         Planning Time: 0.602 ms
         Execution Time: 25058.894 ms
        (8 rows)
        ```

        

        

    4. Получить статистику выполнения запроса с использованием индексов и сравнить с первоначальной статистикой.
  
        |                                | **cost**         | **actual time**  | **Planning Time** | **Execution Time** |
        | ------------------------------ | ---------------- | ---------------- | ----------------- | ------------------ |
        | **без использования индексов** | 0.00..3252844.33 | 0.522..22543.607 | 2.516 ms          | 24233.586 ms       |
        | с использованием индексов(GIN) | 0.00..3252844.33 | 0.514..23314.352 | 0.602 ms          | 25058.894 ms       |
        
  

---



- ==[5]== **Также необходимо продемонстрировать полезность индексов для организации полнотекстового поиска.**

  ​    

    1. Получить план выполнения запроса **без использования индексов** (удаление индекса или отключение его использования в плане запроса).

        ```sql
        SELECT * FROM tb_arrivals WHERE Purpose='sfrht';
        
        DROP INDEX IX_Purpose;
        ```

        

    2. Получить статистику (IO и Time) выполнения запроса **без использования индексов**.

        ```sql
        db_port=*# EXPLAIN ANALYZE SELECT * FROM tb_arrivals WHERE Purpose='sfrht';
                                                                              QUERY PLAN
        -------------------------------------------------------------------------------------------------------------------------------------------------------
         Gather  (cost=1000.00..2108005.45 rows=26 width=91) (actual time=30218.895..30220.101 rows=0 loops=1)
           Workers Planned: 2
           Workers Launched: 2
           ->  Parallel Append  (cost=0.00..2107002.85 rows=10 width=91) (actual time=30192.606..30192.609 rows=0 loops=3)
                 ->  Parallel Seq Scan on tb_arrivals tb_arrivals_1  (cost=0.00..2106986.33 rows=9 width=97) (actual time=30192.604..30192.604 rows=0 loops=3)
                       Filter: (purpose = 'sfrht'::text)
                       Rows Removed by Filter: 33333333
                 ->  Parallel Seq Scan on tb_child_arrivals tb_arrivals_2  (cost=0.00..16.47 rows=2 width=60) (actual time=0.002..0.002 rows=0 loops=1)
                       Filter: (purpose = 'sfrht'::text)
         Planning Time: 1.095 ms
         Execution Time: 30220.227 ms
        (11 rows)
        ```

         

    3. Получить план выполнения запроса с использованием индексов и сравнить с первоначальным планом.

        ```sql
        CREATE INDEX IX_Purpose ON tb_arrivals USING GIN(Purpose gin_trgm_ops);
        ```

        

        Получить план выполнения запроса с использованием индексов и сравнить с первоначальным планом.
  
        ```sql
        db_port=# EXPLAIN ANALYZE SELECT * FROM tb_arrivals WHERE Purpose='sfrht';
                                                                         QUERY PLAN
        ---------------------------------------------------------------------------------------------------------------------------------------------
         Append  (cost=2396.17..2505.33 rows=26 width=91) (actual time=657.419..657.419 rows=0 loops=1)
           ->  Bitmap Heap Scan on tb_arrivals tb_arrivals_1  (cost=2396.17..2484.20 rows=22 width=97) (actual time=657.409..657.409 rows=0 loops=1)
                 Recheck Cond: (purpose = 'sfrht'::text)
                 Rows Removed by Index Recheck: 23
                 Heap Blocks: exact=23
                 ->  Bitmap Index Scan on ix_purpose  (cost=0.00..2396.17 rows=22 width=0) (actual time=642.080..642.080 rows=23 loops=1)
                       Index Cond: (purpose = 'sfrht'::text)
           ->  Seq Scan on tb_child_arrivals tb_arrivals_2  (cost=0.00..21.00 rows=4 width=60) (actual time=0.008..0.008 rows=0 loops=1)
                 Filter: (purpose = 'sfrht'::text)
         Planning Time: 14.311 ms
         Execution Time: 657.908 ms
        (11 rows)
        ```

        

        

    4. Получить статистику выполнения запроса с использованием индексов и сравнить с первоначальной статистикой.
  
        |                                    | **cost**            | **actual time**      | **Planning Time** | **Execution Time** |
        | ---------------------------------- | ------------------- | -------------------- | ----------------- | ------------------ |
        | **без использования индексов**     | 1000.00..2108005.45 | 30218.895..30220.101 | 1.095 ms          | 30220.227 ms       |
        | **с использованием индексов(GIN)** | 2396.17..2505.33    | 657.419..657.419     | 14.311 ms         | 657.908 ms         |
        | **Разница**                        |                     |                      |                   | -29562.319 ms      |





## lab 3.2

> http://www.postgres.cn/docs/14/datatype-json.html
>
> https://juejin.cn/post/6844903857009623048
>
> https://segmentfault.com/a/1190000019344353
>
> https://programmers.buzz/posts/start-exploring-database-indices/
>
> https://habr.com/ru/company/oleg-bunin/blog/646987/

### IMDB-JSONB

Были использованы все три набора данных: `actors.list.txt`, `actresses.list.txt`, `name.basics.tsv`.

Скрипты, используемые для обработки данных:

1. Из-за того, что одновременная обработка всех данных может занимать много памяти. Поэтому используйте скрипт Python для разделения набора данных на более мелкие части и их последующего объединения

    Объединенный результат сохраняется в виде двоичного файла с использованием сериализации Python для уменьшения использования памяти и жесткого диска, а также для облегчения последующей обработки.

    <img src="doc/pic/README/image-20220426124349983.png" alt="image-20220426124349983" style="zoom:50%;" />

    ![image-20220427221234460](doc/pic/README/image-20220427221234460.png)

    

    В этом скрипте можно объединить все фильмы одного актера в один

    ```python
    # ------*------ coding: utf-8 ------*------
    # @Time    : 2022/4/26 16:39
    # @Author  : 冰糖雪狸 (NekoSilverfox)
    # @Project : IMDB 数据处理
    # @File    : 切割提取.py
    # @Software: PyCharm
    # @Github  ：https://github.com/NekoSilverFox
    # -----------------------------------------
    import pandas as pd
    import numpy as np
    import datetime
    import pickle
    import re
    
    
    def normal_actor(source_data: pd.DataFrame, dump_name_title: str, dump_df_res: str) -> pd.DataFrame:
        """
        将 IMDB 的演员数据标准化为 pd.DataFrame。每个演员及其各个作品独占一行（类似于交叉表）
        建议之前将数据通过 VS Code 处理
        :param file_path:
        :return: pd.DataFrame
        """
    
        """
        使用正则表达式提取作品名、上映日期、系列名，并将他们作为新的 DataFrame
        所以取得的结果为带 MutIndex 的 DataFrame
        """
        print('>>' * 50)
        print('[INFO] 开始提取字符串中的信息')
        time_start = datetime.datetime.now()
        list_name_title = []
        i = 1
        name_list = []
        for col in source_data.values:
            if col[0] is not np.nan:
                names = col[0]
                name_list = names.split(', ')
    
            if len(name_list) == 0:
                continue
    
            for this_name in name_list:
    
                title_mix = col[1]
    
                # Регулярные выражения используются для извлечения
                """title 电影标题 字符串前一部分 """
                title = re.search(r'^[^\(\{\[]*', title_mix)
                if title is not None:
                    title = str(title.group()[:-1])
    
                """year 上映年份 ()"""
                year = re.search(r'(?!=\({1})[\d]{4}(?!=\){1})', title_mix)
                if year is not None:
                    year = int(year.group())
    
                """series name 系列名称： {}"""
                series_name = re.search(r'\{(.*?)\}', title_mix)
                if series_name is not None:
                    series_name = str(series_name.group()[1:-1])
    
                """character name 角色名称"""
                character_name = re.search(r'\[(.*?)\]', title_mix)
                if character_name is not None:
                    character_name = str(character_name.group()[1:-1])
                # name_title.append([this_name, title, series_name, year, character_name])
                # name_title.append([this_name, [title, series_name, year, character_name]])
                rols = pd.DataFrame([[title, series_name, year, character_name]],
                                    columns=['title', 'series name', 'year', 'character name'])
    
                list_name_title.append([this_name, rols])  # this_name 是 str, rols 是DataFrame
    
            if i % 10000 == 0:
                use_sec = (datetime.datetime.now() - time_start).seconds
                print('[INFO] 已处理 ', i, ' 行 | ', (i / source_data.shape[0]) * 100, '% | 已用时：', use_sec, ' 秒（', use_sec / 60,
                      '）分钟')
            i += 1
    
        use_sec = (datetime.datetime.now() - time_start).seconds
        print('[INFO] 数据提取结束，用时：', use_sec, ' 秒（', use_sec / 60, '）分钟')
    
        """将取得的结果 df_name_title 为带 MutIndex 的 DataFrame"""
        print('>>' * 50)
        print('[INFO] 将取得的结果 df_name_title 为带 MutIndex 的 DataFrame')
        time_start = datetime.datetime.now()
        df_name_title = pd.DataFrame(list_name_title, columns=['name', 'rols'])
        list_name_title = []
        df_name_title.sort_values(by='name', inplace=True)
        df_name_title.reset_index(drop=True, inplace=True)
        use_sec = (datetime.datetime.now() - time_start).seconds
        print('[INFO] DataFrame 转换结束，用时：', use_sec, ' 秒（', use_sec / 60, '）分钟')
    
        # print('>>' * 50)
        # print('[INFO] 开始序列化（备份）df_name_title')
        # time_start = datetime.datetime.now()
        # f = open(dump_name_title, 'wb')
        # pickle.dump(obj=df_name_title, file=f)
        # f.close()
        # use_sec = (datetime.datetime.now() - time_start).seconds
        # print('[INFO] 序列化（备份）结束，用时：', use_sec, ' 秒（', use_sec / 60, '）分钟')
    
        """合并重复的 name，使其唯一。rols 中增加同一演员的信息"""
        print('>>' * 50)
        print('[INFO] 开始合并重复的 name')
        time_start = datetime.datetime.now()
        name = None
        tmp_df_rols = []
        res_list_name_rols = []
        for i in range(df_name_title.shape[0]):
    
            """如果为同一人，即将作品合并的到一个 DataFrame 中"""
            if name == df_name_title.loc[i]['name']:
                tmp_df_rols = pd.concat([tmp_df_rols, df_name_title.loc[i]['rols']])
    
            else:
                """开始下一个人
                    先将上一个人的信息写入到新的 list 中，再重置 name 和 tmp_df_rols 为当前行的内容
                """
                if name is not None:
                    res_list_name_rols.append([name, tmp_df_rols])
    
                    # if name == '$haniqua':
                    #     print(tmp_df_rols)
    
                name = df_name_title.loc[i]['name']
                tmp_df_rols = df_name_title.loc[i]['rols']
    
            if i % 10000 == 0:
                use_sec = (datetime.datetime.now() - time_start).seconds
                print('[INFO] 已处理 ', i, ' 行 | ', (i / df_name_title.shape[0]) * 100, '% | 已用时：', use_sec, ' 秒（',
                      use_sec / 60, '）分钟')
    
        res_list_name_rols = pd.DataFrame(data=res_list_name_rols, columns=['name', 'rols'])
    
        # print('>>' * 50)
        # print('[INFO] 开始序列化（备份）res_list_name_rols')
        # time_start = datetime.datetime.now()
        # f = open(dump_df_res, 'wb')
        # pickle.dump(obj=res_list_name_rols, file=f)
        # f.close()
        # use_sec = (datetime.datetime.now() - time_start).seconds
        # print('[INFO] 序列化（备份）res_list_name_rols 结束，用时：', use_sec, ' 秒（', use_sec / 60, '）分钟')
    
        return res_list_name_rols
    
    
    if __name__ == '__main__':
        print('>>' * 50)
        print('[INFO] 开始执行')
    
        ##################################################################################################################
        # 演员信息表
        print('>>' * 50)
        print('[INFO] 开始读取 `name.basics.tsv`')
        time_start = datetime.datetime.now()
        df_name_info = pd.read_csv(
            filepath_or_buffer='/Users/fox/Library/CloudStorage/OneDrive-PetertheGreatSt'
                               '.PetersburgPolytechnicalUniversity/СПБПУ/3 курс/6 семестр/СУБД/资料/DataSet/name.basics.tsv',
            header=0,
            sep='\t'
        )
        df_name_info = df_name_info.iloc[:, :-1]
        df_name_info.columns = ['nconst', 'name', 'birthYear', 'deathYear', 'profession']
        time_end = datetime.datetime.now()
        print('[INFO] 读取 `name.basics.tsv`结束，用时：', (time_end - time_start).seconds, ' 秒')
        ##################################################################################################################
    
        ##################################################################################################################
        # 处理缺失值为 None，方便转换为 JSON
        print('>>' * 50)
        print('[INFO] 开始处理缺失值为 None 并移除重复值，方便转换为 JSON')
        time_start = datetime.datetime.now()
        df_name_info.replace(to_replace=['\\N', np.nan], value=None, inplace=True)
        df_name_info.drop_duplicates(subset='name', keep='first', inplace=True)
        time_end = datetime.datetime.now()
        print('[INFO] 处理缺失值并移除重复值结束，用时：', (time_end - time_start).seconds, ' 秒')
        ##################################################################################################################
    
    
        ##################################################################################################################
        print('>>' * 50)
        print('[INFO] 开始读取文件', '/Users/fox/Library/CloudStorage/OneDrive-PetertheGreatSt'
                               '.PetersburgPolytechnicalUniversity/СПБПУ/3 курс/6 '
                               'семестр/СУБД/资料/DataSet/data_actors.list.txt')
        time_start = datetime.datetime.now()
        # source_data = pd.read_csv(
        #     filepath_or_buffer='/Users/fox/Library/CloudStorage/OneDrive-PetertheGreatSt.PetersburgPolytechnicalUniversity/СПБПУ/3 '
        #               'курс/6 семестр/СУБД/资料/DataSet/data_actresses.list.txt',
        #     header=0,
        #     sep='\t'
        # )
    
        # 男演员列表df
        source_data = pd.read_csv(
            filepath_or_buffer='/Users/fox/Library/CloudStorage/OneDrive-PetertheGreatSt.PetersburgPolytechnicalUniversity/СПБПУ/3 '
                      'курс/6 семестр/СУБД/资料/DataSet/data_actors.list.txt',
            header=0,
            sep='\t'
        )
        time_end = datetime.datetime.now()
        print('[INFO] 读取文件结束，用时：', (time_end - time_start).seconds, ' 秒')
    
    
    
        print('>>' * 50)
        print('[INFO] 开始数据预处理')
        time_start = datetime.datetime.now()
        source_data.columns = ['name', 't1', 't2', 't3']
        source_data['t1'].fillna(value='', inplace=True)
        source_data['t2'].fillna(value='', inplace=True)
        source_data['t3'].fillna(value='', inplace=True)
    
        movie_list = source_data['t1'] + source_data['t2'] + source_data['t3']
        source_data = pd.concat([source_data['name'], movie_list], axis=1)
        source_data.columns = ['name', 'title_mix']
    
        # source_data = source_data.iloc[:1000, :]
    
        time_end = datetime.datetime.now()
        print('[INFO] 数据预处理结束，用时：', (time_end - time_start).seconds, ' 秒')
    
    
        start_index = 0
        step_index = 1000000
        end_index = start_index + step_index
        times = 31
    
    
    
        for i in range(1, times):
            print('\n\n')
            print('>>' * 20, ' 开始执行第 ', i, ' 个循环', '<<' * 20)
    
            tmp_source_data = source_data.iloc[start_index:end_index, :]
    
            ##################################################################################################################
            # # 女演员列表df
            # print('[INFO]  main -> 开始处理 `data_actresses.list.txt`')
            # df_actresses = normal_actor(
            #     source_data=tmp_source_data,
            #     dump_name_title='./result/dump_df_actresses_name_title.bits',
            #     dump_df_res='./result/dump_df_actresses.bits'
            # )
            # tmp_source_data = None
            # print('[INFO] main <- 处理 `data_actresses.list.txt`结束')
            ##################################################################################################################
    
    
            ##################################################################################################################
            # # 男演员列表df
            # print('[INFO] Start handle `data_actors.list.txt`')
            # df_actors = normal_actor(
            #     file_path='/Users/fox/Library/CloudStorage/OneDrive-PetertheGreatSt.PetersburgPolytechnicalUniversity/СПБПУ/3 '
            #               'курс/6 семестр/СУБД/资料/DataSet/data_actors.list.txt'
            # )
            print('[INFO]  main -> 开始处理 `data_actors.list.txt`')
            df_actresses = normal_actor(
                source_data=tmp_source_data,
                dump_name_title='./result/dump_df_actors_name_title.bits',
                dump_df_res='./result/dump_df_actors.bits'
            )
            tmp_source_data = None
            print('[INFO] main <- 处理 `data_actresses.list.txt`结束')
            ##################################################################################################################
    
            ##################################################################################################################
            print('>>' * 50)
            print('[INFO] 开始 merge 两张大表，以处理为最终结果')
            time_start = datetime.datetime.now()
            df_all = pd.merge(left=df_name_info,
                              right=df_actresses,
                              how='inner',
                              on='name')
            time_end = datetime.datetime.now()
            print('[INFO] merge 结束，用时：', (time_end - time_start).seconds, ' 秒')
    
            df_actresses = None
            print('[INFO] 释放内存')
            ##################################################################################################################
    
            print('>>' * 50)
            print('[INFO] 开始序列化（备份）合并后的最终结果')
            time_start = datetime.datetime.now()
            dump_df_res = '/Users/fox/Library/CloudStorage/OneDrive-PetertheGreatSt.PetersburgPolytechnicalUniversity/СПБПУ/3 курс/6 семестр/СУБД/资料/DataSet/result_dump_actors/dump_actors_' + str(i) +'.bits'
            f = open(dump_df_res, 'wb')
            pickle.dump(obj=df_all, file=f)
            f.close()
            use_sec = (datetime.datetime.now() - time_start).seconds
            print('[INFO] 序列化（备份）合并后的最终结果结束，用时：', use_sec, ' 秒（', use_sec / 60, '）分钟')
    
    
            ##################################################################################################################
            print('[INFO] Start write to JSON file')
            df_all.to_json(
                path_or_buf='/Users/fox/Library/CloudStorage/OneDrive-PetertheGreatSt.PetersburgPolytechnicalUniversity'
                            '/СПБПУ/3 курс/6 семестр/СУБД/资料/DataSet/result_json_actors/df_final_actors_' + str(i) + '.json',
                orient='records',
                lines=True)
            print('[INFO] JSON 写入完成')
            df_all = None
            print('[INFO] 释放内存')
            ##################################################################################################################
    
            start_index += step_index
            end_index += step_index
    
        pass
    
    ```

    

2. Десериализовать все полученные малые наборы данных и сшить их вместе в большой набор данных, а также удалить дублирующиеся значения

    ```python
    # ------*------ coding: utf-8 ------*------
    # @Time    : 2022/4/27 14:37
    # @Author  : 冰糖雪狸 (NekoSilverfox)
    # @Project : IMDB 数据处理
    # @File    : 反序列化数据.py.py
    # @Software: PyCharm
    # @Github  ：https://github.com/NekoSilverFox
    # -----------------------------------------
    import pickle
    import datetime
    import pandas as pd
    
    
    def concat_df(bits_file_path_header: str,
                  max_index: int,
                  path_result_bits_save: str) -> pd.DataFrame:
        """
        从许多序列化文件中反序列化，并且拼接他们
        :param bits_file_path_header: 序列化文件的【文件头】
        :param max_index: 文件头的最大索引
        :param path_result_bits_save: 合并结果的反序列化保存位置
        :return: 反序列化后的 DataFrame
        """
        df_result = None
    
        for i in range(1, max_index + 1):
            print('-' * 50)
            print('[INFO] 开始读取第 ', i, '个文件')
            time_start = datetime.datetime.now()
            bits_file_path = bits_file_path_header + str(i) + '.bits'
            f = open(bits_file_path, 'rb')
            df_obj = pickle.load(file=f)
            f.close()
            time_end = datetime.datetime.now()
            print('[INFO] 读取第 ', i, '个文件结束，用时：', (time_end - time_start).seconds, ' 秒\n')
    
            if i == 1:
                df_result = df_obj
                continue
    
            print('[INFO] 开始拼接第 ', i, '个文件')
            time_start = datetime.datetime.now()
            df_result = pd.concat([df_result, df_obj])
            time_end = datetime.datetime.now()
            print('[INFO] 拼接第 ', i, '个文件结束，用时：', (time_end - time_start).seconds, ' 秒\n')
    
        # 合并结束，使用序列化保存结果
        print('-' * 50)
        print('[INFO] 合并结束，使用序列化保存结果')
        time_start = datetime.datetime.now()
        f = open(path_result_bits_save, 'wb')
        pickle.dump(obj=df_result, file=f)
        f.close()
        time_end = datetime.datetime.now()
        print('[INFO] 序列化保存结果结束，用时：', (time_end - time_start).seconds, ' 秒\n')
    
        return df_result
    
    
    def merge_duplicates(df_source: pd.DataFrame) -> pd.DataFrame:
        """
        将最终的结果再次去重
        :param df_source: 合并男女演员是数组
        :return: 合并去重后的 DataFrame
        """
        df_source.sort_values(by='nconst', inplace=True)
        df_source.reset_index(drop=True, inplace=True)
    
        i_current = 0
        i_next = i_current + 1
        stop_index = df_source.shape[0]
        while i_next <= stop_index:
            while df_source.loc[i_current]['nconst'] == df_source.loc[i_next]['nconst']:
                df_source.loc[i_current]['rols'] = pd.concat([df_source.loc[i_current]['rols'], df_source.loc[i_next]['rols']])
                df_source.drop(index=i_next, inplace=True)
                i_next += 1
    
                if i_next == stop_index:
                    df_source.reset_index(drop=True, inplace=True)
                    return df_source
    
            print('[INFO] 已合并 ', i_current, ' 行 | ', round(i_current / df_source.shape[0] * 100, 4), '%')
            i_current = i_next
            i_next += 1
    
        df_source.reset_index(drop=True, inplace=True)
        return df_source
    
    
    if __name__ == '__main__':
        ################################################################################################################
        # 合并所有男演员（actors）
        ################################################################################################################
        print('>>' * 50)
        bits_file_path_header = '/Users/fox/Library/CloudStorage/OneDrive-PetertheGreatSt' \
                                '.PetersburgPolytechnicalUniversity/СПБПУ/3 курс/6 ' \
                                'семестр/СУБД/资料/DataSet/result_dump_actors/dump_actors_'
    
        path_result_bits_save = '/Users/fox/Library/CloudStorage/OneDrive-PetertheGreatSt' \
                                '.PetersburgPolytechnicalUniversity/СПБПУ/3 курс/6 ' \
                                'семестр/СУБД/资料/DataSet/result_dump_actors/dump_actors_ALL.bits'
    
        df_all_actors = concat_df(bits_file_path_header=bits_file_path_header,
                                  max_index=20,
                                  path_result_bits_save=path_result_bits_save)
        print('[INFO] 合并并序列化输出成功！\n输出至：', path_result_bits_save)
    
    
        ################################################################################################################
        # 合并所有女演员（actors）
        ################################################################################################################
        print('>>' * 50)
        bits_file_path_header = '/Users/fox/Library/CloudStorage/OneDrive-PetertheGreatSt' \
                                '.PetersburgPolytechnicalUniversity/СПБПУ/3 курс/6 ' \
                                'семестр/СУБД/资料/DataSet/result_dump_actresses/dump_actresses_'
    
        path_result_bits_save = '/Users/fox/Library/CloudStorage/OneDrive-PetertheGreatSt' \
                                '.PetersburgPolytechnicalUniversity/СПБПУ/3 курс/6 ' \
                                'семестр/СУБД/资料/DataSet/result_dump_actresses/dump_actresses_ALL.bits'
    
        df_all_actresses = concat_df(bits_file_path_header=bits_file_path_header,
                                     max_index=13,
                                     path_result_bits_save=path_result_bits_save)
        print('[INFO] 合并并序列化输出成功！\n输出至：', path_result_bits_save)
    
    
        ################################################################################################################
        # 合并所有男演员（actors）和女演员（actors）
        ################################################################################################################
        print('>>' * 50)
        print('[INFO] 合并所有男演员（actors）和女演员（actors）')
        time_start = datetime.datetime.now()
    
        df_result_all = pd.concat([df_all_actors, df_all_actresses])
    
        time_end = datetime.datetime.now()
        print('[INFO] 合并所有男演员（actors）和女演员（actors）结束，用时：', (time_end - time_start).seconds, ' 秒\n')
    
        ################################################################################################################
        df_all_actors = None
        df_all_actresses = None
        print('[INFO] 内存释放')
        ################################################################################################################
    
    
        ################################################################################################################
        # 合并后的最终结果再次去重
        ################################################################################################################
        print('>>' * 50)
        print('[INFO] 合并后的最终结果再次去重')
        time_start = datetime.datetime.now()
        df_result_all = merge_duplicates(df_source=df_result_all)
        time_end = datetime.datetime.now()
        print('[INFO] 合并后的最终结果再次去重结束：', (time_end - time_start).seconds, ' 秒\n')  # [INFO] 合并后的最终结果再次去重结束： 9714  秒
    
        ################################################################################################################
        # 合并后的最终结果再序列化并保存为 JSON 文件
        ################################################################################################################
        path_result_bits_save = '/Users/fox/Library/CloudStorage/OneDrive-PetertheGreatSt' \
                                '.PetersburgPolytechnicalUniversity/СПБПУ/3 курс/6 ' \
                                'семестр/СУБД/资料/DataSet/result_ALL/dump_ALL.bits'
        print('>>' * 50)
        print('[INFO] 合并结束，使用序列化保存[最终]结果')
        time_start = datetime.datetime.now()
        f = open(path_result_bits_save, 'wb')
        pickle.dump(obj=df_result_all, file=f)
        f.close()
        time_end = datetime.datetime.now()
        print('[INFO] 序列化保存结果结束，用时：', (time_end - time_start).seconds, ' 秒\n')
    
    
        path_result_json_save = '/Users/fox/Library/CloudStorage/OneDrive-PetertheGreatSt' \
                                '.PetersburgPolytechnicalUniversity/СПБПУ/3 курс/6 ' \
                                'семестр/СУБД/资料/DataSet/result_ALL/dump_ALL.json'
        print('>>' * 50)
        print('[INFO] 保存[最终]结果为 JSON')
        time_start = datetime.datetime.now()
        df_result_all.to_json(path_or_buf=path_result_json_save,
                              orient='records',
                              lines=True)
        time_end = datetime.datetime.now()
        print('[INFO] 保存[最终]结果为 JSON，用时：', (time_end - time_start).seconds, ' 秒\n')
        ################################################################################################################
        pass
    
    ```

    

3. Выполнение тестов на скорость, сериализация и построение результатов в виде изображений

    ```sql
    # ------*------ coding: utf-8 ------*------
    # @Time    : 2022/4/28 14:22
    # @Author  : 冰糖雪狸 (NekoSilverfox)
    # @Project : JSON 速度测试
    # @File    : 速度测试.py
    # @Software: PyCharm
    # @Github  ：https://github.com/NekoSilverFox
    # -----------------------------------------
    import psycopg2 as pg
    import matplotlib.pyplot as plt
    import pandas as pd
    import datetime
    import pickle
    
    
    def get_id_len_json_df():
        """
        获取数据库中每个 ID 对应 JSON data 的长度
        :return:
        """
        # 如果数据库不存在，那么它将自动创建，最后将返回一个数据库对象
        print('>>' * 50)
        print('[INFO] Start connect database')
        conn = pg.connect(database="db_imdb",
                          user="postgres",
                          password="postgres",
                          host="localhost",
                          port="5432")
        cur = conn.cursor()
        print('[INFO] Connect database successfully')
    
        # 获取行数
        cur.execute("SELECT COUNT(*) FROM tb_json;")
        count_row = cur.fetchall()[0][0]
        print('行数：', count_row)
    
        # 用于统计的 DataFrame
        df_counter = pd.DataFrame([[0, 0]], columns=['id', 'len_json'])
    
        # 执行查询并记录时间
        for i in range(1, count_row):
            print('[INFO] 正在测试第 ' + str(i) + '行 | ' + str(round(i / count_row * 100, 4)) + '%')
    
            comm_sql = 'SELECT imdata FROM tb_json WHERE iddata=' + str(i) + ';'
            cur.execute(comm_sql)
            len_row_json = len(str(cur.fetchall()[0]))  # JSON(B)长度
    
            df_tmp = pd.DataFrame([[i, len_row_json]], columns=['id', 'len_json'])
            df_counter = pd.concat([df_counter, df_tmp])
    
        conn.close()
    
        df_counter = df_counter.iloc[1:, :]
        df_counter.sort_values(by='len_json', inplace=True)
    
        print('>>' * 50)
        print('[INFO] 合并结束，使用序列化保存[最终]结果')
        time_start = datetime.datetime.now()
        f = open('./result/df_id_json_len.bits', 'wb')
        pickle.dump(obj=df_counter, file=f)
        f.close()
        time_end = datetime.datetime.now()
        print('[INFO] 序列化保存结果结束，用时：', (time_end - time_start).seconds, ' 秒\n')
    
    
    def json_by_id_only_full_row_test():
        # 如果数据库不存在，那么它将自动创建，最后将返回一个数据库对象
        print('>>' * 50)
        print('[INFO] Start connect database')
        conn = pg.connect(database="db_imdb",
                          user="postgres",
                          password="postgres",
                          host="localhost",
                          port="5432")
        cur = conn.cursor()
        print('[INFO] Connect database successfully')
    
        # 获取行数
        cur.execute("SELECT COUNT(*) FROM tb_json;")
        count_row = cur.fetchall()[0][0]
        print('行数：', count_row)
    
        # 用于统计的 DataFrame
        df_counter = pd.DataFrame([[0, 0]], columns=['len_row', 'use_time_ms'])
    
        # 执行查询并记录时间
        for i in range(1, 3000):
            print('[INFO] 正在测试第 ' + str(i) + '行 | ' + str(round(i / count_row * 100, 4)) + '%')
    
            comm_sql = 'SELECT imdata FROM tb_json WHERE iddata=' + str(i) + ';'
            start_time = datetime.datetime.now()
            cur.execute(comm_sql)
            end_time = datetime.datetime.now()
            use_time_ms = (end_time - start_time).microseconds
            # print('用时：', (end_time - start_time).microseconds, 'ms')
    
            row = cur.fetchall()[0]
            len_row_json = len(str(row))  # JSON(B)长度
    
            df_tmp = pd.DataFrame([[len_row_json, use_time_ms]], columns=['len_row', 'use_time_ms'])
            df_counter = pd.concat([df_counter, df_tmp])
    
        conn.close()
    
        df_counter = df_counter.iloc[1:, :]
        df_counter.sort_values(by='len_row', inplace=True)
    
        print('>>' * 50)
        print('[INFO] 合并结束，使用序列化保存[最终]结果')
        time_start = datetime.datetime.now()
        f = open('./result/json/res_id.bits', 'wb')
        pickle.dump(obj=df_counter, file=f)
        f.close()
        time_end = datetime.datetime.now()
        print('[INFO] 序列化保存结果结束，用时：', (time_end - time_start).seconds, ' 秒\n')
    
        # print(df_counter)
    
        """绘制结果"""
        plt.figure(figsize=(20, 10), dpi=100)
        plt.scatter(x=df_counter['len_row'].values,
                    y=df_counter['use_time_ms'].values)
        plt.title('Query by key `ID` in tb_json')
        plt.xlabel('Length of JSON')
        plt.ylabel('Query time (milliseconds)')
        plt.savefig('./result/json/res_id.png')
        # plt.show()
    
    
    def jsonb_by_id_only_full_row_test():
        # 如果数据库不存在，那么它将自动创建，最后将返回一个数据库对象
        print('>>' * 50)
        print('[INFO] Start connect database')
        conn = pg.connect(database="db_imdb",
                          user="postgres",
                          password="postgres",
                          host="localhost",
                          port="5432")
        cur = conn.cursor()
        print('[INFO] Connect database successfully')
    
        # 获取行数
        cur.execute("SELECT COUNT(*) FROM tb_jsonb;")
        count_row = cur.fetchall()[0][0]
        print('行数：', count_row)
    
        # 用于统计的 DataFrame
        df_counter = pd.DataFrame([[0, 0]], columns=['len_row', 'use_time_ms'])
    
        # 执行查询并记录时间
        for i in range(1, 3000):
            print('[INFO] 正在测试第 ' + str(i) + '行 | ' + str(round(i / count_row * 100, 4)) + '%')
            comm_sql = 'SELECT imdata FROM tb_jsonb WHERE iddata=' + str(i) + ';'
    
            start_time = datetime.datetime.now()
            cur.execute(comm_sql)
            end_time = datetime.datetime.now()
            use_time_ms = (end_time - start_time).microseconds
            # print('用时：', (end_time - start_time).microseconds, 'ms')
    
            row = cur.fetchall()[0]
            len_row_json = len(str(row))  # JSON(B)长度
    
            df_tmp = pd.DataFrame([[len_row_json, use_time_ms]], columns=['len_row', 'use_time_ms'])
            df_counter = pd.concat([df_counter, df_tmp])
    
        conn.close()
    
        df_counter = df_counter.iloc[1:, :]
        df_counter.sort_values(by='len_row', inplace=True)
    
        print('>>' * 50)
        print('[INFO] 合并结束，使用序列化保存[最终]结果')
        time_start = datetime.datetime.now()
        f = open('./result/jsonb/res_id.bits', 'wb')
        pickle.dump(obj=df_counter, file=f)
        f.close()
        time_end = datetime.datetime.now()
        print('[INFO] 序列化保存结果结束，用时：', (time_end - time_start).seconds, ' 秒\n')
    
        # print(df_counter)
    
        """绘制结果"""
        plt.figure(figsize=(20, 10), dpi=100)
        plt.scatter(x=df_counter['len_row'].values,
                    y=df_counter['use_time_ms'].values)
        plt.title('Query by key `ID` in tb_jsonb')
        plt.xlabel('Length of JSONB')
        plt.ylabel('Query time (milliseconds)')
        plt.savefig('./result/jsonb/res_id.png')
        # plt.show()
    
    
    def json_by_id_every_col_test():
        # 如果数据库不存在，那么它将自动创建，最后将返回一个数据库对象
        print('>>' * 50)
        print('[INFO] Start connect database')
        conn = pg.connect(database="db_imdb",
                          user="postgres",
                          password="postgres",
                          host="localhost",
                          port="5432")
        cur = conn.cursor()
        print('[INFO] Connect database successfully')
    
        # 获取行数
        cur.execute("SELECT COUNT(*) FROM tb_json;")
        count_row = cur.fetchall()[0][0]
        print('行数：', count_row)
    
        # 用于统计的 DataFrame
        df_counter = pd.DataFrame([[0, 0, 0, 0, 0, 0, 0]],
                                  columns=['len_row', 'full_ms', 'nconst_ms', 'name_ms', 'birthYear_ms', 'profession_ms', 'rols_ms'])
    
        # 执行查询并记录时间
        for i in range(1, count_row):
            print('[INFO] 正在测试第 ' + str(i) + '行 | ' + str(round(i / count_row * 100, 4)) + '%')
    
            # 整个 data 行所有字段
            comm_sql = 'SELECT imdata FROM tb_json WHERE iddata=' + str(i) + ';'
            start_time = datetime.datetime.now()
            cur.execute(comm_sql)
            end_time = datetime.datetime.now()
            full_use_time_ms = (end_time - start_time).microseconds
            row = cur.fetchall()[0]
            len_row_json = len(str(row))  # JSON(B)长度
    
            # 整个 data 行的字段 nconst
            comm_sql = "SELECT imdata->>'nconst' FROM tb_json WHERE iddata=" + str(i) + ';'
            start_time = datetime.datetime.now()
            cur.execute(comm_sql)
            end_time = datetime.datetime.now()
            nconst_use_time_ms = (end_time - start_time).microseconds
    
            # 整个 data 行的字段 name
            comm_sql = "SELECT imdata->>'name' FROM tb_json WHERE iddata=" + str(i) + ';'
            start_time = datetime.datetime.now()
            cur.execute(comm_sql)
            end_time = datetime.datetime.now()
            name_use_time_ms = (end_time - start_time).microseconds
    
            # 整个 data 行的字段 birthYear
            comm_sql = "SELECT imdata->>'birthYear' FROM tb_json WHERE iddata=" + str(i) + ';'
            start_time = datetime.datetime.now()
            cur.execute(comm_sql)
            end_time = datetime.datetime.now()
            birthYear_use_time_ms = (end_time - start_time).microseconds
    
            # 整个 data 行的字段 profession
            comm_sql = "SELECT imdata->>'profession' FROM tb_json WHERE iddata=" + str(i) + ';'
            start_time = datetime.datetime.now()
            cur.execute(comm_sql)
            end_time = datetime.datetime.now()
            profession_use_time_ms = (end_time - start_time).microseconds
    
            # 整个 data 行的字段 rols
            comm_sql = "SELECT imdata->>'rols' FROM tb_json WHERE iddata=" + str(i) + ';'
            start_time = datetime.datetime.now()
            cur.execute(comm_sql)
            end_time = datetime.datetime.now()
            rols_use_time_ms = (end_time - start_time).microseconds
    
            df_tmp = pd.DataFrame([[len_row_json, full_use_time_ms, nconst_use_time_ms, name_use_time_ms, birthYear_use_time_ms, profession_use_time_ms, rols_use_time_ms]],
                                  columns=['len_row', 'full_ms', 'nconst_ms', 'name_ms', 'birthYear_ms', 'profession_ms', 'rols_ms'])
            df_counter = pd.concat([df_counter, df_tmp])
    
        conn.close()
    
        df_counter = df_counter.iloc[1:, :]
        df_counter.sort_values(by='len_row', inplace=True)
    
        print('>>' * 50)
        print('[INFO] 合并结束，使用序列化保存[最终]结果')
        time_start = datetime.datetime.now()
        f = open('./result/json/res_id_ix_every_col.bits', 'wb')
        pickle.dump(obj=df_counter, file=f)
        f.close()
        time_end = datetime.datetime.now()
        print('[INFO] 序列化保存结果结束，用时：', (time_end - time_start).seconds, ' 秒\n')
    
        # print(df_counter)
    
        """绘制结果"""
        plt.figure(figsize=(20, 10), dpi=100)
        plt.scatter(x=df_counter['len_row'].values,
                    y=df_counter['full_ms'].values,
                    label='full row')
        plt.scatter(x=df_counter['len_row'].values,
                    y=df_counter['nconst_ms'].values,
                    label='nconst')
        plt.scatter(x=df_counter['len_row'].values,
                    y=df_counter['name_ms'].values,
                    label='name')
        plt.scatter(x=df_counter['len_row'].values,
                    y=df_counter['birthYear_ms'].values,
                    label='birthYear')
        plt.scatter(x=df_counter['len_row'].values,
                    y=df_counter['profession_ms'].values,
                    label='profession')
        plt.scatter(x=df_counter['len_row'].values,
                    y=df_counter['rols_ms'].values,
                    label='rols')
        plt.legend()
        plt.title('Query by key `ID` in tb_json')
        plt.xlabel('Length of JSON')
        plt.ylabel('Query time (milliseconds)')
        plt.savefig('./result/json/res_id_ix_every_col.png')
        # plt.show()
    
    
    def jsonb_by_id_every_col_test():
        # 如果数据库不存在，那么它将自动创建，最后将返回一个数据库对象
        print('>>' * 50)
        print('[INFO] Start connect database')
        conn = pg.connect(database="db_imdb",
                          user="postgres",
                          password="postgres",
                          host="localhost",
                          port="5432")
        cur = conn.cursor()
        print('[INFO] Connect database successfully')
    
        # 获取行数
        cur.execute("SELECT COUNT(*) FROM tb_jsonb;")
        count_row = cur.fetchall()[0][0]
        print('行数：', count_row)
    
        # 用于统计的 DataFrame
        df_counter = pd.DataFrame([[0, 0, 0, 0, 0, 0, 0]],
                                  columns=['len_row', 'full_ms', 'nconst_ms', 'name_ms', 'birthYear_ms', 'profession_ms', 'rols_ms'])
    
        # 执行查询并记录时间
        for i in range(1, count_row):
            print('[INFO] 正在测试第 ' + str(i) + '行 | ' + str(round(i / count_row * 100, 4)) + '%')
    
            # 整个 data 行所有字段
            comm_sql = 'SELECT imdata FROM tb_jsonb WHERE iddata=' + str(i) + ';'
            start_time = datetime.datetime.now()
            cur.execute(comm_sql)
            end_time = datetime.datetime.now()
            full_use_time_ms = (end_time - start_time).microseconds
            row = cur.fetchall()[0]
            len_row_jsonb = len(str(row))  # JSON(B)长度
    
            # 整个 data 行的字段 nconst
            comm_sql = "SELECT imdata->>'nconst' FROM tb_jsonb WHERE iddata=" + str(i) + ';'
            start_time = datetime.datetime.now()
            cur.execute(comm_sql)
            end_time = datetime.datetime.now()
            nconst_use_time_ms = (end_time - start_time).microseconds
    
            # 整个 data 行的字段 name
            comm_sql = "SELECT imdata->>'name' FROM tb_jsonb WHERE iddata=" + str(i) + ';'
            start_time = datetime.datetime.now()
            cur.execute(comm_sql)
            end_time = datetime.datetime.now()
            name_use_time_ms = (end_time - start_time).microseconds
    
            # 整个 data 行的字段 birthYear
            comm_sql = "SELECT imdata->>'birthYear' FROM tb_jsonb WHERE iddata=" + str(i) + ';'
            start_time = datetime.datetime.now()
            cur.execute(comm_sql)
            end_time = datetime.datetime.now()
            birthYear_use_time_ms = (end_time - start_time).microseconds
    
            # 整个 data 行的字段 profession
            comm_sql = "SELECT imdata->>'profession' FROM tb_jsonb WHERE iddata=" + str(i) + ';'
            start_time = datetime.datetime.now()
            cur.execute(comm_sql)
            end_time = datetime.datetime.now()
            profession_use_time_ms = (end_time - start_time).microseconds
    
            # 整个 data 行的字段 rols
            comm_sql = "SELECT imdata->>'rols' FROM tb_jsonb WHERE iddata=" + str(i) + ';'
            start_time = datetime.datetime.now()
            cur.execute(comm_sql)
            end_time = datetime.datetime.now()
            rols_use_time_ms = (end_time - start_time).microseconds
    
            df_tmp = pd.DataFrame([[len_row_jsonb, full_use_time_ms, nconst_use_time_ms, name_use_time_ms, birthYear_use_time_ms, profession_use_time_ms, rols_use_time_ms]],
                                  columns=['len_row', 'full_ms', 'nconst_ms', 'name_ms', 'birthYear_ms', 'profession_ms', 'rols_ms'])
            df_counter = pd.concat([df_counter, df_tmp])
    
        conn.close()
    
        df_counter = df_counter.iloc[1:, :]
        df_counter.sort_values(by='len_row', inplace=True)
    
        print('>>' * 50)
        print('[INFO] 合并结束，使用序列化保存[最终]结果')
        time_start = datetime.datetime.now()
        f = open('./result/jsonb/res_id_ix_every_col.bits', 'wb')
        pickle.dump(obj=df_counter, file=f)
        f.close()
        time_end = datetime.datetime.now()
        print('[INFO] 序列化保存结果结束，用时：', (time_end - time_start).seconds, ' 秒\n')
    
        # print(df_counter)
    
        """绘制结果"""
        plt.figure(figsize=(20, 10), dpi=100)
        plt.scatter(x=df_counter['len_row'].values,
                    y=df_counter['full_ms'].values,
                    label='full row')
        plt.scatter(x=df_counter['len_row'].values,
                    y=df_counter['nconst_ms'].values,
                    label='nconst')
        plt.scatter(x=df_counter['len_row'].values,
                    y=df_counter['name_ms'].values,
                    label='name')
        plt.scatter(x=df_counter['len_row'].values,
                    y=df_counter['birthYear_ms'].values,
                    label='birthYear')
        plt.scatter(x=df_counter['len_row'].values,
                    y=df_counter['profession_ms'].values,
                    label='profession')
        plt.scatter(x=df_counter['len_row'].values,
                    y=df_counter['rols_ms'].values,
                    label='rols')
        plt.legend()
        plt.title('Query by key `ID` in tb_jsonb')
        plt.xlabel('Length of JSONB')
        plt.ylabel('Query time (milliseconds)')
        plt.savefig('./result/jsonb/res_id_ix_every_col.png')
        # plt.show()
    
    
    def json_update_by_id_every_col_test():
        # 如果数据库不存在，那么它将自动创建，最后将返回一个数据库对象
        print('>>' * 50)
        print('[INFO] Start connect database')
        conn = pg.connect(database="db_imdb",
                          user="postgres",
                          password="postgres",
                          host="localhost",
                          port="5432")
        cur = conn.cursor()
        print('[INFO] Connect database successfully')
    
        # 获取行数
        cur.execute("SELECT COUNT(*) FROM tb_json;")
        count_row = cur.fetchall()[0][0]
        print('行数：', count_row)
    
        # 用于统计的 DataFrame
        df_counter = pd.DataFrame([[0, 0, 0, 0, 0]],
                                  columns=['len_row', 'nconst_ms', 'name_ms', 'birthYear_ms', 'rols_ms'])
    
        # 执行查询并记录时间
        for i in range(1, count_row):
            print('\n[INFO] 正在测试第 ' + str(i) + '行 | ' + str(round(i / count_row * 100, 4)) + '%')
    
            try:
                # 整个 data 行所有字段
                comm_sql = 'SELECT imdata FROM tb_json WHERE iddata=' + str(i) + ';'
                cur.execute(comm_sql)
                len_row_json = len(str(cur.fetchall()[0]))  # JSON(B)长度
    
                cur.execute('BEGIN;')
    
                print('\tBEGIN;')
    
                # 整个 data 行的字段 nconst
                comm_sql = "UPDATE tb_json SET imdata=jsonb_set(imdata::jsonb, '{nconst}', '\"tt0000009\"'::jsonb) WHERE iddata=" + str(i) + ';'
                start_time = datetime.datetime.now()
                cur.execute(comm_sql)
                end_time = datetime.datetime.now()
                nconst_use_time_ms = (end_time - start_time).microseconds
                print('\tnconst 测试结束, 用时：', nconst_use_time_ms, ' ms')
    
                # 整个 data 行的字段 name
                comm_sql = "UPDATE tb_json SET imdata=jsonb_set(imdata::jsonb, '{name}', '\"tt_name\"'::jsonb) WHERE iddata=" + str(i) + ';'
                start_time = datetime.datetime.now()
                cur.execute(comm_sql)
                end_time = datetime.datetime.now()
                name_use_time_ms = (end_time - start_time).microseconds
                print('\tname 测试结束, 用时：', name_use_time_ms, ' ms')
    
                # 整个 data 行的字段 birthYear
                comm_sql = "UPDATE tb_json SET imdata=jsonb_set(imdata::jsonb, '{birthYear}', '\"2222\"'::jsonb) WHERE iddata=" + str(i) + ';'
                start_time = datetime.datetime.now()
                cur.execute(comm_sql)
                end_time = datetime.datetime.now()
                birthYear_use_time_ms = (end_time - start_time).microseconds
                print('\tbirthYear 测试结束, 用时：', birthYear_use_time_ms, ' ms')
    
                # 整个 data 行的字段 rols
                comm_sql = 'UPDATE tb_json SET imdata=jsonb_set(imdata::jsonb, \'{rols}\', \'[{"year": 2000, "title": "t_title", "series name": "t_series", "character name": "t_character_name"}]\'::jsonb) WHERE iddata=' + str(i) + ';'
                start_time = datetime.datetime.now()
                cur.execute(comm_sql)
                end_time = datetime.datetime.now()
                rols_use_time_ms = (end_time - start_time).microseconds
                print('\trols 测试结束, 用时：', rols_use_time_ms, ' ms')
    
            except:
                cur.execute('ROLLBACK;')
                continue
    
            cur.execute('ROLLBACK;')
            df_tmp = pd.DataFrame([[len_row_json, nconst_use_time_ms, name_use_time_ms, birthYear_use_time_ms, rols_use_time_ms]],
                                  columns=['len_row', 'nconst_ms', 'name_ms', 'birthYear_ms', 'rols_ms'])
            df_counter = pd.concat([df_counter, df_tmp])
    
        conn.close()
    
        df_counter = df_counter.iloc[1:, :]
        df_counter.sort_values(by='len_row', inplace=True)
    
        print('>>' * 50)
        print('[INFO] 合并结束，使用序列化保存[最终]结果')
        time_start = datetime.datetime.now()
        f = open('./result/json/res_update_id_ix_every_col.bits', 'wb')
        pickle.dump(obj=df_counter, file=f)
        f.close()
        time_end = datetime.datetime.now()
        print('[INFO] 序列化保存结果结束，用时：', (time_end - time_start).seconds, ' 秒\n')
    
        # print(df_counter)
    
        """绘制结果"""
        plt.figure(figsize=(20, 10), dpi=100)
        plt.scatter(x=df_counter['len_row'].values,
                    y=df_counter['nconst_ms'].values,
                    label='nconst')
        plt.scatter(x=df_counter['len_row'].values,
                    y=df_counter['name_ms'].values,
                    label='name')
        plt.scatter(x=df_counter['len_row'].values,
                    y=df_counter['birthYear_ms'].values,
                    label='birthYear')
        plt.scatter(x=df_counter['len_row'].values,
                    y=df_counter['rols_ms'].values,
                    label='rols')
        plt.legend()
        plt.title('Test UPDATE, query by key `ID` in tb_json')
        plt.xlabel('Length of JSON')
        plt.ylabel('Query time (milliseconds)')
        plt.savefig('./result/json/res_update_id_ix_every_col.png')
        # plt.show()
    
    
    def jsonb_update_by_id_every_col_test():
        # 如果数据库不存在，那么它将自动创建，最后将返回一个数据库对象
        print('>>' * 50)
        print('[INFO] Start connect database')
        conn = pg.connect(database="db_imdb",
                          user="postgres",
                          password="postgres",
                          host="localhost",
                          port="5432")
        cur = conn.cursor()
        print('[INFO] Connect database successfully')
    
        # 获取行数
        cur.execute("SELECT COUNT(*) FROM tb_jsonb;")
        count_row = cur.fetchall()[0][0]
        print('行数：', count_row)
    
        # 用于统计的 DataFrame
        df_counter = pd.DataFrame([[0, 0, 0, 0, 0]],
                                  columns=['len_row', 'nconst_ms', 'name_ms', 'birthYear_ms', 'rols_ms'])
    
        # 执行查询并记录时间
        for i in range(1, count_row):
            print('\n[INFO] 正在测试第 ' + str(i) + '行 | ' + str(round(i / count_row * 100, 4)) + '%')
    
            try:
                # 整个 data 行所有字段
                comm_sql = 'SELECT imdata FROM tb_jsonb WHERE iddata=' + str(i) + ';'
                cur.execute(comm_sql)
                len_row_jsonb = len(str(cur.fetchall()[0]))  # JSON(B)长度
    
                cur.execute('BEGIN;')
    
                print('\tBEGIN;')
    
                # 整个 data 行的字段 nconst
                comm_sql = "UPDATE tb_jsonb SET imdata=jsonb_set(imdata::jsonb, '{nconst}', '\"tt0000009\"'::jsonb) WHERE iddata=" + str(i) + ';'
                # comm_sql = "UPDATE tb_jsonb SET imdata=jsonb_set(imdata::jsonb, \'{nconst}\', \'\"tt0000009\"\'::jsonb) WHERE iddata=" + str(i) + ';'
                # print(comm_sql)
                start_time = datetime.datetime.now()
                cur.execute(comm_sql)
                end_time = datetime.datetime.now()
                nconst_use_time_ms = (end_time - start_time).microseconds
                print('\tnconst 测试结束, 用时：', nconst_use_time_ms, ' ms')
    
                # 整个 data 行的字段 name
                comm_sql = "UPDATE tb_jsonb SET imdata=jsonb_set(imdata::jsonb, '{name}', '\"tt_name\"'::jsonb) WHERE iddata=" + str(i) + ';'
                start_time = datetime.datetime.now()
                cur.execute(comm_sql)
                end_time = datetime.datetime.now()
                name_use_time_ms = (end_time - start_time).microseconds
                print('\tname 测试结束, 用时：', name_use_time_ms, ' ms')
    
                # 整个 data 行的字段 birthYear
                comm_sql = "UPDATE tb_jsonb SET imdata=jsonb_set(imdata::jsonb, '{birthYear}', '\"2222\"'::jsonb) WHERE iddata=" + str(i) + ';'
                start_time = datetime.datetime.now()
                cur.execute(comm_sql)
                end_time = datetime.datetime.now()
                birthYear_use_time_ms = (end_time - start_time).microseconds
                print('\tbirthYear 测试结束, 用时：', birthYear_use_time_ms, ' ms')
    
                # 整个 data 行的字段 rols
                comm_sql = 'UPDATE tb_jsonb SET imdata=jsonb_set(imdata::jsonb, \'{rols}\', \'[{"year": 2000, "title": "t_title", "series name": "t_series", "character name": "t_character_name"}]\'::jsonb) WHERE iddata=' + str(i) + ';'
                start_time = datetime.datetime.now()
                cur.execute(comm_sql)
                end_time = datetime.datetime.now()
                rols_use_time_ms = (end_time - start_time).microseconds
                print('\trols 测试结束, 用时：', rols_use_time_ms, ' ms')
    
            except:
                cur.execute('ROLLBACK;')
                continue
    
            cur.execute('ROLLBACK;')
            df_tmp = pd.DataFrame([[len_row_jsonb, nconst_use_time_ms, name_use_time_ms, birthYear_use_time_ms, rols_use_time_ms]],
                                  columns=['len_row', 'nconst_ms', 'name_ms', 'birthYear_ms', 'rols_ms'])
            df_counter = pd.concat([df_counter, df_tmp])
    
        conn.close()
    
        df_counter = df_counter.iloc[1:, :]
        df_counter.sort_values(by='len_row', inplace=True)
    
        print('>>' * 50)
        print('[INFO] 合并结束，使用序列化保存[最终]结果')
        time_start = datetime.datetime.now()
        f = open('./result/jsonb/res_update_id_ix_every_col.bits', 'wb')
        pickle.dump(obj=df_counter, file=f)
        f.close()
        time_end = datetime.datetime.now()
        print('[INFO] 序列化保存结果结束，用时：', (time_end - time_start).seconds, ' 秒\n')
    
        # print(df_counter)
    
        """绘制结果"""
        plt.figure(figsize=(20, 10), dpi=100)
        plt.scatter(x=df_counter['len_row'].values,
                    y=df_counter['nconst_ms'].values,
                    label='nconst')
        plt.scatter(x=df_counter['len_row'].values,
                    y=df_counter['name_ms'].values,
                    label='name')
        plt.scatter(x=df_counter['len_row'].values,
                    y=df_counter['birthYear_ms'].values,
                    label='birthYear')
        plt.scatter(x=df_counter['len_row'].values,
                    y=df_counter['rols_ms'].values,
                    label='rols')
        plt.legend()
        plt.title('Test UPDATE, query by key `ID` in tb_jsonb')
        plt.xlabel('Length of JSONB')
        plt.ylabel('Query time (milliseconds)')
        plt.savefig('./result/jsonb/res_update_id_ix_every_col.png')
        # plt.show()
    
    
    def json_where_name_test():
        print('>>' * 50)
        print('[INFO] 读取序列化数据')
        time_start = datetime.datetime.now()
        f = open('/Users/fox/Library/CloudStorage/OneDrive-PetertheGreatSt.PetersburgPolytechnicalUniversity/СПБПУ/3 '
                 'курс/6 семестр/СУБД/资料/DataSet/result_ALL/dump_ALL.bits', 'rb')
        arr_name = pickle.load(file=f)
        f.close()
        arr_name = arr_name['name'].values
        time_end = datetime.datetime.now()
        print('[INFO] 读取序列化数据结束，用时：', (time_end - time_start).seconds, ' 秒\n')
    
        print('>>' * 50)
        print('[INFO] Start connect database')
        conn = pg.connect(database="db_imdb",
                          user="postgres",
                          password="postgres",
                          host="localhost",
                          port="5432")
        cur = conn.cursor()
        print('[INFO] Connect database successfully')
    
        i = 0
        count_row = len(arr_name)
        # 用于统计的 DataFrame
        df_counter = pd.DataFrame([[0, 0]], columns=['len_row', 'use_time_ms'])
        # TODO 取消分割
        for name in arr_name[244:250]:
            i += 1
            print('[INFO] 正在测试第 ' + str(i) + ' 行 | ' + str(round(i / count_row * 100, 4)) + '% | name = ', name)
    
            comm_sql = "SELECT imdata FROM tb_json WHERE imdata::json->> 'name' = '" + name + "';"
            start_time = datetime.datetime.now()
            try:
                cur.execute(comm_sql)
            except:
                print('[INFO] 第 ' + str(i) + ' 行取消 | name = ', name)
                continue
            end_time = datetime.datetime.now()
            use_time_ms = (end_time - start_time).microseconds
            # print('用时：', (end_time - start_time).microseconds, 'ms')
    
            row = cur.fetchall()[0]
            len_row_json = len(str(row))  # JSON(B)长度
            df_tmp = pd.DataFrame([[len_row_json, use_time_ms]], columns=['len_row', 'use_time_ms'])
            df_counter = pd.concat([df_counter, df_tmp])
    
        conn.close()
    
        df_counter = df_counter.iloc[1:, :]
        df_counter.sort_values(by='len_row', inplace=True)
    
        print('>>' * 50)
        print('[INFO] 合并结束，使用序列化保存[最终]结果')
        time_start = datetime.datetime.now()
        f = open('./result/json/res_name.bits', 'wb')
        pickle.dump(obj=df_counter, file=f)
        f.close()
        time_end = datetime.datetime.now()
        print('[INFO] 序列化保存结果结束，用时：', (time_end - time_start).seconds, ' 秒\n')
    
        # print(df_counter)
    
        """绘制结果"""
        plt.figure(figsize=(20, 10), dpi=100)
        plt.scatter(x=df_counter['len_row'].values,
                    y=df_counter['use_time_ms'].values)
        plt.title('Query by key `name` in tb_json')
        plt.xlabel('Length of JSON')
        plt.ylabel('Query time (milliseconds)')
        plt.savefig('./result/json/res_name.png')
        # plt.show()  # TODO 注释掉
    
    
    def jsonb_where_name_test():
        print('>>' * 50)
        print('[INFO] 读取序列化数据')
        time_start = datetime.datetime.now()
        f = open('/Users/fox/Library/CloudStorage/OneDrive-PetertheGreatSt.PetersburgPolytechnicalUniversity/СПБПУ/3 '
                 'курс/6 семестр/СУБД/资料/DataSet/result_ALL/dump_ALL.bits', 'rb')
        arr_name = pickle.load(file=f)
        f.close()
        arr_name = arr_name['name'].values
        time_end = datetime.datetime.now()
        print('[INFO] 读取序列化数据结束，用时：', (time_end - time_start).seconds, ' 秒\n')
    
        print('>>' * 50)
        print('[INFO] Start connect database')
        conn = pg.connect(database="db_imdb",
                          user="postgres",
                          password="postgres",
                          host="localhost",
                          port="5432")
        cur = conn.cursor()
        print('[INFO] Connect database successfully')
    
        i = 0
        count_row = len(arr_name)
        # 用于统计的 DataFrame
        df_counter = pd.DataFrame([[0, 0]], columns=['len_row', 'use_time_ms'])
        # TODO 取消分割
        for name in arr_name[:3000]:
            i += 1
            print('[INFO] 正在测试第 ' + str(i) + ' 行 | ' + str(round(i / count_row * 100, 4)) + '% | name = ', name)
    
            comm_sql = "SELECT imdata FROM tb_jsonb WHERE imdata::jsonb->> 'name' = '" + name + "';"
            start_time = datetime.datetime.now()
            try:
                cur.execute(comm_sql)
            except:
                print('[INFO] 第 ' + str(i) + ' 行取消 | name = ', name)
                continue
            end_time = datetime.datetime.now()
            use_time_ms = (end_time - start_time).microseconds
            # print('用时：', (end_time - start_time).microseconds, 'ms')
    
            row = cur.fetchall()[0]
            len_row_json = len(str(row))  # JSON(B)长度
            df_tmp = pd.DataFrame([[len_row_json, use_time_ms]], columns=['len_row', 'use_time_ms'])
            df_counter = pd.concat([df_counter, df_tmp])
    
            # print(rows)  # TODO 注释掉
            # print(len(str(rows)))  # TODO 注释掉
    
        conn.close()
    
        df_counter = df_counter.iloc[1:, :]
        df_counter.sort_values(by='len_row', inplace=True)
    
        print('>>' * 50)
        print('[INFO] 合并结束，使用序列化保存[最终]结果')
        time_start = datetime.datetime.now()
        f = open('./result/jsonb/res_name.bits', 'wb')
        pickle.dump(obj=df_counter, file=f)
        f.close()
        time_end = datetime.datetime.now()
        print('[INFO] 序列化保存结果结束，用时：', (time_end - time_start).seconds, ' 秒\n')
    
        # print(df_counter)
    
        """绘制结果"""
        plt.figure(figsize=(20, 10), dpi=100)
        plt.scatter(x=df_counter['len_row'].values,
                    y=df_counter['use_time_ms'].values)
        plt.title('Query by key `name` in tb_jsonb')
        plt.xlabel('Length of JSONB')
        plt.ylabel('Query time (milliseconds)')
        plt.savefig('./result/jsonb/res_name.png')
        # plt.show()  # TODO 注释掉
    
    
    def json_by_where_nconst_only_full_row_test():
        print('>>' * 50)
        print('[INFO] 读取序列化数据')
        time_start = datetime.datetime.now()
        f = open('/Users/fox/Library/CloudStorage/OneDrive-PetertheGreatSt.PetersburgPolytechnicalUniversity/СПБПУ/3 '
                 'курс/6 семестр/СУБД/资料/DataSet/result_ALL/dump_ALL.bits', 'rb')
        arr_nconst = pickle.load(file=f)
        f.close()
        arr_nconst = arr_nconst['nconst'].values
        time_end = datetime.datetime.now()
        print('[INFO] 读取序列化数据结束，用时：', (time_end - time_start).seconds, ' 秒\n')
    
        print('>>' * 50)
        print('[INFO] Start connect database')
        conn = pg.connect(database="db_imdb",
                          user="postgres",
                          password="postgres",
                          host="localhost",
                          port="5432")
        cur = conn.cursor()
        print('[INFO] Connect database successfully')
    
        i = 0
        count_row = len(arr_nconst)
        # 用于统计的 DataFrame
        df_counter = pd.DataFrame([[0, 0]], columns=['len_row', 'use_time_ms'])
        # TODO 取消分割
        for nconst in arr_nconst[:1000]:
            i += 1
            print('[INFO] 正在测试第 ' + str(i) + ' 行 | ' + str(round(i / count_row * 100, 4)) + '% | nconst = ', nconst)
    
            comm_sql = "SELECT imdata FROM tb_json WHERE imdata::json->> 'nconst' = '" + nconst + "';"
            start_time = datetime.datetime.now()
            try:
                cur.execute(comm_sql)
            except:
                print('[INFO] 第 ' + str(i) + ' 行取消 | nconst = ', nconst)
                continue
            end_time = datetime.datetime.now()
            use_time_ms = (end_time - start_time).microseconds
            print('\t用时：', (end_time - start_time).seconds, 's')
    
            row = cur.fetchall()[0]
            len_row_json = len(str(row))  # JSON(B)长度
            df_tmp = pd.DataFrame([[len_row_json, use_time_ms]], columns=['len_row', 'use_time_ms'])
            df_counter = pd.concat([df_counter, df_tmp])
    
        conn.close()
    
        df_counter = df_counter.iloc[1:, :]
        df_counter.sort_values(by='len_row', inplace=True)
    
        print('>>' * 50)
        print('[INFO] 合并结束，使用序列化保存[最终]结果')
        time_start = datetime.datetime.now()
        f = open('./result/json/res_nconst.bits', 'wb')
        pickle.dump(obj=df_counter, file=f)
        f.close()
        time_end = datetime.datetime.now()
        print('[INFO] 序列化保存结果结束，用时：', (time_end - time_start).seconds, ' 秒\n')
    
        # print(df_counter)
    
        """绘制结果"""
        plt.figure(figsize=(20, 10), dpi=100)
        plt.scatter(x=df_counter['len_row'].values,
                    y=df_counter['use_time_ms'].values)
        plt.title('Query by key `nconst` in tb_json')
        plt.xlabel('Length of JSON')
        plt.ylabel('Query time (milliseconds)')
        plt.savefig('./result/json/res_nconst.png')
        # plt.show()  # TODO 注释掉
    
    
    def jsonb_by_where_nconst_only_full_row_test():
        print('>>' * 50)
        print('[INFO] 读取序列化数据')
        time_start = datetime.datetime.now()
        f = open('/Users/fox/Library/CloudStorage/OneDrive-PetertheGreatSt.PetersburgPolytechnicalUniversity/СПБПУ/3 '
                 'курс/6 семестр/СУБД/资料/DataSet/result_ALL/dump_ALL.bits', 'rb')
        arr_nconst = pickle.load(file=f)
        f.close()
        arr_nconst = arr_nconst['nconst'].values
        time_end = datetime.datetime.now()
        print('[INFO] 读取序列化数据结束，用时：', (time_end - time_start).seconds, ' 秒\n')
    
        print('>>' * 50)
        print('[INFO] Start connect database')
        conn = pg.connect(database="db_imdb",
                          user="postgres",
                          password="postgres",
                          host="localhost",
                          port="5432")
        cur = conn.cursor()
        print('[INFO] Connect database successfully')
    
        i = 0
        count_row = len(arr_nconst)
        # 用于统计的 DataFrame
        df_counter = pd.DataFrame([[0, 0]], columns=['len_row', 'use_time_ms'])
        # TODO 取消分割
        for nconst in arr_nconst[:3000]:
            i += 1
            print('\n[INFO] 正在测试第 ' + str(i) + ' 行 | ' + str(round(i / count_row * 100, 4)) + '% | nconst = ', nconst)
    
            comm_sql = "SELECT imdata FROM tb_jsonb WHERE imdata::jsonb->> 'nconst' = '" + nconst + "';"
            start_time = datetime.datetime.now()
            try:
                cur.execute(comm_sql)
            except:
                print('[INFO] 第 ' + str(i) + ' 行取消 | nconst = ', nconst)
                continue
            end_time = datetime.datetime.now()
            use_time_ms = (end_time - start_time).microseconds
            print('\t用时：', (end_time - start_time).seconds, 's')
    
            row = cur.fetchall()[0]
            len_row_json = len(str(row))  # JSON(B)长度
            df_tmp = pd.DataFrame([[len_row_json, use_time_ms]], columns=['len_row', 'use_time_ms'])
            df_counter = pd.concat([df_counter, df_tmp])
    
        conn.close()
    
        df_counter = df_counter.iloc[1:, :]
        df_counter.sort_values(by='len_row', inplace=True)
    
        print('>>' * 50)
        print('[INFO] 合并结束，使用序列化保存[最终]结果')
        time_start = datetime.datetime.now()
        f = open('./result/jsonb/res_nconst.bits', 'wb')
        pickle.dump(obj=df_counter, file=f)
        f.close()
        time_end = datetime.datetime.now()
        print('[INFO] 序列化保存结果结束，用时：', (time_end - time_start).seconds, ' 秒\n')
    
        # print(df_counter)
    
        """绘制结果"""
        plt.figure(figsize=(20, 10), dpi=100)
        plt.scatter(x=df_counter['len_row'].values,
                    y=df_counter['use_time_ms'].values)
        plt.title('Query by key `nconst` in tb_jsonb')
        plt.xlabel('Length of JSONB')
        plt.ylabel('Query time (milliseconds)')
        plt.savefig('./result/jsonb/res_nconst.png')
        # plt.show()  # TODO 注释掉
    
    
    def json_by_where_nconst_every_col_test():
        print('>>' * 50)
        print('[INFO] 读取序列化数据')
        time_start = datetime.datetime.now()
        f = open('/Users/fox/Library/CloudStorage/OneDrive-PetertheGreatSt.PetersburgPolytechnicalUniversity/СПБПУ/3 '
                 'курс/6 семестр/СУБД/资料/DataSet/result_ALL/dump_ALL.bits', 'rb')
        arr_nconst = pickle.load(file=f)
        f.close()
        arr_nconst = arr_nconst['nconst'].values
        time_end = datetime.datetime.now()
        print('[INFO] 读取序列化数据结束，用时：', (time_end - time_start).seconds, ' 秒\n')
    
        print('>>' * 50)
        print('[INFO] Start connect database')
        conn = pg.connect(database="db_imdb",
                          user="postgres",
                          password="postgres",
                          host="localhost",
                          port="5432")
        cur = conn.cursor()
        print('[INFO] Connect database successfully')
    
        i = 0
        count_row = len(arr_nconst)
        # 用于统计的 DataFrame
        df_counter = pd.DataFrame([[0, 0, 0, 0, 0, 0, 0]],
                                  columns=['len_row', 'full_ms', 'nconst_ms', 'name_ms', 'birthYear_ms', 'profession_ms',
                                           'rols_ms'])
        # TODO 取消分割
        # for nconst in arr_nconst[:2000]:
        for nconst in arr_nconst[:10]:
            i += 1
            print('\n[INFO] 正在测试第 ' + str(i) + ' 行 | ' + str(round(i / count_row * 100, 4)) + '% | nconst = ', nconst)
    
            # 整个 data 行所有字段
            comm_sql = "SELECT imdata FROM tb_json WHERE imdata::json->>'nconst' = '" + nconst + "';"
            start_time = datetime.datetime.now()
            try:
                cur.execute(comm_sql)
            except:
                print('[INFO] 第 ' + str(i) + ' 行取消 | nconst = ', nconst)
                continue
            end_time = datetime.datetime.now()
            full_use_time_ms = (end_time - start_time).microseconds
            row = cur.fetchall()[0]
            len_row_json = len(str(row))  # JSON(B)长度
            print('\tfull row 用时：', (end_time - start_time).seconds, 's')
    
            # 整个 data 行的字段 nconst
            comm_sql = "SELECT imdata->>'nconst' FROM tb_json WHERE imdata::json->>'nconst' = '" + nconst + "';"
            start_time = datetime.datetime.now()
            cur.execute(comm_sql)
            end_time = datetime.datetime.now()
            nconst_use_time_ms = (end_time - start_time).microseconds
            print('\tnconst 用时：', (end_time - start_time).seconds, 's')
    
    
    
            # 整个 data 行的字段 name
            comm_sql = "SELECT imdata->>'name' FROM tb_json WHERE imdata::json->>'nconst' = '" + nconst + "';"
            start_time = datetime.datetime.now()
            cur.execute(comm_sql)
            end_time = datetime.datetime.now()
            name_use_time_ms = (end_time - start_time).microseconds
            print('\tname 用时：', (end_time - start_time).seconds, 's')
    
            # 整个 data 行的字段 birthYear
            comm_sql = "SELECT imdata->>'birthYear' FROM tb_json WHERE imdata::json->>'nconst' = '" + nconst + "';"
            start_time = datetime.datetime.now()
            cur.execute(comm_sql)
            end_time = datetime.datetime.now()
            birthYear_use_time_ms = (end_time - start_time).microseconds
            print('\tbirthYear 用时：', (end_time - start_time).seconds, 's')
    
            # 整个 data 行的字段 profession
            comm_sql = "SELECT imdata->>'profession' FROM tb_json WHERE imdata::json->>'nconst' = '" + nconst + "';"
            start_time = datetime.datetime.now()
            cur.execute(comm_sql)
            end_time = datetime.datetime.now()
            profession_use_time_ms = (end_time - start_time).microseconds
            print('\tprofession 用时：', (end_time - start_time).seconds, 's')
    
            # 整个 data 行的字段 rols
            comm_sql = "SELECT imdata->>'rols' FROM tb_json WHERE imdata::json->>'nconst' = '" + nconst + "';"
            start_time = datetime.datetime.now()
            cur.execute(comm_sql)
            end_time = datetime.datetime.now()
            rols_use_time_ms = (end_time - start_time).microseconds
            print('\trols 用时：', (end_time - start_time).seconds, 's')
    
    
            df_tmp = pd.DataFrame([[len_row_json, full_use_time_ms, nconst_use_time_ms, name_use_time_ms, birthYear_use_time_ms, profession_use_time_ms, rols_use_time_ms]],
                                  columns=['len_row', 'full_ms', 'nconst_ms', 'name_ms', 'birthYear_ms', 'profession_ms', 'rols_ms'])
            df_counter = pd.concat([df_counter, df_tmp])
    
        conn.close()
    
        df_counter = df_counter.iloc[1:, :]
        df_counter.sort_values(by='len_row', inplace=True)
    
        print('>>' * 50)
        print('[INFO] 合并结束，使用序列化保存[最终]结果')
        time_start = datetime.datetime.now()
        f = open('./result/json/res_by_nconst_all_col.bits', 'wb')
        pickle.dump(obj=df_counter, file=f)
        f.close()
        time_end = datetime.datetime.now()
        print('[INFO] 序列化保存结果结束，用时：', (time_end - time_start).seconds, ' 秒\n')
    
        # print(df_counter)
    
        """绘制结果"""
        plt.figure(figsize=(20, 10), dpi=100)
        plt.scatter(x=df_counter['len_row'].values,
                    y=df_counter['full_ms'].values,
                    label='full row')
        plt.scatter(x=df_counter['len_row'].values,
                    y=df_counter['nconst_ms'].values,
                    label='nconst')
        plt.scatter(x=df_counter['len_row'].values,
                    y=df_counter['name_ms'].values,
                    label='name')
        plt.scatter(x=df_counter['len_row'].values,
                    y=df_counter['birthYear_ms'].values,
                    label='birthYear')
        plt.scatter(x=df_counter['len_row'].values,
                    y=df_counter['profession_ms'].values,
                    label='profession')
        plt.scatter(x=df_counter['len_row'].values,
                    y=df_counter['rols_ms'].values,
                    label='rols')
        plt.legend()
        plt.title('Query by key `nconst` in tb_json')
        plt.xlabel('Length of JSON')
        plt.ylabel('Query time (milliseconds)')
        plt.savefig('./result/json/res_by_nconst_all_col.png')
        # plt.show()
    
    
    def jsonb_by_where_nconst_every_col_test():
        print('>>' * 50)
        print('[INFO] 读取序列化数据')
        time_start = datetime.datetime.now()
        f = open('/Users/fox/Library/CloudStorage/OneDrive-PetertheGreatSt.PetersburgPolytechnicalUniversity/СПБПУ/3 '
                 'курс/6 семестр/СУБД/资料/DataSet/result_ALL/dump_ALL.bits', 'rb')
        arr_nconst = pickle.load(file=f)
        f.close()
        arr_nconst = arr_nconst['nconst'].values
        time_end = datetime.datetime.now()
        print('[INFO] 读取序列化数据结束，用时：', (time_end - time_start).seconds, ' 秒\n')
    
        print('>>' * 50)
        print('[INFO] Start connect database')
        conn = pg.connect(database="db_imdb",
                          user="postgres",
                          password="postgres",
                          host="localhost",
                          port="5432")
        cur = conn.cursor()
        print('[INFO] Connect database successfully')
    
        i = 0
        count_row = len(arr_nconst)
        # 用于统计的 DataFrame
        df_counter = pd.DataFrame([[0, 0, 0, 0, 0, 0, 0]],
                                  columns=['len_row', 'full_ms', 'nconst_ms', 'name_ms', 'birthYear_ms', 'profession_ms',
                                           'rols_ms'])
        # TODO 取消分割
        # for nconst in arr_nconst[:1000]:
        for nconst in arr_nconst[:2500]:
            i += 1
            print('[INFO] 正在测试第 ' + str(i) + ' 行 | ' + str(round(i / 2500 * 100, 4)) + '% | nconst = ', nconst)
    
            # 整个 data 行所有字段
            comm_sql = "SELECT imdata FROM tb_jsonb WHERE imdata::jsonb->>'nconst' = '" + nconst + "';"
            start_time = datetime.datetime.now()
            try:
                cur.execute(comm_sql)
            except:
                print('[INFO] 第 ' + str(i) + ' 行取消 | nconst = ', nconst)
                continue
            end_time = datetime.datetime.now()
            full_use_time_ms = (end_time - start_time).microseconds
            row = cur.fetchall()[0]
            len_row_jsonb = len(str(row))  # JSON(B)长度
            print('\tfull row 用时：', (end_time - start_time).seconds, 's')
    
            # 整个 data 行的字段 nconst
            comm_sql = "SELECT imdata->>'nconst' FROM tb_jsonb WHERE imdata::jsonb->>'nconst' = '" + nconst + "';"
            start_time = datetime.datetime.now()
            cur.execute(comm_sql)
            end_time = datetime.datetime.now()
            nconst_use_time_ms = (end_time - start_time).microseconds
            print('\tnconst 用时：', (end_time - start_time).seconds, 's')
    
    
            # 整个 data 行的字段 name
            comm_sql = "SELECT imdata->>'name' FROM tb_jsonb WHERE imdata::jsonb->>'nconst' = '" + nconst + "';"
            start_time = datetime.datetime.now()
            cur.execute(comm_sql)
            end_time = datetime.datetime.now()
            name_use_time_ms = (end_time - start_time).microseconds
            print('\tname 用时：', (end_time - start_time).seconds, 's')
    
            # 整个 data 行的字段 birthYear
            comm_sql = "SELECT imdata->>'birthYear' FROM tb_jsonb WHERE imdata::jsonb->>'nconst' = '" + nconst + "';"
            start_time = datetime.datetime.now()
            cur.execute(comm_sql)
            end_time = datetime.datetime.now()
            birthYear_use_time_ms = (end_time - start_time).microseconds
            print('\tbirthYear 用时：', (end_time - start_time).seconds, 's')
    
            # 整个 data 行的字段 profession
            comm_sql = "SELECT imdata->>'profession' FROM tb_jsonb WHERE imdata::jsonb->>'nconst' = '" + nconst + "';"
            start_time = datetime.datetime.now()
            cur.execute(comm_sql)
            end_time = datetime.datetime.now()
            profession_use_time_ms = (end_time - start_time).microseconds
            print('\tprofession 用时：', (end_time - start_time).seconds, 's')
    
            # 整个 data 行的字段 rols
            comm_sql = "SELECT imdata->>'rols' FROM tb_jsonb WHERE imdata::jsonb->>'nconst' = '" + nconst + "';"
            start_time = datetime.datetime.now()
            cur.execute(comm_sql)
            end_time = datetime.datetime.now()
            rols_use_time_ms = (end_time - start_time).microseconds
            print('\trols 用时：', (end_time - start_time).seconds, 's')
    
    
            df_tmp = pd.DataFrame([[len_row_jsonb, full_use_time_ms, nconst_use_time_ms, name_use_time_ms, birthYear_use_time_ms, profession_use_time_ms, rols_use_time_ms]],
                                  columns=['len_row', 'full_ms', 'nconst_ms', 'name_ms', 'birthYear_ms', 'profession_ms', 'rols_ms'])
            df_counter = pd.concat([df_counter, df_tmp])
    
        conn.close()
    
        df_counter = df_counter.iloc[1:, :]
        df_counter.sort_values(by='len_row', inplace=True)
    
        print('>>' * 50)
        print('[INFO] 合并结束，使用序列化保存[最终]结果')
        time_start = datetime.datetime.now()
        f = open('./result/jsonb/res_by_nconst_all_col.bits', 'wb')
        pickle.dump(obj=df_counter, file=f)
        f.close()
        time_end = datetime.datetime.now()
        print('[INFO] 序列化保存结果结束，用时：', (time_end - time_start).seconds, ' 秒\n')
    
        # print(df_counter)
    
        """绘制结果"""
        plt.figure(figsize=(20, 10), dpi=100)
        plt.scatter(x=df_counter['len_row'].values,
                    y=df_counter['full_ms'].values,
                    label='full row')
        plt.scatter(x=df_counter['len_row'].values,
                    y=df_counter['nconst_ms'].values,
                    label='nconst')
        plt.scatter(x=df_counter['len_row'].values,
                    y=df_counter['name_ms'].values,
                    label='name')
        plt.scatter(x=df_counter['len_row'].values,
                    y=df_counter['birthYear_ms'].values,
                    label='birthYear')
        plt.scatter(x=df_counter['len_row'].values,
                    y=df_counter['profession_ms'].values,
                    label='profession')
        plt.scatter(x=df_counter['len_row'].values,
                    y=df_counter['rols_ms'].values,
                    label='rols')
        plt.legend()
        plt.title('Query by key `nconst` in tb_jsonb')
        plt.xlabel('Length of JSONB')
        plt.ylabel('Query time (milliseconds)')
        plt.savefig('./result/jsonb/res_by_nconst_all_col.png')
        # plt.show()
    
    
    if __name__ == '__main__':
        # get_id_len_json_df()
    
        json_by_id_every_col_test()
    
        jsonb_by_id_every_col_test()
    
        # json_id_test()
    
        # jsonb_id_test()
    
        # json_where_name_test()
    
        # jsonb_name_test()
    
        # jsonb_where_nconst_test()
    
        # json_where_nconst_test()
    
        # jsonb_by_where_nconst_every_col_test()
    
        # json_by_where_nconst_every_col_test()
    
        json_update_by_id_every_col_test()
    
        jsonb_update_by_id_every_col_test()
    ```

    



**Сравнение времени, затрачиваемого JSON и JSONB при вставке данных в базу данных:**

| Типа  | Времия |
| ----- | ------ |
| JSON  | 49s    |
| JSONB | 79.32s |



**Сравнение времени SELECT для каждого поля JSON в таблице tb_json：**

![output](doc/pic/README/output-1825514.png)





 **Сравнение времени SELECT для каждого поля JSONB в таблице tb_jsonb：**

![output](doc/pic/README/output-1825595.png)



**Сравнение скорости запросов к таблицам JSON и JSONB для всех полей：**

![output](doc/pic/README/output-1825645.png)

---

**Сравнение времени UPDATE для каждого поля JSON в таблице tb_json：**

![output](doc/pic/README/output-1825888.png)



**Сравнение времени UPDATE для каждого поля JSONB в таблице tb_jsonb：**

![output](doc/pic/README/output-1825910.png)





**Сравнение скорости UPDATE к таблицам JSON и JSONB для всех полей：**

![output](doc/pic/README/output-1825973.png)

---

### TOAST

<p>
    <!-- 在PG中，页是数据在文件存储中的基本单位，其大小是固定的且只能在编译期指定，之后无法修改，默认的大小为8KB。同时，PG不允许一行数据跨页存储。那么对于超长的行数据，PG就会启动TOAST，将大的字段压缩或切片成多个物理行存到另一张系统表中（TOAST表），这种存储方式叫行外存储。-->
</p>

В PG **страница является основной единицей хранения данных в файле**, ее размер фиксирован и может быть задан только во время компиляции и не может быть изменен впоследствии, **размер по умолчанию составляет 8 КБ**. 

Кроме того, **PG не позволяет хранить строку данных на разных страницах**. Для очень длинных строк данных PG инициирует TOAST, который сжимает или нарезает большие поля на несколько физических строк и сохраняет их в другой системной таблице (таблица TOAST), этот тип хранения называется **внерядным хранением**.

<p>
    <!--
 在 PG 中每个表字段有四种 TOAST 的策略：
    PLAIN —— 避免压缩和行外存储。只有那些不需要 TOAST 策略就能存放的数据类型允许选择（例如 int 类型），而对于 text 这类要求存储长度超过页大小的类型，是不允许采用此策略的。
    EXTENDED —— 允许压缩和行外存储。一般会先压缩，如果还是太大，就会行外存储。这是大多数可以TOAST的数据类型的默认策略。
    EXTERNAL —— 允许行外存储，但不许压缩。这让在text类型和bytea类型字段上的子串操作更快。类似字符串这种会对数据的一部分进行操作的字段，采用此策略可能获得更高的性能，因为不需要读取出整行数据再解压。
    MAIN —— 允许压缩，但不许行外存储。不过实际上，为了保证过大数据的存储，行外存储在其它方式（例如压缩）都无法满足需求的情况下，作为最后手段还是会被启动。因此理解为：尽量不使用行外存储更贴切
-->
</p>

**Для каждого поля таблицы в PG существует четыре стратегии TOAST.**

- `PLAIN` - **позволяет избежать сжатия и хранения вне ряда**. Разрешается выбирать только те типы данных, для хранения которых не требуется политика TOAST (например, типы int), в то время как для таких типов, как текст, требующих длины хранения, превышающей размер страницы, эта политика недопустима.
- `EXTENDED` - **позволяет сжимать и хранить вне ряда**. Как правило, сначала он сжимается, а если он все еще слишком большой, то сохраняется вне очереди. Это политика по умолчанию для большинства типов данных, которые могут быть TOASTed.
- `EXTERNAL` - **позволяет хранить данные вне ряда**, но без сжатия. Это значительно ускоряет операции подстроки для полей типа text и bytea. Такие поля, как строки, которые работают с частью данных, могут достичь более высокой производительности при использовании этой политики, поскольку нет необходимости считывать всю строку данных и затем распаковывать ее.
- `MAIN` - **позволяет сжимать, но не хранить вне линии**. На практике, однако, внепоточное хранение активируется в крайнем случае, когда других методов (например, сжатия) недостаточно для гарантированного хранения больших данных. Поэтому правильнее будет сказать, что хранение вне ряда вообще не должно использоваться.



**Просмотр политики TOAST для таблицы tb_jsonb:**

```bash
postgres=# \d+ tb_jsonb;

                                   Table "public.tb_jsonb"
 Column |  Type   | Collation | Nullable | Storage  | Compression | Stats target | Description
--------+---------+-----------+----------+----------+-------------+--------------+-------------
 iddata | integer |           | not null | plain    |             |              |
 imdata | jsonb   |           |          | extended |             |              |
 
Indexes:
    "ix_jsonb_iddata" btree (iddata)
Access method: heap



db_imdb=# select relname, relfilenode, reltoastrelid from pg_class where relname='tb_jsonb';
 relname  | relfilenode | reltoastrelid
----------+-------------+---------------
 tb_jsonb |      162078 |        162082
(1 row)

------------------------------------------------------------------------------------------------------------------
TOAST表有三个字段：
chunk_id —— 用来表示特定 TOAST 值的 OID ，可以理解为具有同样 chunk_id 值的所有行组成原表（这里的 blog ）的 TOAST 字段的一行数据。
chunk_seq —— 用来表示该行数据在整个数据中的位置。
chunk_data —— 该Chunk实际的数据
------------------------------------------------------------------------------------------------------------------
Таблица TOAST имеет три поля.
chunk_id -- используется для указания OID конкретного значения TOAST, которое можно интерпретировать как все строки с одинаковым значением chunk_id, образующие строку данных в поле TOAST исходной таблицы (в данном случае, блога).
chunk_seq -- используется для указания позиции данных ряда в общем массиве данных.
chunk_data -- фактические данные чанка
------------------------------------------------------------------------------------------------------------------

db_imdb=# \d+ pg_toast.pg_toast_162078;
TOAST table "pg_toast.pg_toast_162078"
   Column   |  Type   | Storage
------------+---------+---------
 chunk_id   | oid     | plain
 chunk_seq  | integer | plain
 chunk_data | bytea   | plain
Owning table: "public.tb_jsonb"
Indexes:
    "pg_toast_162078_index" PRIMARY KEY, btree (chunk_id, chunk_seq)
Access method: heap


postgres=# select * from pg_toast.pg_toast_162078;
```



**Тестирование политики TOAST в Postgresql**

1. **==[EXTENDED]== Сравнить изменение объема БД для актера с малым кол-вом ролей**

    ```sql
    BEGIN;
    SELECT * FROM tb_jsonb WHERE iddata=51989;
    SELECT pg_table_size('tb_jsonb');  -- 1145241600 Byte
    SELECT pg_size_pretty(pg_table_size('tb_jsonb'));  -- 1092 MB
    SELECT iddata, pg_column_size(imdata) , imdata, imdata->>'{name}' FROM tb_jsonb WHERE iddata=51989;  -- 202 Byte
    
    UPDATE tb_jsonb SET imdata=jsonb_set(imdata::jsonb, '{name}', '"Bf AAAAAAAAAAAAAAAAAAAAAAAAA"'::jsonb) WHERE iddata=51989;
    
    SELECT iddata, pg_column_size(imdata) , imdata, imdata->>'{name}' FROM tb_jsonb WHERE iddata=51989;  -- 230 Byte
    SELECT pg_table_size('tb_jsonb');  -- 1145241600 Byte
    SELECT pg_size_pretty(pg_table_size('tb_jsonb'));  -- 1092 MB
    ROLLBACK;
    ```

    

2. **==[EXTERNAL]== Сравнить изменение объема БД для актера с малым кол-вом ролей**

    Политика TOAST изменена на EXTERNAL для отключения сжатия

    ```BASH
    postgres=# BEGIN;
    postgres=# ALTER TABLE tb_jsonb ALTER imdata SET STORAGE EXTERNAL;
    
    db_imdb=*# \d+ tb_jsonb;
                                       Table "public.tb_jsonb"
     Column |  Type   | Collation | Nullable | Storage  | Compression | Stats target | Description
    --------+---------+-----------+----------+----------+-------------+--------------+-------------
     iddata | integer |           | not null | plain    |             |              |
     imdata | jsonb   |           |          | external |             |              |
    Indexes:
        "ix_jsonb_iddata" btree (iddata)
    Access method: heap
    
    ```

    

    ```sql
    BEGIN;
    ALTER TABLE tb_jsonb ALTER imdata SET STORAGE EXTERNAL;
    
    SELECT * FROM tb_jsonb WHERE iddata=51989;
    SELECT pg_table_size('tb_jsonb');  -- 1202307072 Byte
    SELECT pg_size_pretty(pg_table_size('tb_jsonb'));  -- 1147 MB
    SELECT iddata, pg_column_size(imdata) , imdata, imdata->>'{name}' FROM tb_jsonb WHERE iddata=51989;  -- 202 Byte
    select count(*) from pg_toast.pg_toast_162078; -- 511805
    
    UPDATE tb_jsonb SET imdata=jsonb_set(imdata::jsonb, '{name}', '"Bf AAAAAAAAAAAAAAAAAAAAAAAAA"'::jsonb) WHERE iddata=51989;
    
    SELECT iddata, pg_column_size(imdata) , imdata, imdata->>'{name}' FROM tb_jsonb WHERE iddata=51989;  -- 230 Byte
    SELECT pg_table_size('tb_jsonb');  -- 1202307072 Byte
    SELECT pg_size_pretty(pg_table_size('tb_jsonb'));  -- 1147 MB
    select count(*) from pg_toast.pg_toast_162078; -- 511805
    ROLLBACK;
    ```

    
    
3. **==[EXTENDED]== Сравнить изменение объема БД для актера с большим кол-вом ролей**

    ```sql
    BEGIN;
    SELECT pg_table_size('tb_jsonb');  -- 1145241600 Byte
    SELECT pg_size_pretty(pg_table_size('tb_jsonb'));  -- 1092 MB
    SELECT iddata, pg_column_size(imdata) , imdata, imdata->>'{name}' FROM tb_jsonb WHERE iddata=3789;  -- 4034997 Byte
    
    UPDATE tb_jsonb SET imdata=jsonb_set(imdata::jsonb, '{name}', '"David AAAAAAAAAAAAAAAAAAAAAAAAA"'::jsonb) WHERE iddata=3789;
    
    SELECT iddata, pg_column_size(imdata) , imdata, imdata->>'{name}' FROM tb_jsonb WHERE iddata=3789;  -- 4035007 [+10]  Byte
    SELECT pg_table_size('tb_jsonb');  -- 1149378560 [+4136960]  Byte
    SELECT pg_size_pretty(pg_table_size('tb_jsonb'));  -- 1096 MB [+3.9453125 MB]
    ROLLBACK;
    ```

    

4. **==[EXTERNAL]== Сравнить изменение объема БД для актера с большим кол-вом ролей**

    Политика TOAST изменена на EXTERNAL для отключения сжатия

    ```BASH
    postgres=# BEGIN;
    postgres=# ALTER TABLE tb_jsonb ALTER imdata SET STORAGE EXTERNAL;
    
    db_imdb=*# \d+ tb_jsonb;
                                                             Table "public.tb_jsonb"
     Column |  Type   | Collation | Nullable | Storage  | Compression | Stats target | Description
    --------+---------+-----------+----------+----------+-------------+--------------+-------------
     iddata | integer |           | not null | plain    |             |              |
     imdata | jsonb   |           |          | external |             |              |
    Indexes:
        "ix_jsonb_iddata" btree (iddata)
    Access method: heap
    
    ```

    

    Вы можете видеть, что объем данных значительно больше без включенного сжатия.

    ```sql
    BEGIN;
    ALTER TABLE tb_jsonb ALTER imdata SET STORAGE EXTERNAL;
    
    SELECT pg_table_size('tb_jsonb');  -- 1186045952 Byte
    SELECT pg_size_pretty(pg_table_size('tb_jsonb'));  -- 1131 MB
    SELECT iddata, pg_column_size(imdata) , imdata, imdata->>'{name}' FROM tb_jsonb WHERE iddata=3789;  -- 4034997 Byte
    
    UPDATE tb_jsonb SET imdata=jsonb_set(imdata::jsonb, '{name}', '"David AAAAAAAAAAAAAAAAAAAAAAAAA"'::jsonb) WHERE iddata=3789;
    
    SELECT iddata, pg_column_size(imdata) , imdata, imdata->>'{name}' FROM tb_jsonb WHERE iddata=3789;  -- 15845197 [+11810200] Byte
    SELECT pg_table_size('tb_jsonb');  -- 1202307072 [+16261120] Byte
    SELECT pg_size_pretty(pg_table_size('tb_jsonb'));  -- 1147 MB [+16 MB]
    ROLLBACK;
    ```

    

    **Результат:**

    <p>
    <!--
        如果策略允许压缩，则TOAST优先选择压缩。
        不管是否压缩，一旦数据超过2KB左右，就会启用行外存储。
        修改TOAST策略，不会影响现有数据的存储方式。
    -->
    </p>

    - Если политика разрешает сжатие, TOAST предпочитает сжатие.
    - Хранение вне ряда включается, когда объем данных превышает примерно 2 КБ, независимо от того, сжаты они или нет.
    - Изменение политики TOAST **не** повлияет на способ хранения существующих данных.





























