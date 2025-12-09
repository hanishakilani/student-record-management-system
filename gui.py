import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

class StudentRecordSystem:
    def _init_(self, root):
        self.root = root
        self.root.title("Student Record Management System")
        self.root.geometry("900x600")
        self.root.configure(bg='#f0f0f0')
        
        self.students = []
        self.load_data()
        
        # Title
        title_frame = tk.Frame(root, bg='#2c3e50', height=60)
        title_frame.pack(fill='x')
        title_label = tk.Label(title_frame, text="Student Record Management System", 
                               font=('Arial', 20, 'bold'), bg='#2c3e50', fg='white')
        title_label.pack(pady=15)
        
        # Main container
        main_frame = tk.Frame(root, bg='#f0f0f0')
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Input Frame
        input_frame = tk.LabelFrame(main_frame, text="Student Information", 
                                    font=('Arial', 12, 'bold'), bg='#ecf0f1', padx=20, pady=15)
        input_frame.pack(fill='x', pady=(0, 20))
        
        # Input fields
        fields = [
            ("Student ID:", "id"),
            ("Name:", "name"),
            ("Age:", "age"),
            ("Grade:", "grade"),
            ("Major:", "major")
        ]
        
        self.entries = {}
        for i, (label, key) in enumerate(fields):
            row = i // 2
            col = (i % 2) * 2
            
            tk.Label(input_frame, text=label, font=('Arial', 10), 
                    bg='#ecf0f1').grid(row=row, column=col, sticky='e', padx=(0, 10), pady=8)
            entry = tk.Entry(input_frame, font=('Arial', 10), width=20)
            entry.grid(row=row, column=col+1, pady=8, padx=(0, 20))
            self.entries[key] = entry
        
        # Buttons Frame
        btn_frame = tk.Frame(input_frame, bg='#ecf0f1')
        btn_frame.grid(row=3, column=0, columnspan=4, pady=15)
        
        buttons = [
            ("Add Student", self.add_student, '#27ae60'),
            ("Update Student", self.update_student, '#3498db'),
            ("Delete Student", self.delete_student, '#e74c3c'),
            ("Clear Fields", self.clear_fields, '#95a5a6')
        ]
        
        for i, (text, command, color) in enumerate(buttons):
            btn = tk.Button(btn_frame, text=text, command=command, 
                           font=('Arial', 9, 'bold'), bg=color, fg='white',
                           width=15, cursor='hand2', relief='raised', bd=2)
            btn.grid(row=0, column=i, padx=5)
        
        # Search Frame
        search_frame = tk.Frame(main_frame, bg='#f0f0f0')
        search_frame.pack(fill='x', pady=(0, 10))
        
        tk.Label(search_frame, text="Search:", font=('Arial', 10), 
                bg='#f0f0f0').pack(side='left', padx=(0, 10))
        self.search_entry = tk.Entry(search_frame, font=('Arial', 10), width=30)
        self.search_entry.pack(side='left', padx=(0, 10))
        self.search_entry.bind('<KeyRelease>', self.search_students)
        
        tk.Button(search_frame, text="Show All", command=self.display_students,
                 font=('Arial', 9), bg='#16a085', fg='white').pack(side='left')
        
        # Treeview Frame
        tree_frame = tk.Frame(main_frame, bg='#f0f0f0')
        tree_frame.pack(fill='both', expand=True)
        
        # Scrollbars
        tree_scroll_y = ttk.Scrollbar(tree_frame)
        tree_scroll_y.pack(side='right', fill='y')
        
        tree_scroll_x = ttk.Scrollbar(tree_frame, orient='horizontal')
        tree_scroll_x.pack(side='bottom', fill='x')
        
        # Treeview
        self.tree = ttk.Treeview(tree_frame, 
                                 columns=('ID', 'Name', 'Age', 'Grade', 'Major'),
                                 show='headings',
                                 yscrollcommand=tree_scroll_y.set,
                                 xscrollcommand=tree_scroll_x.set,
                                 height=12)
        
        tree_scroll_y.config(command=self.tree.yview)
        tree_scroll_x.config(command=self.tree.xview)
        
        # Define headings
        for col in ('ID', 'Name', 'Age', 'Grade', 'Major'):
            self.tree.heading(col, text=col, anchor='w')
            self.tree.column(col, width=120, anchor='w')
        
        self.tree.pack(fill='both', expand=True)
        self.tree.bind('<ButtonRelease-1>', self.on_tree_select)
        
        # Style configuration
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('Treeview', font=('Arial', 10), rowheight=25)
        style.configure('Treeview.Heading', font=('Arial', 10, 'bold'))
        
        self.display_students()
    
    def add_student(self):
        student = {
            'id': self.entries['id'].get().strip(),
            'name': self.entries['name'].get().strip(),
            'age': self.entries['age'].get().strip(),
            'grade': self.entries['grade'].get().strip(),
            'major': self.entries['major'].get().strip()
        }
        
        if not all(student.values()):
            messagebox.showwarning("Warning", "All fields are required!")
            return
        
        if any(s['id'] == student['id'] for s in self.students):
            messagebox.showerror("Error", "Student ID already exists!")
            return
        
        try:
            age_val = int(student['age'])
            if age_val < 0 or age_val > 150:
                messagebox.showerror("Error", "Age must be between 0 and 150!")
                return
        except ValueError:
            messagebox.showerror("Error", "Age must be a valid number!")
            return
        
        self.students.append(student)
        self.save_data()
        self.display_students()
        self.clear_fields()
        messagebox.showinfo("Success", "Student added successfully!")
    
    def update_student(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a student to update!")
            return
        
        student_id = self.entries['id'].get().strip()
        if not student_id:
            messagebox.showwarning("Warning", "Student ID is required!")
            return
        
        # Validate age
        age_str = self.entries['age'].get().strip()
        try:
            age_val = int(age_str)
            if age_val < 0 or age_val > 150:
                messagebox.showerror("Error", "Age must be between 0 and 150!")
                return
        except ValueError:
            messagebox.showerror("Error", "Age must be a valid number!")
            return
        
        for student in self.students:
            if student['id'] == student_id:
                student['name'] = self.entries['name'].get().strip()
                student['age'] = age_str
                student['grade'] = self.entries['grade'].get().strip()
                student['major'] = self.entries['major'].get().strip()
                
                self.save_data()
                self.display_students()
                self.clear_fields()
                messagebox.showinfo("Success", "Student updated successfully!")
                return
        
        messagebox.showerror("Error", "Student not found!")
    
    def delete_student(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a student to delete!")
            return
        
        # Get the student ID from the selected row
        item = self.tree.item(selected[0])
        student_id = str(item['values'][0])  # Convert to string for comparison
        
        # Confirm deletion
        if not messagebox.askyesno("Confirm", "Are you sure you want to delete this student?"):
            return
        
        # Find and remove the student
        initial_count = len(self.students)
        self.students = [s for s in self.students if str(s['id']) != student_id]
        
        # Check if deletion was successful
        if len(self.students) < initial_count:
            self.save_data()
            self.tree.delete(selected[0])  # Remove from tree immediately
            self.clear_fields()  # Clear the input fields
            self.display_students()  # Refresh the entire display
            messagebox.showinfo("Success", "Student deleted successfully!")
        else:
            messagebox.showerror("Error", "Failed to delete student!")
    
    def clear_fields(self):
        for entry in self.entries.values():
            entry.delete(0, tk.END)
        # Also clear any selection in the tree
        for item in self.tree.selection():
            self.tree.selection_remove(item)
    
    def on_tree_select(self, event):
        selected = self.tree.selection()
        if selected:
            item = self.tree.item(selected[0])
            values = item['values']
            
            self.entries['id'].delete(0, tk.END)
            self.entries['id'].insert(0, values[0])
            self.entries['name'].delete(0, tk.END)
            self.entries['name'].insert(0, values[1])
            self.entries['age'].delete(0, tk.END)
            self.entries['age'].insert(0, values[2])
            self.entries['grade'].delete(0, tk.END)
            self.entries['grade'].insert(0, values[3])
            self.entries['major'].delete(0, tk.END)
            self.entries['major'].insert(0, values[4])
    
    def display_students(self):
        # Clear search box when displaying all students
        if hasattr(self, 'search_entry'):
            current_search = self.search_entry.get()
            if not current_search:  # Only refresh if not searching
                self.tree.delete(*self.tree.get_children())
                for student in self.students:
                    self.tree.insert('', 'end', values=(
                        student['id'], student['name'], student['age'], 
                        student['grade'], student['major']
                    ))
        else:
            self.tree.delete(*self.tree.get_children())
            for student in self.students:
                self.tree.insert('', 'end', values=(
                    student['id'], student['name'], student['age'], 
                    student['grade'], student['major']
                ))
    
    def search_students(self, event=None):
        query = self.search_entry.get().lower()
        self.tree.delete(*self.tree.get_children())
        
        for student in self.students:
            if any(query in str(v).lower() for v in student.values()):
                self.tree.insert('', 'end', values=(
                    student['id'], student['name'], student['age'], 
                    student['grade'], student['major']
                ))
    
    def save_data(self):
        try:
            with open('students.json', 'w') as f:
                json.dump(self.students, f, indent=2)
            print(f"Data saved: {len(self.students)} students")  # Debug output
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save data: {str(e)}")
    
    def load_data(self):
        if os.path.exists('students.json'):
            try:
                with open('students.json', 'r') as f:
                    self.students = json.load(f)
                print(f"Data loaded: {len(self.students)} students")  # Debug output
            except json.JSONDecodeError:
                self.students = []
                messagebox.showwarning("Warning", "Could not load students.json. Starting with empty database.")
            except Exception as e:
                self.students = []
                messagebox.showerror("Error", f"Error loading data: {str(e)}")
        else:
            self.students = []


if _name_ == "_main_":
    root = tk.Tk()
    app = StudentRecordSystem(root)
    root.mainloop()
