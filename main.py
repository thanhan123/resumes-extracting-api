from typing import Optional, List
from fastapi import FastAPI, File, UploadFile
from starlette.responses import RedirectResponse
import cv_parsing

app_desc = """<h2>Try this app by uploading resumes with required skill set</h2>
<br>by An Dinh"""

app = FastAPI(title='Resumes extracting information', description=app_desc)

@app.get("/", include_in_schema=False)
def read_root():
    return RedirectResponse(url="/docs")

@app.post("/parsecvs/")
async def create_upload_files(skill_set: List[str], files: List[UploadFile] = File(...)):
    if len(skill_set) == 1:
        skill_set = skill_set[0].split(",")
    cvparsing = cv_parsing.CVParsing()
    return cvparsing.parse_cvs(files, skill_set)