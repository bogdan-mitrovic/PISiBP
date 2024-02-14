import pytest
from news.views import home
from django.contrib.auth.models import AnonymousUser, User


#testiranje home_page kod neprijavljenog korisnika
@pytest.mark.django_db
def test_home_page(client):
    
    expected_content = [
        '<title>Čipčasi i Lukica</title>',
        '<a class="nav-link" href=/1/>Početna <span class="sr-only">(current)</span></a>',
        '<a class="nav-link" href=/accounts/login/>Uloguj se</a>',
    ]
    result = client.get('/1/')  
    #print(result)
    content = result.content.decode("utf-8")
    #print(content)
    
    for value in expected_content:
      assert value in content
    assert result.status_code == 200

#testiranje home_page kod prijavljenog korisnika
@pytest.mark.django_db
def test_dashboard_page(client):
    expected_content = [
        '<title>Čipčasi i Lukica</title>',
        '<a class="nav-link" href=/1/>Početna <span class="sr-only">(current)</span></a>',
        '<a class="nav-link" href=/accounts/logout/>Odjavi se</a>'
    ]
    username = "cone"
    password = "cone"
    client.login(username=username, password=password)
    result = client.get('/1/')
    content = result.content.decode("utf-8")
    #print(content)

    for value in expected_content:
        assert value in content
    assert result.status_code == 200


## test login stranice
@pytest.mark.django_db
def test_login_page(client):

    expected_content = [
      '<title>Čipčasi i Lukica</title>',
      '<label class="form-label" for="username"  style="font-size: xx-large;">Korisničko ime </label>',
      '<input type="text" id="username" name="username" class="form-control form-control-lg" />',
      '<label class="form-label" for="password" style="font-size: xx-large;">Lozinka</label>',
      '<input type="password" id="password" name="password" class="form-control form-control-lg" />',
      '<button class="btn btn-info btn-lg btn-block custom-button" type="submit" >Uloguj se</button>'
    ]

    result = client.get('/accounts/login/')
    #print(result)
    content = result.content.decode("utf-8")
    #print(content)

    for value in expected_content:
      assert value in content
    assert result.status_code == 200




# pretraga po rubrici ps: kategorija 2 je nauka za sad
@pytest.mark.django_db
def test_category_search(client):
  
  expected_content = [
     '<title>Čipčasi i Lukica</title>',
     '<a class="dropdown-item" href="#" onclick="document.getElementById(\'selectedCategory\').value=\'2\';">nauka</a>',
     '<p class="card-text" style="color: #fff; position: absolute; bottom: 0; left: 0; background-color: #113fa2; padding: 5px 10px; margin: 0; font-size: larger;">nauka</p>'
  ]
  result = client.get('/pages/search/1?cat=2')
  content = result.content.decode("utf-8")
  #print(content)
  for value in expected_content:
    assert value in content
  assert result.status_code == 200



# pretraga po naslovu
@pytest.mark.django_db
def test_title_search(client):
  expected_content = [
    '<title>Čipčasi i Lukica</title>',
    '<a href="/pages/news/985" class="card-title" style="color: #113fa2; font-size: x-large;">Djokovic eyes French Open glory after &#x27;g…</a>',
    '<p class="card-text" style="color: #fff; position: absolute; bottom: 0; left: 0; background-color: #113fa2; padding: 5px 10px; margin: 0; font-size: larger;">sport</p>'
  ]

  result = client.get('/pages/search/2?cat=&search=djokovic&date1=&date2=')
  content = result.content.decode("utf-8")
  #print(content)
  for value in expected_content:
    assert value in content
  assert result.status_code == 200

# pretraga po datumu
@pytest.mark.django_db
def test_date_search(client):
  #link_ref = '/pages/news/144'
  expected_content = [
    '<title>Čipčasi i Lukica</title>',
    '/pages/news/144'
  ]

  expected_content2 = ['<strong>Datum kreiranja:</strong> Jan. 17, 2024, 10:58 a.m.']

  

  result = client.get('/pages/search/1?cat=&search=&date1=2024-01-17&date2=2024-01-17')
  content = result.content.decode("utf-8")
  #print(content)

  for value in expected_content:
    assert value in content
  assert result.status_code == 200

  result = client.get('/pages/news/144')
  content = result.content.decode("utf-8")

  for value in expected_content2:
    assert value in content
  assert result.status_code == 200

# pretraga po tagovima  
@pytest.mark.django_db
def test_tags_search(client):
  link_ref = '/pages/news/6922'
  expected_content = [
    '<title>Čipčasi i Lukica</title>',
    '/pages/news/467'
  ]

  expected_content2 = ['<strong>Tagovi:</strong>  world,   tennis,   venue']


  result = client.get('/pages/search/1?cat=&search=tennis&date1=&date2=')
  content = result.content.decode("utf-8")

  for value in expected_content:
    assert value in content
  assert result.status_code == 200

  result = client.get('/pages/news/467')
  content = result.content.decode("utf-8")

  for value in expected_content2:
    assert value in content
  assert result.status_code == 200
