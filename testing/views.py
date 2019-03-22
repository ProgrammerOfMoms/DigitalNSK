from django.shortcuts import render
from django.contrib.auth.signals import user_logged_in
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_jwt.utils import jwt_payload_handler, jwt
from rest_framework.schemas import ManualSchema
from rest_framework.renderers import JSONRenderer
from DigitalNSK import settings
from .models import *
from .serialize import *

import json

def test2(data, user):
    if "answers" in data:
        answers = data["answers"]
        test = Test.objects.get(mode = 2)
        groups = test.groups.all()
        nameOfGroups = []
        val = [0] * len(groups)
        for group in nameOfGroups:
            nameOfGroups.append(group.name)
        for answer in data["answers"]:
            val[answer-1] = val[answer-1] + 1

        maximum = max(val)
        maxI = val.index(maximum)
        if val.count(maximum) == 1:
            res = {
                "additional": False,
                "types": nameOfGroups,
                "values": val
            }
        else:
            types = [maxI]
            for  i in range(maxI+1,len(groups)):
                if maximum == val[i]:
                    types.append(i)
            addQuestion = test.additionalQuestion
            mas = []
            answers = addQuestion.answers.all()
            for item in types:
                group = {
                    "types": answers[item].content,
                    "group": answers[item].group
                }
                mas.append(group)
            res = {
                "additional": True,
                "values": val,
                "types": nameOfGroups,
                "description": addQuestion.content,
                "questions": mas
            }
        result = ResultOfTest.objects.create(competence = str(res), test = test)
        user.passedTests.add(result)
        return Response(data = res, status = status.HTTP_200_OK)
    else:
        res = {"error": "Отсутствуют необходимые поля"}
        return Response(data = res, status = status.HTTP_400_BAD_REQUEST)

