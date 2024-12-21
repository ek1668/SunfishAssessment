Flask IVF Calculation API

This API is built with Flask and is designed to calculate IVF success metrics based on user-provided medical and demographic data. The application is containerized using Docker and exposes the main endpoint at http://127.0.0.1:5000/calculate_ivf/.

Files Included
    app.py: The main Flask application.
    Dockerfile: Configuration for containerizing the app.
    requirements.txt: Dependencies for the Flask API.
    ivf_success_formulas.csv

Running the API

1. Build the Docker Image:
    Clone the repository and navigate to the project directory:

    docker build -t sunfish-image .

2. Run the Docker Container:
    Run the container, exposing port 5000:

    docker run -p 5000:5000 sunfish-image

3. Access the API:
    Once the container is running, the API can be accessed at:

    http://127.0.0.1:5000/calculate_ivf/

API Endpoint
POST /calculate_ivf/
Description:
Calculates IVF success metrics based on the user’s medical and demographic information.

Request Body:
    The API requires the following JSON fields(with value samples) to be sent in a POST request:

```
{
    "user_age": 32, // Age of the user (integer).
    "user_weight_in_lbs": 150, // Weight of the user in pounds (integer).
    "user_height_in_feet": 5, // Height in feet (integer).
    "user_height_in_inches": 8, // Remaining height in inches (integer).
    "using_own_eggs": "TRUE", // Whether the user is using their own eggs ("TRUE" or "FALSE").
    "previously_attempted_ivf": "TRUE", // Whether the user has previously attempted IVF ("TRUE" or "FALSE").
    "reason_for_infertility_known": "TRUE", // Whether the reason for infertility is known ("TRUE" or "FALSE").
    "tubal_factor": "FALSE", // Presence of tubal factor infertility ("TRUE" or "FALSE").
    "male_factor": "FALSE", // Presence of male factor infertility ("TRUE" or "FALSE").
    "endometriosis": "FALSE", // Presence of endometriosis ("TRUE" or "FALSE").
    "ovulatory_disorder": "FALSE", // Presence of ovulatory disorder ("TRUE" or "FALSE").
    "diminished_ovarian_reserve": "FALSE", // Presence of diminished ovarian reserve ("TRUE" or "FALSE").
    "uterine_factor": "FALSE", // Presence of uterine factor infertility ("TRUE" or "FALSE").
    "other_infertilty_reason": "FALSE", // Presence of other infertility reasons ("TRUE" or "FALSE").
    "unexplained_infertility": "FALSE", // Whether the infertility is unexplained ("TRUE" or "FALSE").
    "prior_pregnancies": 1, // Number of prior pregnancies (integer).
    "prior_live_births": 1 // Number of prior live births (integer).
}
```

Response:
On success, the API returns:

{"success_probability":<PERCENTAGE_VALUE>}
