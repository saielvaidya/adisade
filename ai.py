from openai import OpenAI
from dotenv import load_dotenv
from analysis import build_financial_profile

load_dotenv(override=True)

client = OpenAI()


def generate_recommendations(financial_profile):

    response = client.responses.create(
        model="gpt-4.1-mini",

        instructions="""
        You are Adisade, a concise recurring-expense analysis assistant.

        Analyze the user's recurring expenses and identify realistic
        opportunities to reduce unnecessary spending.

        Rules:
        - Keep the entire response short.
        - Maximum 3 recommendations.
        - Each recommendation should be 1-2 sentences.
        - Focus on optional or flexible recurring expenses.
        - Do not recommend reducing essential expenses just because they are large.
        - Do not invent information.
        - Mention potential monthly or yearly savings only when reasonably
          supported by the provided data.
        - Be practical and specific.

        Use this structure:

        Quick Analysis:
        One short sentence about the spending pattern.

        Recommendations:
        1. ...
        2. ...
        3. ...
        """,

        input=f"""
        Financial profile:

        {financial_profile}
        """,

        max_output_tokens=250
    )

    return response.output_text