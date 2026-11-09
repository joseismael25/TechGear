import requests
import json
from urllib.parse import urlparse
from functools import wraps

from django.conf import settings
from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST

TIMEOUT = 12  # Evita mantener bloqueado el portal demasiado tiempo
LOW_STOCK = 5


# ---------------------------------------------------------------- helpers API
def _url(path):
    return f"{settings.API_URL}{path}"


def _auth_headers(request):
    return {"Authorization": f"Bearer {request.session.get('access_token', '')}"}


def _session_expired(request):
    """Token vencido o invalido: limpiamos la sesion y mandamos a login."""
    request.session.flush()
    messages.warning(request, "Tu sesión expiró. Inicia sesión de nuevo.")
    return redirect("login")


def _fetch_products():
    try:
        resp = requests.get(_url("/products"), timeout=TIMEOUT)
        if resp.status_code == 200:
            payload = resp.json()
            return payload if isinstance(payload, list) else None
    except (requests.exceptions.RequestException, ValueError):
        pass
    return None  # None = la API no respondio


def _api_error(resp, default):
    try:
        payload = resp.json()
        detail = payload.get("detail", default) if isinstance(payload, dict) else default
    except ValueError:
        return default
    return detail if isinstance(detail, str) else "Datos inválidos, revisa el formulario."


def session_required(view):
    """Protege las vistas que requieren una sesión autenticada."""
    @wraps(view)
    def wrapper(request, *args, **kwargs):
        token = request.session.get("access_token")
        if not token:
            messages.warning(request, "Inicia sesión para acceder a tu panel.")
            return redirect("login")
        try:
            response = requests.get(_url("/users/me"), headers={"Authorization": f"Bearer {token}"}, timeout=TIMEOUT)
            if response.status_code == 401:
                return _session_expired(request)
            if response.status_code == 200:
                profile = response.json()
                request.session["user_nombre"] = profile.get("nombre", request.session.get("user_email", "Usuario"))
                request.session["rol"] = profile.get("rol", "cliente")
        except (requests.exceptions.RequestException, ValueError):
            # Si la API está temporalmente fuera de línea, se muestra el panel con aviso.
            pass
        return view(request, *args, **kwargs)
    return wrapper


def admin_required(view):
    """Solo deja pasar a usuarios con sesion y rol admin."""
    @wraps(view)
    def wrapper(request, *args, **kwargs):
        if not request.session.get("access_token"):
            messages.warning(request, "Debes iniciar sesión para continuar.")
            return redirect("login")
        if request.session.get("rol") != "admin":
            messages.error(request, "No tienes permisos de administrador.")
            return redirect("product_list")
        return view(request, *args, **kwargs)
    return wrapper


# ------------------------------------------------------------------- catalogo
def product_list(request):
    products = _fetch_products()
    api_down = products is None
    products = products or []

    q = request.GET.get("q", "").strip().lower()
    categoria = request.GET.get("categoria", "").strip()
    categorias = sorted({p.get("categoria", "") for p in products if p.get("categoria")})

    if q:
        products = [
            p for p in products
            if q in str(p.get("nombre") or "").lower()
            or q in str(p.get("descripcion") or "").lower()
        ]
    if categoria:
        products = [p for p in products if p.get("categoria") == categoria]

    return render(request, "store/product_list.html", {
        "products": products,
        "categorias": categorias,
        "q": request.GET.get("q", ""),
        "categoria_sel": categoria,
        "api_down": api_down,
        "low_stock": LOW_STOCK,
    })


