#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 29 14:39:09 2026

@author: baharzafer
"""

import json
import base64
import os

def get_pdf_base64(file_path):
    """
    Reads a local PDF file and converts it to a base64 encoded string.
    If the file does not exist, returns an empty string.
    """
    if not os.path.exists(file_path):
        print(f"⚠️ Warning: Codebook PDF '{file_path}' not found. Loading without PDF.")
        return ""
    
    with open(file_path, "rb") as pdf_file:
        encoded_string = base64.b64encode(pdf_file.read()).decode('utf-8')
        return encoded_string

def generate_coding_tool(output_filename, articles_data, questions_config, article_level_config, pdf_base64=""):
    """
    Generates a standalone HTML coding tool for human annotators.
    """
    
    html_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Text Coding Dashboard</title>
    <style>
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 0; padding: 0; background-color: #f4f7f6; color: #333; overflow: hidden; display: flex; flex-direction: column; height: 100vh; }}
        header {{ background-color: #2c3e50; color: white; padding: 15px 20px; z-index: 100; box-shadow: 0 2px 5px rgba(0,0,0,0.1); flex-shrink: 0; box-sizing: border-box; }}
        .header-top {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; }}
        h1 {{ margin: 0; font-size: 1.2rem; }}
        
        /* Progress Grid */
        .progress-section {{ background: rgba(255,255,255,0.1); padding: 8px; border-radius: 6px; }}
        .grid-container {{ display: flex; gap: 6px; overflow-x: auto; padding-bottom: 5px; }}
        .grid-box {{ min-width: 35px; height: 35px; display: flex; align-items: center; justify-content: center; border-radius: 4px; background: #e74c3c; color: white; cursor: pointer; font-size: 0.85rem; font-weight: bold; transition: 0.2s; box-shadow: inset 0 0 0 1px rgba(0,0,0,0.1); flex-shrink: 0; }}
        .grid-box.completed {{ background: #2ecc71; }}
        .grid-box.current {{ box-shadow: 0 0 0 3px #f1c40f; transform: scale(1.1); z-index: 10; }}
        .grid-box:hover {{ opacity: 0.8; }}
        .grid-label {{ font-size: 0.8rem; margin-bottom: 5px; display: flex; justify-content: space-between; }}

        /* Container */
        .container {{ display: flex; flex-grow: 1; overflow: hidden; }}
        
        /* Left Pane: Article Text */
        .article-pane {{ width: 55%; padding: 30px; overflow-y: auto; background: white; border-right: 2px solid #e0e0e0; box-sizing: border-box; height: 100%; }}
        .chunk-text {{ padding: 15px; margin-bottom: 15px; background: #f9f9f9; border-left: 4px solid #3498db; border-radius: 4px; line-height: 1.6; font-size: 1.05rem; transition: 0.3s; }}
        .chunk-text.answered {{ border-left-color: #2ecc71; background: #f0fdf4; }}
        .chunk-number {{ font-weight: bold; color: #7f8c8d; font-size: 0.9rem; margin-bottom: 8px; display: block; }}
        
        /* Right Pane: Questions */
        .coding-pane {{ width: 45%; padding: 30px; overflow-y: auto; background: #f4f7f6; display: flex; flex-direction: column; box-sizing: border-box; height: 100%; }}
        .question-card {{ background: white; padding: 15px; margin-bottom: 15px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); border: 1px solid #eee; transition: 0.3s; }}
        .question-card.answered {{ border-color: #2ecc71; }}
        .question-card h3 {{ margin-top: 0; font-size: 1rem; color: #2c3e50; }}
        .radio-group {{ display: flex; flex-direction: column; gap: 8px; }}
        .radio-group label {{ cursor: pointer; padding: 8px; border-radius: 4px; transition: background 0.2s; display: block; }}
        .radio-group label:hover {{ background: #f0f4f8; }}
        
        /* Article Level Task */
        .article-level-card {{ background: #fff3e0; border-left: 4px solid #f39c12; padding: 15px; margin-top: auto; margin-bottom: 20px; border-radius: 8px; flex-shrink: 0; }}
        .article-level-card h3 {{ margin-top: 0; font-size: 1rem; color: #2c3e50; margin-bottom: 5px;}}
        .checkbox-group {{ display: flex; flex-direction: column; gap: 8px; margin-top: 10px; }}
        .checkbox-group label {{ cursor: pointer; }}
        
        /* Navigation & Buttons */
        .header-buttons {{ display: flex; gap: 10px; }}
        .nav-buttons {{ display: flex; justify-content: space-between; margin-top: 20px; padding-bottom: 20px; flex-shrink: 0; }}
        button {{ padding: 10px 20px; border: none; border-radius: 4px; font-size: 1rem; cursor: pointer; color: white; background-color: #3498db; transition: 0.2s; font-weight: bold; }}
        button:hover {{ background-color: #2980b9; }}
        button:disabled {{ background-color: #bdc3c7; cursor: not-allowed; }}
        .export-btn {{ background-color: #27ae60; }}
        .export-btn:hover {{ background-color: #2ecc71; }}
        .info-btn {{ background-color: #8e44ad; }}
        .info-btn:hover {{ background-color: #9b59b6; }}

        /* Modal Styles */
        .modal {{ display: none; position: fixed; z-index: 1000; left: 0; top: 0; width: 100%; height: 100%; background-color: rgba(0,0,0,0.6); backdrop-filter: blur(2px); }}
        .modal-content {{ margin: 2% auto; width: 90%; max-width: 1200px; height: 90vh; background-color: #fff; border-radius: 8px; display: flex; flex-direction: column; overflow: hidden; box-shadow: 0 5px 15px rgba(0,0,0,0.3); }}
        .modal-header {{ padding: 15px 20px; background: #f8f9fa; border-bottom: 1px solid #ddd; display: flex; justify-content: space-between; align-items: center; }}
        .modal-header h2 {{ margin: 0; color: #2c3e50; font-size: 1.2rem; }}
        .close-btn {{ color: #7f8c8d; font-size: 28px; font-weight: bold; cursor: pointer; line-height: 1; }}
        .close-btn:hover {{ color: #e74c3c; }}
        .modal-body {{ flex-grow: 1; width: 100%; }}
        .modal-body embed {{ width: 100%; height: 100%; border: none; }}
    </style>
</head>
<body>

<header>
    <div class="header-top">
        <h1>Text Coding Dashboard</h1>
        <div class="header-buttons">
            <button class="info-btn" onclick="openModal()">📖 View Codebook (PDF)</button>
            <button class="export-btn" onclick="exportToCSV()">💾 Export Results</button>
        </div>
    </div>
    <div class="progress-section">
        <div class="grid-label">
            <span><strong>Document Navigator:</strong> Click a box to jump. (Progress is auto-saved locally)</span>
            <span><span style="color:#2ecc71">■</span> Complete &nbsp;&nbsp; <span style="color:#e74c3c">■</span> Skipped/Incomplete</span>
        </div>
        <div class="grid-container" id="gridContainer">
            <!-- Grid boxes injected here -->
        </div>
    </div>
</header>

<div class="container">
    <div class="article-pane" id="articlePane"></div>
    <div class="coding-pane">
        <div id="questionsPane"></div>
        
        <div class="article-level-card">
            <h3 id="articleLevelTitle"></h3>
            <span style="font-size: 0.85rem; color: #7f8c8d;">Select all that apply to the ENTIRE document.</span>
            <div class="checkbox-group" id="articleTagsPane">
                <!-- Article tags injected here -->
            </div>
        </div>

        <div class="nav-buttons">
            <button id="btnPrev" onclick="navigate(-1)">Previous Document</button>
            <button id="btnNext" onclick="navigate(1)">Next Document</button>
        </div>
    </div>
</div>

<!-- INSTRUCTIONS MODAL -->
<div id="codebookModal" class="modal">
    <div class="modal-content">
        <div class="modal-header">
            <h2>Coding Instructions / Codebook</h2>
            <span class="close-btn" onclick="closeModal()">&times;</span>
        </div>
        <div class="modal-body">
            <!-- PDF injected here -->
            <embed src="data:application/pdf;base64,{pdf_base64}" type="application/pdf">
        </div>
    </div>
</div>

<script>
    // --- DYNAMIC DATA INJECTED BY PYTHON ---
    const articlesData = {json.dumps(articles_data)};
    const questionsConfig = {json.dumps(questions_config)};
    const articleTagsConfig = {json.dumps(article_level_config)};

    // --- APPLICATION LOGIC ---
    let currentArticleIndex = 0;
    let codingResults = {{}}; 

    function init() {{
        // Initialize results tracking object
        articlesData.forEach(art => {{
            codingResults[art.record_id] = {{ chunks: {{}}, article_tags: [] }};
        }});
        
        injectArticleTags();
        renderGrid();
        loadArticle(currentArticleIndex);
    }}

    function injectArticleTags() {{
        document.getElementById('articleLevelTitle').innerText = articleTagsConfig.title;
        
        const pane = document.getElementById('articleTagsPane');
        articleTagsConfig.options.forEach(tag => {{
            const label = document.createElement('label');
            label.innerHTML = `<input type="checkbox" id="tag_${{tag.id}}" value="${{tag.id}}" onchange="saveArticleLevel()"> ${{tag.label}}`;
            pane.appendChild(label);
        }});
    }}

    function renderGrid() {{
        const grid = document.getElementById('gridContainer');
        grid.innerHTML = '';
        articlesData.forEach((art, idx) => {{
            const box = document.createElement('div');
            box.className = 'grid-box';
            box.innerText = idx + 1;
            box.onclick = () => {{ loadArticle(idx); }};
            
            // Check completion status
            const data = codingResults[art.record_id];
            const totalChunks = art.chunks.length;
            const answeredChunks = Object.keys(data.chunks).length;
            
            if (answeredChunks === totalChunks || data.article_tags.length > 0) {{
                box.classList.add('completed');
            }}
            if (idx === currentArticleIndex) {{
                box.classList.add('current');
                box.scrollIntoView({{ behavior: 'smooth', block: 'nearest', inline: 'center' }});
            }}
            grid.appendChild(box);
        }});
    }}

    function loadArticle(index) {{
        currentArticleIndex = index;
        const article = articlesData[index];
        
        // 1. Render Left Pane (Article Text)
        const articlePane = document.getElementById('articlePane');
        articlePane.innerHTML = '';
        article.chunks.forEach((c, i) => {{
            const div = document.createElement('div');
            div.className = 'chunk-text';
            div.id = 'chunk_text_' + c.chunk_id;
            
            if(codingResults[article.record_id].chunks[c.chunk_id]) {{
                div.classList.add('answered');
            }}
            
            div.innerHTML = `<span class="chunk-number">Excerpt ${{i + 1}}</span>${{c.text}}`;
            articlePane.appendChild(div);
        }});

        // 2. Render Right Pane (Questions)
        const qPane = document.getElementById('questionsPane');
        qPane.innerHTML = '';
        article.chunks.forEach((c, i) => {{
            const card = document.createElement('div');
            card.className = 'question-card';
            card.id = 'qcard_' + c.chunk_id;
            
            const currentAnswer = codingResults[article.record_id].chunks[c.chunk_id];
            if(currentAnswer) card.classList.add('answered');

            let html = `<h3>Excerpt ${{i + 1}}: ${{questionsConfig.title}}</h3><div class="radio-group">`;
            questionsConfig.options.forEach(opt => {{
                const checked = (currentAnswer === opt.value) ? 'checked' : '';
                html += `<label><input type="radio" name="chunk_${{c.chunk_id}}" value="${{opt.value}}" onchange="saveAnswer('${{article.record_id}}', ${{c.chunk_id}}, '${{opt.value}}')" ${{checked}}> ${{opt.label}}</label>`;
            }});
            html += `</div>`;
            card.innerHTML = html;
            qPane.appendChild(card);
        }});

        // 3. Update Article-Level Checkboxes
        const tags = codingResults[article.record_id].article_tags;
        articleTagsConfig.options.forEach(tag => {{
            document.getElementById('tag_' + tag.id).checked = tags.includes(tag.id);
        }});

        // 4. Update Navigation Buttons
        document.getElementById('btnPrev').disabled = (index === 0);
        document.getElementById('btnNext').disabled = (index === articlesData.length - 1);

        renderGrid();
    }}

    function saveAnswer(recordId, chunkId, value) {{
        codingResults[recordId].chunks[chunkId] = value;
        document.getElementById('chunk_text_' + chunkId).classList.add('answered');
        document.getElementById('qcard_' + chunkId).classList.add('answered');
        renderGrid();
    }}

    function saveArticleLevel() {{
        const article = articlesData[currentArticleIndex];
        const tags = [];
        articleTagsConfig.options.forEach(tag => {{
            if(document.getElementById('tag_' + tag.id).checked) {{
                tags.push(tag.id);
            }}
        }});
        codingResults[article.record_id].article_tags = tags;
        renderGrid();
    }}

    function navigate(step) {{
        const newIndex = currentArticleIndex + step;
        if (newIndex >= 0 && newIndex < articlesData.length) {{
            loadArticle(newIndex);
            document.querySelector('.coding-pane').scrollTop = 0;
            document.querySelector('.article-pane').scrollTop = 0;
        }}
    }}

    function exportToCSV() {{
        let csvContent = "data:text/csv;charset=utf-8,Record_ID,Chunk_ID,Chunk_Code,Document_Tags\\n";
        
        articlesData.forEach(art => {{
            const recId = art.record_id;
            const tags = codingResults[recId].article_tags.join('|');
            
            art.chunks.forEach(c => {{
                const ans = codingResults[recId].chunks[c.chunk_id] || '';
                csvContent += `"${{recId}}",${{c.chunk_id}},"${{ans}}","${{tags}}"\\n`;
            }});
        }});
        
        const encodedUri = encodeURI(csvContent);
        const link = document.createElement("a");
        link.setAttribute("href", encodedUri);
        link.setAttribute("download", "coding_results.csv");
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    }}

    // Modal Functions
    function openModal() {{ document.getElementById('codebookModal').style.display = 'block'; }}
    function closeModal() {{ document.getElementById('codebookModal').style.display = 'none'; }}
    
    // Close modal if clicked outside
    window.onclick = function(event) {{
        const modal = document.getElementById('codebookModal');
        if (event.target == modal) {{
            modal.style.display = "none";
        }}
    }}

    window.onload = init;
</script>
</body>
</html>"""

    with open(output_filename, 'w', encoding='utf-8') as f:
        f.write(html_template)
    print(f"✅ Successfully generated coding tool: {output_filename}")