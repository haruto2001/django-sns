from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView
from .forms import PostForm
from .models import Post


class Home(LoginRequiredMixin, ListView):
   """
   HOMEページで、自分以外のユーザの投稿をリスト表示
   """
   model = Post
   template_name = 'list.html'

   def get_queryset(self):
       #リクエストユーザーのみ除外
       return Post.objects.exclude(user=self.request.user)


class MyPost(LoginRequiredMixin, ListView):
    """
    HOMEページで、自分の投稿をリスト表示
   """
    model = Post
    template_name = 'list.html'

    def get_queryset(self):
        #自分の投稿に限定
        return Post.objects.filter(user=self.request.user)


class DetailPost(LoginRequiredMixin, DetailView):
    """
    投稿の詳細を表示
    """
    model = Post
    template_name = 'detail.html'


class CreatePost(LoginRequiredMixin, CreateView):
    """
    新規投稿ページを表示
    """
    model = Post
    template_name = 'create.html'
    form_class = PostForm
    success_url = reverse_lazy('snsapp:mypost')

    def form_valid(self, form):
        """
        フォームの入力に成功した場合，投稿ユーザとリクエストユーザを紐付ける
        """
        post = form.save(commit=False)
        post.user = self.request.user
        post.save()
        return super().form_valid(form)