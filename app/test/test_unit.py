import pytest
from news.views import home
from django.contrib.auth.models import AnonymousUser, User

# health check
def test_index_page(client):
    expected = 'Application news portal Started'
    result = client.get('/health').content.decode("utf-8")
    assert expected in result

# Test news search function
@pytest.mark.django_db
def test_likes(client):
  link_ref = '/pages/like/6922'
  expected_content = [
    '<strong class="text-secondary">0 Likes</strong>'
  ]

  expected_content2 = ['<strong class="text-secondary">1 Like</strong>']


  result = client.get('/pages/news/6922')
  content = result.content.decode("utf-8")
  print(content)

  for value in expected_content:
    assert value in content
  assert result.status_code == 200

  result = client.get('/pages/like/6922')
  result = client.get('/pages/news/6922')
  content = result.content.decode("utf-8")
  print(content)

  for value in expected_content2:
    assert value in content
  assert result.status_code == 200



@pytest.mark.django_db
def test_dislikes(client):
  link_ref = '/pages/like/6922'
  expected_content = [
    '<strong class="text-secondary">0 Dislikes</strong>'
  ]

  expected_content2 = ['<strong class="text-secondary">1 Dislike</strong>']


  result = client.get('/pages/news/6922')
  content = result.content.decode("utf-8")
  print(content)

  for value in expected_content:
    assert value in content
  assert result.status_code == 200

  result = client.get('/pages/dislike/6922')
  result = client.get('/pages/news/6922')
  content = result.content.decode("utf-8")
  print(content)

  for value in expected_content2:
    assert value in content
  assert result.status_code == 200


#test za postavljanje komentara
@pytest.mark.django_db
def test_comments(client):
    expected_content = [
        'Nemanja',
        'Ovo je probni komentar',
    ]

    form_data = {
        'tmp_username': 'Nemanja',
        'text': 'Ovo je probni komentar',
        'news_id': '6922'
    }

    response = client.get('/pages/news/6922')
    content = response.content.decode("utf-8")
    
    response = client.post('/pages/comment', data=form_data, follow=True)
    response = client.get('/pages/news/6922')
    content = response.content.decode("utf-8")

    for value in expected_content:
        assert value in content


# test za draft bez postavljanja na uvid
@pytest.mark.django_db
def test_add_draft(client):
    
    expected_content = [
        'Test',
        'test',
    ]

    expected_content2 = [
        'No drafts found',
    ]
    
    username = "Nemanja"
    password = "zolazola02"
    client.login(username=username, password=password)

    response = client.get('/pages/add')
    content = response.content.decode("utf-8")

    form_data = {
        'title': 'Test News',
        'tags': 'test, proba, s',
        'content': 'This is a test news article.',
        'category': '1',
        'is_up_for_review': 'false',
        'csrfmiddlewaretoken': 'mUdic9esUucOV6voXp8iLn7B52XFv3hxiqvy1etQwaHL4Bpa7EGZUNb9MgifVKXO'
    }

    response = client.post('/pages/add', data=form_data, follow=True)
    response = client.get('/drafts/view')
    content = response.content.decode("utf-8")
    
    for value in expected_content:
        assert value in content

    response = client.get('/accounts/logout/')
    username = "cone"
    password = "cone"
    client.login(username=username, password=password)

    response = client.get('/drafts/view')
    content = response.content.decode("utf-8")
    print(content)

    for value in expected_content2:
        assert value in content

# test za draft i postavljanje na uvid
@pytest.mark.django_db
def test_add_draft_for_review(client):
    
    expected_content = [
        'Test',
        'test',
    ]

    
    username = "Nemanja"
    password = "zolazola02"
    client.login(username=username, password=password)

    response = client.get('/pages/add')
    content = response.content.decode("utf-8")

    form_data = {
        'title': 'Test News',
        'tags': 'test, proba, s',
        'content': 'This is a test news article.',
        'category': '1',
        'is_up_for_review': 'true',
        'csrfmiddlewaretoken': 'mUdic9esUucOV6voXp8iLn7B52XFv3hxiqvy1etQwaHL4Bpa7EGZUNb9MgifVKXO'
    }

    response = client.post('/pages/add', data=form_data, follow=True)
    response = client.get('/drafts/view')
    content = response.content.decode("utf-8")
    
    for value in expected_content:
        assert value in content

    response = client.get('/accounts/logout/')
    username = "cone"
    password = "cone"
    client.login(username=username, password=password)

    response = client.get('/drafts/view')
    content = response.content.decode("utf-8")
    print(content)

    for value in expected_content:
        assert value in content



# test za draft i postavljanje novosti posle uvida
@pytest.mark.django_db
def test_add_draft_and_approved(client):
    
    expected_content = [
        'Test',
        'test',
    ]

    expected_content2 = [
        'Test',
        'test',
        'proba',
        's',
        'Test News'
    ]

    
    username = "Nemanja"
    password = "zolazola02"
    client.login(username=username, password=password)

    response = client.get('/pages/add')
    content = response.content.decode("utf-8")

    form_data = {
        'title': 'Test News',
        'tags': 'test, proba, s',
        'content': 'This is a test news article.',
        'category': '1',
        'is_up_for_review': 'true',
        'csrfmiddlewaretoken': 'mUdic9esUucOV6voXp8iLn7B52XFv3hxiqvy1etQwaHL4Bpa7EGZUNb9MgifVKXO'
    }

    response = client.post('/pages/add', data=form_data, follow=True)
    response = client.get('/drafts/view')
    content = response.content.decode("utf-8")
    
    for value in expected_content:
        assert value in content

    response = client.get('/accounts/logout/')
    username = "cone"
    password = "cone"
    client.login(username=username, password=password)

    response = client.get('/drafts/detail/10') #vrv nepoteban korak // mora da se namesti da radi prema bazi 
    content = response.content.decode("utf-8")

    for value in expected_content:
      assert value in content

    response = client.get('/drafts/approve/10') #mora da se namesti da radi prema bazi 
    response = client.get('/pages/news/6925') #mora da se namesti da radi prema bazi 
    
    for value in expected_content2:
      assert value in content

    print(content)

   

