from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

BASE_URL = "https://marketplace.atlassian.com/"
BASE_URL_SLICE= BASE_URL.rstrip('/')
APPS_ENDPOINT = "addons"

#get all applications
@app.route('/applications', methods=['GET'])
def get_applications():
    try:
        # Build the URL for the Atlassian Marketplace API
        url = f"{BASE_URL}rest/2/applications"
        response = requests.get(url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the JSON response
            data = response.json()

            # Check if the response is empty or missing the expected structure
            if not data or "_embedded" not in data or "applications" not in data["_embedded"]:
                return jsonify({'error': 'Invalid response structure from Atlassian Marketplace'}), 500
            
            result = []
            for app in data["_embedded"]["applications"]:
                result.append(app["name"])
        return jsonify({"applications" : result})

    except Exception as e:
        # Handle exceptions
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500


#get the required apps by filtering and passing parameters
@app.route('/get-apps', methods=['GET'])
def get_apps():
    try:
        # Get parameters from the request
        application = request.args.get('application')
        hosting_type = request.args.get('hosting_type')
        app_filter = request.args.get('filter')
        search_text = request.args.get('search_text')

        # Check for required parameters
        if not application:
            return jsonify({'error': 'Parameter "application" is required.'}), 400

        # Build the URL for the Atlassian Marketplace API
        url = f"{BASE_URL}rest/2/{APPS_ENDPOINT}?application={application}"
        if hosting_type:
            url += f"&hosting={hosting_type}"
        if app_filter:
            url += f"&filter={app_filter}"
        if search_text:
            url += f"&q={search_text}"

        # Make a request to the Atlassian Marketplace API
        response = requests.get(url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the JSON response
            data = response.json()

            # Check if the response is empty or missing the expected structure
            if not data or "_embedded" not in data or "addons" not in data["_embedded"]:
                return jsonify({'error': 'Invalid response structure from Atlassian Marketplace'}), 500

            # Extract relevant information from the response
            result = []
            for app in data["_embedded"]["addons"]:
                app_info = {
                    'app name': app.get('name', ''),
                    'description': app.get('summary', ''),
                    'link': BASE_URL_SLICE + app['_links']['alternate'].get('href', ''),
                    'total users': app['_embedded']['distribution'].get('totalUsers', ''),
                    'total installs': app['_embedded']['distribution'].get('totalInstalls', ''),
                    'categories': [category.get("name", '') for category in app["_embedded"]["categories"]],
                    'downloads': app['_embedded']['distribution'].get('downloads', ''),
                    'average stars': app['_embedded']['reviews'].get('averageStars', ''),
                    'review count': app['_embedded']['reviews'].get('count', ''),
                    'vendor': app['_embedded']['vendor'].get('name', '')
                }

                result.append(app_info)
            # Return the result as JSON
            return jsonify(result)

        else:
            # Return an error message if the request was not successful
            return jsonify({'error': f'Failed to fetch data from Atlassian Marketplace. Status code: {response.status_code}'}), response.status_code

    except Exception as e:
        # Handle other exceptions
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True)
