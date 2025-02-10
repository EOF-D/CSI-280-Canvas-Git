CANVAS_API_URL = 'https://<canvas>/api/v1'
ACCESS_TOKEN = 'Bearer <your_access_token>'
COURSE_ID = '<course_id>'
FILE_PATH = 'path/to/your/file.txt'
FILE_NAME = 'file.txt'
CONTENT_TYPE = 'text/plain'  # Adjust based on your file type
PARENT_FOLDER_PATH = 'your/folder/path'

# Step 1: Notify Canvas about the file upload
headers = {
    'Authorization': ACCESS_TOKEN
}

data = {
    'name': FILE_NAME,
    'size': str(os.path.getsize(FILE_PATH)),
    'content_type': CONTENT_TYPE,
    'parent_folder_path': PARENT_FOLDER_PATH
}

response = requests.post(
    f'{CANVAS_API_URL}/courses/{COURSE_ID}/files',
    headers=headers,
    data=data
)

if response.status_code != 200:
    raise Exception(f"Failed to initiate file upload: {response.text}")

upload_info = response.json()
upload_url = upload_info['upload_url']
upload_params = upload_info['upload_params']

# Step 2: Upload the file data
files = {
    'file': open(FILE_PATH, 'rb')
}

upload_response = requests.post(
    upload_url,
    files=files,
    data=upload_params
)

if upload_response.status_code not in [201, 301, 302]:
    raise Exception(f"Failed to upload file data: {upload_response.text}")

# Step 3: Confirm the upload's success
if upload_response.status_code in [301, 302]:
    confirmation_url = upload_response.headers['Location']
    confirm_response = requests.post(
        confirmation_url,
        headers=headers
    )
    if confirm_response.status_code != 200:
        raise Exception(f"Failed to confirm upload: {confirm_response.text}")
    print("File uploaded and confirmed successfully!")
else:
    print("File uploaded successfully!")
