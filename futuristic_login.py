import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Futuristic Login", layout="centered")

# Title
st.markdown("<h1 style='text-align:center; color:cyan;'>🚀 Welcome to the Futuristic Login Page</h1>", unsafe_allow_html=True)

# Embed HTML
components.html("""
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>Futuristic Login</title>
  <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
  <script src="https://cdn.jsdelivr.net/npm/tsparticles@2.11.1/tsparticles.bundle.min.js"></script>
  <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&display=swap');
    * {
      margin: 0; padding: 0; box-sizing: border-box;
      font-family: 'Orbitron', sans-serif;
    }
    html, body {
      height: 100%;
      background: #0f0c29;
    }
    #tsparticles {
      position: fixed;
      width: 100%;
      height: 100%;
      z-index: 0;
    }
    .login-box {
      position: relative;
      z-index: 1;
      margin: 0 auto;
      top: 10vh;
      background: rgba(0,0,0,0.7);
      padding: 40px;
      border-radius: 20px;
      max-width: 400px;
      color: white;
      box-shadow: 0 0 25px rgba(0, 255, 255, 0.2);
    }
    .login-box h2 {
      text-align: center;
      color: #00f0ff;
      margin-bottom: 30px;
    }
    .input-wrapper {
      position: relative;
      margin-bottom: 20px;
    }
    .input-wrapper i {
      position: absolute;
      top: 50%;
      left: 15px;
      transform: translateY(-50%);
      color: #7efcff;
    }
    .input-wrapper input {
      width: 100%;
      height: 45px;
      padding: 0 15px 0 40px;
      border: 1px solid #00f0ff;
      background: transparent;
      color: white;
      border-radius: 25px;
      font-size: 14px;
      outline: none;
    }
    .login-box button {
      width: 100%;
      height: 48px;
      background: linear-gradient(135deg, #00f0ff, #ff00e0);
      color: white;
      font-weight: bold;
      font-size: 16px;
      border: none;
      border-radius: 25px;
      cursor: pointer;
    }
  </style>
</head>
<body>
  <div id="tsparticles"></div>
  <div class="login-box">
    <h2>Welcome Back</h2>
    <div class="input-wrapper">
      <i class="fas fa-user"></i>
      <input type="text" placeholder="Username"/>
    </div>
    <div class="input-wrapper">
      <i class="fas fa-lock"></i>
      <input type="password" placeholder="Password"/>
    </div>
    <button onclick="alert('Simulated login. Integrate backend for real auth.')">LOGIN</button>
  </div>
  <script>
    tsParticles.load("tsparticles", {
      background: { color: "#0f0c29" },
      particles: {
        number: { value: 100 },
        color: { value: ["#00f0ff", "#ff00e0", "#ffc400"] },
        shape: { type: ["circle", "square"] },
        opacity: { value: 0.7 },
        size: { value: 4 },
        move: { enable: true, speed: 1, outModes: "bounce" }
      },
      interactivity: {
        events: {
          onHover: { enable: true, mode: "repulse" },
          onClick: { enable: true, mode: "push" }
        },
        modes: {
          repulse: { distance: 100 },
          push: { quantity: 4 }
        }
      },
      detectRetina: true
    });
  </script>
</body>
</html>
""", height=600, width=800) 