# ---------------------------------------------------------------------- auth
def login_view(request):
    if request.session.get("access_token"):
        return redirect("dashboard")

    if request.method == "POST":
        email = request.POST.get("email", "").strip()
        password = request.POST.get("password", "")

        try:
            resp = requests.post(
                _url("/auth/login"),
                json={
                    "email": email,
                    "password": password
                },
                timeout=TIMEOUT
            )

            if resp.status_code == 200:
                token = resp.json().get("access_token")

                if not token:
                    return render(
                        request,
                        "store/login.html",
                        {
                            "error": "La API no devolvió un token válido",
                            "email": email
                        }
                    )

                # Consultar el perfil del usuario.
                me = requests.get(
                    _url("/users/me"),
                    headers={
                        "Authorization": f"Bearer {token}"
                    },
                    timeout=TIMEOUT
                )

                try:
                    perfil = me.json() if me.status_code == 200 else {}
                except ValueError:
                    perfil = {}

                # Guardar los datos de sesión.
                # No se utiliza cycle_key porque ahora usamos
                # sesiones mediante cookies firmadas.
                request.session["access_token"] = token
                request.session["user_email"] = email
                request.session["user_id"] = perfil.get("id", "")
                request.session["user_nombre"] = perfil.get(
                    "nombre",
                    email
                )
                request.session["rol"] = perfil.get(
                    "rol",
                    "cliente"
                )

                messages.success(
                    request,
                    f"¡Bienvenido, {request.session['user_nombre']}!"
                )

                return redirect("dashboard")

            if resp.status_code == 401:
                return render(
                    request,
                    "store/login.html",
                    {
                        "error": "Correo o contraseña incorrectos",
                        "email": email
                    }
                )

            return render(
                request,
                "store/login.html",
                {
                    "error": "La API respondió con un error inesperado",
                    "email": email
                }
            )

        except requests.exceptions.RequestException:
            return render(
                request,
                "store/login.html",
                {
                    "error": "No se pudo conectar con la API",
                    "email": email
                }
            )

    return render(request, "store/login.html")


def register_view(request):
    if request.session.get("access_token"):
        return redirect("dashboard")
    if request.method == "POST":
        payload = {
            "nombre": request.POST.get("nombre", "").strip(),
            "email": request.POST.get("email", "").strip(),
            "password": request.POST.get("password", ""),
        }
        try:
            resp = requests.post(_url("/users"), json=payload, timeout=TIMEOUT)
            if resp.status_code == 201:
                messages.success(request, "Cuenta creada. Ya puedes iniciar sesión.")
                return redirect("login")
            return render(request, "store/register.html", {
                "error": _api_error(resp, "No se pudo crear la cuenta"), "form": payload})
        except requests.exceptions.RequestException:
            return render(request, "store/register.html", {"error": "No se pudo conectar con la API", "form": payload})
    return render(request, "store/register.html")


@require_POST
def logout_view(request):
    request.session.flush()  # elimina el token JWT y el rol de la sesion
    messages.info(request, "Sesión cerrada correctamente.")
    return redirect("product_list")


# ------------------------------------------------------ dashboard (CRUD admin)
def _safe_int(value, default=0):
    """Convierte valores numéricos externos sin romper el panel."""
    try:
        return int(value or 0)
    except (TypeError, ValueError, OverflowError):
        return default


def _safe_float(value, default=0.0):
    """Convierte importes externos y descarta NaN/infinitos."""
    import math
    try:
        number = float(value or 0)
        return number if math.isfinite(number) else default
    except (TypeError, ValueError, OverflowError):
        return default


def _fetch_private_list(path, token):
    """Consulta una lista privada de la API usando el JWT de la sesión."""
    try:
        response = requests.get(
            _url(path), headers={"Authorization": f"Bearer {token}"}, timeout=TIMEOUT
        )
        if response.status_code == 200:
            payload = response.json()
            return payload if isinstance(payload, list) else None
    except (requests.exceptions.RequestException, ValueError):
        pass
    return None


@session_required
def dashboard(request):
    products = _fetch_products()
    token = request.session.get("access_token", "")
    orders = _fetch_private_list("/orders", token)
    api_down = products is None or orders is None
    products = products or []
    orders = orders or []
    # Ignora registros mal formados para que un dato incompleto no provoque HTTP 500.
    products = [item for item in products if isinstance(item, dict)]
    orders = [item for item in orders if isinstance(item, dict)]
    orders.sort(key=lambda item: str(item.get("fecha", "")), reverse=True)

    stats = {
        "total": len(products),
        "unidades": sum(_safe_int(p.get("stock")) for p in products),
        "valor": sum(_safe_float(p.get("precio")) * _safe_int(p.get("stock")) for p in products),
        "bajo_stock": sum(1 for p in products if _safe_int(p.get("stock")) <= LOW_STOCK),
        "ventas": len(orders),
        "total_ventas": sum(_safe_float(order.get("total")) for order in orders),
    }
    recent_products = products[:5]
    recent_orders = orders[:5]
    is_admin = request.session.get("rol") == "admin"
    users = _fetch_private_list("/users", token) if is_admin else []
    stats["usuarios"] = len(users or [])
    low_stock_percent = round((stats["bajo_stock"] / stats["total"]) * 100) if stats["total"] else 0
    customer_stats = {
        "total": stats["total"],
        "categorias": len({p.get("categoria") for p in products if p.get("categoria")}),
        "disponibles": sum(1 for p in products if _safe_int(p.get("stock")) > 0),
        "pedidos": len(orders),
        "total_pedidos": stats["total_ventas"],
    }
    return render(request, "store/dashboard.html", {
        "products": products, "recent_products": recent_products, "recent_orders": recent_orders,
        "stats": stats, "customer_stats": customer_stats, "api_down": api_down,
        "low_stock": LOW_STOCK, "low_stock_percent": low_stock_percent, "is_admin": is_admin,
    })


