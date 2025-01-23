from datetime import datetime
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from todo.models import TODOO
from django.contrib.auth.decorators import login_required
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.core.validators import MaxLengthValidator


# SignUp Function Code
@csrf_exempt
def signup(request):
    if request.method == 'POST':
        try:
            body = json.loads(request.body.decode('utf-8'))
            username = body.get('username')
            email = body.get('email')
            password = body.get('password')

            if not (username and email and password):
                return JsonResponse({"error": "Missing required fields."}, status=400)
            
            max_lenght = 20
            if len(username) > max_lenght:
                return JsonResponse({"error": f"username must not exceed {max_lenght} characters."}, status=400)

            if User.objects.filter(email=email).exists():
                return JsonResponse({"error": "Email already exists."}, status=400)

            my_user = User.objects.create_user(username=username, email=email, password=password)
            my_user.save()

            return JsonResponse({
                "user": {
                    "username": username,
                    "email": email,
                    "password": password
                }
            }, status=201)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format."}, status=400)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

# Login Function Code        
@csrf_exempt
def user_login(request):
    if request.method == 'POST':
        try:
            body = json.loads(request.body.decode('utf-8'))
            username = body.get('username')
            password = body.get('password')

            if not (username and password):
                return JsonResponse({"error": "Missing required fields."}, status=400)

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return JsonResponse({
                    "user": {
                        "username": username
                    }
                }, status=200)
            else:
                return JsonResponse({"error": "Invalid credentials."}, status=401)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format."}, status=400)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

# Create Todo Function Code
@csrf_exempt
@login_required
def createTodo(request):
    if request.method == 'POST':
        try:
            body = json.loads(request.body.decode('utf-8'))
            title = body.get('title')

            if not title:
                return JsonResponse({"error": "Title is required."}, status=400)

            max_length = 10
            if len(title) > max_length:
                return JsonResponse({"error": f"Title must not exceed {max_length} characters."}, status=400)

            try:
                MaxLengthValidator(max_length)(title)
            except ValidationError as e:
                return JsonResponse({"error": e.message}, status=400)

            user = request.user

            new_todo = TODOO.objects.create(title=title, user=user)

            return JsonResponse({
                "todo": {
                    "srno": new_todo.srno,
                    "title": new_todo.title
                }
            }, status=201)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON data."}, status=400)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid HTTP method."}, status=405)

# List Todos Function Code
@login_required
def listTodo(request):
    if request.method == 'GET':
        try:
            todos = TODOO.objects.filter(user=request.user)

            todos_data = [
                {
                    "srno": todo.srno,
                    "title": todo.title
                }
                for todo in todos
            ]

            return JsonResponse({
                "todos": todos_data
            }, status=200)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

# Delete Todo Function Code
@csrf_exempt
@login_required
def deleteTodo(request, srno):
    if request.method == 'DELETE':
        try:
            todo = TODOO.objects.filter(srno=srno, user=request.user).first()
            
            if not todo:
                return JsonResponse({"error": "Todo Not Found"}, status=404)

            todo.delete()

            return JsonResponse({"success": f"Todo with srno {srno} deleted successfully."}, status=200)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

# Update Todo Function Code
@csrf_exempt
@login_required
def updateTodo(request, srno):
    if request.method == 'PUT':
        try:
            todo = TODOO.objects.filter(srno=srno, user=request.user).first()
            
            if not todo:
                return JsonResponse({'error': 'Todo Not Found'}, status=404)
            
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
        
        try:
            data = json.loads(request.body)
            title = data.get('title')

            if not title:
                return JsonResponse({'error': 'Title is required'}, status=400)

            todo.title = title
            todo.save()

            response_data = {
                'srno': srno,
                'title': title,
                'status': todo.status,
                'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            }

            return JsonResponse(response_data, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)