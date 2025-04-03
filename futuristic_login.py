import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Futuristic Login", layout="centered")

# Inject Colorful Floating Particles
components.html("""
<div id="tsparticles"></div>
<script src="https://cdn.jsdelivr.net/npm/tsparticles@2.11.1/tsparticles.bundle.min.js"></script>
<script>
  tsParticles.load("tsparticles", {
    fullScreen: { enable: true, zIndex: -1 },
    background: { color: "#0f0c29" },
    particles: {
      number: { value: 80 },
      color: { value: ["#00f0ff", "#ff00e0", "#ffc400", "#00ff99"] },
      shape: { type: ["circle", "square"] },
      opacity: { value: 0.6 },
      size: { value: { min: 2, max: 4 } },
      move: {
        enable: true,
        speed: 1.2,
        direction: "none",
        random: true,
        outModes: "bounce"
      },
      links: {
        enable: true,
        distance: 120,
        color: "#ffffff",
        opacity: 0.1
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
""", height=0)

# Add Custom Orbitron + FontAwesome + Neon Login Styles
st.markdown("""
<link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
<link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&display=swap" rel="stylesheet">

<style>
.stApp {
  font-family: 'Orbitron', sans-serif;
  background-color: transparent !important;
  color: white;
}

.login-box {
  background: rgba(0, 0, 0, 0.7);
  border-radius: 20px;
  padding: 40px 30px;
  max-width: 400px;
  margin: 120px auto;
  box-shadow: 0 0 25px rgba(0, 255, 255, 0.2);
  z-index: 1;
  position: relative;
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

.login-button {
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

.login-button:hover {
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
""", unsafe_allow_html=True)

# Login Form UI
st.markdown(f"""
<div class="login-box">
  <h2>Welcome Back</h2>
  <form>
    <div class="input-wrapper">
      <i class="fas fa-user"></i>
      <input type="text" placeholder="Username" name="username" required />
    </div>
    <div class="input-wrapper">
      <i class="fas fa-lock"></i>
      <input type="password" placeholder="Password" name="password" required />
    </div>
    <button class="login-button" type="submit">LOGIN</button>
    <div class="options">
      <label><input type="checkbox" checked /> Remember me</label>
      <a href="#">Forgot password?</a>
    </div>
  </form>
</div>
""", unsafe_allow_html=True) 
