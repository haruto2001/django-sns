from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView
from accounts.models import User
from .forms import PostForm
from .models import Post, Connection


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

    def get_context_data(self, *args, **kwargs):
        """
        コネクションに関するオブジェクト情報をコンテクストに追加
        """
        context = super().get_context_data(*args, **kwargs)
        # コンテクストに追加
        context['connection'] = Connection.objects.get_or_create(user=self.request.user)
        return context


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

    def get_context_data(self, *args, **kwargs):
        """
        コネクションに関するオブジェクト情報をコンテクストに追加
        """
        context = super().get_context_data(*args, **kwargs)
        # コンテクストに追加
        context['connection'] = Connection.objects.get_or_create(user=self.request.user)
        return context


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
        related_post = Post.objects.get(pk=pk)

        # 既にいいねしていた場合は解除
        if  self.request.user in related_post.like_users.all():
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
        # homeにリダイレクト
        return redirect('snsapp:home')


class LikeDetail(LikeBase):
    """"
    詳細ページでいいねした場合
    """
    def get(self, request, *args, **kwargs):
        # LikeBaseのobjを継承
        super().get(request, *args, **kwargs)
        pk = self.kwargs['pk']
        # detailにリダイレクト
        return redirect('snsapp:detail', pk)


class FollowBase(LoginRequiredMixin, View):
    """
    フォローのベース．データベースとのやり取りを定義．
    リダイレクト先は継承先のViewで決定
    """
    def get(self, request, *args, **kwargs):
        # フォローまたはフォロー解除するユーザの特定
        pk = self.kwargs['pk']
        target_user = Post.objects.get(pk=pk).user

        # コネクション情報を取得．存在しなければ作成．
        my_connection = Connection.objects.get_or_create(user=self.request.user)

        # フォローテーブルにターゲットが存在する場合はフォローテーブルから削除
        if target_user in my_connection[0].following.all():
            obj = my_connection[0].following.remove(target_user)
        # 存在しない場合はフォローテーブルに追加
        else:
            obj = my_connection[0].following.add(target_user)

        return obj


class FollowHome(FollowBase):
    """
    HOMEでフォローした場合
    """
    def get(self, request, *args, **kwargs):
        # FollowBaseのobjを継承
        super().get(request, *args, **kwargs)
        # homeにリダイレクト
        return redirect('snsapp:home')


class FollowDetail(FollowBase):
    """
    詳細ページでフォローした場合
    """
    def get(self, request, *args, **kwargs):
        # FollowBaseのobjを継承
        super().get(request, *args, **kwargs)
        pk = self.kwargs['pk']
        # detailにリダイレクト
        return redirect('snsapp:detail', pk)


class FollowList(LoginRequiredMixin, ListView):
    """
    フォローしているユーザの投稿をリスト表示
    """
    model = Post
    template_name = 'list.html'

    def get_queryset(self):
        """
        フォローリスト内にユーザが含まれている場合のみクエリセットを返す
        """
        my_connection = Connection[0].objects.get_or_create(user=self.request.user)
        all_following = my_connection[0].following.all()
        # 投稿ユーザがフォローしているユーザに含まれている場合オブジェクトを返す
        return Post.objects.filter(user__in=all_following)

    def get_context_data(self, *args, **kwargs):
        """
        コネクションに関するオブジェクト情報をコンテクストに追加
        """
        context = super().get_context_data(*args, **kwargs)
        # コンテクストに追加
        context['connection'] = Connection.objects.get_or_create(user=self.request.user)
        return context


class Profile(LoginRequiredMixin, ListView):
    """
    特定のユーザのユーザ情報をリスト表示
    """
    model = User
    template_name = 'profile.html'

    def get_queryset(self):
        """
        ユーザ情報を取得
        """
        # 現在のページのURLからユーザ名を取得
        username = self.request.path.split('/')[-1]
        return User.objects.filter(username=username)
