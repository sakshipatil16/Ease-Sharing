from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from .models import Item,OrderItem,Order
from .forms import ItemForm,CommentForm
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.views.generic import ListView, DetailView,DeleteView,View
from django.db.models import Q
from django.utils import timezone
from django.contrib import messages


# Create your views here.
def item_list(request):
    items=Item.objects.all()
    query=request.GET.get("q")
    if query :
        items= items.filter(
            Q(title__icontains=query)|
            Q(description__icontains=query)
            ).distinct()    
    context={
        'items':items
        }
    return render(request,"home-page.html",context)

class ItemDetailView(DetailView):
    model= Item
    template_name = "product.html"

def upload_item(request):
    if request.method=='POST':
        form=ItemForm(request.POST, request.FILES)
        if form.is_valid():
            form.instance.user=request.user
            form.save()
            return redirect('item_list')
    else:
        form = ItemForm()
    return render(request,'upload_item.html',{
        
        'form':form
        })



class ItemDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model= Item
    template_name='item_confirm_delete.html'
    success_url='/item/'
    def test_func(self):
        item=self.get_object()
        if self.request.user == item.user:
            return True
        return False


def add_to_cart(request, pk):
    item =get_object_or_404(Item, pk=pk)
    order_item, created=OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False
        )
    order_qs=Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order=order_qs[0]
        if order.items.filter(item__pk=item.pk).exists():  
           
            messages.info(request,"This item already exists in your cart")
            return redirect("product",pk=pk)
        else:
            messages.info(request,"This item was added to your cart")
            order.items.add(order_item)
            return redirect("product",pk=pk)
    else:
        ordered_date=timezone.now()
        order = Order.objects.create(user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request,"This item quantity was added to your cart")
        return redirect("product",pk=pk)

def remove_from_cart(request,pk):
    item=get_object_or_404(Item,pk=pk)
    order_qs=Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order=order_qs[0]
        if order.items.filter(item__pk=item.pk).exists():
            order_item =OrderItem.objects.filter(
                 item=item,
                 user=request.user,
                 ordered=False
            )[0]           
            order.items.remove(order_item)
            messages.info(request,"This item was removed from your cart")
            return redirect("product",pk=pk)
        else:
            messages.info(request,"This item was not your cart")
            return redirect("product",pk=pk)
    else:
        messages.info(request,"You do not have an active order")
        return redirect("product",pk=pk)

class OrderSummaryView(LoginRequiredMixin, View):
    def get(self,*args,**kwargs):
        try:
            order = Order.objects.get(user=self.request.user,ordered=False)
            context={
                'object':order
                }
            return render(self.request,'order_summary.html',context)
        except ObjectDoesNotExist:
            messages.error(self.request,"YOU do not have an active order")
            return redirect("/")



def add_comment_to_item(request, pk):
    item = get_object_or_404(Item, pk=pk)
    form=CommentForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            form.instance.item = item
            form.instance.user=request.user
            form.save()
            return redirect('product', pk=item.pk)
    else:
        form = CommentForm()
    return render(request, 'add_comment_to_item.html', {'form': form})

def chat(request, pk):
    item = get_object_or_404(Item, pk=pk)
    form=ChatForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            form.instance.item = item
            form.instance.user=request.user
            form.save()
            return redirect('chat', pk=item.pk)
    else:
        form = ChatForm()
    return render(request, 'chat.html', {'form': form})

class UserItemListView(ListView):
    model= Item
    template_name='user_items.html'
    context_object_name = 'items' 
    def get_queryset(self):
        user = get_object_or_404(User, pk=self.kwargs.get('pk')) 
        return Item.objects.filter(user=user)