def _parse_product(post):
    """Valida el formulario y devuelve (datos, errores)."""
    data = {
        "nombre": post.get("nombre", "").strip(),
        "descripcion": post.get("descripcion", "").strip(),
        "categoria": post.get("categoria", "").strip(),
        "image_url": post.get("image_url", "").strip(),
        "precio": post.get("precio", "").strip(),
        "stock": post.get("stock", "").strip(),
    }
    errors = []
    if not data["nombre"]:
        errors.append("El nombre es obligatorio.")
    if not data["categoria"]:
        errors.append("La categoría es obligatoria.")
    if data["image_url"]:
        parsed = urlparse(data["image_url"])
        if parsed.scheme not in {"http", "https"} or not parsed.netloc:
            errors.append("La URL de la imagen debe comenzar con http:// o https://.")
    try:
        data["precio"] = float(data["precio"])
        if data["precio"] <= 0:
            errors.append("El precio debe ser mayor que 0.")
    except ValueError:
        errors.append("El precio debe ser un número.")
    try:
        data["stock"] = int(data["stock"])
        if data["stock"] < 0:
            errors.append("El stock no puede ser negativo.")
    except ValueError:
        errors.append("El stock debe ser un número entero.")
    return data, errors


def _upload_product_image(request):
    """Envía una imagen local a FastAPI y devuelve su URL pública."""
    uploaded = request.FILES.get("imagen")
    if not uploaded:
        return None, None
    if uploaded.size > 5 * 1024 * 1024:
        return None, "La imagen no puede superar 5 MB."
    content_type = uploaded.content_type or ""
    if content_type not in {"image/jpeg", "image/png", "image/webp"}:
        return None, "Formato no permitido. Selecciona JPG, PNG o WebP."
    try:
        response = requests.post(
            _url("/images"),
            headers=_auth_headers(request),
            files={"image": (uploaded.name, uploaded.file, content_type)},
            timeout=30,
        )
    except requests.exceptions.RequestException:
        return None, "No se pudo subir la imagen al servidor."
    if response.status_code == 401:
        return None, "SESSION_EXPIRED"
    if response.status_code != 201:
        return None, _api_error(response, "No se pudo guardar la imagen.")
    try:
        return response.json().get("image_url"), None
    except ValueError:
        return None, "La API devolvió una respuesta de imagen inválida."


def _form_ctx(modo, product, errors=None):
    return {"modo": modo, "product": product, "errors": errors or []}


@admin_required
def product_create(request):
    if request.method == "POST":
        data, errors = _parse_product(request.POST)
        if not errors:
            image_url, image_error = _upload_product_image(request)
            if image_error:
                if image_error == "SESSION_EXPIRED":
                    return _session_expired(request)
                errors.append(image_error)
            if image_url:
                data["image_url"] = image_url
        if errors:
            return render(request, "store/product_form.html", _form_ctx("crear", request.POST, errors))
        try:
            resp = requests.post(_url("/products"), json=data, headers=_auth_headers(request), timeout=TIMEOUT)
        except requests.exceptions.RequestException:
            return render(request, "store/product_form.html",
                          _form_ctx("crear", request.POST, ["No se pudo conectar con la API."]))
        if resp.status_code == 401:
            return _session_expired(request)
        if resp.status_code == 201:
            messages.success(request, f"Producto «{data['nombre']}» creado correctamente.")
            return redirect("dashboard")
        return render(request, "store/product_form.html",
                      _form_ctx("crear", request.POST, [_api_error(resp, "No se pudo crear el producto.")]))
    return render(request, "store/product_form.html", _form_ctx("crear", {}))


