import spacy
import os
import re
import pdftotext

class CVParsing:
    def __init__(self):
        self.nlp = spacy.load('en_core_web_sm')

    def convert_pdf(self, f):
        pdf = pdftotext.PDF(f)
        return ''.join(pdf)

    def parse_content(self, text, required_skillset):
        skillset = re.compile("|".join(required_skillset))
        phone_num = re.compile(
            "(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})"
        )
        doc = self.nlp(text)
        name = [entity.text for entity in doc.ents if entity.label_ == "PERSON"][0]
        email = [str(word) for word in doc if word.like_email == True][0]
        phone = str(re.findall(phone_num, text.lower()))
        skills_list = re.findall(skillset, text.lower())
        unique_skills_list = str(set(skills_list))
        return (name, email, phone, unique_skills_list)

    def process_content(self, text):
        # remove "broken" space character
        text = re.sub('\u200b', '', text)
        
        # process for all uppercase name
        uppercase_words_regex = re.compile("[A-Z]+")
        uppercase_words = [w for w in re.findall(uppercase_words_regex, text) if len(w) > 1]
        for i in range(len(uppercase_words)):
            w = uppercase_words[i]
            new_w = w[0]+w[1:].lower()
            text = re.sub(w, new_w, text)
        return text

    def parse_cvs(self, pdf_files, required_skillset):
        result_dict = {'name': [], 'phone': [], 'email': [], 'skills': [], 'resumes': []} 
        names = []
        phones = []
        emails = []
        skills = []
        resumes = []

        for file in pdf_files:
            if file.filename.endswith('.pdf'):
                txt = self.process_content(self.convert_pdf(file.file))
                name, email, phone, skill_set = self.parse_content(txt, required_skillset)
                names.append(name)
                emails.append(email)
                phones.append(phone)
                skills.append(skill_set)
                resumes.append(file.filename)
        
        result_dict['name'] = names
        result_dict['phone'] = phones
        result_dict['email'] = emails
        result_dict['skills'] = skills
        result_dict['resumes'] = resumes

        return result_dict