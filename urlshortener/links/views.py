from datetime import datetime
from urllib.parse import urlparse
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Link
from .serializers import LinkSerializer
from django.shortcuts import redirect
from rest_framework.views import APIView
from rest_framework.exceptions import NotFound
from django.views import View
from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Link
from django.contrib.auth.decorators import login_required
from .forms import LinkForm


class LinkViewSet(viewsets.ModelViewSet):
    queryset = Link.objects.all()
    serializer_class = LinkSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)



class RedirectLinkView(APIView):
    def get(self, request, short_id):
        try:
            link = Link.objects.get(short_id=short_id)
            link.last_accessed = datetime.now()
            link.save()
            return redirect(link.original_url)
        except Link.DoesNotExist:
            raise NotFound(detail="Short link not found")



def user_dashboard(request):
    if request.user.is_authenticated:
        links = Link.objects.filter(user=request.user)
        return render(request, 'links/dashboard.html', {'links': links})
    else:
        return redirect('login')

from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm

class SignUpView(View):
    def get(self, request):
        form = UserCreationForm()
        return render(request, 'links/signup.html', {'form': form})

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        return render(request, 'links/signup.html', {'form': form})


@login_required
def create_link(request):
    if request.method == 'POST':
        form = LinkForm(request.POST)

        if form.is_valid():
            original_url = form.cleaned_data['original_url']

            short_id = Link.generate_short_id()
            link = Link.objects.create(
                original_url=original_url,
                short_id=short_id,
                user=request.user
            )


            # Возвращаем результат в формате JSON с полным URL
            return JsonResponse({
                'short_id': short_id,
                'original_url': original_url
            })
        else:
            return JsonResponse({'error': 'URL не может быть пустым'}, status=400)
    else:
        form = LinkForm()

    return render(request, 'links/create_link.html', {'form': form})