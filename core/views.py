from django.shortcuts import render, redirect
from registration.models import user_profile
from django.contrib.auth.models import User

from core.models import chat_history

def add_question_to_users_message(user_id, curr_session_id , question , response):

    curr_user = User.objects.get(id=user_id)

    chat_session = chat_history.objects.get(id = curr_session_id)

    print(f"chat session is {chat_session}")

    if chat_session:
        print(f"{curr_user} posted the message {question} and the history is {chat_session.question_list} : {chat_session.answer_list}")
        
        if chat_session.question_list == '':
            print('EMPTY QUESTION LIST ... NEW .....')
            chat_session.question_list = chat_session.question_list + str(question)
            chat_session.answer_list = chat_session.answer_list + str(response)
            chat_session.save()
        else:
            chat_session.question_list = chat_session.question_list + '||' + str(question)
            chat_session.answer_list = chat_session.answer_list + '||' + str(response)
            chat_session.save()
    else:
        print('No chat session found')
        print(f"{curr_user} posted the message {question} and No previous chat session found")
        chat_session = chat_history.objects.create(user=curr_user,question_list=str(question) , answer_list = str(response))
        print(f"chat session created successfully {chat_session}" )


    print('Exits')



# Create your views here.
def home(request,chatid = None):
    
    if request.user.is_authenticated:
        curruser = request.user
        print('Enters home with authenticated user : ' , curruser)
        # return render(request,'core/homepage.html',{'curr_user' : curruser})
    else:
        # return render(request,'core/homepage.html')
        print('Enters home with no authenticated user ... Redirecting to Signin page ...')
        return redirect('registration:signin')


    if request.method == 'POST':

        print('Enters core_home POST with parameters ' , request.POST )

        user_question = request.POST.get("user_question")
        curr_user = request.user
        curr_session_id = request.POST.get("curr_session_id" , None)

        print(f"{curr_user} asked the question {user_question} and the session is {curr_session_id}")

        import openai
        
        
        import os
        os.environ["OPENAI_API_KEY"] = "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"

        from openai import OpenAI
        client = OpenAI(api_key = os.environ["OPENAI_API_KEY"])

        # Set the prompt.
        messages_lst = []


        # print('The summarised contennt is ' , summarised_content)

        curr_user = request.user

        # chat_session = chat_history.objects.filter(user__id=curr_user.id).first()
        if curr_session_id:
            chat_session = chat_history.objects.get(id = curr_session_id)
        else:
            print('Error')
            return redirect('https://www.google.com')


        if chat_session:
            question_list = chat_session.get_chat_questions() or None   
            answer_list = chat_session.get_chat_answers() or None
            question_answer_list = zip(question_list, answer_list)
        else:
            question_list = None
            answer_list = None
            question_answer_list = None


        messages_lst.append({"role": "user", "content": 'あなたは優れたビジネス アシスタントであり、質問を受け、コンテンツを読んで答えることができます。 内容に基づいてのみ返信でき、自分で返信することはできません。 経験豊富で丁寧なチャットボットのように、要件に応じて短、中、または長文で回答してください。' })
        
        if question_answer_list:
            for ques,ans in question_answer_list:
                messages_lst.append({"role": "user", "content": ques})
                messages_lst.append({"role": "assistant", "content": ans})
        

        messages_lst.append({"role": "user", "content": user_question })


        print('final message list is ' , messages_lst)

        response = client.chat.completions.create(
        model="gpt-4-1106-preview",
        messages=messages_lst
        )

        # print(response)
        print(response.choices[0].message.content)

        gpt_response = response.choices[0].message.content


        # 

        add_question_to_users_message(curr_user.id , curr_session_id , str(user_question) , str(gpt_response))

        # 

        curr_user = request.user

        chat_session = chat_history.objects.get(id = curr_session_id)

        if chat_session:
            question_list = chat_session.get_chat_questions() or None   
            answer_list = chat_session.get_chat_answers() or None
            question_answer_list = zip(question_list[:-1], answer_list[:-1])
        else:
            question_list = None
            answer_list = None
            question_answer_list = None

        


        print(f" Question list is {question_list} and the answer list is {answer_list} and zipped is {question_answer_list}")

        # return JsonResponse({'connection': 'Connected to GPT'}, status=200)


        curr_user = request.user
    
        chat_session = chat_history.objects.get(id = curr_session_id)

        if chat_session:
            question_list = chat_session.get_chat_questions() or None   
            answer_list = chat_session.get_chat_answers() or None
            question_answer_list = zip(question_list[:-1], answer_list[:-1])
        else:
            question_list = None
            answer_list = None
            question_answer_list = None

        users_sessions = chat_history.objects.filter(user__id=curr_user.id).order_by('-created')

        print(f'users_session values are ' , users_sessions)

        if(question_list[0] == ''):
            print('JUST CREATED EMPTY')
            question_answer_list = None
            question_list = None
            answer_list = None


        context = {
            'gpt_response' : gpt_response,
            'user_question' : user_question,
            'question_answer_list' : question_answer_list,
            'curr_user' : curr_user,
            'users_sessions' : users_sessions,
            'chat_session' : chat_session

        }

        return render(request, 'core/homepage.html' , context = context)

    curr_user = request.user
    
    chat_session = chat_history.objects.filter(user__id=curr_user.id).order_by('-created')[0]

    try:
        print('TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTOOOOOOOOOOOOOOOOOOOOOOOOOOOO')
        if chatid:
            chat_session = chat_history.objects.get(id=int(chatid))
    except Exception as e:
        print(e)

    if chat_session:
        question_list = chat_session.get_chat_questions() or None   
        answer_list = chat_session.get_chat_answers() or None
        
        question_answer_list = zip(question_list, answer_list)
    else:
        question_list = None
        answer_list = None
        question_answer_list = None

    print(f" Question list in get is {question_list} and the answer list is {answer_list} and zipped is {question_answer_list}")

    users_sessions = chat_history.objects.filter(user__id=curr_user.id).order_by('-created')

    print(f'users_session values are ' , users_sessions)

    print('home passed param is ' , chatid)

    if(question_list[0] == ''):
        print('JUST CREATED EMPTY')
        question_answer_list = None
        question_list = None
        answer_list = None

    context = {
        'curr_user' : curr_user,
        'question_list' : question_list,
        'answer_list' : answer_list,
        'question_answer_list' : question_answer_list,
        'users_sessions' : users_sessions,
        'chat_session' : chat_session
    }

    return render(request, 'core/homepage.html' , context = context)



