"""
Dashboard Module for Techsol Student Management System
Provides a modern, responsive Tkinter graphical interface for student records,
fee management, statistics tracking, and receipt generation.
Optimized for all desktop display resolutions (including 1366x768 and High-DPI scaling)
with permanently visible Delete and Receipt buttons.
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import csv
from datetime import datetime
import database
from receipt_window import FeeReceiptWindow


class TechsolDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("Techsol Student Management System - Dashboard")
        self.root.geometry("1240x650")
        self.root.minsize(960, 540)

        # Theme Colors
        self.COLOR_BG = "#0f172a"          # Slate 900
        self.COLOR_SURFACE = "#1e293b"     # Slate 800
        self.COLOR_CARD_BG = "#1e293b"     # Slate 800
        self.COLOR_BORDER = "#334155"      # Slate 700
        self.COLOR_TEXT_PRIMARY = "#f8fafc"# Slate 50
        self.COLOR_TEXT_MUTED = "#94a3b8"  # Slate 400
        self.COLOR_PRIMARY = "#2563eb"     # Blue 600
        self.COLOR_SUCCESS = "#10b981"     # Emerald 500
        self.COLOR_WARNING = "#f59e0b"     # Amber 500
        self.COLOR_DANGER = "#ef4444"      # Red 500
        self.COLOR_ACCENT = "#38bdf8"      # Sky 400

        self.root.configure(bg=self.COLOR_BG)

        # Configure TTK Styles
        self._setup_styles()

        # Build Main Layout
        self._build_header()
        self._build_kpi_cards()
        self._build_main_content()
        self._setup_shortcuts()

        # Initial Data Load & Clock
        self.refresh_all()
        self._update_clock()

    def _setup_styles(self):
        """Configures ttk styles for treeview, scrollbars, and comboboxes."""
        self.style = ttk.Style()
        self.style.theme_use("clam")

        # Treeview styling
        self.style.configure(
            "Treeview",
            background="#1e293b",
            foreground="#f8fafc",
            fieldbackground="#1e293b",
            rowheight=28,
            font=("Segoe UI", 9),
            borderwidth=0
        )
        self.style.configure(
            "Treeview.Heading",
            background="#0f172a",
            foreground="#38bdf8",
            font=("Segoe UI", 9, "bold"),
            relief="flat",
            padding=5
        )
        self.style.map(
            "Treeview",
            background=[("selected", "#2563eb")],
            foreground=[("selected", "#ffffff")]
        )
        self.style.map(
            "Treeview.Heading",
            background=[("active", "#1e293b")]
        )

        # Combobox styling
        self.style.configure(
            "TCombobox",
            fieldbackground="#0f172a",
            background="#334155",
            foreground="#f8fafc",
            arrowcolor="#38bdf8"
        )
        self.style.map(
            "TCombobox",
            fieldbackground=[("readonly", "#0f172a")],
            selectbackground=[("readonly", "#2563eb")],
            selectforeground=[("readonly", "#ffffff")]
        )

    def _build_header(self):
        """Top Branding & Live Status Bar (compact and sleek)."""
        header = tk.Frame(self.root, bg=self.COLOR_SURFACE, height=50, padx=20, pady=6)
        header.pack(fill=tk.X, side=tk.TOP)

        # Left branding
        brand_frame = tk.Frame(header, bg=self.COLOR_SURFACE)
        brand_frame.pack(side=tk.LEFT)

        title_lbl = tk.Label(
            brand_frame,
            text="TECHSOL",
            font=("Segoe UI", 16, "bold"),
            bg=self.COLOR_SURFACE,
            fg=self.COLOR_ACCENT
        )
        title_lbl.pack(side=tk.LEFT)

        subtitle_lbl = tk.Label(
            brand_frame,
            text=" | Student Management & Fee Portal",
            font=("Segoe UI", 12),
            bg=self.COLOR_SURFACE,
            fg=self.COLOR_TEXT_PRIMARY
        )
        subtitle_lbl.pack(side=tk.LEFT)

        # Right status & clock
        right_frame = tk.Frame(header, bg=self.COLOR_SURFACE)
        right_frame.pack(side=tk.RIGHT)

        self.clock_lbl = tk.Label(
            right_frame,
            text="",
            font=("Segoe UI", 9, "bold"),
            bg="#0f172a",
            fg=self.COLOR_ACCENT,
            padx=10,
            pady=3,
            relief=tk.FLAT
        )
        self.clock_lbl.pack(side=tk.RIGHT)

    def _update_clock(self):
        now_str = datetime.now().strftime("%A, %d %b %Y  |  %I:%M:%S %p")
        self.clock_lbl.config(text=now_str)
        self.root.after(1000, self._update_clock)

    def _setup_shortcuts(self):
        """Binds standard keyboard shortcuts for fast operation."""
        self.root.bind("<Delete>", lambda e: self.action_delete_student())
        self.root.bind("<F5>", lambda e: self.refresh_all())
        self.root.bind("<Control-r>", lambda e: self.refresh_all())
        self.root.bind("<Control-R>", lambda e: self.refresh_all())

    def _build_kpi_cards(self):
        """Metric summary cards at top of dashboard (compact padding)."""
        cards_container = tk.Frame(self.root, bg=self.COLOR_BG, padx=16, pady=4)
        cards_container.pack(fill=tk.X, side=tk.TOP)

        # 4 Responsive Metric Cards
        self.card_total_students = self._create_card(
            cards_container, "Total Students", "0", "👥 Enrolled", "#3b82f6", col=0
        )
        self.card_total_fees = self._create_card(
            cards_container, "Total Course Fees", "Rs. 0.00", "💰 Total Value", "#8b5cf6", col=1
        )
        self.card_total_paid = self._create_card(
            cards_container, "Fees Collected", "Rs. 0.00", "✅ Paid to Date", "#10b981", col=2
        )
        self.card_total_dues = self._create_card(
            cards_container, "Pending Dues", "Rs. 0.00", "⚠️ Outstanding", "#ef4444", col=3
        )

        for i in range(4):
            cards_container.columnconfigure(i, weight=1, uniform="card")

    def _create_card(self, parent, title, initial_val, subtext, accent_color, col):
        card = tk.Frame(parent, bg=self.COLOR_CARD_BG, bd=1, relief=tk.SOLID, padx=12, pady=6)
        card.grid(row=0, column=col, sticky="nsew", padx=4)

        t_lbl = tk.Label(
            card, text=title.upper(), font=("Segoe UI", 8, "bold"),
            bg=self.COLOR_CARD_BG, fg=self.COLOR_TEXT_MUTED
        )
        t_lbl.pack(anchor="w")

        val_lbl = tk.Label(
            card, text=initial_val, font=("Segoe UI", 14, "bold"),
            bg=self.COLOR_CARD_BG, fg=accent_color
        )
        val_lbl.pack(anchor="w", pady=(1, 1))

        sub_lbl = tk.Label(
            card, text=subtext, font=("Segoe UI", 8),
            bg=self.COLOR_CARD_BG, fg=self.COLOR_TEXT_MUTED
        )
        sub_lbl.pack(anchor="w")

        return val_lbl

    def _build_main_content(self):
        """Main body with Left Form Panel and Right Table Directory."""
        main_frame = tk.Frame(self.root, bg=self.COLOR_BG, padx=16, pady=4)
        main_frame.pack(fill=tk.BOTH, expand=True)

        main_frame.columnconfigure(0, weight=4)   # Left Form (40%)
        main_frame.columnconfigure(1, weight=6)   # Right Table (60%)
        main_frame.rowconfigure(0, weight=1)

        self._build_left_form(main_frame)
        self._build_right_table(main_frame)

    def _build_left_form(self, parent):
        """
        Form Card for Student Registration & Modifications.
        Action buttons are pinned to the bottom using side=tk.BOTTOM
        so that Delete and Clear buttons are NEVER cut off.
        """
        form_card = tk.Frame(parent, bg=self.COLOR_CARD_BG, bd=1, relief=tk.SOLID, padx=16, pady=10)
        form_card.grid(row=0, column=0, sticky="nsew", padx=(0, 8), pady=(0, 6))

        # Title
        f_title = tk.Label(
            form_card,
            text="🎓 Student Registration & Details",
            font=("Segoe UI", 12, "bold"),
            bg=self.COLOR_CARD_BG,
            fg=self.COLOR_ACCENT
        )
        f_title.pack(anchor="w", pady=(0, 6))

        # PINNED BOTTOM ACTION BUTTONS: Add, Update, Delete, Clear
        # Packed with side=tk.BOTTOM so they are GUARANTEED visible at all screen sizes
        btn_grid = tk.Frame(form_card, bg=self.COLOR_CARD_BG)
        btn_grid.pack(side=tk.BOTTOM, fill=tk.X, pady=(6, 0))
        btn_grid.columnconfigure(0, weight=1)
        btn_grid.columnconfigure(1, weight=1)

        # Add Button
        self.btn_add = tk.Button(
            btn_grid, text="➕ Add Student", font=("Segoe UI", 9, "bold"),
            bg=self.COLOR_SUCCESS, fg="#ffffff", activebackground="#059669",
            activeforeground="#ffffff", relief=tk.FLAT, pady=6, cursor="hand2",
            command=self.action_add_student
        )
        self.btn_add.grid(row=0, column=0, sticky="ew", padx=(0, 3), pady=2)

        # Update Button
        self.btn_update = tk.Button(
            btn_grid, text="✏️ Update Student", font=("Segoe UI", 9, "bold"),
            bg=self.COLOR_PRIMARY, fg="#ffffff", activebackground="#1d4ed8",
            activeforeground="#ffffff", relief=tk.FLAT, pady=6, cursor="hand2",
            command=self.action_update_student
        )
        self.btn_update.grid(row=0, column=1, sticky="ew", padx=(3, 0), pady=2)

        # Delete Button (Prominently styled in Red)
        self.btn_delete = tk.Button(
            btn_grid, text="🗑️ Delete Student", font=("Segoe UI", 9, "bold"),
            bg=self.COLOR_DANGER, fg="#ffffff", activebackground="#dc2626",
            activeforeground="#ffffff", relief=tk.FLAT, pady=6, cursor="hand2",
            command=self.action_delete_student
        )
        self.btn_delete.grid(row=1, column=0, sticky="ew", padx=(0, 3), pady=2)

        # Clear Form Button
        self.btn_clear = tk.Button(
            btn_grid, text="🔄 Clear Form", font=("Segoe UI", 9, "bold"),
            bg="#475569", fg="#ffffff", activebackground="#334155",
            activeforeground="#ffffff", relief=tk.FLAT, pady=6, cursor="hand2",
            command=self.action_clear_form
        )
        self.btn_clear.grid(row=1, column=1, sticky="ew", padx=(3, 0), pady=2)

        # Form Fields Container (fills remaining middle space)
        fields_frame = tk.Frame(form_card, bg=self.COLOR_CARD_BG)
        fields_frame.pack(fill=tk.BOTH, expand=True)

        # 1. Student ID
        id_box = tk.Frame(fields_frame, bg=self.COLOR_CARD_BG)
        id_box.pack(fill=tk.X, pady=2)
        tk.Label(
            id_box, text="Student ID *", font=("Segoe UI", 8, "bold"),
            bg=self.COLOR_CARD_BG, fg=self.COLOR_TEXT_PRIMARY
        ).pack(anchor="w")

        id_input_row = tk.Frame(id_box, bg=self.COLOR_CARD_BG)
        id_input_row.pack(fill=tk.X, pady=(1, 0))

        self.ent_id = tk.Entry(
            id_input_row, font=("Segoe UI", 9), bg="#0f172a", fg="#ffffff",
            insertbackground="#ffffff", relief=tk.FLAT, bd=4
        )
        self.ent_id.pack(side=tk.LEFT, fill=tk.X, expand=True)

        auto_id_btn = tk.Button(
            id_input_row, text="Auto ID", font=("Segoe UI", 8, "bold"),
            bg="#334155", fg="#38bdf8", activebackground="#475569",
            activeforeground="#ffffff", relief=tk.FLAT, padx=8, pady=2,
            cursor="hand2", command=self._generate_auto_id
        )
        auto_id_btn.pack(side=tk.RIGHT, padx=(4, 0))

        # 2. Student Name
        self.ent_name = self._add_entry_field(fields_frame, "Student Name *", "Enter full name")

        # 3. Student Course
        course_box = tk.Frame(fields_frame, bg=self.COLOR_CARD_BG)
        course_box.pack(fill=tk.X, pady=2)
        tk.Label(
            course_box, text="Student Course *", font=("Segoe UI", 8, "bold"),
            bg=self.COLOR_CARD_BG, fg=self.COLOR_TEXT_PRIMARY
        ).pack(anchor="w")

        self.courses_list = [
            "Python Full Stack",
            "Data Science & AI",
            "Web Development (MERN)",
            "Cloud Computing & DevOps",
            "Cyber Security",
            "Java Enterprise Developer",
            "UI/UX Design & Frontend",
            "Mobile App Development (Flutter)"
        ]
        self.cb_course = ttk.Combobox(course_box, values=self.courses_list, font=("Segoe UI", 9))
        self.cb_course.pack(fill=tk.X, pady=(1, 0))
        self.cb_course.set("Python Full Stack")

        # 4 & 5. Fees Row (Student Fees & Student Dues Fees side by side)
        fees_row = tk.Frame(fields_frame, bg=self.COLOR_CARD_BG)
        fees_row.pack(fill=tk.X, pady=2)
        fees_row.columnconfigure(0, weight=1)
        fees_row.columnconfigure(1, weight=1)

        # Student Fees
        fees_col1 = tk.Frame(fees_row, bg=self.COLOR_CARD_BG)
        fees_col1.grid(row=0, column=0, sticky="ew", padx=(0, 4))
        tk.Label(
            fees_col1, text="Student Fees (Rs.) *", font=("Segoe UI", 8, "bold"),
            bg=self.COLOR_CARD_BG, fg=self.COLOR_TEXT_PRIMARY
        ).pack(anchor="w")
        self.ent_fees = tk.Entry(
            fees_col1, font=("Segoe UI", 9), bg="#0f172a", fg="#ffffff",
            insertbackground="#ffffff", relief=tk.FLAT, bd=4
        )
        self.ent_fees.pack(fill=tk.X, pady=(1, 0))
        self.ent_fees.bind("<KeyRelease>", self._on_fees_change)

        # Student Dues Fees
        fees_col2 = tk.Frame(fees_row, bg=self.COLOR_CARD_BG)
        fees_col2.grid(row=0, column=1, sticky="ew", padx=(4, 0))
        tk.Label(
            fees_col2, text="Student Dues Fees (Rs.) *", font=("Segoe UI", 8, "bold"),
            bg=self.COLOR_CARD_BG, fg=self.COLOR_TEXT_PRIMARY
        ).pack(anchor="w")
        self.ent_dues = tk.Entry(
            fees_col2, font=("Segoe UI", 9), bg="#0f172a", fg="#ffffff",
            insertbackground="#ffffff", relief=tk.FLAT, bd=4
        )
        self.ent_dues.pack(fill=tk.X, pady=(1, 0))
        self.ent_dues.bind("<KeyRelease>", self._on_fees_change)

        # Dynamic Calculated Paid & Status Bar
        self.calc_bar = tk.Label(
            fields_frame,
            text="Calculated Paid: Rs. 0.00  |  Status: New",
            font=("Segoe UI", 8, "italic"),
            bg="#0f172a",
            fg=self.COLOR_ACCENT,
            padx=8,
            pady=3,
            relief=tk.FLAT
        )
        self.calc_bar.pack(fill=tk.X, pady=(3, 2))

        # 6. Contact / Phone
        self.ent_contact = self._add_entry_field(fields_frame, "Contact Number", "+91 ...")

        # 7. Email Address
        self.ent_email = self._add_entry_field(fields_frame, "Email Address", "student@example.com")

    def _add_entry_field(self, parent, label_text, placeholder=""):
        box = tk.Frame(parent, bg=self.COLOR_CARD_BG)
        box.pack(fill=tk.X, pady=2)
        tk.Label(
            box, text=label_text, font=("Segoe UI", 8, "bold"),
            bg=self.COLOR_CARD_BG, fg=self.COLOR_TEXT_PRIMARY
        ).pack(anchor="w")

        ent = tk.Entry(
            box, font=("Segoe UI", 9), bg="#0f172a", fg="#ffffff",
            insertbackground="#ffffff", relief=tk.FLAT, bd=4
        )
        ent.pack(fill=tk.X, pady=(1, 0))
        return ent

    def _build_right_table(self, parent):
        """Right Records Directory & Treeview Table."""
        table_card = tk.Frame(parent, bg=self.COLOR_CARD_BG, bd=1, relief=tk.SOLID, padx=14, pady=10)
        table_card.grid(row=0, column=1, sticky="nsew", padx=(8, 0), pady=(0, 6))

        # Top Search & Action Bar
        search_bar = tk.Frame(table_card, bg=self.COLOR_CARD_BG)
        search_bar.pack(fill=tk.X, pady=(0, 6))

        tk.Label(
            search_bar, text="🔍 Search:", font=("Segoe UI", 8, "bold"),
            bg=self.COLOR_CARD_BG, fg=self.COLOR_TEXT_PRIMARY
        ).pack(side=tk.LEFT, padx=(0, 4))

        self.ent_search = tk.Entry(
            search_bar, font=("Segoe UI", 9), bg="#0f172a", fg="#ffffff",
            insertbackground="#ffffff", relief=tk.FLAT, bd=4, width=14
        )
        self.ent_search.pack(side=tk.LEFT, padx=(0, 6))
        self.ent_search.bind("<Return>", lambda e: self.action_search())

        tk.Label(
            search_bar, text="In:", font=("Segoe UI", 8),
            bg=self.COLOR_CARD_BG, fg=self.COLOR_TEXT_MUTED
        ).pack(side=tk.LEFT, padx=(0, 3))

        self.cb_search_by = ttk.Combobox(
            search_bar, values=["All Fields", "Student ID", "Student Name", "Course"],
            state="readonly", width=10, font=("Segoe UI", 8)
        )
        self.cb_search_by.set("All Fields")
        self.cb_search_by.pack(side=tk.LEFT, padx=(0, 6))

        tk.Label(
            search_bar, text="Filter:", font=("Segoe UI", 8),
            bg=self.COLOR_CARD_BG, fg=self.COLOR_TEXT_MUTED
        ).pack(side=tk.LEFT, padx=(0, 3))

        self.cb_filter_status = ttk.Combobox(
            search_bar, values=["All Students", "With Dues", "Fully Paid"],
            state="readonly", width=10, font=("Segoe UI", 8)
        )
        self.cb_filter_status.set("All Students")
        self.cb_filter_status.pack(side=tk.LEFT, padx=(0, 6))
        self.cb_filter_status.bind("<<ComboboxSelected>>", lambda e: self.action_search())

        btn_search = tk.Button(
            search_bar, text="Search", font=("Segoe UI", 8, "bold"),
            bg=self.COLOR_PRIMARY, fg="#ffffff", relief=tk.FLAT, padx=8, pady=2,
            cursor="hand2", command=self.action_search
        )
        btn_search.pack(side=tk.LEFT, padx=(0, 4))

        btn_reset_search = tk.Button(
            search_bar, text="Reset", font=("Segoe UI", 8),
            bg="#475569", fg="#ffffff", relief=tk.FLAT, padx=6, pady=2,
            cursor="hand2", command=self.action_reset_search
        )
        btn_reset_search.pack(side=tk.LEFT)

        # Quick Action Buttons in Top Table Toolbar for Instant Access
        btn_top_delete = tk.Button(
            search_bar, text="🗑️ Delete", font=("Segoe UI", 8, "bold"),
            bg=self.COLOR_DANGER, fg="#ffffff", activebackground="#dc2626",
            relief=tk.FLAT, padx=8, pady=2, cursor="hand2",
            command=self.action_delete_student
        )
        btn_top_delete.pack(side=tk.RIGHT, padx=(4, 0))

        btn_top_receipt = tk.Button(
            search_bar, text="🧾 Fee Receipt", font=("Segoe UI", 8, "bold"),
            bg="#0284c7", fg="#ffffff", activebackground="#0369a1",
            relief=tk.FLAT, padx=8, pady=2, cursor="hand2",
            command=self.action_open_receipt
        )
        btn_top_receipt.pack(side=tk.RIGHT, padx=(4, 0))

        # PINNED BOTTOM ACTION TOOLBAR
        # Packed with side=tk.BOTTOM BEFORE tree_frame so it is ALWAYS visible
        tbl_actions = tk.Frame(table_card, bg=self.COLOR_CARD_BG, pady=6)
        tbl_actions.pack(side=tk.BOTTOM, fill=tk.X)

        btn_receipt = tk.Button(
            tbl_actions, text="🧾 Generate Fee Receipt", font=("Segoe UI", 9, "bold"),
            bg="#0284c7", fg="#ffffff", activebackground="#0369a1",
            relief=tk.FLAT, padx=12, pady=5, cursor="hand2",
            command=self.action_open_receipt
        )
        btn_receipt.pack(side=tk.LEFT, padx=(0, 8))

        btn_delete_tbl = tk.Button(
            tbl_actions, text="🗑️ Delete Student", font=("Segoe UI", 9, "bold"),
            bg=self.COLOR_DANGER, fg="#ffffff", activebackground="#dc2626",
            relief=tk.FLAT, padx=12, pady=5, cursor="hand2",
            command=self.action_delete_student
        )
        btn_delete_tbl.pack(side=tk.LEFT, padx=(0, 8))

        btn_export = tk.Button(
            tbl_actions, text="📥 Export CSV", font=("Segoe UI", 9),
            bg="#059669", fg="#ffffff", activebackground="#047857",
            relief=tk.FLAT, padx=10, pady=5, cursor="hand2",
            command=self.action_export_csv
        )
        btn_export.pack(side=tk.LEFT, padx=(0, 8))

        btn_refresh = tk.Button(
            tbl_actions, text="🔄 Refresh All", font=("Segoe UI", 9),
            bg="#475569", fg="#ffffff", activebackground="#334155",
            relief=tk.FLAT, padx=10, pady=5, cursor="hand2",
            command=self.refresh_all
        )
        btn_refresh.pack(side=tk.LEFT)

        self.table_count_lbl = tk.Label(
            tbl_actions, text="Showing: 0 records", font=("Segoe UI", 8),
            bg=self.COLOR_CARD_BG, fg=self.COLOR_TEXT_MUTED
        )
        self.table_count_lbl.pack(side=tk.RIGHT)

        # Treeview Frame with Dual Scrollbars (fills center)
        tree_frame = tk.Frame(table_card, bg=self.COLOR_CARD_BG)
        tree_frame.pack(fill=tk.BOTH, expand=True)

        scroll_y = tk.Scrollbar(tree_frame, orient=tk.VERTICAL)
        scroll_x = tk.Scrollbar(tree_frame, orient=tk.HORIZONTAL)

        columns = (
            "student_id", "student_name", "student_course",
            "student_fees", "student_dues_fees", "student_paid_fees",
            "status", "student_contact"
        )

        self.tree = ttk.Treeview(
            tree_frame,
            columns=columns,
            show="headings",
            yscrollcommand=scroll_y.set,
            xscrollcommand=scroll_x.set
        )

        scroll_y.config(command=self.tree.yview)
        scroll_x.config(command=self.tree.xview)

        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Define Headings & Widths
        col_meta = [
            ("student_id", "Student ID", 85, "center"),
            ("student_name", "Student Name", 135, "w"),
            ("student_course", "Course", 155, "w"),
            ("student_fees", "Fees (Rs.)", 95, "e"),
            ("student_dues_fees", "Dues (Rs.)", 95, "e"),
            ("student_paid_fees", "Paid (Rs.)", 95, "e"),
            ("status", "Status", 105, "center"),
            ("student_contact", "Contact", 115, "center")
        ]

        for col_id, col_name, width, align in col_meta:
            self.tree.heading(col_id, text=col_name, command=lambda c=col_id: self._sort_tree(c))
            self.tree.column(col_id, width=width, anchor=align, minwidth=65)

        # Tag styles for dues / paid
        self.tree.tag_configure("due", foreground="#fca5a5")       # Light red text
        self.tree.tag_configure("paid", foreground="#86efac")      # Light green text

        # Bind row selection & double-click for receipt
        self.tree.bind("<<TreeviewSelect>>", self._on_tree_select)
        self.tree.bind("<Double-1>", lambda e: self.action_open_receipt())

        # Right-Click Context Menu on Treeview
        self.context_menu = tk.Menu(
            self.root, tearoff=0, bg="#1e293b", fg="#f8fafc",
            activebackground="#2563eb", activeforeground="#ffffff",
            font=("Segoe UI", 9)
        )
        self.context_menu.add_command(label="🧾 Generate Fee Receipt", command=self.action_open_receipt)
        self.context_menu.add_command(label="🗑️ Delete Selected Student", command=self.action_delete_student)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="✏️ Update / Edit in Form", command=self.action_update_student)
        self.context_menu.add_command(label="📋 Copy Student ID", command=self._copy_selected_student_id)

        self.tree.bind("<Button-3>", self._on_tree_right_click)

    def _on_tree_right_click(self, event):
        """Displays contextual right-click popup on the selected student row."""
        row_id = self.tree.identify_row(event.y)
        if row_id:
            self.tree.selection_set(row_id)
            self._on_tree_select()
        try:
            self.context_menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.context_menu.grab_release()

    def _copy_selected_student_id(self):
        selected = self.tree.selection()
        if not selected:
            return
        s_id = str(self.tree.item(selected[0])["values"][0])
        self.root.clipboard_clear()
        self.root.clipboard_append(s_id)
        messagebox.showinfo("Copied", f"Student ID '{s_id}' copied to clipboard.", parent=self.root)

    # -----------------------------
    # Business Logic & CRUD Actions
    # -----------------------------

    def _validate_inputs(self, is_update=False):
        """
        Validates user input fields.
        Returns: (is_valid, validated_data_dict_or_error_message)
        """
        s_id = self.ent_id.get().strip()
        name = self.ent_name.get().strip()
        course = self.cb_course.get().strip()
        fees_raw = self.ent_fees.get().strip()
        dues_raw = self.ent_dues.get().strip()
        contact = self.ent_contact.get().strip()
        email = self.ent_email.get().strip()

        # Check required fields
        if not s_id:
            return False, "Student ID cannot be empty. Please enter an ID or click 'Auto ID'."
        if not name:
            return False, "Student Name cannot be empty."
        if not course:
            return False, "Please select or enter a Student Course."
        if not fees_raw:
            return False, "Student Fees cannot be empty."
        if not dues_raw:
            return False, "Student Dues Fees cannot be empty (enter 0 if no dues)."

        # Validate numeric fees
        try:
            fees = float(fees_raw)
            if fees < 0:
                return False, "Student Fees must be a non-negative number."
        except ValueError:
            return False, "Invalid Student Fees amount. Please enter a valid number (e.g. 45000)."

        # Validate numeric dues
        try:
            dues = float(dues_raw)
            if dues < 0:
                return False, "Student Dues Fees cannot be negative."
            if dues > fees:
                return False, f"Student Dues Fees (Rs. {dues:,.2f}) cannot exceed Total Fees (Rs. {fees:,.2f})."
        except ValueError:
            return False, "Invalid Student Dues Fees amount. Please enter a valid number (e.g. 5000)."

        return True, {
            "student_id": s_id,
            "student_name": name,
            "student_course": course,
            "student_fees": fees,
            "student_dues_fees": dues,
            "student_paid_fees": fees - dues,
            "student_contact": contact,
            "student_email": email
        }

    def action_add_student(self):
        """Adds a new student to database."""
        # Auto-generate ID if user left it blank
        if not self.ent_id.get().strip():
            self._generate_auto_id()

        valid, result = self._validate_inputs()
        if not valid:
            messagebox.showerror("Validation Error", result, parent=self.root)
            return

        # Check if ID already exists
        existing = database.get_student_by_id(result["student_id"])
        if existing:
            messagebox.showwarning(
                "ID Already Exists",
                f"A student with ID '{result['student_id']}' already exists ({existing['student_name']}).\n\n"
                f"• Click '✏️ Update Student' to modify this existing student.\n"
                f"• Or click 'Auto ID' to assign a new unique ID.",
                parent=self.root
            )
            return

        success, msg = database.add_student(
            student_id=result["student_id"],
            name=result["student_name"],
            course=result["student_course"],
            fees=result["student_fees"],
            dues_fees=result["student_dues_fees"],
            contact=result["student_contact"],
            email=result["student_email"]
        )

        if success:
            messagebox.showinfo("Success", f"Student '{result['student_name']}' ({result['student_id']}) added successfully!", parent=self.root)
            new_id = result["student_id"]
            self.action_clear_form()
            self.refresh_all()
            self._select_tree_row_by_id(new_id)
        else:
            messagebox.showerror("Error Adding Student", msg, parent=self.root)

    def action_update_student(self):
        """Updates currently selected or typed student record."""
        # If form ID is empty, check if row is selected in table
        if not self.ent_id.get().strip():
            selected = self.tree.selection()
            if selected:
                self._on_tree_select()
            else:
                messagebox.showwarning(
                    "Selection Required",
                    "Please select a student from the table or fill in the student form to update.",
                    parent=self.root
                )
                return

        valid, result = self._validate_inputs(is_update=True)
        if not valid:
            messagebox.showerror("Validation Error", result, parent=self.root)
            return

        # Check if record exists
        existing = database.get_student_by_id(result["student_id"])
        if not existing:
            messagebox.showwarning(
                "Not Found",
                f"No student found with ID '{result['student_id']}'.\n\n"
                f"To add this as a new student, click '➕ Add Student' instead.",
                parent=self.root
            )
            return

        confirm = messagebox.askyesno(
            "Confirm Update",
            f"Are you sure you want to update records for:\n\n"
            f"• Student ID: {result['student_id']}\n"
            f"• Name: {result['student_name']}\n"
            f"• Course: {result['student_course']}\n"
            f"• Total Fees: Rs. {result['student_fees']:,.2f}\n"
            f"• Dues Fees: Rs. {result['student_dues_fees']:,.2f}?",
            parent=self.root
        )
        if not confirm:
            return

        success, msg = database.update_student(
            student_id=result["student_id"],
            name=result["student_name"],
            course=result["student_course"],
            fees=result["student_fees"],
            dues_fees=result["student_dues_fees"],
            contact=result["student_contact"],
            email=result["student_email"]
        )

        if success:
            messagebox.showinfo("Success", f"Student '{result['student_name']}' ({result['student_id']}) updated successfully!", parent=self.root)
            self.refresh_all()
            self._select_tree_row_by_id(result["student_id"])
        else:
            messagebox.showerror("Update Error", msg, parent=self.root)

    def action_delete_student(self):
        """Deletes a student record with confirmation."""
        s_id = None
        selected = self.tree.selection()
        if selected:
            s_id = str(self.tree.item(selected[0])["values"][0])
        elif self.ent_id.get().strip():
            s_id = self.ent_id.get().strip()

        if not s_id:
            messagebox.showwarning(
                "Selection Required",
                "Please select a student record from the table to delete.",
                parent=self.root
            )
            return

        existing = database.get_student_by_id(s_id)
        if not existing:
            messagebox.showerror("Not Found", f"Student with ID '{s_id}' does not exist.", parent=self.root)
            return

        confirm = messagebox.askyesno(
            "Confirm Deletion",
            f"⚠️ Are you sure you want to permanently delete student:\n\n"
            f"• Student ID: {s_id}\n"
            f"• Name: {existing['student_name']}\n"
            f"• Course: {existing['student_course']}\n"
            f"• Total Fees: Rs. {float(existing['student_fees']):,.2f}\n"
            f"• Pending Dues: Rs. {float(existing['student_dues_fees']):,.2f}\n\n"
            "This action cannot be undone!",
            icon="warning",
            parent=self.root
        )
        if not confirm:
            return

        success, msg = database.delete_student(s_id)
        if success:
            messagebox.showinfo("Deleted", f"Student '{existing['student_name']}' ({s_id}) deleted successfully.", parent=self.root)
            self.action_clear_form()
            self.refresh_all()
        else:
            messagebox.showerror("Deletion Error", msg, parent=self.root)

    def action_clear_form(self):
        """Clears all input fields in the registration panel."""
        self.ent_id.delete(0, tk.END)
        self.ent_name.delete(0, tk.END)
        self.cb_course.set("Python Full Stack")
        self.ent_fees.delete(0, tk.END)
        self.ent_dues.delete(0, tk.END)
        self.ent_contact.delete(0, tk.END)
        self.ent_email.delete(0, tk.END)
        self.calc_bar.config(text="Calculated Paid: Rs. 0.00  |  Status: New", fg=self.COLOR_ACCENT)

        selected = self.tree.selection()
        if selected:
            self.tree.selection_remove(selected)

    def _generate_auto_id(self):
        """Generates next available Student ID and populates entry."""
        next_id = database.get_next_student_id()
        self.ent_id.delete(0, tk.END)
        self.ent_id.insert(0, next_id)

    def _select_tree_row_by_id(self, student_id):
        """Selects and scrolls to a given student record in the treeview table."""
        for item in self.tree.get_children():
            vals = self.tree.item(item, "values")
            if vals and str(vals[0]) == str(student_id):
                self.tree.selection_set(item)
                self.tree.see(item)
                break

    def _on_fees_change(self, event=None):
        """Recalculates Paid amount live as user types fees and dues."""
        try:
            f = float(self.ent_fees.get().strip() or 0)
            d = float(self.ent_dues.get().strip() or 0)
            p = f - d
            if d == 0 and f > 0:
                status = "FULLY PAID ✅"
                color = self.COLOR_SUCCESS
            elif d > 0:
                status = f"PENDING DUES: Rs. {d:,.2f} ⚠️"
                color = self.COLOR_WARNING
            else:
                status = "Ready"
                color = self.COLOR_ACCENT

            self.calc_bar.config(
                text=f"Paid: Rs. {p:,.2f}  |  {status}",
                fg=color
            )
        except ValueError:
            self.calc_bar.config(
                text="⚠️ Please enter valid numeric values for fees & dues",
                fg=self.COLOR_DANGER
            )

    def _on_tree_select(self, event=None):
        """Fills form when a row in treeview is clicked."""
        selected = self.tree.selection()
        if not selected:
            return

        item = self.tree.item(selected[0])
        vals = item["values"]
        if not vals:
            return

        s_id = str(vals[0])
        student = database.get_student_by_id(s_id)
        if not student:
            return

        # Fill inputs
        self.ent_id.delete(0, tk.END)
        self.ent_id.insert(0, student["student_id"])

        self.ent_name.delete(0, tk.END)
        self.ent_name.insert(0, student["student_name"])

        self.cb_course.set(student["student_course"])

        self.ent_fees.delete(0, tk.END)
        self.ent_fees.insert(0, f"{float(student['student_fees']):.2f}")

        self.ent_dues.delete(0, tk.END)
        self.ent_dues.insert(0, f"{float(student['student_dues_fees']):.2f}")

        self.ent_contact.delete(0, tk.END)
        self.ent_contact.insert(0, student["student_contact"] or "")

        self.ent_email.delete(0, tk.END)
        self.ent_email.insert(0, student["student_email"] or "")

        self._on_fees_change()

    def action_search(self):
        """Executes search and filter on student table."""
        q = self.ent_search.get().strip()
        search_by = self.cb_search_by.get()
        filter_status = self.cb_filter_status.get()

        rows = database.search_students(query=q, search_by=search_by, status_filter=filter_status)
        self._populate_tree(rows)

    def action_reset_search(self):
        """Resets search filters and reloads all records."""
        self.ent_search.delete(0, tk.END)
        self.cb_search_by.set("All Fields")
        self.cb_filter_status.set("All Students")
        self.refresh_all()

    def _populate_tree(self, rows):
        """Populates Treeview with given student rows."""
        self.tree.delete(*self.tree.get_children())
        for row in rows:
            fees = float(row["student_fees"])
            dues = float(row["student_dues_fees"])
            paid = float(row["student_paid_fees"])

            if dues > 0:
                status = f"DUE ({dues:,.0f})"
                tag = "due"
            else:
                status = "PAID"
                tag = "paid"

            self.tree.insert(
                "",
                tk.END,
                values=(
                    row["student_id"],
                    row["student_name"],
                    row["student_course"],
                    f"{fees:,.2f}",
                    f"{dues:,.2f}",
                    f"{paid:,.2f}",
                    status,
                    row["student_contact"] or "-"
                ),
                tags=(tag,)
            )

        self.table_count_lbl.config(text=f"Showing: {len(rows)} records")

    def _sort_tree(self, col):
        """Sorts treeview by column."""
        items = [(self.tree.set(k, col), k) for k in self.tree.get_children("")]
        try:
            items.sort(key=lambda t: float(t[0].replace(",", "").replace("Rs.", "").strip()))
        except ValueError:
            items.sort(key=lambda t: t[0].lower())

        for index, (_, k) in enumerate(items):
            self.tree.move(k, "", index)

    def refresh_all(self):
        """Refreshes KPI metric cards and student directory table."""
        stats = database.get_statistics()

        self.card_total_students.config(text=str(stats["total_students"]))
        self.card_total_fees.config(text=f"Rs. {stats['total_fees']:,.2f}")
        self.card_total_paid.config(text=f"Rs. {stats['total_paid']:,.2f}")
        self.card_total_dues.config(text=f"Rs. {stats['total_dues']:,.2f}")

        rows = database.get_all_students()
        self._populate_tree(rows)

    def action_open_receipt(self):
        """Opens the Fee Receipt window for the selected student."""
        selected = self.tree.selection()
        if not selected:
            s_id = self.ent_id.get().strip()
            if not s_id:
                messagebox.showwarning("Receipt Generation", "Please select a student from the table first.", parent=self.root)
                return
        else:
            s_id = self.tree.item(selected[0])["values"][0]

        student = database.get_student_by_id(s_id)
        if not student:
            messagebox.showerror("Error", f"Student record '{s_id}' not found.", parent=self.root)
            return

        FeeReceiptWindow(self.root, dict(student))

    def action_export_csv(self):
        """Exports currently displayed student records to CSV."""
        rows = database.get_all_students()
        if not rows:
            messagebox.showwarning("Export CSV", "No student records available to export.", parent=self.root)
            return

        file_path = filedialog.asksaveasfilename(
            parent=self.root,
            defaultextension=".csv",
            initialfile=f"Techsol_Students_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
            filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")]
        )
        if not file_path:
            return

        try:
            with open(file_path, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow([
                    "Student ID", "Student Name", "Student Course",
                    "Total Fees", "Dues Fees", "Paid Fees",
                    "Contact", "Email", "Enrollment Date"
                ])
                for r in rows:
                    writer.writerow([
                        r["student_id"], r["student_name"], r["student_course"],
                        r["student_fees"], r["student_dues_fees"], r["student_paid_fees"],
                        r["student_contact"], r["student_email"], r["enrollment_date"]
                    ])

            messagebox.showinfo("Export Successful", f"Exported {len(rows)} records to:\n{file_path}", parent=self.root)
        except Exception as e:
            messagebox.showerror("Export Error", f"Failed to export CSV: {str(e)}", parent=self.root)
