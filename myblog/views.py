# Create your views here.
from tkinter.font import names

from Demos.win32ts_logoff_disconnected import session
from django.contrib.sessions.models import Session
from django.shortcuts import render, HttpResponse, redirect
from openai import OpenAI
from myblog.models import UserBookmark
from . import api_auth
import html

class Dish:
    def __init__(self) -> None:
        self.name = ""
        self.content = ""
        self.html_table = ""

    def set_dish(self, name, content, html_table) -> None:
        self.name = name
        self.content = content
        self.html_table = html_table

    def get_dish(self):
        return {'name': self.name, 'content' : self.content, 'html_table' : self.html_table}

current_dish = Dish()

def http_test(request) -> 'http response':
    value = request.GET['sga']
    return HttpResponse("AI<a href='https://github.com/pawelsalawa/sqlitestudio/releases'>AI機器人"+value+"</a>上菜囉~")

site_name = "我最AI的私房料理"

def index(request) -> 'html':
    vegetable_list = ('高麗菜','菠菜','胡蘿蔔','番茄','絲瓜','玉米','苦瓜',
                      '竹筍','馬鈴薯','小白菜','香菇','洋蔥','不吃菜')
    meat_list = ('豬', '雞', '牛', '魚', '羊','不吃肉')
    favor_list = ('重口味', '重口味又辣', '清淡', '煮湯')

    return render(request, 'index.html',{"site_name":site_name, "vegetable_list":vegetable_list
                                         ,"meat_list":meat_list, "favor_list":favor_list})

def get_ai_response(ingredients) -> str:
    client = OpenAI(
        api_key = api_auth.get_api_auth()
    )

    keyword = "加上"

    if ingredients[0] == '不吃菜':
        ingredients[0] = ''
        keyword = ''

    if ingredients[1] == '不吃肉':
        ingredients[1] = ''
        keyword = ',素食'

    ai_input = "提供一道用" + ingredients[0] + keyword + ingredients[1] + "烹飪的料理，味道要" \
            + ingredients[2] +"料理名稱放在全文最前面" + "全文最後附上營養成分整理成html的表格語法，整段語法前後附上'@tbl'這個字串"

    print(ai_input)

    debug = False

    if not debug:
        response = client.responses.create(
            model="gpt-4.1-mini",
            input=ai_input
        )

        return response.output_text

    return 'demo菜色\ndemo作法'

def get_sessionid(request):
    session_id = request.COOKIES.get('sessionid')

    if session_id:
        return True
    return False

def result(request) -> 'html':
    vegetable = request.POST['vege-select']
    meat = request.POST['meat-select']
    favor = request.POST['favor-select']
    ingredients_list = [vegetable, meat, favor]

    ai_output = get_ai_response(ingredients_list)
    # print(ai_output)
    dish = ai_output.split("\n", 1)
    dish_name = dish[0]
    table_start_index = dish[1].find('@')
    html_table = dish[1][table_start_index+4:-4]
    dish_content = dish[1][:table_start_index]
    current_dish.set_dish(dish_name, dish_content, html_table)

    # print(dish_content_substring)

    has_cookie = 'false'

    if get_sessionid(request):
        has_cookie = 'true'

    return render(request,'result.html',{ "site_name":site_name, "dish_name":dish_name,
                                         "dish_content":dish_content, "html_table":html_table, "has_cookie":has_cookie })

def add_bookmark(request):
    print("register here")
    if not request.session.has_key('logged_in'):
        request.session['logged_in'] = True
        request.session.save()
    else:
        logged_in = request.session['logged_in']
        print("session", logged_in)

    # print(request.session.session_key)
    # print(current_dish.get_dish()['name'])
    # print(current_dish.get_dish()['content'])

    current_session = Session.objects.get(session_key = request.session.session_key)
    current_bookmark = UserBookmark(title = current_dish.get_dish()['name'], content = current_dish.get_dish()['content'],
                                    html_table = current_dish.get_dish()['html_table'], session = current_session)

    current_bookmark.save()
    #return HttpResponse("已加入收藏!")
    return redirect('/bookmark/')

def show_bookmark(request):

    try:
        Session.objects.get(session_key=request.session.session_key)
    except Exception as err:
        print(str(err))
        print("No keys found in cookie!")
        return render(request, 'bookmark.html', {"site_name": site_name, 'dishes': None, 'dishes_num': 0})

    # dishes = UserBookmark.objects.all()
    dishes = UserBookmark.objects.filter(session_id=request.session.session_key)
    # dishes = UserBookmark.objects.filter(session_id='d84mj0s3yinjqsbs1gqj0yl8cuzznwuq')
    dishes_num = dishes.count()

    print(dishes_num)
    return render(request,'bookmark.html', { "site_name":site_name,'dishes' : dishes,'dishes_num':dishes_num })


def delete_bookmark(request, dish_id):
    dish = UserBookmark.objects.get( id=dish_id )
    dish.delete()
    return redirect('/bookmark')