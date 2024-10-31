import pandas as pd
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os



# Load environment variables
load_dotenv()

# Get the API key from environment variables
key = os.getenv("GOOGLE_API_KEY")

# Initialize the Gemini Pro model
model = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=key)


# Function to evaluate decision rationale and assign grade points
def evaluate_decision_rationale(messages,batch_response_count):


    prompt_template = f"""
    Your task: Evaluate the decision rationales (Messages) provided below according to the criteria specified. Each rationale should be assessed individually and assigned either Pass, Low Pass, or Fail. Do not deviate from the provided instructions. 

    **Important Instructions:**
    - Each message must have a name and a message.
    - This batch should contain exactly {batch_response_count} student messages.
    - Ensure that you correctly identify and evaluate this many student messages.

    **Input format:** 
    Each message is structured as follows: 
    `name1: message ****************************************** name2: message ****************************************** name3: message ......`

    **Output format:** 
    `name1: Pass/Low Pass/Fail && <your reasoning> | name2: Pass/Low Pass/Fail && <your reasoning> |`

    **Grading criteria:**

    - **Grading Scale**:
    - If the decision rationale explains the reasoning behind decisions with references to specific data from the coffee shop's performance, then give **10 points** (Pass).
    - If the decision rationale lacks sufficient depth, mentioning some data but failing to adequately explain the reasoning or connect with past performance data, give **6 points** (Low Pass).
    - If the rationale is missing, empty, or does not meet the minimum requirements, assign **0 points** (Fail).

    **Important Note:** 
    - Double-check that your output matches the required format exactly. 

    Here are the decision rationales:
    {messages}
    """


    # Invoke the model with the prompt
    response = model.invoke(prompt_template)

    # Assuming the response contains the grade points and rationale 
    return extract_grading_info(response.content)


# Function to extract grading info from the response
def extract_grading_info(response):
    # Split the response by pipe to get each student's rationale
    student_rationales = response.split("|")
    
    points_list = []
    
    rationale_list = []
    
    
    # Process each student's response
    for rationale in student_rationales:
        points = 0
        reasoning = "No specific rationale provided."
        

        if 'Fail' in rationale:
            points = 0
            reasoning = "Reasoning not provided."
        
        
        elif 'low pass' == rationale.split('&&')[0].split(":")[1].strip().lower():
            points = 6
            reasoning = rationale.split("&&")[1].strip(" ")
            
            
        elif 'pass' == rationale.split('&&')[0].split(":")[1].strip().lower():
            points = 10
            reasoning = rationale.split("&&")[1].strip(" ")
            

        # Append the points and reasoning to their respective lists
        points_list.append(points)
        rationale_list.append(reasoning)
    
    return points_list, rationale_list


def grade_messages():



    # Load the Excel file
    file_path = 'data.xlsx'  # Update this with your actual file path

    df = pd.read_excel(file_path)
    

# Process records in batches of 15
    batch_size = 15
    grades = []
    rationales = []


    for start in range(0, len(df), batch_size):
        end = min(start + batch_size, len(df))
        
        batch_response_count=end-start
        
        # Get the names and messages, handling NaN values
        batch_data = df[['Name', 'Message']].iloc[start:end].fillna('No Messages Submitted').astype(str)

        # Convert to a list of dictionaries
        batch_messages = batch_data.to_dict(orient='records')

        # Combine messages and rationales
        combined_messages = " ****************************************** ".join(
            f"{entry['Name']}: {entry['Message']}" for entry in batch_messages)


        # Evaluate the batch using combined messages
        points_list, rationale_list = evaluate_decision_rationale(combined_messages,batch_response_count)
        

        # Extend lists
        grades.extend(points_list)
        rationales.extend(rationale_list)


    # Assign the results to the DataFrame
    df['points'] = grades
    df['grading rationale'] = rationales

    # Save the updated DataFrame to a new Excel file
    output_file_path = 'updated_grades_with_rationale.xlsx'  # Update this with your desired output file name
    df.to_excel(output_file_path, index=False)

    # Print confirmation
    print(f'Grading completed. Results saved to {output_file_path}.')
    
    return df



