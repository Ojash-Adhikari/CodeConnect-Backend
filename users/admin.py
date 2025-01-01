from django.contrib import admin

from users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'first_name', 'last_name', 'email', 'phone_number', 'user_type']
    search_fields = ['username', 'first_name', 'last_name', 'email', 'phone_number']
    list_filter = ['user_type']
    ordering = ['first_name', 'last_name', 'email', 'phone_number', 'user_type']
    list_per_page = 20
    date_hierarchy = 'date_joined'
    readonly_fields = ['date_joined', 'last_login']
    filter_horizontal = []
    raw_id_fields = []
    list_select_related = []
    save_as = False
    save_on_top = False
    preserve_filters = False
    inlines = []
    actions = []
    exclude = []
    formfield_overrides = { }
    show_full_result_count = True
    show_admin_actions = True
    show_change_link = True
    show_delete_link = True
    show_history_link = True
    show_full_documentation_link = True
    def save_model(self, request, obj, form, change):
        if form.cleaned_data.get('password'):
            obj.set_password(form.cleaned_data['password'])  # Hash the password
        super().save_model(request, obj, form, change)
