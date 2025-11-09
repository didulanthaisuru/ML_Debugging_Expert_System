"""
Gemini API Integration for ML Debugging Expert System
Handles natural language queries and generates friendly explanations
"""

import google.generativeai as genai
import re
import json

class GeminiIntegration:
    """Integration with Gemini API for NL processing"""
    
    def __init__(self, api_key):
        """Initialize Gemini API"""
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-pro')
    
    def extract_metrics(self, user_query):
        """
        Extract ML metrics from natural language query
        
        Args:
            user_query (str): User's natural language question
            
        Returns:
            dict: Extracted metrics
        """
        prompt = f"""
You are an expert at extracting ML training metrics from natural language descriptions.

User Query: "{user_query}"

Extract the following metrics if mentioned (return null if not mentioned):
- train_accuracy (percentage, 0-100)
- test_accuracy (percentage, 0-100) 
- validation_accuracy (percentage, 0-100)
- loss_oscillation ("high", "medium", "low", or null)
- convergence_speed ("very_slow", "slow", "normal", "fast", or null)
- dataset_size (number of samples)
- batch_size (number)
- learning_rate (decimal number)
- epochs (number)

Return ONLY a valid JSON object with these fields. Use null for missing values.
Example: {{"train_accuracy": 95, "test_accuracy": 70, "dataset_size": null, "batch_size": null}}
"""
        
        try:
            response = self.model.generate_content(prompt)
            text = response.text.strip()
            
            # Extract JSON from response (handle markdown code blocks)
            json_match = re.search(r'\{[^}]+\}', text, re.DOTALL)
            if json_match:
                metrics = json.loads(json_match.group())
                # Remove null values
                return {k: v for k, v in metrics.items() if v is not None}
            else:
                return {}
        except Exception as e:
            print(f"Error extracting metrics: {e}")
            return {}
    
    def generate_explanation(self, diagnosis_results, user_query):
        """
        Generate friendly explanation from expert system diagnosis
        
        Args:
            diagnosis_results (dict): Results from expert system
            user_query (str): Original user query
            
        Returns:
            str: Friendly explanation
        """
        diagnoses = "\n".join(diagnosis_results.get("diagnoses", []))
        recommendations = "\n".join([f"- {r}" for r in diagnosis_results.get("recommendations", [])])
        
        prompt = f"""
You are a friendly ML debugging assistant helping a student understand their model's issues.

Original Question: "{user_query}"

Expert System Diagnosis:
{diagnoses}

Recommendations:
{recommendations}

Provide a clear, friendly, and educational explanation that:
1. Summarizes the main problem in simple terms
2. Explains WHY this is happening
3. Gives actionable next steps
4. Includes a brief code example if relevant

Keep it concise (2-3 paragraphs) and encouraging.
"""
        
        try:
            response = self.model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            return f"Error generating explanation: {e}"
    
    def conversational_query(self, user_message, context=None):
        """
        Handle conversational queries for clarification
        
        Args:
            user_message (str): User's message
            context (str): Previous conversation context
            
        Returns:
            str: Response
        """
        context_text = f"\n\nPrevious context:\n{context}" if context else ""
        
        prompt = f"""
You are an ML debugging assistant. The user is describing their model training issue.

User: "{user_message}"{context_text}

If the user hasn't provided enough information to diagnose the issue, ask ONE specific clarifying question about:
- Training accuracy
- Test/validation accuracy  
- Dataset size
- Loss behavior (oscillating, plateauing, etc.)
- Other relevant metrics

If they've provided enough info, acknowledge and prepare to diagnose.
Keep your response brief and friendly.
"""
        
        try:
            response = self.model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            return f"Error in conversation: {e}"


# Example usage
if __name__ == "__main__":
    # NOTE: Replace with your actual Gemini API key
    API_KEY = "YOUR_GEMINI_API_KEY_HERE"
    
    gemini = GeminiIntegration(API_KEY)
    
    # Test metric extraction
    print("=" * 60)
    print("TEST: Metric Extraction")
    print("=" * 60)
    query = "My model gets 92% accuracy on training but only 68% on test set"
    metrics = gemini.extract_metrics(query)
    print(f"Query: {query}")
    print(f"Extracted metrics: {json.dumps(metrics, indent=2)}")
    
    # Test explanation generation
    print("\n" + "=" * 60)
    print("TEST: Explanation Generation")
    print("=" * 60)
    sample_diagnosis = {
        "diagnoses": ["OVERFITTING DETECTED: Train accuracy (92%) significantly higher than test accuracy (68%)"],
        "recommendations": [
            "Add regularization (L1/L2)",
            "Increase dropout rate (try 0.3-0.5)",
            "Use data augmentation"
        ]
    }
    explanation = gemini.generate_explanation(sample_diagnosis, query)
    print(explanation)