import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import subprocess
import webbrowser

def get_existing_tunnels():
    try:
        result = subprocess.run(['wg', 'show'], capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError:
        return "No existing tunnels found."

def check_existing_tunnels():
    try:
        result = subprocess.run(['wg', 'show'], capture_output=True, text=True, check=True)
        if result.stdout:
            return True
        return False
    except subprocess.CalledProcessError:
        return False

def create_tunnel():
    if check_existing_tunnels():
        messagebox.showinfo("Info", "Tunnel already exists.")
        return
    
    config_path = filedialog.askopenfilename(title="Select WireGuard Config", filetypes=[("WireGuard Config", "*.conf")])
    if config_path:
        try:
            result = subprocess.run(['wireguard', '/installtunnelservice', config_path], capture_output=True, text=True, check=True)
            messagebox.showinfo("Success", "Tunnel created successfully.")
            show_tunnel_details(config_path)
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"Failed to create tunnel:\n{e.stderr}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

def start_tunnel():
    if not check_existing_tunnels():
        messagebox.showerror("Error", "No tunnel exists to start. Please create a tunnel first.")
        return
    
    try:
        result = subprocess.run(['net', 'start', 'wg-quick@wg0'], capture_output=True, text=True, check=True)
        messagebox.showinfo("Success", "Tunnel started successfully.")
        show_tunnel_details('wg0.conf')
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error", f"Failed to start tunnel:\n{e.stderr}")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def stop_tunnel():
    try:
       
        subprocess.run(['wireguard', '/uninstalltunnelservice', 'wg0'], capture_output=True, text=True, check=True)
        messagebox.showinfo("Success", "Tunnel stopped successfully.")
        details_text.config(state=tk.NORMAL)
        details_text.delete(1.0, tk.END)
        details_text.config(state=tk.DISABLED)
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error", f"Failed to stop tunnel:\n{e.stderr}")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def show_tunnel_details(config_path):
    with open(config_path, 'r') as file:
        config_content = file.read()
    details_text.config(state=tk.NORMAL)
    details_text.delete(1.0, tk.END)
    details_text.insert(tk.END, config_content)
    details_text.config(state=tk.DISABLED)

def browse_url():
    webbrowser.open("https://ttlabs.me")

def on_close():
    stop_tunnel()
    root.destroy()

# Create main window
root = tk.Tk()
root.title("WireGuard Tunnel Manager")
root.geometry("600x400")
root.protocol("WM_DELETE_WINDOW", on_close)

# Show existing tunnels
existing_tunnels = get_existing_tunnels()
details_text = scrolledtext.ScrolledText(root, width=70, height=10, state=tk.DISABLED)
details_text.pack(pady=10)
details_text.insert(tk.END, existing_tunnels)

# Create and place buttons
create_button = tk.Button(root, text="Create Tunnel", command=create_tunnel)
create_button.pack(pady=10)

start_button = tk.Button(root, text="Start Tunnel", command=start_tunnel)
start_button.pack(pady=10)

stop_button = tk.Button(root, text="Stop Tunnel", command=stop_tunnel)
stop_button.pack(pady=10)

browse_button = tk.Button(root, text="Browse URL", command=browse_url)
browse_button.pack(pady=10)

# Start the GUI event loop
root.mainloop()