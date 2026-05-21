import json
import bcrypt
import secrets
import datetime
import os
import base64
import smtplib
import decimal
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from django.conf import settings
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST, require_http_methods
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage
from django.utils.cache import patch_cache_control

from django.db.models import Q, Sum, Case, When, Value, IntegerField
from .models import (
    Users, Vehicle, Appointment, Invoice, Payment,
    Jobcard, Inventoryitem, Jobcardparts, Inspection,
    Certification, Timelog, Client,
    Admin as AdminProfile, Technician, Servicemanager,
    Stockkeeper, Financemanager, Dataanalyst, Supplier,
)

# ---------- Gemini AI Config ----------
# Using requests for maximum reliability across environments
GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"


# ========================================================================
#  HELPERS
# ========================================================================

def _paginate_queryset(queryset, request):
    """Helper to paginate a queryset and return paginated data + metadata"""
    page_number = request.GET.get('page', 1)
    page_size = request.GET.get('page_size', 10)
    
    paginator = Paginator(queryset, page_size)
    try:
        page_obj = paginator.get_page(page_number)
    except EmptyPage:
        page_obj = paginator.get_page(paginator.num_pages)
        
    return {
        'total_pages': paginator.num_pages,
        'current_page': page_obj.number,
        'total_items': paginator.count,
        'has_next': page_obj.has_next(),
        'has_previous': page_obj.has_previous(),
        'page_obj': page_obj,
    }

def _get_session_user(request):
    """Return session user dict or None."""
    user_data = request.session.get('user')
    if user_data:
        # Normalize role to lowercase for view checks
        if 'role' in user_data:
            user_data['role'] = user_data.get('role', '').lower()
        
        # Verify user still exists in DB if we have a user_id
        user_id = user_data.get('user_id')
        if user_id:
            try:
                u = Users.objects.get(user_id=user_id)
                # Ensure name is fresh and handle None values
                fname = u.firstname or ''
                lname = u.lastname or ''
                user_data['name'] = f"{fname} {lname}".strip() or "User"
                user_data['profile_picture'] = u.profilepicture
                request.session['user'] = user_data
            except Users.DoesNotExist:
                # User deleted from DB; invalidate session
                request.session.flush()
                return None
            
    return user_data


def _json_error(msg, status=400):
    response = JsonResponse({'error': msg}, status=status)
    patch_cache_control(response, no_cache=True, no_store=True, must_revalidate=True, private=True)
    return response


def _award_loyalty_point(user_id):
    """
    DEEP SYNC: Awards points based on completed services count vs lifetime earned.
    Supports manual DB edits by syncing whenever called.
    """
    try:
        from .models import Users, Appointment
        user = Users.objects.filter(user_id=user_id).first()
        if not user:
            return

        # 1. Count actual completed appointments in DB
        actual_completed = Appointment.objects.filter(user_id=user_id, status='Completed').count()
        
        # 2. Track 'Lifetime Earned' in resettoken field (hidden tracking)
        try:
            lifetime_earned = int(user.resettoken) if (user.resettoken and user.resettoken.isdigit()) else 0
        except:
            lifetime_earned = 0

        # 3. If DB shows more completed services than we've rewarded so far
        if actual_completed > lifetime_earned:
            diff = actual_completed - lifetime_earned
            user.loyalty_points = (user.loyalty_points or 0) + diff
            user.resettoken = str(actual_completed) # Update lifetime tracker
            user.save()
            print(f"Deep Sync: Awarded {diff} points to User {user_id}. New Balance: {user.loyalty_points}")
        elif actual_completed < lifetime_earned:
            # This handles case where services might have been deleted or status reversed
            user.resettoken = str(actual_completed)
            user.save()

    except Exception as e:
        print(f"Error in Loyalty Deep Sync: {e}")

def _json_ok(extra=None):
    data = {'success': True}
    if extra:
        data.update(extra)
    response = JsonResponse(data)
    patch_cache_control(response, no_cache=True, no_store=True, must_revalidate=True, private=True)
    return response


def _serialize(obj):
    """Make datetime/decimal JSON-safe."""
    if isinstance(obj, (datetime.datetime, datetime.date)):
        return obj.isoformat()
    if isinstance(obj, decimal.Decimal):
        return float(obj)
    return obj


def _map_role(raw_role):
    """Map DB role string to JS-friendly role slug."""
    raw = raw_role.strip()
    mapping = {
        'ServiceManager': 'service-manager',
        'FinanceManager': 'finance-manager',
        'StockKeeper': 'stock-keeper',
        'DataAnalyst': 'data-analyst',
        'TopManager': 'top-manager',
        'Supplier': 'supplier',
    }
    if raw in mapping:
        return mapping[raw]
    if raw.lower() == 'manager':
        return 'manager'
    return raw.lower()


ROLE_TO_DASHBOARD = {
    'admin': 'pages/admin/admin-dashboard.html',
    'client': 'pages/client/client-dashboard.html',
    'technician': 'pages/technician/technician-dashboard.html',
    'inventory': 'pages/inventory/inventory-dashboard.html',
    'manager': 'pages/manager/manager-dashboard.html',
    'service-manager': 'pages/manager/manager-dashboard.html',
    'general-manager': 'pages/manager/general-manager-dashboard.html',
    'top-manager': 'pages/top-manager/top-manager-dashboard.html',
    'stock-keeper': 'pages/inventory/inventory-dashboard.html',
    'fleet-manager': 'pages/manager/manager-dashboard.html',
    'finance-manager': 'pages/finance/finance-dashboard.html',
    'data-analyst': 'pages/analytics/data-dashboard.html',
}


def _send_reset_email(target_email, reset_link):
    """Send password-reset email via SMTP - Premium Dark Design."""
    try:
        system = settings.SYSTEM_NAME
        import smtplib
        from email.mime.multipart import MIMEMultipart
        from email.mime.text import MIMEText

        msg = MIMEMultipart('alternative')
        msg['From'] = f"{system} <{settings.SMTP_USER}>"
        msg['To'] = target_email
        msg['Subject'] = f"Password Reset Request - {system}"

        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Password Reset</title>
</head>
<body style="margin:0;padding:0;background-color:#0f0f1a;font-family:'Segoe UI',Arial,sans-serif;">

  <!-- Wrapper -->
  <table width="100%" cellpadding="0" cellspacing="0" style="background:#0f0f1a;padding:40px 16px;">
    <tr>
      <td align="center">
        <table width="600" cellpadding="0" cellspacing="0" style="max-width:600px;width:100%;">

          <!-- HEADER -->
          <tr>
            <td style="background:linear-gradient(135deg,#1e1b4b 0%,#312e81 50%,#4338ca 100%);border-radius:20px 20px 0 0;padding:40px 40px 30px;text-align:center;">
              <div style="display:inline-block;background:rgba(255,255,255,0.12);border-radius:50%;width:72px;height:72px;line-height:72px;font-size:32px;margin-bottom:16px;">🚗</div>
              <h1 style="margin:0;color:#ffffff;font-size:28px;font-weight:800;letter-spacing:-0.5px;">{system}</h1>
              <p style="margin:8px 0 0;color:#a5b4fc;font-size:14px;letter-spacing:2px;text-transform:uppercase;">Security Update</p>
              <div style="width:60px;height:3px;background:linear-gradient(90deg,#818cf8,#c084fc);margin:20px auto 0;border-radius:2px;"></div>
            </td>
          </tr>

          <!-- GREETING -->
          <tr>
            <td style="background:#1e1b4b;padding:32px 40px 0;">
              <p style="margin:0;color:#e2e8f0;font-size:16px;">Hello,</p>
              <p style="margin:12px 0 0;color:#94a3b8;font-size:14px;line-height:1.6;">
                We received a request to reset your password for your <strong>{system}</strong> account.
              </p>
            </td>
          </tr>

          <!-- ACTION -->
          <tr>
            <td style="background:#1e1b4b;padding:32px 40px;text-align:center;">
              <a href="{reset_link}"
                 style="display:inline-block;background:linear-gradient(135deg,#4338ca,#7c3aed);color:#ffffff;text-decoration:none;font-size:16px;font-weight:700;padding:16px 40px;border-radius:50px;box-shadow:0 8px 30px rgba(99,102,241,0.5);">
                Reset Password Now
              </a>
              <p style="margin:20px 0 0;color:#64748b;font-size:12px;">This link will expire in 60 minutes for your security.</p>
            </td>
          </tr>

          <!-- FOOTER -->
          <tr>
            <td style="background:#0f0f1a;border-radius:0 0 20px 20px;padding:30px 40px;text-align:center;border-top:1px solid rgba(255,255,255,0.05);">
              <p style="margin:0;color:#4a5568;font-size:12px;">Sent by {system} Security Team. Do not reply to this email.</p>
              <p style="margin:8px 0 0;color:#374151;font-size:11px;">&copy; 2026 {system}. All rights reserved.</p>
            </td>
          </tr>

        </table>
      </td>
    </tr>
  </table>

