# Проjектни задатак из Проjектовања информационих система - backend грана

[Задатак](./поставка.pdf) - Креирати веб апликациjу коjа представља портал електронских новина.

Чланови тима *Чипчаши и Лукица* :
* Богдан Митровић
* Лазар Илић
* Немања Марковић
* Лука Петровић


## Упутство за инсталацију

<br>

**Препоручен поступак**:
* Клонирати овај репозиторијум
* Креирати виртуелно [**python**](https://www.python.org/) окружење коришћењем [anaconda](https://www.anaconda.com/) менаџера.
  ```bash
  cd app
  conda env create --file django.yml
  ```
* Активирати поменуто виртуелно окружење (извршити прe покретањa пројекта, након сваког рестартовања оперативног система).
  ```bash
  conda activate djangoo
  ```
* Креирати *superuser*-а, корисника који одговара роли главног уредника.
  ```bash
  python manage.py createsuperuser
  ```
* Апликацију покренути командом:
  ```bash
  python manage.py runserver
  ```
* У *web-browser*-у се упутити на [адресу](http://127.0.0.1:8000/).

<br>

**Алтернативни поступак**
* Клонирати овај репозиторијум
* Инсталирати верзију [**python**](https://www.python.org/downloads/release/python-379/)-а 3.7.9.
  
<details markdown='block'>
<summary>Опционо</summary>

---

И даље је препорука користити виртуелна окружења, помоћу [anaconda](https://www.anaconda.com/) менаџера или [venv](https://docs.python.org/3/library/venv.html) модула(укљученог у **python** дистрибуције).

<br>

Искористити следеће команде(*anaconda* варијанта):
```bash
  conda env create -n "ime_okruzenja" python=3.7.9
  conda activate ime_okruzenja
```
<br>

или(*venv* варијанта):

```bash
  python3.7.9 -m venv ime_okruzenja
```
*venv* активација за *Windows* кориснике
```bash
  venv\Scripts\activate
```

*venv* активација за *Linux/MacOS* кориснике
```bash
  source venv/bin/activate
```
<br>

Потребно је активирати окружење након ресетовања система, а пре покретања пројекта.
Како бисте изашли из виртуелног окружења, користите:
```bash
  conda deactivate
```
или

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

* Креирати *superuser*-а, корисника који одговара роли главног уредника.
  ```bash
  python manage.py createsuperuser
  ```
* Апликацију покренути командом:
  ```bash
  python manage.py runserver
  ```
* У *web-browser*-у се упутити на [адресу](http://127.0.0.1:8000/).




<br>


## Имплементирано до сада

* систем пријаве
* претрага новости
* коментарисање новости
* лајковање новости/коментара
* **superuser** има могћуности (парцијално имплементиране) креирања, измене, уклањања чланака
