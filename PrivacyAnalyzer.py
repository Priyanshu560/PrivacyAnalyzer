import mysql.connector
from tabulate import tabulate
import csv

try:
    # Step 1: Connect to MySQL
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Priyanshu@123",
        database="PrivacyAnalyzer"
    )
    cursor = conn.cursor()

    print("✅ Connected to database.\n🔍 Running Privacy Analysis with Scoring...\n")

    # Step 2: Fetch data
    cursor.execute("SELECT name, email, phone, password FROM user_data")
    rows = cursor.fetchall()

    # Step 3: Analyze privacy and calculate score
    report = []
    for row in rows:
        name, email, phone, password = row
        issues = []
        score = 100  # Start from full score

        # Check email
        if '@' in email and "." in email:
            issues.append("Email visible")
            score -= 30

        # Check phone
        if phone.isdigit() and len(phone) == 10:
            issues.append("Phone exposed")
            score -= 30

        # Check password
        if not (password.startswith("$2b$") or password.startswith("pbkdf2:")):
            issues.append("Password not hashed")
            score -= 40

        # Prepare report row
        issue_text = ", ".join(issues) if issues else "✅ No issues"
        report.append([name, max(score, 0), issue_text])  # Prevent negative score

    # Step 4: Display in terminal
    print(tabulate(report, headers=["User", "Privacy Score (100)", "Issues Found"]))

    # Step 5: Save to CSV
    with open("privacy_report.csv", "w", newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["User", "Privacy Score (100)", "Issues Found"])
        writer.writerows(report)

    print("\n📁 Report saved as 'privacy_report.csv'")

except Exception as e:
    print("❌ Error:", e)

finally:
    if 'conn' in locals():
        conn.close()
