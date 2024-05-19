import pdfplumber
import re

def extract_text_from_pdf(pdf_file):
    with pdfplumber.open(pdf_file) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text()
    return text

def preprocess_text(text):
    # Remove extra whitespaces and newlines
    text = " ".join(text.split())
    return text


def parse_resume(text):
    # Regular expressions for extracting name, email, and phone number
    name_pattern = re.compile(r'(?i)(\b[A-Z][a-z]*\s[A-Z][a-z]*\b)')
    email_pattern = re.compile(r'[\w\.-]+@[\w\.-]+')
    phone_pattern = re.compile(r'[\+\(]?[1-9][0-9 .\-\(\)]{8,}[0-9]')
    # categories = {
    #     "Programming Languages": re.compile(r'(?i)Programming Languages:\s*(.*?)(?=\s*•|$)'),
    #     "Frontend": re.compile(r'(?i)Frontend:\s*(.*?)(?=\s*•|$)'),
    #     "Database- Tools": re.compile(r'(?i)Database- Tools:\s*(.*?)(?=\s*•|$)'),
    #     "Concepts Known": re.compile(r'(?i)Concepts Known:\s*(.*?)(?=\s*•|$)'),
    #     # Add more categories as needed
    # }

    # skills_pattern = re.compile(r'(?i)SKILLS(?:.*?)(\n•\s*[\w\s,.-]+)')
    linkedin_pattern = re.compile(r'(?i)linkedin\.com\/\S+')
    github_pattern = re.compile(r'(?i)github\.com\/\S+')
    portfolio_pattern = re.compile(r'(?i)portfolio link:?\s*(https?://\S+)')

    # Extract skills for each category
    # skills = {}
    # for category, pattern in categories.items():
    #     match = pattern.search(text)
    #     if match:
    #         # Split the matched text by commas and strip whitespace
    #         skills[category] = [skill.strip() for skill in match.group(1).split(',') if skill.strip()]
    #     else:
    #         skills[category] = []

    # Extract name
    name_match = name_pattern.search(text)
    name = name_match.group(1) if name_match else None

    # Extract email
    email_match = email_pattern.search(text)
    email = email_match.group() if email_match else None

    # Extract phone number
    phone_match = phone_pattern.search(text)
    phone = phone_match.group() if phone_match else None

    linkedin_match = linkedin_pattern.search(text)
    linkedin = linkedin_match.group() if linkedin_match else None

    github_match = github_pattern.search(text)
    github = github_match.group() if github_match else None

    portfolio_match = portfolio_pattern.search(text)
    protfolio = portfolio_match.group() if portfolio_match else None



    # skills_match = skills_pattern.search(text)
    # skills_list=[]
    # if skills_match:
    #     skills_text = skills_match.group(1)
    #     # Split the skills text into individual skills
    #     skills_list = [skill.strip() for skill in re.split(r'\n•\s*', skills_text) if skill.strip()]
    # else:
    #     print("Skills section not found")


    return {"Name": name, "Email": email, "Phone": phone, "Linkedin": linkedin, "Github":github, "Portfolio": protfolio}


def get_skills(text):
    # Find the index of "SKILLS" in the text
    skills_index = text.find("SKILLS")
    if skills_index == -1:
        return []  # Return an empty list if "SKILLS" is not found

    # Find the end of the "SKILLS" section or the start of the next section
    next_section_start_index = text.find("\n\n", skills_index)
    if next_section_start_index == -1:
        next_section_start_index = len(text)

    # Extract the "SKILLS" section text
    skills_section = text[skills_index:next_section_start_index]

    # Split the "SKILLS" section text into lines
    skills_lines = []
    for line in skills_section.split("\n"):
        line_lower = line.strip().lower()
        if any(line_lower.startswith(section.lower()) for section in ("projects", "certifications", "education", "co-curricular activities")):
            break  # Stop processing once a new section or category marker is encountered
        if line.strip():  # Skip empty lines
            skills_lines.append(line.strip("• ").strip())

    return skills_lines


pdf_file = "shreerakshapbhat(1NH20IS158)resume.pdf"
text = extract_text_from_pdf(pdf_file)
cleaned_text = preprocess_text(text)
parsed_data=parse_resume(cleaned_text)
# print(cleaned_text)
if parsed_data["Portfolio"]:
    parsed_data["Portfolio"] = parsed_data["Portfolio"].replace("Portfolio link: ", "")
skills_data=get_skills(text)
print(parsed_data)
print(skills_data)
skill_needed = ['HTML','CSS','C','Python']
length=len(skill_needed)
count=0
for skill in skill_needed:
    for skill_need in skills_data:
        if skill in skill_need:
            print(skill)
            count+=1
            break
if count>=(length/2) :
    print("You are eligible for this job")
else:
    print("sorry try elsewhere")
