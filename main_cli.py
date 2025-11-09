"""
ML Debugging Expert System - Main CLI Interface
Interactive command-line interface for the hybrid expert system
"""

import sys
from ml_debugging_expert import run_diagnosis
from gemini_integration import GeminiIntegration
import json

class MLDebugCLI:
    """Command-line interface for ML debugging"""
    
    def __init__(self, api_key):
        self.gemini = GeminiIntegration(api_key)
        self.mode = None
    
    def print_header(self):
        """Print welcome header"""
        print("\n" + "=" * 70)
        print("🤖 ML MODEL DEBUGGING EXPERT SYSTEM 🤖")
        print("Hybrid AI: Expert System + Gemini LLM")
        print("=" * 70)
    
    def show_menu(self):
        """Display main menu"""
        print("\n📋 Choose interaction mode:")
        print("1. Natural Language Mode (describe your problem)")
        print("2. Structured Input Mode (provide exact metrics)")
        print("3. Conversational Mode (interactive Q&A)")
        print("4. Exit")
        print("-" * 70)
    
    def natural_language_mode(self):
        """Handle natural language queries"""
        print("\n🗣️  NATURAL LANGUAGE MODE")
        print("-" * 70)
        print("Describe your ML training issue in plain English.")
        print("Example: 'My model gets 95% train accuracy but 70% test accuracy'\n")
        
        query = input("Your question: ").strip()
        
        if not query:
            print("❌ No input provided.")
            return
        
        print("\n⏳ Extracting metrics from your query...")
        metrics = self.gemini.extract_metrics(query)
        
        if not metrics:
            print("❌ Could not extract metrics. Please try again with more details.")
            return
        
        print(f"✅ Extracted metrics: {json.dumps(metrics, indent=2)}")
        
        print("\n⏳ Running expert system diagnosis...")
        results = run_diagnosis(metrics)
        
        print("\n" + "=" * 70)
        print("🔍 EXPERT SYSTEM DIAGNOSIS")
        print("=" * 70)
        for diagnosis in results["diagnoses"]:
            print(f"• {diagnosis}")
        
        print("\n⏳ Generating friendly explanation...")
        explanation = self.gemini.generate_explanation(results, query)
        
        print("\n" + "=" * 70)
        print("💡 EXPLANATION & RECOMMENDATIONS")
        print("=" * 70)
        print(explanation)
        print("=" * 70)
    
    def structured_mode(self):
        """Handle structured metric input"""
        print("\n📊 STRUCTURED INPUT MODE")
        print("-" * 70)
        print("Enter metrics (press Enter to skip optional fields):\n")
        
        metrics = {}
        
        try:
            ta = input("Training accuracy (0-100): ").strip()
            if ta:
                metrics["train_accuracy"] = float(ta)
            
            tea = input("Test accuracy (0-100): ").strip()
            if tea:
                metrics["test_accuracy"] = float(tea)
            
            ds = input("Dataset size (number of samples): ").strip()
            if ds:
                metrics["dataset_size"] = int(ds)
            
            bs = input("Batch size: ").strip()
            if bs:
                metrics["batch_size"] = int(bs)
            
            loss_osc = input("Loss oscillation (high/medium/low): ").strip().lower()
            if loss_osc in ["high", "medium", "low"]:
                metrics["loss_oscillation"] = loss_osc
            
            conv_speed = input("Convergence speed (very_slow/slow/normal/fast): ").strip().lower()
            if conv_speed in ["very_slow", "slow", "normal", "fast"]:
                metrics["convergence_speed"] = conv_speed
            
        except ValueError:
            print("❌ Invalid input. Please enter numbers for numeric fields.")
            return
        
        if not metrics:
            print("❌ No metrics provided.")
            return
        
        print("\n⏳ Running diagnosis...")
        results = run_diagnosis(metrics)
        
        print("\n" + "=" * 70)
        print("🔍 DIAGNOSIS RESULTS")
        print("=" * 70)
        
        for diagnosis in results["diagnoses"]:
            print(f"\n• {diagnosis}")
        
        print("\n📋 RECOMMENDATIONS:")
        for i, rec in enumerate(results["recommendations"], 1):
            print(f"{i}. {rec}")
        
        print("=" * 70)
    
    def conversational_mode(self):
        """Handle conversational interaction"""
        print("\n💬 CONVERSATIONAL MODE")
        print("-" * 70)
        print("Chat with the system to diagnose your issue.")
        print("Type 'done' when you've provided all information.\n")
        
        context = ""
        conversation = []
        
        while True:
            user_input = input("You: ").strip()
            
            if user_input.lower() == 'done':
                print("\n⏳ Analyzing conversation for diagnosis...")
                
                # Combine conversation
                full_context = " ".join([msg for msg in conversation])
                metrics = self.gemini.extract_metrics(full_context)
                
                if metrics:
                    results = run_diagnosis(metrics)
                    print("\n" + "=" * 70)
                    print("🔍 FINAL DIAGNOSIS")
                    print("=" * 70)
                    for diagnosis in results["diagnoses"]:
                        print(f"• {diagnosis}")
                    
                    print("\n📋 RECOMMENDATIONS:")
                    for i, rec in enumerate(results["recommendations"], 1):
                        print(f"{i}. {rec}")
                    print("=" * 70)
                else:
                    print("❌ Not enough information gathered for diagnosis.")
                break
            
            conversation.append(user_input)
            response = self.gemini.conversational_query(user_input, context)
            print(f"\nAssistant: {response}\n")
            
            context += f"\nUser: {user_input}\nAssistant: {response}"
    
    def run(self):
        """Main execution loop"""
        self.print_header()
        
        while True:
            self.show_menu()
            choice = input("\nEnter your choice (1-4): ").strip()
            
            if choice == "1":
                self.natural_language_mode()
            elif choice == "2":
                self.structured_mode()
            elif choice == "3":
                self.conversational_mode()
            elif choice == "4":
                print("\n👋 Thank you for using ML Debugging Expert System!")
                print("=" * 70)
                sys.exit(0)
            else:
                print("❌ Invalid choice. Please enter 1-4.")
            
            input("\nPress Enter to continue...")


if __name__ == "__main__":
    print("\n🔑 Enter your Gemini API key:")
    api_key = input("API Key: ").strip()
    
    if not api_key:
        print("❌ API key required. Get one from: https://makersuite.google.com/app/apikey")
        sys.exit(1)
    
    cli = MLDebugCLI(api_key)
    cli.run()