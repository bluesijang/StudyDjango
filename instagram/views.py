from django.urls import reverse, reverse_lazy
from django.contrib import messages
from http.client import HTTPResponse
from urllib import request
from django.shortcuts import redirect, render, get_object_or_404
from django.utils.decorators import method_decorator
from django.http import HttpResponse, HttpRequest, Http404
from django.views.generic import DetailView, ListView
from  .models import Post
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ArchiveIndexView, YearArchiveView
from .forms import PostForm
from django.views.generic import CreateView, UpdateView, DeleteView

# @login_required
# def post_new(request):
#     if request.method == "POST":
#         form = PostForm(request.POST, request.FILES)
#         if form.is_valid():
#             post = form.save(commit=False)
#             post.author = request.user
#             post.save()
#             messages.success(request, "포스팅을 저장했습니다.")
#             return redirect(post)
#     else:
#         form = PostForm()       
    
#     return render(request, 'instagram/post_form.html', {
#         'form': form,
#         'post': None,
#     })

# CBV 기반
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        messages.success(self.request, "포스팅을 저장했습니다.")
        return super().form_valid(form)

post_new = PostCreateView.as_view()




# post_list = login_required(ListView.as_view(model=Post, paginate_by = 10))


#@method_decorator(login_required, name='dispatch')
#class PostListView(ListView):
class PostListView(LoginRequiredMixin, ListView):
    model = Post
    paginate_by = 10

post_list = PostListView.as_view()    

# @login_required
# def post_list(request):
#     qs = Post.objects.all()
#     q = request.GET.get('q', '')
    
#     if q:
#         qs = qs.filter(message__icontains=q)
        
#     messages.info(request, 'messages 테스트')
    
#     # 위치 : instagram/templates/instagram/post_list.html
#     return render(request, 'instagram/post_list.html',{
#         'post_list': qs,        
#         'q': q,
#     })    


# def post_detail(request: HttpRequest, pk: int) -> HttpResponse:
#     post = get_object_or_404(Post, pk=pk)
#
#     # 아래 내용은 위 한줄로 나타낼 수 있음
#     # try:
#     #     post = Post.objects.get(pk=pk)
#     # except Post.DoesNotExist:
#     #     raise Http404
#    
#     return render(request, 'instagram/post_detail.html', {
#         'post': post,
#     })

# 위 내용을 아래 한줄로 대체

# post_detail = DetailView.as_view(model=Post)
# post_detail = DetailView.as_view(model=Post,queryset=Post.objects.filter(is_public=True))


class PostDetailView(DetailView):
    model = Post
    #queryset = Post.objects.filter(is_public=True)
    
    # 부모 함수를 재정의할 때 super 를 많이 사용함
    def get_queryset(self):
        # if self.request.user.is_authenticated   # 인증이 되어 있다면
        qs = super().get_queryset()
        
        if not self.request.user.is_authenticated:     # login 안되면 공개된것만 봐라
            qs = qs.filter(is_public=True)
            
        return qs
        
    
post_detail = PostDetailView.as_view()


post_archive = ArchiveIndexView.as_view(model=Post, date_field = 'created_at',
                                        paginate_by = 10 )
post_archive_year = YearArchiveView.as_view(model=Post, date_field = 'created_at')




# @login_required
# def post_edit(request, pk):
#     post = get_object_or_404(Post, pk=pk)
    
#     # 작성자 check Tip (@~~로)
#     if post.author != request.user:        
#         messages.error(request, '작성자만 수정할 수 있습니다.')
#         return redirect(post)
    
#     if request.method == "POST":
#         form = PostForm(request.POST, request.FILES, instance=post)
#         if form.is_valid():            
#             post.save()
#             messages.success(request, "포스팅을 수정했습니다.")
#             return redirect(post)
#     else:
#         form = PostForm(instance=post)
    
#     return render(request, 'instagram/post_form.html', {
#         'form': form,
#         'post': post,
#     })
    
class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    
    def form_valid(self, form):
        messages.success(self.request, "포스팅을 수정했습니다.")
        return super().form_valid(form)
    
    
post_edit = PostUpdateView.as_view()


    
    
# @login_required
# def post_delete(request, pk):
#     post = get_object_or_404(Post, pk=pk)
    
#     if request.method == "POST":
#         post.delete()
#         messages.success(request, "포스팅을 삭제했습니다.")
#         return redirect('instagram:post_list')

#     return render(request, 'instagram/post_confirm_delete.html', {   
#         'post': post,                                                                       
#     })
    


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('instagram:post_list')
    
    # def get_success_url(self):
    #     return reverse('instagram:post_list')   
    


post_delete = PostDeleteView.as_view()

    
    