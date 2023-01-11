# Importing the required libraries
import tkinter as tk
from tkinter import Label, Entry, Button, Checkbutton, OptionMenu, StringVar, messagebox
import socket
import psutil
import threading

# Create the main window
root = tk.Tk()
root.title("Network Monitor")
root.geometry("400x400")

# Create the labels
lbl_host = Label(root, text="Host IP:").grid(row=0, column=0)
lbl_port = Label(root, text="Port:").grid(row=1, column=0)
lbl_alert_threshold = Label(root, text="Alert Threshold:").grid(row=2, column=0)

# Create the Entry boxes
ent_host = Entry(root)
ent_host.grid(row=0, column=1)
ent_port = Entry(root)
ent_port.grid(row=1, column=1)
ent_alert_threshold = Entry(root)
ent_alert_threshold.grid(row=2, column=1)

# Create the Checkbutton
var1 = tk.IntVar()
chk_conn = Checkbutton(root, text="Monitor Connections", variable=var1).grid(row=3, column=0)

# Create the Options Menu
var2 = StringVar()
var2.set("TCP")
opt_menu = OptionMenu(root, var2, "TCP", "UDP").grid(row=3, column=1)

# Create the monitor and alert Button
def monitor_alert():
    host_ip = ent_host.get()
    port_num = int(ent_port.get())
    threshold = int(ent_alert_threshold.get())
    protocol = var2.get()
    
    # Check if all the inputs are filled
    if host_ip and port_num and threshold:
        # Start the monitoring thread
        monitor_thread = threading.Thread(target=monitor_connections,args=(host_ip, port_num, threshold, protocol,))
        monitor_thread.start()
        
        # Disable the start button
        btn_start.config(state="disabled")
        messagebox.showinfo("Success","Monitoring Started")

btn_start = Button(root, text="Start Monitor & Alert", command=monitor_alert).grid(row=4, column=0)

# Create the stop Button
def stop_monitor():
    # Stop the monitoring thread
    
    btn_start.config(state="normal")
    messagebox.showinfo("Success","Monitoring Stopped")

btn_stop = Button(root, text="Stop Monitor", command=stop_monitor).grid(row=4, column=1)

# Function to monitor network connections
def monitor_connections(host_ip, port_num, threshold, protocol):
    count = 0
    while True:
        # Get the active connection details
        conn_details = psutil.net_connections(kind=protocol)
        
        # Check if the host and port matches in any connection
        for conn in conn_details:
            if conn.laddr[0] == host_ip and conn.laddr[1] == port_num:
                count += 1
        
        # Check if the count exceeds the threshold
        if count > threshold:
            messagebox.showwarning("Alert","Suspicious activity detected")
            break

# Start the main loop
root.mainloop()