"""
def test1(request):
    if request.method == "GET":
        try:
            res = {
                "status": True,
                "name": "Предпочитаемая сфера",
                "desciption": "Ниже представлены мысленные эксперименты касательно разных направлений деятельности. Пожалуйста укажите, какой из двух вариантов ответа наиболее предпочтителен для вас. Возможно, некоторые направления покажутся вам равнозначно интересными или же, напротив, вы не будете заинтересованы ни в одном из них. В таком случае всё же отдайте предпочтение одному из вариантов.",
                "questions": [
                    {
                        "content": "В моем городе проходит одновременно две масштабные конференции с зарубежными специалистами по двум направлениям. Зная, что я могу посетить лишь одну из них, остановлю свой выбор на:",
                        "answers":[
                            {"content": "конференция «Кибербезопасность в каждый дом. Опыт и перспективы»", "group": 4},
                            {"content": "конференция «Природные ресурсы: экослед и жизнь взаймы»", "group": 2}
                        ]
                    },
                    {
                        "content": "В своей работе я бы хотел использовать цифровые технологии в качестве:",
                        "answers":[
                            {"content": "площадки для профессионального взаимодействия с другими людьми", "group": 1},
                            {"content": "системы, которую я буду настраивать и совершенствовать", "group": 4}
                        ]
                    },
                    {
                        "content": "Благотворительный фонд «Ритм будущего» предоставил вам выбор в том, как распорядиться крупной суммой. Вы выберете профинансировать проект:",
                        "answers":[
                            {"content": "«Онлайн-образование для стран третьего мира: дай ребенку шанс»", "group": 1},
                            {"content": "«Социализация роботов-нянь в дом малютки как фактор увеличения выживаемости младенцев»", "group": 5}
                        ]
                    },
                    {
                        "content": "Я бы хотел внести вклад в развитие человечества в области:",
                        "answers":[
                            {"content": "разработки программы психологической реабилитации военнослужащих с помощью искусственного интеллекта", "group": 5},
                            {"content": "улучшения медицинской диагностики с помощью Big Data", "group": 2}
                        ]
                    },
                    {
                        "content": "В свободное время мне скорее было бы интересно прочитать новость:",
                        "answers":[
                            {"content": "о создании прототипа искусственной руки для помощи пациентам, потерявшим конечность", "group": 3},
                            {"content": "о снижении производственных рисков за счет переструктурирования иерархии взаимоотношений внутри компании", "group": 1}
                        ]
                    },
                    {
                        "content": "Если бы мне предложили сделать доклад с возможностью выбора темы, я бы скорее остановился на:",
                        "answers":[
                            {"content": "«Криптовалюты: что нужно знать каждому»", "group": 4},
                            {"content": "«Эмоциональный интеллект: методы развития у взрослых людей»", "group": 5}
                        ]
                    },
                    {
                        "content": "В одно и то же время в школе проходят внеурочные занятия по двум направлениям. Я определенно выберу занятия по:",
                        "answers":[
                            {"content": "робототехнике", "group": 3},
                            {"content": "разработке веб-приложений", "group": 4}
                        ]
                    },
                    {
                        "content": "Думаю, что в общеобразовательную программу было бы полезно добавить курсы по:",
                        "answers":[
                            {"content": "развитию навыков публичных выступлений и ведения переговоров", "group": 5},
                            {"content": "основам виртуальной реальности как ресурса для самообразования", "group": 3}
                        ]
                    },
                    {
                        "content": "Я бы с интересом побыл стажером в компании, которая занимается:",
                        "answers":[
                            {"content": "продвижением социальных проектов по технологии краудфандинга", "group": 1},
                            {"content": "разработкой роботизированного комбайна для сбора урожая пшеницы", "group": 2}
                        ]
                    },
                    {
                        "content": "Местная газета поручила вам подготовить статью о современных технологиях. Для сбора необходимых сведений вам выдадут пропуск в любую компанию. Вы, конечно же, выберете посетить:",
                        "answers":[
                            {"content": "первое в мире здание, снабжаемое энергией с помощью морских водорослей","group": 2},
                            {"content": "лабораторию по разработке системы «умный город» для восточного мегаполиса", "group": 3}
                        ]
                    }
                ]
            }
            return JsonResponse(res)
        except:
            return JsonResponse({"status": False, "error": "что-то пошло не так"})
    elif request.method == "POST":
        #try:
            # data = json.loads(request.body.decode("utf-8"))
            # if "answers" in data:
            #     _types = [
            #             "Социальное управление",
            #             "Естественные науки и биотехнологии",
            #             "Современная инженерия",
            #             "IT-компетенции",
            #             "Гуманитарные технологии, наука и искусство"
            #         ]
            #     values = [1,4,2,1,0]
            #     for answer in data["answers"]:
            #         values[answer-1] = values[answer-1] + 1
            #     maximum = values[0]
            #     maxI = 0
            #     lenght = len(values)
            #     for i in range(lenght):
            #         if maximum < values[i]:
            #             maximum = values[i]
            #             maxI = i
                types = [maxI+1]
                for  i in range(maxI+1,lenght):
                    if maximum == values[i]:
                        types.append(i+1)
                if len(types) == 1:
                    res = {
                        "status": True,
                        "additional": False,
                        "types": _types,
                        "values": values
                    }
                else:
                    mas = [
                        "координировать и регулировать людей, их группы и коллективы с целью совершенствования и развития общества, достижения стоящих перед людьми задач (области применения — правовые основы цифровой трансформации, регулярный менеджмент, онлайн-образование и др.)",
                        "изучать взаимосвязи живых организмов и законы естественных наук, использовать знания о наземных и водных биологических системах для улучшения технологических инноваций (области применения — экологические инициативы, цифровое сельское хозяйство, биоинженерия и др.)",
                        "решать инженерные задачи — создавать и улучшать технические устройства, механизмы, оборудование (области применения — искусственный интеллект, цифровая среда обитания, индустрия 4 и др.)",
                        "заниматься IT-сферой — создавать, обрабатывать, хранить, защищать и передавать информацию с помощью вычислительной техники (области применения — веб-разработка, кибербезопасность, цифровые каналы связи и др.)",
                        "заниматься изучением непосредственной коммуникации с целью решения социальных проблем в условиях цифрового мира (области применения — социализация роботов, data scientist, психология и др.)"
                    ]
                    jMas = []
                    for item in types:
                        group = {
                            "types": mas[item-1],
                            "group": item,
                        }
                        jMas.append(group)
                    res ={
                        "status": True,
                        "additional": True,
                        "values": values,
                        "types": _types,
                        "description": "Внимание! У вас выявлено равное предпочтение по двум сферам. Пожалуйста, ответьте на дополнительный вопрос, чтобы определить ваше дальнейшее направление участия в проекте. В условиях цифровой экономики вас больше привлекает:",
                        "questions": jMas
                    }
                return JsonResponse(res)
            else:
                return JsonResponse({"status": False, "error": "Неверный запрос"})
        #except:
        #    return JsonResponse({"status": False, "error": "что-то пошло не так"})
def additional(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body.decode("utf-8"))
            if "values" in data:
                
                return JsonResponse(res)
            else:
                return JsonResponse({"status": False, "error": "Неверный запрос"})
        except:
            return JsonResponse({"status": False, "error": "что-то пошло не так"})
def resultOfAdditional(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body.decode("utf-8"))
            if "answer" in data and "values" in data:
                mas = [
                    "Социальное управление",
                    "Естественные науки и биотехнологии",
                    "Современная инженерия",
                    "IT-компетенции",
                    "Гуманитарные технологии, наука и искусство"
                ]
                values = data["values"]
                values[data["answer"]-1] = values[data["answer"]-1] + 1
                return JsonResponse({"status": True, "types": mas, "values": values})
            else:
                return JsonResponse({"status": False, "error": "Неверный запрос"})
        except:
            return JsonResponse({"status": False, "error": "что-то пошло не так"})
"""

