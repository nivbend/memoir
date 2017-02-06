from django.shortcuts import render, redirect
from quotes.models import Board

def index(request):
    if not request.user.is_authenticated:
        return redirect('login')

    context = {}
    if request.user.is_superuser:
        context['boards'] = Board.objects.all()
    else:
        boards = Board.objects.filter(groups__in = request.user.groups.all()).distinct()
        if 1 == boards.count():
            board = boards.get()
            return redirect('board:top', board = board.slug)

        context['boards'] = boards

    return render(request, 'index.html', context)
