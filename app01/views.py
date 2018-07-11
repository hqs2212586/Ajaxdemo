from django.shortcuts import render,HttpResponse

# Create your views here.

def index(request):

    return render(request, "index.html")


def test_ajax(request):

    print(request.GET)   # <QueryDict: {'a': ['1'], 'b': ['2']}>
    return HttpResponse("Hello kobe!")


def cal(request):
    print(request.POST)  # <QueryDict: {'n1': ['12'], 'n2': ['23']}>
    n1 = int(request.POST.get("n1"))
    n2 = int(request.POST.get("n2"))
    ret = n1 + n2

    return HttpResponse(ret)


# 引入User表
from app01.models import User


def login(request):

    print(request.POST)  # <QueryDict: {'user': ['HQS'], 'pwd': ['123']}>
    user = request.POST.get("user")
    pwd = request.POST.get("pwd")

    print(User.objects.filter(name=user, pwd=pwd))
    """
    在数据库查询失败：<QuerySet []>
    在数据库查询对应数据：<QuerySet [<User: User object (1)>]>
    """
    user = User.objects.filter(name=user, pwd=pwd).first()
    print(user)  # User object (1)

    res = {"user": None, "msg": None}
    if user:
        # user有值的情况
        res["user"] = user.name
    else:
        res["msg"] = "username or password wrong!"

    import json   # 运用json把python的字典转换为json字符串进行传递
    return HttpResponse(json.dumps(res))  # HttpResponse方法只能传递字符串


def file_put(request):

    if request.method == "POST":
        print("body", request.body)    # 请求报文的请求体
        # print(request.GET)     # GET请求数据
        print("post", request.POST)    # POST请求数据：<QueryDict: {'user': ['yuan']}>
        """
        只有contentType=urlencoded的时候，request.POST才会有数据：
        body b'a=1&b=2'
        post <QueryDict: {'a': ['1'], 'b': ['2']}>
        
        contentType:"application/json"  情况下输出：
        body b'{"a":1,"b":2}'
        post <QueryDict: {}>
        """


        print(request.FILES)   # 上传的文件数据：<MultiValueDict: {'avatar': [<InMemoryUploadedFile: bojie.jpg (image/jpeg)>]}>

        """
        body b'------WebKitFormBoundary7aWZK41JdkpQEnfA\r\nContent-Disposition: form-data; name="user"\r\n\r\nyuan\r\n------WebKitFormBoundary7aWZK41JdkpQEnfA\r\nContent-Disposition: form-data; name="avatar"; filename="bojie.jpg"\r\nContent-Type: image/jpeg.....
        post <QueryDict: {'user': ['yuan']}>
        <MultiValueDict: {'avatar': [<InMemoryUploadedFile: bojie.jpg (image/jpeg)>]}>
        """

        file_obj = request.FILES.get("avatar")
        with open(file_obj.name, "wb") as f:
            for line in file_obj:
                f.write(line)

        return HttpResponse("OK")

    return render(request, "file_put.html")

