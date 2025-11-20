function guardarCarritoEnBD() {
  let carrito = JSON.parse(localStorage.getItem('cart')) || [];

  if (carrito.length === 0) {
    alert("Tu carrito está vacío 🛒");
    return;
  }

  fetch("/guardar_carrito", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ productos: carrito })
  })
  .then(res => res.json())
  .then(data => {
    if (data.message) {
      alert(data.message);
      localStorage.removeItem("cart");
    } else if (data.error) {
      alert("Error: " + data.error);
    }
  })
  .catch(err => {
    console.error("Error al guardar el carrito:", err);
    alert("Hubo un error al guardar el carrito ❌");
  });
}
