import time
import customtkinter as ctk

# Configure CustomTkinter window theme and colors
ctk.set_appearance_mode("dark")  # Sleek dark mode perfect for a cyber tool
ctk.set_default_color_theme("blue")


class IOSLockscreenSim(ctk.CTk):
    def __init__(self):
        super().__init__()

        # --- SECURITY DATA ---
        self.correct_pin = "4982"
        self.max_attempts = 10
        self.failed_attempts = 0
        self.locked_until = 0.0

        # Lockout cooling schedule (attempts: delay in seconds)
        self.lockout_schedule = {
            3: 5,  # 3rd failure = 5s lock
            5: 15,  # 5th failure = 15s lock
            7: 30,  # 7th failure = 30s lock
            10: 60  # 10th failure = 60s lock
        }

        # --- GUI SETUP ---
        self.title("INSA Security Lab: Lockscreen Simulator")
        self.geometry("380x620")
        self.resizable(False, False)

        # Phone Container Frame
        self.phone_frame = ctk.CTkFrame(self, width=350, height=580, corner_radius=25)
        self.phone_frame.pack(pady=20, padx=15)

        # 1. Screen Title / Status Display
        self.status_label = ctk.CTkLabel(
            self.phone_frame,
            text="ENTER PASSCODE",
            font=("Helvetica", 18, "bold"),
            text_color="#FFFFFF"
        )
        self.status_label.pack(pady=(40, 5))

        self.sub_status_label = ctk.CTkLabel(
            self.phone_frame,
            text="Device Secured by StrongBox Rate-Limiting",
            font=("Helvetica", 11),
            text_color="#888888"
        )
        self.sub_status_label.pack(pady=(0, 15))

        # 2. PIN Dots Display (simulating hidden input dots)
        self.pin_display_var = ctk.StringVar(value="")
        self.dots_label = ctk.CTkLabel(
            self.phone_frame,
            textvariable=self.pin_display_var,
            font=("Helvetica", 28, "bold"),
            text_color="#3B8ED0"
        )
        self.dots_label.pack(pady=10)

        # 3. Numeric Grid Frame
        self.grid_frame = ctk.CTkFrame(self.phone_frame, fg_color="transparent")
        self.grid_frame.pack(pady=25)

        # Define keypad layout
        keys = [
            '1', '2', '3',
            '4', '5', '6',
            '7', '8', '9',
            'Clear', '0', 'OK'
        ]

        # Dynamically generate keypad buttons
        row = 0
        col = 0
        for key in keys:
            # Custom styling for utility buttons
            if key in ["Clear", "OK"]:
                btn_color = "#2b2b2b"
                hover_color = "#3a3a3a"
                text_color = "#3B8ED0"
            else:
                btn_color = "#1f1f1f"
                hover_color = "#2a2a2a"
                text_color = "#FFFFFF"

            btn = ctk.CTkButton(
                self.grid_frame,
                text=key,
                width=80,
                height=80,
                corner_radius=40,  # Makes buttons perfectly circular
                fg_color=btn_color,
                hover_color=hover_color,
                text_color=text_color,
                font=("Helvetica", 18, "bold"),
                command=lambda k=key: self.keypad_press(k)
            )
            btn.grid(row=row, column=col, padx=10, pady=10)

            col += 1
            if col > 2:
                col = 0
                row += 1

        # 4. Security Log Terminal at Bottom
        self.log_box = ctk.CTkTextbox(self.phone_frame, width=300, height=80, font=("Courier", 11))
        self.log_box.pack(pady=(10, 20))
        self.log_box.insert("0.0", "System initialized. Waiting for input...\n")
        self.log_box.configure(state="disabled")

        # Keep checking the security clock for rate limiting delays
        self.check_lockout_loop()

    # --- ACTION HANDLERS ---
    def log_message(self, message):
        """Helper to output messages to the simulated system terminal"""
        self.log_box.configure(state="normal")
        self.log_box.insert("end", f"> {message}\n")
        self.log_box.see("end")
        self.log_box.configure(state="disabled")

    def keypad_press(self, key):
        # Check security gate first
        current_time = time.time()
        if current_time < self.locked_until:
            wait_remaining = int(self.locked_until - current_time)
            self.log_message(f"BLOCKED: Lockout active ({wait_remaining}s left).")
            return

        current_pin = self.pin_display_var.get()

        if key == "Clear":
            self.pin_display_var.set("")
        elif key == "OK":
            if current_pin:
                self.process_submission(current_pin)
        else:
            # Mask characters visually with '*'
            if len(current_pin) < 4:
                self.pin_display_var.set(current_pin + key)

    def process_submission(self, entered_pin):
        self.pin_display_var.set("")  # Clear input box immediately

        if entered_pin == self.correct_pin:
            self.failed_attempts = 0
            self.status_label.configure(text="ACCESS GRANTED", text_color="#2ecc71")
            self.log_message("Success! Device unlocked.")
        else:
            self.failed_attempts += 1
            self.status_label.configure(text="WRONG PASSCODE", text_color="#e74c3c")
            self.log_message(f"Invalid PIN try. (Fails: {self.failed_attempts})")

            # Check if we should trigger a lockout delay
            if self.failed_attempts in self.lockout_schedule:
                delay = self.lockout_schedule[self.failed_attempts]
                self.locked_until = time.time() + delay
                self.log_message(f"RATE LIMIT TRIGGERED: {delay}s cooldown.")

    def check_lockout_loop(self):
        """Runs continuously in background to update countdown timer UI"""
        current_time = time.time()
        if current_time < self.locked_until:
            wait_remaining = int(self.locked_until - current_time)
            self.status_label.configure(text=f"TRY AGAIN IN {wait_remaining}s", text_color="#e67e22")
        elif self.status_label.cget("text").startswith("TRY AGAIN"):
            self.status_label.configure(text="ENTER PASSCODE", text_color="#FFFFFF")

        # Loop every 100 milliseconds
        self.after(100, self.check_lockout_loop)


if __name__ == "__main__":
    app = IOSLockscreenSim()
    app.mainloop() 