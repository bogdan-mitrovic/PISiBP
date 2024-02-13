import pytest
from news.views import home
from django.contrib.auth.models import AnonymousUser, User


# health check
def test_index_page(client):
    expected = 'Application news portal Started'
    result = client.get('/health').content.decode("utf-8")
    assert expected in result

#testiranje home_page kod neprijavljenog korisnika
@pytest.mark.django_db
def test_home_page(client):
    
    expected_content = [
        '<title>Čipčasi i Lukica</title>',
        '<a class="nav-link" href=/1/>Pocetna <span class="sr-only">(current)</span></a>',
        '<a class="nav-link" href=/accounts/login/>Uloguj se</a>',
    ]
    result = client.get('/1/')  
    print(result)
    content = result.content.decode("utf-8")
    print(content)
    
    for value in expected_content:
      assert value in content
    assert result.status_code == 200

#testiranje home_page kod prijavljenog korisnika
@pytest.mark.django_db
def test_dashboard_page(client):
    expected_content = [
        '<title>Čipčasi i Lukica</title>',
        '<a class="nav-link" href=/1/>Pocetna<span class="sr-only">(current)</span></a>',
        '<a class="nav-link" href=/accounts/logout/>Odjavi se</a>'
    ]
    username = "cone"
    password = "cone"
    client.login(username=username, password=password)
    result = client.get('/1/')
    content = result.content.decode("utf-8")
    print(content)

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

  


# Test news search function
@pytest.mark.django_db
def test_title_search(client):
  expected_content = [
    '<title>Čipčasi i Lukica</title>',
    '<a href="/pages/news/3557" class="card-title" style="color: #113fa2; font-size: x-large;">Serbians wait on No. 1 Djokovic for home Davis Cup sem…</a>',
    '<p class="card-text" style="color: #fff; position: absolute; bottom: 0; left: 0; background-color: #113fa2; padding: 5px 10px; margin: 0; font-size: larger;">sport</p>'
  ]

  result = client.get('/pages/search/1?cat=&search=djokovic')
  content = result.content.decode("utf-8")
  print(content)
  for value in expected_content:
    assert value in content
  assert result.status_code == 200

# Test news search function
@pytest.mark.django_db
def test_date_search(client):
  link_ref = '/pages/news/3962'
  expected_content = [
    '<title>Čipčasi i Lukica</title>',
    '/pages/news/3962'
  ]

  expected_content2 = ['Date created: Nov. 15, 2011, 11:08 p.m.']

  

  result = client.get('/pages/search/1?cat=&search=&date1=2011-11-15&date2=2011-11-15')
  content = result.content.decode("utf-8")
  print(content)

  for value in expected_content:
    assert value in content
  assert result.status_code == 200

  result = client.get('/pages/news/3962')
  content = result.content.decode("utf-8")

  for value in expected_content2:
    assert value in content
  assert result.status_code == 200

# Test news search function
@pytest.mark.django_db
def test_tags_search(client):
  link_ref = '/pages/news/6922'
  expected_content = [
    '<title>Čipčasi i Lukica</title>',
    '/pages/news/6922'
  ]

  expected_content2 = ['Tags: nauka ,  baze ,  faks']


  result = client.get('/pages/search/1?cat=&search=faks&date1=&date2=')
  content = result.content.decode("utf-8")

  for value in expected_content:
    assert value in content
  assert result.status_code == 200

  result = client.get('/pages/news/6922')
  content = result.content.decode("utf-8")

  for value in expected_content2:
    assert value in content
  assert result.status_code == 200

'''
# test unauthorized access to premium category
@pytest.mark.django_db
@pytest.mark.xfail
def test_unauthorized_premium_category(client):
  expected_content = [
    '<h5 class="card-title">Once upon a time</h5>',
    '<p class="card-text">A page in an Oliver Twist book Oliver Twist Parish Boy&#39;s Progress is a title-character novel, written in 1838. It was written by Charles Dickens.  Storyline &#39;Oliver Twist&#39; The Parish Boy&#39;s Progress is</p>',
    '<a href="/pages/news/1" class="btn btn-primary">Read More</a>'
  ]
  result = client.get('/pages/news?cat=4')
  content = result.content.decode("utf-8")
  #print(content)
  for value in expected_content:
    assert value in content
  assert result.status_code == 200



# test premium user ask for premium content
@pytest.mark.django_db
def test_authorized_premium_category(client):
  expected_content = [
    '<h5 class="card-title">Once upon a time</h5>',
    '<p class="card-text">A page in an Oliver Twist book Oliver Twist Parish Boy&#39;s Progress is a title-character novel, written in 1838. It was written by Charles Dickens.  Storyline &#39;Oliver Twist&#39; The Parish Boy&#39;s Progress is</p>',
    '<a href="/pages/news/1" class="btn btn-primary">Read More</a>'
  ]
  username = "admin"
  password = "123456"
  client.login(username=username, password=password)
  result = client.get('/pages/news?cat=4')
  content = result.content.decode("utf-8")
  #print(content)
  for value in expected_content:
    assert value in content
  assert result.status_code == 200
'''

