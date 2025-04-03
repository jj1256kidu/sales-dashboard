import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Futuristic Login", layout="centered")

# Inject particles background with exact HTML/CSS/JS from your shared code
components.html("""
<!DOCTYPE html>
<html lang=\"en\">
<head>
  <meta charset=\"UTF-8\" />
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\"/>
  <link href=\"https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css\" rel=\"stylesheet\">
  <script src=\"https://cdn.jsdelivr.net/npm/tsparticles@2.11.1/tsparticles.bundle.min.js\"></script>
  <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&display=swap');

    * {
      margin: 0;
      padding: 0;
      box-sizing: border-box;
      font-family: 'Orbitron', sans-serif;
    }

    html, body {
      height: 100%;
      overflow: hidden;
      background: #0f0c29;
    }

    #tsparticles {
      position: absolute;
      width: 100%;
      height: 100%;
      z-index: 0;
    }

    .container {
      position: relative;
      z-index: 1;
      display: flex;
      justify-content: center;
      align-items: center;
      height: 100%;
      padding: 20px;
    }

    .login-box {
      background: rgba(0, 0, 0, 0.7);
      border-radius: 20px;
      padding: 40px 30px;
      width: 100%;
      max-width: 400px;
      box-shadow: 0 0 25px rgba(0, 255, 255, 0.2);
    }

    .login-box h2 {
      text-align: center;
      color: #00f0ff;
      margin-bottom: 30px;
      font-size: 26px;
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
      font-size: 14px;
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
      transition: box-shadow 0.3s;
    }

    .input-wrapper input:focus {
      box-shadow: 0 0 10px #00f0ff;
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
      transition: all 0.3s ease;
    }

    .login-box button:hover {
      transform: scale(1.03);
      box-shadow: 0 0 15px #00f0ff;
    }

    .options {
      display: flex;
      justify-content: space-between;
      font-size: 12px;
      color: #a0cbe8;
      margin-top: 10px;
    }

    .options a {
      color: #a0cbe8;
      text-decoration: underline;
    }
  </style>
</head>
<body>

<!-- Particle Background -->
<div id=\"tsparticles\"></div>

<!-- Login Form -->
<div class=\"container\">
  <form class=\"login-box\">
    <h2>Welcome Back</h2>
    <div class=\"input-wrapper\">
      <i class=\"fas fa-user\"></i>
      <input type=\"text\" placeholder=\"Username\" required />
    </div>
    <div class=\"input-wrapper\">
      <i class=\"fas fa-lock\"></i>
      <input type=\"password\" placeholder=\"Password\" required />
    </div>
    <button type=\"submit\">LOGIN</button>
    <div class=\"options\">
      <label><input type=\"checkbox\" checked /> Remember me</label>
      <a href=\"#\">Forgot password?</a>
    </div>
  </form>
</div>

<!-- tsparticles config -->
<script>
  tsParticles.load("tsparticles", {
    fullScreen: { enable: false },
    background: { color: "#0f0c29" },
    particles: {
      number: { value: 100 },
      color: { value: ["#00f0ff", "#ff00e0", "#ffc400"] },
      shape: { type: ["circle", "square"] },
      opacity: { value: 0.7 },
      size: { value: 4 },
      move: {
        enable: true,
        speed: 1,
        direction: "none",
        random: false,
        straight: false,
        outModes: "bounce"
      }
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
""", height=800, scrolling=False)

st.markdown("""
<style>
    .block-container {
        padding-top: 0 !important;
    }
</style>
""", unsafe_allow_html=True)

st.empty()  # Prevent default Streamlit layout from interfering
