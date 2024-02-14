# Проjектни задатак из Проjектовања информационих система

[Задатак](./поставка.pdf) - Креирати веб апликациjу коjа представља портал електронских новина.

Чланови тима *Чипчаши и Лукица* :
* Богдан Митровић - *frontend engineer*
* Лазар Илић - *backend engineer*
* Немања Марковић - *Quality assurance engineer*
* Лука Петровић - *DevOps/system/infra engineer*


## Структура апликације

Апликација је базирана на [*Django*](https://www.djangoproject.com/) фрејмворку, а с тим у вези, тестови су писани у **python**-у, док је фронтенд базиран на употреби [*bootstrap*](https://getbootstrap.com/)-a. 

Што се тиче базе података, у локалној верзији је коришћен [*sqlite3*](https://www.sqlite.org/index.html), док је у контејнеризованој верзији рађено са [*postgres*](https://www.postgresql.org/)-ом.





## Упутство за покретање




<br>

**Докеризовано покретање**
* Клонирати овај репозиторијум
* Инсталирати [*docker*](https://docs.docker.com/get-docker/).
* Распаковати [fajlovi_baze.zip](./app/fajlovi_baze.zip)
* Апликацију покренути командом:
   ```bash
  docker compose build
  docker compose up
  ```
* <details markdown='block'>
  <summary>Опционо (superuser)</summary>

    При иницијализацији базе се генерише *superuser* са параметрима за приступ систему:

    * username: pantelija
    * password: pantelija
  
    Уколико желите додати још неког, потребно је унети следеће команде:
    ```bash
    docker exec -it mysite sh
    python manage.py createsuperuser
    ```
  </details>

* У *web-browser*-у се упутити на [адресу](http://127.0.0.1:8000/).


<br>

<br>

**Локална инсталација**
* Клонирати овај репозиторијум
* Инсталирати верзију [**python**](https://www.python.org/downloads/release/python-379/)-а 3.7.9.
  
<details markdown='block'>
<summary>Опционо</summary>

---

И даље је препорука користити виртуелна окружења, помоћу [anaconda](https://www.anaconda.com/) менаџера или [venv](https://docs.python.org/3/library/venv.html) модула(укљученог у **python** дистрибуције).

<br>

Искористити следеће команде (*anaconda* варијанта):
```bash
  conda env create -n "ime_okruzenja" python=3.7.9
  conda activate ime_okruzenja
```
<br>

или (*venv* варијанта):

```bash
  python3.7.9 -m venv ime_okruzenja
```
*venv* активација за *Windows* кориснике
```bash
  ime_okruzenja\Scripts\activate
```

*venv* активација за *Linux/MacOS* кориснике
```bash
  source ime_okruzenja/bin/activate
```
<br>

Потребно је активирати окружење након ресетовања система, а пре покретања пројекта.
Како бисте изашли из виртуелног окружења, користите (*anaconda* варијанта):
```bash
  conda deactivate
```
или (*venv* варијанта):

```bash
  deactivate
```
---

<br>

<br>



</details>

* Инсталирати неопходне *dependency*-е:
```bash
cd app
pip install -r requirement.txt
```
<details markdown='block'>
<summary>Грешке при инсталирању</summary>

<br>

---

Уколико се деси да се поступак заврши грешком при инсталацији *Pillow*-а (или генерално било које ставке), поступити на следећи начин:
  * Исећи из фајла **requirement.txt** линију која садржи ставку која генерише грешку, у овом примеру Pillow==5.3.0.
  * Сачувати измењени фајл **requirement.txt**.
  * Покренути команду:
```bash
pip install Pillow==5.3.0
```
  * Поново покренути команду:
```bash
pip install -r requirement.txt
```
  * Понављати поступак док се процес не заврши без грешака.
  * Уколико ово није од помоћи, посаветујте се са [лекаром или фармацеутом](https://chat.openai.com/).

---
<br>

</details>

* Распаковати [fajlovi_baze.zip](./app/fajlovi_baze.zip)

* Покренути скрипту за иницијализацију базе података. 
  ```bash
  python baza_local.py
  ```
* Креирати *superuser*-а, корисника који одговара роли главног уредника.
  ```bash
  python manage.py -l createsuperuser
  ```
  Ово је такође опционо, при иницијализацији базе се генерише *superuser* са параметрима за приступ систему: 
    * username: pantelija
    * password: pantelija
* Апликацију покренути командом:
  ```bash
  python manage.py -l runserver
  ```
* У *web-browser*-у се упутити на [адресу](http://127.0.0.1:8000/).


<br>


**Тестирање**
* Како бисте покренули тестове, пребаците се у одговарајући директоријум, и покрените их:
  ```bash
  cd app
  pytest test/test_unit.py
  pytest test/test_int.py
  ```


