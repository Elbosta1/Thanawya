import customtkinter as ctk
from tkinter import messagebox
import pandas as pd
import threading
import sys
import os

ctk.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

class PremiumResultApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("البحث في نتيجة الثانوية العامة")
        self.geometry("700x600")
        
        self.df = None
        
        # Fonts
        self.title_font = ctk.CTkFont(family="Arial", size=24, weight="bold")
        self.normal_font = ctk.CTkFont(family="Arial", size=18)
        
        # Title Label
        self.lbl_title = ctk.CTkLabel(self, text="نظام الاستعلام عن نتيجة الثانوية العامة", font=self.title_font, text_color="#00ffcc")
        self.lbl_title.pack(pady=(20, 10))
        
        # Status Label
        self.lbl_status = ctk.CTkLabel(self, text="جاري تحميل البيانات، يرجى الانتظار قد يستغرق بعض الوقت...", font=self.normal_font, text_color="orange")
        self.lbl_status.pack(pady=(0, 20))
        
        # Search Frame
        self.frame_search = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_search.pack(fill="x", padx=40, pady=10)
        
        # Search Button (left side in RTL effect)
        self.btn_search = ctk.CTkButton(self.frame_search, text="بحث", font=self.normal_font, command=self.search, state="disabled", corner_radius=8, width=100, height=40)
        self.btn_search.pack(side="left", padx=10)
        
        # Entry (right side)
        self.entry_search = ctk.CTkEntry(self.frame_search, font=self.normal_font, placeholder_text="أدخل اسم الطالب أو رقم الجلوس هنا...", justify="right", height=40)
        self.entry_search.pack(side="left", fill="x", expand=True)
        self.entry_search.bind('<Return>', lambda event: self.search())
        
        # Results Textbox
        self.text_result = ctk.CTkTextbox(self, font=self.normal_font, corner_radius=10, border_width=1, border_color="#333333")
        self.text_result.pack(fill="both", expand=True, padx=40, pady=(10, 30))
        self.text_result.tag_config('right', justify='right')
        
        # Start loading data in a separate thread
        threading.Thread(target=self.load_data, daemon=True).start()

    def load_data(self):
        try:
            file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "نتيجة ثانوية عامة نظام حديث.xlsx")
            self.df = pd.read_excel(file_path)
            self.after(0, self.on_data_loaded)
        except Exception as e:
            self.after(0, lambda: self.lbl_status.configure(text=f"خطأ في التحميل: {str(e)}", text_color="red"))

    def on_data_loaded(self):
        self.lbl_status.configure(text="تم تحميل البيانات بنجاح. يمكنك الآن البحث.", text_color="#00ff00")
        self.btn_search.configure(state="normal")

    def search(self):
        if self.df is None:
            return
            
        query = self.entry_search.get().strip()
        if not query:
            messagebox.showwarning("تنبيه", "يرجى إدخال اسم أو رقم جلوس للبحث")
            return
            
        self.text_result.delete("1.0", "end")
        self.text_result.insert("end", f"جاري البحث عن: {query}...\n\n", 'right')
        
        # Clean seating_no to string without decimal '.0'
        seating_str = self.df['seating_no'].fillna('').astype(str).str.replace(r'\.0$', '', regex=True)
        name_str = self.df['arabic_name'].fillna('').astype(str)
        
        if query.isdigit():
            # Exact match for seating number
            mask = seating_str == query
        else:
            # Partial match for name
            mask = name_str.str.contains(query, na=False, regex=False)
            
        results = self.df[mask]
        
        self.text_result.delete("1.0", "end")
        
        if results.empty:
            self.text_result.insert("end", "لم يتم العثور على طالب بهذا الاسم أو رقم الجلوس.\n", 'right')
        else:
            self.text_result.insert("end", f"تم العثور على {len(results)} نتيجة:\n\n", 'right')
            for index, row in results.iterrows():
                res_text = (
                    f"الاسم: {row.get('arabic_name', 'غير متوفر')}\n"
                    f"رقم الجلوس: {row.get('seating_no', 'غير متوفر')}\n"
                    f"المجموع: {row.get('total_degree', 'غير متوفر')}\n"
                    f"حالة الطالب: {row.get('student_case_desc', 'غير متوفر')}\n"
                    f"{'-'*60}\n"
                )
                self.text_result.insert("end", res_text, 'right')

if __name__ == "__main__":
    app = PremiumResultApp()
    app.mainloop()
