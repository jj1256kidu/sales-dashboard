import streamlit as st
import streamlit.components.v1 as components
import time
import json
import pandas as pd

# Initialize session state for debugging
if 'debug_mode' not in st.session_state:
    st.session_state.debug_mode = False
    st.session_state.login_attempts = 0
    st.session_state.debug_log = []
    st.session_state.last_error = None
    st.session_state.performance_metrics = {
        'page_load_time': time.time(),
        'login_attempts_timing': []
    }

def log_debug_event(event_type, details):
    if st.session_state.debug_mode:
        st.session_state.debug_log.append({
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
            'type': event_type,
            'details': details
        })

# Page configuration with error handling
try:
    st.set_page_config(page_title="Futuristic Login", layout="centered")
    log_debug_event('config', 'Page configuration successful')
except Exception as e:
    st.error(f"Page configuration error: {str(e)}")
    log_debug_event('error', f'Page configuration failed: {str(e)}')
    st.session_state.last_error = str(e)

# Debug mode toggle and information
with st.sidebar:
    col1, col2 = st.columns([3, 1])
    with col1:
        st.session_state.debug_mode = st.checkbox("Debug Mode", value=st.session_state.debug_mode)
    with col2:
        if st.session_state.debug_mode and st.button("Clear Log"):
            st.session_state.debug_log = []
            st.session_state.login_attempts = 0
            log_debug_event('system', 'Debug log cleared')
    
    if st.session_state.debug_mode:
        st.write("### Debug Information")
        st.write("#### System Status")
        st.write(f"- Session Duration: {int(time.time() - st.session_state.performance_metrics['page_load_time'])}s")
        st.write(f"- Login Attempts: {st.session_state.login_attempts}")
        
        st.write("#### Performance Metrics")
        if st.session_state.performance_metrics['login_attempts_timing']:
            avg_time = sum(st.session_state.performance_metrics['login_attempts_timing']) / len(st.session_state.performance_metrics['login_attempts_timing'])
            st.write(f"- Avg Login Time: {avg_time:.2f}s")
        
        st.write("#### Last Error")
        if st.session_state.last_error:
            st.error(st.session_state.last_error)
        
        st.write("#### Debug Log")
        if st.session_state.debug_log:
            log_df = pd.DataFrame(st.session_state.debug_log)
            st.dataframe(log_df, height=200)
        
        if st.button("Export Debug Log"):
            log_json = json.dumps(st.session_state.debug_log, indent=2)
            st.download_button(
                "Download Debug Log",
                log_json,
                "debug_log.json",
                "application/json"
            )

# Title
st.markdown("<h1 style='text-align:center; color:cyan;'>🚀 Welcome to the Futuristic Login Page</h1>", unsafe_allow_html=True)

# Embed HTML with enhanced debugging
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
    /* Enhanced debug styles */
    .debug-info {
      position: fixed;
      bottom: 10px;
      right: 10px;
      background: rgba(0,0,0,0.9);
      padding: 15px;
      border-radius: 8px;
      color: #00f0ff;
      font-size: 12px;
      z-index: 1000;
      display: none;
      border: 1px solid #00f0ff;
      box-shadow: 0 0 10px rgba(0, 255, 255, 0.3);
      max-width: 300px;
    }
    .debug-info.show {
      display: block;
    }
    .debug-section {
      margin-bottom: 10px;
      padding-bottom: 5px;
      border-bottom: 1px solid rgba(0, 255, 255, 0.2);
    }
    .debug-title {
      color: #ff00e0;
      font-weight: bold;
      margin-bottom: 5px;
    }
    .debug-value {
      margin-left: 10px;
      word-break: break-all;
    }
    .debug-error {
      color: #ff3366;
    }
  </style>
