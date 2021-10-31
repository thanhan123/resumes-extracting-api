import spacy
import os
import re
import pandas as pd
import pdfminer
import pdf2txt

def convert_pdf(f):
    output_filename = os.path.basename(os.path.splitext(f)[0]) + ".txt"
    output_filepath = os.path.join("output/txt/", output_filename)
    pdf2txt.main(args=[f, "--outfile", output_filepath])
    print(output_filepath + " saved successfully!")
    return open(output_filepath).read()

nlp = spacy.load('en_core_web_sm')

required_skillset = {"ios", "swift", "xcode", "objective c", "realm", "fastlane", "android"}
result_dict = {'name': [], 'phone': [], 'email': [], 'skills': []} 
names = []
phones = []
emails = []
skills = []

def parse_content(text):
    skillset = re.compile("|".join(required_skillset))
    phone_num = re.compile(
        "(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})"
    )
    doc = nlp(text)
    name_array = [entity.text for entity in doc.ents if entity.label_ == "PERSON"]
    print(name_array)
    email = [word for word in doc if word.like_email == True][0]
    print(email)
    phone = str(re.findall(phone_num, text.lower()))
    skills_list = re.findall(skillset, text.lower())
    unique_skills_list = str(set(skills_list))
    names.append(name_array[0])
    emails.append(email)
    phones.append(phone)
    skills.append(unique_skills_list)
    print("Extraction completed successfully!!!")
    
for file in os.listdir('resumes/'):
    if file.endswith('.pdf'):
        print('Reading.....' + file)
        txt = convert_pdf(os.path.join('resumes/',file))
        parse_content(txt)
        
result_dict['name'] = names
result_dict['phone'] = phones
result_dict['email'] = emails
result_dict['skills'] = skills
result_df = pd.DataFrame(result_dict)
result_df.to_csv('output/csv/parsed_resumes.csv')