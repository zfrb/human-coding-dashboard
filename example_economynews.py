#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 29 14:33:58 2026

@author: baharzafer
"""

from generate_html import generate_coding_tool, get_pdf_base64
import json


economy_valence_questions = {
"title": "Does this excerpt convey a positive, negative, or neutral assessment of the economic situation?",
"options": [
    {"label": "🟢 Positive (Optimistic/Favorable outlook)", "value": "Positive"},
    {"label": "🔴 Negative (Pessimistic/Unfavorable outlook)", "value": "Negative"},
    {"label": "⚖️ Mixed (Contains competing positive and negative assessments)", "value": "Mixed"},
    {"label": "📊 Neutral / Fact-Based (Objective reporting without directional tone)", "value": "Neutral"},
    {"label": "❓ Not Applicable (Does not discuss the economy)", "value": "NA"}
]}

economy_article_tags = {
        "title": "Overall Article Attributes",
        "options": [
            {"id": "macro_focus", "label": "Focuses on Macroeconomic Indicators (e.g., inflation, GDP)"},
            {"id": "micro_focus", "label": "Focuses on Microeconomic/Individual Impact"},
            {"id": "policy_critique", "label": "Contains explicit critique of government policy"}]}

with open("articles.json", "r", encoding="utf-8") as f:
        economy_news = json.load(f)
        
codebook = get_pdf_base64("codebook.pdf")


print("Building coding dashboard...")
generate_coding_tool(
    output_filename = "human_coding_economy_valence.html",
    articles_data = economy_news,
    questions_config = economy_valence_questions,
    article_level_config = economy_article_tags,
    pdf_base64 = codebook 
)

