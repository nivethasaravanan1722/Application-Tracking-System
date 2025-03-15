import pdfplumber
import re
import spacy
import json
import os
import glob

# Load NLP model
nlp = spacy.load("en_core_web_sm")

def extract_text(pdf_path):
    """Extract text from a PDF using pdfplumber"""
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text.strip()

def extract_email(text):
    """Extract email addresses using regex"""
    match = re.search(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", text)
    return match.group() if match else None

def extract_phone(text):
    """Extract phone numbers"""
    match = re.search(r"\+?\d{1,3}[-.\s]?\d{3}[-.\s]?\d{3,4}[-.\s]?\d{4}", text)
    return match.group() if match else None

def extract_name(text):
    """Extract full name using NLP"""
    doc = nlp(text)
    names = [ent.text.strip() for ent in doc.ents if ent.label_ == "PERSON" and len(ent.text.split()) > 1]
    return names[0] if names else None

def extract_experience(text):
    """Extract work experience details"""
    experience_keywords = ["Experience", "Intern", "Work", "Company", "Project", "Employment", "Job", "Position", "Responsibilities"]
    lines = text.split("\n")
    experience = [line.strip() for line in lines if any(keyword in line for keyword in experience_keywords)]
    return experience if experience else None

def extract_education(text):
    """Extract education details"""
    education_keywords = ["Bachelor", "Master", "B.E", "B.Tech", "M.Tech", "Engineering", "Degree", "University", "College", "School", "CGPA"]
    lines = text.split("\n")
    education = [line.strip() for line in lines if any(keyword in line for keyword in education_keywords)]
    return education if education else None

def extract_skills(text):
    """Extract skills using predefined list"""
    skills_list = ["Python", "Java", "C++", "Machine Learning", "Artificial Intelligence", "Data Science", "React", "SQL", "JavaScript",
                   "HTML", "CSS", "Node.js", "Angular", "Django", "Flask", "Excel", "Power BI", "Cloud Computing", "AWS", "Azure"]
    found_skills = [skill for skill in skills_list if skill.lower() in text.lower()]
    return found_skills if found_skills else None

def extract_certifications(text):
    """Extract certifications"""
    certification_keywords = ["Certification", "Certified", "Course", "Diploma", "Training"]
    lines = text.split("\n")
    certifications = [line.strip() for line in lines if any(keyword in line for keyword in certification_keywords)]
    return certifications if certifications else None

def extract_projects(text):
    """Extract projects"""
    project_keywords = ["Project", "Research", "Developed", "Built"]
    lines = text.split("\n")
    projects = [line.strip() for line in lines if any(keyword in line for keyword in project_keywords)]
    return projects if projects else None

def extract_languages(text):
    """Extract languages"""
    language_list = ["English", "Spanish", "French", "German", "Chinese", "Hindi", "Portuguese", "Russian", "Arabic", "Japanese"]
    found_languages = [lang for lang in language_list if lang.lower() in text.lower()]
    return found_languages if found_languages else None

def extract_social_links(text):
    """Extract social media and personal website links"""
    social_patterns = {
        "LinkedIn": r"(https?:\/\/)?(www\.)?linkedin\.com\/[a-zA-Z0-9\-_/]+",
        "GitHub": r"(https?:\/\/)?(www\.)?github\.com\/[a-zA-Z0-9\-_/]+",
        "Twitter": r"(https?:\/\/)?(www\.)?twitter\.com\/[a-zA-Z0-9_]+",
        "Portfolio": r"(https?:\/\/)?(www\.)?[a-zA-Z0-9\-]+\.(com|net|org|io|dev)[a-zA-Z0-9\-_/]*"
    }

    social_links = {}
    for platform, pattern in social_patterns.items():
        matches = re.findall(pattern, text)
        if matches:
            social_links[platform] = matches[0]  # Extract first valid link

    return social_links if social_links else None

def sanitize_filename(name, phone, email):
    """Sanitize and make filenames unique"""
    name = name.replace("\n", " ").strip() if name else "Unknown"
    name = re.sub(r"[^\w\s-]", "", name).replace(" ", "_")

    # Use phone's last 4 digits if available, otherwise use email identifier
    unique_id = ""
    if phone:
        unique_id = phone[-4:]  # Last 4 digits of phone number
    elif email:
        unique_id = email.split("@")[0][:4]  # First 4 characters of email username

    return f"{name}_{unique_id}" if unique_id else name

def extract_data_from_pdf(pdf_path):
    """Extract structured data from PDF for ATS"""
    text = extract_text(pdf_path)
    
    name = extract_name(text)
    email = extract_email(text)
    phone = extract_phone(text)
    
    data = {
        "name": name,
        "email": email,
        "phone": phone,
        "experience": extract_experience(text),
        "education": extract_education(text),
        "skills": extract_skills(text),
        "certifications": extract_certifications(text),
        "projects": extract_projects(text),
        "languages": extract_languages(text),
        "social_links": extract_social_links(text)
    }
    
    return {key: value for key, value in data.items() if value is not None}, name, phone, email

def process_multiple_resumes(input_folder="input_resumes", output_folder="parsed_resumes"):
    """Process all PDFs in a folder and save extracted data"""
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    pdf_files = glob.glob(os.path.join(input_folder, "*.pdf"))
    
    if not pdf_files:
        print("⚠️ No PDF files found in the folder!")
        return

    print(f"📂 Found {len(pdf_files)} resumes. Processing...\n")

    for pdf_file in pdf_files:
        print(f"📄📃📄 Processing: {os.path.basename(pdf_file)}")
        extracted_data, name, phone, email = extract_data_from_pdf(pdf_file)
        unique_filename = sanitize_filename(name, phone, email)
        json_filename = os.path.join(output_folder, f"{unique_filename}.json")

        with open(json_filename, "w", encoding="utf-8") as json_file:
            json.dump(extracted_data, json_file, indent=4)

        print(f"✅ Extracted data saved to: {json_filename}")

# Run the processing
process_multiple_resumes()
