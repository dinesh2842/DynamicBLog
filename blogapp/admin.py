from django.contrib import admin
from .models import Category,Blogs,ContactUs,Ajaxx


class CategoryAdmin(admin.ModelAdmin):
  list_display=('id','category_name','created_at','updated_at')



class BlogAdmin(admin.ModelAdmin):
  list_display=('id','title','category','is_featured','blog_image')
  prepopulated_fields={'slug':('title',)}
  search_fields=('id','title','category__category_name','status')
  list_editable=('is_featured',)


admin.site.register(Category,CategoryAdmin)
admin.site.register(Blogs,BlogAdmin)
admin.site.register(ContactUs)
admin.site.register(Ajaxx)
