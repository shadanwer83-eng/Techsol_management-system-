"""
Receipt Window Module for Techsol Student Management System
Generates and displays printable fee receipts with save & copy capabilities.
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime


class FeeReceiptWindow(tk.Toplevel):
    def __init__(self, parent, student_data):
        super().__init__(parent)
        self.student = student_data
        self.title(f"Fee Receipt - {self.student.get('student_id', 'N/A')}")
        self.geometry("620x720")
        self.minsize(580, 650)
        self.configure(bg="#0f172a")

        # Center on parent
        self.transient(parent)
        self.grab_set()

        self._build_ui()
        self._populate_receipt()

    def _build_ui(self):
        # Header banner
        header_frame = tk.Frame(self, bg="#1e293b", pady=15, padx=20)
        header_frame.pack(fill=tk.X)

        title_lbl = tk.Label(
            header_frame,
            text="TECHSOL INSTITUTE OF TECHNOLOGY",
            font=("Segoe UI", 16, "bold"),
            bg="#1e293b",
            fg="#38bdf8"
        )
        title_lbl.pack()

        subtitle_lbl = tk.Label(
            header_frame,
            text="Official Student Fee Receipt & Financial Statement",
            font=("Segoe UI", 10),
            bg="#1e293b",
            fg="#94a3b8"
        )
        subtitle_lbl.pack(pady=(2, 0))

        # Receipt Container Frame
        body_frame = tk.Frame(self, bg="#0f172a", padx=20, pady=15)
        body_frame.pack(fill=tk.BOTH, expand=True)

        # Receipt Text Display with Scrollbar
        text_frame = tk.Frame(body_frame, bg="#ffffff", bd=1, relief=tk.SOLID)
        text_frame.pack(fill=tk.BOTH, expand=True)

        scroll_y = tk.Scrollbar(text_frame, orient=tk.VERTICAL)
        self.receipt_text = tk.Text(
            text_frame,
            wrap=tk.WORD,
            font=("Consolas", 10),
            bg="#f8fafc",
            fg="#1e293b",
            padx=16,
            pady=16,
            yscrollcommand=scroll_y.set,
            relief=tk.FLAT
        )
        scroll_y.config(command=self.receipt_text.yview)
        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        self.receipt_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Bottom Button Bar
        btn_bar = tk.Frame(self, bg="#0f172a", pady=15, padx=20)
        btn_bar.pack(fill=tk.X)

        save_btn = tk.Button(
            btn_bar,
            text="💾 Save Receipt (.txt)",
            font=("Segoe UI", 10, "bold"),
            bg="#0284c7",
            fg="#ffffff",
            activebackground="#0369a1",
            activeforeground="#ffffff",
            relief=tk.FLAT,
            padx=15,
            pady=8,
            cursor="hand2",
            command=self._save_receipt
        )
        save_btn.pack(side=tk.LEFT, padx=(0, 10))

        copy_btn = tk.Button(
            btn_bar,
            text="📋 Copy to Clipboard",
            font=("Segoe UI", 10, "bold"),
            bg="#475569",
            fg="#ffffff",
            activebackground="#334155",
            activeforeground="#ffffff",
            relief=tk.FLAT,
            padx=15,
            pady=8,
            cursor="hand2",
            command=self._copy_to_clipboard
        )
        copy_btn.pack(side=tk.LEFT, padx=(0, 10))

        close_btn = tk.Button(
            btn_bar,
            text="✕ Close",
            font=("Segoe UI", 10),
            bg="#ef4444",
            fg="#ffffff",
            activebackground="#dc2626",
            activeforeground="#ffffff",
            relief=tk.FLAT,
            padx=18,
            pady=8,
            cursor="hand2",
            command=self.destroy
        )
        close_btn.pack(side=tk.RIGHT)

    def _populate_receipt(self):
        s = self.student
        student_id = s.get("student_id", "N/A")
        name = s.get("student_name", "N/A")
        course = s.get("student_course", "N/A")
        fees = float(s.get("student_fees", 0.0))
        dues = float(s.get("student_dues_fees", 0.0))
        paid = float(s.get("student_paid_fees", fees - dues))
        contact = s.get("student_contact", "N/A") or "N/A"
        email = s.get("student_email", "N/A") or "N/A"
        date_str = s.get("enrollment_date", datetime.now().strftime("%Y-%m-%d"))
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        status_text = "PAID IN FULL" if dues == 0 else f"PENDING DUES: {dues:,.2f}"

        receipt_content = f"""
======================================================================
               TECHSOL INSTITUTE OF TECHNOLOGY & LEARNING
             Student Management & Financial Accounts Bureau
======================================================================
Receipt ID      : RCP-{student_id}-{datetime.now().strftime('%y%m%d%H%M')}
Generated On    : {timestamp}
Academic Date   : {date_str}
======================================================================

STUDENT PARTICULARS:
----------------------------------------------------------------------
Student ID      : {student_id}
Student Name    : {name}
Enrolled Course : {course}
Contact Phone   : {contact}
Email Address   : {email}

----------------------------------------------------------------------
FEE BREAKDOWN & ACCOUNT SUMMARY:
----------------------------------------------------------------------
1. Total Course Tuition Fees      :   Rs. {fees:>12,.2f}
2. Fees Paid to Date              :   Rs. {paid:>12,.2f}
----------------------------------------------------------------------
3. OUTSTANDING DUES FEES          :   Rs. {dues:>12,.2f}
----------------------------------------------------------------------

FEE STATUS      : [{status_text}]

======================================================================
Terms & Conditions:
1. This is a computer-generated fee acknowledgement receipt.
2. Dues must be cleared before course completion and certification.
3. For fee queries, contact Techsol Accounts at accounts@techsol.edu.
======================================================================

                       [ AUTHORIZED SIGNATORY ]
                     Techsol Academic Administration
======================================================================
"""
        self.receipt_text.delete("1.0", tk.END)
        self.receipt_text.insert(tk.END, receipt_content.strip())
        self.receipt_text.config(state=tk.DISABLED)

    def _save_receipt(self):
        content = self.receipt_text.get("1.0", tk.END)
        student_id = self.student.get("student_id", "student")
        default_file = f"Techsol_Fee_Receipt_{student_id}.txt"

        file_path = filedialog.asksaveasfilename(
            parent=self,
            defaultextension=".txt",
            initialfile=default_file,
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        )
        if file_path:
            try:
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(content)
                messagebox.showinfo("Receipt Saved", f"Fee receipt saved successfully to:\n{file_path}", parent=self)
            except Exception as e:
                messagebox.showerror("Save Error", f"Could not save receipt: {str(e)}", parent=self)

    def _copy_to_clipboard(self):
        content = self.receipt_text.get("1.0", tk.END)
        self.clipboard_clear()
        self.clipboard_append(content)
        messagebox.showinfo("Copied", "Fee receipt content copied to clipboard.", parent=self)