def test1(data, user):
    if "answers" in data:
        test = Test.objects.get(mode = 1)
        types = test.groups.all()
        val = [0] * len(types)
        maximum = [0] * len(types)
        for answer in data["answers"]:
            group = Group.object.get(id = answer)
            #говно ебанное
            val[i] = val[i] + answer["group"]
            maximum[i] = maximum[i] + 1
        res = {
            "status": True,
            "types": types,
            "values": val,
            "max": maximum
        }
        result = ResultOfTest.objects.create(competence = str(res), test = test)
        user.passedTests.add(result)
        return Response(data = res, status = status.HTTP_200_OK)
    else:
        res = {"error": "Отсутствуют необходимые поля"}
        return Response(data = res, status = status.HTTP_400_BAD_REQUEST)

def test3(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body.decode("utf-8"))
            mas = [
                    "Социальное управление",
                    "Естественные науки и биотехнологии",
                    "Современная инженерия",
                    "IT-компетенции",
                    "Гуманитарные технологии, наука и искусство"
                ]
            if "test1" in data:
                test1 = data["test1"]
                if test1 == mas[0]:
                    res = [
                        "Государственное регулирование цифровой экономики",
                        "Цифровое право и коллизии",
                        "Технологии общественного равития",
                        "Digital-торговля",
                        "Сервисное мышление",
                        "Digital-логистика",
                        "Комплексное решение проблем",
                        "Критическое мышление",
                        "Оценка и принятие решений",
                        "Бизнес-аналитика",
                        "Управление командами",
                        "Управление на основе данных (CDO)",
                        "Цифровой маркетинг",
                        "Экономические модели",
                        "Управление проектами",
                        "Технологии краудфандинга",
                        "Онлайн-образование",
                        "Организация производства кастомизированных продуктов"
                    ]
                elif test1 == mas[1]:
                    res = [
                        "Синтетические биоматериалы",
                        "Производящие микроорганизмы",
                        "Digital-решения для биотехнологий",
                        "Технологии защиты окружающей среды",
                        "Эффективное использование природных ресурсов",
                        "Цифровая диагностика и большие данные для медицины",
                        "Биочипы",
                        "Технология управления здоровьем человека",
                        "Индивидуальные лечебные траектории",
                        "Цифровое сельское хозяйство",
                        "Интернет животных",
                        "Восстановление экосистем"
                    ]
                elif test1 == mas[2]:
                    res = [
                        "Беспилотные технологии",
                        "Машинное обучение",
                        "Виртуальная/дополненная реальность",
                        "Умный дом",
                        "Умный город",
                        "ГИС-технологии",
                        "Интернет вещей",
                        "Промышленный дизайн",
                        "Системный инжиниринг",
                        "Методы решения инженерных задач",
                        "Теория инноватики",
                        "Цифровые двойники",
                        "Индустриальная робототехника",
                        "Беспилотный транспорт",
                        "Новые материалы и аддитивные технологии",
                        "Тенологии внедрения и обслуживания новых технологий",
                    ]
                elif test1 == mas[3]:
                    res = [
                        "Веб-разработка",
                        "Теническое письмо",
                        "Системное администрирование и настройка сетей",
                        "Сетевые протоколы",
                        "Социальные сети",
                        "Глобальные сети передачи данных и каналы связи",
                        "Облачные технологии",
                        "Каналы связи",
                        "Защита персональных данных",
                        "Менеджмнт ИБ",
                        "Технологии блокчейн",
                        "Криптовалюты",
                        "Создание ценностей внутри цифрового мира"
                    ]
                elif test1 == mas[4]:
                    res = [
                        "Трансфессиональность и видение целого",
                        "Психология",
                        "Data scientist",
                        "Искусственный интеллект",
                        "Социализация роботов",
                        "Нейросети",
                        "Филология, чувство языка",
                        "Дизайн-мышление",
                        "Эмоциональный интеллект",
                        "Генерация идей/креативность",
                        "Ведение переговоров",
                        "Навыки публичных выступлений",
                        "Иностранный язык",
                        "Мультикультурализм/толерантность",
                        "Культурный запас человечества",
                        "Новые знаковые системы",
                        'Технологии "взаимодействия с человеком"'
                    ]
                return JsonResponse({
                    "status": True, 
                    "description": "Вам предлагается оценить свои возможности по каждому направлению на данный момент. Выберите соответственно 2, 1 или 0 согласно следующей шкале: 2 — имею практический опыт в данном направлении 1 — владею теоретическими знаниями / имею представление, как это используется на практике 0 — о данном направлении мне неизвестно ничего / известно очень мало. Опирайтесь на ваши возможности на данный момент времени. Наш проект поможет вам в приобретении недостающих знаний.", 
                    "test":res
                })
            else:
                return JsonResponse({"status": False, "error": "Неверный запрос"})
        except:
            return JsonResponse({"status": False, "error": "что-то пошло не так"})

