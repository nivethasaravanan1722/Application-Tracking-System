import json
import os
import glob

# Define job-specific required skills and keywords
REQUIRED_SKILLS = {"Python", "Machine Learning", "Data Science", "SQL", "JavaScript", "Cloud Computing"}
KEYWORDS = {"AI", "Deep Learning", "AWS", "Leadership", "Project Management"}

def calculate_experience_score(experience):
    """Calculate experience score based on the number of job titles listed."""
    if not experience:
        return 0
    max_experience = 10  # Assume 10+ years is full score
    years = len(experience)  # Each job entry adds to experience
    return min((years / max_experience) * 100, 100)

def calculate_skills_score(skills):
    """Calculate skill match score based on required job skills."""
    if not skills:
        return 0
    matched_skills = len(set(skills) & REQUIRED_SKILLS)
    return (matched_skills / len(REQUIRED_SKILLS)) * 100

def calculate_education_score(education):
    """Give higher weight to degrees that match the field."""
    if not education:
        return 0
    for degree in education:
        if "Computer Science" in degree or "Engineering" in degree:
            return 100  # Full score for relevant degrees
    return 50  # Partial score for other degrees

def calculate_certification_score(certifications):
    """Score based on number of relevant certifications."""
    if not certifications:
        return 0
    return min(len(certifications) * 20, 100)  # More certifications = higher score

def calculate_projects_score(projects):
    """Score based on number of projects."""
    if not projects:
        return 0
    return min(len(projects) * 25, 100)  # More projects = higher score

def calculate_social_media_score(social_links):
    """Give score based on social media presence."""
    if not social_links:
        return 0
    score = 0
    if "LinkedIn" in social_links:
        score += 40
    if "GitHub" in social_links:
        score += 40
    if "Portfolio" in social_links:
        score += 20
    return min(score, 100)

def calculate_keyword_match_score(text):
    """Calculate score based on presence of job-related keywords."""
    if not text:
        return 0
    matched_keywords = len(set(text.split()) & KEYWORDS)
    return (matched_keywords / len(KEYWORDS)) * 100

def score_candidate(json_file):
    """Calculate ATS score for a candidate based on the extracted JSON data."""
    with open(json_file, "r", encoding="utf-8") as file:
        data = json.load(file)

    experience_score = calculate_experience_score(data.get("experience", []))
    skills_score = calculate_skills_score(data.get("skills", []))
    education_score = calculate_education_score(data.get("education", []))
    certification_score = calculate_certification_score(data.get("certifications", []))
    projects_score = calculate_projects_score(data.get("projects", []))
    social_score = calculate_social_media_score(data.get("social_links", {}))
    keyword_score = calculate_keyword_match_score(" ".join(data.get("experience", []) + data.get("education", [])))

    final_score = (
        (experience_score * 0.30) +
        (skills_score * 0.25) +
        (education_score * 0.15) +
        (certification_score * 0.10) +
        (projects_score * 0.10) +
        (social_score * 0.05) +
        (keyword_score * 0.05)
    )

    return {
        "resume_file": os.path.basename(json_file),
        "name": data.get("name", "Unknown"),
        "score": round(final_score, 2)
    }

def process_resumes(json_folder="parsed_resumes"):
    """Process all JSON resume files and print structured results."""
    json_files = glob.glob(f"{json_folder}/*.json")
    results = []

    for json_file in json_files:
        candidate_data = score_candidate(json_file)
        results.append(candidate_data)

    # Print structured results
    print("\n🏆 Candidate Scoring Results 🏆\n")
    for result in sorted(results, key=lambda x: x["score"], reverse=True):
        print(f"📄 Resume File: {result['resume_file']}")
        print(f"👤 Name: {result['name']}")
        print(f"⭐ ATS Score: {result['score']}%")
        print("-" * 40)

# Example Usage
process_resumes()