'''
# poseban sadrzaj koji pokusava da pogleda neovlascena osoba
# nije dobar primer jer mora da se namesti da radi zapravo
@pytest.mark.django_db
def test_unauthorized_premium_content(client):
  expected_content = [
     '<title>News Portal</title>',
    '<h1>Manchester City ban talk of Tevez</h1>',
    'Date created: Sept. 30, 2011, 4:54 p.m.',
    '<strong class="text-secondary">261 Likes</strong>',
    ' <img class="img-fluid mx-auto p-2 content-image" src="https://cdn.cnn.com/cnnnext/dam/assets/110930033652-tevez-30-9-2011-story-top.jpg">'
  ]
  result = client.get('/pages/news/5')
  content = result.content.decode("utf-8")
  #print(content)
  for value in expected_content:
    assert value in content
  assert result.status_code == 200
'''
#ZBOG OVOG GORE NEMA SMISLA RADITI TESTOVE ISPOD
'''
# test unauthorized access client error message
@pytest.mark.django_db
def test_unauthorized_premium_content_error_msg(client):
  expected_content = [
    'Signup to view news'
  ]
  result = client.get('/pages/news/5')
  content = result.content.decode("utf-8")
  #print(content)
  for value in expected_content:
    assert value in content
  assert result.status_code == 200

# premium sadrzaj
@pytest.mark.django_db
def test_authorized_premium_content(client):
  expected_content = [
    '<h1>Science News for Premium Users</h1>',
    'Science News for Premium Users'
  ]

  username = "admin"
  password = "123456"
  client.login(username=username, password=password)
  result = client.get('/pages/news/5')
  content = result.content.decode("utf-8")
  #print(content)
  for value in expected_content:
    assert value in content
  assert result.status_code == 200
'''

# OVAJ TREBA DA TESTIRA KAD KORISNIK TRAZI VEST DIREKTNO U URL-U
# PREKO ID-A KOJI NE POSTOJI
'''
# test invalid content id
@pytest.mark.django_db
#@pytest.mark.xfail
def test_invalid_content_id(client):
  expected_content = [
    'Signup to view news'
  ]
  result = client.get('/pages/news/100')
  content = result.content.decode("utf-8")
  #print(content)
  for value in expected_content:
    assert value in content
  assert result.status_code == 200
'''

#TREBA DA SE NAPRAVI PREMIUM SADRZAJ
'''
# Test unauthorized news search function
@pytest.mark.django_db
def test_news_search_unauthorized(client):
  expected_content = [
    'User not supported'
  ]

  result = client.get('/pages/search?search=science')
  content = result.content.decode("utf-8")
  #print(content)
  for value in expected_content:
    assert value in content
  assert result.status_code == 200
'''

#OVO JE NEKO LUDILO ZNACI
'''
# Test login feature
@pytest.mark.django_db
def test_login_function(client):
  data = {
    "username" : "cone",
    "password" : "cone"
  }
  result = client.post('/accounts/login/',data)
  content = result.content.decode("utf-8")
  #print(result)
  assert result.status_code == 302
'''

#SIGN UP NE POSTOJI DIREKTNO NEGO PREKO SUPERUSERA KOJI MOZE DA REGISTRUJE KORISNIKA
'''
# Test Signup feature with invalid password
@pytest.mark.django_db
def test_invalid_signup(client):
  expected_content = [
    'Your password must contain at least 8 characters.'
  ]
  data = {
    "username" : "test_user",
    "password1" : "1",
    "password1" : "1"
  }
  result = client.post('/pages/signup',data)
  content = result.content.decode("utf-8")
  #print(content)
  for value in expected_content:
    assert value in content
  assert result.status_code == 200
'''


#NEMAMO COMMENT STRANICU TAKO DA MORA DRUGACIJE
'''
@pytest.mark.django_db
def test_comment_unauthorized(client):
  expected_content = [
    'User not supported'
  ]
  data = {
    "text" : "new comment from user 1",
    "id": 1
  }

  result = client.post('/pages/comment',data)
  content = result.content.decode("utf-8")
  #print(content)
  for value in expected_content:
    assert value in content
  assert result.status_code == 200




# Test invalid Post comment without id by authorized user
@pytest.mark.django_db
def test_invalid_comment(client):
  expected_content = [
    'invalid form'
  ]

  data = {
    "text" : "new comment from user 1"
  }
  client.login(username="admin", password="123456")
  result = client.post('/pages/comment',data)
  content = result.content.decode("utf-8")
  #print(result)
  for value in expected_content:
    assert value in content
  assert result.status_code == 200



# Test Post comment with invalid http method
@pytest.mark.django_db
def test_comment_invalid_method(client):
  expected_content = [
    'method not supported'
  ]

  client.login(username="admin", password="123456")
  result = client.get('/pages/comment?text=new')
  content = result.content.decode("utf-8")
  #print(result)
  for value in expected_content:
    assert value in content  
  assert result.status_code == 200
'''