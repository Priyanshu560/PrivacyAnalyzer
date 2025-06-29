import mysql.connector
from tkinter import *
from tkinter import messagebox, ttk
import csv

# Function to run privacy check and display in GUI
def run_privacy_analysis():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Priyanshu@123",  # change if your password is different
            database="PrivacyAnalyzer"
        )
        cursor = conn.cursor()
        cursor.execute("SELECT name, email, phone, password FROM user_data")
        rows = cursor.fetchall()

        # Clear previous data
        for i in tree.get_children():
            tree.delete(i)

        report_data.clear()

        for row in rows:
            name, email, phone, password = row
            score = 100
            issues = []

            if '@' in email and '.' in email:
                issues.append("Email visible")
                score -= 30

            if phone.isdigit() and len(phone) == 10:
                issues.append("Phone exposed")
                score -= 30

            if not (password.startswith("$2b$") or password.startswith("pbkdf2:")):
                issues.append("Password not hashed")
                score -= 40

            issue_text = ", ".join(issues) if issues else "✅ No issues"
            report_data.append([name, max(score, 0), issue_text])
            tree.insert("", END, values=(name, max(score, 0), issue_text))

        messagebox.showinfo("Success", "Privacy analysis completed!")

    except Exception as e:
        messagebox.showerror("Error", f"Something went wrong:\n{e}")

# Export report to CSV
def export_to_csv():
    with open("privacy_report.csv", "w", newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["User", "Privacy Score", "Issues"])
        writer.writerows(report_data)
    messagebox.showinfo("Exported", "Report saved as 'privacy_report.csv'")

# GUI Setup
root = Tk()
root.title("PrivacyAnalyzer - GUI Tool")
root.geometry("700x400")
root.configure(bg="#f0f0f0")

title = Label(root, text="🛡️ PrivacyAnalyzer", font=("Arial", 18, "bold"), bg="#f0f0f0", fg="#333")
title.pack(pady=10)

btn_frame = Frame(root, bg="#f0f0f0")
btn_frame.pack()

analyze_btn = Button(btn_frame, text="Run Privacy Check", font=("Arial", 12), command=run_privacy_analysis)
analyze_btn.grid(row=0, column=0, padx=10)

export_btn = Button(btn_frame, text="Export to CSV", font=("Arial", 12), command=export_to_csv)
export_btn.grid(row=0, column=1, padx=10)

tree = ttk.Treeview(root, columns=("User", "Score", "Issues"), show="headings", height=10)
tree.heading("User", text="User")
tree.heading("Score", text="Privacy Score")
tree.heading("Issues", text="Issues Found")
tree.column("User", width=150)
tree.column("Score", width=100)
tree.column("Issues", width=400)
tree.pack(pady=20)

report_data = []

root.mainloop()