@admin_required
def product_update(request, product_id):
    if request.method == "POST":
        data, errors = _parse_product(request.POST)
        product = dict(request.POST.items(), id=product_id)
        current_image = request.POST.get("current_image_url", "").strip()
        if request.POST.get("remove_image") == "on":
            data["image_url"] = ""
        elif data.get("image_url"):
            pass  # Si se proporciona URL, tiene prioridad sobre la imagen anterior.
        else:
            data["image_url"] = current_image or None
        if not errors:
            image_url, image_error = _upload_product_image(request)
            if image_error:
                if image_error == "SESSION_EXPIRED":
                    return _session_expired(request)
                errors.append(image_error)
            if image_url:
                data["image_url"] = image_url
        if errors:
            product["image_url"] = current_image
            return render(request, "store/product_form.html", _form_ctx("editar", product, errors))
        try:
            resp = requests.put(_url(f"/products/{product_id}"), json=data,
                                headers=_auth_headers(request), timeout=TIMEOUT)
        except requests.exceptions.RequestException:
            return render(request, "store/product_form.html",
                          _form_ctx("editar", product, ["No se pudo conectar con la API."]))
        if resp.status_code == 401:
            return _session_expired(request)
        if resp.status_code == 200:
            messages.success(request, f"Producto «{data['nombre']}» actualizado.")
            return redirect("dashboard")
        return render(request, "store/product_form.html",
                      _form_ctx("editar", product, [_api_error(resp, "No se pudo actualizar el producto.")]))

    # GET: precargamos el formulario con los datos actuales
    try:
        resp = requests.get(_url(f"/products/{product_id}"), timeout=TIMEOUT)
    except requests.exceptions.RequestException:
        messages.error(request, "No se pudo conectar con la API.")
        return redirect("dashboard")
    if resp.status_code != 200:
        messages.error(request, "El producto no existe o ya fue eliminado.")
        return redirect("dashboard")
    try:
        product = resp.json()
    except ValueError:
        messages.error(request, "La API devolvió una respuesta inválida.")
        return redirect("dashboard")
    return render(request, "store/product_form.html", _form_ctx("editar", product))


@admin_required
@require_POST
def product_delete(request, product_id):
    try:
        resp = requests.delete(_url(f"/products/{product_id}"), headers=_auth_headers(request), timeout=TIMEOUT)
    except requests.exceptions.RequestException:
        messages.error(request, "No se pudo conectar con la API.")
        return redirect("dashboard")
    if resp.status_code == 401:
        return _session_expired(request)
    if resp.status_code == 200:
        messages.success(request, "Producto eliminado correctamente.")
    else:
        messages.error(request, _api_error(resp, "No se pudo eliminar el producto."))
    return redirect("dashboard")


@require_POST
def checkout(request):
    """Envía el carrito al API; el servidor valida precio y stock."""
    token = request.session.get("access_token")
    if not token:
        return JsonResponse({"error": "Inicia sesión para finalizar la compra."}, status=401)
    try:
        payload = json.loads(request.body or "{}")
        raw_items = payload.get("items", [])
        if not isinstance(raw_items, list) or not raw_items:
            return JsonResponse({"error": "El carrito está vacío."}, status=400)
        items = []
        for item in raw_items:
            product_id = str(item.get("product_id", "")).strip()
            cantidad = int(item.get("cantidad", 0))
            precio_unitario = float(item.get("precio_unitario", 0))
            if not product_id or cantidad < 1 or precio_unitario <= 0:
                return JsonResponse({"error": "Hay productos, precios o cantidades inválidas."}, status=400)
            items.append({"product_id": product_id, "cantidad": cantidad, "precio_unitario": precio_unitario})
    except (ValueError, TypeError, AttributeError):
        return JsonResponse({"error": "No se pudo leer el carrito."}, status=400)
    try:
        response = requests.post(
            _url("/orders"),
            json={"usuario_id": request.session.get("user_id", ""), "items": items},
            headers=_auth_headers(request),
            timeout=TIMEOUT,
        )
    except requests.exceptions.RequestException:
        return JsonResponse({"error": "No se pudo conectar con el servicio de pedidos."}, status=503)
    try:
        data = response.json()
    except ValueError:
        data = {"error": "La API devolvió una respuesta inválida."}
    if response.status_code == 401:
        request.session.flush()
        return JsonResponse({"error": "Tu sesión expiró. Inicia sesión de nuevo."}, status=401)
    if response.status_code not in (200, 201):
        detail = data.get("detail", data.get("error", "No se pudo finalizar la compra."))
        return JsonResponse({"error": detail}, status=response.status_code)
    return JsonResponse({"message": "Compra exitosa", "order": data}, status=201)
