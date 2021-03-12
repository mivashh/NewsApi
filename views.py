from django.shortcuts import render
from django.http import HttpResponse,HttpResponseBadRequest
from .models import NewsStories,Author
from django.views.decorators.csrf import csrf_exempt


import json
from datetime import datetime
# Create your views here.
global authorname
@csrf_exempt
def Login_view(request):
    if (request.method=='POST'):
        #retrieving the credentials of the user
        username= request.POST.get('username')
        password= request.POST.get('password')
        #retrieving the asked username and password
        #If username or password does not exist in the Author object set them to None
        try :
            field_username=Author.objects.get(username=username).username
            field_password=Author.objects.get(password=password).password
        except Author.DoesNotExist:
            field_password= None
            field_username= None


        #checking if the credentials provided are correct
        if field_password==password and field_username==username:

            #saving the author as a global variable to re-use it for posting
            global authorname
            authorname=field_username

            response=HttpResponse()
            response['Content-Type']='text/plain'
            response.content='\n Welcome to the news agency Api '+authorname
            response.status_code=200
            response.reason_phrase='OK'
            return (response)

        #If the user provides wrong credentials
        else:
            response=HttpResponse()
            response['Content-Type']='text/plain'
            response.content='\n Incorrect Username or Password '
            response.status_code=404
            response.reason_phrase='Not found'
            return(response)

    else:
        bad_response=HttpResponseBadRequest()
        bad_response['Content-Type']='text/plain'
        bad_response.content='\n Something went wrong (maybe not using post request)'

        return (bad_response)

@csrf_exempt
def Logout_view(request):
    if (request.method=='POST'):

        response=HttpResponse()
        response['Content-Type']='text/plain'
        response.content='\n Logging you out...'
        response.status_code=200
        response.reason_phrase='OK'

        return (response)
@csrf_exempt
def PostStory(request):
    if (request.method=='POST'):

        #collecting information from the user for creating new story
        payload=json.loads(request.body)
        headline=payload['headline']
        category=payload['category']
        region=payload['region']
        details=payload['details']

        #Setting the information for the creation of the new story
        NewsStory=NewsStories(headline=headline,category=category,region=region,details=details,author=authorname)
        try:
            #if we reached this point everything is correct and
            #we should save the new story into our database
            NewsStory.save()
            response=HttpResponse()
            response['Content-Type']='text/plain'
            response.status_code=201
            response.reason_phrase='Created'
        except:
            response=HttpResponseBadRequest()
            response['Content-Type']='text/plain'
            response.content='Something went wrong'
            response.status_code=503
            response.reason_phrase='Error'

        return (response)
    else:
        bad_response=HttpResponseBadRequest()
        bad_response['Content-Type']='text/plain'
        bad_response.content='\n Something went wrong (maybe post using get request)'

        return (bad_response)

def GetStory(request):
    if (request.method=='GET'):
        #get the list of stories from the database

        payload1=json.loads(request.read())
        category=payload1['story_cat']
        region=payload1['story_region']
        date3=payload1['story_date']
        print(category)
        print(region)
        print(date3)
        stories_list=NewsStories.objects.all().values('id','headline','category','region','author','date','details')

        #collect the list items and put a new list with appropriate json names as pre requirements
        the_list=[]

        for record in stories_list:

            date1=str(record['date'])
            chop=len(date1.split()[-1])+1
            date1=date1[:-chop]
            #Changing the format of date to dd/mm/YY
            formatDate=datetime.strptime(date1,"%Y-%m-%d").strftime("%d/%m/%Y")

            #checking if the requested fileds match in the database
            if record['category']==category and record['region']==region and formatDate==date3:
                item={'key': record['id'] ,'headline': record['headline'] , 'story_cat':record['category'], 'story_region':record['region'] , 'author':record['author'] , 'story_date':formatDate ,'story_details':record['details']}
                the_list.append(item)

            if category=='*' and region=='*' and date3=='*':
                item={'key': record['id'] ,'headline': record['headline'] , 'story_cat':record['category'], 'story_region':record['region'] , 'author':record['author'] , 'story_date':formatDate ,'story_details':record['details']}
                the_list.append(item)

            if record['category']==category and region=='*' and date3=='*':
                item={'key': record['id'] ,'headline': record['headline'] , 'story_cat':record['category'], 'story_region':record['region'] , 'author':record['author'] , 'story_date':formatDate ,'story_details':record['details']}
                the_list.append(item)

            if category=='*' and record['region']==region and date3=='*':
                item={'key': record['id'] ,'headline': record['headline'] , 'story_cat':record['category'], 'story_region':record['region'] , 'author':record['author'] , 'story_date':formatDate ,'story_details':record['details']}
                the_list.append(item)

            if category=='*' and region=='*' and  formatDate==date3:
                item={'key': record['id'] ,'headline': record['headline'] , 'story_cat':record['category'], 'story_region':record['region'] , 'author':record['author'] , 'story_date':formatDate ,'story_details':record['details']}
                the_list.append(item)

            if category=='*' and record['region']==region and  formatDate==date3:
                item={'key': record['id'] ,'headline': record['headline'] , 'story_cat':record['category'], 'story_region':record['region'] , 'author':record['author'] , 'story_date':formatDate ,'story_details':record['details']}
                the_list.append(item)

            if  record['category']==category and record['region']==region and  date3=='*':
                item={'key': record['id'] ,'headline': record['headline'] , 'story_cat':record['category'], 'story_region':record['region'] , 'author':record['author'] , 'story_date':formatDate ,'story_details':record['details']}
                the_list.append(item)

            if  record['category']==category and region=='*' and  formatDate==date3:
                item={'key': record['id'] ,'headline': record['headline'] , 'story_cat':record['category'], 'story_region':record['region'] , 'author':record['author'] , 'story_date':formatDate ,'story_details':record['details']}
                the_list.append(item)


        if len(the_list)==0:
            response=HttpResponse()
            response['Content-Type']='text/plain'
            response.content='\n This story does not exist try a different one '
            response.status_code=404
            response.reason_phrase='Not found'
            return(response)

            print(formatDate)



        #creating the json response payload
        payload={'stories':the_list}

        #creating and returning a normal response
        response=HttpResponse(json.dumps(payload))
        response['Content-Type']='application/json'
        response.status_code=200

        return response

@csrf_exempt
def DeleteStory(request):
    #receiving the story_key from the user
    payload=json.loads(request.body)
    story_key=payload['story_key']

    #retriving all the ids from the list
    storylist=list(NewsStories.objects.all().values_list('id'))

    #creating and empty string to parse the ids in so i can indlude them in the repsonse
    StringStory=" ".join(map(str,storylist))

    #Checking if the id exists in our database
    try :
        obj=NewsStories.objects.get(id=story_key)
    except NewsStories.DoesNotExist:
        obj=None


    #if the id does not exists send status code 503 and reasoning
    if obj==None:
        bad_response=HttpResponseBadRequest()
        bad_response['Content-Type']='text/plain'
        bad_response.content='\n This Key story does not exist try a different one : Available story_key '+ StringStory
        bad_response.status_code=503
        return (bad_response)

    if request.method=='POST':

        #delete object
        obj.delete()
        response=HttpResponse()
        response['Content-Type']='text/plain'
        response.content='\n Story deleted'
        response.status_code=201
        response.reason_phrase='OK'
        return (response)

    #In case the user tries a different reqeust from post
    else:
        bad_response=HttpResponseBadRequest()
        bad_response['Content-Type']='text/plain'
        bad_response.content='\n Something went wrong (maybe post using get request)'
