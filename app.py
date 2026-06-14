from flask import Flask, request, render_template_string
import xml.etree.ElementTree as ET
import re

app = Flask(__name__)

# ==========================================
# 1. THE HTML DASHBOARD TEMPLATE (Elegant Light Theme)
# ==========================================
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>XML Configuration Analyzer</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    
    <style>
        :root {
            --bg-body: #fafbfc;
            --bg-surface: #ffffff;
            --bg-surface-hover: #f8f9fb;
            
            --text-primary: #1a1f36;
            --text-secondary: #697386;
            --text-tertiary: #8792a2;
            
            --border-light: #e3e8ee;
            --border-lighter: #f0f3f7;
            
            --accent-primary: #635bff;
            --accent-primary-light: #f0efff;
            --accent-red: #cd3d64;
            --accent-red-light: #fdf0f3;
            --accent-orange: #d97706;
            --accent-orange-light: #fef6e8;
            --accent-green: #0d9488;
            --accent-green-light: #ecfdf5;
            --accent-blue: #3b82f6;
            --accent-blue-light: #eff6ff;
            
            --shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.04);
            --shadow-md: 0 4px 12px rgba(0, 0, 0, 0.05);
            --shadow-lg: 0 8px 24px rgba(0, 0, 0, 0.06);
            
            --radius-sm: 8px;
            --radius-md: 12px;
            --radius-lg: 16px;
        }

        * { box-sizing: border-box; margin: 0; padding: 0; }
        
        body { 
            font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif; 
            background-color: var(--bg-body);
            color: var(--text-primary); 
            min-height: 100vh;
            -webkit-font-smoothing: antialiased;
            -moz-osx-font-smoothing: grayscale;
            display: flex;
        }

        /* Sidebar */
        .sidebar {
            width: 420px;
            min-width: 280px;
            background: var(--bg-surface);
            border-right: 1px solid var(--border-light);
            height: 100vh;
            position: sticky;
            top: 0;
            display: flex;
            flex-direction: column;
            overflow: hidden;
        }
        
        .sidebar-header {
            padding: 1.25rem 1.5rem;
            border-bottom: 1px solid var(--border-light);
            display: flex;
            align-items: center;
            gap: 0.75rem;
        }
        
        .sidebar-logo {
            width: 32px;
            height: 32px;
            background: linear-gradient(135deg, var(--accent-primary) 0%, #8b5cf6 100%);
            border-radius: var(--radius-sm);
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-size: 0.875rem;
        }
        
        .sidebar-title {
            font-weight: 700;
            font-size: 1rem;
            color: var(--text-primary);
        }
        
        .sidebar-content {
            flex: 1;
            overflow-y: auto;
            padding: 1.25rem;
        }
        
        .sidebar-section {
            margin-bottom: 1.5rem;
        }
        
        .sidebar-section-title {
            font-size: 0.6875rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            color: var(--text-tertiary);
            margin-bottom: 0.75rem;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }
        
        .meta-list {
            list-style: none;
        }
        
        .meta-item {
            padding: 0.75rem;
            background: var(--bg-body);
            border-radius: var(--radius-sm);
            margin-bottom: 0.5rem;
            border: 1px solid var(--border-lighter);
        }
        
        .meta-key {
            display: block;
            font-size: 0.625rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.03em;
            color: var(--text-tertiary);
            margin-bottom: 0.25rem;
        }
        
        .meta-value {
            display: block;
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.75rem;
            color: var(--text-primary);
            word-break: break-word;
            line-height: 1.4;
        }
        
        .sidebar-empty {
            text-align: center;
            padding: 2rem 1rem;
            color: var(--text-tertiary);
        }
        
        .sidebar-empty i {
            font-size: 1.5rem;
            margin-bottom: 0.5rem;
            opacity: 0.5;
        }
        
        .sidebar-empty span {
            display: block;
            font-size: 0.8125rem;
        }

        /* Main Wrapper */
        .main-wrapper {
            flex: 1;
            display: flex;
            flex-direction: column;
            min-width: 0;
        }

        /* Header */
        .header {
            background: var(--bg-surface);
            border-bottom: 1px solid var(--border-light);
            padding: 0.875rem 2rem;
            position: sticky;
            top: 0;
            z-index: 100;
        }
        
        .header-inner {
            display: flex;
            align-items: center;
            justify-content: space-between;
        }
        
        .page-heading {
            font-size: 1.125rem;
            font-weight: 600;
            color: var(--text-primary);
        }
        
        .header-actions {
            display: flex;
            align-items: center;
            gap: 1rem;
        }
        
        .header-btn {
            width: 36px;
            height: 36px;
            border-radius: 50%;
            border: 1px solid var(--border-light);
            background: var(--bg-surface);
            color: var(--text-secondary);
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            transition: all 0.2s;
        }
        
        .header-btn:hover {
            background: var(--bg-surface-hover);
            color: var(--text-primary);
        }

        /* Main Container */
        .main-container {
            flex: 1;
            padding: 1.5rem 2rem;
            overflow-y: auto;
        }

        /* Upload Section */
        .upload-section {
            background: var(--bg-surface);
            border: 1px solid var(--border-light);
            border-radius: var(--radius-lg);
            padding: 1.5rem;
            margin-bottom: 1.5rem;
            box-shadow: var(--shadow-sm);
        }
        
        .upload-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 1rem;
            margin-bottom: 1rem;
        }
        
        .upload-item {
            position: relative;
        }
        
        .upload-item label {
            display: block;
            font-size: 0.8125rem;
            font-weight: 600;
            color: var(--text-primary);
            margin-bottom: 0.5rem;
        }
        
        .upload-zone {
            position: relative;
            border: 1.5px dashed var(--border-light);
            border-radius: var(--radius-md);
            padding: 1rem;
            text-align: center;
            cursor: pointer;
            transition: all 0.2s;
            background: var(--bg-body);
        }
        
        .upload-zone:hover {
            border-color: var(--accent-primary);
            background: var(--accent-primary-light);
        }
        
        .upload-zone.has-file {
            border-color: var(--accent-green);
            background: var(--accent-green-light);
        }
        
        .upload-zone i {
            font-size: 1.25rem;
            color: var(--text-tertiary);
            margin-bottom: 0.25rem;
            display: block;
        }
        
        .upload-zone span {
            font-size: 0.75rem;
            color: var(--text-tertiary);
        }
        
        .upload-zone input[type="file"] {
            position: absolute;
            inset: 0;
            opacity: 0;
            cursor: pointer;
        }
        
        .btn-analyze {
            background: var(--accent-primary);
            color: white;
            border: none;
            padding: 0.75rem 1.5rem;
            border-radius: var(--radius-sm);
            font-weight: 600;
            font-size: 0.875rem;
            cursor: pointer;
            transition: all 0.2s;
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
        }
        
        .btn-analyze:hover {
            background: #5046e5;
            transform: translateY(-1px);
            box-shadow: var(--shadow-md);
        }

        /* Error Alert */
        .error-alert {
            display: flex;
            align-items: flex-start;
            gap: 1rem;
            background: var(--accent-red-light);
            border: 1px solid var(--accent-red);
            border-radius: var(--radius-md);
            padding: 1rem 1.25rem;
            margin-bottom: 1.5rem;
        }
        
        .error-icon {
            width: 36px;
            height: 36px;
            background: var(--accent-red);
            color: white;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            flex-shrink: 0;
        }
        
        .error-content {
            flex: 1;
        }
        
        .error-title {
            font-weight: 600;
            font-size: 0.9375rem;
            color: var(--accent-red);
            margin-bottom: 0.25rem;
        }
        
        .error-message {
            font-size: 0.875rem;
            color: var(--text-secondary);
            line-height: 1.5;
        }
        
        .error-close {
            background: none;
            border: none;
            color: var(--accent-red);
            cursor: pointer;
            padding: 0.25rem;
            font-size: 1rem;
            opacity: 0.7;
            transition: opacity 0.2s;
        }
        
        .error-close:hover {
            opacity: 1;
        }

        /* Stats Cards */
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 1rem;
            margin-bottom: 1.5rem;
        }
        
        .stat-card {
            background: var(--bg-surface);
            border: 1px solid var(--border-light);
            border-radius: var(--radius-md);
            padding: 1.25rem;
            cursor: pointer;
            transition: all 0.2s;
            box-shadow: var(--shadow-sm);
        }
        
        .stat-card:hover, .stat-card.active {
            border-color: var(--accent-primary);
            box-shadow: var(--shadow-md);
            transform: translateY(-2px);
        }
        
        .stat-card.active {
            background: var(--accent-primary-light);
        }
        
        .stat-header {
            display: flex;
            align-items: flex-start;
            justify-content: space-between;
            margin-bottom: 0.75rem;
        }
        
        .stat-icon {
            width: 40px;
            height: 40px;
            border-radius: var(--radius-sm);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1rem;
        }
        
        .stat-icon.red { background: var(--accent-red-light); color: var(--accent-red); }
        .stat-icon.orange { background: var(--accent-orange-light); color: var(--accent-orange); }
        .stat-icon.blue { background: var(--accent-blue-light); color: var(--accent-blue); }
        .stat-icon.green { background: var(--accent-green-light); color: var(--accent-green); }
        
        .stat-value {
            font-size: 1.75rem;
            font-weight: 700;
            color: var(--text-primary);
            line-height: 1;
        }
        
        .stat-label {
            font-size: 0.75rem;
            font-weight: 600;
            color: var(--text-secondary);
            text-transform: uppercase;
            letter-spacing: 0.025em;
        }

        /* Data Panel */
        .data-panel {
            background: var(--bg-surface);
            border: 1px solid var(--border-light);
            border-radius: var(--radius-lg);
            overflow: hidden;
            box-shadow: var(--shadow-sm);
        }
        
        .panel-view {
            display: none;
        }
        
        .panel-view.active {
            display: block;
        }
        
        .panel-header {
            padding: 1rem 1.5rem;
            border-bottom: 1px solid var(--border-light);
            display: flex;
            align-items: center;
            justify-content: space-between;
            background: var(--bg-surface);
        }
        
        .panel-title {
            display: flex;
            align-items: center;
            gap: 0.625rem;
            font-weight: 600;
            font-size: 0.9375rem;
            color: var(--text-primary);
        }
        
        .panel-title i {
            font-size: 0.875rem;
        }
        
        .panel-badge {
            background: var(--bg-body);
            border: 1px solid var(--border-light);
            padding: 0.25rem 0.625rem;
            border-radius: 20px;
            font-size: 0.75rem;
            font-weight: 600;
            color: var(--text-secondary);
        }
        
        .panel-body {
            max-height: 400px;
            overflow-y: auto;
        }
        
        .data-list {
            list-style: none;
        }
        
        .data-item {
            padding: 0.875rem 1.5rem;
            border-bottom: 1px solid var(--border-lighter);
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.8125rem;
            color: var(--text-primary);
            transition: background 0.15s;
        }
        
        .data-item:last-child {
            border-bottom: none;
        }
        
        .data-item:hover {
            background: var(--bg-surface-hover);
        }
        
        .data-item strong {
            font-weight: 600;
            display: block;
            margin-bottom: 0.25rem;
        }
        
        .data-item .detail {
            font-family: 'Plus Jakarta Sans', sans-serif;
            font-size: 0.75rem;
            color: var(--text-secondary);
            display: flex;
            align-items: center;
            gap: 0.375rem;
            margin-top: 0.25rem;
            padding: 0.375rem 0.5rem;
            background: var(--bg-body);
            border-radius: 4px;
            width: fit-content;
        }
        
        .empty-state {
            padding: 3rem 1.5rem;
            text-align: center;
            color: var(--text-tertiary);
        }
        
        .empty-state i {
            font-size: 2rem;
            margin-bottom: 0.75rem;
            opacity: 0.5;
        }
        
        .empty-state span {
            display: block;
            font-size: 0.875rem;
        }
        
        .success-state i {
            color: var(--accent-green);
            opacity: 1;
        }

        /* Scrollbar */
        ::-webkit-scrollbar { width: 6px; }
        ::-webkit-scrollbar-track { background: transparent; }
        ::-webkit-scrollbar-thumb { background: var(--border-light); border-radius: 3px; }
        ::-webkit-scrollbar-thumb:hover { background: var(--text-tertiary); }

        /* Responsive */
        @media (max-width: 1200px) {
            .sidebar { width: 240px; min-width: 240px; }
        }
        
        @media (max-width: 1024px) {
            .upload-grid { grid-template-columns: repeat(2, 1fr); }
            .stats-grid { grid-template-columns: repeat(2, 1fr); }
            .sidebar { display: none; }
        }
        
        @media (max-width: 640px) {
            .main-container { padding: 1rem; }
            .upload-grid { grid-template-columns: 1fr; }
            .stats-grid { grid-template-columns: 1fr; }
        }
    </style>
