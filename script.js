let socket;
let userData = null;

document.getElementById("connectBtn").addEventListener("click", () => {
  if (socket && socket.readyState === WebSocket.OPEN) {
    console.log("WebSocket is already connected.");
    return;
  }

  socket = new WebSocket("ws://localhost:8765");

  socket.onopen = () => {
    console.log("Connected to WebSocket server!");
    document.getElementById("getUserInfoBtn").disabled = false;
    document.getElementById("updateEmailBtn").disabled = false;
  };

  socket.onmessage = (event) => {
    try {
      const parsedData = JSON.parse(event.data);
      console.log("Received data:", parsedData);

      if (parsedData.user_data) {
        userData = parsedData.user_data;
        document.getElementById("response").innerText = JSON.stringify(parsedData, null, 4);
        document.getElementById("emailInput").value = userData.email;
      }
    } catch (error) {
      console.error("Error parsing message:", error);
    }
  };

  socket.onclose = (event) => {
    console.warn("WebSocket connection closed!", event);
  };

  socket.onerror = (error) => {
    console.error("WebSocket error occurred:", error);
  };
});

document.getElementById("getUserInfoBtn").addEventListener("click", () => {
  if (socket && socket.readyState === WebSocket.OPEN) {
    socket.send("get_user_info");
  } else {
    console.error("WebSocket is not connected!");
  }
});

document.getElementById("updateEmailBtn").addEventListener("click", () => {
  if (socket && socket.readyState === WebSocket.OPEN) {
    const newEmail = document.getElementById("emailInput").value.trim();
    if (newEmail) {
      const updateData = {
        action: "update_user_info",
        user_data: { email: newEmail }
      };
      socket.send(JSON.stringify(updateData));
    } else {
      console.error("Invalid email input.");
    }
  } else {
    console.error("WebSocket is not connected!");
  }
});