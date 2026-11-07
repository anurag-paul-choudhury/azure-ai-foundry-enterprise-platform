
import time
from groq import Groq
from application.config import GROQ_API_KEY, GROQ_MODEL

client = Groq(api_key=GROQ_API_KEY)


def generate_response(prompt):

    start_time = time.time()

    try:
        response = client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_completion_tokens=1000
        )

        latency = round(time.time() - start_time, 2)

        choice = response.choices[0]
        answer = choice.message.content or ""

        return {
            "answer": answer,
            "latency": latency,
            "prompt_tokens": response.usage.prompt_tokens,
            "completion_tokens": response.usage.completion_tokens,
            "total_tokens": response.usage.total_tokens,
            "model": response.model,
            "finish_reason": choice.finish_reason,
            "status": "success" if answer.strip() else "empty"
        }

    except Exception as error:
        return {
            "answer": None,
            "latency": round(time.time() - start_time, 2),
            "error": str(error),
            "status": "failed"
        }
