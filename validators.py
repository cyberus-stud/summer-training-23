# Set allowed file extensions and maximum file size in bytes
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
MAX_FILE_SIZE_BYTES = 10 * 1024 * 1024  # 10MB

# Function to check if the file extension is allowed
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Function to check if the file size is within the limit
def allowed_file_size(file):
    return len(file.read()) <= MAX_FILE_SIZE_BYTES
