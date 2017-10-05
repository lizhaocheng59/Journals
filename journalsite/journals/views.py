from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Model
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
import datetime
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.views.generic import CreateView, TemplateView, UpdateView
from braces.views import SelectRelatedMixin
from django.db.models import Q
from django.views.generic.edit import FormMixin

from journals.models import Journal, Entry
from .forms import UserCreateForm, JournalCreateForm, EntryCreateForm, EntryUpdateForm, JournalEditForm, EntryCopyForm


class HomePage(TemplateView):
    template_name = "journals/index.html"

class SignUp(CreateView):
    form_class = UserCreateForm
    # add url from urls.py
    success_url = reverse_lazy('journals:login')
    template_name = 'journals/signup.html'

class TestPage(TemplateView):
    template_name = 'journals/test.html'

class ThanksPage(TemplateView):
    template_name = 'journals/thanks.html'


class CreateJournal(LoginRequiredMixin, SelectRelatedMixin, generic.CreateView):
    # fields = ("name_text", "description_text")
    # success_url = reverse_lazy("groups:all")
    model = Journal
    form_class = JournalCreateForm


    def form_valid(self, form):
        self.object = form.save(commit = False)
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)

class JournalDetail( generic.DetailView):
    model = Journal
    # select_related = ("User", "Journal")
    # success_url = reverse_lazy("journals:all")


class EditJournal(LoginRequiredMixin, UpdateView):
    model = Journal
    # template_name = 'about.html'
    login_url = 'journals:login'
    # redirect_field_name = 'blog/post_detail.html'
    form_class = JournalEditForm


class DeleteJournal(LoginRequiredMixin, generic.DeleteView):
    model = Journal
    # there is a selected name which is something to do with it
    # select_related = ("user", "group")
    success_url = reverse_lazy("journals:all")

    # filter the information
    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     return queryset.filter(user_id=self.request.user.id)

    def delete(self, *args, **kwargs):
        # messages.success(self.request, "Post Deleted")

        return super().delete(*args, **kwargs)

class JournalList(LoginRequiredMixin, generic.ListView):
    model = Journal


