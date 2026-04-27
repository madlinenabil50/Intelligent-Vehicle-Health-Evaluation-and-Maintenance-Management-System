from django.urls import path
from . import views

urlpatterns = [
    # Auth
    path('login', views.login_view, name='login'),
    path('register', views.register_view, name='register'),
    path('api/session', views.session_view, name='session'),
    path('api/forgot-password', views.forgot_password_view, name='forgot_password'),
    path('api/reset-password', views.reset_password_view, name='reset_password'),
    path('api/logout', views.logout_view, name='logout'),

    # User profile
    path('api/me', views.me_view, name='me'),
    path('api/me/password', views.change_password_view, name='change_password'),

    # Users management (admin)
    path('api/users', views.users_list_create, name='users_list_create'),
    path('api/users/<int:user_id>', views.users_detail, name='users_detail'),

    # Vehicles
    path('api/vehicles', views.vehicles_view, name='vehicles'),
    path('add-vehicle', views.add_vehicle_view, name='add_vehicle'),

    # Appointments
    path('api/appointments', views.appointments_view, name='appointments'),
    path('api/cancel-appointment', views.cancel_appointment_view, name='cancel_appointment'),
    path('api/admin/appointments', views.admin_appointments_view, name='admin_appointments'),
    path('api/appointments/review', views.review_appointment_view, name='review_appointment'),

    # Service History
    path('api/service-history', views.service_history_view, name='service_history'),

    # Work Orders
    path('api/work-orders', views.work_orders_view, name='work_orders'),
    path('api/assign-wo', views.assign_work_order_view, name='assign_work_order'),
    path('api/complete-wo', views.complete_work_order_view, name='complete_work_order'),
    path('api/update-wo-status', views.update_work_order_status_view, name='update_work_order_status'),
    path('api/log-time', views.log_work_time_view, name='log_work_time'),

    # Invoices
    path('api/invoices', views.client_invoices_view, name='client_invoices'),
    path('api/admin/invoices', views.admin_invoices_view, name='admin_invoices'),
    path('api/invoice-preview', views.invoice_preview_view, name='invoice_preview'),
    path('api/admin/uninvoiced-jobcards', views.uninvoiced_jobcards_view, name='uninvoiced_jobcards'),
    path('api/admin/invoices/<int:invoice_id>/mark-paid', views.admin_mark_paid_view, name='admin_mark_paid'),

    # Payments
    path('api/payments', views.payments_view, name='payments'),
    path('api/admin/payments', views.admin_payments_view, name='admin_payments'),
    path('api/finance/stats', views.finance_stats_view, name='finance_stats'),
    path('api/maintenance-stats', views.maintenance_stats_view, name='maintenance_stats'),

    # Inventory
    path('api/inventory', views.inventory_list_create, name='inventory_list_create'),
    path('api/inventory/<int:item_id>', views.inventory_detail, name='inventory_detail'),

    # Parts Requests
    path('api/parts-requests', views.parts_request_api, name='parts_requests'),
    path('api/parts-approval', views.parts_approval_api, name='parts_approval'),

    # Inspections
    path('api/inspections', views.inspection_list_create, name='inspection_list_create'),

    # Chat / AI
    path('api/chat', views.chat_view, name='chat'),

    # Services
    path('api/services', views.services_list_view, name='services_list'),
    # Purchase Orders
    path('api/supplier-parts', views.supplier_parts_api, name='supplier_parts'),
    path('api/purchase-orders', views.purchase_orders_api, name='purchase_orders'),
]