</head>
<body>

    <aside class="sidebar">
        <div class="sidebar-header">
            <div class="sidebar-logo"><i class="fas fa-layer-group"></i></div>
            <span class="sidebar-title">XML Analyzer</span>
        </div>
        <div class="sidebar-content">
            <div class="sidebar-section">
                <h3 class="sidebar-section-title"><i class="fas fa-file-code"></i> Document Metadata</h3>
                {% if processed and metadata %}
                <ul class="meta-list">
                    {% for key, value in metadata.items() %}
                    <li class="meta-item">
                        <span class="meta-key">{{ key }}</span>
                        <span class="meta-value">{{ value }}</span>
                    </li>
                    {% endfor %}
                </ul>
                {% else %}
                <div class="sidebar-empty">
                    <i class="fas fa-inbox"></i>
                    <span>Upload files to view metadata</span>
                </div>
                {% endif %}
            </div>
            
            {% if processed %}
            <div class="sidebar-section">
                <h3 class="sidebar-section-title"><i class="fas fa-chart-pie"></i> Summary</h3>
                <ul class="meta-list">
                    <li class="meta-item">
                        <span class="meta-key">Total Issues</span>
                        <span class="meta-value">{{ (missing_from_pavast | length) + (missing_from_fs | length) + (incorrect_tags | length) + (syscond_deviations | length) }}</span>
                    </li>
                    <li class="meta-item">
                        <span class="meta-key">Variables</span>
                        <span class="meta-value">{{ missing_from_pavast | length }} orphaned in FS</span>
                    </li>
                    <li class="meta-item">
                        <span class="meta-key">SYSCOND</span>
                        <span class="meta-value">{{ syscond_deviations | length }} deviations</span>
                    </li>
                </ul>
            </div>
            {% endif %}
        </div>
    </aside>

    <div class="main-wrapper">
        <header class="header">
            <div class="header-inner">
                <span class="page-heading">Configuration Analysis</span>
                <div class="header-actions">
                    <button class="header-btn"><i class="fas fa-question-circle"></i></button>
                    <button class="header-btn"><i class="fas fa-cog"></i></button>
                </div>
            </div>
        </header>

        <main class="main-container">

        <section class="upload-section">
            <form action="/" method="POST" enctype="multipart/form-data">
                <div class="upload-grid">
                    <div class="upload-item">
                        <label>XDI Data XML <span style="font-weight: 400; color: var(--text-muted);">(optional)</span></label>
                        <div class="upload-zone" id="zone1">
                            <i class="fas fa-cloud-arrow-up"></i>
                            <span id="name1">Choose file or drag here</span>
                            <input type="file" name="xdidata" accept=".xml" onchange="updateZone(this, 'zone1', 'name1')">
                        </div>
                    </div>
                    <div class="upload-item">
                        <label>PAVAST XML <span style="color: var(--accent-red);">*</span></label>
                        <div class="upload-zone" id="zone2">
                            <i class="fas fa-cloud-arrow-up"></i>
                            <span id="name2">Choose file or drag here</span>
                            <input type="file" name="pavast" accept=".xml" required onchange="updateZone(this, 'zone2', 'name2')">
                        </div>
                    </div>
                    <div class="upload-item">
                        <label>FS XML <span style="color: var(--accent-red);">*</span></label>
                        <div class="upload-zone" id="zone3">
                            <i class="fas fa-cloud-arrow-up"></i>
                            <span id="name3">Choose file or drag here</span>
                            <input type="file" name="fs_xml" accept=".xml" required onchange="updateZone(this, 'zone3', 'name3')">
                        </div>
                    </div>
                </div>
                <button type="submit" class="btn-analyze">
                    <i class="fas fa-play"></i>
                    Run Analysis
                </button>
            </form>
        </section>

        {% if error %}
        <div class="error-alert">
            <div class="error-icon"><i class="fas fa-exclamation-triangle"></i></div>
            <div class="error-content">
                <div class="error-title">File Validation Error</div>
                <div class="error-message">{{ error }}</div>
            </div>
            <button class="error-close" onclick="this.parentElement.remove()"><i class="fas fa-times"></i></button>
        </div>
        {% endif %}

        {% if processed %}
        <div class="stats-grid">
            <div class="stat-card active" data-target="view-pavast">
                <div class="stat-header">
                    <div class="stat-icon red"><i class="fas fa-circle-xmark"></i></div>
                </div>
                <div class="stat-value">{{ missing_from_pavast | length }}</div>
                <div class="stat-label">Missing in PAVAST</div>
            </div>
            
            <div class="stat-card" data-target="view-fs">
                <div class="stat-header">
                    <div class="stat-icon orange"><i class="fas fa-triangle-exclamation"></i></div>
                </div>
                <div class="stat-value">{{ missing_from_fs | length }}</div>
                <div class="stat-label">Missing in FS</div>
            </div>
            
            <div class="stat-card" data-target="view-tags">
                <div class="stat-header">
                    <div class="stat-icon blue"><i class="fas fa-tags"></i></div>
                </div>
                <div class="stat-value">{{ incorrect_tags | length }}</div>
                <div class="stat-label">Incorrect Tags</div>
            </div>
            
            <div class="stat-card" data-target="view-syscond">
                <div class="stat-header">
                    <div class="stat-icon green"><i class="fas fa-code-branch"></i></div>
                </div>
                <div class="stat-value">{{ syscond_deviations | length }}</div>
                <div class="stat-label">SYSCOND Deviations</div>
            </div>
        </div>

        <div class="data-panel">
            
            <div id="view-pavast" class="panel-view active">
                <div class="panel-header">
                    <div class="panel-title">
                        <i class="fas fa-circle-xmark" style="color: var(--accent-red);"></i>
                        Items in FS but Missing in PAVAST
                    </div>
                    <span class="panel-badge">{{ missing_from_pavast | length }} items</span>
                </div>
                <div class="panel-body">
                    {% if missing_from_pavast %}
                    <ul class="data-list">
                        {% for item in missing_from_pavast %}
                        <li class="data-item">{{ item }}</li>
                        {% endfor %}
                    </ul>
                    {% else %}
                    <div class="empty-state success-state">
                        <i class="fas fa-check-circle"></i>
                        <span>All items are properly synced</span>
                    </div>
                    {% endif %}
                </div>
            </div>

            <div id="view-fs" class="panel-view">
                <div class="panel-header">
                    <div class="panel-title">
                        <i class="fas fa-triangle-exclamation" style="color: var(--accent-orange);"></i>
                        Items in PAVAST but Missing in FS
                    </div>
                    <span class="panel-badge">{{ missing_from_fs | length }} items</span>
                </div>
                <div class="panel-body">
                    {% if missing_from_fs %}
                    <ul class="data-list">
                        {% for item in missing_from_fs %}
                        <li class="data-item">{{ item }}</li>
                        {% endfor %}
                    </ul>
                    {% else %}
                    <div class="empty-state success-state">
                        <i class="fas fa-check-circle"></i>
                        <span>All items are properly synced</span>
                    </div>
                    {% endif %}
                </div>
            </div>

            <div id="view-tags" class="panel-view">
                <div class="panel-header">
                    <div class="panel-title">
                        <i class="fas fa-tags" style="color: var(--accent-blue);"></i>
                        Tag Type Mismatches
                    </div>
                    <span class="panel-badge">{{ incorrect_tags | length }} items</span>
                </div>
                <div class="panel-body">
                    {% if incorrect_tags %}
                    <ul class="data-list">
                        {% for item in incorrect_tags %}
                            {% set parts = item.split(': ', 1) %}
                            <li class="data-item">
                                <strong>{{ parts[0] }}</strong>
                                <div class="detail"><i class="fas fa-arrow-right"></i> {{ parts[1] }}</div>
                            </li>
                        {% endfor %}
                    </ul>
                    {% else %}
                    <div class="empty-state success-state">
                        <i class="fas fa-check-circle"></i>
                        <span>All tags are correctly configured</span>
                    </div>
                    {% endif %}
                </div>
            </div>

            <div id="view-syscond" class="panel-view">
                <div class="panel-header">
                    <div class="panel-title">
                        <i class="fas fa-code-branch" style="color: var(--accent-green);"></i>
                        SYSCOND Deviations
                    </div>
                    <span class="panel-badge">{{ syscond_deviations | length }} items</span>
                </div>
                <div class="panel-body">
                    {% if syscond_deviations %}
                    <ul class="data-list">
                        {% for item in syscond_deviations %}
                            {% set parts = item.split(': ', 1) %}
                            <li class="data-item">
                                <strong>{{ parts[0] }}</strong>
                                <div class="detail"><i class="fas fa-info-circle"></i> {{ parts[1] }}</div>
                            </li>
                        {% endfor %}
                    </ul>
                    {% else %}
                    <div class="empty-state success-state">
                        <i class="fas fa-check-circle"></i>
                        <span>No deviations found</span>
                    </div>
                    {% endif %}
                </div>
            </div>

        </div>
        {% endif %}

        </main>
    </div>

    <script>
        function updateZone(input, zoneId, nameId) {
            const zone = document.getElementById(zoneId);
            const name = document.getElementById(nameId);
            if (input.files && input.files[0]) {
                zone.classList.add('has-file');
                name.textContent = input.files[0].name;
            }
        }

        document.addEventListener('DOMContentLoaded', function() {
            const cards = document.querySelectorAll('.stat-card');
            const views = document.querySelectorAll('.panel-view');

            cards.forEach(card => {
                card.addEventListener('click', function() {
                    cards.forEach(c => c.classList.remove('active'));
                    this.classList.add('active');
                    
                    views.forEach(v => v.classList.remove('active'));
                    const targetId = this.getAttribute('data-target');
                    if (targetId) {
                        document.getElementById(targetId).classList.add('active');
                    }
                });
            });
        });
    </script>