</head>
<body>
  <div id="tsparticles"></div>
  <div class="login-box">
    <h2>Welcome Back</h2>
    <div class="input-wrapper">
      <i class="fas fa-user"></i>
      <input type="text" placeholder="Username" id="username" oninput="logInput('username')" autocomplete="off"/>
    </div>
    <div class="input-wrapper">
      <i class="fas fa-lock"></i>
      <input type="password" placeholder="Password" id="password" oninput="logInput('password')" autocomplete="off"/>
    </div>
    <button onclick="handleLogin()">LOGIN</button>
  </div>
  
  <!-- Enhanced debug information panel -->
  <div class="debug-info" id="debugInfo">
    <div class="debug-section">
      <div class="debug-title">System Status</div>
      <div class="debug-value" id="systemStatus">Initializing...</div>
    </div>
    <div class="debug-section">
      <div class="debug-title">Last Action</div>
      <div class="debug-value" id="lastAction">None</div>
    </div>
    <div class="debug-section">
      <div class="debug-title">Input Status</div>
      <div class="debug-value" id="inputStatus">Waiting</div>
    </div>
    <div class="debug-section">
      <div class="debug-title">Performance</div>
      <div class="debug-value" id="performance">Loading...</div>
    </div>
    <div class="debug-section">
      <div class="debug-title">Errors</div>
      <div class="debug-value debug-error" id="errors">None</div>
    </div>
  </div>

  <script>
    // Enhanced debug logging
    let debugStartTime = Date.now();
    let inputHistory = [];
    let errorCount = 0;
    
    function logToDebug(message, type = 'info') {
      if (window.debugMode) {
        const timestamp = new Date().toISOString();
        console.log(`[Debug][${type}][${timestamp}] ${message}`);
        
        // Update debug panel
        document.getElementById('lastAction').textContent = message;
        document.getElementById('systemStatus').textContent = `Running for ${((Date.now() - debugStartTime)/1000).toFixed(1)}s`;
        document.getElementById('performance').textContent = `Errors: ${errorCount}, Inputs: ${inputHistory.length}`;
        
        // Log to parent Streamlit
        window.parent.postMessage({
          type: 'streamlit:debug',
          message: message,
          timestamp: timestamp,
          category: type
        }, '*');
      }
    }

    // Enhanced input logging
    function logInput(field) {
      const input = document.getElementById(field);
      const timestamp = Date.now();
      const inputData = {
        field: field,
        length: input.value.length,
        timestamp: timestamp
      };
      inputHistory.push(inputData);
      
      logToDebug(`${field} changed: ${input.value.length} characters`, 'input');
      document.getElementById('inputStatus').textContent = 
        `${field} updated (${inputHistory.length} total inputs)`;
    }

    // Enhanced login handler
    function handleLogin() {
      const startTime = performance.now();
      const username = document.getElementById('username').value;
      const password = document.getElementById('password').value;
      
      try {
        logToDebug(`Login attempt started`, 'auth');
        
        if (!username || !password) {
          errorCount++;
          throw new Error('Empty fields');
        }
        
        // Simulate network delay
        setTimeout(() => {
          const endTime = performance.now();
          logToDebug(`Login attempt completed in ${(endTime-startTime).toFixed(1)}ms`, 'auth');
          alert('Simulated login. Integrate backend for real auth.');
        }, 500);
        
      } catch (error) {
        errorCount++;
        logToDebug(`Login error: ${error.message}`, 'error');
        document.getElementById('errors').textContent = error.message;
        alert('Please fill in all fields');
      }
    }

    // Enhanced particle initialization
    try {
      tsParticles.load("tsparticles", {
        background: { color: "#0f0c29" },
        fpsLimit: 60,
        particles: {
          number: {
            value: 80,
            density: {
              enable: true,
              value_area: 800
            }
          },
          color: {
            value: ["#00f0ff", "#ff00e0", "#00ff00"],
            animation: {
              enable: true,
              speed: 20,
              sync: false
            }
          },
          shape: {
            type: ["circle", "triangle", "star"],
            options: {
              star: {
                sides: 5
              }
            }
          },
          opacity: {
            value: 0.5,
            random: true,
            animation: {
              enable: true,
              speed: 3,
              minimumValue: 0.1,
              sync: false
            }
          },
          size: {
            value: 3,
            random: true,
            animation: {
              enable: true,
              speed: 2,
              minimumValue: 0.5,
              sync: false
            }
          },
          links: {
            enable: true,
            distance: 150,
            color: "#00f0ff",
            opacity: 0.4,
            width: 1,
            triangles: {
              enable: true,
              opacity: 0.1
            }
          },
          move: {
            enable: true,
            speed: 2,
            direction: "none",
            random: true,
            straight: false,
            outModes: {
              default: "bounce",
              bottom: "bounce",
              left: "bounce",
              right: "bounce",
              top: "bounce"
            },
            attract: {
              enable: true,
              rotateX: 600,
              rotateY: 1200
            }
          },
          life: {
            duration: {
              value: 2,
              sync: false
            },
            count: 1,
            delay: {
              random: {
                enable: true,
                minimumValue: 0.5
              }
            }
          },
          rotate: {
            random: true,
            direction: "random",
            animation: {
              enable: true,
              speed: 5,
              sync: false
            }
          },
          tilt: {
            direction: "random",
            enable: true,
            move: true,
            value: {
              min: 0,
              max: 360
            },
            animation: {
              enable: true,
              speed: 6,
              sync: false
            }
          },
          roll: {
            darken: {
              enable: true,
              value: 25
            },
            enable: true,
            speed: {
              min: 15,
              max: 25
            }
          },
          wobble: {
            distance: 30,
            enable: true,
            move: true,
            speed: {
              min: -15,
              max: 15
            }
          }
        },
        interactivity: {
          detectsOn: "window",
          events: {
            onHover: {
              enable: true,
              mode: ["grab", "bubble", "repulse"],
              parallax: {
                enable: true,
                force: 60,
                smooth: 10
              }
            },
            onClick: {
              enable: true,
              mode: ["push", "attract"]
            },
            resize: true
          },
          modes: {
            grab: {
              distance: 200,
              links: {
                opacity: 0.8
              }
            },
            bubble: {
              distance: 250,
              size: 10,
              duration: 2,
              opacity: 0.8
            },
            repulse: {
              distance: 150,
              duration: 0.4
            },
            push: {
              quantity: 4,
              groups: ["z5000", "z7500", "z2500", "z1000"]
            },
            attract: {
              distance: 200,
              duration: 0.4,
              factor: 3
            }
          }
        },
        particles: [
          {
            number: {
              value: 20,
              density: {
                enable: true,
                value_area: 800
              }
            },
            color: {
              value: "#00f0ff"
            },
            shape: {
              type: "circle"
            },
            opacity: {
              value: 0.8
            },
            size: {
              value: 3
            },
            move: {
              enable: true,
              speed: 2,
              direction: "none",
              outModes: "bounce"
            }
          },
          {
            number: {
              value: 15,
              density: {
                enable: true,
                value_area: 800
              }
            },
            color: {
              value: "#ff00e0"
            },
            shape: {
              type: "star"
            },
            opacity: {
              value: 0.7
            },
            size: {
              value: 4
            },
            move: {
              enable: true,
              speed: 1.5,
              direction: "none",
              outModes: "bounce"
            }
          },
          {
            number: {
              value: 10,
              density: {
                enable: true,
                value_area: 800
              }
            },
            color: {
              value: "#00ff00"
            },
            shape: {
              type: "triangle"
            },
            opacity: {
              value: 0.6
            },
            size: {
              value: 5
            },
            move: {
              enable: true,
              speed: 3,
              direction: "none",
              outModes: "bounce"
            }
          }
        ],
        detectRetina: true,
        motion: {
          disable: false,
          reduce: {
            factor: 4,
            value: true
          }
        }
      }).then(() => {
        logToDebug('Particles initialized successfully', 'system');
      }).catch(error => {
        errorCount++;
        console.error('Particles initialization error:', error);
        logToDebug(`Particles error: ${error.message}`, 'error');
        document.getElementById('errors').textContent = `Particle Init: ${error.message}`;
      });
    } catch (error) {
      errorCount++;
      console.error('Critical error:', error);
      logToDebug(`Critical error: ${error.message}`, 'error');
      document.getElementById('errors').textContent = `Critical: ${error.message}`;
    }

    // Initialize debug mode
    window.debugMode = """ + str(st.session_state.debug_mode).lower() + """;
    if (window.debugMode) {
      document.getElementById('debugInfo').classList.add('show');
      logToDebug('Debug mode initialized', 'system');
    }
    
    // Performance monitoring
    window.addEventListener('load', () => {
      const loadTime = performance.now();
      logToDebug(`Page loaded in ${loadTime.toFixed(1)}ms`, 'performance');
    });
  </script>
</body>
</html>
""", height=600, width=800)

# Enhanced debug controls
if st.session_state.debug_mode:
    st.write("---")
    st.write("### Debug Controls")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Simulate Success"):
            log_debug_event('test', 'Simulated successful login')
            st.session_state.login_attempts += 1
            st.session_state.performance_metrics['login_attempts_timing'].append(time.time() % 1)
            st.success("Login simulation successful!")
            
    with col2:
        if st.button("Simulate Error"):
            log_debug_event('test', 'Simulated login error')
            st.session_state.last_error = "Simulated authentication error"
            st.error("Login simulation failed!")
            
    with col3:
        if st.button("Clear Errors"):
            st.session_state.last_error = None
            log_debug_event('system', 'Errors cleared')
            st.info("Error log cleared") 
