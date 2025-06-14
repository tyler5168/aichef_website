# Create your views here.
from django.shortcuts import render, HttpResponse
from openai import OpenAI

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

def result(request) -> 'html':
    vegetable = request.POST['vege-select']
    meat = request.POST['meat-select']
    favor = request.POST['favor-select']
    ingredients_list = [vegetable, meat, favor]

    ai_output = get_ai_response(ingredients_list)
    # print(ai_output)
    dish = ai_output.split("\n", 1)
    return render(request,'result.html',{"site_name":site_name, "dish_name":dish[0],
                                         "dish_content":dish[1]})


def get_ai_response(ingredients) -> str:
    client = OpenAI(
        api_key=""
    )

    keyword = "加上"

    if ingredients[0] == '不吃菜':
        ingredients[0] = ''
        keyword = ''

    if ingredients[1] == '不吃肉':
        ingredients[1] = ''
        keyword = ',素食'

    ai_input = "提供一道用" + ingredients[0] + keyword + ingredients[1] + "烹飪的料理，味道要" \
            + ingredients[2] +"料理名稱放在全文最前面"

    print(ai_input)

    debug = False

    if not debug:
        response = client.responses.create(
            model="gpt-4.1-mini",
            input=ai_input
        )

        return response.output_text

    return 'demo菜色\ndemo作法'