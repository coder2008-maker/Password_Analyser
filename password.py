import tkinter as tk
import string


# ============================================================
# SAMPLE COMMON PASSWORDS
# These are only used for educational testing.
# ============================================================

COMMON_PASSWORDS = {
    "password",
    "password123",
    "123456",
    "12345678",
    "qwerty",
    "qwerty123",
    "admin",
    "welcome",
    "abc123",
    "letmein",
    "iloveyou"
}


# ============================================================
# SAMPLE TEST CASES
# Each case demonstrates a different security condition.
# ============================================================

TEST_CASES = [
    ("123456", "Very weak/common password"),
    ("password123", "Common password + predictable pattern"),
    ("hello123", "Short password + predictable pattern"),
    ("HelloWorld", "Letters only / low character diversity"),
    ("HelloWorld123", "Longer password with mixed characters"),
    ("T7!qR9@vL2#xP8", "Stronger and less predictable password")
]


# ============================================================
# PASSWORD CHECKING FUNCTIONS
# ============================================================

def has_sequence(password):
    """
    Checks for simple sequences such as:
    123, 456, abc, xyz
    """

    password = password.lower()

    for i in range(len(password) - 2):

        a = ord(password[i])
        b = ord(password[i + 1])
        c = ord(password[i + 2])

        if b == a + 1 and c == b + 1:
            return True

        if b == a - 1 and c == b - 1:
            return True

    return False


def has_repeated_characters(password):
    """
    Checks for patterns such as:
    aaa, 111, !!!
    """

    for i in range(len(password) - 2):

        if (
            password[i]
            == password[i + 1]
            == password[i + 2]
        ):
            return True

    return False


def analyze_password(password):

    score = 0
    risks = []
    recommendations = []

    # --------------------------------------------------------
    # 1. LENGTH
    # --------------------------------------------------------

    if len(password) >= 12:
        score += 2

    elif len(password) >= 8:
        score += 1

    else:
        risks.append("Password is too short.")
        recommendations.append(
            "Use at least 12 characters when possible."
        )


    # --------------------------------------------------------
    # 2. CHARACTER DIVERSITY
    # --------------------------------------------------------

    lowercase = any(
        c in string.ascii_lowercase
        for c in password
    )

    uppercase = any(
        c in string.ascii_uppercase
        for c in password
    )

    numbers = any(
        c in string.digits
        for c in password
    )

    symbols = any(
        c in string.punctuation
        for c in password
    )

    character_types = sum([
        lowercase,
        uppercase,
        numbers,
        symbols
    ])


    if character_types >= 4:
        score += 2

    elif character_types >= 3:
        score += 1

    else:
        risks.append(
            "Password has low character diversity."
        )

        recommendations.append(
            "Use a mix of uppercase, lowercase, numbers and symbols."
        )


    # --------------------------------------------------------
    # 3. COMMON PASSWORD CHECK
    # --------------------------------------------------------

    if password.lower() in COMMON_PASSWORDS:

        score -= 3

        risks.append(
            "Password is commonly used."
        )

        recommendations.append(
            "Avoid commonly used passwords."
        )


    # --------------------------------------------------------
    # 4. SEQUENCE CHECK
    # --------------------------------------------------------

    if has_sequence(password):

        score -= 1

        risks.append(
            "Password contains a predictable sequence."
        )

        recommendations.append(
            "Avoid sequences such as 1234 or ABCD."
        )


    # --------------------------------------------------------
    # 5. REPEATED CHARACTER CHECK
    # --------------------------------------------------------

    if has_repeated_characters(password):

        score -= 1

        risks.append(
            "Password contains repeated characters."
        )

        recommendations.append(
            "Avoid repeated patterns such as AAA or 111."
        )


    # --------------------------------------------------------
    # FINAL STRENGTH
    # --------------------------------------------------------

    if score <= 1:

        strength = "VERY WEAK"
        risk = "HIGH"

    elif score <= 3:

        strength = "WEAK"
        risk = "HIGH"

    elif score <= 5:

        strength = "MODERATE"
        risk = "MEDIUM"

    else:

        strength = "STRONG"
        risk = "LOW"


    return {
        "score": score,
        "strength": strength,
        "risk": risk,
        "character_types": character_types,
        "risks": risks,
        "recommendations": recommendations
    }


# ============================================================
# GUI APPLICATION
# ============================================================

