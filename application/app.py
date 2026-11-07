
from application.groq_client import generate_response
from application.telemetry import initialize_database, log_request


def main():

    initialize_database()

    print("\n===================================")
    print("      ENTERPRISE AI PLATFORM")
    print("===================================")

    prompt = input("\nEnter your question: ")

    print("\nGenerating response...\n")

    result = generate_response(prompt)

    if result["status"] == "success":

        print("AI RESPONSE:")
        print(result["answer"])

    elif result["status"] == "empty":

        print("The model returned an empty response.")
        print("Finish reason:", result["finish_reason"])

    else:

        print("Request failed!")
        print("Error:", result["error"])

    # Save request metrics
    log_request(result)

    print("\n---------- REQUEST METRICS ----------")

    print("Model:", result.get("model"))
    print("Latency:", result["latency"], "seconds")
    print("Prompt tokens:", result.get("prompt_tokens"))
    print("Completion tokens:", result.get("completion_tokens"))
    print("Total tokens:", result.get("total_tokens"))
    print("Finish reason:", result.get("finish_reason"))
    print("Status:", result["status"])

    print("\nRequest saved to telemetry database.")


if __name__ == "__main__":
    main()
