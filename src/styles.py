import base64
import os

def get_page_styling():
    return """
        <style>
    /* Main theme colors and styling */
    :root {
        --primary-color: #1E88E5;
        --secondary-color: #00ff88;
        --background-color: transparent;
        --card-bg: rgba(255, 255, 255, 0.05);
        --text-color: #ffffff;
    }
    
    .stApp {
        background: transparent;
    }
    
    /* Ensure content is above particles */
    .main .block-container {
        background: transparent !important;
    }
    
    .main {
        background-color: transparent !important;
    }
    
    /* Glassmorphism card effect */
    .glass-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 15px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
    }
    
    /* Enhanced metric card styling */
    .metric-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 15px;
        padding: 20px;
        text-align: center;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
    }
    
    .metric-value {
        font-size: 28px;
        font-weight: bold;
        background: linear-gradient(45deg, var(--primary-color), var(--secondary-color));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 8px;
    }
    
    .metric-label {
        font-size: 16px;
        color: rgba(255, 255, 255, 0.7);
        font-weight: 500;
    }
    
    /* Chart container styling */
    .chart-container {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 15px;
        padding: 20px;
        margin-bottom: 20px;
    }
    
    /* Custom header styling */
    .custom-header {
        font-size: 24px;
        font-weight: bold;
        color: var(--text-color);
        margin-bottom: 20px;
        padding-bottom: 10px;
        border-bottom: 2px solid var(--primary-color);
        text-shadow: 0 0 10px rgba(30, 136, 229, 0.5);
    }
    
    /* Sidebar styling */
    .sidebar .sidebar-content {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
    }
    
    /* Table styling */
    .dataframe {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border-radius: 10px;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .dataframe th {
        background: rgba(30, 136, 229, 0.1);
        padding: 12px;
        text-align: left;
        color: var(--primary-color);
    }
    
    .dataframe td {
        padding: 12px;
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    /* Button styling */
    .stButton>button {
        background: linear-gradient(45deg, var(--primary-color), var(--secondary-color));
        color: white;
        border-radius: 10px;
        padding: 10px 20px;
        border: none;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(30, 136, 229, 0.3);
    }
    
    /* Section headers */
    h1, h2, h3 {
        color: var(--text-color);
        font-weight: 600;
        text-shadow: 0 0 10px rgba(30, 136, 229, 0.3);
    }
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 10px;
        height: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(255, 255, 255, 0.05);
    }
    
    ::-webkit-scrollbar-thumb {
        background: var(--primary-color);
        border-radius: 5px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: var(--secondary-color);
    }
    </style>
    """

def get_particles_js():
   return """
    <canvas id="starfield"></canvas>
    <style>
    #starfield {
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        z-index: -1;
        background: #0d1117;
    }
    </style>
    <script>
    const canvas = document.getElementById('starfield');
    const ctx = canvas.getContext('2d');

    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;

    const stars = [];
    const numStars = 200;
    const centerX = canvas.width / 2;
    const centerY = canvas.height / 2;

    class Star {
        constructor() {
            this.reset();
        }

        reset() {
            this.x = Math.random() * canvas.width - centerX;
            this.y = Math.random() * canvas.height - centerY;
            this.z = Math.random() * canvas.width;
        }

        update() {
            this.z -= 10;
            if (this.z <= 0) this.reset();
        }

        draw() {
            const x = (this.x / this.z) * canvas.width + centerX;
            const y = (this.y / this.z) * canvas.height + centerY;
            const size = (1 - this.z / canvas.width) * 3;

            ctx.beginPath();
            ctx.arc(x, y, size, 0, Math.PI * 2);
            ctx.fillStyle = '#1E88E5';
            ctx.fill();
        }
    }

    for (let i = 0; i < numStars; i++) {
        stars.push(new Star());
    }

    function animate() {
        ctx.fillStyle = 'rgba(13, 17, 23, 0.2)';
        ctx.fillRect(0, 0, canvas.width, canvas.height);

        stars.forEach(star => {
            star.update();
            star.draw();
        });

        requestAnimationFrame(animate);
    }

    animate();
    </script>
    """

# read gif file
def read_gif(file_name):
    with open(os.path.join(os.getcwd(),file_name),'rb') as f:
        contents=f.read()
        data_url=base64.b64encode(contents).decode('utf-8')
    return data_url

# create variables for gif files
BMW_GIF = read_gif('assets/giphy.webp')

URLS= {
    "BMW": f"data:image/gif;base64,{BMW_GIF}"
}