from pyngrok import ngrok
import subprocess
import time
import os

ngrok.set_auth_token("2yM0gkgPF9xlL8w8UXYeEYaW9LD_2jVFzjYtwZtbr6VZXkCia")

def start_server():
    # Start Django server
    server = subprocess.Popen(
        ['python', 'manage.py', 'runserver', '0.0.0.0:8000'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        cwd=os.getcwd()
    )

    # Wait for server to start
    print("Starting Django server...")
    time.sleep(5)

    # Create ngrok tunnel
    print("Creating ngrok tunnel...")
    tunnel = ngrok.connect(8000, proto="http")
    public_url = tunnel.public_url

    print(f"Server running locally at http://127.0.0.1:8000")
    print(f"Public URL: {public_url}")
    print(f"API available at: {public_url}/api/")

    try:
        print("Press Ctrl+C to stop...")
        server.wait()
    except KeyboardInterrupt:
        print("Stopping server...")
        # Terminate server
        server.terminate()
        server.wait()
        # Kill ngrok
        ngrok.kill()
        print("Server stopped.")

if __name__ == "__main__":
    start_server()
