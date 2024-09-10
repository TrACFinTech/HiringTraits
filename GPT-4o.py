import openai
import os
import json
import time


openai.api_key = ''

def read_full_content(file_path):
    """Read the content of a file and handle errors if they occur."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        return ""

def analyze_full_transcript(transcript):
    """Analyze the transcript and evaluate personality traits using the GPT-4 chat model."""
    messages = [
        {
            "role": "system",
            "content": "You are a helpful assistant analyzing personality traits based on provided transcripts."
        },
        {
            "role": "user",
            "content": f"""
The following transcript is a conversation between an ‘interviewer’ and ‘interviewee’:
{transcript}

Your task is to analyze the transcript and rate the personality traits of the ‘interviewee’ for the following five personality trait categories:

1. Openness to Experience
2. Conscientiousness
3. Extraversion
4. Agreeableness
5. Neuroticism

Assign a score between 1 and 5 for each of these five categories, with 1 being the lowest and 5 being the highest. Ensure each score is distinct, reflective of the relative prominence of the traits based on the ‘interviewee’s’ responses, tone, and behavior during the conversation given in the transcript. Follow the evaluation criteria given below while assigning scores to each of the five personality trait categories.

Evaluation Criteria:

1. Openness to Experience:
   - High Score: Traits like scientific and artistic creativity, divergent thinking, political liberalism, imaginative, cultured, curious, original, and broad-mindedness.
   - Low Score: Traits like close-mindedness and conservatism.

2. Conscientiousness:
   - High Score: Traits such as being hardworking, achievement-oriented, persevering, careful, and responsible.
   - Low Score: Traits like unreliability, carelessness, lack of self-discipline, low need for achievement, disorganized.

3. Extraversion:
   - High Score: Traits such as sociable, gregarious, assertive, talkative, active, high level of energy, excited, expressing feelings of happiness and joy, enjoys large noisy crowds and parties.
   - Low Score: Traits like introspective, quiet, unsociable, and lacking in assertiveness.

4. Agreeableness:
   - High Score: Traits such as altruism, nurturance, caring, emotional support, courteous, flexible, trusting, good-natured, cooperative, forgiving, soft-hearted, and tolerant.
   - Low Score: Traits like hostility, indifference to others, self-centeredness, spitefulness, jealousy, relatively stubborn, critical, manipulative.

5. Neuroticism:
   - High Score: Traits such as anxious, depressed, angry, embarrassed, emotional, worried, insecure, unable to handle stress.
   - Low Score: Traits like high emotional stability, impulse control, staying calm in high-stress situations.
    
Output Format:

The output should be in the following format just give me the score:

{{
   {{
    "Openness to Experience": X1, 
    "Conscientiousness": X2, 
    "Extraversion": X3, 
    "Agreeableness": X4, 
    "Neuroticism": X5 
  }}
}}

Here ‘X1’ denotes the score assigned for Openness to Experience, ‘X2’ denotes the score assigned for Conscientiousness, ‘X3’ denotes the score assigned for Extraversion, ‘X4’ denotes the score assigned for Agreeableness, and ‘X5’ denotes the score for Neuroticism.
"""
        }
    ]

    max_retries = 3
    for attempt in range(max_retries):
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4o",  
                messages=messages,
                max_tokens=300,
                temperature=0.9,
            )

            result_text = response.choices[0].message['content'].strip()

            # Attempt to parse the response as JSON
            try:
                result_json = json.loads(result_text)
                return result_json
            except json.JSONDecodeError:
                print(f"Failed to parse JSON: {result_text}")
                return {"Openness to Experience": 0, "Conscientiousness": 0, "Extraversion": 0, "Agreeableness": 0, "Neuroticism": 0}

        except openai.OpenAIError as e:
            print(f"Error during API call: {e}")
            if attempt < max_retries - 1:
                time.sleep(5)  # Wait before retrying
            else:
                return {"Openness to Experience": 0, "Conscientiousness": 0, "Extraversion": 0, "Agreeableness": 0, "Neuroticism": 0}

def process_transcripts(directory):
    """Process all VTT files in the given directory and analyze them."""
    files = [filename for filename in os.listdir(directory) if filename.endswith(".vtt")]

    if not files:
        print("No VTT files found in the directory.")
        return

    for file in files:
        file_path = os.path.join(directory, file)
        
        transcript = read_full_content(file_path)
        if transcript:
            result = analyze_full_transcript(transcript)
            print(f"{file}: {result}")
        else:
            print(f"Failed to read content from {file}")

if __name__ == "__main__":
    # Directory containing the VTT files
    directory = ""

    # Run the main function
    process_transcripts(directory)