def resultOfTest3(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body.decode("utf-8"))
            if "answers" in data:
                sum = 0
                for answer in data["answers"]:
                    sum = sum + answer
                res = sum * 5 / len(data["answers"])
                return JsonResponse({"status": True, "result": res})
            else:
                return JsonResponse({"status": False, "error": "Неверный запрос"})
        except:
            return JsonResponse({"status": False, "error": "что-то пошло не так"})

class Testing(APIView):
    permission_classes = (AllowAny,)

    def get(self,request):
        try:
            _type = request.GET["type"]
            test = Test.objects.get(mode = _type)
            serializer = TestSerializer(test)
            data = serializer.data
            res = {"id": data["id"]}
            data.pop("id")
            res.update(data)
            return Response(data = res, status = status.HTTP_200_OK)
        except:
            res = {"error": "Неизвестная ошибка"}
            return Response(data = res, status = status.HTTP_400_BAD_REQUEST)

    def post(self,request):
        data = json.loads(request.body.decode("utf-8"))
        if "HTTP_ID" in request.META:
            id = request.META["HTTP_ID"]
            try:
                user = Participant.objects.get(id = id)
                if "type" in data:
                    if data["type"] == 1:
                        return test1(data = data, user = user)
                    elif data["type"] == 2:
                        return test2(data = data, user = user)
                    elif data["type"] == 3:
                        return test3(data = data, user = user)
                    else:
                        res = {"error": "Неизвестный тип теста"}
                        return Response(data = res, status = status.HTTP_400_BAD_REQUEST)
                else:
                    res = {"error": "Не указан тип теста"}
                    return Response(data = res, status = status.HTTP_400_BAD_REQUEST)
            except:
                res = {"error": "Такого пользователя не существует"}
                return Response(data = res, status = status.HTTP_400_BAD_REQUEST)
        else:
            res = {"error": "Не указан id пользователя"}
            return Response(data = res, status = status.HTTP_400_BAD_REQUEST)
            
