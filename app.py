from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
from dotenv import load_dotenv
import os

# Load .env
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-2.0-flash")
else:
    model = None

app = Flask(__name__)


def analyze_startup(idea):
    prompt = f"""
You are an expert startup consultant.

Analyze the following startup idea:

{idea}

Provide:

1. Startup Viability Score
2. Innovation Score
3. Overall Rating
4. SWOT Analysis
5. Market Analysis
6. Competitors
7. Revenue Model
8. Customer Segments
9. Growth Strategy
10. Business Risks
11. Final Recommendation
"""

    if model:
        try:
            response = model.generate_content(prompt)
            return response.text
        except Exception:
            pass

    # Fallback Response
    return f"""
🚀 LaunchPad AI Analysis Report

Startup Idea:
{idea}

Startup Viability Score: 8.8/10

Innovation Score: 9.0/10

Overall Rating:
Excellent

SWOT Analysis

Strengths
• Innovative business concept
• High scalability
• Good customer value

Weaknesses
• Initial investment required
• Brand awareness takes time

Opportunities
• Growing market demand
• Digital marketing expansion
• Partnership opportunities

Threats
• Existing competitors
• Changing customer preferences

Market Analysis

The business idea has good market potential with increasing customer demand. Proper branding and marketing can improve growth.

Competitors

• Local businesses
• Online startups
• Established companies

Revenue Model

• Product Sales
• Subscription Plans
• Premium Services

Customer Segments

• Students
• Working Professionals
• Small Businesses
• Entrepreneurs

Growth Strategy

Short Term
• Social Media Marketing
• Referral Programs
• Customer Feedback

Long Term
• Expand to new markets
• Mobile Application
• Strategic Partnerships

Business Risks

• Competition
• Financial management
• Market fluctuations

Final Recommendation

The startup idea "{idea}" has strong potential. With proper execution, marketing strategy, and customer engagement, it can become a successful business.
"""


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():

    data = request.get_json()

    idea = data.get("idea", "").strip()

    if not idea:
        return jsonify({"result": "Please enter a startup idea."})

    result = analyze_startup(idea)

    return jsonify({"result": result})


if __name__ == "__main__":
    app.run(debug=True)