def create_new_chat(request):
    print('Enters create new chat ... CREATING NEW CHAT')

    
    new_chat_history = chat_history.objects.create(
        user = request.user,
    )

    print('new chat is ' , new_chat_history , ' and the ID is ' , new_chat_history.id)

    return redirect('core:home_with_parameters', chatid=new_chat_history.id)


def change_session_name(request):

    if request.method == "POST":
        print('Enters change session name POST with parameters ' , request.POST)

        new_value = request.POST.get('change_session_name' , None)
        old_Session_id = request.POST.get('change_session_name_id' , None)



        chat_history_instance =  chat_history.objects.get(id = int(old_Session_id))
        chat_history_instance.chat_history_title = new_value
        chat_history_instance.save()

        print('New value and the session ID is ' , new_value , old_Session_id)

        return redirect('core:home')
    
    else:
        return redirect('core:home')



def errorpage(request , error_text = None):
    print('Enters Errorpage. Error text is ' , error_text)

    context = {
        'error_text' : error_text
    }

    return render(request, 'errorpage/errorpage.html' , context = context)


def custom_page_not_found_view(request, exception):

    context = {
        'error_text' : '404 Error'
    }

    return render(request, 'errors/404.html', context = context, status=404)

def custom_error_view(request):
    
    context = {
        'error_text' : '500 Error'
    }

    return render(request, 'errors/500.html', context = context, status=500)

def custom_permission_denied_view(request, exception):

    context = {
        'error_text' : '403 Error'
    }

    return render(request, 'errors/403.html', context = context, status=403)

def custom_bad_request_view(request, exception):

    context = {
        'error_text' : 'Bad Request Error'
    }

    return render(request, 'errors/400.html', context = context, status=400)