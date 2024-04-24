import dotenv
import os
import requests
import base64
from pyperclip import copy

dotenv.load_dotenv()

key = os.getenv("OPENAI_API_KEY")

# Function to encode the image
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

# Path to your image
prefix = r"E:\Toppity2\maxwe\Pictures\Ebay Pictures\Round 2\\"
postfix = ".JPG"
image_path = prefix + input("Enter the file name: ") + postfix
image_path2 = prefix + input("Enter the file name: ") + postfix

conditions = ["New", "Used", "For parts or not working", "Open box"]
conditions = [f"{i} - {conditions[i]}" for i in range(len(conditions))]
print("\n".join(conditions))
condition = conditions[int(input("Enter the condition: "))]

otherNotes = input("Enter any other notes: ")


# Getting the base64 string
base64_image1 = encode_image(image_path)
base64_image2 = encode_image(image_path2)

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {key}"
}

payload = {
    "model": "gpt-4-turbo",
    "messages": [
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "Short (like 100 word), un-salesy, although still informative ebay description for this item. Use pure ascii formatting, no html or markdown."
                },
                {
                    "type": "text",
                    "text": "Here's an example: EK AIO Elite 360 D-RGB All-in-One Liquid Cooling System. Previously used, fully functional. Features a 360mm radiator with 6 D-RGB lighting for vibrant aesthetics. Includes PWM controls for silent operation, efficient cooling for your high-end CPU, and universal mounting mechanism. Original packaging included."
                },
                {
                    "type": "text",
                    "text": f"Here's some other notes: condition: {condition}. Other notes: {otherNotes}"
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{base64_image1}"
                    }
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{base64_image2}"
                    }
                }
            ]
        }
    ],
}

response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

print(response.json())

print(response.json()['choices'][0]['message']['content'])
copy(response.json()['choices'][0]['message']['content'])
