import os
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.db import transaction
from .models import Project, EditorElement
from .forms import ProjectForm



def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

@login_required
def projects(request):
    if request.user.is_authenticated:
        user_projects = Project.objects.filter(owner=request.user)
    else:
        user_projects = []
    return render(request, 'projects/projects.html', {'projects': user_projects})

@login_required
def add_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = request.user
            project.save()
            return redirect('projects')
    else:
        form = ProjectForm()
    return render(request, 'projects/add_project.html', {'form': form})

@login_required
def delete_project(request, pk):
    project = get_object_or_404(Project, pk=pk, owner=request.user)

    if request.method == 'POST':
        with transaction.atomic():
            for element in project.elements.all():
                if element.type in ['image', 'svg'] and element.file:
                    file_path = element.file.path
                    if os.path.isfile(file_path):
                        os.remove(file_path)
            project.delete()
        return redirect('projects')

    return render(request, 'projects/delete_confirm.html', {'project': project})

@login_required
def update_project_title(request, pk):
    project = get_object_or_404(Project, pk=pk, owner=request.user)
    new_title = request.POST.get('title', '').strip()
    if new_title:
        project.title = new_title
        project.save()
        return JsonResponse({'success': True, 'title': new_title})
    return JsonResponse({'success': False, 'error': 'Title cannot be empty'})

@login_required
def project_editor(request, pk):
    project = get_object_or_404(Project, pk=pk, owner=request.user)
    return render(request, 'projects/editor.html', {
        'project': project,
    })


@login_required
def add_text_element(request, pk):
    project = get_object_or_404(Project, pk=pk, owner=request.user)
    text = request.POST.get('text', '').strip()

    if text:
        element = EditorElement.objects.create(
            project=project,
            type='text',
            text_content=text
        )
        element_data = {
            'id': element.id,
            'type': element.type,
            'text_content': element.text_content,
            'position_x': element.position_x,
            'position_y': element.position_y,
            'width': element.width,
            'height': element.height
        }
        return JsonResponse({'success': True, 'element': element_data})

    return JsonResponse({'success': False, 'error': 'No text provided'})

@require_POST
@login_required
def upload_editor_file(request, pk):
    project = get_object_or_404(Project, pk=pk, owner=request.user)

    if request.method == 'POST' and request.FILES.get('file'):
        uploaded_file = request.FILES['file']
        if uploaded_file.content_type.startswith('image/'):
            element_type = 'image'
        else:
            return JsonResponse({'success': False, 'error': 'Unsupported file type'})
        element = EditorElement.objects.create(
            project=project,
            type=element_type,
            file=uploaded_file
        )
        element_data = {
            'id': element.id,
            'type': element.type,
            'file_url': element.file.url if element.file else '',
            'position_x': element.position_x,
            'position_y': element.position_y,
            'width': element.width,
            'height': element.height
        }
        return JsonResponse({'success': True, 'element': element_data})

    return JsonResponse({'success': False, 'error': 'No file uploaded'})

@require_POST
@login_required
def update_element_properties(request, element_id):
    try:
        element = EditorElement.objects.get(pk=element_id, project__owner=request.user)

        # Update position if provided
        if 'position_x' in request.POST:
            element.position_x = float(request.POST.get('position_x'))
        if 'position_y' in request.POST:
            element.position_y = float(request.POST.get('position_y'))

        # Update size if provided
        if 'width' in request.POST:
            element.width = float(request.POST.get('width'))
        if 'height' in request.POST:
            element.height = float(request.POST.get('height'))

        element.save()
        return JsonResponse({'success': True})
    except EditorElement.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Element not found'})

@require_POST
@login_required
def delete_editor_element(request, element_id):
    try:
        element = EditorElement.objects.get(pk=element_id, project__owner=request.user)
        if element.type in ['image', 'svg'] and element.file:
            file_path = element.file.path
            if os.path.isfile(file_path):
                os.remove(file_path)
        element.delete()
        return JsonResponse({'success': True})
    except EditorElement.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Element not found'})