class JournalEntryList(LoginRequiredMixin, generic.ListView):
    model = Entry



    def get_queryset(self):
        queryset = super().get_queryset()
        # print("********" + self.request)
        return queryset.filter(journal_id=self.kwargs.get("pk")).exclude(deleted_boolean=True).exclude(hidden_boolean=True).exclude(is_available=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["gournal_id"] = self.kwargs.get("pk")
        return context



class JournalEntrySearchList(LoginRequiredMixin, generic.ListView):
    model = Entry
    #
    # def post(self, request, *args, **kwargs):
    #     print("********" + self.request)

    journal_id = 0
    def get_queryset(self):

        self.journal_id = self.request.GET.get("journal_id")
        queryset = super().get_queryset().filter(journal_id=self.journal_id).exclude(deleted_boolean=True).exclude(
            hidden_boolean=True).exclude(is_available=False)
        # print("********" + self.request.GET.get("content"))

        content = self.request.GET.get("content")
        if content != None:
            queryset = queryset.filter(Q(title_text__icontains=content) | Q(body_text__icontains=content))

        date = self.request.GET.get("date")
        start_date = self.request.GET.get("start_date")
        end_date = self.request.GET.get("end_date")
        if date != '':
            queryset = queryset.filter(published_date=date)

        if start_date != '' and end_date != '':
            queryset = queryset.filter(Q(published_date__gte = start_date) & Q(published_date__lte =end_date))

        # date = self.request.GET.get("date")
        # date = datetime.datetime.strptime(date, '%Y-%m-%d')
        #
        # # date = datetime.time.strftime(date, '%Y-%m-%d')
        # print( date.year, date.month, date.day)
        # datetime.datetime.now().da

        # print("********"  + "**" + date + "*" + start_date + "*" +end_date )
        # return queryset
        # if content != None:
        #     else if
        return queryset

    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     print("********" , queryset.count(), self.kwargs.get("pk"))
    #     self.journal_id = self.request.GET.get("journal_id")
    #
    #     return queryset.filter(journal_id=self.kwargs.get("pk")).exclude(is_available=False)

    #

        # journal = models.ForeignKey(Journal, on_delete=models.CASCADE)
        # title_text = models.CharField('entry title', max_length=200)
        # body_text = models.CharField('entry body', max_length=200)
        # published_date = models.DateTimeField('published date', default=timezone.now)
        # hidden_boolean = models.BooleanField('hidden', default=False)
        # deleted_boolean = models.BooleanField('deleted', default=False)
        # orginal_id = models.IntegerField('orginal entry id', null=True)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # print("********" + self.kwargs.get("gournal_id"))
        context["gournal_id"] = self.journal_id
        return context



class JournalEntryListAll(LoginRequiredMixin, generic.ListView):
    model = Entry

    def get_queryset(self):
        queryset = super().get_queryset()
        # print("********" + self.request)
        return queryset.filter(journal_id=self.kwargs.get("pk")).exclude(is_available=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["gournal_id"] = self.kwargs.get("pk")
        return context

class JournalEntryCreate(LoginRequiredMixin, CreateView):
    # fields = ('title_text', 'body_text')
    model = Entry
    form_class = EntryCreateForm
    def form_valid(self, form):
        entry = form.save(commit=False)
        entry.journal = get_object_or_404(Journal, pk = self.kwargs.get("pk"))
        # entry.orginal_entry = entry.id
        entry.save()
        entry.orginal_entry = entry.id
        entry.save()
        # print("**********self.object.pk**************" , entry.id)
        return super().form_valid(form)



    # def get_queryset(self):
    #     try:
    #         self

    # def get_success_url(self):
    #     # print("********" + self.title_text + "***" + self.pk)
    #     self.orginal_id = get_object_or_404(Entry, pk=self.kwargs.get("pk"))
    #     return reverse("journals:entry_log", kwargs={"orginal_id": self.orginal_id})

class JournalEntryDetail(LoginRequiredMixin, generic.DetailView):
    model = Entry
    # select_related = ("user", "group")
    login_url = 'journals:login'

    # form_class = EntryUpdateForm

    def get_queryset(self):
        queryset = super().get_queryset()
        # print(queryset)
                # kwargs 是指r"by/(?P<username>[-\w]+)/(?P<pk>\d+)/$" 里面的username和ok
        return queryset.filter(pk=self.kwargs.get("pk"))

class JournalEntryUpdate(LoginRequiredMixin, UpdateView):
        model = Entry
        # template_name = 'about.html'
        login_url = 'journals:login'
        # redirect_field_name = 'journals/entry_log_list.html'
        # success_url  = 'journals:login'
        form_class = EntryUpdateForm

        # reverse("journals:entry_detail", kwargs={"entryname": self.title_text, "pk": self.pk})
        # redirect_field_name = 'journals:EntryLog  pk=journal.id'

        # def get_queryset(self):
        # def get_context_data(self, **kwargs):
        #     context = super().get_context_data(**kwargs)
        #     context["entry_body_"]

        def get_success_url(self):
            # get entry list including same value of orginal_entry

            entry = get_object_or_404(Entry, pk=self.kwargs.get("pk"))
            # have to store the original entry

            # originalEntry =


            # print("********" + entry.orginal_entry)
            return reverse("journals:entry_log", kwargs={"orginal_entry":entry.orginal_entry})


        #
        # def get_redirect_url(self, *args, **kwargs):
        #     self.redirect_field_name = reverse("journals:entry_log", kwargs={"pk": self.pk})
        #     return reverse("journals:entry_log", kwargs={"pk": self.pk})
        # def get_absolute_url(self):
        #     # print("********" + self.title_text + "***" + self.pk)
        #     return reverse("journals:entry_log", kwargs={"pk": self.pk})



        def form_valid(self, form):

            self.object = form.save(commit=False)
            entry_orginal_id = 0
            if self.object.orginal_entry != 0:
                entry_orginal_id = self.object.orginal_entry





            entry = Entry(journal= self.object.journal,
                          title_text=self.object.title_text,
                          body_text=self.object.body_text,
                          published_date=self.object.published_date,
                          hidden_boolean=self.object.hidden_boolean,
                          deleted_boolean=self.object.deleted_boolean,
                          orginal_entry=entry_orginal_id,
                          is_available=False)

            # self.object.is_replaced=True
            # self.object.save()

            entry_log = EntryCopyForm(instance=entry)
            entry_log.is_valid()
            # entry_log.cleaned_data
            entry.save()

            # self.object.save(commit=False)
            # success_url = reverse_lazy("journals:entry_log", kwargs={"pk": self.kwargs.get("pk")})
            # print("************" +entry.pk)
            return super().form_valid(entry)

# class JournalEntryRemove(LoginRequiredMixin, generic.DeleteView):
#     model = Entry
#     # 建表的时候  there is a selected name which is something to do with it
#     # select_related = ("user", "group")
#     success_url = reverse_lazy("journals:entry_list")
#
#     def get_queryset(self):
#         queryset = super().get_queryset()
#
#     def form_vali

@login_required
def entry_remove(request, pk):
    entry = get_object_or_404(Entry, pk = pk)
    entry.deleted_boolean = True
    entry.save()
    return redirect('journals:entry_list', pk=entry.journal.id)


@login_required
def entry_hide(request, pk):
    entry = get_object_or_404(Entry, pk = pk)
    if entry.hidden_boolean:
        entry.hidden_boolean = False
    else:
        entry.hidden_boolean = True
    entry.save()
    return redirect('journals:entry_list', pk=entry.journal.id)

@login_required
def entry_replace(request, pk, orginal_entry_index):
    # print("*****"+orginal_entry_index)
    # old_entry = Entry.objects.get(is_available=True)
    old_entry = get_object_or_404(Entry, is_available=True, orginal_entry=orginal_entry_index)
    old_entry.is_available=False
    old_entry.save()
    entry = get_object_or_404(Entry, pk=pk)
    entry.is_available = True
    entry.save()
    # entry.hidden_boolean = True
    # entry.save()
    # 'journals:entry_list'
    # pk = journal.id
    # 'journals:entry_log'
    # orginal_entry = entry.orginal_entry
    return redirect('journals:entry_log', orginal_entry=entry.orginal_entry)







class JournalEntryLog(LoginRequiredMixin, generic.ListView):
        model = Entry
        template_name_suffix = '_log_list'
        def get_queryset(self):
            queryset = super().get_queryset()
            print("********" + self.kwargs.get("orginal_entry"))
            return queryset.filter(orginal_entry=self.kwargs.get("orginal_entry"))

        # def get_context_data(self, **kwargs):
        #     context = super().get_context_data(**kwargs)
        #     # context["gournal_id"] = self.kwargs.get("pk")
        #     return context

        # from .models import Journal, User, Entry, EntryLog
#
# def index(request):
#     # template = loader.get_template('journals/jounals_login.html')
#     return HttpResponseRedirect(reverse('journals:journal_login'))
#     # return HttpResponse("Hi world")
#
# def journal_login(request):
#     template = loader.get_template('journals/journals_login.html')
#     context = {}
#     return HttpResponse(template.render(context, request))
#     # return HttpResponse("Hi world")
#
# def journal_login_confirm(request):
#
#     email = request.POST.get('email')
#     password = request.POST.get('password')
#     try:
#         user = get_object_or_404(User, email_text=email, password_hash=password)
#     except:
#         return HttpResponse("The email or the password is incorrect!!")
#
#
#     return HttpResponseRedirect(reverse('journals:journals'))
# def journal_register(request):
#     template = loader.get_template('journals/journals_register.html')
#     context = {}
#     return HttpResponse(template.render(context, request))
#     # return HttpResponse("Hi world")
# def journal_register_confirm(request):
#     name = request.POST.get('name')
#     email = request.POST.get('email')
#     gender = request.POST.get('gender')
#     password = request.POST.get('password')
#     # print(name, "+", email, "+", gender, "+", password)
#     user = User(email_text = email, password_hash = password)
#     user.save()
#     return HttpResponse("Your email is %s, password is %s" % (user.email_text, user.password_hash))
#
#
# def journals(request):
#     journal_list = Journal.objects.order_by('-created_date')
#     template = loader.get_template('journals/journals_all.html')
#     context = {
#         'journal_list': journal_list,
#     }
#     return HttpResponse(template.render(context,request))
#
#
#
# def journal_create(request):
#     template = loader.get_template('journals/create_journal.html')
#     context = {    }
#     return HttpResponse(template.render(context,request))
#
# def journal_create_confirm(request):
#     j = Journal(
#         author=User.objects.get(pk=1), #debug
#         name_text=request.POST.get('name'),
#         description_text=request.POST.get('description'),
#         created_date=datetime.datetime.now(),
#         modified_date=datetime.datetime.now()
#     )
#     j.save()
#     return HttpResponseRedirect(reverse('journals:journals'))
#
# def journal_search(request):
#         search_text = request.POST.get('search')
#         journal_search_list = Journal.objects.filter(name_text__icontains=search_text)
#         template = loader.get_template('journals/journals_search.html')
#         context = {
#             'journal_list': journal_search_list,
#             'search_text' : search_text
#         }
#         print(journal_search_list)
#         # return HttpResponse("You're looking at question %s." % journal_search_list)
#         return HttpResponse(template.render(context, request))
#
# def journal_view(request, journal_id):
#     journal = get_object_or_404(Journal, pk=journal_id)
#     entry_list = Entry.objects.filter(entry_log__journal=journal_id).order_by('-published_date')
#     template = loader.get_template('journals/view_journal.html')
#     context = {
#         'journal': journal,
#         'entry_list': entry_list,
#     }
#     return HttpResponse(template.render(context, request))
#
#
#
#
# def entry_create(request, journal_id):
#     journal = get_object_or_404(Journal, pk=journal_id)
#     template = loader.get_template('journals/create_entry.html')
#     context = {
#         'journal': journal,
#     }
#     return HttpResponse(template.render(context, request))
#
# def entry_create_confirm(request, journal_id):
#     journal = get_object_or_404(Journal, pk=journal_id)
#     context = {
#         'journal': journal,
#     }
#     el = EntryLog(
#         journal=Journal.objects.get(pk=journal_id)
#     )
#     el.save()
#     e = Entry(
#         entry_log=el,
#         title_text=request.POST.get('name'),
#         body_text=request.POST.get('description'),
#         published_date=datetime.datetime.now(),
#         hidden_boolean=False,
#         deleted_boolean=False
#     )
#     e.save()
#     return HttpResponseRedirect(reverse('journals:journal_view', kwargs={'journal_id': journal_id}))
#
# def entry_view(request, journal_id, entry_id):
#     entry = Entry.objects.get(pk = entry_id)
#     print(entry)
#     return HttpResponse("view entry %s" % entry.body_text)
#
# def entry_edit(request, journal_id, entry_id):
#     # entry = Entry.objects.get(pk=entry_id)
#     # print(entry)
#     # journal = get_object_or_404(Journal, pk=journal_id)
#     entry = get_object_or_404(Entry, pk = entry_id)
#     template = loader.get_template('journals/edit_entity.html')
#     context = {
#         "journal_id":journal_id,
#         'entry': entry,
#     }
#     return HttpResponse(template.render(context, request))
#     # print(entry.body_text)
#     # return HttpResponse("edit entry %s" % entry_id)
# def entry_edit_confirm(request, journal_id, entry_id):
#     # context = {
#     #     'entry': entry,
#     # }
#     entry = get_object_or_404(Entry, pk = entry_id)
#     entry.body_text = request.POST.get('description')
#     entry.title_text = request.POST.get('name')
#     entry.save()
#
#     print(entry.title_text)
#     return HttpResponseRedirect(reverse('journals:journal_view', kwargs={'journal_id': journal_id}))
#
#     # journal = get_object_or_404(Journal, pk=journal_id)
#     # context = {
#     #     'journal': journal,
#     # }
#     # el = EntryLog(
#     #     journal=Journal.objects.get(pk=journal_id)
#     # )
#     # el.save()
#     # e = Entry(
#     #     entry_log=el,
#     #     title_text=request.POST.get('name'),
#     #     body_text=request.POST.get('description'),
#     #     published_date=datetime.datetime.now(),
#     #     hidden_boolean=False,
#     #     deleted_boolean=False
#     # )
#     # e.save()
#     # return HttpResponseRedirect(reverse('journals:journal_view', kwargs={'journal_id': journal_id}))
#     # template = loader.get_template('journals/edit_entity.html')
#     # return HttpResponse(template.render(context, request))
#
#
# def entry_history(request, journal_id, entry_id):
#     return HttpResponse("entry history %s" % entry_id)