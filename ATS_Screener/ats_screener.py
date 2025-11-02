#!/usr/bin/env python3
"""
ATS (Applicant Tracking System) Screener
A single-file application to screen resumes against job descriptions using keyword matching.
"""

import tkinter as tk
from tkinter import scrolledtext, messagebox, ttk
import re
from collections import Counter


class ATSScreener:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("ATS Resume Screener")
        self.window.geometry("900x700")
        self.setup_ui()
    
    def setup_ui(self):
        # Title
        title_label = tk.Label(
            self.window, 
            text="ATS Resume Screener",
            font=("Arial", 18, "bold"),
            pady=10
        )
        title_label.pack()
        
        # Main frame
        main_frame = tk.Frame(self.window, padx=20, pady=10)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Job Description Section
        jd_label = tk.Label(
            main_frame,
            text="Job Description:",
            font=("Arial", 12, "bold")
        )
        jd_label.pack(anchor=tk.W, pady=(0, 5))
        
        self.jd_text = scrolledtext.ScrolledText(
            main_frame,
            height=8,
            width=80,
            font=("Arial", 10),
            wrap=tk.WORD
        )
        self.jd_text.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Resume Section
        resume_label = tk.Label(
            main_frame,
            text="Resume/CV:",
            font=("Arial", 12, "bold")
        )
        resume_label.pack(anchor=tk.W, pady=(0, 5))
        
        self.resume_text = scrolledtext.ScrolledText(
            main_frame,
            height=8,
            width=80,
            font=("Arial", 10),
            wrap=tk.WORD
        )
        self.resume_text.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Button Frame
        button_frame = tk.Frame(main_frame)
        button_frame.pack(pady=10)
        
        # Analyze Button
        analyze_btn = tk.Button(
            button_frame,
            text="Analyze Match",
            command=self.analyze_match,
            font=("Arial", 12, "bold"),
            bg="#4CAF50",
            fg="white",
            padx=20,
            pady=10
        )
        analyze_btn.pack(side=tk.LEFT, padx=5)
        
        # Clear Button
        clear_btn = tk.Button(
            button_frame,
            text="Clear All",
            command=self.clear_all,
            font=("Arial", 12),
            bg="#f44336",
            fg="white",
            padx=20,
            pady=10
        )
        clear_btn.pack(side=tk.LEFT, padx=5)
        
        # Results Section
        results_label = tk.Label(
            main_frame,
            text="Analysis Results:",
            font=("Arial", 12, "bold")
        )
        results_label.pack(anchor=tk.W, pady=(10, 5))
        
        self.results_text = scrolledtext.ScrolledText(
            main_frame,
            height=10,
            width=80,
            font=("Arial", 10),
            wrap=tk.WORD,
            state=tk.DISABLED
        )
        self.results_text.pack(fill=tk.BOTH, expand=True)
    
    def extract_keywords(self, text):
        """Extract meaningful keywords from text."""
        # Convert to lowercase
        text = text.lower()
        
        # Remove special characters but keep spaces
        text = re.sub(r'[^a-z0-9\s+#]', ' ', text)
        
        # Common stop words to ignore
        stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
            'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'were', 'been',
            'be', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would',
            'should', 'could', 'may', 'might', 'must', 'can', 'this', 'that',
            'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they',
            'what', 'which', 'who', 'when', 'where', 'why', 'how', 'all', 'each',
            'every', 'both', 'few', 'more', 'most', 'other', 'some', 'such', 'no',
            'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very'
        }
        
        # Extract words (including compound terms like "machine learning")
        words = text.split()
        
        # Filter out stop words and short words
        keywords = []
        for word in words:
            if len(word) > 2 and word not in stop_words:
                keywords.append(word)
        
        # Also look for multi-word phrases (bigrams)
        phrases = []
        for i in range(len(words) - 1):
            if words[i] not in stop_words or words[i+1] not in stop_words:
                phrase = f"{words[i]} {words[i+1]}"
                if len(phrase) > 5:  # Reasonable phrase length
                    phrases.append(phrase)
        
        return keywords, phrases
    
    def calculate_match_score(self, jd_keywords, resume_keywords, jd_phrases, resume_phrases):
        """Calculate matching score between job description and resume."""
        # Convert to sets for comparison
        jd_kw_set = set(jd_keywords)
        resume_kw_set = set(resume_keywords)
        jd_ph_set = set(jd_phrases)
        resume_ph_set = set(resume_phrases)
        
        # Find matches
        matched_keywords = jd_kw_set.intersection(resume_kw_set)
        matched_phrases = jd_ph_set.intersection(resume_ph_set)
        
        # Calculate scores
        keyword_score = (len(matched_keywords) / len(jd_kw_set) * 100) if jd_kw_set else 0
        phrase_score = (len(matched_phrases) / len(jd_ph_set) * 100) if jd_ph_set else 0
        
        # Overall score (weighted average)
        overall_score = (keyword_score * 0.7 + phrase_score * 0.3)
        
        # Find missing keywords
        missing_keywords = jd_kw_set - resume_kw_set
        
        return {
            'overall_score': overall_score,
            'keyword_score': keyword_score,
            'phrase_score': phrase_score,
            'matched_keywords': matched_keywords,
            'matched_phrases': matched_phrases,
            'missing_keywords': missing_keywords,
            'total_jd_keywords': len(jd_kw_set),
            'total_resume_keywords': len(resume_kw_set)
        }
    
    def analyze_match(self):
        """Analyze the match between job description and resume."""
        jd_content = self.jd_text.get("1.0", tk.END).strip()
        resume_content = self.resume_text.get("1.0", tk.END).strip()
        
        if not jd_content or not resume_content:
            messagebox.showwarning(
                "Missing Input",
                "Please enter both job description and resume text."
            )
            return
        
        # Extract keywords and phrases
        jd_keywords, jd_phrases = self.extract_keywords(jd_content)
        resume_keywords, resume_phrases = self.extract_keywords(resume_content)
        
        # Calculate match
        results = self.calculate_match_score(
            jd_keywords, resume_keywords,
            jd_phrases, resume_phrases
        )
        
        # Display results
        self.display_results(results)
    
    def display_results(self, results):
        """Display analysis results."""
        self.results_text.config(state=tk.NORMAL)
        self.results_text.delete("1.0", tk.END)
        
        # Overall score with color coding
        score = results['overall_score']
        if score >= 75:
            rating = "EXCELLENT MATCH"
            color = "green"
        elif score >= 60:
            rating = "GOOD MATCH"
            color = "blue"
        elif score >= 40:
            rating = "FAIR MATCH"
            color = "orange"
        else:
            rating = "POOR MATCH"
            color = "red"
        
        output = f"""{'='*70}
OVERALL ATS SCORE: {score:.1f}% - {rating}
{'='*70}

Detailed Breakdown:
-------------------
Keyword Match Score: {results['keyword_score']:.1f}%
Phrase Match Score: {results['phrase_score']:.1f}%

Matched Keywords ({len(results['matched_keywords'])}):
{', '.join(sorted(results['matched_keywords']))}

Matched Phrases ({len(results['matched_phrases'])}):
{', '.join(sorted(list(results['matched_phrases'])[:10]))}

Missing Keywords ({len(results['missing_keywords'])}):
{', '.join(sorted(list(results['missing_keywords'])[:20]))}

{'='*70}
Recommendations:
"""
        
        if score >= 75:
            output += "✓ Your resume is well-optimized for this position!\n"
        elif score >= 60:
            output += "→ Consider adding more relevant keywords from the job description.\n"
        else:
            output += "! Strongly recommend updating your resume with missing keywords.\n"
        
        if results['missing_keywords']:
            output += "\nTop Missing Keywords to Consider Adding:\n"
            missing_list = sorted(list(results['missing_keywords']))[:10]
            for kw in missing_list:
                output += f"  • {kw}\n"
        
        output += f"\n{'='*70}"
        
        self.results_text.insert("1.0", output)
        self.results_text.config(state=tk.DISABLED)
    
    def clear_all(self):
        """Clear all text fields."""
        self.jd_text.delete("1.0", tk.END)
        self.resume_text.delete("1.0", tk.END)
        self.results_text.config(state=tk.NORMAL)
        self.results_text.delete("1.0", tk.END)
        self.results_text.config(state=tk.DISABLED)
    
    def run(self):
        """Run the application."""
        self.window.mainloop()


if __name__ == "__main__":
    app = ATSScreener()
    app.run()
