import pytest
from news.views import home
from django.contrib.auth.models import AnonymousUser, User


def test_index_page(client):
    expected = 'Application news portal Started'
    result = client.get('/health').content.decode("utf-8")
    assert expected in result

#testiranje home_page
@pytest.mark.django_db
def test_home_page(client):
    
    expected_content = [
        ' <title>News Portal</title>',
        '<a class="nav-link" href=/1/>Home <span class="sr-only">(current)</span></a>',
        ' <a class="nav-link" href=/accounts/login/>Login</a>',
    ]
    result = client.get('/1')  
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
        '<title>News Portal</title>',
        '<a class="nav-link" href=/change_password/>Change Password</a>',
        '<a class="nav-link" href=/users/register>Register a user</a>',
        '<a class="nav-link" href=/accounts/logout/>Signout</a>'
    ]
    username = "cone"
    password = "cone"
    client.login(username=username, password=password)
    result = client.get('/1')
    content = result.content.decode("utf-8")

    for value in expected_content:
        assert value in content
    assert result.status_code == 200


## test login stranice
@pytest.mark.django_db
def test_login_page(client):

    expected_content = [
      '<title>News Portal</title>',
      '<label for="id_username">Username:</label>',
      '<input type="text" name="username" autofocus autocapitalize="none" autocomplete="username" maxlength="150" required id="id_username">',
      '<label for="id_username">Username:</label>',
      '<input type="password" name="password" autocomplete="current-password" required id="id_password">',
      '<button type="submit">Login</button>'
    ]

    result = client.get('/accounts/login/')
    #print(result)
    content = result.content.decode("utf-8")
    #print(content)

    for value in expected_content:
      assert value in content
    assert result.status_code == 200




# pretraga po rubrici
@pytest.mark.django_db
def test_category(client):

  expected_content = [
     '<title>News Portal</title>',
     'Sharapova, Djokovic hit by injury'
  ]
  result = client.get('/pages/search/1?cat=2')
  content = result.content.decode("utf-8")
  #print(content)
  for value in expected_content:
    assert value in content
  assert result.status_code == 200

 
# testiranje pretrage
@pytest.mark.django_db
def test_news_search(client):
  expected_content = [
    '<title>News Portal</title>',
    'Serbians wait on No. 1 Djokovic for home Davis Cup semifinal'
  ]

  username = "cone"
  password = "cone"
  client.login(username=username, password=password)
  result = client.get('/pages/search/1?cat=&search=djokovic')
  content = result.content.decode("utf-8")
  #print(content)
  for value in expected_content:
    assert value in content
  assert result.status_code == 200