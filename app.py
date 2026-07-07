import html
import re
from io import BytesIO

import streamlit as st
from PyPDF2 import PdfReader

st.set_page_config(page_title="AI Resume Analyzer", page_icon="📄", layout="wide")

st.markdown(
    """
    <style>
        .block-container { padding-top: 1.2rem; }
        .hero {
            background: linear-gradient(135deg, #1d4ed8, #2563eb);
            color: white;
            border-radius: 18px;
            padding: 1.2rem 1.4rem;
            margin-bottom: 1rem;
            box-shadow: 0 10px 30px rgba(37, 99, 235, 0.18);
        }
        .card {
            background: rgba(255, 255, 255, 0.9);
            border: 1px solid #e2e8f0;
            border-radius: 14px;
            padding: 1rem;
            box-shadow: 0 8px 24px rgba(15, 23, 42, 0.06);
        }
        .skill-chip {
            display: inline-block;
            padding: 0.35rem 0.7rem;
            margin: 0.25rem 0.25rem 0.25rem 0;
            border-radius: 999px;
            background: #2563eb;
            color: white;
            font-size: 0.9rem;
            font-weight: 600;
        }
        mark {
            background-color: #fde68a;
            color: #111827;
            padding: 0 0.2rem;
            border-radius: 0.25rem;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="hero">
        <h2 style="margin-bottom:0.2rem;">🤖 AI Resume Analyzer</h2>
        <p style="margin:0; font-size:1rem; opacity:0.95;">
            Upload a PDF resume to discover the strongest technical skills and estimate how well it matches your target profile.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

SKILL_DATA = {
    "Python": {"keywords": ["python", "py", "python3"]},
    "Java": {"keywords": ["java", "jdk", "jvm"]},
    "JavaScript": {"keywords": ["javascript", "js", "node.js"]},
    "TypeScript": {"keywords": ["typescript", "ts"]},
    "C++": {"keywords": ["c++", "cpp"]},
    "C#": {"keywords": ["c#", "csharp"]},
    "React": {"keywords": ["react", "reactjs"]},
    "Django": {"keywords": ["django"]},
    "Flask": {"keywords": ["flask"]},
    "FastAPI": {"keywords": ["fastapi"]},
    "SQL": {"keywords": ["sql", "database"]},
    "MySQL": {"keywords": ["mysql"]},
    "PostgreSQL": {"keywords": ["postgresql", "postgres"]},
    "MongoDB": {"keywords": ["mongodb"]},
    "Azure": {"keywords": ["azure", "microsoft azure"]},
    "AWS": {"keywords": ["aws", "amazon web services"]},
    "Docker": {"keywords": ["docker", "containerization"]},
    "Kubernetes": {"keywords": ["kubernetes", "k8s"]},
    "Machine Learning": {"keywords": ["machine learning", "ml"]},
    "Artificial Intelligence": {"keywords": ["artificial intelligence", "ai"]},
    "Data Science": {"keywords": ["data science", "data scientist"]},
    "TensorFlow": {"keywords": ["tensorflow"]},
    "PyTorch": {"keywords": ["pytorch"]},
    "Git": {"keywords": ["git", "github"]},
    "Linux": {"keywords": ["linux", "ubuntu"]},
    "DevOps": {"keywords": ["devops", "ci/cd"]},
    "REST APIs": {"keywords": ["rest api", "restapis", "rest"]},
    "GraphQL": {"keywords": ["graphql"]},
}

JOB_ROLE_RULES = [
    ("Data Scientist", ["machine learning", "artificial intelligence", "data science", "python", "tensorflow", "pytorch"]),
    ("Backend Developer", ["python", "django", "flask", "fastapi", "sql", "rest api", "api"]),
    ("Full Stack Developer", ["javascript", "typescript", "react", "python", "sql", "api"]),
    ("DevOps Engineer", ["docker", "kubernetes", "aws", "azure", "linux", "devops", "git"]),
    ("Cloud Engineer", ["aws", "azure", "docker", "kubernetes", "linux"]),
]


def extract_text_from_pdf(uploaded_file) -> str:
    reader = PdfReader(uploaded_file)
    text_chunks = [page.extract_text() or "" for page in reader.pages]
    return "\n".join(text_chunks)


def normalize_text(text: str) -> str:
    return re.sub(r"[^a-z0-9+\s]", " ", text.lower())


def find_matched_skills(text: str):
    normalized_text = normalize_text(text)
    matched_skills = []
    total_possible = 0
    matched_points = 0

    for skill, config in SKILL_DATA.items():
        matched_keywords = []
        for keyword in config["keywords"]:
            normalized_keyword = normalize_text(keyword)
            if not normalized_keyword:
                continue
            pattern = rf"(?<![a-z0-9]){re.escape(normalized_keyword)}(?![a-z0-9])"
            if re.search(pattern, normalized_text):
                matched_keywords.append(keyword)

        if matched_keywords:
            confidence = min(100, round((len(matched_keywords) / len(config["keywords"])) * 100, 1))
            matched_skills.append({
                "skill": skill,
                "score": len(matched_keywords),
                "confidence": confidence,
                "keywords": matched_keywords,
            })
            matched_points += len(matched_keywords)

        total_possible += len(config["keywords"])

    percentage = round((matched_points / total_possible) * 100, 1) if total_possible else 0
    return matched_skills, percentage


def suggest_job_role(matched_skills):
    matched_terms = {keyword.lower() for item in matched_skills for keyword in item["keywords"]}
    scores = []

    for role, terms in JOB_ROLE_RULES:
        role_score = sum(1 for term in terms if term.lower() in matched_terms)
        if role_score > 0:
            scores.append((role_score, role))

    if not scores:
        return "General Software Engineer"

    _, best_role = max(scores, key=lambda item: (item[0], item[1]))
    return best_role


def build_report(matched_skills, score, best_role, candidate_name="Candidate") -> str:
    lines = []
    lines.append("AI Resume Analyzer Report")
    lines.append(f"Candidate: {candidate_name}")
    lines.append(f"Match Percentage: {score}%")
    lines.append(f"Best Match Job Role: {best_role}")
    lines.append("")
    lines.append("Matched Skills:")
    for item in matched_skills:
        lines.append(f"- {item['skill']}: confidence {item['confidence']}%")
    return "\n".join(lines)


def download_report(matched_skills, score, best_role):
    report_text = build_report(matched_skills, score, best_role)
    buffer = BytesIO(report_text.encode("utf-8"))
    return buffer


def highlight_matches(text: str, matched_skills) -> str:
    preview_text = text[:4000] if text else ""
    if not preview_text:
        return "<em>No text could be extracted from the PDF.</em>"

    keywords = [keyword for item in matched_skills for keyword in item["keywords"]]
    highlighted_text = html.escape(preview_text).replace("\n", "<br>")

    if not keywords:
        return highlighted_text

    for keyword in sorted(set(keywords), key=len, reverse=True):
        pattern = rf"(?<![a-z0-9]){re.escape(keyword)}(?![a-z0-9])"
        highlighted_text = re.sub(
            pattern,
            lambda match: f"<mark>{html.escape(match.group(0))}</mark>",
            highlighted_text,
            flags=re.IGNORECASE,
        )

    return highlighted_text


uploaded_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])

if uploaded_file is not None:
    with st.spinner("Analyzing the resume and scoring the technical match..."):
        raw_text = extract_text_from_pdf(uploaded_file)
        matched_skills, score = find_matched_skills(raw_text)
        best_role = suggest_job_role(matched_skills)

    st.success("Resume analyzed successfully")

    left_col, right_col = st.columns([1.35, 0.85])

    with left_col:
        st.subheader("Resume Preview")
        st.markdown(f"<div class='card'>{highlight_matches(raw_text, matched_skills)}</div>", unsafe_allow_html=True)

    with right_col:
        st.subheader("Skill Match Results")
        st.metric("Match Percentage", f"{score}%")
        st.metric("Matched Skills", len(matched_skills))
        st.progress(min(score / 100, 1.0))
        st.info(f"Best Match Job Role: **{best_role}**")

        if matched_skills:
            st.caption("Highlighted keywords are weighted for better relevance")
            skill_html = "".join(f"<span class='skill-chip'>{item['skill']}</span>" for item in matched_skills)
            st.markdown(skill_html, unsafe_allow_html=True)

            st.markdown("### Detailed Matches")
            for item in matched_skills:
                st.markdown(f"- **{item['skill']}** · {item['score']} keyword match(es) · confidence **{item['confidence']}%**")

            report_buffer = download_report(matched_skills, score, best_role)
            st.download_button(
                label="Download Report",
                data=report_buffer.getvalue(),
                file_name="resume_analysis_report.txt",
                mime="text/plain",
            )
        else:
            st.info("No strong skill matches were found. Add more specific terms such as Python, SQL, Docker, React, Azure, or AWS.")

else:
    st.info("Please upload a PDF resume to begin analysis.")
