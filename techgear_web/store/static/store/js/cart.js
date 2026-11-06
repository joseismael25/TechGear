(() => {
  "use strict";
  const STORAGE_KEY = "techgear_cart_v1";
  const toNumber = value => {
    if (typeof value === "string") {
      let raw = value.trim().replace(/[^0-9,.-]/g, "");
      if (raw.includes(",") && raw.includes(".")) {
        raw = raw.lastIndexOf(",") > raw.lastIndexOf(".")
          ? raw.replace(/\./g, "").replace(",", ".")
          : raw.replace(/,/g, "");
      } else if (raw.includes(",")) {
        raw = /,\d{1,2}$/.test(raw) ? raw.replace(",", ".") : raw.replace(/,/g, "");
      } else if (raw.includes(".")) {
        raw = /\.\d{1,2}$/.test(raw) ? raw : raw.replace(/\./g, "");
      }
      value = raw;
    }
    const number = Number(value);
    return Number.isFinite(number) && number >= 0 ? number : 0;
  };
  const normalizeItem = item => {
    if (!item || typeof item !== "object") return null;
    const productId = String(item.product_id ?? item.id ?? "").trim();
    const quantity = Math.floor(toNumber(item.quantity ?? item.cantidad));
    const price = toNumber(item.price ?? item.precio ?? item.valor ?? item.precio_unitario);
    if (!productId || quantity < 1) return null;
    return {
      product_id: productId,
      name: String(item.name ?? item.nombre ?? "Producto"),
      price,
      quantity,
      stock: Math.max(quantity, Math.floor(toNumber(item.stock ?? quantity))),
      image: String(item.image ?? item.image_url ?? "")
    };
  };
  const readCart = () => {
    try {
      const value = JSON.parse(localStorage.getItem(STORAGE_KEY) || "[]");
      return Array.isArray(value) ? value.map(normalizeItem).filter(Boolean) : [];
    } catch (_) { return []; }
  };
  let cart = readCart();
  let pendingInvoice = false;
  const money = value => new Intl.NumberFormat("es-CO", {
    style: "currency", currency: "COP", maximumFractionDigits: 0
  }).format(toNumber(value));
  const save = () => {
    try { localStorage.setItem(STORAGE_KEY, JSON.stringify(cart)); } catch (_) { /* El carrito sigue disponible en memoria. */ }
    render();
  };
  const count = () => cart.reduce((sum, item) => sum + item.quantity, 0);
  const safeImage = value => {
    try {
      const url = new URL(value, window.location.origin);
      return ["http:", "https:"].includes(url.protocol) ? url.href : "";
    } catch (_) { return ""; }
  };
  function render() {
    const countNode = document.getElementById("cart-count");
    const list = document.getElementById("cart-items");
    const totalNode = document.getElementById("cart-total");
    if (countNode) countNode.textContent = String(count());
    const floatingButton = document.getElementById("floating-cart");
    if (floatingButton) floatingButton.setAttribute("aria-label", `Abrir carrito, ${count()} productos`);
    if (!list || !totalNode) return;
    list.replaceChildren();
    if (!cart.length) {
      const empty = document.createElement("div");
      empty.className = "text-center py-4";
      const message = document.createElement("p");
      message.className = "fw-semibold mb-3";
      message.textContent = "Tu carrito está vacío";
      const catalog = document.createElement("a");
      catalog.className = "btn btn-primary";
      catalog.href = "/";
      catalog.textContent = "Ver catálogo";
      empty.append(message, catalog);
      list.append(empty);
    }
    let total = 0;
    cart.forEach(item => {
      const subtotal = item.price * item.quantity;
      total += subtotal;
      const row = document.createElement("div");
      row.className = "d-flex flex-wrap align-items-center gap-3 border rounded p-3 cart-row";
      const imageUrl = safeImage(item.image);
      if (imageUrl) {
        const img = document.createElement("img");
        img.src = imageUrl; img.alt = ""; img.width = 64; img.height = 64;
        img.loading = "lazy"; img.className = "rounded object-fit-contain cart-thumb";
        row.append(img);
      }
      const info = document.createElement("div");
      info.className = "flex-grow-1 cart-item-info";
      const name = document.createElement("strong");
      name.className = "d-block"; name.textContent = item.name;
      const price = document.createElement("span");
      price.className = "d-block small"; price.textContent = money(item.price) + " c/u";
      const subtotalNode = document.createElement("span");
      subtotalNode.className = "d-block fw-semibold";
      subtotalNode.textContent = "Subtotal: " + money(subtotal);
      info.append(name, price, subtotalNode);
      const controls = document.createElement("div");
      controls.className = "d-flex align-items-center gap-1 flex-wrap";
      [["−", "decrease"], [String(item.quantity), "quantity"], ["+", "increase"]].forEach(([label, action]) => {
        const button = document.createElement("button");
        button.type = "button"; button.className = "btn btn-sm btn-outline-secondary";
        button.textContent = label; button.dataset.action = action;
        button.dataset.id = item.product_id;
        button.setAttribute("aria-label", action === "decrease" ? `Disminuir ${item.name}` : action === "increase" ? `Aumentar ${item.name}` : `Cantidad de ${item.name}`);
        if (action === "quantity") button.disabled = true;
        controls.append(button);
      });
      const remove = document.createElement("button");
      remove.type = "button"; remove.className = "btn btn-sm btn-outline-danger";
      remove.textContent = "Eliminar"; remove.dataset.action = "remove";
      remove.dataset.id = item.product_id;
      controls.append(remove);
      row.append(info, controls); list.append(row);
    });
    totalNode.textContent = money(total);
    const checkout = document.getElementById("checkout-cart");
    if (checkout) checkout.disabled = !cart.length;
  }
  function showInvoice(order, snapshot) {
    const orderItems = Array.isArray(order.items) ? order.items : [];
    const tbody = document.getElementById("invoice-items");
    const client = document.getElementById("invoice-client");
    const number = document.getElementById("invoice-number");
    const date = document.getElementById("invoice-date");
    const subtotalNode = document.getElementById("invoice-subtotal");
    const totalNode = document.getElementById("invoice-total");
    if (!tbody || !client || !number || !date || !subtotalNode || !totalNode) return;
    tbody.replaceChildren();
    let total = 0;
    orderItems.forEach((line, index) => {
      const original = snapshot.find(item => item.product_id === String(line.product_id)) || snapshot[index] || {};
      const quantity = Math.max(0, Number(line.cantidad) || 0);
      const unit = toNumber(line.precio_unitario ?? original.price);
      const lineTotal = unit * quantity;
      total += lineTotal;
      const tr = document.createElement("tr");
      const productCell = document.createElement("td");
      const productWrap = document.createElement("div");
      productWrap.className = "d-flex align-items-center gap-2";
      const image = safeImage(original.image);
      if (image) {
        const img = document.createElement("img"); img.src = image; img.alt = "";
        img.width = 44; img.height = 44; img.className = "object-fit-contain rounded";
        productWrap.append(img);
      }
      const productName = document.createElement("span");
      productName.textContent = original.name || "Producto";
      productWrap.append(productName); productCell.append(productWrap);
      [productCell, ...[quantity, money(unit), money(lineTotal)].map(value => {
        const td = document.createElement("td"); td.textContent = String(value); return td;
      })].forEach(td => tr.append(td));
      tbody.append(tr);
    });
    client.textContent = document.body.dataset.clientName || "Cliente";
    number.textContent = "#TG-" + String(order.id || Date.now()).slice(-8).toUpperCase();
    const createdAt = order.fecha ? new Date(order.fecha) : new Date();
    date.textContent = Number.isNaN(createdAt.getTime()) ? new Date().toLocaleString("es-CO") : createdAt.toLocaleString("es-CO");
    subtotalNode.textContent = money(total);
    totalNode.textContent = money(toNumber(order.total) || total);
    const cartModal = bootstrap.Modal.getInstance(document.getElementById("cartModal"));
    cartModal?.hide();
    bootstrap.Modal.getOrCreateInstance(document.getElementById("invoiceModal")).show();
    pendingInvoice = true;
  }
  document.addEventListener("click", event => {
    const add = event.target.closest(".add-to-cart");
    if (add) {
      const card = add.closest(".product-body");
      const input = card && card.querySelector(".product-quantity");
      const stock = Math.floor(toNumber(add.dataset.stock));
      const quantity = Math.floor(toNumber(input && input.value));
      const price = toNumber(add.dataset.price ?? add.dataset.precio);
      if (!Number.isInteger(quantity) || quantity < 1 || quantity > stock || price <= 0) {
        const feedback = document.getElementById("cart-feedback");
        if (feedback) feedback.textContent = price <= 0 ? "Este producto no tiene un precio válido." : "Selecciona una cantidad válida según el stock.";
        return;
      }
      const id = String(add.dataset.id || "");
      const existing = cart.find(item => item.product_id === id);
      if (existing) {
        if (existing.quantity + quantity > stock) {
          const feedback = document.getElementById("cart-feedback");
          if (feedback) feedback.textContent = "No puedes superar las unidades disponibles.";
          return;
        }
        existing.quantity += quantity; existing.stock = stock;
        existing.price = price; existing.name = add.dataset.name || existing.name;
        existing.image = add.dataset.image || existing.image;
      } else {
        cart.push({ product_id: id, name: add.dataset.name || "Producto", price,
          quantity, stock, image: add.dataset.image || "" });
      }
      save();
      const feedback = document.getElementById("cart-feedback");
      if (feedback) feedback.textContent = "Producto agregado al carrito.";
    }
    const action = event.target.closest("[data-action]");
    if (action) {
      const item = cart.find(entry => entry.product_id === action.dataset.id);
      if (!item) return;
      if (action.dataset.action === "increase" && item.quantity < item.stock) item.quantity++;
      if (action.dataset.action === "decrease" && item.quantity > 1) item.quantity--;
      if (action.dataset.action === "remove") cart = cart.filter(entry => entry !== item);
      save();
    }
  });
  document.getElementById("clear-cart")?.addEventListener("click", () => {
    cart = []; save();
    const feedback = document.getElementById("cart-feedback");
    if (feedback) feedback.textContent = "Carrito vacío.";
  });
  document.getElementById("checkout-cart")?.addEventListener("click", async event => {
    const feedback = document.getElementById("cart-feedback");
    const button = event.currentTarget;
    if (!cart.length) { if (feedback) feedback.textContent = "Agrega productos antes de finalizar la compra."; return; }
    const snapshot = cart.map(item => ({...item}));
    button.disabled = true;
    if (feedback) feedback.textContent = "Generando informe de compra…";
    const csrf = document.cookie.split("; ").find(row => row.startsWith("csrftoken="))?.split("=")[1] || "";
    try {
      const response = await fetch("/checkout/", {
        method: "POST",
        headers: {"Content-Type": "application/json", "X-CSRFToken": decodeURIComponent(csrf)},
        body: JSON.stringify({items: snapshot.map(item => ({
          product_id: item.product_id, cantidad: item.quantity, precio_unitario: item.price
        }))})
      });
      const data = await response.json();
      if (!response.ok) {
        if (response.status === 401) {
          if (feedback) feedback.textContent = (data.error || "Inicia sesión para comprar.") + " ";
          const link = document.createElement("a"); link.href = "/login/";
          link.textContent = "Iniciar sesión"; feedback?.append(link);
        } else if (feedback) feedback.textContent = data.error || "No se pudo procesar el pedido.";
        return;
      }
      showInvoice(data.order || {}, snapshot);
      if (feedback) feedback.textContent = "";
    } catch (_) {
      if (feedback) feedback.textContent = "No se pudo conectar con el servidor. Tu carrito sigue guardado.";
    } finally { button.disabled = false; }
  });
  document.getElementById("invoice-print")?.addEventListener("click", () => window.print());
  document.getElementById("invoice-continue")?.addEventListener("click", () => {
    // El stock ya fue descontado por FastAPI en MongoDB.
    // Al cerrar el informe se recarga el catálogo para mostrar las existencias reales.
    bootstrap.Modal.getInstance(document.getElementById("invoiceModal"))?.hide();
  });
  document.getElementById("invoiceModal")?.addEventListener("hidden.bs.modal", () => {
    if (pendingInvoice) {
      cart = [];
      save();
      pendingInvoice = false;
      window.location.reload();
    }
  });
  render();
})();
