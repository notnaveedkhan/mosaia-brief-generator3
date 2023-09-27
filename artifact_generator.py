import requests
import json
import openai

def read_artifact_mapping(file_path):
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
            print(f"Debug: Loaded data is {type(data)}")
            return data
    except Exception as e:
        print(f"An error occurred: {e}")
      
def generate_artifacts_list(sow_points, artifact_mapping):
    custom_artifacts_list = []
    if not isinstance(artifact_mapping, dict):  # Add this line to validate the type
        print("Error: artifact_mapping should be a dictionary.")
        return custom_artifacts_list

    for work_area in sow_points:
        print(f"Checking work_area: {work_area}")
        for key in artifact_mapping.keys():  # This line assumes artifact_mapping is a dictionary
            if key.lower() in work_area.lower():
                custom_artifacts_list.extend(artifact_mapping[key])
    return custom_artifacts_list

def main():
    artifact_mapping = read_artifact_mapping("artifact_map.json")

    sow_points = ['Understand the problem: need more leads', 'Develop a solution: hiring an agency to build a go to market plan that we can execute on']

    custom_artifacts_list = generate_artifacts_list(sow_points, artifact_mapping)

    if custom_artifacts_list:
        # Send the list to OpenAI API
        payload = {
            "model": "gpt-3.5-turbo",
            "messages": [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Help me find relevant artifacts for my project."},
                {"role": "assistant", "content": f"{custom_artifacts_list}"}
            ]
        }
        headers = {"Authorization": f"Bearer {OPENAI_API_KEY}"}
        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
        chat_response = json.loads(response.text)

        print(chat_response['choices'][0]['message']['content'])

if __name__ == "__main__":
    main()
