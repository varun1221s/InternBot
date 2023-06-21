import time
import requests
import pandas as pd
import os

def get_question_and_accepted_answer(question_id, accepted_answer_id):
    question_url = f"https://api.stackexchange.com/2.3/questions/{question_id}?site=stackoverflow&filter=withbody"
    answer_url = f"https://api.stackexchange.com/2.3/answers/{accepted_answer_id}?site=stackoverflow&filter=withbody"

    question_response = requests.get(question_url).json()
    answer_response = requests.get(answer_url).json()

    question = question_response["items"][0]
    answer = answer_response["items"][0]

    return {
        "question_id": question_id,
        "question_title": question["title"],
        "question_body": question["body"],
        "answer_body": answer["body"],
        "tags": ";".join(question["tags"])
    }


# Load existing data from CSV file
existing_data = pd.read_csv("stackoverflow_data.csv") if os.path.isfile("stackoverflow_data.csv") else pd.DataFrame()

# Check if 'question_id' column exists in the DataFrame
if 'question_id' not in existing_data.columns:
    existing_data['question_id'] = None

# Track question IDs already present in the CSV file
existing_question_ids = set(existing_data["question_id"]) if not existing_data.empty else set()


# Infinite loop to continuously scrape data
while True:
    # Get recent questions
    url = "https://api.stackexchange.com/2.3/questions?order=desc&sort=activity&site=stackoverflow"
    response = requests.get(url)
    
    print(f"Response status code: {response.status_code}")
    print(f"Response JSON: {response.json()}")

    try:
        questions = response.json()["items"]
    except KeyError:
        print("Error: 'items' key not found in the response JSON.")
        continue

    data = []
    for question in questions:
        # Check if the question has an accepted answer and if it's not already in the CSV
        if "accepted_answer_id" in question and question["question_id"] not in existing_question_ids:
            try:
                result = get_question_and_accepted_answer(question["question_id"], question["accepted_answer_id"])
                data.append(result)
            except Exception as e:
                print(f"Exception occurred: {e}")

    print(f"Data collected: {data}")

    # Merge new data with existing data
    if data:
        new_data = pd.DataFrame(data)
        merged_data = pd.concat([existing_data, new_data], ignore_index=True)

        # Save merged data to CSV
        merged_data.to_csv("stackoverflow_data.csv", index=False)
    else:
        merged_data = existing_data

    # Delay for 10 minutes before the next iteration
    time.sleep(600)  # 600 seconds = 10 minutes
