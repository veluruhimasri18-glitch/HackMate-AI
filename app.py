from flask import Flask, render_template, request
from google import genai
from dotenv import load_dotenv
import os
from flask import make_response
from reportlab.pdfgen import canvas
from io import BytesIO
from flask import send_file

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

app = Flask(__name__)


def generate_ai_response(team_size, skills, theme, duration, experience, goal):

    prompt = f"""
You are HackMate AI, an intelligent hackathon assistant.

Team Size: {team_size}
Skills: {skills}
Hackathon Theme: {theme}
Duration: {duration}
Experience Level: {experience}
Goal: {goal}

IMPORTANT RULES:
- Return ONLY HTML.
- Do NOT use markdown symbols like ##, **, or *.
- Use attractive formatting with headings, spacing, emojis, and cards.
- Each major section should be inside a styled <div>.
- Use <h2> for section titles.
- Use <ol> for project ideas (numbered 1, 2, 3).
- Use <ul> for bullet points.
- Keep output clean and professional.

Generate the following sections:

<h2>🔥 3 Unique AI-Powered Project Ideas</h2>

For EACH project idea include:
1. Project Name
2. Tagline
3. Problem Statement (1-2 lines)
4. Main Features (3 bullet points with emojis)
5. AI Technologies Used
6. Suggested Tech Stack
7. Why it is a strong hackathon idea (3 bullet points)

--------------------------------------------------

<h2>👥 Suggested Team Roles</h2>

Provide roles like:
🧠 AI/ML Engineer
🖥 Backend Developer
🎨 Frontend Developer

Include:
- Responsibilities
- Tools/Tech used

--------------------------------------------------

<h2>⏰ Development Timeline ({duration} hours)</h2>

Make a realistic hour-wise plan based on duration.

--------------------------------------------------

<h2>🎤 Short & Impressive Project Pitch</h2>

5–6 lines startup-style pitch covering:
- Problem
- Solution
- AI innovation
- Impact

--------------------------------------------------

End with:
"🚀 Good luck, HackMates! Build something amazing and impress the judges!"

Return ONLY valid HTML.
"""
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text


@app.route("/", methods=["GET", "POST"])
def home():

    if request.method == "POST":

        team_size = request.form["team_size"]
        skills = request.form["skills"]
        theme = request.form["theme"]
        duration = request.form["duration"]
        experience = request.form["experience"]
        goal = request.form["goal"]

        ai_output = generate_ai_response(
            team_size,
            skills,
            theme,
            duration,
            experience,
            goal
        )

        return render_template(
            "result.html",
            ai_output=ai_output,
            team_size=team_size,
            skills=skills,
            theme=theme,
            duration=duration,
            experience=experience,
            goal=goal
        )

    return render_template("index.html")

@app.route("/download-pdf", methods=["POST"])
def download_pdf():
    html_content = request.form["html_content"]

    buffer = BytesIO()
    pdf = canvas.Canvas(buffer)

    # simple PDF text output
    text_object = pdf.beginText(40, 800)
    for line in html_content.split("<br>"):
        text_object.textLine(line)

    pdf.drawText(text_object)
    pdf.save()

    buffer.seek(0)

    return send_file(
        buffer,
        as_attachment=True,
        download_name="HackMateAI_Plan.pdf",
        mimetype="application/pdf"
    )



if __name__ == "__main__":
    app.run(debug=True)