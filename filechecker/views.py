from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView


from filechecker.apps import FilecheckerConfig
from filechecker.forms import UploadFileForm
from filechecker.models import File, FileStatuses, Logs

app_name = FilecheckerConfig.name


class FilesList(ListView):
    model = File
    template_name = 'filechecker/home.html'

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return File.objects.filter(owner=self.request.user)
        else:
            return None


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

    def get_object(self, *args, **kwargs):
        try:
            return Logs.objects.get(file_id=self.kwargs['pk'])
        except:
            return None


class UpdateFile(UpdateView):
    form_class = UploadFileForm
    model = File
    success_url = reverse_lazy('home')

    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)

        if self.form_valid:

            self.object.status = FileStatuses.UPDATE
            self.object.save()

        return redirect(self.success_url)


class DeleteFile(DeleteView):
    model = File
    success_url = reverse_lazy('home')