</body>
</html>"""

        text = (
            f"Hello,\n\nYou requested a password reset for your {system} account.\n"
            f"Reset Link: {reset_link}\n\nIf you did not request this, please ignore this email."
        )

        msg.attach(MIMEText(text, 'plain'))
        msg.attach(MIMEText(html, 'html'))

        server = smtplib.SMTP_SSL(settings.SMTP_SERVER, settings.SMTP_PORT)
        server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
        server.send_message(msg)
        server.quit()
        return True
    except Exception as e:
        print(f"Failed to send email: {e}")
        return False


# ========================================================================
#  AUTH VIEWS
# ========================================================================

@csrf_exempt
def logout_view(request):
    """POST /api/logout"""
    request.session.flush()
    return _json_ok()


def login_view(request):
    if request.method != 'POST':
        return _json_error('Method not allowed', 405)

    email = request.POST.get('email', '').strip()
    password = request.POST.get('password', '')

    try:
        user = Users.objects.filter(email=email).first()

        if user:
            stored_pw = user.password or ''
            if stored_pw.startswith('$2'):
                ok = bcrypt.checkpw(password.encode('utf-8'), stored_pw.encode('utf-8'))
            else:
                ok = (stored_pw == password)
            if not ok:
                user = None

        if not user:
            return _json_error('Invalid email or password.', 401)

        mapped_role = _map_role(user.role)

        user_obj = {
            "user_id": user.user_id,
            "email": user.email,
            "name": f"{user.firstname} {user.lastname}",
            "role": mapped_role,
            "phone": user.phone or '',
            "address": user.address or '',
        }

        # Store in Django session
        request.session['user'] = {
            "user_id": user.user_id,
            "email": user.email,
            "name": f"{user.firstname} {user.lastname}",
            "role": mapped_role,
            "ProfilePicture": user.profilepicture,
        }

        # Role-based redirection logic
        if mapped_role == 'data-analyst':
            target_url = '/ml-dashboard'
        else:
            target_url = '/index.html'

        return JsonResponse({"success": True, "redirect": target_url})

    except Exception as e:
        return _json_error(str(e))


@csrf_exempt
def register_view(request):
    if request.method != 'POST':
        return _json_error('Method not allowed', 405)

    first_name = request.POST.get('firstName', '').strip()
    last_name = request.POST.get('lastName', '').strip()
    email = request.POST.get('email', '').strip()
    phone = request.POST.get('phone', '').strip()
    address = request.POST.get('address', '').strip()
    password = request.POST.get('password', '')
    password_confirm = request.POST.get('passwordConfirm', '')
    role = request.POST.get('role', 'Client').strip()

    if role not in ['Client', 'StockKeeper']:
        role = 'Client'

    if password != password_confirm:
        return _json_error('Passwords do not match.', 400)

    if len(password) < 6:
        return _json_error('Password must be at least 6 characters.', 400)

    try:
        if Users.objects.filter(email=email).exists():
            return _json_error('An account with this email already exists.', 400)

        hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        new_user = Users.objects.create(
            firstname=first_name,
            lastname=last_name,
            password=hashed_pw,
            email=email,
            phone=phone,
            address=address,
            role=role,
        )

        # Create the corresponding Client profile record
        if role == 'Client':
            Client.objects.create(user=new_user, registrationdate=datetime.date.today())
        elif role == 'StockKeeper':
            Stockkeeper.objects.create(user=new_user)

        request.session['user'] = {
            "user_id": new_user.user_id,
            "email": email,
            "name": f"{first_name} {last_name}",
            "role": role.lower(),
        }

        target_url = "pages/client/client-dashboard.html"
        return JsonResponse({"success": True, "redirect": target_url})

    except Exception as e:
        return _json_error(str(e))


@csrf_exempt
def session_view(request):
    """GET /api/session"""
    user_data = _get_session_user(request)
    if not user_data:
        return _json_error('Not logged in', 401)

    # Refresh profile picture from DB
    try:
        u = Users.objects.get(user_id=user_data['user_id'])
        user_data['profile_picture'] = u.profilepicture
        request.session['user'] = user_data
    except Users.DoesNotExist:
        pass

    return JsonResponse(user_data)


@csrf_exempt
def forgot_password_view(request):
    """POST /api/forgot-password"""
    if request.method != 'POST':
        return _json_error('Method not allowed', 405)

    try:
        data = json.loads(request.body)
        email = data.get('email', '').strip()
        if not email:
            return _json_error('Email is required')

        user = Users.objects.filter(email=email).first()
        if user:
            print(f"DEBUG: Found user {user.firstname} with email {email}")
            token = secrets.token_urlsafe(32)
            expiry = datetime.datetime.now() + datetime.timedelta(hours=1)
            user.resettoken = token
            user.resettokenexpiry = expiry
            user.save()

            reset_link = f"http://localhost:8000/reset-password.html?token={token}"
            print("\n" + "=" * 50)
            print("PASSWORD RESET EMAIL TRIGGERED")
            print(f"To: {email}")
            print(f"Link: {reset_link}")
            
            success = _send_reset_email(email, reset_link)
            if success:
                print("SUCCESS: Email sent via SMTP.")
            else:
                print("ERROR: SMTP delivery failed. Check your credentials in settings.py.")
            print("=" * 50 + "\n")
        else:
            print(f"DEBUG: No user found with email {email}")

        # Always return success to prevent email enumeration
        return _json_ok()
    except Exception as e:
        print("Forgot Password Error:", e)
        return _json_error('Server error', 500)


@csrf_exempt
def reset_password_view(request):
    """POST /api/reset-password"""
    if request.method != 'POST':
        return _json_error('Method not allowed', 405)

    try:
        data = json.loads(request.body)
        token = data.get('token')
        new_password = data.get('password')

        if not token or not new_password:
            return _json_error('Token and password are required')

        user = Users.objects.filter(
            resettoken=token,
            resettokenexpiry__gt=datetime.datetime.now()
        ).first()

        if not user:
            return _json_error('Invalid or expired token')

        hashed = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        user.password = hashed
        user.resettoken = None
        user.resettokenexpiry = None
        user.save()

        return _json_ok()
    except Exception as e:
        print("Reset Password Error:", e)
        return _json_error('Server error', 500)


# ========================================================================
#  USER VIEWS
# ========================================================================

def _sync_user_role(u):
    from .models import Client, Admin, Technician, Servicemanager, Financemanager, Topmanager, Stockkeeper, Dataanalyst
    import datetime
    role_model_map = {
        'client': Client, 'admin': Admin, 'technician': Technician,
        'service-manager': Servicemanager, 'finance-manager': Financemanager,
        'top-manager': Topmanager, 'stock-keeper': Stockkeeper, 'data-analyst': Dataanalyst,
        'servicemanager': Servicemanager, 'financemanager': Financemanager,
        'topmanager': Topmanager, 'stockkeeper': Stockkeeper, 'dataanalyst': Dataanalyst
    }
    role = (u.role or '').strip().lower()
    model_class = role_model_map.get(role)
    for r, m_class in role_model_map.items():
        if m_class != model_class:
            m_class.objects.filter(user=u).delete()
    if model_class and not model_class.objects.filter(user=u).exists():
        if role == 'client':
            model_class.objects.create(user=u, registrationdate=datetime.date.today())
        elif role == 'technician':
            model_class.objects.create(user=u, hiredate=datetime.date.today(), currentstatus='Available')
        else:
            model_class.objects.create(user=u)

@csrf_exempt
def me_view(request):
    """GET/POST /api/me"""
    user_data = _get_session_user(request)
    if not user_data:
        return _json_error('Not logged in', 401)

    if request.method == 'GET':
        try:
            uid = user_data.get('user_id')
            if not uid:
                return _json_error('Session error: User ID missing', 400)

            # --- DEEP SYNC LOYALTY ---
            _award_loyalty_point(uid)
            # -------------------------
                
            user = Users.objects.filter(user_id=uid).first()
            if not user:
                return _json_error('User not found in database', 404)
                
            client = Client.objects.filter(user_id=user.user_id).first()
            if not client and (user.role or '').strip().lower() == 'client':
                import datetime
                client = Client.objects.create(user=user, registrationdate=datetime.date.today())
            elif client and not client.registrationdate:
                import datetime
                client.registrationdate = datetime.date.today()
                client.save()

            # Read loyalty points from database (allows manual edits to stick)
            loyalty_count = user.loyalty_points or 0

            result = {
                'User_ID': user.user_id,
                'FirstName': user.firstname or '',
                'LastName': user.lastname or '',
                'Email': user.email or '',
                'Phone': user.phone or '',
                'Address': user.address or '',
                'Role': user.role or '',
                'ProfilePicture': user.profilepicture or '',
                'RegistrationDate': (client.registrationdate.isoformat() if client and client.registrationdate else ''),
                'LoyaltyPoints': user.loyalty_points
            }
            return JsonResponse(result)
        except Exception as e:
            import traceback
            error_details = traceback.format_exc()
            print(f"Me View CRITICAL Error: {error_details}")
            return _json_error(f'Database error: {str(e)}', 500)

    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
            user = Users.objects.get(user_id=user_data['user_id'])

            user.firstname = data.get('FirstName', user.firstname)
            user.lastname = data.get('LastName', user.lastname)
            user.phone = data.get('Phone', user.phone)
            user.address = data.get('Address', user.address)
            
            new_email = data.get('Email', user.email)
            if new_email and new_email != user.email:
                if Users.objects.filter(email=new_email).exclude(user_id=user.user_id).exists():
                    return _json_error('This email is already in use by another account.', 400)
                user.email = new_email

            user.save()
            
            # Update session name
            user_data['name'] = f"{user.firstname} {user.lastname}".strip() or "User"
            request.session['user'] = user_data

            profile_pic_base64 = data.get('ProfilePicture')
            if profile_pic_base64 and profile_pic_base64.startswith('data:image/'):
                try:
                    header, encoded = profile_pic_base64.split(",", 1)
                    ext = header.split("/")[1].split(";")[0]
                    filename = f"user_{user_data['user_id']}_{int(datetime.datetime.now().timestamp())}.{ext}"
                    save_dir = os.path.join(str(settings.BASE_DIR), "assets", "uploads", "profiles")
                    os.makedirs(save_dir, exist_ok=True)
                    save_path = os.path.join(save_dir, filename)
                    with open(save_path, "wb") as f:
                        f.write(base64.b64decode(encoded))
                    user.profilepicture = f"/assets/uploads/profiles/{filename}"
                except Exception as img_err:
                    print("Image save error:", img_err)

            user.save()

            # Update session
            user_data['name'] = f"{user.firstname} {user.lastname}"
            user_data['ProfilePicture'] = user.profilepicture
            request.session['user'] = user_data

            return _json_ok()
        except Exception as e:
            print("DB Error (/api/me POST):", e)
            return _json_error(str(e), 500)

    return _json_error('Method not allowed', 405)


@csrf_exempt
def change_password_view(request):
    """POST /api/me/password"""
    if request.method != 'POST':
        return _json_error('Method not allowed', 405)

    user_data = _get_session_user(request)
    if not user_data:
        return _json_error('Not logged in', 401)

    try:
        data = json.loads(request.body)
        current_pwd = data.get('currentPassword')
        new_pwd = data.get('newPassword')

        user = Users.objects.get(user_id=user_data['user_id'])
        stored_pwd = user.password or ''

        if stored_pwd.startswith('$2b$'):
            is_correct = bcrypt.checkpw(current_pwd.encode('utf-8'), stored_pwd.encode('utf-8'))
        else:
            is_correct = (current_pwd == stored_pwd)

        if not is_correct:
            return _json_error('Current password is incorrect')

        hashed_new = bcrypt.hashpw(new_pwd.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        user.password = hashed_new
        user.save()

        return _json_ok()
    except Users.DoesNotExist:
        return _json_error('User not found', 404)
    except Exception as e:
        print("Error updating password:", e)
        return _json_error(str(e), 500)


@csrf_exempt
def users_list_create(request):
    """GET/POST /api/users"""
    if request.method == 'GET':
        user_data = _get_session_user(request)
        if not user_data or user_data['role'] not in ['admin', 'manager', 'service-manager', 'top-manager']:
            return _json_error('Forbidden', 403)

        try:
            qs = Users.objects.all().values(
                'user_id', 'firstname', 'lastname', 'email', 'phone', 'address', 'role'
            ).order_by('-user_id')
            
            paginated = _paginate_queryset(qs, request)
            result = []
            for u in paginated['page_obj']:
                result.append({
                    'User_ID': u['user_id'],
                    'FirstName': u['firstname'],
                    'LastName': u['lastname'],
                    'Email': u['email'],
                    'Phone': u['phone'],
                    'Address': u['address'],
                    'Role': u['role'],
                })
            paginated['data'] = result
            paginated.pop('page_obj', None)
            return JsonResponse(paginated, safe=False)
        except Exception as e:
            print("DB Error (Users GET):", e)
            return _json_error('Database error', 500)

    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
            first_name = data.get('FirstName', '')
            last_name = data.get('LastName', '')
            email = data.get('Email', '')
            password = data.get('Password', '')
            role = data.get('Role', 'Client')
            phone = data.get('Phone', '')
            address = data.get('Address', '')

            if not email or not password or not first_name:
                return _json_error('Missing required fields')

            if Users.objects.filter(email=email).exists():
                return _json_error('Email already exists')

            hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            new_user = Users.objects.create(
                firstname=first_name,
                lastname=last_name,
                email=email,
                password=hashed,
                phone=phone,
                address=address,
                role=role,
            )
            _sync_user_role(new_user)
            return _json_ok({'user_id': new_user.user_id})
        except Exception as e:
            print("DB Error (Users POST):", e)
            return _json_error('Database error', 500)

    return _json_error('Method not allowed', 405)


@csrf_exempt
def users_detail(request, user_id):
    """PUT/DELETE /api/users/<id>"""
    if request.method == 'PUT':
        try:
            data = json.loads(request.body)
            user = Users.objects.get(user_id=user_id)

            user.firstname = data.get('FirstName', user.firstname)
            user.lastname = data.get('LastName', user.lastname)
            user.email = data.get('Email', user.email)
            user.role = data.get('Role', user.role)
            user.phone = data.get('Phone', user.phone)
            user.address = data.get('Address', user.address)

            password = data.get('Password', '')
            if password:
                hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
                user.password = hashed

            user.save()
            _sync_user_role(user)
            return _json_ok()
        except Users.DoesNotExist:
            return _json_error('User not found', 404)
        except Exception as e:
            print("DB Error (Users PUT):", e)
            return _json_error('Database error', 500)

    elif request.method == 'DELETE':
        try:
            # Delete from all related tables (child to parent order)
            Jobcardparts.objects.filter(jobcard__user_id=user_id).delete()
            Certification.objects.filter(inspection__jobcard__user_id=user_id).delete()
            Certification.objects.filter(user_id=user_id).delete()
            Inspection.objects.filter(jobcard__user_id=user_id).delete()
            Inspection.objects.filter(vehicle__user_id=user_id).delete()
            Timelog.objects.filter(jobcard__user_id=user_id).delete()
            Timelog.objects.filter(user_id=user_id).delete()
            Jobcard.objects.filter(user_id=user_id).delete()
            Payment.objects.filter(user_id=user_id).delete()
            Appointment.objects.filter(user_id=user_id).delete()
            Invoice.objects.filter(user_id=user_id).delete()
            Vehicle.objects.filter(user_id=user_id).delete()
            Inventoryitem.objects.filter(user_id=user_id).delete()

            # Role profile tables
            for model in [AdminProfile, Client, Technician, Servicemanager,
                          Stockkeeper, Financemanager, Dataanalyst]:
                try:
                    model.objects.filter(user_id=user_id).delete()
                except Exception:
                    pass

            Users.objects.filter(user_id=user_id).delete()
            return _json_ok()
        except Exception as e:
            print("DB Error (Users DELETE):", e)
            return _json_error(f'Database error: {str(e)}', 500)

    return _json_error('Method not allowed', 405)


# ========================================================================
#  VEHICLE VIEWS
# ========================================================================

@csrf_exempt
def vehicles_view(request):
    """GET /api/vehicles — list vehicles; POST /api/vehicles — delete a vehicle by VIN"""
    user_data = _get_session_user(request)

    if request.method == 'GET':
        role = (user_data.get('role', '') if user_data else '').lower()
        if not user_data or role not in ['admin', 'client', 'top-manager']:
            return _json_error('Forbidden', 403)

        try:
            if role == 'admin':
                qs = Vehicle.objects.all()
            else:
                qs = Vehicle.objects.filter(user_id=user_data['user_id'])

            result = list(qs.values(
                'vehicle_id', 'user_id', 'vin', 'platenumber',
                'model', 'year', 'mileage', 'make', 'color'
            ))
            # Map keys to what frontend expects
            mapped = []
            for v in result:
                # 1. Find the LATEST appointment for this vehicle
                latest_app = Appointment.objects.filter(vehicle_id=v['vehicle_id']).order_by('-appointment_id').first()

                is_in_service = False
                current_status = None
                active_jc_id = None
                active_app_id = None

                if latest_app:
                    active_app_id = latest_app.appointment_id
                    # 2. Check if this appointment has a Jobcard
                    jc = Jobcard.objects.filter(appointment=latest_app).first()
                    
                    # Use status from Jobcard if it exists, otherwise Appointment
                    current_status = jc.status if jc else latest_app.status
                    active_jc_id = jc.jobcard_id if jc else None

                    # If not finished, it is "in service"
                    if current_status not in ['Completed', 'Cancelled', 'Closed']:
                        is_in_service = True

                mapped.append({
                    'Vehicle_ID': v['vehicle_id'],
                    'User_ID': v['user_id'],
                    'VIN': v['vin'],
                    'PlateNumber': v['platenumber'],
                    'Model': v['model'],
                    'Year': v['year'],
                    'Mileage': v['mileage'],
                    'Make': v['make'],
                    'Color': v['color'],
                    'is_in_service': is_in_service,
                    'active_jobcard_id': active_jc_id,
                    'active_appointment_id': active_app_id,
                    'current_status': current_status
                })
            return JsonResponse(mapped, safe=False)
        except Exception as e:
            print("DB Error:", e)
            return _json_error('Database error', 500)

    elif request.method == 'POST':
        if not user_data or user_data['role'] != 'admin':
            return _json_error('Forbidden', 403)
        try:
            data = json.loads(request.body)
            vin = data.get('vin')
            if not vin:
                return _json_error('VIN is missing')
            Vehicle.objects.filter(vin=vin).delete()
            return _json_ok()
        except Exception as e:
            print("DB Error (Delete Vehicle):", e)
            return _json_error('Database error', 500)

    return _json_error('Method not allowed', 405)


@csrf_exempt
def add_vehicle_view(request):
    """POST /add-vehicle — form-based vehicle creation"""
    if request.method != 'POST':
        return _json_error('Method not allowed', 405)

    user_data = _get_session_user(request)
    if not user_data:
        return HttpResponseRedirect('/index.html')

    make = request.POST.get('make', '').strip()
    model = request.POST.get('model', '').strip()
    color = request.POST.get('color', '').strip()
    plate = request.POST.get('plate', '').strip()
    vin = request.POST.get('vin', '').strip()

    year_str = request.POST.get('year', '').strip()
    mileage_str = request.POST.get('mileage', '0').strip()
    db_year = int(year_str) if year_str else None
    db_mileage = int(mileage_str) if mileage_str else None

    try:
        Vehicle.objects.create(
            user_id=user_data['user_id'],
            vin=vin,
            platenumber=plate,
            model=model,
            year=db_year,
            mileage=db_mileage,
            make=make,
            color=color,
        )
        return HttpResponseRedirect('/pages/client/vehicle-list.html')
    except Exception as e:
        print("DB Error on Add Vehicle:", e)
        return HttpResponseRedirect('/pages/client/add-vehicle.html?error=db')


# ========================================================================
#  APPOINTMENT VIEWS
# ========================================================================

@csrf_exempt
def appointments_view(request):
    """POST /api/appointments — create appointment"""
    if request.method != 'POST':
        return _json_error('Method not allowed', 405)

    user_data = _get_session_user(request)
    if not user_data:
        return _json_error('Not logged in', 401)

    try:
        data = json.loads(request.body)
        vehicle_id = data.get('vehicle_id')
        service_type = data.get('service_type')
        date = data.get('date')
        time = data.get('time')

        if not vehicle_id or not service_type or not date or not time:
            return _json_error('Missing required fields')

        start_time = datetime.datetime.strptime(f"{date} {time}:00", "%Y-%m-%d %H:%M:%S")

        # Validate: No past appointments
        now = datetime.datetime.now()
        if start_time < now:
            return _json_error('Cannot book an appointment in the past.')

        Appointment.objects.create(
            user_id=user_data['user_id'],
            vehicle_id=vehicle_id,
            date_time=start_time,
            status='Scheduled',
            service_type=service_type,
        )
        return _json_ok()
    except Exception as e:
        print("DB Error (Add Appointment):", e)
        return _json_error('Database error', 500)


@csrf_exempt
def cancel_appointment_view(request):
    """POST /api/cancel-appointment"""
    if request.method != 'POST':
        return _json_error('Method not allowed', 405)

    user_data = _get_session_user(request)
    if not user_data:
        return _json_error('Not logged in', 401)

    try:
        data = json.loads(request.body)
        appointment_id = data.get('appointment_id')
        if not appointment_id:
            return _json_error('Missing appointment_id')

        apt = Appointment.objects.filter(appointment_id=appointment_id, user_id=user_data['user_id']).first()
        if not apt:
            return _json_error('Appointment not found or not yours', 404)

        # Security Check: Prevent cancellation if work has started or invoice exists
        job = Jobcard.objects.filter(appointment=apt).first()
        if job and (job.status == 'Completed' or (job.totallaborcost and float(job.totallaborcost) > 0)):
            return _json_error('Cannot cancel appointment: work is already in progress or completed.')
            
        # Check for invoice through Jobcard bridge
        invoice_exists = Invoice.objects.filter(jobcard__appointment=apt).exists()
        if invoice_exists:
            return _json_error('Cannot cancel appointment: an invoice has already been generated.')

        if apt.status in ['Completed', 'Cancelled']:
            return _json_error(f'Cannot cancel appointment in {apt.status} status')

        apt.status = 'Cancelled'
        apt.save()
        return _json_ok()
    except Exception as e:
        print("DB Error (Cancel Appointment):", e)
        return _json_error('Database error', 500)


@csrf_exempt
def admin_appointments_view(request):
    """GET /api/admin/appointments"""
    if request.method != 'GET':
        return _json_error('Method not allowed', 405)

    user_data = _get_session_user(request)
    if not user_data or user_data['role'] not in ['admin', 'manager', 'service-manager', 'top-manager']:
        print(f"DEBUG: Access denied to {user_data.get('email') if user_data else 'Anonymous'} (Role: {user_data.get('role') if user_data else 'None'})")
        return _json_error('Forbidden', 403)

    try:
        # Custom status ordering: Scheduled/Confirmed (1), In Progress (2), Completed (3), Cancelled (4)
        qs = Appointment.objects.select_related('user', 'vehicle').annotate(
            status_order=Case(
                When(status__iexact='Scheduled', then=Value(1)),
                When(status__iexact='Confirmed', then=Value(1)),
                When(status__iexact='In Progress', then=Value(2)),
                When(status__iexact='Completed', then=Value(3)),
                When(status__iexact='Cancelled', then=Value(4)),
                default=Value(1),
                output_field=IntegerField(),
            )
        ).order_by('status_order', '-date_time')
        
        status_filter = request.GET.get('status')
        from_date = request.GET.get('from')
        to_date = request.GET.get('to')
        
        if status_filter:
            qs = qs.filter(status__iexact=status_filter)
        if from_date:
            qs = qs.filter(date_time__gte=from_date)
        if to_date:
            qs = qs.filter(date_time__lte=f"{to_date} 23:59:59")
            
        paginated = _paginate_queryset(qs, request)
        result = []
        for a in paginated['page_obj']:
            result.append({
                'Appointment_ID': a.appointment_id,
                'date_time': _serialize(a.date_time),
                'Status': a.status,
                'service_type': a.service_type,
                'ClientEmail': a.user.email if a.user else None,
                'ClientName': f"{a.user.firstname} {a.user.lastname}" if a.user else None,
                'Make': a.vehicle.make if a.vehicle else None,
                'Model': a.vehicle.model if a.vehicle else None,
                'Year': a.vehicle.year if a.vehicle else None,
                'PlateNumber': a.vehicle.platenumber if a.vehicle else None,
            })
        paginated['data'] = result
        paginated.pop('page_obj', None)
        return JsonResponse(paginated, safe=False)
    except Exception as e:
        print("DB Error (Admin Appointments):", e)
        return _json_error('Database error', 500)


@csrf_exempt
def review_appointment_view(request):
    """POST /api/appointments/review"""
    if request.method != 'POST':
        return _json_error('Method not allowed', 405)

    user_data = _get_session_user(request)
    if not user_data or user_data['role'] not in ['admin', 'manager', 'service-manager', 'top-manager']:
        return _json_error('Forbidden: Managers only.', 403)

    try:
        data = json.loads(request.body)
        appointment_id = data.get('appointment_id')
        action = data.get('action')

        if not appointment_id or action not in ['approve', 'reject']:
            return _json_error('Missing or invalid parameters')

        apt = Appointment.objects.filter(appointment_id=appointment_id).first()
        if not apt:
            return _json_error('Appointment not found', 404)

        if action == 'approve':
            apt.status = 'In Progress'
            apt.save()

            # Prevent duplicate Jobcards
            if not Jobcard.objects.filter(appointment=apt).exists():
                Jobcard.objects.create(
                    appointment=apt,
                    vehicle_id=apt.vehicle_id,
                    user_id=apt.user_id,
                    status='Scheduled',
                    createdat=datetime.datetime.now(),
                )
        else:
            apt.status = 'Cancelled'
            apt.save()

        return _json_ok()
    except Exception as e:
        print("DB Error (Review Appt):", e)
        return _json_error('Database error', 500)


# ========================================================================
#  SERVICE HISTORY
# ========================================================================

@csrf_exempt
def service_history_view(request):
    """GET /api/service-history"""
    if request.method != 'GET':
        return _json_error('Method not allowed', 405)

    user_data = _get_session_user(request)
    if not user_data or user_data['role'] not in ['admin', 'client', 'top-manager']:
        return _json_error('Forbidden', 403)

    try:
        qs = Appointment.objects.select_related('vehicle').annotate(
            status_priority=Case(
                When(status='Scheduled', then=Value(1)),
                When(status='Confirmed', then=Value(1)),
                When(status='In Progress', then=Value(2)),
                When(status='Completed', then=Value(3)),
                When(status='Cancelled', then=Value(4)),
                default=Value(5),
                output_field=IntegerField(),
            )
        ).order_by('status_priority', '-date_time')
        
        if user_data['role'] not in ['admin', 'top-manager']:
            qs = qs.filter(user_id=user_data['user_id'])
        
        vehicle_id = request.GET.get('vehicle_id')
        if vehicle_id:
            qs = qs.filter(vehicle_id=vehicle_id)

        status_filter = request.GET.get('status')
        if status_filter:
            qs = qs.filter(status__iexact=status_filter)

        paginated = _paginate_queryset(qs, request)
        result = []
        for a in paginated['page_obj']:
            row = {
                'Appointment_ID': a.appointment_id,
                'date_time': _serialize(a.date_time),
                'Status': a.status,
                'service_type': a.service_type,
                'Make': a.vehicle.make if a.vehicle else None,
                'Model': a.vehicle.model if a.vehicle else None,
                'Year': a.vehicle.year if a.vehicle else None,
                'PlateNumber': a.vehicle.platenumber if a.vehicle else None,
            }

            # For non-admin, fetch invoice info
            if user_data['role'] != 'admin':
                # Try finding invoice via Jobcard or direct link
                inv = Invoice.objects.filter(jobcard__appointment=a).first()
                if not inv:
                    jc = Jobcard.objects.filter(appointment=a).first()
                    inv = jc.invoice if jc else None

                if inv:
                    row['TotalCost'] = _serialize(inv.total)
                    row['Invoice_ID'] = inv.invoice_id
                else:
                    row['TotalCost'] = None
                    row['Invoice_ID'] = None

            result.append(row)

        paginated['data'] = result
        paginated.pop('page_obj', None)
        return JsonResponse(paginated, safe=False)
    except Exception as e:
        print("DB Error (service-history):", e)
        return _json_error('Database error', 500)


# ========================================================================
#  WORK ORDERS
# ========================================================================

@csrf_exempt
def work_orders_view(request):
    """GET /api/work-orders"""
    if request.method != 'GET':
        return _json_error('Method not allowed', 405)

    user_data = _get_session_user(request)
    if not user_data or user_data['role'] not in ['admin', 'manager', 'service-manager', 'technician', 'top-manager', 'finance-manager', 'stock-keeper']:
        return _json_error('Forbidden', 403)

    try:
        # Fetch all users with technician role
        techs_qs = Users.objects.filter(role__iexact='technician')
        technicians = []
        for t in techs_qs:
            status = 'Available'
            is_busy = Jobcard.objects.filter(technician_id=t.user_id, status='In Progress').exists()
            if is_busy:
                status = 'Busy'
            technicians.append({
                'user_id': t.user_id,
                'name': f"{t.firstname} {t.lastname}",
                'status': status
            })

        qs = Jobcard.objects.select_related('vehicle', 'user', 'appointment', 'technician')\
                           .prefetch_related('timelog_set')\
                           .order_by('-createdat')
        
        # If the user is a technician, show only their assigned jobs
        if user_data['role'] == 'technician':
            qs = qs.filter(technician_id=user_data['user_id'])
        
        # Filter by specific ID if matching
        job_id = request.GET.get('id')
        if job_id:
            try:
                qs = qs.filter(jobcard_id=int(job_id))
            except (ValueError, TypeError):
                qs = Jobcard.objects.none()

        paginated = _paginate_queryset(qs, request)
        result = []
        for j in paginated['page_obj']:
            item = {
                'JobCard_ID': j.jobcard_id,
                'Status': j.status,
                'CreatedAt': _serialize(j.createdat),
                'Vehicle_ID': j.vehicle.vehicle_id if j.vehicle else None,
                'Make': j.vehicle.make if j.vehicle else None,
                'Model': j.vehicle.model if j.vehicle else None,
                'Year': j.vehicle.year if j.vehicle else None,
                'PlateNumber': j.vehicle.platenumber if j.vehicle else None,
                'ClientName': f"{j.user.firstname} {j.user.lastname}" if j.user else None,
                'service_type': j.appointment.service_type if j.appointment else None,
                'Technician_ID': j.technician.user_id if j.technician else None,
                'TechnicianName': f"{j.technician.firstname} {j.technician.lastname}" if j.technician else None,
                'has_active_session': Timelog.objects.filter(jobcard_id=j.jobcard_id, user_id=user_data['user_id'], endtime__isnull=True).exists() if user_data['role'] == 'technician' else False,
                'technician_notes': j.technician_notes,
                'total_hours': float(j.total_hours or 0)
            }

            # If searching for a specific ID, include the linked inspection checklist
            if job_id:
                # Fallback: If no inspection is explicitly linked to the jobcard, find the latest for the vehicle
                insp = Inspection.objects.filter(jobcard_id=j.jobcard_id).order_by('-date').first()
                if not insp:
                    insp = Inspection.objects.filter(vehicle_id=j.vehicle_id).order_by('-date').first()
                
                if insp:
                    item['inspection'] = {
                        'id': insp.inspection_id,
                        'health_score': insp.healthscore,
                        'health_category': insp.healthcategory,
                        'results': insp.results,
                        'checklist': json.loads(insp.diagnosticdata) if insp.diagnosticdata else {}
                    }
                
                # (Inspection already included above)
                
                logs = Timelog.objects.filter(jobcard_id=j.jobcard_id).order_by('-timelog_id')
                item['time_logs'] = [
                    {
                        'id': log.timelog_id,
                        'start': log.starttime.isoformat() if log.starttime else None,
                        'end': log.endtime.isoformat() if log.endtime else None,
                        'total': float(log.totalhours or 0)
                    } for log in logs
                ]
            
            result.append(item)
            
        # Merge pagination metadata into the response
        paginated['work_orders'] = result
        paginated['technicians'] = technicians
        paginated.pop('page_obj', None)
        
        response = JsonResponse(paginated)
        patch_cache_control(response, no_cache=True, no_store=True, must_revalidate=True, private=True)
        return response
    except Exception as e:
        print("DB Error (Work Orders):", e)
        return _json_error('Database error', 500)


@csrf_exempt
def assign_work_order_view(request):
    """POST /api/assign-wo"""
    if request.method != 'POST':
        return _json_error('Method not allowed', 405)

    user_data = _get_session_user(request)
    if not user_data or user_data['role'] not in ['admin', 'manager', 'service-manager', 'top-manager']:
        return _json_error('Forbidden: Managers only.', 403)

    try:
        data = json.loads(request.body)
        jobcard_id = data.get('jobcard_id')
        technician_id = data.get('technician_id')

        if not jobcard_id:
            return _json_error('Missing jobcard_id')

        job = Jobcard.objects.filter(jobcard_id=jobcard_id).first()
        if not job:
            return _json_error('Jobcard not found', 404)

        if technician_id:
            tech = Users.objects.filter(user_id=technician_id, role__iexact='technician').first()
            if not tech:
                return _json_error('Technician not found', 404)

            job.technician = tech
            if job.status in ['Scheduled', 'Confirmed']:
                job.status = 'In Progress'
        else:
            job.technician = None
            if job.status == 'In Progress':
                job.status = 'Scheduled'

        job.save()

        return _json_ok()
    except Exception as e:
        print("DB Error (Assign WO):", e)
        return _json_error('Database error', 500)


@csrf_exempt
def update_work_order_status_view(request):
    """POST /api/update-wo-status"""
    if request.method != 'POST':
        return _json_error('Method not allowed', 405)

    user_data = _get_session_user(request)
    if not user_data:
        return _json_error('Unauthorized', 401)

    try:
        data = json.loads(request.body)
        jobcard_id = data.get('jobcard_id')
        new_status = data.get('status')
        note = data.get('note')

        if not jobcard_id:
            return _json_error('Missing jobcard_id')

        job = Jobcard.objects.filter(jobcard_id=jobcard_id).first()
        if not job:
            return _json_error('Work order not found', 404)

        # Permissions: Manager or the assigned Technician
        is_manager = user_data['role'] in ['admin', 'manager', 'service-manager', 'top-manager']
        is_assigned_tech = (user_data['role'] == 'technician' and job.technician_id == user_data['user_id'])

        if not (is_manager or is_assigned_tech):
            return _json_error('Forbidden: You are not authorized to update this work order.', 403)

        if new_status:
            # Prevent updating if already closed (unless manager)
            if job.status == 'Closed' and not is_manager:
                return _json_error('Cannot update a closed work order.', 400)
            
            # Simple validation
            valid_statuses = ['Scheduled', 'Confirmed', 'In Progress', 'Completed', 'Cancelled']
            if new_status not in valid_statuses:
                return _json_error(f'Invalid status: {new_status}')
                
            if new_status.lower() == 'completed':
                # Update appointment status and award loyalty points
                from .models import Appointment
                app = Appointment.objects.filter(appointment_id=job.appointment_id).first()
                if app and app.status.lower() != 'completed':
                    app.status = 'Completed'
                    app.save()
                    _award_loyalty_point(app.user_id)
                    
                    # Notify Client via Email
                    try:
                        from .models import Users
                        client = Users.objects.filter(user_id=app.user_id).first()
                        if client and client.email:
                            vehicle_name = f"{app.vehicle.year or ''} {app.vehicle.make} {app.vehicle.model}".strip()
                            _send_service_completion_email(
                                client.email, 
                                f"{client.firstname} {client.lastname}",
                                vehicle_name,
                                app.appointment_id
                            )
                    except Exception as e:
                        print(f"Failed to trigger completion email: {e}")
            
            job.status = new_status
            job.save()

        if note:
            # Persistent Tech Notes column
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
            user_name = user_data.get('name', 'User')
            new_note_entry = f"[{timestamp}] {user_name}: {note}\n"
            
            # Update Technician_Notes column
            job.technician_notes = (job.technician_notes or "") + new_note_entry

        job.save()
        return _json_ok()
    except Exception as e:
        print("DB Error (Update WO Status):", e)
        return _json_error('Database error', 500)


@csrf_exempt
def log_work_time_view(request):
    """POST /api/log-time"""
    if request.method != 'POST':
        return _json_error('Method not allowed', 405)

    user_data = _get_session_user(request)
    print(f"[log-time] user_data={user_data}")
    if not user_data or user_data['role'] != 'technician':
        return _json_error('Forbidden: Technicians only.', 403)

    try:
        data = json.loads(request.body)
        jobcard_id = data.get('jobcard_id')
        action = data.get('action')
        print(f"[log-time] jobcard_id={jobcard_id!r} action={action!r}")

        if not jobcard_id or action not in ['start', 'end']:
            return _json_error('Missing jobcard_id or invalid action')

        job = Jobcard.objects.filter(jobcard_id=jobcard_id).first()
        if not job:
            return _json_error('Work order not found', 404)

        from django.utils import timezone as tz
        now = tz.now()

        if action == 'start':
            # Check if there's already an active session for this job
            active_log = Timelog.objects.filter(
                jobcard_id=jobcard_id,
                user_id=user_data['user_id'],
                endtime__isnull=True
            ).first()
            if active_log:
                return _json_error('You already have an active work session.')

            Timelog.objects.create(
                jobcard_id=jobcard_id,
                user_id=user_data['user_id'],
                starttime=now
            )
            # Move status to In Progress automatically
            job.status = 'In Progress'
            job.save()
            return _json_ok()

        elif action == 'end':
            # Find any active (unclosed) session for this jobcard
            active_log = Timelog.objects.filter(
                jobcard_id=jobcard_id,
                endtime__isnull=True
            ).first()
            print(f"[log-time] end: active_log={active_log}")
            if not active_log:
                return _json_error('No active work session. Click Start Work first.')

            active_log.endtime = now
            # Handle legacy naive starttime safely
            starttime = active_log.starttime
            if starttime and starttime.tzinfo is None:
                starttime = tz.make_aware(starttime)
            duration = now - starttime
            hours = duration.total_seconds() / 3600.0
            active_log.totalhours = decimal.Decimal(str(round(hours, 2)))
            active_log.save()
            print(f"[log-time] saved endtime={active_log.endtime} hours={active_log.totalhours}")

            # Sum all sessions and mark Completed
            all_logs = Timelog.objects.filter(jobcard_id=jobcard_id)
            total = sum(log.totalhours or 0 for log in all_logs)
            job.total_hours = decimal.Decimal(str(round(float(total), 2)))
            job.status = 'Completed'
            job.save()
            # award point if appointment exists
            if job.appointment and job.appointment.status != 'Completed':
                job.appointment.status = 'Completed'
                job.appointment.save()
                _award_loyalty_point(job.appointment.user_id)
                
                # Notify Client via Email
                try:
                    from .models import Users
                    client = Users.objects.filter(user_id=job.appointment.user_id).first()
                    if client and client.email:
                        vehicle_name = f"{job.vehicle.year or ''} {job.vehicle.make} {job.vehicle.model}".strip()
                        _send_service_completion_email(
                            client.email, 
                            f"{client.firstname} {client.lastname}",
                            vehicle_name,
                            job.appointment_id
                        )
                except Exception as e:
                    print(f"Failed to trigger completion email (log_time): {e}")
            return _json_ok()

    except Exception as e:
        print("DB Error (Log Time):", e)
        return _json_error(str(e), 500)




    return _json_error('Method not allowed', 405)


@csrf_exempt
def parts_approval_api(request):
    """GET /api/parts-approval  — list all pending requests
       POST /api/parts-approval — approve or reject a request"""
    user_data = _get_session_user(request)
    if not user_data:
        return _json_error('Unauthorized', 401)

    if request.method == 'GET':
        try:
            status_filter = request.GET.get('status', 'all')
            qs = Jobcardparts.objects.select_related('item').order_by('-id')
            if status_filter and status_filter.lower() != 'all':
                qs = qs.filter(status=status_filter)

            # Summary counts across ALL records (not just current page)
            all_qs = Jobcardparts.objects.all()
            pending_count = all_qs.filter(status='Pending').count()
            approved_count = all_qs.filter(status='Approved').count()
            rejected_count = all_qs.filter(status='Rejected').count()

            paginated = _paginate_queryset(qs, request)

            # Build a tech_name map from current page jobcard IDs
            all_jc_ids = [r.jobcard_id for r in paginated['page_obj']]
            tech_map = {}
            if all_jc_ids:
                from django.db import connection
                with connection.cursor() as cur:
                    placeholders = ','.join(['%s'] * len(all_jc_ids))
                    cur.execute(
                        f"SELECT jc.JobCard_ID, u.FirstName, u.LastName "
                        f"FROM jobcard jc "
                        f"JOIN technician t ON t.User_ID = jc.Technician_ID "
                        f"JOIN users u ON u.User_ID = t.User_ID "
                        f"WHERE jc.JobCard_ID IN ({placeholders})",
                        all_jc_ids
                    )
                    for row in cur.fetchall():
                        tech_map[row[0]] = f"{row[1] or ''} {row[2] or ''}".strip()

            result = []
            for r in paginated['page_obj']:
                result.append({
                    'id': r.id,
                    'JobCard_ID': r.jobcard_id,
                    'ItemName': r.item.name if r.item else 'Unknown',
                    'Quantity': r.quantityused,
                    'Status': r.status or 'Pending',
                    'RequestedBy': tech_map.get(r.jobcard_id, '—'),
                })
            paginated['data'] = result
            paginated['pending_count'] = pending_count
            paginated['approved_count'] = approved_count
            paginated['rejected_count'] = rejected_count
            paginated.pop('page_obj', None)
            return JsonResponse(paginated, safe=False)
        except Exception as e:
            return _json_error(str(e), 500)

    elif request.method == 'POST':
        if user_data['role'] not in ['admin', 'manager', 'service-manager', 'stockkeeper', 'top-manager']:
            return _json_error('Not authorized to approve.', 403)
        try:
            data = json.loads(request.body)
            req_id = data.get('id')
            action = data.get('action')  # 'approve' or 'reject'
            if not req_id or action not in ['approve', 'reject']:
                return _json_error('Missing id or invalid action')
            row = Jobcardparts.objects.select_related('item').filter(id=req_id).first()
            if not row:
                return _json_error('Request not found', 404)
            
            new_status = 'Approved' if action == 'approve' else 'Rejected'
            
            # --- Stock Deduction Logic ---
            if action == 'approve' and row.status != 'Approved':
                # Attempt to deduct from Inventoryitem (Internal Stock)
                if row.item:
                    if row.item.stockqty >= row.quantityused:
                        row.item.stockqty -= row.quantityused
                        row.item.save()
                    else:
                        return _json_error(f"Insufficient stock in Inventory: {row.item.name} (Available: {row.item.stockqty})")
                
                # Also check matching SupplierPart if needed (as per user screenshot)
                from core.models import SupplierPart
                # Find matching part by name/code to deduct from "Total Warehouse Stock"
                sup_part = SupplierPart.objects.filter(name=row.item.name).first()
                if sup_part:
                    if sup_part.quantity >= row.quantityused:
                        sup_part.quantity -= row.quantityused
                        sup_part.save()

            row.status = new_status
            row.save()
            return _json_ok({'message': f'Request {row.status}'})
        except Exception as e:
            return _json_error(str(e), 500)

    return _json_error('Method not allowed', 405)


def complete_work_order_view(request):
    """POST /api/complete-wo"""
    if request.method != 'POST':
        return _json_error('Method not allowed', 405)

    user_data = _get_session_user(request)
    if not user_data or user_data['role'] not in ['admin', 'manager', 'service-manager', 'technician', 'top-manager']:
        return _json_error('Forbidden.', 403)

    try:
        data = json.loads(request.body)
        jobcard_id = data.get('jobcard_id')
        labor_cost = data.get('labor_cost', 0)
        parts_cost = data.get('parts_cost', 0)

        if not jobcard_id:
            return _json_error('Missing jobcard_id')

        total_cost = float(labor_cost) + float(parts_cost)

        job = Jobcard.objects.select_related('appointment').filter(jobcard_id=jobcard_id).first()
        if not job or not job.appointment:
            return _json_error('Jobcard not found', 404)

        client_id = job.appointment.user_id
        now = datetime.datetime.now()

        # Update jobcard
        job.totallaborcost = labor_cost
        job.totalpartscost = parts_cost
        job.status = 'Completed'
        job.save()

        # Update appointment status and award loyalty points
        if job.appointment:
            if job.appointment.status != 'Completed':
                job.appointment.status = 'Completed'
                job.appointment.save()
                _award_loyalty_point(job.appointment.user_id)

                # Notify Client via Email
                try:
                    from .models import Users
                    client = Users.objects.filter(user_id=job.appointment.user_id).first()
                    if client and client.email:
                        vehicle_name = f"{job.vehicle.year or ''} {job.vehicle.make} {job.vehicle.model}".strip()
                        _send_service_completion_email(
                            client.email, 
                            f"{client.firstname} {client.lastname}",
                            vehicle_name,
                            job.appointment_id
                        )
                except Exception as e:
                    print(f"Failed to trigger completion email (complete_wo): {e}")

        return _json_ok()
    except Exception as e:
        print("DB Error (Complete WO):", e)
        return _json_error('Database error', 500)


# ========================================================================
#  INVOICE VIEWS
# ========================================================================

# --- Fixed Service Prices (EGP) ---
SERVICE_PRICES = {
    'Oil Change & Filter': 350,
    'Brake Inspection': 300,
    'Engine Diagnostics': 600,
    'Tyre Replacement': 200,
    'AC Service': 500,
    'Battery Replacement': 150,
    'Car Wash': 100,
    'Suspension Check': 400,
    'Transmission Service': 800,
    'Fuel System Cleaning': 450,
    'Wheel Alignment': 350,
    'Car Detailing': 600,
    'Electrical System Check': 300,
    'General Service': 500,
}
TAX_RATE = 0.14  # 14% VAT

@csrf_exempt
def invoice_preview_view(request):
    """GET /api/invoice-preview?jobcard_id=X  — returns auto-calculated amounts for a jobcard"""
    user_data = _get_session_user(request)
    if not user_data or user_data['role'] not in ['admin', 'manager', 'service-manager', 'finance-manager', 'top-manager']:
        return _json_error('Forbidden', 403)

    jobcard_id = request.GET.get('jobcard_id')
    if not jobcard_id:
        return _json_error('jobcard_id is required')

    try:
        jc = Jobcard.objects.select_related('appointment', 'vehicle', 'user').filter(jobcard_id=jobcard_id).first()
        if not jc:
            return _json_error('JobCard not found', 404)
        
        if jc.invoice_id:
            return _json_error('This JobCard has already been invoiced.', 400)

        # --- Service Price from appointment service_type ---
        service_type = jc.appointment.service_type if jc.appointment else 'General Service'
        labor_price = SERVICE_PRICES.get(service_type, 500)

        # --- Inspection fee removed per user request (replaced by book check) ---
        inspection = Inspection.objects.filter(jobcard=jc).first()
        inspection_fee = 0

        # --- Parts cost from jobcardparts ---
        parts_qs = Jobcardparts.objects.filter(jobcard=jc).select_related('item')
        parts_total = 0
        parts_list = []
        for p in parts_qs:
            unit_price = float(p.item.unitprice or 0)
            qty = p.quantityused or 0
            line_total = round(unit_price * qty, 2)
            parts_total += line_total
            parts_list.append({
                'name': p.item.name,
                'qty': qty,
                'unit_price': unit_price,
                'total': line_total,
            })

        subtotal_labor = round(labor_price + inspection_fee, 2)
        subtotal_parts = round(parts_total, 2)
        subtotal = round(subtotal_labor + subtotal_parts, 2)
        
        # Calculate tax on full subtotal
        tax = round(subtotal * TAX_RATE, 2)
        
        # Initial total before discount
        total = round(subtotal + tax, 2)

        return JsonResponse({
            'JobCard_ID': jc.jobcard_id,
            'ClientEmail': jc.user.email if jc.user else None,
            'ClientName': f"{jc.user.firstname} {jc.user.lastname}" if jc.user else None,
            'User_ID': jc.user_id,
            'service_type': service_type,
            'vehicle': f"{jc.vehicle.make} {jc.vehicle.model} ({jc.vehicle.platenumber})" if jc.vehicle else None,
            'has_inspection': inspection is not None,
            'inspection_fee': inspection_fee,
            'labor_price': labor_price,
            'parts': parts_list,
            'subtotal_labor': subtotal_labor,
            'subtotal_parts': subtotal_parts,
            'tax': tax,
            'total': total,
        })
    except Exception as e:
        print("DB Error (invoice_preview):", e)
        return _json_error('Database error', 500)



@csrf_exempt
def client_invoices_view(request):
    """GET /api/invoices"""
    if request.method != 'GET':
        return _json_error('Method not allowed', 405)

    user_data = _get_session_user(request)
    if not user_data or user_data['role'] != 'client':
        return _json_error('Forbidden', 403)

    try:
        uid = user_data['user_id']

        # All unpaid invoices for this user
        all_unpaid = list(Invoice.objects.filter(
            user_id=uid, status='Unpaid'
        ).select_related('jobcard__appointment').order_by('-invoicedate'))

        # Separate: check invoices vs service invoices
        check_unpaid_mapped = []
        service_unpaid_mapped = []
        for inv in all_unpaid:
            jc = inv.jobcard
            is_check = (
                jc is not None and
                jc.appointment is not None and
                (jc.appointment.service_type or '').strip().lower() == 'check'
            )
            entry = {
                'Invoice_ID': inv.invoice_id,
                'InvoiceDate': _serialize(inv.invoicedate),
                'DueDate': _serialize(inv.duedate or (inv.invoicedate + datetime.timedelta(days=14) if inv.invoicedate else None)),
                'Total': _serialize(inv.total),
                'Status': 'Check-Unpaid' if is_check else 'Unpaid',
                'is_check': is_check,
            }
            if is_check:
                check_unpaid_mapped.append(entry)
            else:
                service_unpaid_mapped.append(entry)

        # All paid — separate check vs service via payment → invoice → jobcard → appointment
        all_paid_payments = Payment.objects.filter(
            user_id=uid,
            invoice__status='Paid'
        ).select_related('invoice__jobcard__appointment').order_by('-paymentdate')

        paginated = _paginate_queryset(all_paid_payments, request)
        paid_mapped = []
        check_paid_mapped = []
        for p in paginated['page_obj']:
            inv = p.invoice
            is_check = False
            if inv:
                jc = inv.jobcard
                is_check = (
                    jc is not None and
                    jc.appointment is not None and
                    (jc.appointment.service_type or '').strip().lower() == 'check'
                )
            entry = {
                'Invoice_ID': p.invoice_id,
                'Total': _serialize(inv.total) if inv else None,
                'Status': 'Check-Paid' if is_check else 'Paid',
                'PaymentDate': _serialize(p.paymentdate),
                'Method': p.method,
                'is_check': is_check,
            }
            if is_check:
                check_paid_mapped.append(entry)
            else:
                paid_mapped.append(entry)

        paginated['paid_data'] = paid_mapped
        paginated.pop('page_obj', None)
        return JsonResponse({
            'unpaid': service_unpaid_mapped,
            'paid_paginated': paginated,
            'check_unpaid': check_unpaid_mapped,
            'check_paid': check_paid_mapped,
        })
    except Exception as e:
        print("DB Error:", e)
        return _json_error('Database error', 500)


@csrf_exempt
def admin_invoices_view(request):
    """GET/POST /api/admin/invoices"""
    user_data = _get_session_user(request)
    if not user_data or user_data['role'] not in ['admin', 'manager', 'finance-manager', 'top-manager']:
        return _json_error('Forbidden', 403)

    if request.method == 'GET':
        try:
            qs = Invoice.objects.select_related('user').order_by('-invoicedate')
            
            # Calculate grand totals for KPIs (across all pages)
            total_count = Invoice.objects.count()
            paid_count = Invoice.objects.filter(status='Paid').count()
            unpaid_count = Invoice.objects.exclude(status='Paid').count()
            
            from django.db.models import Sum
            rev_collected = Invoice.objects.filter(status='Paid').aggregate(Sum('total'))['total__sum'] or 0
            
            paginated = _paginate_queryset(qs, request)
            result = []
            for inv in paginated['page_obj']:
                client_name = f"{inv.user.firstname} {inv.user.lastname}" if inv.user else None
                result.append({
                    'Invoice_ID': inv.invoice_id,
                    'Total': _serialize(inv.total),
                    'SubtotalLabor': _serialize(inv.subtotallabor),
                    'SubtotalParts': _serialize(inv.subtotalparts),
                    'Tax': _serialize(inv.tax),
                    'Discount': _serialize(inv.discount),
                    'Status': inv.status,
                    'DueDate': _serialize(inv.duedate),
                    'InvoiceDate': _serialize(inv.invoicedate),
                    'ClientEmail': inv.user.email if inv.user else None,
                    'ClientName': client_name,
                    'User_ID': inv.user_id,
                    'JobCard_ID': inv.jobcard_id or (Jobcard.objects.filter(invoice=inv).first().jobcard_id if Jobcard.objects.filter(invoice=inv).exists() else None),
                })
            paginated['data'] = result
            paginated['total_count'] = total_count
            paginated['paid_count'] = paid_count
            paginated['unpaid_count'] = unpaid_count
            paginated['revenue_collected'] = float(rev_collected)
            paginated.pop('page_obj', None)
            return JsonResponse(paginated, safe=False)
        except Exception as e:
            print("DB Error (Admin Invoices GET):", e)
            return _json_error('Database error', 500)

    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
            jobcard_id = data.get('jobcard_id')
            discount = float(data.get('discount', 0))
            due_date_str = data.get('due_date')

            if not jobcard_id:
                return _json_error('jobcard_id is required')

            jc = Jobcard.objects.select_related('appointment', 'vehicle', 'user').filter(jobcard_id=jobcard_id).first()
            if not jc:
                return _json_error('JobCard not found', 404)
            
            if jc.invoice_id:
                return _json_error('This JobCard already has an invoice.', 400)

            if not jc.user:
                return _json_error('JobCard has no associated client')

            # Auto-calculate from service prices
            service_type = jc.appointment.service_type if jc.appointment else 'General Service'
            labor_price = SERVICE_PRICES.get(service_type, 500)

            inspection = Inspection.objects.filter(jobcard=jc).first()
            inspection_fee = 0

            parts_qs = Jobcardparts.objects.filter(jobcard=jc).select_related('item')
            parts_total = sum(float(p.item.unitprice or 0) * (p.quantityused or 0) for p in parts_qs)

            subtotal_labor = round(labor_price + inspection_fee, 2)
            subtotal_parts = round(parts_total, 2)
            subtotal = round(subtotal_labor + subtotal_parts, 2)
            
            # Tax on full subtotal
            tax = round(subtotal * TAX_RATE, 2)
            
            # Total after tax, then subtract discount as requested by user
            total = round(subtotal + tax - discount, 2)

            invoice_date_str = data.get('invoice_date')
            due_date_str = data.get('due_date')
            
            invoice_date = datetime.date.today()
            if invoice_date_str:
                try:
                    parsed_date = datetime.datetime.strptime(invoice_date_str, '%Y-%m-%d').date()
                    if parsed_date >= datetime.date.today():
                        invoice_date = parsed_date
                except Exception: pass

            due_date = None
            if due_date_str:
                try:
                    parsed_due = datetime.datetime.strptime(due_date_str, '%Y-%m-%d').date()
                    if parsed_due >= invoice_date:
                        due_date = parsed_due
                except Exception:
                    pass
            
            if not due_date:
                due_date = invoice_date + datetime.timedelta(days=14)

            invoice = Invoice.objects.create(
                user_id=jc.user_id,
                invoicedate=invoice_date,
                duedate=due_date,
                jobcard=jc,
                subtotallabor=subtotal_labor,
                subtotalparts=subtotal_parts,
                tax=tax,
                discount=discount,
                total=total,
                status='Unpaid',
            )

            # Link the jobcard to the invoice and mark as completed
            jc.invoice = invoice
            jc.status = 'Completed'
            jc.save()

            if jc.appointment:
                if jc.appointment.status != 'Completed':
                    jc.appointment.status = 'Completed'
                    jc.appointment.save()
                    _award_loyalty_point(jc.appointment.user_id)

            return _json_ok({'Invoice_ID': invoice.invoice_id, 'Total': total})
        except Exception as e:
            print("DB Error (Admin Invoices POST):", e)
            return _json_error(str(e), 500)

    return _json_error('Method not allowed', 405)


# ========================================================================
#  PAYMENT VIEWS
# ========================================================================

@csrf_exempt
def finance_stats_view(request):
    """GET /api/finance/stats — stats for reports (Revenue, aging, etc)"""
    user_data = _get_session_user(request)
    if not user_data or user_data['role'] not in ['admin', 'manager', 'finance-manager', 'top-manager']:
        return _json_error('Forbidden', 403)
    
    try:
        # 1. Total Revenue (Paid) - Starting from 2026
        paid_total = Invoice.objects.filter(status='Paid', invoicedate__year__gte=2026).aggregate(Sum('total'))['total__sum'] or 0
        unpaid_total = Invoice.objects.filter(status='Unpaid', invoicedate__year__gte=2026).aggregate(Sum('total'))['total__sum'] or 0
        
        # 2. Get available years for the filter (Only 2026 onwards)
        year_qs = Invoice.objects.filter(invoicedate__year__gte=2026).values_list('invoicedate__year', flat=True).distinct()
        year_list = sorted(list(year_qs), reverse=True)
        if not year_list: 
            year_list = [2026]
        
        # 3. Monthly Revenue for selected year
        y_param = request.GET.get('year', '')
        selected_year = int(y_param) if y_param and y_param.isdigit() else 2026
        if selected_year < 2026: selected_year = 2026
        
        monthly_data = []
        for m in range(1, 13):
            month_sum = Invoice.objects.filter(
                invoicedate__year=selected_year, 
                invoicedate__month=m,
                status='Paid'
            ).aggregate(Sum('total'))['total__sum'] or 0
            
            monthly_data.append({
                'month': datetime.date(2000, m, 1).strftime('%b'),
                'amount': float(month_sum)
            })

        # 3. Aging
        aging = {'0-30': 0.0, '31-60': 0.0, '61-90': 0.0, '90+': 0.0}
        unpaid_invoices = Invoice.objects.filter(status='Unpaid')
        for inv in unpaid_invoices:
            if inv.invoicedate:
                diff = (datetime.date.today() - inv.invoicedate).days
                if diff <= 30: aging['0-30'] += float(inv.total)
                elif diff <= 60: aging['31-60'] += float(inv.total)
                elif diff <= 90: aging['61-90'] += float(inv.total)
                else: aging['90+'] += float(inv.total)

        total_count = Invoice.objects.count()
        unpaid_count = Invoice.objects.filter(status='Unpaid').count()

        return JsonResponse({
            'paid_total': float(paid_total),
            'unpaid_total': float(unpaid_total),
            'unpaid_count': unpaid_count,
            'monthly_revenue': monthly_data,
            'available_years': year_list,
            'selected_year': selected_year,
            'aging': aging,
            'total_items': total_count
        })
    except Exception as e:
        print("Stats Error:", e)
        return _json_error(str(e), 500)

@require_GET
def maintenance_stats_view(request):
    """GET /api/maintenance-stats?year=2026&vehicle_id=123"""
    user_data = _get_session_user(request)
    if not user_data:
        return _json_error('Unauthorized', 401)
    
    try:
        year = int(request.GET.get('year', datetime.date.today().year))
        vehicle_id = request.GET.get('vehicle_id')
        
        # Base query: Invoices for this user's vehicles
        qs = Invoice.objects.filter(user_id=user_data['user_id'], invoicedate__year=year)
        
        # Calculate TOTAL UNPAID BALANCE for this user (not limited by year)
        from django.db.models import Sum
        unpaid_balance = Invoice.objects.filter(user_id=user_data['user_id'], status='Unpaid').aggregate(total=Sum('total'))['total'] or 0
        
        if vehicle_id and vehicle_id != 'all':
            qs = qs.filter(jobcard__vehicle_id=vehicle_id)
            
        # Group by month (1 to 12)
        monthly_data = [0.0] * 12
        results = qs.values('invoicedate__month').annotate(total=Sum('total'))
        
        for r in results:
            m = r['invoicedate__month']
            if m and 1 <= m <= 12:
                monthly_data[m-1] = float(r['total'] or 0)
                
        return JsonResponse({
            'success': True, 
            'data': monthly_data,
            'unpaid_balance': float(unpaid_balance)
        })
    except Exception as e:
        print("Maintenance Stats Error:", e)
        return _json_error(str(e))



@csrf_exempt
def admin_payments_view(request):
    """GET /api/admin/payments — list all payments (Finance Manager view)"""
    if request.method != 'GET':
        return _json_error('Method not allowed', 405)
    user_data = _get_session_user(request)
    if not user_data or user_data['role'] not in ['admin', 'manager', 'finance-manager', 'top-manager']:
        return _json_error('Forbidden', 403)
    try:
        qs = Payment.objects.select_related('user', 'invoice').order_by('-paymentdate')
        
        # Calculate grand totals for KPIs (across all pages)
        total_payments_count = Payment.objects.count()
        from django.db.models import Sum
        total_collected_val = Payment.objects.aggregate(Sum('amount'))['amount__sum'] or 0
        
        paginated = _paginate_queryset(qs, request)
        result = []
        for p in paginated['page_obj']:
            result.append({
                'Payment_ID': p.payment_id,
                'Invoice_ID': p.invoice_id,
                'User_ID': p.user_id,
                'ClientEmail': p.user.email if p.user else None,
                'ClientName': f"{p.user.firstname} {p.user.lastname}" if p.user else None,
                'Amount': str(p.amount),
                'Method': p.method,
                'PaymentDate': str(p.paymentdate) if p.paymentdate else None,
            })
        paginated['data'] = result
        paginated['total_payments_count'] = total_payments_count
        paginated['total_collected'] = float(total_collected_val)
        paginated.pop('page_obj', None)
        return JsonResponse(paginated, safe=False)
    except Exception as e:
        print("DB Error (Admin Payments):", e)
        return _json_error('Database error', 500)


@csrf_exempt
def admin_mark_paid_view(request, invoice_id):
    """POST /api/admin/invoices/<id>/mark-paid — Finance Manager marks an invoice as paid"""
    if request.method != 'POST':
        return _json_error('Method not allowed', 405)
    user_data = _get_session_user(request)
    if not user_data or user_data['role'] not in ['admin', 'manager', 'finance-manager']:
        return _json_error('Forbidden', 403)
    try:
        data = json.loads(request.body) if request.body else {}
        method = data.get('method', 'CreditCard')
        if method not in ['CreditCard']:
            method = 'CreditCard'

        invoice = Invoice.objects.filter(invoice_id=invoice_id).first()
        if not invoice:
            return _json_error('Invoice not found', 404)
        if invoice.status == 'Paid':
            return _json_error('Invoice already paid')

        Payment.objects.create(
            user_id=invoice.user_id,
            invoice=invoice,
            paymentdate=datetime.date.today(),
            amount=invoice.total,
            method=method,
        )
        # 1. Update Invoice status first
        invoice.status = 'Paid'
        invoice.save()

        # 2. AGGRESSIVE SYNC: Update EVERY possible linked record
        # Path A: Explicit link on Invoice object
        if invoice.jobcard:
            invoice.jobcard.status = 'Completed'
            invoice.jobcard.save()
            if invoice.jobcard.appointment:
                if invoice.jobcard.appointment.status != 'Completed':
                    invoice.jobcard.appointment.status = 'Completed'
                    invoice.jobcard.appointment.save()
                    _award_loyalty_point(invoice.jobcard.appointment.user_id)

        # Path B: Find via Jobcards that point to THIS invoice
        # (This handles the case where multiple jobcards might be linked)
        from .models import Jobcard, Appointment
        linked_jobs = Jobcard.objects.filter(invoice=invoice)
        for j in linked_jobs:
            j.status = 'Completed'
            j.save()
            if j.appointment:
                if j.appointment.status != 'Completed':
                    j.appointment.status = 'Completed'
                    j.appointment.save()
                    _award_loyalty_point(j.appointment.user_id)

        return _json_ok({'message': f'Invoice marked as Paid via {method}'})
    except Exception as e:
        print("DB Error (Mark Paid):", e)
        return _json_error('Database error', 500)


VALID_PAYMENT_METHODS = ['CreditCard']

@csrf_exempt
def payments_view(request):
    """POST /api/payments"""
    if request.method != 'POST':
        return _json_error('Method not allowed', 405)

    user_data = _get_session_user(request)
    if not user_data:
        return _json_error('Not logged in', 401)

    try:
        data = json.loads(request.body)
        invoice_id = data.get('invoice_id')
        method = data.get('method', '').strip()

        if not invoice_id or not method:
            return _json_error('Missing required fields: invoice_id and method')

        if method not in VALID_PAYMENT_METHODS:
            return _json_error(f"Invalid payment method. Choose from: {', '.join(VALID_PAYMENT_METHODS)}")

        invoice = Invoice.objects.filter(
            invoice_id=invoice_id,
            user_id=user_data['user_id']
        ).select_related('jobcard__appointment').first()

        if not invoice:
            return _json_error('Invoice not found or not yours', 404)

        if invoice.status == 'Paid':
            return _json_error('Invoice is already paid')

        # Detect if this is a Check invoice via the linked jobcard → appointment
        from .models import Jobcard, Appointment
        jc = invoice.jobcard
        is_check_invoice = (
            jc is not None and
            jc.appointment is not None and
            (jc.appointment.service_type or '').strip().lower() == 'check'
        )

        # Apply loyalty points logic
        user = Users.objects.filter(user_id=user_data['user_id']).first()
        final_amount = invoice.total
        points_to_deduct = 0

        if user:
            # 30+ points: Checks are free
            if is_check_invoice and (user.loyalty_points or 0) >= 30:
                final_amount = 0
                points_to_deduct = 30
            # 20+ points: 50% discount on anything
            elif (user.loyalty_points or 0) >= 20:
                from decimal import Decimal
                final_amount = invoice.total * Decimal('0.5')
                points_to_deduct = 20

        if points_to_deduct > 0:
            user.loyalty_points = max(0, (user.loyalty_points or 0) - points_to_deduct)
            user.save()
            
            # Update the invoice record to permanently reflect the discount
            from decimal import Decimal
            loyalty_discount_val = Decimal(str(invoice.total)) - Decimal(str(final_amount))
            invoice.discount = (invoice.discount or 0) + loyalty_discount_val
            invoice.total = final_amount

        Payment.objects.create(
            user_id=user_data['user_id'],
            invoice=invoice,
            paymentdate=datetime.date.today(),
            amount=final_amount,
            method=method,
        )
        invoice.status = 'Paid'
        invoice.save()

        if is_check_invoice:
            # Check invoice paid → activate Jobcard to Scheduled for technician
            if jc.status == 'Pending Payment':
                jc.status = 'Scheduled'
                jc.save()
            Jobcard.objects.filter(invoice=invoice, status='Pending Payment').update(status='Scheduled')
            return _json_ok({'message': f'Check invoice paid via {method}. Your inspection is now scheduled!'})

        # --- Regular service invoice flow → Completed ---
        def _is_check(appt):
            return appt and (appt.service_type or '').strip().lower() == 'check'

        def _update_job(j):
            if _is_check(j.appointment):
                j.status = 'Scheduled'
            else:
                if j.status != 'Completed':
                    j.status = 'Completed'
                    if j.appointment:
                        if j.appointment.status != 'Completed':
                            j.appointment.status = 'Completed'
                            j.appointment.save()
                            _award_loyalty_point(j.appointment.user_id)
                    j.save()

        if invoice.jobcard:
            _update_job(invoice.jobcard)
        for j in Jobcard.objects.filter(invoice=invoice):
            _update_job(j)

        return _json_ok({'message': f'Payment via {method} recorded successfully!'})
    except Exception as e:
        print("DB Error (Add Payment):", e)
        return _json_error('Database error', 500)




# ========================================================================
#  INVENTORY VIEWS
# ========================================================================

@csrf_exempt
def inventory_list_create(request):
    """GET/POST /api/inventory"""
    if request.method == 'GET':
        try:
            from django.db.models import F, Q, Sum
            
            # Global KPIs
            low_stock_count = Inventoryitem.objects.filter(stockqty__lte=F('minstocklevel')).count()
            total_items = Inventoryitem.objects.count()
            stock_value_agg = Inventoryitem.objects.aggregate(total_val=Sum(F('stockqty') * F('unitprice')))
            total_stock_value = stock_value_agg['total_val'] or 0
            
            qs = Inventoryitem.objects.all().order_by('item_id')
            
            # Filter by low stock if requested
            if request.GET.get('filter') == 'lowstock':
                qs = qs.filter(stockqty__lte=F('minstocklevel'))
            
            # Search by name or item number
            search_query = request.GET.get('q')
            if search_query:
                qs = qs.filter(Q(name__icontains=search_query) | Q(itemnumber__icontains=search_query))

            paginated = _paginate_queryset(qs, request)
            result = [{
                'Item_ID': i.item_id,
                'ItemNumber': i.itemnumber,
                'Name': i.name,
                'UnitPrice': _serialize(i.unitprice),
                'StockQty': i.stockqty,
                'MinStockLevel': i.minstocklevel,
            } for i in paginated['page_obj']]
            
            paginated['data'] = result
            paginated['low_stock_count'] = low_stock_count
            paginated['total_items'] = total_items
            paginated['total_stock_value'] = float(total_stock_value)
            paginated.pop('page_obj', None)
            return JsonResponse(paginated, safe=False)
        except Exception as e:
            print("DB Error (Inventory GET):", e)
            return _json_error('Database error', 500)

    elif request.method == 'POST':
        user_data = _get_session_user(request)
        if not user_data:
            return _json_error('Not logged in', 401)

        try:
            data = json.loads(request.body)
            item_number = int(data.get('item_number')) if data.get('item_number') else None
            name = data.get('name')
            stock_qty = int(data.get('stock_qty', 0))
            min_stock = int(data.get('min_stock', 0))
            unit_price = float(data.get('unit_price', 0))

            if item_number is None or not name:
                return _json_error('Missing required fields')

            Inventoryitem.objects.create(
                itemnumber=item_number,
                name=name,
                unitprice=unit_price,
                stockqty=stock_qty,
                minstocklevel=min_stock,
                user_id=user_data['user_id'],
            )
            return _json_ok()
        except Exception as e:
            print("DB Error (Inventory POST):", e)
            return JsonResponse({'error': str(e), 'success': False}, status=500)

    return _json_error('Method not allowed', 405)


@csrf_exempt
def inventory_detail(request, item_id):
    """PUT/DELETE /api/inventory/<id>"""
    if request.method == 'PUT':
        try:
            data = json.loads(request.body)
            item = Inventoryitem.objects.get(item_id=item_id)
            item.itemnumber = data.get('item_number', item.itemnumber)
            item.name = data.get('name', item.name)
            item.unitprice = data.get('unit_price', item.unitprice)
            item.stockqty = data.get('stock_qty', item.stockqty)
            item.minstocklevel = data.get('min_stock', item.minstocklevel)
            item.save()
            return _json_ok()
        except Inventoryitem.DoesNotExist:
            return _json_error('Item not found', 404)
        except Exception as e:
            print("DB Error (Inventory PUT):", e)
            return _json_error('Database error', 500)

    elif request.method == 'DELETE':
        try:
            Jobcardparts.objects.filter(item_id=item_id).delete()
            Inventoryitem.objects.filter(item_id=item_id).delete()
            return _json_ok()
        except Exception as e:
            print("DB Error (Inventory DELETE):", e)
            return _json_error('Database error', 500)

    return _json_error('Method not allowed', 405)


# ========================================================================
#  PARTS REQUESTS
# ========================================================================

@csrf_exempt
def parts_request_api(request):
    """GET/POST /api/parts-requests"""
    user_data = _get_session_user(request)
    if not user_data:
        return _json_error('Not logged in', 401)

    if request.method == 'GET':
        try:
            # Technicians see only their requests, others see all
            qs = Jobcardparts.objects.select_related('jobcard__technician', 'item').all().order_by('-id')
            if user_data['role'] == 'technician':
                qs = qs.filter(jobcard__technician_id=user_data['user_id'])
            
            paginated = _paginate_queryset(qs, request)
            result = []
            for p in paginated['page_obj']:
                tech_name = "Unknown"
                if p.jobcard and p.jobcard.technician:
                    tech_name = f"{p.jobcard.technician.firstname} {p.jobcard.technician.lastname}"
                
                result.append({
                    'id': p.id,
                    'JobCard_ID': p.jobcard_id,
                    'Item_ID': p.item_id,
                    'ItemName': p.item.name,
                    'Quantity': p.quantityused,
                    'Status': p.status or 'Pending', 
                    'TechnicianName': tech_name,
                })
            paginated['data'] = result
            paginated.pop('page_obj', None)
            return JsonResponse(paginated, safe=False)
        except Exception as e:
            print("DB Error (Parts GET):", e)
            return _json_error('Database error', 500)

    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
            jobcard_id = data.get('jobcard_id')
            item_id = data.get('item_id')
            quantity = data.get('quantity')

            if not jobcard_id or not item_id or not quantity:
                return _json_error('Missing fields')

            # Check if jobcard belongs to technician
            job = Jobcard.objects.filter(jobcard_id=jobcard_id).first()
            if not job:
                return _json_error('Jobcard not found', 404)
            
            if user_data['role'] == 'technician' and job.technician_id != user_data['user_id']:
                return _json_error('Not assigned to this jobcard', 403)

            # Always create a NEW part request to avoid overwriting/resetting statuses of old ones
            Jobcardparts.objects.create(
                jobcard_id=jobcard_id,
                item_id=item_id,
                quantityused=quantity,
                status='Pending'
            )
            return _json_ok()
        except Exception as e:
            print("DB Error (Parts POST):", e)
            return _json_error('Database error', 500)

    return _json_error('Method not allowed', 405)


@csrf_exempt
def parts_approval_api(request):
    if request.method == 'GET':
        try:
            status_filter = request.GET.get('status')
            # Managers see all requests. Paginate.
            qs = Jobcardparts.objects.select_related('jobcard__technician', 'item').all().order_by('-id')
            
            # Counts for summary (total across all pages)
            pending_count = Jobcardparts.objects.filter(status='Pending').count()
            approved_count = Jobcardparts.objects.filter(status='Approved').count()
            rejected_count = Jobcardparts.objects.filter(status='Rejected').count()

            if status_filter and status_filter.lower() != 'all':
                qs = qs.filter(status__iexact=status_filter)
                
            paginated = _paginate_queryset(qs, request)
            result = []
            for p in paginated['page_obj']:
                tech_name = "Unknown"
                if p.jobcard and p.jobcard.technician:
                    tech_name = f"{p.jobcard.technician.firstname} {p.jobcard.technician.lastname}"
                
                result.append({
                    'id': p.id,
                    'JobCard_ID': p.jobcard_id,
                    'Item_ID': p.item_id,
                    'ItemName': p.item.name,
                    'Quantity': p.quantityused,
                    'Status': p.status or 'Pending', 
                    'RequestedBy': tech_name,
                })
            paginated['data'] = result
            paginated['pending_count'] = pending_count
            paginated['approved_count'] = approved_count
            paginated['rejected_count'] = rejected_count
            paginated.pop('page_obj', None)
            return JsonResponse(paginated, safe=False)
        except Exception as e:
            print("DB Error (Parts Approval GET):", e)
            return _json_error('Database error', 500)

    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
            request_id = data.get('id')
            action = data.get('action') # 'approve' or 'reject'
            
            if not request_id or not action:
                return _json_error('Missing fields (id, action)')

            req = Jobcardparts.objects.filter(id=request_id).first()
            if not req:
                return _json_error(f'Request {request_id} not found', 404)

            if action.lower() == 'approve':
                # Deduct stock
                item = req.item
                if item.stockqty < req.quantityused:
                    return _json_error(f'Insufficient stock. Only {item.stockqty} available.')
                
                item.stockqty -= req.quantityused
                item.save()
                req.status = 'Approved'
            else:
                req.status = 'Rejected'

            req.save()
            return _json_ok()
        except Exception as e:
            print("DB Error (Parts Approval POST):", e)
            return _json_error('Database error', 500)


# ========================================================================
#  INSPECTION VIEWS
# ========================================================================

@csrf_exempt
def inspection_list_create(request):
    """GET/POST /api/inspections"""
    if request.method == 'GET':
        user_data = _get_session_user(request)
        try:
            qs = Inspection.objects.select_related('vehicle', 'jobcard__vehicle').order_by('-date', '-inspection_id')
            # Role-based filtering
            if user_data and user_data.get('role') == 'technician':
                qs = qs.filter(jobcard__technician_id=user_data['user_id'])
            elif user_data and user_data.get('role') == 'client':
                qs = qs.filter(jobcard__user_id=user_data['user_id'])
            
            paginated = _paginate_queryset(qs, request)
            result = []
            for i in paginated['page_obj']:
                # Fallback to jobcard vehicle if direct link is missing
                v = i.vehicle or (i.jobcard.vehicle if i.jobcard else None)
                result.append({
                    'Inspection_ID': i.inspection_id,
                    'Vehicle_ID': v.vehicle_id if v else None,
                    'VehicleName': f"{(v.make or '')} {(v.model or '')} ({(v.platenumber or '')})".strip() or "Unknown Vehicle",
                    'JobCard_ID': i.jobcard.jobcard_id if i.jobcard else None,
                    'Date': i.date.isoformat() if i.date else None,
                    'HealthScore': i.healthscore,
                    'HealthCategory': i.healthcategory,
                    'Results': i.results,
                    'DiagnosticData': json.loads(i.diagnosticdata) if i.diagnosticdata else {}
                })
            paginated['data'] = result
            paginated.pop('page_obj', None)
            return JsonResponse(paginated, safe=False)
        except Exception as e:
            print("DB Error (Inspection GET):", e)
            return _json_error('Database error', 500)

    elif request.method == 'POST':
        user_data = _get_session_user(request)
        if not user_data:
            return _json_error('Not logged in', 401)

        try:
            data = json.loads(request.body)
            vehicle_id = data.get('vehicle_id') or None
            jobcard_id = data.get('jobcard_id')
            health_score = data.get('health_score')
            health_category = data.get('health_category')
            results = data.get('results')

            # Extract all other keys as diagnostic data
            standard_keys = ['vehicle_id', 'jobcard_id', 'health_score', 'health_category', 'results']
            diag_data = {k: v for k, v in data.items() if k not in standard_keys}

            # Fallback to JobCard for vehicle_id if it's missing
            if not vehicle_id and jobcard_id:
                jc = Jobcard.objects.filter(jobcard_id=jobcard_id).first()
                if jc:
                    vehicle_id = jc.vehicle_id

            Inspection.objects.create(
                vehicle_id=vehicle_id,
                jobcard_id=jobcard_id,
                date=datetime.date.today(),
                healthscore=health_score,
                healthcategory=health_category,
                results=results,
                diagnosticdata=json.dumps(diag_data)
            )

            # Auto-complete if service type is "Check"
            if jobcard_id:
                jc = Jobcard.objects.select_related('appointment', 'vehicle').filter(jobcard_id=jobcard_id).first()
                if jc and jc.appointment and jc.appointment.service_type and jc.appointment.service_type.lower() == 'check':
                    jc.status = 'Completed'
                    jc.save()
                    if jc.appointment.status != 'Completed':
                        jc.appointment.status = 'Completed'
                        jc.appointment.save()
                        _award_loyalty_point(jc.appointment.user_id)
                        try:
                            from .models import Users
                            client = Users.objects.filter(user_id=jc.appointment.user_id).first()
                            if client and client.email:
                                vehicle_name = f"{jc.vehicle.year or ''} {jc.vehicle.make} {jc.vehicle.model}".strip()
                                _send_service_completion_email(
                                    client.email, 
                                    f"{client.firstname} {client.lastname}",
                                    vehicle_name,
                                    jc.appointment_id
                                )
                        except Exception as e:
                            print(f"Failed to trigger completion email (inspection): {e}")

            return _json_ok()
        except Exception as e:
            print("DB Error (Inspection POST):", e)
            return _json_error('Database error', 500)

    return _json_error('Method not allowed', 405)


# ========================================================================
#  CHAT / AI VIEW
# ========================================================================

@csrf_exempt
def chat_view(request):
    """POST /api/chat"""
    if request.method != 'POST':
        return _json_error('Method not allowed', 405)

    user_data = _get_session_user(request)
    if not user_data:
        return _json_error('Not logged in', 401)

    try:
        data = json.loads(request.body)
        prompt = data.get('prompt')

        if not prompt:
            return _json_error('No prompt provided')

        # --- Comprehensive Database Context Injection ---
        from core.models import Vehicle, Appointment, Jobcard, Invoice
        
        # 1. User's Vehicle Fleet
        vehicles = Vehicle.objects.filter(user_id=user_data['user_id'])
        v_list = [f"{v.make} {v.model} (Plate: {v.platenumber}, VIN: {v.vin}, Year: {v.year})" for v in vehicles]
        v_info = "\n".join(v_list) if v_list else "No vehicles registered."
        
        # 2. Service & Maintenance History (Jobcards)
        history_qs = Jobcard.objects.filter(user_id=user_data['user_id']).select_related('vehicle').order_by('-createdat')[:10]
        h_list = []
        total_spent = 0
        for jc in history_qs:
            invoice = Invoice.objects.filter(jobcard_id=jc.jobcard_id).first()
            amt = float(invoice.total) if invoice else 0
            total_spent += amt
            date_str = jc.createdat.strftime('%Y-%m-%d') if jc.createdat else "N/A"
            h_list.append(
                f"- ID: #{jc.jobcard_id}, {date_str}, {jc.vehicle.make} {jc.vehicle.model}, "
                f"Status: {jc.status}, Cost: EGP {amt}"
            )
        h_info = "\n".join(h_list) if h_list else "None."
        
        # 3. Upcoming Appointments
        appts = Appointment.objects.filter(user_id=user_data['user_id']).exclude(status__in=['Cancelled', 'Completed']).order_by('date_time')[:5]
        a_list = []
        for a in appts:
            a_date = a.date_time.strftime('%Y-%m-%d %H:%M') if a.date_time else "TBD"
            a_list.append(f"- ID: #{a.appointment_id}, {a_date}, {a.vehicle.make} {a.vehicle.model}, Status: {a.status}")
        a_info = "\n".join(a_list) if a_list else "None."

        system_instruction = (
            f"You are the IVHEMMS AI Assistant, an expert in automotive management. "
            f"Below is the REAL-TIME DATA for the current user ({user_data['name']}):\n\n"
            f"--- VEHICLE FLEET ---\n{v_info}\n\n"
            f"--- RECENT SERVICE HISTORY ---\n{h_info}\n\n"
            f"--- UPCOMING APPOINTMENTS ---\n{a_info}\n\n"
            f"--- ACCOUNT STATS ---\nTotal Maintenance Spend: EGP {total_spent}\n\n"
            "INSTRUCTIONS:\n"
            "1. You are strictly restricted to the user's database records provided above.\n"
            "2. If the user asks about a specific vehicle (e.g., 'BMW M4'), you MUST first check if it exists in the 'VEHICLE FLEET'.\n"
            "3. If the vehicle IS NOT in the fleet, DO NOT provide general information about it. Instead, explicitly reply that this vehicle is not registered in their account.\n"
            "4. If the vehicle IS in the fleet, provide its details based solely on the provided 'VEHICLE FLEET' and 'SERVICE HISTORY'.\n"
            "5. Be professional, concise, and helpful. Always reply in the exact same language the user uses (e.g., Arabic or English).\n"
            "6. NEVER hallucinate or invent vehicle data. Only use the provided records."
        )

        import requests
        try:
            url = f"{GEMINI_URL}?key={settings.GEMINI_API_KEY}"
            payload = {
                "contents": [{
                    "parts": [{
                        "text": f"{system_instruction}\n\nUser Question: {prompt}"
                    }]
                }]
            }
            resp = requests.post(url, json=payload, timeout=15)
            result = resp.json()

            if resp.status_code == 200:
                # Extract text from Gemini response structure
                try:
                    ai_text = result['candidates'][0]['content']['parts'][0]['text']
                except:
                    ai_text = "I received an empty response. Please try again."
            else:
                err_msg = result.get('error', {}).get('message', 'Unknown error')
                ai_text = f"Connection error. Please try again. (Ref: {resp.status_code}) - Details: {err_msg}"
                print(f"[AI ERROR] {resp.status_code}: {err_msg}")

        except Exception as e:
            ai_text = f"The system is currently busy. Please try again in a moment. (Ref: {str(e)[:15]})"

        return JsonResponse({"response": ai_text})

    except Exception as e:
        print("!!! Chat API Critical Error:", e)
        return JsonResponse({"error": f"AI Error: {str(e)}"}, status=500)


# ========================================================================
#  HTML PAGE SERVING
# ========================================================================

@csrf_exempt
def uninvoiced_jobcards_view(request):
    """GET /api/admin/uninvoiced-jobcards — list completed jobcards without an invoice"""
    user_data = _get_session_user(request)
    if not user_data or user_data['role'] not in ['admin', 'manager', 'finance-manager', 'top-manager']:
        return _json_error('Forbidden', 403)

    try:
        # Completed jobs without a linked invoice
        qs = Jobcard.objects.filter(status='Completed', invoice__isnull=True).select_related('vehicle', 'user').order_by('-updatedat')
        paginated = _paginate_queryset(qs, request)
        result = []
        for jc in paginated['page_obj']:
            result.append({
                'JobCard_ID': jc.jobcard_id,
                'ClientName': f"{jc.user.firstname} {jc.user.lastname}" if jc.user else "Unknown Client",
                'Vehicle': f"{jc.vehicle.make} {jc.vehicle.model} ({jc.vehicle.platenumber})" if jc.vehicle else "Unknown Vehicle",
                'Date': _serialize(jc.updatedat),
            })
        paginated['data'] = result
        paginated.pop('page_obj', None)
        return JsonResponse(paginated, safe=False)
    except Exception as e:
        print("DB Error (Uninvoiced jobs):", e)
        return _json_error('Database error', 500)


def serve_html(request, page_path):
    """Serve any HTML file as a template."""
    # Special case: public pages don't need auth
    public_pages = ['index.html', 'reset-password.html', 'login.html', 'register.html', 'forgot-password.html']
    
    user_data = _get_session_user(request)
    
    # If user is logged in and tries to access index or login, redirect to their dashboard
    is_root_or_login = any(x in page_path for x in ['index.html', 'login.html'])
    if user_data and is_root_or_login:
        target = ROLE_TO_DASHBOARD.get(user_data['role'], 'index.html')
        if target != 'index.html':
            return HttpResponseRedirect('/' + target)

    # Check if page is in public list
    if any(x in page_path for x in public_pages):
        response = render(request, page_path)
        patch_cache_control(response, no_cache=True, no_store=True, must_revalidate=True)
        return response
    
    # Check session for protected pages
    if not user_data:
        return HttpResponseRedirect('/index.html')

    # Security & Logic: Redirect direct access to protected dashboards to their dedicated views
    if 'pages/analytics/data-dashboard.html' in page_path:
        if user_data.get('role') == 'data-analyst':
            return HttpResponseRedirect('/ml-dashboard')
        else:
            return HttpResponseRedirect('/index.html')

    response = render(request, page_path, {'user_data': user_data})
    patch_cache_control(response, no_cache=True, no_store=True, must_revalidate=True)
    return response


def ml_dashboard(request):
    """
    ML Dashboard View - Protected.
    Only allows access for DataAnalyst role.
    Integrates ML models for health score prediction.
    """
    user_data = _get_session_user(request)
    
    # Access Control: Only DataAnalyst
    if not user_data or user_data.get('role') != 'data-analyst':
        return HttpResponseRedirect('/index.html')

    prediction = None
    selected_truck = None
    truck_ids = []
    error_msg = None
    
    # Initialize default stats to prevent template errors
    stats = {
        'total_services': 0,
        'avg_health': 0,
        'critical_trucks': 0,
        'fleet_size': 0
    }

    # ML integration - Only runs when DataAnalyst interacts
    try:
        import sys
        import os
        from django.conf import settings
        
        # Add ML directory to path
        ml_path = os.path.join(settings.BASE_DIR, 'ML - Copy')
        if ml_path not in sys.path:
            sys.path.append(ml_path)
        
        # 1. Load dataset FIRST to ensure stats and dropdown are populated
        from data_processing import load_data, GROUP_COL, TIME_COL, TARGET_COL
        from ml import predict_truck_health_score, calculate_health_score
        
        data_file = os.path.join(ml_path, 'Train_Test_FleetData.xlsx')
        df = load_data(path=data_file)
        
        # User specified IDs to show in the dashboard
        USER_TRUCK_IDS = [
            'Truck_0021X1', 'Truck_0051X1', 'Truck_0061X1', 'Truck_0081X1',
            'Truck_0101X1', 'Truck_0111X1', 'Truck_0131X1', 'Truck_0141X1',
            'Truck_0151X1', 'Truck_0681X1', 'Truck_0691X1', 'Truck_0701X1', 
            'Truck_0711X1', 'Truck_0741X1', 'Truck_0751X1', 'Truck_0771X1', 
            'Truck_0781X1', 'Truck_0791X1', 'Truck_0801X1'
        ]
        
        # Filter dataframe and IDs to match the user's model/requirement
        df = df[df[GROUP_COL].isin(USER_TRUCK_IDS)]
        truck_ids = sorted(df[GROUP_COL].unique().tolist())
        
        # Update actual stats based on filtered data
        stats = {
            'total_services': df.shape[0],
            'avg_health': round(df[TARGET_COL].mean(), 1) if not df.empty else 0,
            'critical_trucks': df[df[TARGET_COL] < 40][GROUP_COL].nunique() if not df.empty else 0,
            'fleet_size': len(truck_ids)
        }

        # 2. Try to handle prediction if requested
        if request.method == 'POST':
            truck_id_raw = request.POST.get('truck_id')
            if truck_id_raw:
                selected_truck = truck_id_raw
                truck_df = df[df[GROUP_COL] == selected_truck].sort_values(TIME_COL)
                
                if not truck_df.empty:
                    try:
                        # Attempt ML prediction
                        prediction = predict_truck_health_score(truck_df)
                        if prediction is not None:
                            prediction = round(float(prediction), 1)
                    except Exception as ml_err:
                        # Fallback to direct calculation if ML fails (e.g. tensorflow missing)
                        print(f"ML Model Error: {ml_err}. Falling back to sensor calculation.")
                        prediction = calculate_health_score(truck_df.iloc[-1])
                        if prediction is not None:
                            prediction = round(float(prediction), 1)
                    
                    # Update stats for selected truck
                    stats['avg_health'] = round(truck_df[TARGET_COL].mean(), 1)
                    stats['min_health'] = round(truck_df[TARGET_COL].min(), 1)
                    stats['max_health'] = round(truck_df[TARGET_COL].max(), 1)
                    stats['services_count'] = len(truck_df)
                else:
                    error_msg = f"No data found for Truck {selected_truck}"
            
    except Exception as e:
        print(f"ML Dashboard Execution Error: {e}")
        error_msg = f"System Error: {str(e)}"

    return render(request, 'pages/analytics/data-dashboard.html', {
        'user_data': user_data,
        'truck_ids': truck_ids,
        'prediction': prediction,
        'selected_truck': selected_truck,
        'stats': stats,
        'error': error_msg
    })


def export_ml_certificate(request):
    """
    Generate and download a PDF health certificate for a vehicle.
    Uses the existing certificate_generator logic.
    """
    user_data = _get_session_user(request)
    if not user_data or user_data.get('role') != 'data-analyst':
        return HttpResponseRedirect('/index.html')

    truck_id = request.GET.get('truck_id')
    health_score = request.GET.get('health_score')

    if not truck_id or not health_score:
        return HttpResponse("Missing truck_id or health_score parameters", status=400)

    try:
        import sys
        import os
        from django.conf import settings
        from django.http import FileResponse
        
        # Add ML directory to path for imports
        ml_path = os.path.join(settings.BASE_DIR, 'ML - Copy')
        if ml_path not in sys.path:
            sys.path.append(ml_path)
            
        from certificate_generator import generate_certificate
        
        # Generate the PDF
        file_path = generate_certificate(str(truck_id), float(health_score))
        
        if os.path.exists(file_path):
            # Open the file and return as a response
            response = FileResponse(open(file_path, 'rb'), content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="Vehicle_Health_Certificate_{truck_id}.pdf"'
            return response
        else:
            return HttpResponse("Failed to generate certificate file.", status=500)
            
    except Exception as e:
        print(f"Certificate Export Error: {e}")
        return HttpResponse(f"Error generating certificate: {str(e)}", status=500)


@csrf_exempt
def services_list_view(request):
    """GET /api/services — returns the list of available services with icons/colors"""
    # Define services with metadata for the UI
    services = [
        # Maintenance & Services
        {'name': 'Oil Change & Filter', 'icon': 'bi-droplet-fill', 'color': 'text-warning'},
        {'name': 'Electrical System Check', 'icon': 'bi-lightning-fill', 'color': 'text-warning'},
        
        # Repairs & Mechanics
        {'name': 'Engine Diagnostics', 'icon': 'bi-cpu-fill', 'color': 'text-info'},
        {'name': 'Brake Inspection', 'icon': 'bi-disc-fill', 'color': 'text-danger'},
        {'name': 'Suspension Check', 'icon': 'bi-tools', 'color': 'text-danger'},
        {'name': 'Transmission Service', 'icon': 'bi-gear-wide-connected', 'color': 'text-primary'},
        {'name': 'Fuel System Cleaning', 'icon': 'bi-fuel-pump-fill', 'color': 'text-dark'},
        
        # Wheels & Power
        {'name': 'Tyre Replacement', 'icon': 'bi-circle-fill', 'color': 'text-success'},
        {'name': 'Wheel Alignment', 'icon': 'bi-aspect-ratio', 'color': 'text-success'},
        {'name': 'Battery Replacement', 'icon': 'bi-battery-full', 'color': 'text-warning'},
        
        # Cleaning & Care
        {'name': 'Car Wash', 'icon': 'bi-water', 'color': 'text-info'},
        {'name': 'Car Detailing', 'icon': 'bi-stars', 'color': 'text-info'},
        {'name': 'AC Service', 'icon': 'bi-snow2', 'color': 'text-primary'},
    ]
    return JsonResponse(services, safe=False)

# ========================================================================
#  PURCHASE ORDERS API
# ========================================================================

@csrf_exempt
def supplier_parts_api(request):
    """GET /api/supplier-parts — Returns list of all available parts across all suppliers"""
    if request.method == 'GET':
        from core.models import SupplierPart
        model_filter = request.GET.get('car_model')
        parts = SupplierPart.objects.select_related('supplier').all()
        
        if model_filter:
            parts = parts.filter(car_model__icontains=model_filter)
            
        data = []
        for p in parts:
            data.append({
                'part_id': p.part_id,
                'supplier_id': p.supplier.user_id,
                'supplier_name': p.supplier.company_name,
                'car_model': p.car_model,
                'name': p.name,
                'code': p.code,
                'price': p.price,
                'quantity': p.quantity
            })
        return _json_ok({'data': data})
    return _json_error('Method not allowed', 405)

@csrf_exempt
def purchase_orders_api(request):
    """GET and POST for ordering parts from suppliers"""
    session_user = _get_session_user(request)
    if not session_user:
        return _json_error('Unauthorized', 401)
        
    if request.method == 'GET':
        from core.models import PurchaseOrder
        orders = PurchaseOrder.objects.select_related('supplier_part', 'supplier', 'stock_keeper').all().order_by('-order_date')
        paginated = _paginate_queryset(orders, request)
        data = []
        for o in paginated['page_obj']:
            data.append({
                'order_id': o.order_id,
                'supplier_name': o.supplier.company_name,
                'part_name': o.supplier_part.name,
                'part_code': o.supplier_part.code,
                'quantity': o.quantity,
                'total_price': o.total_price,
                'status': o.status,
                'order_date': o.order_date.isoformat(),
                'ordered_by': f"{o.stock_keeper.firstname} {o.stock_keeper.lastname}"
            })
        paginated['data'] = data
        paginated.pop('page_obj', None)
        return JsonResponse(paginated, safe=False)
        
    if request.method == 'POST':
        import json
        from core.models import SupplierPart, PurchaseOrder, Users
        try:
            body = json.loads(request.body)
            part_id = body.get('part_id')
            qty = int(body.get('quantity', 0))
            if not part_id or qty <= 0:
                return _json_error('Invalid parameters', 400)
                
            part = SupplierPart.objects.get(part_id=part_id)
            user = Users.objects.get(user_id=session_user['user_id'])
            
            order = PurchaseOrder.objects.create(
                supplier=part.supplier,
                supplier_part=part,
                stock_keeper=user,
                quantity=qty,
                total_price=qty * part.price,
                status='Pending'
            )
            return _json_ok({'order_id': order.order_id})
        except Exception as e:
            return _json_error(str(e), 500)
            
    if request.method == 'PUT':
        import json
        from core.models import PurchaseOrder, Inventoryitem
        try:
            body = json.loads(request.body)
            order_id = body.get('order_id')
            action = body.get('action')
            
            if not order_id or action not in ['approve', 'reject', 'deliver']:
                return _json_error('Invalid parameters', 400)
                
            order = PurchaseOrder.objects.get(order_id=order_id)
            if action == 'approve':
                order.status = 'Approved'
            elif action == 'reject':
                order.status = 'Rejected'
            elif action == 'deliver':
                if order.status != 'Delivered':
                    order.status = 'Delivered'
                    inv_item = None
                    if order.supplier_part.code.isdigit():
                        inv_item = Inventoryitem.objects.filter(itemnumber=int(order.supplier_part.code)).first()
                    if not inv_item:
                        inv_item = Inventoryitem.objects.filter(name__icontains=order.supplier_part.name).first()
                    if inv_item:
                        inv_item.stockqty = (inv_item.stockqty or 0) + order.quantity
                        inv_item.save()
                    else:
                        Inventoryitem.objects.create(itemnumber=0, name=order.supplier_part.name, unitprice=order.supplier_part.price, stockqty=order.quantity, minstocklevel=10)
            order.save()
            return _json_ok({'status': order.status})
        except PurchaseOrder.DoesNotExist:
            return _json_error('Order not found', 404)
        except Exception as e:
            return _json_error(str(e), 500)
            
    return _json_error('Method not allowed', 405)


# ========================================================================
#  BOOK CHECK VIEW
# ========================================================================

@csrf_exempt
def book_check_view(request):
    """POST /api/book-check — Client requests a vehicle check for 3000 EGP."""
    if request.method != 'POST':
        return _json_error('Method not allowed', 405)

    user_data = _get_session_user(request)
    if not user_data or user_data['role'] != 'client':
        return _json_error('Forbidden: Clients only.', 403)

    try:
        data = json.loads(request.body)
        vehicle_id = data.get('vehicle_id')
        date_str   = data.get('date')
        time_str   = data.get('time', '10:00')

        if not vehicle_id:
            return _json_error('Please select a vehicle.')
        if not date_str:
            return _json_error('Please select a date.')

        # Verify vehicle belongs to this client
        vehicle = Vehicle.objects.filter(vehicle_id=vehicle_id, user_id=user_data['user_id']).first()
        if not vehicle:
            return _json_error('Vehicle not found or does not belong to you.', 404)

        # Combine date + time into a datetime
        try:
            start_dt = datetime.datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")
        except ValueError:
            return _json_error('Invalid date or time format.')

        CHECK_PRICE = 3000  # Fixed check price in EGP

        # 1. Create Appointment with service_type = 'Check'
        appointment = Appointment.objects.create(
            user_id=user_data['user_id'],
            vehicle=vehicle,
            date_time=start_dt,
            status='Scheduled',
            service_type='Check',
        )

        # 2. Create Jobcard linked to the appointment (status = 'Pending Payment')
        now = datetime.datetime.now()
        jobcard = Jobcard.objects.create(
            appointment=appointment,
            vehicle=vehicle,
            user_id=user_data['user_id'],
            createdat=now,
            updatedat=now,
            status='Pending Payment',
            totallaborcost=CHECK_PRICE,
            totalpartscost=0,
        )

        # 3. Create Invoice for 3000 EGP
        invoice_date = datetime.date.today()
        due_date     = invoice_date + datetime.timedelta(days=7)

        invoice = Invoice.objects.create(
            user_id=user_data['user_id'],
            invoicedate=invoice_date,
            duedate=due_date,
            jobcard=jobcard,
            subtotallabor=CHECK_PRICE,
            subtotalparts=0,
            tax=0,
            discount=0,
            total=CHECK_PRICE,
            status='Unpaid',
        )

        # Link invoice back to jobcard
        jobcard.invoice = invoice
        jobcard.save()

        # 4. Send confirmation email using existing SMTP setup
        client_email = user_data.get('email', '')
        client_name  = user_data.get('name', 'Valued Client')
        vehicle_label = f"{vehicle.year or ''} {vehicle.make} {vehicle.model} ({vehicle.platenumber})".strip()

        # Generate a secure signed token for the direct Pay Now link in email
        from django.core import signing
        pay_token = signing.dumps(
            {'invoice_id': invoice.invoice_id, 'user_id': user_data['user_id']},
            salt='check-pay-email',
        )

        _send_check_confirmation_email(
            client_email, client_name, vehicle_label,
            date_str, time_str, invoice.invoice_id, CHECK_PRICE, pay_token
        )

        return _json_ok({
            'message': 'Check request submitted successfully. An email confirmation has been sent.',
            'invoice_id': invoice.invoice_id,
            'amount': CHECK_PRICE,
        })

    except Exception as e:
        print("DB Error (book_check_view):", e)
        return _json_error('Database error: ' + str(e), 500)


def _send_check_confirmation_email(target_email, client_name, vehicle_label, date_str, time_str, invoice_id, amount, pay_token=''):
    """Send vehicle check request confirmation email via SMTP - Premium Dark Design."""
    try:
        system = settings.SYSTEM_NAME
        import smtplib
        from email.mime.multipart import MIMEMultipart
        from email.mime.text import MIMEText

        msg = MIMEMultipart('alternative')
        msg['From'] = f"{system} <{settings.SMTP_USER}>"
        msg['To']   = target_email
        msg['Subject'] = f"Vehicle Check Confirmed — Invoice #{invoice_id} | {system}"

        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Vehicle Check Confirmation</title>
</head>
<body style="margin:0;padding:0;background-color:#0f0f1a;font-family:'Segoe UI',Arial,sans-serif;">

  <!-- Wrapper -->
  <table width="100%" cellpadding="0" cellspacing="0" style="background:#0f0f1a;padding:40px 16px;">
    <tr>
      <td align="center">
        <table width="600" cellpadding="0" cellspacing="0" style="max-width:600px;width:100%;">

          <!-- HEADER -->
          <tr>
            <td style="background:linear-gradient(135deg,#1e1b4b 0%,#312e81 50%,#4338ca 100%);border-radius:20px 20px 0 0;padding:40px 40px 30px;text-align:center;">
              <div style="display:inline-block;background:rgba(255,255,255,0.12);border-radius:50%;width:72px;height:72px;line-height:72px;font-size:32px;margin-bottom:16px;">🚗</div>
              <h1 style="margin:0;color:#ffffff;font-size:28px;font-weight:800;letter-spacing:-0.5px;">{system}</h1>
              <p style="margin:8px 0 0;color:#a5b4fc;font-size:14px;letter-spacing:2px;text-transform:uppercase;">Vehicle Check Confirmation</p>
              <div style="width:60px;height:3px;background:linear-gradient(90deg,#818cf8,#c084fc);margin:20px auto 0;border-radius:2px;"></div>
            </td>
          </tr>

          <!-- GREETING -->
          <tr>
            <td style="background:#1e1b4b;padding:24px 40px 0;">
              <p style="margin:0;color:#e2e8f0;font-size:16px;">Hello <strong>{client_name}</strong> 👋</p>
              <p style="margin:8px 0 0;color:#94a3b8;font-size:14px;line-height:1.6;">
                Your <strong>Vehicle Check</strong> request has been successfully submitted and is awaiting your payment to be activated.
              </p>
            </td>
          </tr>

          <!-- DETAILS CARD -->
          <tr>
            <td style="background:#1e1b4b;padding:24px 40px;">
              <table width="100%" cellpadding="0" cellspacing="0"
                     style="background:linear-gradient(135deg,#0f172a,#1e1b4b);border:1px solid rgba(129,140,248,0.3);border-radius:16px;overflow:hidden;">
                <tr>
                  <td style="padding:20px 24px;">
                    <table width="100%" cellpadding="0" cellspacing="0">
                      <tr>
                        <td style="padding:8px 0;border-bottom:1px solid rgba(255,255,255,0.05);">
                          <span style="color:#64748b;font-size:12px;text-transform:uppercase;letter-spacing:1px;">Vehicle</span><br>
                          <span style="color:#f1f5f9;font-size:15px;font-weight:600;margin-top:4px;display:block;">{vehicle_label}</span>
                        </td>
                      </tr>
                      <tr>
                        <td style="padding:8px 0;border-bottom:1px solid rgba(255,255,255,0.05);">
                          <span style="color:#64748b;font-size:12px;text-transform:uppercase;letter-spacing:1px;">Scheduled</span><br>
                          <span style="color:#f1f5f9;font-size:15px;font-weight:600;margin-top:4px;display:block;">{date_str} at {time_str}</span>
                        </td>
                      </tr>
                      <tr>
                        <td style="padding:8px 0;">
                          <span style="color:#64748b;font-size:12px;text-transform:uppercase;letter-spacing:1px;">Amount Due</span><br>
                          <span style="color:#818cf8;font-size:24px;font-weight:800;margin-top:4px;display:block;">EGP {amount:,}</span>
                        </td>
                      </tr>
                    </table>
                  </td>
                </tr>
              </table>
            </td>
          </tr>

          <!-- PAY BUTTON -->
          <tr>
            <td style="background:#1e1b4b;padding:0 40px 40px;text-align:center;">
              <a href="http://127.0.0.1:8000/pay-check/{pay_token}/"
                 style="display:inline-block;background:linear-gradient(135deg,#4338ca,#7c3aed);color:#ffffff;text-decoration:none;font-size:17px;font-weight:800;padding:18px 48px;border-radius:50px;box-shadow:0 8px 30px rgba(99,102,241,0.5);">
                PAY NOW VIA CREDIT CARD
              </a>
            </td>
          </tr>

          <!-- FOOTER -->
          <tr>
            <td style="background:#0f0f1a;border-radius:0 0 20px 20px;padding:30px 40px;text-align:center;border-top:1px solid rgba(255,255,255,0.05);">
              <p style="margin:0;color:#4a5568;font-size:12px;">Sent by {system}. Do not reply to this email.</p>
              <p style="margin:8px 0 0;color:#374151;font-size:11px;">&copy; 2026 {system}. All rights reserved.</p>
            </td>
          </tr>

        </table>
      </td>
    </tr>
  </table>

</body>
</html>"""

        text = (
            f"Hello {client_name},\n\n"
            f"Your Vehicle Check has been confirmed. Please pay via Credit Card to activate.\n\n"
            f"Vehicle : {vehicle_label}\n"
            f"Date    : {date_str} at {time_str}\n"
            f"Amount  : EGP {amount:,}\n\n"
            f"PAY NOW via Credit Card:\n"
            f"http://127.0.0.1:8000/pay-check/{pay_token}/\n\n"
            f"Best regards,\nThe {system} Team"
        )

        msg.attach(MIMEText(text, 'plain'))
        msg.attach(MIMEText(html, 'html'))

        server = smtplib.SMTP_SSL(settings.SMTP_SERVER, settings.SMTP_PORT)
        server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
        server.send_message(msg)
        server.quit()
        print(f"[book_check] Premium email sent to {target_email}")
        return True
    except Exception as e:
        print(f"[book_check] Failed to send email: {e}")
        return False


