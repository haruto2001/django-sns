from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView
from .forms import PostForm
from .models import Post


class Home(LoginRequiredMixin, ListView):
   """
   HOMEページで、自分以外のユーザの投稿をリスト表示
   """
   model = Post
   template_name = 'list.html'

   def get_queryset(self):
       """
       リクエストユーザーのみ除外
       """
       return Post.objects.exclude(user=self.request.user)


class MyPost(LoginRequiredMixin, ListView):
    """
    HOMEページで、自分の投稿をリスト表示
   """
    model = Post
    template_name = 'list.html'

    def get_queryset(self):
        """
        自分の投稿に限定
        """
        return Post.objects.filter(user=self.request.user)


class DetailPost(LoginRequiredMixin, DetailView):
    """
    投稿の詳細を表示
    """
    model = Post
    template_name = 'detail.html'


class UpdatePost(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    投稿編集ページ
    """
    model = Post
    template_name = 'update.html'
    form_class = PostForm

    def get_success_url(self, **kwargs):
        """
        編集完了後の遷移先
        """
        pk = self.kwargs['pk']
        return reverse_lazy('snsapp:detail', kwargs={'pk': pk})

    def test_func(self, **kwargs):
        """
        アクセスできるユーザを制限
        """
        pk = self.kwargs['pk']
        post = Post.objects.get(pk=pk)
        return post.user == self.request.user


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


class DeletePost(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    投稿削除ページを表示
    """
    model = Post
    template_name = 'delete.html'
    success_url = reverse_lazy('snsapp:mypost')

    def test_func(self, **kwargs):
        """
        アクセスできるユーザを制限
        """
        pk = self.kwargs['pk']
        post = Post.objects.get(pk=pk)
        return post.user == self.request.user


class LikeBase(LoginRequiredMixin, View):
    """
    いいねのベース．データベースとのやり取りを定義．
    リダイレクト先は継承先のViewで決定
    """
    def get(self, request, *args, **kwargs):
        # 投稿を特定
        pk = self.kwargs['pk']
        like_posts = Post.objects.get(pk=pk)

        # 既にいいねしていた場合は解除
        if  self.request.user in like_posts.like_users.all():
            obj = related_post.like_users.remove(self.request.user)
        # そうでなければいいねをする
        else:
            obj = related_post.like_users.add(self.request.user)

        return obj


class LikeHome(LikeBase):
    """
    HOMEでいいねした場合
    """
    def get(self, request, *args, **kwargs):
        # LikeBaseのobjを継承
        super().get(request, *args, **kwargs)
        pk = kwargs['pk']
        # homeにリダイレクト
        return redirect('snsapp:home', pk)


class LikeDetail(LikeBase):
    """"
    詳細ページでいいねした場合
    """
    def get(self, request, *args, **kwargs):
        # LikeBaseのobjを継承
        super().get(request, *args, **kwargs)
        pk = kwargs['pk']
        # detailにリダイレクト
        return redirect('snsapp:detail', pk)