class PasswordAnalyzer:

    def __init__(self, root):

        self.root = root

        self.root.title(
            "Password Security Analyzer"
        )

        self.root.geometry(
            "850x650"
        )

        self.root.configure(
            bg="#0b0f14"
        )

        self.create_gui()


    # ========================================================
    # CREATE GUI
    # ========================================================

    def create_gui(self):

        # ----------------------------------------------------
        # TITLE
        # ----------------------------------------------------

        title = tk.Label(
            self.root,
            text="🔐 PASSWORD SECURITY ANALYZER",
            font=("Segoe UI", 22, "bold"),
            fg="#00e5ff",
            bg="#0b0f14"
        )

        title.pack(
            pady=(25, 5)
        )


        subtitle = tk.Label(
            self.root,
            text="Cybersecurity password risk assessment tool",
            font=("Segoe UI", 10),
            fg="#8b9aaa",
            bg="#0b0f14"
        )

        subtitle.pack(
            pady=(0, 20)
        )


        # ----------------------------------------------------
        # PASSWORD INPUT
        # ----------------------------------------------------

        input_frame = tk.Frame(
            self.root,
            bg="#111820"
        )

        input_frame.pack(
            padx=40,
            fill="x",
            pady=5
        )


        tk.Label(
            input_frame,
            text="ENTER SAMPLE PASSWORD",
            font=("Segoe UI", 9, "bold"),
            fg="#8b9aaa",
            bg="#111820"
        ).pack(
            anchor="w",
            padx=20,
            pady=(15, 5)
        )


        self.password_entry = tk.Entry(
            input_frame,
            font=("Consolas", 14),
            show="•",
            bg="#0d1319",
            fg="white",
            insertbackground="#00e5ff",
            relief="flat"
        )

        self.password_entry.pack(
            side="left",
            fill="x",
            expand=True,
            padx=(20, 10),
            pady=(0, 15),
            ipady=8
        )


        self.show_button = tk.Button(
            input_frame,
            text="SHOW",
            command=self.toggle_password,
            bg="#18232e",
            fg="white",
            relief="flat",
            width=8
        )

        self.show_button.pack(
            side="right",
            padx=(0, 20),
            pady=(0, 15),
            ipady=6
        )


        # ----------------------------------------------------
        # BUTTONS
        # ----------------------------------------------------

        button_frame = tk.Frame(
            self.root,
            bg="#0b0f14"
        )

        button_frame.pack(
            pady=15
        )


        tk.Button(
            button_frame,
            text="⚡ ANALYZE",
            command=self.analyze,
            bg="#00e5ff",
            fg="#001014",
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            width=15
        ).grid(
            row=0,
            column=0,
            padx=5
        )


        tk.Button(
            button_frame,
            text="🧪 TEST CASES",
            command=self.show_test_cases,
            bg="#18232e",
            fg="white",
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            width=15
        ).grid(
            row=0,
            column=1,
            padx=5
        )


        tk.Button(
            button_frame,
            text="✕ CLEAR",
            command=self.clear,
            bg="#18232e",
            fg="white",
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            width=15
        ).grid(
            row=0,
            column=2,
            padx=5
        )


        # ----------------------------------------------------
        # RESULT
        # ----------------------------------------------------

        self.result_label = tk.Label(
            self.root,
            text="STRENGTH: --",
            font=("Segoe UI", 18, "bold"),
            fg="#8b9aaa",
            bg="#0b0f14"
        )

        self.result_label.pack(
            pady=5
        )


        self.risk_label = tk.Label(
            self.root,
            text="RISK: --",
            font=("Segoe UI", 11, "bold"),
            fg="#8b9aaa",
            bg="#0b0f14"
        )

        self.risk_label.pack()


        self.score_label = tk.Label(
            self.root,
            text="SECURITY SCORE: --",
            font=("Segoe UI", 10),
            fg="#8b9aaa",
            bg="#0b0f14"
        )

        self.score_label.pack(
            pady=5
        )


        # ----------------------------------------------------
        # REPORT BOX
        # ----------------------------------------------------

        report_frame = tk.Frame(
            self.root,
            bg="#111820"
        )

        report_frame.pack(
            fill="both",
            expand=True,
            padx=40,
            pady=10
        )


        self.report = tk.Text(
            report_frame,
            font=("Consolas", 10),
            bg="#0d1319",
            fg="#e6edf3",
            insertbackground="#00e5ff",
            relief="flat",
            wrap="word"
        )

        self.report.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )


        # ----------------------------------------------------
        # PRIVACY NOTICE
        # ----------------------------------------------------

        tk.Label(
            self.root,
            text="⚠ SAMPLE PASSWORDS ONLY • Passwords are not stored",
            font=("Segoe UI", 9, "bold"),
            fg="#ffd740",
            bg="#0b0f14"
        ).pack(
            pady=(5, 15)
        )


    # ========================================================
    # SHOW / HIDE PASSWORD
    # ========================================================

    def toggle_password(self):

        if self.password_entry.cget("show") == "":

            self.password_entry.config(
                show="•"
            )

            self.show_button.config(
                text="SHOW"
            )

        else:

            self.password_entry.config(
                show=""
            )

            self.show_button.config(
                text="HIDE"
            )


    # ========================================================
    # ANALYZE BUTTON
    # ========================================================

    def analyze(self):

        password = self.password_entry.get()

        if not password:

            self.display_message(
                "Please enter a sample password."
            )

            return


        result = analyze_password(
            password
        )

        self.display_result(
            result
        )

        # Delete password after analysis.
        self.password_entry.delete(
            0,
            tk.END
        )


    # ========================================================
    # DISPLAY RESULT
    # ========================================================

    def display_result(self, result):

        strength = result["strength"]
        risk = result["risk"]


        if strength == "STRONG":

            strength_color = "#00e676"

        elif strength == "MODERATE":

            strength_color = "#ffd740"

        else:

            strength_color = "#ff5252"


        if risk == "LOW":

            risk_color = "#00e676"

        elif risk == "MEDIUM":

            risk_color = "#ffd740"

        else:

            risk_color = "#ff5252"


        self.result_label.config(
            text=f"STRENGTH: {strength}",
            fg=strength_color
        )


        self.risk_label.config(
            text=f"RISK: {risk}",
            fg=risk_color
        )


        self.score_label.config(
            text=f"SECURITY SCORE: {result['score']}"
        )


        self.report.delete(
            "1.0",
            tk.END
        )


        # ----------------------------------------------------
        # RISKS
        # ----------------------------------------------------

        self.report.insert(
            tk.END,
            "🔎 RISKS DETECTED\n"
        )

        self.report.insert(
            tk.END,
            "-" * 55 + "\n\n"
        )


        if result["risks"]:

            for risk_item in result["risks"]:

                self.report.insert(
                    tk.END,
                    f"[!] {risk_item}\n"
                )

        else:

            self.report.insert(
                tk.END,
                "[+] No major risks detected.\n"
            )


        # ----------------------------------------------------
        # RECOMMENDATIONS
        # ----------------------------------------------------

        self.report.insert(
            tk.END,
            "\n💡 RECOMMENDATIONS\n"
        )

        self.report.insert(
            tk.END,
            "-" * 55 + "\n\n"
        )


        if result["recommendations"]:

            unique_recommendations = list(
                dict.fromkeys(
                    result["recommendations"]
                )
            )

            for recommendation in unique_recommendations:

                self.report.insert(
                    tk.END,
                    f"[+] {recommendation}\n"
                )

        else:

            self.report.insert(
                tk.END,
                "[+] No major improvements required.\n"
            )


        # ----------------------------------------------------
        # BASIC ANALYSIS
        # ----------------------------------------------------

        self.report.insert(
            tk.END,
            "\n📊 ANALYSIS\n"
        )

        self.report.insert(
            tk.END,
            "-" * 55 + "\n\n"
        )

        self.report.insert(
            tk.END,
            f"Character types detected: "
            f"{result['character_types']}/4\n"
        )

        self.report.insert(
            tk.END,
            "Character types: lowercase / uppercase / "
            "numbers / symbols\n"
        )


        self.report.insert(
            tk.END,
            "\nThis is a heuristic security assessment, "
            "not a guarantee of password safety.\n"
        )


    # ========================================================
    # TEST CASES
    # ========================================================

    def show_test_cases(self):

        self.password_entry.delete(
            0,
            tk.END
        )


        self.report.delete(
            "1.0",
            tk.END
        )


        self.result_label.config(
            text="STRENGTH: TEST MODE",
            fg="#00e5ff"
        )

        self.risk_label.config(
            text="RISK: --"
        )

        self.score_label.config(
            text="SECURITY SCORE: --"
        )


        self.report.insert(
            tk.END,
            "🧪 TEST CASES\n"
        )

        self.report.insert(
            tk.END,
            "=" * 65 + "\n\n"
        )

        self.report.insert(
            tk.END,
            "Each case demonstrates a different "
            "password-security condition.\n\n"
        )


        for number, (password, purpose) in enumerate(
            TEST_CASES,
            start=1
        ):

            result = analyze_password(
                password
            )


            self.report.insert(
                tk.END,
                f"TEST CASE {number}\n"
            )

            self.report.insert(
                tk.END,
                f"Purpose : {purpose}\n"
            )

            self.report.insert(
                tk.END,
                f"Strength: {result['strength']}\n"
            )

            self.report.insert(
                tk.END,
                f"Risk    : {result['risk']}\n"
            )

            self.report.insert(
                tk.END,
                f"Score   : {result['score']}\n"
            )

            self.report.insert(
                tk.END,
                "-" * 65 + "\n\n"
            )


    # ========================================================
    # CLEAR
    # ========================================================

    def clear(self):

        self.password_entry.delete(
            0,
            tk.END
        )

        self.report.delete(
            "1.0",
            tk.END
        )

        self.result_label.config(
            text="STRENGTH: --",
            fg="#8b9aaa"
        )

        self.risk_label.config(
            text="RISK: --",
            fg="#8b9aaa"
        )

        self.score_label.config(
            text="SECURITY SCORE: --"
        )


    # ========================================================
    # MESSAGE
    # ========================================================

    def display_message(self, message):

        self.report.delete(
            "1.0",
            tk.END
        )

        self.report.insert(
            tk.END,
            message
        )


# ============================================================
# START PROGRAM
# ============================================================

if __name__ == "__main__":

    root = tk.Tk()

    app = PasswordAnalyzer(
        root
    )

    root.mainloop()
