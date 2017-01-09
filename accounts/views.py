from django.contrib.auth import get_user_model
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import get_object_or_404
from django.views.generic import UpdateView, FormView
from django.views.generic.detail import DetailView
from django.db.models import Q

from accounts.forms import ProfileEditForm, AcceptTermsForm
from accounts.serializers import TimtecUserSerializer, TimtecUserAdminSerializer
from braces.views import LoginRequiredMixin

from rest_framework import viewsets
from rest_framework import filters
from rest_framework import generics

from core.permissions import IsAdmin


class ProfileEditView(LoginRequiredMixin, UpdateView):
    model = get_user_model()
    form_class = ProfileEditForm
    template_name = 'profile-edit.html'

    def get_success_url(self):
        return reverse_lazy('profile')

    def get_object(self):
        return self.request.user


class ProfileView(LoginRequiredMixin, DetailView):
    model = get_user_model()
    template_name = 'profile.html'
    context_object_name = 'profile_user'

    def get_object(self):
        if hasattr(self, 'kwargs') and 'username' in self.kwargs:
            try:
                return get_object_or_404(self.model, username=self.kwargs['username'])
            except:
                return self.request.user
        else:
            return self.request.user


class TimtecUserViewSet(viewsets.ReadOnlyModelViewSet):
    model = get_user_model()
    lookup_field = 'id'
    filter_fields = ('groups__name',)
    filter_backends = (filters.DjangoFilterBackend, filters.OrderingFilter,)
    serializer_class = TimtecUserSerializer
    ordering = ('first_name', 'username',)


class TimtecUserAdminViewSet(viewsets.ModelViewSet):
    model = get_user_model()
    # lookup_field = 'id'
    # filter_backends = (filters.OrderingFilter,)
    permission_classes = (IsAdmin, )
    serializer_class = TimtecUserAdminSerializer
    ordering = ('first_name', 'username',)
    # search_fields = ('first_name', 'last_name', 'username', 'email')

    def get_queryset(self):
        page = self.request.QUERY_PARAMS.get('page')
        keyword = self.request.QUERY_PARAMS.get('keyword')
        admin = self.request.QUERY_PARAMS.get('admin')
        blocked = self.request.QUERY_PARAMS.get('keyword')
        queryset = super(TimtecUserAdminViewSet, self).get_queryset()

        if keyword:
            queryset = queryset.filter(Q(first_name__icontains=keyword) |
                                       Q(last_name__icontains=keyword) |
                                       Q(username__icontains=keyword) |
                                       Q(email__icontains=keyword))

        if admin:
            queryset = queryset.filter(is_superuser=True)

        if blocked:
            queryset = queryset.filter(is_active=False)

        if page:
            paginator = Paginator(queryset, 50)
            try:
                queryset = paginator.page(page)
            except PageNotAnInteger:
                # If page is not an integer, deliver first page.
                queryset = paginator.page(1)
            except EmptyPage:
                # If page is out of range (e.g. 9999),
                # deliver last page of results.
                queryset = paginator.page(paginator.num_pages)

        return queryset


class UserSearchView(LoginRequiredMixin, generics.ListAPIView):
    model = get_user_model()
    serializer_class = TimtecUserSerializer

    def get_queryset(self):
        queryset = self.model.objects.all()
        query = self.request.QUERY_PARAMS.get('name', None)
        if query is not None:
            queryset = queryset.filter(Q(first_name__icontains=query) |
                                       Q(last_name__icontains=query) |
                                       Q(username__icontains=query) |
                                       Q(email__icontains=query))
        return queryset


class StudentSearchView(LoginRequiredMixin, generics.ListAPIView):
    model = get_user_model()
    serializer_class = TimtecUserSerializer
    search_fields = ('first_name', 'last_name', 'username', 'email')

    def get_queryset(self):
        queryset = self.model.objects.all()
        course = self.request.QUERY_PARAMS.get('course', None)

        classes = self.request.user.professor_classes.all()

        if classes:
            queryset = queryset.filter(classes__in=classes)
        else:
            # FIXME: if every student is in a class, this is useless.
            if course is not None:
                queryset = queryset.filter(studentcourse_set=course)
        query = self.request.QUERY_PARAMS.get('name', None)
        if query is not None:
            queryset = queryset.filter(Q(first_name__icontains=query) |
                                       Q(last_name__icontains=query) |
                                       Q(username__icontains=query) |
                                       Q(email__icontains=query))
        return queryset


class AcceptTermsView(FormView):
    template_name = 'accept-terms.html'
    form_class = AcceptTermsForm
    success_url = reverse_lazy('courses')

    def get_success_url(self):
        next_url = self.request.POST.get('next', None)
        if next_url:
            return next_url
        return reverse_lazy('courses')

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        self.request.user.accepted_terms = True
        self.request.user.save()
        return super(AcceptTermsView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(AcceptTermsView, self).get_context_data(**kwargs)

        next_url = self.request.GET.get('next')
        if next_url:
            context['next_url'] = next_url
        return context
