from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
from groq import Groq

# -------------------------------
# Load API Key from .env
load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# -------------------------------
# FastAPI Setup
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------------
# Pydantic Models
class IkigaiRequest(BaseModel):
    love: str
    good_at: str
    paid_for: str
    world_needs: str

class IkigaiResponse(BaseModel):
    success: bool
    summary: str
    role: str

# -------------------------------
# Groq Summarizer Function
def summarize_with_groq(data: IkigaiRequest) -> tuple:
    prompt = f"""
The user is trying to find their ideal AI-aligned career path using the Ikigai method.

Here are their reflections:
- What they love: {data.love}
- What they're good at: {data.good_at}
- What they can be paid for: {data.paid_for}
- What the world needs: {data.world_needs}

Please respond in the following format:
Summary: <short 1–2 line summary of their Ikigai>
Suggested Roles: <suggest 1 or 2 specific AI-related career roles>
"""

    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="llama3-70b-8192",  # Or any other model Groq supports
        )

        output = chat_completion.choices[0].message.content

        # Parse lines
        lines = output.split("\n")
        summary = next((l.replace("Summary:", "").strip() for l in lines if l.startswith("Summary:")), "")
        roles = next((l.replace("Suggested Roles:", "").strip() for l in lines if l.startswith("Suggested Roles:")), "")

        return summary, roles

    except Exception as e:
        print(f"[Groq Error] {e}")
        return "Unable to generate summary at the moment.", "Unavailable"

# -------------------------------
# Endpoint
@app.post("/summarize", response_model=IkigaiResponse)
def summarize_ikigai(data: IkigaiRequest):
    summary, roles = summarize_with_groq(data)

    return IkigaiResponse(
        success=True,
        summary=summary,
        role=roles
    )
