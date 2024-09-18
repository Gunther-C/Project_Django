
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordChangeView
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.http import JsonResponse

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView
from django.views import View

from django.db.models import F, Case, When, Value, CharField, BooleanField

from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin

from itertools import chain

from authentication.models import User
from .models import Ticket, Review, Follow
from .forms import NewTicket, NewReview


@login_required
def searching(request):
    user = request.user

    if request.method == 'POST':
        users_searching = request.POST.get('user-searching')

        if users_searching:
            response = {}
            users_result = User.objects.filter(username__icontains=users_searching).exclude(pk=user.pk)

            for _user in users_result:

                if Follow.objects.filter(user=user, followed_user=_user):
                    response['followed'] = _user.username
                else:
                    response[_user.id] = _user.username

            return JsonResponse(response)

        return JsonResponse({'status': 'errors'})



class UserFluxView(ListView):
    template_name = 'user_page.html'
    context_object_name = 'posts'

    def get_context_data(self, **kwargs):
        kwargs['page_type'] = 'flux'
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        user = self.request.user
        ticket_user = Ticket.objects.filter(user=user)

        """ Abonnés """
        followed_user = Follow.objects.filter(user=user).values_list('followed_user', flat=True)
        followed_tickets = Ticket.objects.filter(user__in=list(followed_user))
        followed_reviews = Review.objects.filter(ticket__in=list(followed_tickets)).exclude(user=F('ticket__user'))

        """ non abonnés """
        untracked_user_review = (Review.objects.filter(ticket__in=list(ticket_user))
                                 .exclude(user__in=[user] + list(followed_user)))
        untracked_user = untracked_user_review.values_list('user', flat=True)

        """ Tickets ne pouvant plus recevoir de critique"""
        ticket_blocked = Ticket.objects.filter(review__in=list(followed_reviews) + list(untracked_user_review))

        tickets = Ticket.objects.filter(user__in=[user] + list(followed_user))
        tickets = tickets.annotate(content_type=Value('TICKET', CharField()))
        tickets = tickets.annotate(reviews_response=Case(
                When(pk__in=ticket_blocked.values_list('pk', flat=True), then=Value(True)),
                default=Value(False),
                output_field=BooleanField()
            )
        )

        reviews = Review.objects.filter(user__in=[user] + list(followed_user) + list(untracked_user))
        reviews = reviews.annotate(content_type=Value('REVIEW', CharField()))
        reviews = reviews.annotate(reviews_response=Case(
                When(ticket__in=list(ticket_blocked), then=Value(True)),
                default=Value(False),
                output_field=BooleanField()
            )
        )

        return sorted(chain(reviews, tickets), key=lambda flux: flux.time_created, reverse=True)


class UserPostView(ListView):
    template_name = 'user_page.html'
    context_object_name = 'posts'

    def get_context_data(self, **kwargs):
        kwargs['page_type'] = 'post'
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        user = self.request.user
        reviews = Review.objects.filter(user=user)
        reviews = reviews.annotate(content_type=Value('REVIEW', CharField()))

        tickets = Ticket.objects.filter(user=user)
        tickets = tickets.annotate(content_type=Value('TICKET', CharField()))

        return sorted(chain(reviews, tickets), key=lambda post: post.time_created, reverse=True)


class UserFollowView(ListView):
    template_name = 'userFollows/users_follow.html'

    def get_context_data(self, **kwargs):
        kwargs['page_type'] = 'follow'
        kwargs['followed'] = ''
        kwargs['following'] = ''
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        user = self.request.user
        following = user.following.all()
        followed = user.followed_by.all()
        self.extra_context = {'followed': followed, 'following': following}
        return self.extra_context


class FollowCreateView(View):

    def get(self, request, pk):
        followed_user = get_object_or_404(User, pk=pk)
        if followed_user and request.user != followed_user:
            Follow.objects.get_or_create(user=request.user, followed_user=followed_user)

        return redirect('/env/user_follows/')


class TicketCreateView(SuccessMessageMixin, CreateView):
    model = Ticket
    form_class = NewTicket
    template_name = 'tickets/ticket_created.html'
    success_url = reverse_lazy('env:user-flux')
    success_message = 'Votre ticket est créé.'

    def form_valid(self, form):
        _title = form.cleaned_data['title']
        _exist = Ticket.objects.filter(user=self.request.user, title=_title).exists()
        if _exist:
            messages.add_message(self.request, messages.WARNING,
                                 'Vous avez déja crée un ticket ayant le mème titre.')

        form.instance.user = self.request.user
        return super().form_valid(form)


