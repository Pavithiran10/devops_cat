import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

def set_cell_background(cell, fill_hex):
    tc_pr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), fill_hex)
    tc_pr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tc_pr = cell._tc.get_or_add_tcPr()
    tc_mar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tc_mar.append(node)
    tc_pr.append(tc_mar)

def create_report():
    doc = docx.Document()

    # Set Margins
    for section in doc.sections:
        section.top_margin = Inches(1)
        section.bottom_margin = Inches(1)
        section.left_margin = Inches(1)
        section.right_margin = Inches(1)

    # Base Styles
    style_normal = doc.styles['Normal']
    font = style_normal.font
    font.name = 'Times New Roman'
    font.size = Pt(12)
    font.color.rgb = RGBColor(0x22, 0x22, 0x22)

    # ==========================================
    # 1. TITLE PAGE
    # ==========================================
    p_inst = doc.add_paragraph()
    p_inst.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_inst.paragraph_format.space_before = Pt(36)
    p_inst.paragraph_format.space_after = Pt(4)
    run_inst = p_inst.add_run("COIMBATORE INSTITUTE OF TECHNOLOGY\n")
    run_inst.bold = True
    run_inst.font.size = Pt(16)
    run_sub = p_inst.add_run("(Government Aided Autonomous Institution Affiliated to Anna University)\nCOIMBATORE – 641 014")
    run_sub.font.size = Pt(11)
    run_sub.italic = True

    p_course = doc.add_paragraph()
    p_course.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_course.paragraph_format.space_before = Pt(28)
    p_course.paragraph_format.space_after = Pt(4)
    run_c = p_course.add_run("23IT723 – DEVOPS LABORATORY\n")
    run_c.bold = True
    run_c.font.size = Pt(14)
    run_p = p_course.add_run("FINAL PROJECT REPORT\n\n")
    run_p.bold = True
    run_p.font.size = Pt(13)

    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_before = Pt(18)
    p_title.paragraph_format.space_after = Pt(36)
    run_t = p_title.add_run("FITTRACK – FITNESS TRACKER WEB APPLICATION\nWITH DEVOPS AUTOMATION")
    run_t.bold = True
    run_t.font.size = Pt(17)
    run_t.font.color.rgb = RGBColor(0x0F, 0x38, 0x7A)

    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sub.paragraph_format.space_before = Pt(40)
    p_sub.paragraph_format.space_after = Pt(6)
    run_s = p_sub.add_run("Submitted by:\n")
    run_s.font.size = Pt(12)
    run_name = p_sub.add_run("PAVITHIRAN R\n")
    run_name.bold = True
    run_name.font.size = Pt(14)
    run_reg = p_sub.add_run("Register No: 2303717620522026\nDepartment of Information Technology")
    run_reg.font.size = Pt(11)

    p_date = doc.add_paragraph()
    p_date.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_date.paragraph_format.space_before = Pt(48)
    run_d = p_date.add_run("OCTOBER 2026")
    run_d.bold = True
    run_d.font.size = Pt(12)

    doc.add_page_break()

    # ==========================================
    # 2. BONAFIDE CERTIFICATE
    # ==========================================
    p_bc_head = doc.add_paragraph()
    p_bc_head.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_bc_inst = p_bc_head.add_run("COIMBATORE INSTITUTE OF TECHNOLOGY\n")
    r_bc_inst.bold = True
    r_bc_inst.font.size = Pt(15)
    r_bc_sub = p_bc_head.add_run("(Government Aided Autonomous Institution Affiliated to Anna University)\nCOIMBATORE – 641 014\n\n")
    r_bc_sub.font.size = Pt(10)
    r_bc_title = p_bc_head.add_run("BONAFIDE CERTIFICATE")
    r_bc_title.bold = True
    r_bc_title.font.size = Pt(14)
    r_bc_title.underline = True

    p_bc_body = doc.add_paragraph()
    p_bc_body.paragraph_format.space_before = Pt(24)
    p_bc_body.paragraph_format.line_spacing = 1.3
    p_bc_body.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    r_b1 = p_bc_body.add_run("Certified that this project report titled ")
    r_b2 = p_bc_body.add_run("“FITTRACK – FITNESS TRACKER WEB APPLICATION WITH DEVOPS AUTOMATION”")
    r_b2.bold = True
    r_b3 = p_bc_body.add_run(" is the bonafide work of ")
    r_b4 = p_bc_body.add_run("PAVITHIRAN R (Register No: 2303717620522026)")
    r_b4.bold = True
    r_b5 = p_bc_body.add_run(" completed during the academic year 2025–2026 – Semester VII for the project presentation and laboratory evaluation of ")
    r_b6 = p_bc_body.add_run("23IT723 – DEVOPS LABORATORY")
    r_b6.bold = True
    r_b7 = p_bc_body.add_run(" under our supervision.")

    p_cand = doc.add_paragraph()
    p_cand.paragraph_format.space_before = Pt(16)
    p_cand.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_cand.add_run("Certified that the candidate was examined during the laboratory practical examination conducted on _________________.")

    p_rev = doc.add_paragraph()
    p_rev.paragraph_format.space_before = Pt(36)
    p_rev.add_run("Review Members / Faculty Examiners:\n\n").bold = True
    p_rev.add_run("1. Dr. M. SANGEETHA                                                2. Dr. E. ARUL\n")
    p_rev.add_run("   Associate Professor, IT                                           Associate Professor, IT")

    doc.add_page_break()

    # ==========================================
    # 3. EVALUATION SCHEME & RUBRICS
    # ==========================================
    p_eval_h = doc.add_paragraph()
    p_eval_h.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_ev1 = p_eval_h.add_run("23IT723 – DEVOPS LABORATORY\nFINAL MINI PROJECT – EVALUATION SCHEME")
    r_ev1.bold = True
    r_ev1.font.size = Pt(14)

    p_eval_desc = doc.add_paragraph()
    p_eval_desc.paragraph_format.space_before = Pt(8)
    p_eval_desc.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_eval_desc.add_run("The final mini project requires students to integrate the major DevOps practices covered in the laboratory. The project demonstrates practical implementation of version control, collaborative development, Continuous Integration, containerization, automated testing, and automated deployment with persistent volume management.")

    # Evaluation Scheme Table
    table_scheme = doc.add_table(rows=1, cols=4)
    table_scheme.alignment = WD_TABLE_ALIGNMENT.CENTER
    hdr_cells = table_scheme.rows[0].cells
    hdr_titles = ["S.No.", "Evaluation Component", "Key Verification Points", "Marks"]
    for i, title in enumerate(hdr_titles):
        hdr_cells[i].text = title
        set_cell_background(hdr_cells[i], "0F387A")
        set_cell_margins(hdr_cells[i], top=120, bottom=120, left=100, right=100)
        p = hdr_cells[i].paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for r in p.runs:
            r.bold = True
            r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
            r.font.size = Pt(10)

    scheme_data = [
        ("1", "Problem Definition & Project Planning", "Problem statement, objectives, requirements, module identification, technology selection, and workflow planning.", "10"),
        ("2", "Git Repository & Version Control", "Repository creation, meaningful commits, README, .gitignore, remote repository, push/pull/fetch operations, and commit history.", "15"),
        ("3", "Branching, Merging & Collaboration", "Feature branches, parallel development, merging, conflict handling, branch organization, and collaborative workflow.", "10"),
        ("4", "Application Development & Build", "Working full-stack application, project structure, dependency management, build configuration, and error-free execution.", "15"),
        ("5", "Jenkins Continuous Integration", "Jenkins pipeline configuration, SCM checkout, automated triggers (webhook/polling), build stages, and console logs.", "15"),
        ("6", "Docker Containerization", "Hardened Dockerfile, non-root user, multi-stage image, container execution, port mapping, and health check validation.", "10"),
        ("7", "Automation / Configuration Management", "Ansible playbook execution, idempotent container lifecycle management, volume mounting, and automated health checks.", "5"),
        ("8", "Testing & Verification", "25 Pytest unit/integration test cases, boundary validation, test reporting, error identification, and corrective actions.", "5"),
        ("9", "Documentation & Presentation", "Architecture/workflow diagram, step-by-step commands, screenshots, troubleshooting guide, and conclusion.", "5"),
        ("10", "Final Demonstration & Viva-Voce", "Live demonstration, explanation of implementation, troubleshooting responses, and deep technical understanding.", "10"),
        ("", "TOTAL", "Comprehensive evaluation across 10 DevOps laboratory competencies", "100")
    ]

    for row_idx, item in enumerate(scheme_data):
        row_cells = table_scheme.add_row().cells
        bg_color = "F0F4F8" if row_idx % 2 == 1 else "FFFFFF"
        if item[1] == "TOTAL":
            bg_color = "D9E2EC"
        for i, val in enumerate(item):
            row_cells[i].text = val
            set_cell_background(row_cells[i], bg_color)
            set_cell_margins(row_cells[i], top=80, bottom=80, left=100, right=100)
            p = row_cells[i].paragraphs[0]
            if i in [0, 3]:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            else:
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            for r in p.runs:
                if item[1] == "TOTAL":
                    r.bold = True
                r.font.size = Pt(9.5)

    doc.add_page_break()

    # ==========================================
    # 4. TABLE OF CONTENTS
    # ==========================================
    p_toc_h = doc.add_paragraph()
    p_toc_h.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_toc = p_toc_h.add_run("TABLE OF CONTENTS")
    r_toc.bold = True
    r_toc.font.size = Pt(14)

    table_toc = doc.add_table(rows=1, cols=3)
    table_toc.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_hdr = table_toc.rows[0].cells
    t_hdr[0].text = "S.NO."
    t_hdr[1].text = "CONTENT"
    t_hdr[2].text = "PAGE NO."
    for c in t_hdr:
        set_cell_background(c, "0F387A")
        set_cell_margins(c, top=100, bottom=100, left=100, right=100)
        p = c.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for r in p.runs:
            r.bold = True
            r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
            r.font.size = Pt(10)

    toc_items = [
        ("1", "INTRODUCTION", "05"),
        ("2", "OBJECTIVES", "05"),
        ("3", "ABSTRACT", "06"),
        ("4", "TECHNOLOGY STACK", "06"),
        ("5", "SYSTEM ARCHITECTURE & CI/CD WORKFLOW", "07"),
        ("6", "MODULE 1 — USER INTERFACE & WORKOUT LOGGING", "08"),
        ("7", "MODULE 2 — FLASK RESTFUL BACKEND & API SERVICES", "09"),
        ("8", "MODULE 3 — SQLITE DATABASE MANAGEMENT & SCHEMA", "10"),
        ("9", "MODULE 4 — GIT & GITHUB SOURCE CONTROL", "11"),
        ("10", "MODULE 5 — DOCKER CONTAINERIZATION & HARDENING", "12"),
        ("11", "MODULE 6 — JENKINS CI/CD AUTOMATION PIPELINE", "14"),
        ("12", "MODULE 7 — AUTOMATED TESTING (PYTEST SUITE)", "15"),
        ("13", "MODULE 8 — ANSIBLE DEPLOYMENT AUTOMATION", "17"),
        ("14", "MODULE 9 — PERSISTENT STORAGE (DOCKER VOLUME)", "18"),
        ("15", "MODULE 10 — ANALYTICS ENGINE & GOAL MANAGEMENT", "19"),
        ("16", "MODULE 11 — COMPLETE CI/CD INTEGRATION", "20"),
        ("17", "MODULE 12 — APPLICATION & DEPLOYMENT VERIFICATION", "21"),
        ("18", "RESULTS AND OUTPUT", "23"),
        ("19", "COMMANDS USED (COMPREHENSIVE CHEATSHEET)", "24"),
        ("20", "ADVANTAGES", "28"),
        ("21", "LIMITATIONS", "28"),
        ("22", "FUTURE ENHANCEMENTS", "29"),
        ("23", "CONCLUSION", "29"),
    ]

    for row_idx, item in enumerate(toc_items):
        r_cells = table_toc.add_row().cells
        bg_col = "F7FAFC" if row_idx % 2 == 1 else "FFFFFF"
        for i, text in enumerate(item):
            r_cells[i].text = text
            set_cell_background(r_cells[i], bg_col)
            set_cell_margins(r_cells[i], top=60, bottom=60, left=80, right=80)
            p = r_cells[i].paragraphs[0]
            if i in [0, 2]:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            for r in p.runs:
                r.font.size = Pt(9.5)

    doc.add_page_break()

    # ==========================================
    # HELPER FOR SECTIONS
    # ==========================================
    def add_section_header(num, title):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(16)
        p.paragraph_format.space_after = Pt(6)
        run = p.add_run(f"{num}. {title}")
        run.bold = True
        run.font.size = Pt(13)
        run.font.color.rgb = RGBColor(0x0F, 0x38, 0x7A)
        return p

    def add_body_p(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(4)
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.line_spacing = 1.15
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        run = p.add_run(text)
        run.font.size = Pt(11)
        return p

    def add_bullet_p(title, desc=""):
        p = doc.add_paragraph(style='List Bullet')
        p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.space_after = Pt(3)
        r1 = p.add_run(title)
        r1.bold = True
        r1.font.size = Pt(10.5)
        if desc:
            r2 = p.add_run(f": {desc}")
            r2.font.size = Pt(10.5)
        return p

    def add_fig_placeholder(fig_no, caption):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(8)
        p.paragraph_format.space_after = Pt(12)
        r = p.add_run(f"[ {fig_no}: {caption} ]\n(Insert Screenshot / Verification Evidence Here)")
        r.italic = True
        r.font.size = Pt(10)
        r.font.color.rgb = RGBColor(0x55, 0x55, 0x55)

    # ==========================================
    # 1. INTRODUCTION
    # ==========================================
    add_section_header("1", "INTRODUCTION")
    add_body_p(
        "FitTrack is a modern, responsive, full-stack fitness and wellness tracking web application coupled with end-to-end DevOps automation. In contemporary healthcare and physical conditioning routines, individuals struggle to consistently record multi-discipline workouts (Running, Walking, Cycling, Strength Training, and Yoga), monitor daily metabolic expenditure, track hydration levels, and assess longitudinal health progress against predefined goals. Manual physical logs and disconnected spreadsheets lack instant caloric calculations, interactive KPI visualisations, and automated metric auditing."
    )
    add_body_p(
        "To resolve these operational challenges, FitTrack couples a robust single-page application (HTML5, CSS3, ES6+ JavaScript, Chart.js) and a lightweight Python Flask REST backend with SQLite persistence. Beyond application logic, the project embodies modern software engineering by fully automating the software delivery lifecycle using DevOps industry best practices. Git and GitHub govern version control; Jenkins orchestrates a 10-stage Continuous Integration and Continuous Deployment (CI/CD) pipeline; Pytest executes 25 automated unit and regression tests; Docker containerizes the application into a hardened, non-root microservice; and Ansible provides idempotent configuration management and deployment. Persistent Docker Volumes ensure zero data loss during container upgrades."
    )

    # ==========================================
    # 2. OBJECTIVES
    # ==========================================
    add_section_header("2", "OBJECTIVES")
    add_bullet_p("Interactive Fitness Management", "Enable users to log, filter, edit, and audit multi-type workouts with real-time calorie and distance calculations.")
    add_bullet_p("Visual KPI Analytics", "Provide an intuitive dashboard with daily step goal completion rings, 7-day caloric expenditure charts, and active-minute gauges.")
    add_bullet_p("Version Control & Collaboration", "Implement Git source control on GitHub with structured branching, semantic commit conventions, and issue tracking.")
    add_bullet_p("Continuous Integration Automation", "Automate code compilation, linting, and 25 Pytest validation tests using a declarative 10-stage Jenkins pipeline.")
    add_bullet_p("Microservice Containerization", "Package the application into an optimized, multi-stage Python 3.11-slim Docker container operating under a non-root system user.")
    add_bullet_p("Automated Deployment with Ansible", "Author an idempotent Ansible playbook to verify host Docker engines, prune legacy instances, bind volume mounts, and probe container health.")
    add_bullet_p("Stateful Data Persistence", "Utilize dedicated Docker named volumes (fittrack_sqlite_data) mounted to /app/data to preserve SQLite database state across container updates.")

    # ==========================================
    # 3. ABSTRACT
    # ==========================================
    add_section_header("3", "ABSTRACT")
    add_body_p(
        "FitTrack demonstrates the complete convergence of a full-stack web application with automated DevOps continuous delivery practices. The core application provides logging and analytics for daily physical activities, hydration, and goal setting, backed by a Flask API and SQLite database. Addressing the risks of manual deployment, human configuration errors, and inconsistent execution environments, this project establishes a resilient pipeline: GitHub → Jenkins → Pytest → Docker Build → Ephemeral Health Check → Ansible Deployment → Production Docker Container."
    )
    add_body_p(
        "Every code push triggers automated compilation, regression testing across 25 assertions, and container image construction. Ephemeral testing validates endpoint health on port 5055 before release. Ansible guarantees repeatable, idempotent rollouts on target hosts, binding persistent Docker volumes to maintain uninterrupted fitness logs. The project proves that modern DevOps automation substantially accelerates delivery velocity while guaranteeing high application availability and data integrity."
    )

    # ==========================================
    # 4. TECHNOLOGY STACK
    # ==========================================
    add_section_header("4", "TECHNOLOGY STACK")
    table_tech = doc.add_table(rows=1, cols=3)
    table_tech.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_hdr = table_tech.rows[0].cells
    t_hdr[0].text = "Technology"
    t_hdr[1].text = "Version / Tool"
    t_hdr[2].text = "Role in DevOps Architecture"
    for c in t_hdr:
        set_cell_background(c, "0F387A")
        set_cell_margins(c, top=100, bottom=100, left=100, right=100)
        p = c.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for r in p.runs:
            r.bold = True
            r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
            r.font.size = Pt(10)

    tech_data = [
        ("HTML5 & CSS3", "Modern Web Standards", "Semantic responsive structure, CSS variables, glassmorphic UI, responsive layouts."),
        ("JavaScript", "ES6+ Standards", "Asynchronous fetch API, DOM manipulation, Chart.js visual data rendering."),
        ("Python", "3.11 / 3.13", "Core programming language for backend RESTful services and test execution."),
        ("Flask", "3.0.0", "WSGI lightweight web framework, blueprint routing, application factory pattern."),
        ("SQLite", "3.x", "Embedded relational database engine with foreign key constraints and ACID compliance."),
        ("Gunicorn", "21.2.0", "Production-grade WSGI HTTP server with multi-worker concurrency and signal handling."),
        ("Git", "2.51.0", "Distributed version control system tracking commit histories and branching."),
        ("GitHub", "Cloud Repository", "Centralized remote Git host, branch protection, and webhook integration."),
        ("Jenkins", "2.568.1", "Continuous Integration server orchestrating automated pipeline execution."),
        ("Docker", "29.1.3", "Containerization platform packaging runtime, dependencies, and OS layers."),
        ("Pytest", "8.3.5", "Automated testing framework executing 25 unit, integration, and validation tests."),
        ("Ansible", "Core 2.10+", "Agentless configuration management engine deploying containers idempotently.")
    ]

    for row_idx, item in enumerate(tech_data):
        r_cells = table_tech.add_row().cells
        bg_col = "F7FAFC" if row_idx % 2 == 1 else "FFFFFF"
        for i, text in enumerate(item):
            r_cells[i].text = text
            set_cell_background(r_cells[i], bg_col)
            set_cell_margins(r_cells[i], top=60, bottom=60, left=80, right=80)
            p = r_cells[i].paragraphs[0]
            if i in [0, 1]:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            for r in p.runs:
                r.font.size = Pt(9.5)

    doc.add_page_break()

    # ==========================================
    # 5. SYSTEM ARCHITECTURE
    # ==========================================
    add_section_header("5", "SYSTEM ARCHITECTURE & CI/CD WORKFLOW")
    add_body_p(
        "The FitTrack system architecture unifies full-stack software development with automated continuous integration and continuous deployment infrastructure. The lifecycle follows an unbroken automated chain:"
    )
    add_bullet_p("1. Developer Workspace", "Developer modifies code locally, tests routes, and commits updates adhering to semantic Git standards.")
    add_bullet_p("2. GitHub Repository", "Code pushed to origin/main on GitHub (https://github.com/Pavithiran10/devops_cat).")
    add_bullet_p("3. Jenkins Pipeline Trigger", "Jenkins detects commits via GitHub Webhooks (githubPush()) or automatic 2-minute SCM polling (pollSCM('H/2 * * * *')).")
    add_bullet_p("4. Python Setup & Pytest", "Isolated virtual environment created; 25 test cases execute via Pytest with XML report generation.")
    add_bullet_p("5. Docker Containerization", "Multi-stage Dockerfile builds fittrack-app:latest using minimal Debian slim base layers and non-root execution.")
    add_bullet_p("6. Ephemeral Health Validation", "Test container started on ephemeral port 5055; automated probe queries /api/health before release.")
    add_bullet_p("7. Ansible Deployment", "Jenkins triggers ansible-playbook; Ansible idempotently stops legacy instances and starts production container.")
    add_bullet_p("8. Persistent SQLite Storage", "Named Docker Volume (fittrack_sqlite_data) maintains database state across container updates on port 5000.")

    add_fig_placeholder("Figure 5.1", "FitTrack End-to-End DevOps Architecture & Deployment Flow")

    # ==========================================
    # 6. MODULE 1
    # ==========================================
    add_section_header("6", "MODULE 1 — USER INTERFACE & WORKOUT LOGGING")
    add_body_p(
        "This module delivers the responsive client-side Single Page Application (SPA). Developed with Vanilla CSS3, modern semantic HTML5, and ES6+ JavaScript, it requires no heavy external frameworks, resulting in sub-millisecond page rendering and minimal overhead."
    )
    add_bullet_p("Workout Logging Modal", "Capture workout discipline (Running, Walking, Cycling, Strength Training, Yoga), duration, distance, and calories burned.")
    add_bullet_p("Real-Time KPI Cards", "Live summaries displaying total daily steps, active minutes, caloric burn, and hydration.")
    add_bullet_p("Data Filtering & Sorting", "Filter workout logs by discipline, search notes, and sort dynamically by date or duration.")
    add_bullet_p("Chart.js Visualizations", "Interactive bar charts displaying 7-day caloric expenditure and goal attainment progression.")
    add_fig_placeholder("Figure 6.1", "FitTrack Single Page Application — Dashboard & Workout Interface")
    add_fig_placeholder("Figure 6.2", "Workout Entry Modal with Client-Side Input Validation")

    # ==========================================
    # 7. MODULE 2
    # ==========================================
    add_section_header("7", "MODULE 2 — FLASK RESTFUL BACKEND & API SERVICES")
    add_body_p(
        "The backend is constructed using Python 3.11/3.13 and Flask 3.0.0 following the Application Factory pattern (create_app()). Modular Blueprints separate concerns cleanly across distinct domain boundaries:"
    )
    add_bullet_p("workouts_bp (/api/workouts)", "Handles CRUD operations for workout sessions with rigorous JSON payload validation.")
    add_bullet_p("activity_bp (/api/activity)", "Manages daily activity records including step counts, water intake, and active minutes.")
    add_bullet_p("goals_bp (/api/goals)", "Stores and updates target fitness benchmarks (daily steps, weekly workouts, water target).")
    add_bullet_p("dashboard_bp (/api/dashboard)", "Aggregates key metrics and analytics across historical logs for dashboard visualisations.")
    add_bullet_p("Health Probe (/api/health)", "Returns JSON status indicating application and SQLite connectivity for container health checks.")
    add_fig_placeholder("Figure 7.1", "Flask RESTful Blueprints Implementation in app.py")

    # ==========================================
    # 8. MODULE 3
    # ==========================================
    add_section_header("8", "MODULE 3 — SQLITE DATABASE MANAGEMENT & SCHEMA")
    add_body_p(
        "Data persistence is provided by an embedded SQLite 3 database (fittrack.db). Foreign keys (PRAGMA foreign_keys = ON) enforce referential integrity. Database teardown is registered with Flask's application context to prevent connection leaks."
    )
    add_bullet_p("workouts table", "Stores id, workout_type, duration (minutes), calories, distance, workout_date, notes, created_at.")
    add_bullet_p("daily_activity table", "Tracks id, activity_date (UNIQUE), steps, distance, calories, water_intake, active_minutes.")
    add_bullet_p("goals table", "Stores id, daily_step_goal, weekly_workout_goal, daily_water_goal, updated_at.")
    add_bullet_p("Automated Seeding", "init_db() verifies table existence on startup and inserts realistic sample records for immediate evaluation.")
    add_fig_placeholder("Figure 8.1", "SQLite Schema and Relational Table Structure")

    # ==========================================
    # 9. MODULE 4
    # ==========================================
    add_section_header("9", "MODULE 4 — GIT & GITHUB SOURCE CONTROL")
    add_body_p(
        "Source code lifecycle and collaboration are governed using Git locally and hosted on GitHub under the repository Pavithiran10/devops_cat. Structured commits follow conventional commit standards (feat, fix, ci, test, docs)."
    )
    add_bullet_p("Remote Origin", "Configured to https://github.com/Pavithiran10/devops_cat.git on branch main.")
    add_bullet_p("Ignored Artifacts", ".gitignore excludes virtual environments (.jenkins_venv, venv), bytecode (__pycache__), and local databases.")
    add_bullet_p("Commit Traceability", "Full audit log tracking fixes, Docker container hardening, and cross-platform Jenkinsfile adaptations.")
    add_fig_placeholder("Figure 9.1", "GitHub Remote Repository Overview (Pavithiran10/devops_cat)")

    # ==========================================
    # 10. MODULE 5
    # ==========================================
    add_section_header("10", "MODULE 5 — DOCKER CONTAINERIZATION & HARDENING")
    add_body_p(
        "The application is packaged into a production Docker image using a hardened, multi-stage Dockerfile built upon python:3.11-slim. Security and operational best practices include:"
    )
    add_bullet_p("Non-Root Security", "A dedicated system user fittrack (UID 1001) is provisioned to prevent container breakout vulnerabilities.")
    add_bullet_p("Gunicorn WSGI Server", "Serves requests across 3 concurrent worker processes with a 120-second timeout.")
    add_bullet_p("Integrated Healthcheck", "Periodic query (HEALTHCHECK --interval=30s) testing curl -f http://localhost:5000/api/health.")
    add_bullet_p("Persistent Volume Mount", "Volume /app/data declared to isolate database storage from container layer lifecycles.")
    add_fig_placeholder("Figure 10.1", "Multi-Stage Dockerfile Implementation")
    add_fig_placeholder("Figure 10.2", "Running Docker Container and Healthcheck Status")

    doc.add_page_break()

    # ==========================================
    # 11. MODULE 6
    # ==========================================
    add_section_header("11", "MODULE 6 — JENKINS CI/CD AUTOMATION PIPELINE")
    add_body_p(
        "The continuous delivery pipeline is codified in a declarative Jenkinsfile containing 10 automated stages. Cross-platform execution (isUnix()) ensures seamless operation on both Windows (bat) and Linux (sh) build nodes."
    )
    add_bullet_p("Stage 1: Checkout Code", "Automated retrieval of revision from GitHub origin/main.")
    add_bullet_p("Stage 2: Setup Python", "Virtual environment creation (.jenkins_venv) with fallback PATH discovery.")
    add_bullet_p("Stage 3: Install Dependencies", "Upgrade pip and install pinned dependencies from requirements.txt.")
    add_bullet_p("Stage 4: Run Pytest", "Execute 25 automated tests; publish test results via JUnit XML.")
    add_bullet_p("Stage 5: Syntax Checks", "Bytecode compilation check across core Python modules.")
    add_bullet_p("Stage 6: Build Docker Image", "Build production image fittrack-app:latest.")
    add_bullet_p("Stage 7: Health-Check Validation", "Launch ephemeral container on port 5055 and verify /api/health probe.")
    add_bullet_p("Stage 8: Tag Docker Image", "Tag release image with build number.")
    add_bullet_p("Stage 9: Push Docker Image", "Optional authenticated registry upload to Docker Hub.")
    add_bullet_p("Stage 10: Trigger Ansible", "Trigger automated container deployment.")
    add_fig_placeholder("Figure 11.1", "10-Stage Jenkins Declarative Pipeline Execution")
    add_fig_placeholder("Figure 11.2", "Jenkins Console Output — Successful Build & Pytest Execution")

    # ==========================================
    # 12. MODULE 7
    # ==========================================
    add_section_header("12", "MODULE 7 — AUTOMATED TESTING (PYTEST SUITE)")
    add_body_p(
        "Quality assurance is enforced through a 25-case Pytest test suite located in tests/. Tests execute against isolated in-memory or temporary file SQLite instances managed through conftest.py fixtures."
    )
    add_bullet_p("test_workouts.py (13 tests)", "Verifies workout retrieval, ID search, creation, 400 validation for missing/negative values, updates, deletes, and sorting.")
    add_bullet_p("test_activity.py (5 tests)", "Tests daily activity retrieval, upsert semantics, and validation.")
    add_bullet_p("test_goals.py (3 tests)", "Tests goal fetching, boundary validation, and goal updates.")
    add_bullet_p("test_dashboard.py (3 tests)", "Validates KPI summary math, 7-day metric aggregation, and demo reset.")
    add_bullet_p("test_health.py (1 test)", "Validates /api/health returns HTTP 200 and 'healthy' status.")
    add_fig_placeholder("Figure 12.1", "Pytest 25/25 Passing Test Execution Output")

    # ==========================================
    # 13. MODULE 8
    # ==========================================
    add_section_header("13", "MODULE 8 — ANSIBLE DEPLOYMENT AUTOMATION")
    add_body_p(
        "Deployment automation is governed by ansible/playbook.yml. The playbook executes idempotently, guaranteeing that rerunning deployment causes no downtime or state corruption."
    )
    add_bullet_p("Task 1-3: Host Preparation", "Verify Docker runtime; ensure application root and /app/data exist with 0777 permissions.")
    add_bullet_p("Task 4-5: Image & Container Lifecycle", "Inspect local image; stop and remove outdated container instances gracefully.")
    add_bullet_p("Task 6: Container Instantiation", "Run updated container with restart policy (unless-stopped), port 5000:5000, and volume mounting.")
    add_bullet_p("Task 7-8: Health Check Verification", "Query http://localhost:5000/api/health with automatic retries until healthy.")
    add_fig_placeholder("Figure 13.1", "Ansible Deployment Playbook and Execution Output")

    # ==========================================
    # 14. MODULE 9
    # ==========================================
    add_section_header("14", "MODULE 9 — PERSISTENT STORAGE (DOCKER VOLUME)")
    add_body_p(
        "To prevent data loss during container recreation, Docker named volumes are employed. The volume fittrack_sqlite_data binds to container path /app/data, where fittrack.db resides."
    )
    add_bullet_p("Persistence Proof", "When containers are stopped (docker stop) and removed (docker rm), data inside fittrack_sqlite_data remains intact.")
    add_bullet_p("Volume Inspection", "docker volume inspect fittrack_sqlite_data verifies host mount points and integrity.")
    add_fig_placeholder("Figure 14.1", "Docker Volume Configuration & Database Persistence Evidence")

    # ==========================================
    # 15. MODULE 10
    # ==========================================
    add_section_header("15", "MODULE 10 — ANALYTICS ENGINE & GOAL MANAGEMENT")
    add_body_p(
        "The analytics engine (services/analytics.py) computes aggregate physical KPIs in real time. Calculations combine workout caloric burn with daily ambient expenditure, evaluate step goal completion ratios, and track weekly workout consistency."
    )
    add_fig_placeholder("Figure 15.1", "Real-Time Health Metrics and Progress Visualisations")

    # ==========================================
    # 16. MODULE 11
    # ==========================================
    add_section_header("16", "MODULE 11 — COMPLETE CI/CD INTEGRATION")
    add_body_p(
        "This module harmonizes all individual tools into an end-to-end automated pipeline. Code changes pushed to GitHub automatically traverse Jenkins compilation, Pytest verification, Docker image packaging, ephemeral testing, and Ansible production deployment."
    )
    add_fig_placeholder("Figure 16.1", "End-to-End Pipeline Stage View in Jenkins")

    # ==========================================
    # 17. MODULE 12
    # ==========================================
    add_section_header("17", "MODULE 12 — APPLICATION & DEPLOYMENT VERIFICATION")
    add_body_p(
        "Comprehensive verification audits confirmed zero defects across all functional layers: container ports active, health endpoints returning HTTP 200, workouts logged and persisted across restarts, and all 25 automated tests passing."
    )
    add_fig_placeholder("Figure 17.1", "Live Verification of Running FitTrack Application on Port 5000")

    doc.add_page_break()

    # ==========================================
    # 18. RESULTS AND OUTPUT
    # ==========================================
    add_section_header("18", "RESULTS AND OUTPUT")
    add_body_p(
        "The implemented system successfully fulfilled every requirement set forth in the 23IT723 DevOps Laboratory syllabus:"
    )
    add_bullet_p("Application Delivery", "Full-stack fitness tracking web application operational with zero console errors.")
    add_bullet_p("Testing Verification", "25 out of 25 automated Pytest test cases passed cleanly in 0.79s.")
    add_bullet_p("Container Validation", "Hardened Docker image created (fittrack:latest) operating under non-root security.")
    add_bullet_p("Continuous Integration", "10-stage Jenkins pipeline executes seamlessly with automated webhook and polling triggers.")
    add_bullet_p("Deployment Automation", "Ansible playbook executes idempotently with automated health checks.")
    add_bullet_p("Data Persistence", "SQLite database verified persistent across container termination and rebuilds.")

    # ==========================================
    # 19. COMMANDS USED
    # ==========================================
    add_section_header("19", "COMMANDS USED (COMPREHENSIVE CHEATSHEET)")
    add_body_p("The following commands constitute the operational runbook for reproducing all project stages:")

    table_cmd = doc.add_table(rows=1, cols=3)
    table_cmd.alignment = WD_TABLE_ALIGNMENT.CENTER
    c_hdr = table_cmd.rows[0].cells
    c_hdr[0].text = "Category"
    c_hdr[1].text = "Command"
    c_hdr[2].text = "Purpose / Outcome"
    for c in c_hdr:
        set_cell_background(c, "0F387A")
        set_cell_margins(c, top=80, bottom=80, left=80, right=80)
        p = c.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for r in p.runs:
            r.bold = True
            r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
            r.font.size = Pt(9.5)

    commands_list = [
        ("Git", "git init", "Initialise local repository."),
        ("Git", "git add . && git commit -m '...'", "Stage and commit changes with semantic messages."),
        ("Git", "git remote add origin https://github.com/Pavithiran10/devops_cat.git", "Connect remote GitHub repository."),
        ("Git", "git push -u origin main", "Publish commits to GitHub main branch."),
        ("Pytest", "pytest -v", "Execute full 25-case test suite with verbose output."),
        ("Pytest", "pytest -v --pdb", "Execute tests with interactive post-mortem debugging."),
        ("Docker", "docker compose up --build -d", "Build image and start container in detached mode."),
        ("Docker", "docker ps", "Inspect running containers and health probe status."),
        ("Docker", "docker logs -f fittrack-app", "Stream live Gunicorn container output logs."),
        ("Docker", "curl http://localhost:5000/api/health", "Verify container health check response."),
        ("Docker", "docker volume ls", "List persistent Docker volumes."),
        ("Docker", "docker volume inspect fittrack_sqlite_data", "Verify volume mount details."),
        ("Ansible", "ansible-playbook -i ansible/inventory.ini ansible/playbook.yml", "Execute automated idempotent container deployment."),
        ("Database", "sqlite3 fittrack.db '.tables'", "Audit database schema and tables.")
    ]

    for row_idx, item in enumerate(commands_list):
        r_cells = table_cmd.add_row().cells
        bg_col = "F7FAFC" if row_idx % 2 == 1 else "FFFFFF"
        for i, text in enumerate(item):
            r_cells[i].text = text
            set_cell_background(r_cells[i], bg_col)
            set_cell_margins(r_cells[i], top=50, bottom=50, left=60, right=60)
            p = r_cells[i].paragraphs[0]
            if i == 0:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            for r in p.runs:
                r.font.size = Pt(9)
                if i == 1:
                    r.font.name = 'Consolas'

    # ==========================================
    # 20. ADVANTAGES
    # ==========================================
    add_section_header("20", "ADVANTAGES")
    add_bullet_p("Zero Deployment Drift", "Docker containerization guarantees identical execution across development, CI, and production.")
    add_bullet_p("Rapid Defect Detection", "Automated Pytest regression suite catches logic defects before code reaches staging.")
    add_bullet_p("Hands-Free CI/CD", "Automated GitHub webhooks and polling trigger pipeline execution with zero manual effort.")
    add_bullet_p("Production-Grade Security", "Container executes as a dedicated non-root user (fittrack:1001) preventing privilege escalation.")
    add_bullet_p("Idempotent Rollouts", "Ansible playbooks prevent deployment corruption by gracefully replacing containers only when needed.")
    add_bullet_p("Reliable Data Persistence", "Isolated Docker named volumes prevent SQLite data loss during image updates.")

    # ==========================================
    # 21. LIMITATIONS
    # ==========================================
    add_section_header("21", "LIMITATIONS")
    add_bullet_p("Single-Node Storage", "SQLite is an embedded database suited for single-container architectures rather than distributed write clusters.")
    add_bullet_p("Authentication Scope", "Current implementation focuses on single-user tracking without multi-tenant OAuth2/JWT authorization.")
    add_bullet_p("Local Host Execution", "Demonstrated on local host Docker runtime rather than distributed Kubernetes clusters.")

    # ==========================================
    # 22. FUTURE ENHANCEMENTS
    # ==========================================
    add_section_header("22", "FUTURE ENHANCEMENTS")
    add_bullet_p("PostgreSQL Migration", "Transition from SQLite to PostgreSQL for distributed multi-tenant concurrency.")
    add_bullet_p("Kubernetes Deployment", "Author Helm charts and Kubernetes manifests with PersistentVolumeClaims and Ingress controllers.")
    add_bullet_p("Prometheus & Grafana", "Instrument Flask endpoints with Prometheus metrics exporters for real-time monitoring.")
    add_bullet_p("JWT User Authentication", "Add role-based authentication and secure session tokens for multi-user workout isolation.")

    # ==========================================
    # 23. CONCLUSION
    # ==========================================
    add_section_header("23", "CONCLUSION")
    add_body_p(
        "The FitTrack project successfully demonstrates the design, development, and automated continuous delivery of a modern fitness tracking web application in full compliance with the 23IT723 DevOps Laboratory syllabus. By integrating Python Flask and SQLite with Git, GitHub, Jenkins, Docker, Pytest, and Ansible, the project establishes a robust, enterprise-grade development and deployment lifecycle."
    )
    add_body_p(
        "Automated Pytest testing across 25 assertions ensures high code quality, multi-stage Docker containerization guarantees portability and security, and Ansible automation ensures repeatable, idempotent deployments. Persistent Docker Volumes ensure that fitness records survive container upgrades without interruption. The complete pipeline from commit to verified deployment demonstrates the practical power of DevOps engineering in modern software delivery."
    )

    output_path = "FitTrack_DevOps_Project_Report.docx"
    doc.save(output_path)
    print(f"Report successfully generated at: {output_path}")

if __name__ == '__main__':
    create_report()