</body>
</html>
"""

# ==========================================
# 2. PYTHON PARSING LOGIC & FLASK ROUTE
# ==========================================

def normalize(text):
    if not text:
        return ""
    text = text.strip()
    text = re.sub(r'^[^\w]+|[^\w]+$', '', text)
    return text

def parse_syscond(cond_text):
    cond_text = cond_text.replace("(", "").replace(")", "")
    or_parts = [x.strip() for x in cond_text.split("||")]
    or_groups = []
    for part in or_parts:
        and_conditions = []
        and_parts = [x.strip() for x in part.split("&&")]
        for cond in and_parts:
            m = re.search(r'([A-Za-z0-9_]+)\s*==\s*([0-9]+)', cond)
            if m:
                and_conditions.append({"sysconst": m.group(1), "value": m.group(2)})
                continue
            m = re.search(r'([A-Za-z0-9_]+)', cond)
            if m:
                and_conditions.append({"sysconst": m.group(1), "value": 1})
        if and_conditions:
            or_groups.append({"and_conditions": and_conditions})
    return {"or_groups": or_groups}

def parse_fs_syscond(syscond_str):
    if not syscond_str:
        return None
    syscond_str = re.sub(r'\s+', '', syscond_str)
    or_groups = []
    or_parts = syscond_str.split('||')
    for or_part in or_parts:
        and_conditions = []
        and_parts = or_part.split('&&')
        for and_part in and_parts:
            m = re.search(r'i\(([A-Za-z0-9_]+)\)==(\d+)', and_part)
            if m:
                and_conditions.append({"sysconst": m.group(1), "value": m.group(2)})
            else:
                m = re.search(r'i\(([A-Za-z0-9_]+)\)', and_part)
                if m:
                    and_conditions.append({"sysconst": m.group(1), "value": "1"})
        if and_conditions:
            or_groups.append({"and_conditions": and_conditions})
    return {"or_groups": or_groups}

def get_elem_syscond(elem, parent_map):
    current = elem
    while current is not None:
        syscond = current.get("SYSCOND")
        if syscond:
            return syscond
        current = parent_map.get(current)
    return None

def compare_syscond(expected_binding, actual_syscond_str):
    if not expected_binding or not expected_binding.get("or_groups"):
        return True, None
    if not actual_syscond_str:
        return False, "Missing SYSCOND"
    
    actual_parsed = parse_fs_syscond(actual_syscond_str)
    if not actual_parsed or not actual_parsed.get("or_groups"):
        return False, f"Could not parse SYSCOND: {actual_syscond_str}"
    
    expected_or_groups = expected_binding["or_groups"]
    actual_or_groups = actual_parsed["or_groups"]
    
    for exp_group in expected_or_groups:
        exp_and_conds = exp_group["and_conditions"]
        for act_group in actual_or_groups:
            act_and_conds = act_group["and_conditions"]
            all_match = True
            for exp_cond in exp_and_conds:
                found = False
                for act_cond in act_and_conds:
                    if (exp_cond["sysconst"] == act_cond["sysconst"] and str(exp_cond["value"]) == str(act_cond["value"])):
                        found = True
                        break
                    elif (exp_cond["sysconst"] == act_cond["sysconst"] and str(exp_cond["value"]) == "1" and str(act_cond["value"]) == "1"):
                        found = True
                        break
                if not found:
                    all_match = False
                    break
            if all_match:
                return True, None
                
    expected_parts = []
    for og in expected_or_groups:
        and_parts = []
        for ac in og["and_conditions"]:
            and_parts.append(f"i({ac['sysconst']})=={ac['value']}")
        expected_parts.append("&&".join(and_parts))
    expected_str = "||".join(expected_parts)
    return False, f"Expected '{expected_str}', Found '{actual_syscond_str}'"


# The main route that handles both GET (show page) and POST (process files)
@app.route('/', methods=['GET', 'POST'])
def dashboard():
    if request.method == 'POST':
        try:
            # 1. GET UPLOADED FILES FROM USER
            files = {
                'xdidata': request.files.get('xdidata'),
                'pavast': request.files.get('pavast'),
                'fs_xml': request.files.get('fs_xml')
            }

            # Check if required files were uploaded (pavast and fs_xml are mandatory, xdidata is optional)
            required_files = ['pavast', 'fs_xml']
            missing_files = [k for k in required_files if not files.get(k) or files[k].filename == '']
            if missing_files:
                return render_template_string(HTML_TEMPLATE, processed=False, 
                    error=f"Missing required file(s): {', '.join(missing_files)}. Please upload pavast and fs XML files.")

            # Check if xdidata was provided
            has_xdidata = files.get('xdidata') and files['xdidata'].filename != ''

            # 2. Validate file extensions for provided files
            files_to_validate = ['pavast', 'fs_xml']
            if has_xdidata:
                files_to_validate.append('xdidata')
            
            for key in files_to_validate:
                file = files[key]
                if not file.filename.lower().endswith('.xml'):
                    return render_template_string(HTML_TEMPLATE, processed=False,
                        error=f"Invalid file type for {key}: '{file.filename}'. Only XML files are accepted.")

            # 3. Extract prefix from pavast file and validate naming convention
            pavast_filename = files['pavast'].filename
            match = re.match(r'(.+)_pavast\.xml$', pavast_filename, re.IGNORECASE)
            if not match:
                return render_template_string(HTML_TEMPLATE, processed=False, 
                    error=f"Pavast file name '{pavast_filename}' must follow the pattern 'prefix_pavast.xml' (e.g., 'scrmon_gnrlcalcnif_pavast.xml').")
            
            project_prefix = match.group(1)
            
            # Validate fs_xml naming
            expected_fs = f"{project_prefix}_fs.xml"
            if files['fs_xml'].filename.lower() != expected_fs.lower():
                return render_template_string(HTML_TEMPLATE, processed=False, 
                    error=f"File naming mismatch. Expected '{expected_fs}', but got '{files['fs_xml'].filename}'. Files must share the same prefix '{project_prefix}'.")

            # Validate xdidata naming if provided
            if has_xdidata:
                expected_xdi = f"{project_prefix}_xdidata.xml"
                if files['xdidata'].filename.lower() != expected_xdi.lower():
                    return render_template_string(HTML_TEMPLATE, processed=False, 
                        error=f"File naming mismatch. Expected '{expected_xdi}', but got '{files['xdidata'].filename}'. Files must share the same prefix '{project_prefix}'.")

            # 4. PARSE THE XML FILES
            tree_pavast = ET.parse(files['pavast'])
            root_pavast = tree_pavast.getroot()

            tree_fs = ET.parse(files['fs_xml'])
            root_fs = tree_fs.getroot()

            # Parse xdidata only if provided
            root_conf = None
            if has_xdidata:
                tree_conf = ET.parse(files['xdidata'])
                root_conf = tree_conf.getroot()

            # 5. RUN ANALYSIS LOGIC
            variables = set()
            parameters = set()
            system_constants = set()
            messages = set()
            instances = set()

            for elem in root_pavast.findall(".//SW-VARIABLE"):
                short_name = elem.find("SHORT-NAME")
                if short_name is None or not short_name.text:
                    continue
                name = normalize(short_name.text)
                impl_policy = elem.find(".//SW-IMPL-POLICY")
                if impl_policy is not None and impl_policy.text == "MESSAGE":
                    messages.add(name)
                else:
                    variables.add(name)

            for elem in root_pavast.findall(".//SW-CALPRM"):
                short_name = elem.find("SHORT-NAME")
                if short_name is not None and short_name.text:
                    parameters.add(normalize(short_name.text))

            for elem in root_pavast.findall(".//SW-SYSTEMCONST"):
                short_name = elem.find("SHORT-NAME")
                if short_name is not None and short_name.text:
                    system_constants.add(normalize(short_name.text))

            for elem in root_pavast.findall(".//SW-CLASS-INSTANCE"):
                category = elem.find("CATEGORY")
                if category is not None and category.text == "CLASS_INSTANCE":
                    short_name = elem.find("SHORT-NAME")
                    if short_name is not None and short_name.text:
                        instances.add(normalize(short_name.text)) 

            variable_bindings = {}

            for elem in root_pavast.findall(".//SW-VARIABLE-REF-SYSCOND"):
                var_ref = elem.find("SW-VARIABLE-REF")
                sw_syscond = elem.find("SW-SYSCOND")
                if var_ref is None or not var_ref.text or sw_syscond is None:
                    continue
                name = normalize(var_ref.text)
                cond_text = "".join(sw_syscond.itertext()).strip()
                variable_bindings[name] = parse_syscond(cond_text)

            for elem in root_pavast.findall(".//SW-CALPRM-REF-SYSCOND"):
                var_ref = elem.find("SW-CALPRM-REF")
                sw_syscond = elem.find("SW-SYSCOND")
                if var_ref is None or not var_ref.text or sw_syscond is None:
                    continue
                name = normalize(var_ref.text)
                cond_text = "".join(sw_syscond.itertext()).strip()
                variable_bindings[name] = parse_syscond(cond_text)

            for elem in root_pavast.findall(".//SW-CLASS-INSTANCE-REF-SYSCOND"):
                var_ref = elem.find("SW-CLASS-INSTANCE-REF")
                sw_syscond = elem.find("SW-SYSCOND")
                if var_ref is None or not var_ref.text or sw_syscond is None:
                    continue
                name = normalize(var_ref.text)
                if "/" in name:
                    name = name.split("/", 1)[1]
                cond_text = "".join(sw_syscond.itertext()).strip()
                variable_bindings[name] = parse_syscond(cond_text)

            vt_values = set()
            if root_conf is not None:
                for conf_item in root_conf.findall(".//CONF-ITEM"):
                    short_name = conf_item.find("SHORT-NAME")
                    if short_name is not None and short_name.text == "DSM_XDI_FID_NAME":
                        vt = conf_item.find("VT")
                        if vt is not None and vt.text:
                            vt_values.add(normalize(vt.text))

            parent_map = {child: parent for parent in root_fs.iter() for child in parent}

            missing_from_pavast = set()
            fs_names = set()
            incorrect_tags = []
            syscond_deviations = []
            metadata = {}
  
            for sd in tree_fs.findall(".//SD"):
                key = sd.get("GID")
                value = (sd.text or "").strip()
                if key:
                    metadata[key] = value

            for tt in root_fs.findall(".//TT"):
                tt_type = tt.get("TYPE")
                if tt.text is None:
                    continue
                name = normalize(tt.text)
                if name.startswith("DINH_stFId."):
                    name = name[len("DINH_stFId."):]
                if "_I." in name:
                    name = name.split(".", 1)[0]
                
                fs_names.add(name)

                if name in variable_bindings:
                    expected_binding = variable_bindings[name]
                    actual_syscond = get_elem_syscond(tt, parent_map)
                    is_match, reason = compare_syscond(expected_binding, actual_syscond)
                    if not is_match:
                        syscond_deviations.append(f"{name}: {reason}")

                if name in variables:
                    if tt_type != "SW-VARIABLE":
                        incorrect_tags.append(f"{name}: Expected SW-VARIABLE, Found {tt_type}")
                elif name in parameters:
                    if tt_type != "SW-CALPRM":
                        incorrect_tags.append(f"{name}: Expected SW-CALPRM, Found {tt_type}")
                elif name in system_constants:
                    if tt_type != "SW-SYSTEMCONST":
                        incorrect_tags.append(f"{name}: Expected SW-SYSTEMCONST, Found {tt_type}")
                elif name in messages:
                    if tt_type != "SW-VARIABLE":
                        incorrect_tags.append(f"{name}: Expected MESSAGE, Found {tt_type}")
                elif name in vt_values:
                    if tt_type != "SW-VARIABLE":
                        incorrect_tags.append(f"{name}: Expected MESSAGE, Found {tt_type}")
                elif name in instances:
                    if tt_type != "SW-VARIABLE":
                        incorrect_tags.append(f"{name}: Expected MESSAGE, Found {tt_type}")
                else:
                    if tt_type != "OTHER":
                        missing_from_pavast.add(name)

            all_pavast_items = variables | parameters | system_constants | messages | instances
            missing_from_fs = all_pavast_items - fs_names
            missing_from_fs = missing_from_fs - instances

            # 6. SEND DATA TO DASHBOARD
            return render_template_string(HTML_TEMPLATE,
                                          processed=True,
                                          missing_from_pavast=sorted(missing_from_pavast),
                                          missing_from_fs=sorted(missing_from_fs),
                                          syscond_deviations=sorted(set(syscond_deviations)),
                                          incorrect_tags=sorted(incorrect_tags),
                                          metadata=metadata)
                                          
        except ET.ParseError as e:
            return render_template_string(HTML_TEMPLATE, processed=False, 
                error=f"XML Parsing Error: The file could not be parsed. {str(e)}")
        except Exception as e:
            return render_template_string(HTML_TEMPLATE, processed=False, 
                error=f"Unexpected Error: {str(e)}") 

    # Initial Page Load (Show the form, hide the dashboard)
    return render_template_string(HTML_TEMPLATE, processed=False)

if __name__ == '__main__':
    print("Starting server... Open your browser to http://127.0.0.1:5000")
    app.run(debug=True)
