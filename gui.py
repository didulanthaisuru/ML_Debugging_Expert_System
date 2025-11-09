"""
ML Debugging Expert System - Simple GUI
Tkinter-based graphical interface for easy demonstration
"""

try:
    import tkinter as tk
    from tkinter import ttk, scrolledtext, messagebox
except ImportError as e:
    print("=" * 70)
    print("❌ GUI Error: tkinter is not available")
    print("=" * 70)
    print("\ntkinter is not installed in your Python environment.")
    print("\nTo fix this on macOS:")
    print("  brew install python-tk@3.11")
    print("\nOr use the command-line interface instead:")
    print("  python main_cli.py")
    print("=" * 70)
    import sys
    sys.exit(1)

from ml_debugging_expert import run_diagnosis
from gemini_integration import GeminiIntegration
import threading
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class MLDebugGUI:
    """Simple GUI for ML debugging expert system"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("🤖 ML Debugging Expert System")
        self.root.geometry("950x750")
        self.root.configure(bg="#f8fafc")
        
        self.gemini = None
        self.api_key = None
        
        # Modern Color Palette - accessible throughout the class
        self.colors = {
            'primary': '#2563eb',      # Modern blue
            'success': '#10b981',      # Modern green
            'danger': '#ef4444',       # Modern red
            'warning': '#f59e0b',      # Modern orange
            'dark': '#1e293b',         # Dark slate
            'light': '#f8fafc',        # Light background
            'text': '#334155',         # Text color
            'border': '#e2e8f0'        # Border color
        }
        
        # Try to load API key from environment
        self.env_api_key = (
            os.getenv("GEMINI_API_KEY")
            or os.getenv("GOOGLE_API_KEY")
            or os.getenv("API_KEY")
        )
        
        self.setup_ui()
        
        # Auto-connect if API key is in environment
        if self.env_api_key:
            self.api_entry.insert(0, "●" * 20 + " (from .env)")
            self.api_entry.config(state='disabled')
            self.connect_api()
    
    def setup_ui(self):
        """Setup the user interface"""
        
        # Title Frame - Modern gradient-like effect
        title_frame = tk.Frame(self.root, bg=self.colors['dark'], height=100)
        title_frame.pack(fill=tk.X, pady=0)
        
        title_label = tk.Label(
            title_frame,
            text="🤖 ML Model Debugging Expert System",
            font=("Helvetica", 22, "bold"),
            bg=self.colors['dark'],
            fg="white"
        )
        title_label.pack(pady=(25, 5))
        
        subtitle_label = tk.Label(
            title_frame,
            text="Hybrid AI: Expert System + Gemini LLM",
            font=("Helvetica", 12),
            bg=self.colors['dark'],
            fg="#94a3b8"
        )
        subtitle_label.pack(pady=(0, 20))
        
        # Main container
        main_frame = tk.Frame(self.root, bg=self.colors['light'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=25, pady=25)
        
        # API Connection Frame - Clean card design
        api_frame = tk.LabelFrame(
            main_frame,
            text=" 🔑 Gemini API Connection ",
            font=("Helvetica", 12, "bold"),
            bg="white",
            fg=self.colors['text'],
            relief=tk.FLAT,
            bd=2
        )
        api_frame.pack(fill=tk.X, pady=(0, 20), ipady=10, ipadx=10)
        
        tk.Label(
            api_frame,
            text="API Key:",
            font=("Helvetica", 11),
            bg="white",
            fg=self.colors['text'],
            anchor=tk.W
        ).grid(row=0, column=0, sticky=tk.W, padx=10, pady=5)
        
        self.api_entry = tk.Entry(
            api_frame,
            width=50,
            font=("Helvetica", 10),
            relief=tk.SOLID,
            bd=1,
            show="*"
        )
        self.api_entry.grid(row=0, column=1, padx=10, pady=5)
        
        self.connect_btn = tk.Button(
            api_frame,
            text="🔌 Connect API",
            command=self.connect_api,
            font=("Helvetica", 11, "bold"),
            bg=self.colors['success'],
            fg="white",
            relief=tk.FLAT,
            cursor="hand2",
            padx=20,
            pady=8
        )
        self.connect_btn.grid(row=0, column=2, padx=10, pady=5)
        
        self.api_status = tk.Label(
            api_frame,
            text="⚠️ Not Connected",
            font=("Helvetica", 10),
            bg="white",
            fg=self.colors['danger']
        )
        self.api_status.grid(row=1, column=0, columnspan=3, pady=5)
        
        # Mode Selection - Modern card style
        mode_frame = tk.LabelFrame(
            main_frame,
            text="📋 Select Input Mode",
            font=("Helvetica", 12, "bold"),
            bg="white",
            fg=self.colors['text'],
            relief=tk.FLAT,
            borderwidth=2,
            padx=15,
            pady=15
        )
        mode_frame.pack(fill=tk.X, pady=(0, 20))
        
        self.mode_var = tk.StringVar(value="natural")
        
        tk.Radiobutton(
            mode_frame,
            text="🗣️  Natural Language (Describe your problem)",
            variable=self.mode_var,
            value="natural",
            bg="white",
            fg=self.colors['text'],
            font=("Helvetica", 11),
            activebackground="white",
            selectcolor=self.colors['primary'],
            command=self.switch_mode
        ).pack(anchor="w", pady=5)
        
        tk.Radiobutton(
            mode_frame,
            text="📊 Structured Input (Enter exact metrics)",
            variable=self.mode_var,
            value="structured",
            bg="white",
            fg=self.colors['text'],
            font=("Helvetica", 11),
            activebackground="white",
            selectcolor=self.colors['primary'],
            command=self.switch_mode
        ).pack(anchor="w", pady=5)
        
        # Input Frame (switchable) - Modern card style
        self.input_frame = tk.LabelFrame(
            main_frame,
            text="📝 Input",
            font=("Helvetica", 12, "bold"),
            bg="white",
            fg=self.colors['text'],
            relief=tk.FLAT,
            borderwidth=2,
            padx=15,
            pady=15
        )
        self.input_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        # Natural Language Input
        self.natural_frame = tk.Frame(self.input_frame, bg="white")
        
        tk.Label(
            self.natural_frame,
            text="Describe your ML training issue:",
            bg="white",
            fg=self.colors['text'],
            font=("Helvetica", 11, "bold")
        ).pack(anchor="w", pady=(0, 8))
        
        self.natural_text = scrolledtext.ScrolledText(
            self.natural_frame,
            height=6,
            font=("Helvetica", 11),
            wrap=tk.WORD,
            relief=tk.SOLID,
            borderwidth=1,
            padx=10,
            pady=10
        )
        self.natural_text.pack(fill=tk.BOTH, expand=True)
        self.natural_text.insert("1.0", "Example: My model gets 92% train accuracy but only 68% test accuracy")
        
        # Structured Input
        self.structured_frame = tk.Frame(self.input_frame, bg="white")
        
        metrics = [
            ("Training Accuracy (%):", "train_acc"),
            ("Test Accuracy (%):", "test_acc"),
            ("Dataset Size:", "dataset_size"),
            ("Batch Size:", "batch_size"),
        ]
        
        self.metric_entries = {}
        for i, (label, key) in enumerate(metrics):
            tk.Label(
                self.structured_frame, 
                text=label, 
                bg="white",
                fg=self.colors['text'],
                font=("Helvetica", 11)
            ).grid(row=i, column=0, sticky="w", padx=5, pady=8)
            
            entry = tk.Entry(
                self.structured_frame, 
                width=25, 
                font=("Helvetica", 11),
                relief=tk.SOLID,
                borderwidth=1
            )
            entry.grid(row=i, column=1, padx=10, pady=8, sticky="w")
            self.metric_entries[key] = entry
        
        # Loss Oscillation
        tk.Label(
            self.structured_frame, 
            text="Loss Oscillation:", 
            bg="white",
            fg=self.colors['text'],
            font=("Helvetica", 11)
        ).grid(row=4, column=0, sticky="w", padx=5, pady=8)
        
        self.loss_var = tk.StringVar(value="none")
        loss_combo = ttk.Combobox(
            self.structured_frame,
            textvariable=self.loss_var,
            values=["none", "high", "medium", "low"],
            width=23,
            font=("Helvetica", 11),
            state="readonly"
        )
        loss_combo.grid(row=4, column=1, padx=10, pady=8, sticky="w")
        
        # Convergence Speed
        tk.Label(
            self.structured_frame, 
            text="Convergence Speed:", 
            bg="white",
            fg=self.colors['text'],
            font=("Helvetica", 11)
        ).grid(row=5, column=0, sticky="w", padx=5, pady=8)
        
        self.conv_var = tk.StringVar(value="normal")
        conv_combo = ttk.Combobox(
            self.structured_frame,
            textvariable=self.conv_var,
            values=["very_slow", "slow", "normal", "fast"],
            width=23,
            font=("Helvetica", 11),
            state="readonly"
        )
        conv_combo.grid(row=5, column=1, padx=10, pady=8, sticky="w")
        
        # Show natural language by default
        self.natural_frame.pack(fill=tk.BOTH, expand=True)
        
        # Diagnose Button - Large, modern, attention-grabbing
        self.diagnose_btn = tk.Button(
            main_frame,
            text="🔍 Diagnose Issue",
            command=self.diagnose,
            bg=self.colors['primary'],
            fg="white",
            font=("Helvetica", 14, "bold"),
            cursor="hand2",
            height=2,
            relief=tk.FLAT,
            borderwidth=0,
            state=tk.DISABLED
        )
        self.diagnose_btn.pack(fill=tk.X, pady=(0, 20))
        
        # Output Frame - Modern card style
        output_frame = tk.LabelFrame(
            main_frame,
            text="💡 Diagnosis & Recommendations",
            font=("Helvetica", 12, "bold"),
            bg="white",
            fg=self.colors['text'],
            relief=tk.FLAT,
            borderwidth=2,
            padx=15,
            pady=15
        )
        output_frame.pack(fill=tk.BOTH, expand=True)
        
        self.output_text = scrolledtext.ScrolledText(
            output_frame,
            height=20,
            font=("Helvetica", 11),
            wrap=tk.WORD,
            bg="#fafafa",
            fg=self.colors['text'],
            relief=tk.SOLID,
            borderwidth=1,
            padx=12,
            pady=12
        )
        self.output_text.pack(fill=tk.BOTH, expand=True)
        self.output_text.insert("1.0", "👆 Connect to API and describe your issue to get started!\n\nThe system will analyze your ML training problem and provide:\n  • Expert system diagnosis\n  • Detailed recommendations\n  • Friendly AI-generated explanations")
        self.output_text.config(state=tk.DISABLED)
    
    def switch_mode(self):
        """Switch between natural language and structured input"""
        mode = self.mode_var.get()
        
        # Hide both frames
        self.natural_frame.pack_forget()
        self.structured_frame.pack_forget()
        
        # Show selected frame
        if mode == "natural":
            self.natural_frame.pack(fill=tk.BOTH, expand=True)
        else:
            self.structured_frame.pack(fill=tk.BOTH, expand=True)
    
    def connect_api(self):
        """Connect to Gemini API"""
        # Use environment key if available, otherwise get from entry field
        if self.env_api_key:
            api_key = self.env_api_key
        else:
            api_key = self.api_entry.get().strip()
        
        if not api_key:
            messagebox.showerror("Error", "Please enter your Gemini API key!")
            return
        
        try:
            self.gemini = GeminiIntegration(api_key)
            self.api_key = api_key
            self.api_status.config(text="✅ Connected", fg=self.colors['success'])
            self.connect_btn.config(state=tk.DISABLED, bg="#6b7280")
            self.diagnose_btn.config(state=tk.NORMAL, bg=self.colors['primary'])
            
            # Only show success message if manually connected
            if not self.env_api_key:
                messagebox.showinfo("Success", "Connected to Gemini API successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to connect: {str(e)}")
    
    def diagnose(self):
        """Run diagnosis based on selected mode"""
        if not self.gemini:
            messagebox.showerror("Error", "Please connect to Gemini API first!")
            return
        
        mode = self.mode_var.get()
        
        # Disable button during processing
        self.diagnose_btn.config(state=tk.DISABLED, text="⏳ Processing...")
        self.output_text.config(state=tk.NORMAL)
        self.output_text.delete("1.0", tk.END)
        self.output_text.insert("1.0", "⏳ Analyzing your issue...\n\n")
        self.output_text.config(state=tk.DISABLED)
        
        # Run diagnosis in separate thread to avoid freezing
        if mode == "natural":
            thread = threading.Thread(target=self.diagnose_natural)
        else:
            thread = threading.Thread(target=self.diagnose_structured)
        
        thread.daemon = True
        thread.start()
    
    def diagnose_natural(self):
        """Diagnose using natural language input"""
        try:
            query = self.natural_text.get("1.0", tk.END).strip()
            
            if not query or query.startswith("Example:"):
                self.show_error("Please describe your ML training issue!")
                return
            
            # Extract metrics
            metrics = self.gemini.extract_metrics(query)
            
            if not metrics:
                self.show_error("Could not extract metrics from your description. Please provide more details!")
                return
            
            # Run expert system
            results = run_diagnosis(metrics)
            
            # Generate explanation
            explanation = self.gemini.generate_explanation(results, query)
            
            # Display results
            self.display_results(results, explanation, metrics)
            
        except Exception as e:
            self.show_error(f"Error during diagnosis: {str(e)}")
    
    def diagnose_structured(self):
        """Diagnose using structured input"""
        try:
            metrics = {}
            
            # Get numeric values
            if self.metric_entries["train_acc"].get().strip():
                metrics["train_accuracy"] = float(self.metric_entries["train_acc"].get())
            
            if self.metric_entries["test_acc"].get().strip():
                metrics["test_accuracy"] = float(self.metric_entries["test_acc"].get())
            
            if self.metric_entries["dataset_size"].get().strip():
                metrics["dataset_size"] = int(self.metric_entries["dataset_size"].get())
            
            if self.metric_entries["batch_size"].get().strip():
                metrics["batch_size"] = int(self.metric_entries["batch_size"].get())
            
            # Get dropdown values
            if self.loss_var.get() != "none":
                metrics["loss_oscillation"] = self.loss_var.get()
            
            if self.conv_var.get() != "normal":
                metrics["convergence_speed"] = self.conv_var.get()
            
            if not metrics:
                self.show_error("Please enter at least some metrics!")
                return
            
            # Run expert system
            results = run_diagnosis(metrics)
            
            # Display results (no LLM explanation for structured mode)
            self.display_results(results, None, metrics)
            
        except ValueError:
            self.show_error("Please enter valid numbers for numeric fields!")
        except Exception as e:
            self.show_error(f"Error during diagnosis: {str(e)}")
    
    def display_results(self, results, explanation, metrics):
        """Display diagnosis results"""
        output = "=" * 60 + "\n"
        output += "📊 EXTRACTED METRICS\n"
        output += "=" * 60 + "\n"
        for key, value in metrics.items():
            output += f"  • {key}: {value}\n"
        
        output += "\n" + "=" * 60 + "\n"
        output += "🔍 EXPERT SYSTEM DIAGNOSIS\n"
        output += "=" * 60 + "\n"
        
        if results["diagnoses"]:
            for diagnosis in results["diagnoses"]:
                output += f"\n{diagnosis}\n"
        else:
            output += "\n⚠️ No specific issues detected with provided metrics.\n"
        
        output += "\n" + "=" * 60 + "\n"
        output += "📋 RECOMMENDATIONS\n"
        output += "=" * 60 + "\n"
        
        for i, rec in enumerate(results["recommendations"], 1):
            output += f"\n{i}. {rec}\n"
        
        if explanation:
            output += "\n" + "=" * 60 + "\n"
            output += "💡 FRIENDLY EXPLANATION\n"
            output += "=" * 60 + "\n"
            output += f"\n{explanation}\n"
        
        output += "\n" + "=" * 60 + "\n"
        
        self.root.after(0, lambda: self.update_output(output))
    
    def update_output(self, text):
        """Update output text (thread-safe)"""
        self.output_text.config(state=tk.NORMAL)
        self.output_text.delete("1.0", tk.END)
        self.output_text.insert("1.0", text)
        self.output_text.config(state=tk.DISABLED)
        self.diagnose_btn.config(state=tk.NORMAL, text="🔍 Diagnose Issue")
    
    def show_error(self, message):
        """Show error message (thread-safe)"""
        self.root.after(0, lambda: messagebox.showerror("Error", message))
        self.root.after(0, lambda: self.diagnose_btn.config(state=tk.NORMAL, text="🔍 Diagnose Issue"))


def main():
    """Main entry point"""
    root = tk.Tk()
    app = MLDebugGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()