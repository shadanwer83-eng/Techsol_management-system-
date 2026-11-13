# Techsol Student Management System 🎓💼

An executive, modern desktop student management and fee tracking system built with **Python**, **Tkinter**, and **SQLite**. Designed for training institutes, academies, schools, and colleges to seamlessly manage student admissions, enrollments, course assignments, fee collections, and pending dues with real-time financial analytics.

---

## 🌟 Key Features

### 1. 📊 Executive KPI Dashboard
- **Total Students Counter**: Live count of all enrolled students.
- **Total Course Fees**: Sum of all assigned tuition and course fees.
- **Fees Collected to Date**: Aggregate of all fees received.
- **Pending Dues Tracker**: Real-time monitoring of all outstanding student dues.
- **Live Clock & Status Bar**: Displays current system time and operational status.

### 2. 🎓 Student Record Management (Full CRUD)
- **Student ID**: Unique identifier with an **"Auto ID"** button (e.g. `TS-1001`, `TS-1002`). If left blank, the system automatically assigns the next available sequential ID.
- **Student Name**: Full student name.
- **Student Course**: Pre-configured dropdown list of industry courses (Python Full Stack, Data Science & AI, Web Development, Cyber Security, Cloud Computing, etc.) with custom typing support.
- **Student Fees**: Total tuition/course fee amount with automatic numeric validation.
- **Student Dues Fees**: Outstanding balance amount.
- **Student Paid Fees**: Automatically calculated in real time (`Fees - Dues Fees`).
- **Contact & Email**: Student phone number and email address.
- **Action Buttons (Left Form Panel)**:
  - **➕ Add Student**: Validates entries, prevents duplicate IDs, saves record, and updates the table & KPI metrics.
  - **✏️ Update Student**: Select any student from the table, make modifications, and save updates with confirmation.
  - **🗑️ Delete Student**: Select any student and remove their record with full verification dialog.
  - **🔄 Clear Form**: Clears input fields and resets calculation status.

### 3. 🔍 Smart Search & Filtering
- Search records dynamically by:
  - **All Fields**
  - **Student ID**
  - **Student Name**
  - **Course Name**
- Filter by fee payment status:
  - **All Students**
  - **With Dues** (Highlights students with pending balances)
  - **Fully Paid** (Highlights students with zero dues)

### 4. 🧾 Instant Fee Receipt Generator
- Select any student record and click **"Generate Fee Receipt"** (or double-click the record).
- Formatted institutional receipt with student details, course name, fee breakdown, and signature section.
- **Save as Text File (`.txt`)** or **Copy to Clipboard** with one click.

### 5. 📥 Data Export & Backup
- Export the entire student directory to **CSV format** (compatible with Microsoft Excel, Google Sheets, etc.).
- Robust local **SQLite database** (`techsol_students.db`) requires zero external server setup.

### 6. 🛡️ Robust Validation & Error Handling ("Zero Errors")
- Automatic prevention of duplicate Student IDs.
- Strict numeric verification for fee and dues values (rejects negative numbers and prevents dues from exceeding total fees).
- Confirmation popups before record deletion.
- Native Windows High-DPI scaling enabled for crisp, high-resolution rendering.

---

## 📁 Project Structure

```text
Techsol management system/
│
├── main.py                             # Main entry point for the application
├── Techsol_student_management_system.py # Named entry point alias
├── dashboard.py                        # Tkinter Dashboard UI, KPI cards, and event handling
├── database.py                         # SQLite database operations, CRUD queries & statistics
├── receipt_window.py                   # Fee Receipt preview & export module
├── run.bat                             # One-click Windows desktop launcher
├── techsol_students.db                 # SQLite database (auto-generated)
└── README.md                           # Documentation & instructions
```

---

## 🚀 How to Run the Application

### Method 1: Double-Click Launcher (Windows)
Simply double-click the **`run.bat`** file located in this directory. It will detect Python and immediately launch the system.

### Method 2: Using the Command Line
Open PowerShell or Command Prompt in the project folder and run either of the following commands:

```bash
python main.py
```
*or*
```bash
python Techsol_student_management_system.py
```

---

## 📋 Required Fields Specification

| Field Name | Type | Description |
| :--- | :--- | :--- |
| `student_id` | Alphanumeric (`TEXT`) | Unique identifier for each student (e.g., `TS-1001`) |
| `student_name` | Text (`TEXT`) | Full name of the student |
| `student_course` | Text (`TEXT`) | Enrolled course/program name |
| `student_fees` | Numeric (`REAL`) | Total tuition fee for the course |
| `student_dues_fees` | Numeric (`REAL`) | Pending dues amount (0.00 if fully paid) |
| `student_paid_fees` | Numeric (`REAL`) | Automatically computed as `(fees - dues)` |
| `student_contact` | Text (`TEXT`) | Student contact / phone number |
| `student_email` | Text (`TEXT`) | Student email address |
| `enrollment_date` | Date (`TEXT`) | Date of registration (`YYYY-MM-DD`) |

---

## 💻 Tech Stack & Requirements

- **Language**: Python 3.8+ (Tested on Python 3.14)
- **GUI Framework**: Tkinter & `ttk` (Standard Python GUI library — **no external pip packages required**)
- **Database**: SQLite 3 (Built-in standard library)
- **OS**: Windows 10 / 11, Linux, or macOS

---

## 🛠️ Usage Guide

1. **Adding a Student**:
   - Click **"Auto ID"** to generate the next available ID, or type a custom ID.
   - Enter Student Name, select Course from dropdown.
   - Enter Total Fees (e.g. `45000`) and Dues Fees (e.g. `5000`). Notice the live calculation bar instantly displays the paid amount and status.
   - (Optional) Enter Contact Number and Email.
   - Click **"➕ Add Student"**.

2. **Updating a Student**:
   - Click on any row in the table. The form on the left will automatically populate with the student's information.
   - Modify the required fields and click **"✏️ Update Student"**.

3. **Deleting a Student**:
   - Select the student from the table.
   - Click **"🗑️ Delete Student"** and confirm the prompt.

4. **Generating Fee Receipt**:
   - Select a student from the table and click **"🧾 Generate Fee Receipt"** (or double-click the row).
   - Review the financial receipt, and click **"💾 Save Receipt (.txt)"** or **"📋 Copy to Clipboard"**.

5. **Exporting Data**:
   - Click **"📥 Export to CSV"** to save an Excel-ready `.csv` file.

---

## 📄 License
Developed for Techsol Institute. Free to use, adapt, and extend.
