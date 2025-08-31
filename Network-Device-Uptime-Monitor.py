import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
import time
import subprocess
import platform
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import queue
import sys

class NetworkDeviceUptimeMonitor:
    def __init__(self, root):
        self.root = root
        self.root.title("Network Device Uptime Monitor")
        self.root.geometry("600x650")
        self.root.configure(bg='#f0f0f0')
        
        # Configuration variables
        self.ping_interval = 3  # seconds
        self.notification_threshold = 10  # seconds
        
        # Email configuration (modify these)
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587
        self.email_username = "your_email@gmail.com"  # Change this
        self.email_password = "your_app_password"     # Change this (use app password for Gmail)
        
        # Monitoring state
        self.monitoring = False
        self.monitor_thread = None
        self.device_states = {}  # {ip: {'mac': mac, 'last_seen': timestamp, 'notified': bool}}
        self.log_queue = queue.Queue()
        
        self.setup_ui()
        self.update_log_display()
        
    def setup_ui(self):
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="🌐 Network Device Uptime Monitor", 
                               font=('Arial', 14, 'bold'))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 15))
        
        # IP Addresses section
        ip_label = ttk.Label(main_frame, text="IP Addresses", font=('Arial', 10, 'bold'))
        ip_label.grid(row=1, column=0, sticky=tk.W, pady=(0, 5))
        
        self.ip_text = tk.Text(main_frame, width=25, height=8, font=('Consolas', 9))
        self.ip_text.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 5))
        
        # MAC Addresses section
        mac_label = ttk.Label(main_frame, text="MAC Addresses", font=('Arial', 10, 'bold'))
        mac_label.grid(row=1, column=1, sticky=tk.W, pady=(0, 5))
        
        self.mac_text = tk.Text(main_frame, width=25, height=8, font=('Consolas', 9))
        self.mac_text.grid(row=2, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(5, 0))
        
        # Control buttons frame
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=3, column=0, columnspan=2, pady=15)
        
        self.start_btn = ttk.Button(button_frame, text="Start Monitoring", 
                                   command=self.start_monitoring)
        self.start_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.stop_btn = ttk.Button(button_frame, text="Stop Monitoring", 
                                  command=self.stop_monitoring, state=tk.DISABLED)
        self.stop_btn.pack(side=tk.LEFT)
        
        # Configuration frame
        config_frame = ttk.LabelFrame(main_frame, text="Configuration", padding="10")
        config_frame.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)
        config_frame.columnconfigure(1, weight=1)
        config_frame.columnconfigure(3, weight=1)
        
        ttk.Label(config_frame, text="Ping Interval (s):").grid(row=0, column=0, sticky=tk.W)
        self.ping_interval_var = tk.StringVar(value=str(self.ping_interval))
        ttk.Entry(config_frame, textvariable=self.ping_interval_var, width=10).grid(row=0, column=1, sticky=tk.W, padx=(5, 20))
        
        ttk.Label(config_frame, text="Notification Threshold (s):").grid(row=0, column=2, sticky=tk.W)
        self.threshold_var = tk.StringVar(value=str(self.notification_threshold))
        ttk.Entry(config_frame, textvariable=self.threshold_var, width=10).grid(row=0, column=3, sticky=tk.W, padx=(5, 0))
        
        # Email configuration frame
        email_frame = ttk.LabelFrame(main_frame, text="Email Notification", padding="10")
        email_frame.grid(row=5, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)
        email_frame.columnconfigure(1, weight=1)
        
        ttk.Label(email_frame, text="Subject:").grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        self.email_subject = tk.StringVar(value="Device Unresponsive Alert")
        ttk.Entry(email_frame, textvariable=self.email_subject, width=50).grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(5, 0), pady=(0, 5))
        
        ttk.Label(email_frame, text="Recipients (comma-separated):").grid(row=1, column=0, sticky=tk.W, pady=(0, 5))
        self.email_recipients = tk.StringVar(value="admin@example.com")
        ttk.Entry(email_frame, textvariable=self.email_recipients, width=50).grid(row=1, column=1, sticky=(tk.W, tk.E), padx=(5, 0), pady=(0, 5))
        
        ttk.Label(email_frame, text="Email Body:").grid(row=2, column=0, sticky=(tk.W, tk.N), pady=(0, 5))
        self.email_body = tk.Text(email_frame, width=50, height=4, font=('Arial', 9))
        self.email_body.insert('1.0', "Device with MAC {MacAddress} and IP {IpAddress} has become unresponsive for more than 10 seconds at {Time}.")
        self.email_body.grid(row=2, column=1, sticky=(tk.W, tk.E), padx=(5, 0), pady=(0, 5))
        
        # Log output
        log_label = ttk.Label(main_frame, text="Log Output", font=('Arial', 10, 'bold'))
        log_label.grid(row=6, column=0, columnspan=2, sticky=tk.W, pady=(10, 5))
        
        self.log_text = scrolledtext.ScrolledText(main_frame, width=70, height=12, font=('Consolas', 8))
        self.log_text.grid(row=7, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        # Configure grid weights for resizing
        main_frame.rowconfigure(2, weight=1)
        main_frame.rowconfigure(7, weight=2)
        
        # Copyright attribution
        copyright_frame = ttk.Frame(main_frame)
        copyright_frame.grid(row=8, column=0, columnspan=2, pady=(10, 0))
        
        copyright_label = ttk.Label(copyright_frame, text="© Oleksiy Gorbenko | ProfitsPlusX.com", 
                                   font=('Arial', 8), foreground='gray')
        copyright_label.pack()
    
    def log(self, message):
        """Add message to log queue for thread-safe logging"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.log_queue.put(f"[{timestamp}] {message}")
    
    def update_log_display(self):
        """Update log display from queue"""
        try:
            while True:
                message = self.log_queue.get_nowait()
                self.log_text.insert(tk.END, message + "\n")
                self.log_text.see(tk.END)
        except queue.Empty:
            pass
        
        # Schedule next update
        self.root.after(100, self.update_log_display)
    
    def ping_host(self, ip):
        """Ping a host and return True if reachable"""
        try:
            # Determine ping command based on OS
            if platform.system().lower() == "windows":
                cmd = ["ping", "-n", "1", "-w", "1000", ip]
            else:
                cmd = ["ping", "-c", "1", "-W", "1", ip]
            
            result = subprocess.run(cmd, capture_output=True, timeout=3)
            return result.returncode == 0
        except Exception as e:
            self.log(f"Error pinging {ip}: {str(e)}")
            return False
    
    def send_email_notification(self, ip, mac):
        """Send email notification for unresponsive device"""
        try:
            recipients = [email.strip() for email in self.email_recipients.get().split(',')]
            if not recipients or recipients == ['']:
                self.log("No recipients specified for email notification")
                return
            
            subject = self.email_subject.get()
            body = self.email_body.get('1.0', tk.END).strip()
            
            # Replace placeholders
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            body = body.replace("{IpAddress}", ip)
            body = body.replace("{MacAddress}", mac)
            body = body.replace("{Time}", current_time)
            
            # Create email
            msg = MIMEMultipart()
            msg['From'] = self.email_username
            msg['To'] = ', '.join(recipients)
            msg['Subject'] = subject
            msg.attach(MIMEText(body, 'plain'))
            
            # Send email
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.email_username, self.email_password)
            server.send_message(msg)
            server.quit()
            
            self.log(f"Email notification sent for {ip} ({mac})")
            
        except Exception as e:
            self.log(f"Failed to send email notification: {str(e)}")
    
    def monitor_devices(self):
        """Main monitoring loop"""
        self.log("Starting device monitoring...")
        
        # Parse IP and MAC addresses
        ip_lines = [line.strip() for line in self.ip_text.get('1.0', tk.END).strip().split('\n') if line.strip()]
        mac_lines = [line.strip() for line in self.mac_text.get('1.0', tk.END).strip().split('\n') if line.strip()]
        
        # Initialize device states
        self.device_states = {}
        for i, ip in enumerate(ip_lines):
            mac = mac_lines[i] if i < len(mac_lines) else "Unknown"
            self.device_states[ip] = {
                'mac': mac,
                'last_seen': time.time(),
                'notified': False
            }
        
        self.log(f"Monitoring {len(self.device_states)} devices")
        
        while self.monitoring:
            try:
                # Update configuration
                self.ping_interval = int(self.ping_interval_var.get())
                self.notification_threshold = int(self.threshold_var.get())
                
                current_time = time.time()
                
                for ip, state in self.device_states.items():
                    if not self.monitoring:
                        break
                    
                    # Ping device
                    if self.ping_host(ip):
                        # Device is responsive
                        if current_time - state['last_seen'] > self.notification_threshold:
                            self.log(f"Device {ip} ({state['mac']}) is back online")
                        state['last_seen'] = current_time
                        state['notified'] = False
                    else:
                        # Device is not responsive
                        down_time = current_time - state['last_seen']
                        if down_time > self.notification_threshold and not state['notified']:
                            # Send notification
                            self.log(f"Device {ip} ({state['mac']}) unresponsive for {down_time:.1f}s - sending notification")
                            threading.Thread(target=self.send_email_notification, 
                                           args=(ip, state['mac']), daemon=True).start()
                            state['notified'] = True
                        elif down_time <= self.notification_threshold:
                            self.log(f"Device {ip} ({state['mac']}) not responding ({down_time:.1f}s)")
                
                # Wait for next ping interval
                time.sleep(self.ping_interval)
                
            except ValueError:
                self.log("Invalid configuration values - using defaults")
                self.ping_interval = 3
                self.notification_threshold = 10
                time.sleep(1)
            except Exception as e:
                self.log(f"Error in monitoring loop: {str(e)}")
                time.sleep(1)
        
        self.log("Monitoring stopped")
    
    def start_monitoring(self):
        """Start monitoring devices"""
        if not self.ip_text.get('1.0', tk.END).strip():
            messagebox.showerror("Error", "Please enter at least one IP address")
            return
        
        # Validate email configuration
        if not self.email_username or self.email_username == "your_email@gmail.com":
            messagebox.showwarning("Warning", 
                                 "Email credentials not configured. Please update the email_username and email_password in the code.")
        
        self.monitoring = True
        self.monitor_thread = threading.Thread(target=self.monitor_devices, daemon=True)
        self.monitor_thread.start()
        
        self.start_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.NORMAL)
    
    def stop_monitoring(self):
        """Stop monitoring devices"""
        self.monitoring = False
        if self.monitor_thread and self.monitor_thread.is_alive():
            self.monitor_thread.join(timeout=2)
        
        self.start_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)
    
    def on_closing(self):
        """Handle application closing"""
        self.stop_monitoring()
        self.root.destroy()

def main():
    root = tk.Tk()
    app = NetworkDeviceUptimeMonitor(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()

if __name__ == "__main__":
    main()