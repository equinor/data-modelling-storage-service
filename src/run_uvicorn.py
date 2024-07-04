import uvicorn
from app import create_app, init_application, reset_app, create_key
import os
import subprocess
import tempfile

# Setting environment variables
os.environ["SECRET_KEY"] = "sg9aeUM5i1JO4gNN8fQadokJa3_gXQMLBjSGGYcfscs="
os.environ["ENVIRONMENT"] = "local"
os.environ["LOGGING_LEVEL"] = "debug"
os.environ["MONGO_PASSWORD"] = "maf"
os.environ["AUTH_ENABLED"] = "False"
os.environ["OAUTH_TOKEN_ENDPOINT"] = "https://login.microsoftonline.com/3aa4a235-b6e2-48d5-9195-7fcf05b459b0/oauth2/v2.0/token"
os.environ["OAUTH_AUTH_ENDPOINT"] = "https://login.microsoftonline.com/3aa4a235-b6e2-48d5-9195-7fcf05b459b0/oauth2/v2.0/authorize"
os.environ["OAUTH_WELL_KNOWN"] = "https://login.microsoftonline.com/3aa4a235-b6e2-48d5-9195-7fcf05b459b0/v2.0/.well-known/openid-configuration"
os.environ["AUTH_AUDIENCE"] = "97a6b5bd-63fb-42c6-bb75-7e5de2394ba0"
os.environ["OAUTH_CLIENT_ID"] = "97a6b5bd-63fb-42c6-bb75-7e5de2394ba0"
os.environ["OAUTH_CLIENT_SECRET"] = "your_oauth_client_secret"
os.environ["OAUTH_AUTH_SCOPE"] = "api://97a6b5bd-63fb-42c6-bb75-7e5de2394ba0/dmss"
os.environ["AAD_ENTERPRISE_APP_OID"] = "b9041025-05f0-44d4-89a7-3b5f955c0de5"
os.environ["OTEL_SERVICE_NAME"] = "DMSS - local"
os.environ["REDIS_PASSWORD"] = "maf"

if __name__ == "__main__":
    base_dir = r"C:\Users\jta\OneDrive - SevanSSP AS\Desktop\equinor_fork\data-modelling-storage-service\src"
    script_path = os.path.join(base_dir, 'init_dev.sh')
    bash_path = r"C:\Program Files\Git\bin\bash.exe"  # Adjust this path to your bash installation
    env = os.environ.copy()

    env['BASE_DIR'] = base_dir.replace('\\', '/')  # Convert to Unix-style path


    with tempfile.TemporaryDirectory() as tmp_dir:
        print(f"Temporary directory created at {tmp_dir}")
        tmp_dir_unix = tmp_dir.replace('\\', '/')
        print(f"Unix-style temporary directory path: {tmp_dir_unix}")
        result = subprocess.run([bash_path, script_path, tmp_dir_unix, 'api'],
                                capture_output=True, text=True, cwd=base_dir, env=env)

        if result.returncode != 0:
            print("An error occurred:", result.stderr)
        else:
            print("Script ran successfully:", result.stdout)

        json_file_path = os.path.join(tmp_dir, 'DMSS_systemDS.json')
        if os.path.exists(json_file_path) and os.access(json_file_path, os.R_OK):
            print(f"JSON file {json_file_path} exists and is readable.")
        else:
            print(f"JSON file {json_file_path} does not exist or is not readable.")

    # Try to read the JSON file
        reset_app()
        #create_key()

        #init_application()
        uvicorn.run("app:create_app", host="0.0.0.0", port=5000, log_level="debug", reload=True)