class ReviewCreateView(SuccessMessageMixin, CreateView):
    model = Review
    form_class = NewReview
    template_name = 'reviews/review_created.html'
    success_url = reverse_lazy('env:user-flux')
    success_message = 'Votre critique est créée.'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.object = None

    def get_context_data(self, **kwargs):
        kwargs['form_ticket'] = NewTicket()
        return super().get_context_data(**kwargs)

    def post(self, request, *args, **kwargs):
        form_ticket = NewTicket(request.POST, request.FILES)
        form_review = self.get_form()

        if form_ticket.is_valid() and form_review.is_valid():
            ticket = form_ticket.save(commit=False)
            ticket.user = request.user
            ticket.save()

            review = form_review.save(commit=False)
            review.user = request.user
            review.ticket = ticket
            review.save()
            return self.form_valid(form_review)

        else:
            return self.form_invalid(form_review)


class ReviewResponseCreateView(SuccessMessageMixin, CreateView):
    model = Review
    form_class = NewReview
    template_name = 'reviews/review_response.html'
    success_message = 'Votre critique est créée.'

    def get_context_data(self, **kwargs):
        kwargs['return_url'] = reverse('env:user-flux')
        kwargs['post'] = get_object_or_404(Ticket, pk=self.kwargs.get('pk'))
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        ticket = get_object_or_404(Ticket, pk=self.kwargs.get('pk'))
        review_response = Review.objects.filter(ticket=ticket).exclude(user=F('ticket__user')).exists()

        if review_response:
            messages.add_message(self.request, messages.WARNING, 'Une critique sur ce ticket existe déjà.')
            return self.form_invalid(form)

        form.instance.user = self.request.user
        form.instance.ticket = ticket
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('env:user-flux')


class TicketUpdateView(SuccessMessageMixin, UpdateView):
    model = Ticket
    form_class = NewTicket
    template_name = 'tickets/ticket_created.html'
    success_message = "Votre ticket est modifié"

    def get_object(self, queryset=None):
        return get_object_or_404(Ticket, pk=self.kwargs.get('pk'))

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('env:user-posts')


class ReviewUpdateView(SuccessMessageMixin, UpdateView):
    model = Review
    form_class = NewReview
    template_name = 'reviews/review_response.html'
    success_message = "Votre critique est modifiée"

    def get_object(self, queryset=None):
        return get_object_or_404(Review, pk=self.kwargs.get('pk'))

    def get_context_data(self, **kwargs):
        kwargs['return_url'] = reverse('env:user-posts')
        kwargs['post'] = get_object_or_404(Ticket, pk=self.object.ticket.pk)
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('env:user-posts')


class TicketDeleteView(SuccessMessageMixin, DeleteView):
    model = Ticket
    template_name = 'modal.html'
    success_url = reverse_lazy('env:user-posts')
    success_message = "Votre ticket est supprimé"

    def get_object(self, queryset=None):
        return get_object_or_404(Ticket, user=self.request.user, pk=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        kwargs['text'] = "Souhaitez-vous supprimer votre ticket :"
        kwargs['name'] = f" {self.object.title}"
        kwargs['return_url'] = reverse('env:user-posts')
        return super().get_context_data(**kwargs)


class ReviewDeleteView(SuccessMessageMixin, DeleteView):
    model = Review
    template_name = 'modal.html'
    success_url = reverse_lazy('env:user-posts')
    success_message = "Votre critique est supprimée"

    def get_object(self, queryset=None):
        return get_object_or_404(Review, user=self.request.user, pk=self.kwargs.get('pk'))

    def get_context_data(self, **kwargs):
        kwargs['text'] = 'Souhaitez-vous supprimer votre critique :'
        kwargs['name'] = f" {self.object.title_review}"
        kwargs['return_url'] = reverse('env:user-posts')
        return super().get_context_data(**kwargs)


class FollowDeleteView(SuccessMessageMixin, DeleteView):
    model = Follow
    template_name = 'modal.html'
    success_url = reverse_lazy('env:user-follows')
    success_message = "Votre suivi est supprimé"

    def get_object(self, queryset=None):
        return get_object_or_404(Follow, user=self.request.user, followed_user_id=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        kwargs['text'] = "Vous désabonner de :"
        kwargs['name'] = f" {self.object.followed_user.username}"
        kwargs['return_url'] = reverse('env:user-follows')
        return super().get_context_data(**kwargs)
