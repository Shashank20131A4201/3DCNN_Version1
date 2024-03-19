import uvicorn
from fastapi import FastAPI, UploadFile, File, Request,Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, RedirectResponse
import io
from PIL import Image
import os
import shutil
import psycopg2
from fastapi.responses import RedirectResponse
from dotenv import load_dotenv
from model import test_pnemonia

load_dotenv('.env')

conn = psycopg2.connect(
    dbname=os.getenv("POSTGRES_DB"),
    user=os.getenv("POSTGRES_USER"),
    password=os.getenv("POSTGRES_PASSWORD"),
    host="postgres",
    port=os.getenv("DATABASE_PORT")
)

app = FastAPI()
app.mount("/static", StaticFiles(directory = "static"), name = "static")

UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

templates = Jinja2Templates(directory="templates")

@app.get("/")
def read_root(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

@app.get("/sign")
def signup(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})

@app.post("/sign")
async def signup(
    request: Request, username: str = Form(...), email: str = Form(...),password1: str = Form(...),password2:str = Form(...) 
):
   
    cur = conn.cursor()
    cur.execute("INSERT INTO users(Username,Email,Password_) VALUES (%s, %s,%s)", (username,email,password1))
    conn.commit()
    cur.close() 
 
    return RedirectResponse("/login", status_code=303)

@app.get("/login")
def login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login")
async def do_login(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
):
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE Username=%s and Password_=%s", (username,password))
    existing_user = cur.fetchone()
    cur.close()
    
    if existing_user:
        print(existing_user)
        return RedirectResponse("/upload", status_code=303)
    
    else:
        return JSONResponse(status_code=401, content={"message": "Wrong credentials"})

   

@app.get("/upload")
def index_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/upload")
async def upload_nib_scan(request: Request, scan: UploadFile):
    if scan.filename != '':
        # Check if the file extension is appropriate for NiB scans (e.g., .nii)
        # allowed_extensions = {'.nii', '.nii.gz', '.hdr', '.img'}
        # file_ext = os.path.splitext(scan.filename)[-1].lower()

        # if file_ext not in allowed_extensions:
        #     return JSONResponse(content={"error": "Invalid file format. Only NIfTI or Analyze files are allowed."}, status_code=400)

        # scan_path = os.path.join(UPLOAD_FOLDER, scan.filename)
        # with open(scan_path, "wb") as f:
        #     shutil.copyfileobj(scan.file, f)

        # Process the uploaded NiB scan
        # try:
        #     nib_scan = nib.load(scan_path)
        #     # Perform additional processing on the NiB scan if needed
        #     # For example: processed_data = process_nib_scan(nib_scan)
        #     # ...
        #     # return {"message": "NiB scan uploaded and processed successfully."}
        #     print("NiB scan uploaded and processed successfully")
        # except Exception as e:
        #     # return JSONResponse(content={"error": f"Error processing NiB scan: {str(e)}"}, status_code=500)
        #     print("Error processing NiB scan")


        scan_path = os.path.join(UPLOAD_FOLDER, scan.filename)
        with open(scan_path, "wb") as f:
            shutil.copyfileobj(scan.file, f)

        prediction = test_pnemonia(scan_path)
        prediction=round(prediction*100, 2)
        return templates.TemplateResponse("index.html", {"request": request, "message": "CT Scan uploaded and processed successfully.", "Pred": prediction})
       
    return templates.TemplateResponse("index.html", {"request": request, "error": "No file uploaded."})

    


if __name__ == '__main__':
   uvicorn.run(app, host='0.0.0.0', port=8000)