def _send_service_completion_email(target_email, client_name, vehicle_label, appointment_id):
    """Send vehicle service completion notification email via SMTP - Premium Dark Design."""
    try:
        system = settings.SYSTEM_NAME
        import smtplib
        from email.mime.multipart import MIMEMultipart
        from email.mime.text import MIMEText

        msg = MIMEMultipart('alternative')
        msg['From'] = f"{system} <{settings.SMTP_USER}>"
        msg['To']   = target_email
        msg['Subject'] = f"Service Completed — Your {vehicle_label} is Ready! | {system}"

        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Service Completed</title>
</head>
<body style="margin:0;padding:0;background-color:#0f0f1a;font-family:'Segoe UI',Arial,sans-serif;">
  <table width="100%" cellpadding="0" cellspacing="0" style="background:#0f0f1a;padding:40px 16px;">
    <tr>
      <td align="center">
        <table width="600" cellpadding="0" cellspacing="0" style="max-width:600px;width:100%;">
          <tr>
            <td style="background:linear-gradient(135deg,#065f46 0%,#047857 50%,#059669 100%);border-radius:20px 20px 0 0;padding:40px 40px 30px;text-align:center;">
              <div style="display:inline-block;background:rgba(255,255,255,0.12);border-radius:50%;width:72px;height:72px;line-height:72px;font-size:32px;margin-bottom:16px;">✨</div>
              <h1 style="margin:0;color:#ffffff;font-size:28px;font-weight:800;letter-spacing:-0.5px;">{system}</h1>
              <p style="margin:8px 0 0;color:#a7f3d0;font-size:14px;letter-spacing:2px;text-transform:uppercase;">Service Successfully Completed</p>
            </td>
          </tr>
          <tr>
            <td style="background:#1e1b4b;padding:32px 40px;">
              <p style="margin:0;color:#e2e8f0;font-size:18px;">Great news, <strong>{client_name}</strong>!</p>
              <p style="margin:16px 0 0;color:#94a3b8;font-size:15px;line-height:1.7;">
                We are pleased to inform you that the maintenance for your <strong>{vehicle_label}</strong> has been completed. 
                Our team has performed all necessary checks and services to ensure your vehicle is in top condition.
              </p>
              <div style="background:rgba(16, 185, 129, 0.1); border: 1px solid rgba(16, 185, 129, 0.2); border-radius:12px; padding:20px; margin-top:24px;">
                <p style="margin:0; color:#10b981; font-weight:700; font-size:14px; text-transform:uppercase;">Vehicle Status: READY FOR PICKUP</p>
                <p style="margin:8px 0 0; color:#94a3b8; font-size:13px;">You can now visit the workshop to collect your vehicle at your earliest convenience.</p>
              </div>
            </td>
          </tr>
          <tr>
            <td style="background:#1e1b4b;padding:0 40px 40px;text-align:center;">
              <a href="http://127.0.0.1:8000/pages/client/service-history.html"
                 style="display:inline-block;background:linear-gradient(135deg,#059669,#10b981);color:#ffffff;text-decoration:none;font-size:16px;font-weight:700;padding:16px 32px;border-radius:50px;box-shadow:0 8px 20px rgba(16,185,129,0.3);">
                VIEW SERVICE DETAILS
              </a>
            </td>
          </tr>
          <tr>
            <td style="background:#0f0f1a;border-radius:0 0 20px 20px;padding:30px 40px;text-align:center;border-top:1px solid rgba(255,255,255,0.05);">
              <p style="margin:0;color:#4a5568;font-size:12px;">Thank you for choosing {system} for your automotive needs.</p>
            </td>
          </tr>
        </table>
      </td>
    </tr>
  </table>
