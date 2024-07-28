async function calculateTotal() {
    const sushiA = parseInt(document.getElementById("sushi-a").value) || 0;
    const sushiB = parseInt(document.getElementById("sushi-b").value) || 0;
    const totalPieces = sushiA + sushiB;

    let totalPrice = sushiA * 3 + sushiB * 4;
    let discount = 0;

    // Calculate discounts
    if (totalPieces >= 20) {
        discount = totalPrice * 0.20;
    } else if (totalPieces >= 10) {
        discount = totalPrice * 0.10;
    }

    // Lunch discount
    const now = new Date();
    const hours = now.getHours();
    if (hours >= 11 && hours < 14) {
        discount += totalPrice * 0.20;
    }

    const finalPrice = totalPrice - discount;

    document.getElementById("total-price").innerText = `Total Price: £${finalPrice.toFixed(2)}`;
    document.getElementById("discount").innerText = `Discount: £${discount.toFixed(2)}`;
}

async function placeOrder() {
    const sushiA = parseInt(document.getElementById("sushi-a").value) || 0;
    const sushiB = parseInt(document.getElementById("sushi-b").value) || 0;

    const sushiItems = {
        1: sushiA,
        2: sushiB
    };

    await fetch("http://localhost:5000/add-order", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ sushi_items: sushiItems })
    });
    alert("Order placed successfully!");
    document.getElementById("sushi-a").value = 0;
    document.getElementById("sushi-b").value = 0;
    document.getElementById("total-price").innerText = "Total Price: £0";
    document.getElementById("discount").innerText = "Discount: £0";
}

async function fetchOrders() {
    const response = await fetch("http://localhost:5000/get-orders");
    const data = await response.json();

    const ordersDiv = document.getElementById("orders");
    ordersDiv.innerHTML = ""; // Clear previous orders

    data.orders.forEach(order => {
        const orderElement = document.createElement("div");
        orderElement.innerHTML = `
            <p><strong>Order ID:</strong> ${order.id}</p>
            <p><strong>Sushi:</strong> ${order.name} x ${order.quantity}</p>
            <p><strong>Price per Sushi:</strong> £${order.price}</p>
            <p><strong>Discount Applied:</strong> ${order.discount_applied}</p>
            <p><strong>Discount Amount:</strong> £${order.discount_amount}</p>
            <p><strong>Total Price:</strong> £${order.total_price}</p>
            <hr>
        `;
        ordersDiv.appendChild(orderElement);
    });
}


async function clearAllData() {
    const response = await fetch("http://localhost:5000/clear-all", {
        method: "DELETE"
    });

    if (response.ok) {
        alert("All data cleared successfully!");
        document.getElementById("orders").innerHTML = ""; // Clear displayed orders
    } else {
        alert("Failed to clear data. Please try again.");
    }
}