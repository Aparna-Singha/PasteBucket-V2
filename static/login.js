if (localStorage.getItem("username") !== null) {
  document.querySelector('.auth-modal').classList.add('hidden');
}

function toggleAuthMode() {
  document.querySelector('.auth-modal').classList.toggle('sign-up-modal');
  document.querySelector('.auth-modal').classList.toggle('sign-in-modal');
}

function signIn() {
  let username = document.getElementById("username").value;
  let password = document.getElementById("password").value;

  let data = {
    username: username,
    password: password,
  };

  fetch("/sign-in", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  }).then((response) => response.json()).then((data) => {
    if (data.status === 200) {
      alert("Login successful");
      localStorage.setItem("username", username);
      location.reload();
    } else {
      alert(`Login failed: ${data.message}`);
    }
  });
}

function signUp() {
  let username = document.getElementById("username").value;
  let password = document.getElementById("password").value;

  let data = {
    username: username,
    password: password,
  };

  fetch("/sign-up", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  }).then((response) => response.json()).then((data) => {
    if (data.status === 200) {
      alert("Sign up successful");
      localStorage.setItem("username", username);
      location.reload();
    } else {
      alert(`Login failed: ${data.message}`);
    }
  });
}