</body>
</html>"""

        text = (
            f"Hello {client_name},\n\n"
            f"Your vehicle ({vehicle_label}) is ready! Service has been successfully completed.\n\n"
            f"You can view the details here:\n"
            f"http://127.0.0.1:8000/pages/client/service-history.html\n\n"
            f"Best regards,\nThe {system} Team"
        )

        msg.attach(MIMEText(text, 'plain'))
        msg.attach(MIMEText(html, 'html'))

        server = smtplib.SMTP_SSL(settings.SMTP_SERVER, settings.SMTP_PORT)
        server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
        server.send_message(msg)
        server.quit()
        print(f"[service_complete] Email sent to {target_email} for vehicle {vehicle_label}")
        return True
    except Exception as e:
        print(f"[service_complete] Failed to send email: {e}")
        return False


# ========================================================================
#  VEHICLE CHECK STATUS VIEW
# ========================================================================

@require_GET
def vehicle_check_status_view(request):
    """GET /api/vehicle-check-status?vehicle_id=X
    Returns whether the given vehicle has a paid Check invoice,
    meaning the client is allowed to book a regular service for it.
    """
    user_data = _get_session_user(request)
    if not user_data:
        return _json_error('Unauthorized', 401)

    vehicle_id = request.GET.get('vehicle_id')
    if not vehicle_id:
        return _json_error('vehicle_id is required')

    try:
        # Logic: Allow booking if there is a PAID check and it hasn't been "consumed" by a newer service
        # We check if the latest Paid Check is newer or equal to the latest Service
        latest_paid_check = Jobcard.objects.filter(
            vehicle_id=vehicle_id,
            user_id=user_data['user_id'],
            appointment__service_type__iexact='check',
            invoice__status='Paid'
        ).order_by('-appointment_id').first()

        latest_service = Appointment.objects.filter(
            vehicle_id=vehicle_id,
            user_id=user_data['user_id']
        ).exclude(service_type__iexact='check').exclude(status='Cancelled').order_by('-appointment_id').first()

        can_book = False
        if latest_paid_check:
            if not latest_service:
                can_book = True # No services done yet, but has a check
            elif latest_paid_check.appointment_id >= latest_service.appointment_id:
                can_book = True # Paid check is more recent than (or the same as) the last service

        if can_book:
            return JsonResponse({
                'has_paid_check': True,
                'message': 'Vehicle eligible for service booking.'
            })
        else:
            # Pending unpaid check = Jobcard with status='Pending Payment' linked to 'check' appointment
            unpaid_check = Jobcard.objects.filter(
                vehicle_id=vehicle_id,
                user_id=user_data['user_id'],
                appointment__service_type__iexact='check',
                status='Pending Payment',
                invoice__status='Unpaid',
            ).select_related('invoice').first()

            if unpaid_check:
                return JsonResponse({
                    'has_paid_check': False,
                    'has_pending_check': True,
                    'invoice_id': unpaid_check.invoice_id,
                    'message': 'You have a pending Check invoice. Please pay it first before booking a service.',
                })
            else:
                return JsonResponse({
                    'has_paid_check': False,
                    'has_pending_check': False,
                    'message': 'No vehicle check found. Please book and pay for a vehicle check before booking a service.',
                })
    except Exception as e:
        print("DB Error (vehicle_check_status):", e)
        return _json_error('Database error: ' + str(e), 500)


@require_GET
def client_check_status_view(request):
    """GET /api/client-check-status
    Returns whether this client has ANY paid Check inspection across all vehicles.
    Used to gate access to the Book Service page.
    """
    user_data = _get_session_user(request)
    if not user_data:
        return _json_error('Unauthorized', 401)

    try:
        uid = user_data['user_id']

        # Has any paid check? (Paid invoice linked to a 'check' appointment)
        paid_check = Jobcard.objects.filter(
            user_id=uid,
            appointment__service_type__iexact='check',
            invoice__status='Paid',
        ).first()

        if paid_check:
            return JsonResponse({'has_paid_check': True})

        # Has any pending (not yet paid) check?
        pending_check = Jobcard.objects.filter(
            user_id=uid,
            appointment__service_type__iexact='check',
            status='Pending Payment',
        ).first()

        if pending_check:
            return JsonResponse({
                'has_paid_check': False,
                'has_pending_check': True,
                'invoice_id': pending_check.invoice_id,
            })

        return JsonResponse({'has_paid_check': False, 'has_pending_check': False})

    except Exception as e:
        print("DB Error (client_check_status):", e)
        return _json_error('Database error: ' + str(e), 500)


# ========================================================================
#  DIRECT PAY-CHECK PAGE (from email link — no login required)
# ========================================================================

def pay_check_page_view(request, token):
    """GET /pay-check/<token>/ — renders the direct payment page."""
    from django.core import signing
    from django.shortcuts import render as django_render

    error = None
    invoice = None
    try:
        payload = signing.loads(token, salt='check-pay-email', max_age=7 * 24 * 3600)
        invoice_id = payload['invoice_id']

        # We only use 'Unpaid' status now
        invoice = Invoice.objects.filter(
            invoice_id=invoice_id,
            status='Unpaid',
        ).select_related('jobcard__appointment').first()

        if invoice:
            # Make sure it's actually a Check type invoice
            jc = invoice.jobcard
            if not jc or not jc.appointment or (jc.appointment.service_type or '').lower() != 'check':
                invoice = None
                error = 'This is not a valid vehicle check invoice.'
        else:
            # Check if already paid
            paid_inv = Invoice.objects.filter(invoice_id=invoice_id, status='Paid').first()
            if paid_inv:
                error = 'This invoice has already been paid. Thank you!'
            else:
                error = 'Invoice not found or link is invalid.'

    except signing.SignatureExpired:
        error = 'This payment link has expired (7-day limit). Please log in to your account to pay.'
    except signing.BadSignature:
        error = 'Invalid or tampered payment link.'

    return django_render(request, 'pages/public/pay-check.html', {
        'token': token,
        'invoice': invoice,
        'error': error,
    })


@csrf_exempt
def pay_check_api_view(request, token):
    """POST /pay-check/<token>/process — processes the check payment from email link."""
    if request.method != 'POST':
        return _json_error('Method not allowed', 405)

    from django.core import signing

    try:
        payload = signing.loads(token, salt='check-pay-email', max_age=7 * 24 * 3600)
    except signing.SignatureExpired:
        return _json_error('Payment link expired. Please log in to pay.', 410)
    except signing.BadSignature:
        return _json_error('Invalid payment link.', 400)

    try:
        data = json.loads(request.body)
        method = data.get('method', 'CreditCard')
        if method not in VALID_PAYMENT_METHODS:
            method = 'CreditCard'

        invoice_id = payload['invoice_id']
        user_id    = payload['user_id']

        # We only use 'Unpaid' status
        invoice = Invoice.objects.filter(
            invoice_id=invoice_id,
            status='Unpaid',
        ).select_related('jobcard__appointment').first()

        if not invoice:
            return _json_error('Invoice already paid or not found.', 404)

        # Verify it's actually a check invoice
        jc = invoice.jobcard
        if not jc or not jc.appointment or (jc.appointment.service_type or '').lower() != 'check':
            return _json_error('This is not a valid vehicle check invoice.', 400)

        # Record payment
        Payment.objects.create(
            user_id=user_id,
            invoice=invoice,
            paymentdate=datetime.date.today(),
            amount=invoice.total,
            method=method,
        )
        invoice.status = 'Paid'
        invoice.save()

        # Activate the Jobcard
        Jobcard.objects.filter(invoice=invoice, status='Pending Payment').update(status='Scheduled')
        if jc.status == 'Pending Payment':
            jc.status = 'Scheduled'
            jc.save()

        return _json_ok({'message': 'Payment successful! Your vehicle check is now scheduled.'})

    except Exception as e:
        print("DB Error (pay_check_api):", e)
        return _json_error('Database error: ' + str(e), 500)


def vehicle_track_api_view(request, vehicle_id):
    """GET /api/vehicle-track/<vehicle_id> - Strictly based on Appointment Status."""
    user_data = _get_session_user(request)
    if not user_data:
        return _json_error('Unauthorized', 401)

    try:
        vehicle = Vehicle.objects.filter(vehicle_id=vehicle_id).first()
        if not vehicle:
            return _json_error('Vehicle not found', 404)

        # 1. Find the latest active appointment for this vehicle (exclude Cancelled)
        app = Appointment.objects.filter(vehicle=vehicle).exclude(status='Cancelled').order_by('-appointment_id').first()
        if not app:
            return _json_error('No service history found', 404)

        # 2. Check for linked Jobcard (if any)
        jc = Jobcard.objects.filter(appointment=app).first()
        has_tech = jc and jc.technician_id is not None

        # 3. Use Jobcard status if it exists and is not empty, else Appointment status
        status = jc.status if (jc and jc.status) else app.status
        
        # 4. Map to 5 steps
        step = 1
        label = "Booking Received"
        progress = 20

        if status == 'Scheduled':
            step = 1
            label = "Booking Received"
            progress = 20
        elif status == 'Confirmed':
            if has_tech:
                step = 3
                label = "Technician Assigned"
                progress = 60
            else:
                step = 2
                label = "Appointment Confirmed"
                progress = 40
        elif status == 'In Progress':
            step = 4
            label = "Service Underway"
            progress = 80
        elif status in ['Completed', 'Closed']:
            step = 5
            label = "Service Completed"
            progress = 100

        tech_name = jc.technician.firstname if (has_tech and jc.technician) else 'Assigning...'

        return JsonResponse({
            'appointment_id': app.appointment_id,
            'status': status,
            'progress': progress,
            'step': step,
            'label': label,
            'technician': tech_name,
            'last_update': app.date_time.strftime('%Y-%m-%d %H:%M') if app.date_time else '--',
            'vehicle_name': f"{vehicle.make} {vehicle.model}"
        })

    except Exception as e:
        print('Track Error:', e)
        return _json_error(str(e), 500)

    except Exception as e:
        print('Track Error:', e)
        return _json_error(str(e), 500)
