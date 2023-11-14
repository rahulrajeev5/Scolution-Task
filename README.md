# Atlassian Marketplace API Integration using Flask

## Overview

This Flask application provides endpoints to interact with the Atlassian Marketplace API. It allows you to fetch a list of applications and retrieve information about specific apps based on various parameters.

## Installation

1. **Clone the repository:**

    ```bash
    https://github.com/rahulrajeev5/Scolution-Task.git
    cd Atlassian Marketplace
    ```

2. **Install the required Python packages:**

    ```bash
    pip install Flask requests
    ```

## Usage

### Run the Application

Run the Flask application:

```bash
python app.py


The application will be accessible at http://localhost:5000/.

Endpoints
1. Get a list of available applications
Endpoint: /applications
Method: GET
Description: Retrieves a list of available applications from the Atlassian Marketplace.
Example Request:
curl http://localhost:5000/applications
Example Response:

{
  "applications": ["Jira", "Confluence", "Bitbucket"]
}

2. Get apps based on specified parameters
Endpoint: /get-apps
Method: GET
Query Parameters:
application (required): The name of the application (e.g., "Jira").
hosting_type: The hosting type (e.g., "cloud").
filter: Additional filters for apps.
search_text: Search text for filtering apps.
Description: Retrieves information about apps based on the specified parameters.
Example Request:
curl http://localhost:5000/get-apps?application=Jira&hosting_type=cloud&filter=featured&search_text=collaboration
[
  {
    "app name": "Example App",
    "description": "An example app description.",
    "link": "https://marketplace.atlassian.com/apps/example-app",
    "total users": 10000,
    "total installs": 5000,
    "categories": ["Integration", "Collaboration"],
    "downloads": 100000,
    "average stars": 4.5,
    "review count": 200,
    "vendor": "Example Vendor"
  },
  // ... (other apps)
]

