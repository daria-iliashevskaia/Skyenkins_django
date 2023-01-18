from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from filechecker.apps import FilecheckerConfig
from filechecker.forms import UploadFileForm
from filechecker.models import File, FileStatuses

app_name = FilecheckerConfig.name


class FilesList(ListView):
    model = File
    template_name = 'filechecker/home.html'

    def get_queryset(self):
        return File.objects.filter(owner=self.request.user)


class FileCreate(CreateView):
    form_class = UploadFileForm
    template_name = 'filechecker/addfile.html'
    success_url = reverse_lazy('home')

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            file = form.save(commit=False)
            file.owner = self.request.user
            file.save()

        return redirect(self.success_url)


class ShowFile(DetailView):
    model = File
    template_name = 'filechecker/detailfile.html'


class UpdateFile(UpdateView):
    form_class = UploadFileForm
    model = File
    success_url = reverse_lazy('home')

    # def post(self, request, *args, **kwargs):
    #     form = self.form_class(request.POST, request.FILES)
    #     if form.is_valid():
    #         file = form.save(commit=False)
    #         file.status = FileStatuses.UPDATE
    #         file.save()
    #
    #     return redirect(self.success_url)

    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)

        self.status = FileStatuses.UPDATE

        return redirect(self.success_url)



class DeleteFile(DeleteView):
    model = File
    success_url = reverse_lazy('home')


