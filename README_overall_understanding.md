#  Adobe India Hackathon – PDF Outline & Persona-Based Intelligence

This repository contains the solution for **Round 1A** and **Round 1B** of the **Adobe India Hackathon - "Connecting the Dots" Challenge**.  
The goal is to build a Dockerized system that:

-  **Round 1A**: Extracts structured outlines from PDFs (Title, H1, H2, H3).
-  **Round 1B**: Acts as a persona-based intelligent reader that extracts and ranks relevant content based on a persona's job-to-be-done.

---

## 📁 Folder Structure

```bash
pdf_outline_project/
├── Dockerfile
├── extract_outline.py               # Round 1A extractor
├── requirements.txt
├── run_extractor.ps1               # PowerShell runner for Round 1A                # PowerShell runner for Round 1B
├── input/
│   ├── your_pdf_file.pdf
│── persona.json
├── output/
│   ├── your_pdf_file.json
│   


 Technologies Used
 Python 3.12

 PyPDF2

 scikit-learn

 Docker

 PowerShell for easy execution

 How to Run (Step-by-Step)
1.  Build the Docker Image (Run once)
powershell
Copy
Edit
docker build --platform=linux/amd64 -t pdf-outline-extractor .
2.  Round 1A: Structure Extractor
Put your PDFs inside the input/ folder.

powershell
Copy
Edit
.\run_extractor.ps1
This generates <filename>.json in the output/ folder containing the title and heading hierarchy.

3.  Round 1B: Persona-Based Relevance Extractor
Create a persona.json file in input/:

json
Copy
Edit
{
  "persona": "Hackathon Organizer",
  "job_to_be_done": "Extract and rank the instructions about Round 1A and Round 1B from the document"
}
Then run:

powershell
Copy
Edit
.\run_analyst.ps1
This will generate persona_output.json inside the output/ folder.

 Expected Output Format
-> For Round 1A:
json
Copy
Edit
{
  "title": "Document Title",
  "outline": [
    { "level": "H1", "text": "Heading", "page": 1 },
    { "level": "H2", "text": "Subheading", "page": 2 }
  ]
}
-> For Round 1B:
json
Copy
Edit
{
  "metadata": {
    "persona": "Hackathon Organizer",
    "job_to_be_done": "...",
    ...
  },
  "extracted_sections": [
    {
      "page": 3,
      "section_title": "Round 1A: Understand Your Document",
      "importance_rank": 1
    }
  ],
  "sub_section_analysis": [
    {
      "page": 3,
      "refined_text": "..."
    }
  ]
}
 Requirements Met
 Under 10s runtime for 50-page PDFs

 No network/internet usage

 Model size (if used) ≤ 200MB

 Docker image supports linux/amd64

 Handles multiple PDFs in batch

