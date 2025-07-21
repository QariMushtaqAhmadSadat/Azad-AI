import requests
import base64

API_KEY = "18a26c97378a2d48ef4235aa80b88803e1b937ccef5503640f7da1a63b595709"

headers = {
    "x-apikey": API_KEY
}

def check_url_reputation(url):
    try:
        url_id = base64.urlsafe_b64encode(url.encode()).decode().strip("=")
        api_url = f"https://www.virustotal.com/api/v3/urls/{url_id}"
        response = requests.get(api_url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            stats = data.get("data", {}).get("attributes", {}).get("last_analysis_stats", {})
            return f"VirusTotal URL scan results: {stats}"
        else:
            return f"Error: {response.status_code} - {response.text}"
    except Exception as e:
        return f"Exception occurred: {str(e)}"
