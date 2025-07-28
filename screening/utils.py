import PyPDF2
import docx
import re
from typing import Dict, List, Tuple

class ResumeParser:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.content = self._extract_content()
        
    def _extract_content(self) -> str:
        """Extract text content from PDF or DOCX file."""
        if self.file_path.endswith('.pdf'):
            return self._extract_from_pdf()
        elif self.file_path.endswith('.docx'):
            return self._extract_from_docx()
        return ""
    
    def _extract_from_pdf(self) -> str:
        """Extract text from PDF file."""
        with open(self.file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = ""
            for page in reader.pages:
                text += page.extract_text()
        return text
    
    def _extract_from_docx(self) -> str:
        """Extract text from DOCX file."""
        doc = docx.Document(self.file_path)
        return " ".join([paragraph.text for paragraph in doc.paragraphs])

    def extract_skills(self) -> List[str]:
        """Extract skills from resume content."""
        # This is a basic implementation. In a production environment,
        # you might want to use NLP or a more sophisticated approach
        common_skills = [
            'python', 'java', 'javascript', 'html', 'css', 'sql',
            'react', 'angular', 'vue', 'node', 'django', 'flask',
            'aws', 'docker', 'kubernetes', 'git', 'agile', 'scrum'
        ]
        
        found_skills = []
        for skill in common_skills:
            if re.search(r'\b' + skill + r'\b', self.content.lower()):
                found_skills.append(skill)
        return found_skills

    def extract_experience(self) -> int:
        """Extract years of experience from resume content."""
        # Basic implementation - look for patterns like "X years of experience"
        experience_patterns = [
            r'(\d+)\+?\s*years?\s+(?:of\s+)?experience',
            r'experience\s*:\s*(\d+)\+?\s*years?',
            r'worked\s+(?:for\s+)?(\d+)\+?\s*years?'
        ]
        
        years = []
        for pattern in experience_patterns:
            matches = re.finditer(pattern, self.content.lower())
            for match in matches:
                try:
                    years.append(int(match.group(1)))
                except (IndexError, ValueError):
                    continue
        
        return max(years) if years else 0

class ResumeScorer:
    def __init__(self, resume_content: str, job_description: Dict):
        self.resume_content = resume_content.lower()
        self.job_description = job_description
        
    def calculate_scores(self) -> Tuple[float, float, float]:
        """Calculate skills match score, experience match score, and overall score."""
        skills_score = self._calculate_skills_match()
        exp_score = self._calculate_experience_match()
        overall_score = (skills_score * 0.7) + (exp_score * 0.3)
        
        return skills_score, exp_score, overall_score
    
    def _calculate_skills_match(self) -> float:
        """Calculate the skills match score."""
        required_skills = [
            skill.strip().lower() 
            for skill in self.job_description['required_skills'].split(',')
        ]
        
        matched_skills = sum(
            1 for skill in required_skills 
            if re.search(r'\b' + re.escape(skill) + r'\b', self.resume_content)
        )
        
        return (matched_skills / len(required_skills)) * 100 if required_skills else 0
    
    def _calculate_experience_match(self) -> float:
        """Calculate the experience match score."""
        # Extract years of experience from resume
        experience_patterns = [
            r'(\d+)\+?\s*years?\s+(?:of\s+)?experience',
            r'experience\s*:\s*(\d+)\+?\s*years?',
            r'worked\s+(?:for\s+)?(\d+)\+?\s*years?'
        ]
        
        years = []
        for pattern in experience_patterns:
            matches = re.finditer(pattern, self.resume_content)
            for match in matches:
                try:
                    years.append(int(match.group(1)))
                except (IndexError, ValueError):
                    continue
                    
        candidate_experience = max(years) if years else 0
        required_experience = self.job_description['minimum_experience']
        
        if candidate_experience >= required_experience:
            return 100.0
        else:
            return (candidate_experience / required_experience) * 100 if required_experience > 0 else 0
