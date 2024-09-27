# Insurance Premium Calculation API

This project is a FastAPI backend service that calculates insurance premiums based on user inputs. The API accepts
various parameters related to the insured individual or object and returns a calculated insurance premium.

## Features

- **FastAPI**: A modern, fast (high-performance) web framework for building APIs with Python 3.7+.
- **Insurance Premium Calculation**: The core functionality of the API is to calculate insurance premiums based on
  inputs provided by the user.
- **JSON Response**: The API returns the calculated premium in a structured JSON format.
- **Validation**: Input validation is handled automatically by FastAPI.

## Installation

### Prerequisites

- Python 3.7+
- pip (Python package installer)

### Setup

1. **Clone the repository:**

   ```bash
   git clone https://github.com/UbeyOzcan/insurance-premium-api.git
   cd insurance-premium-api
   ```

2. **Create a virtual environment:**

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install the dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **navigate to app folder**

   ```bash
   cd app
   ```
   
5. **Run the FastAPI server:**

   ```bash
   uvicorn api:app --host 127.0.0.1 --port 8080
   ```

   The API will be available at `http://127.0.0.1:8080`.

    The API interactive documentation will be available at `http://127.0.0.1:8080/docs`

## API Endpoints

### `POST /calculate-premium`

Calculates the insurance premium based on the provided input data.

- **Request Body:**

  ```json
  {
    "power": 20,
    "VehAge": 10,
    "DrivAge": 30,
    "BonusMalus": 10,
    "VehGas": "Regular",
    "Area": "D"
  }
  ```

- **Response:**

  ```json
  {
    "VehPower": [
        20
    ],
    "VehAge": [
        10
    ],
    "DrivAge": [
        30
    ],
    "BonusMalus": [
        10
    ],
    "VehGas": [
        "Regular"
    ],
    "Area": [
        "D"
    ],
    "Predicted Frequency": [
        0.0269
    ],
    "Predicted Severity": [
        624.51
    ],
    "Risk Premium": [
        16.8
    ]
  }
  ```

### Example Usage

You can test the API using tools like [Postman](https://www.postman.com/) or Powershell - RestMethod.

**Using Powershell - RestMethod:**

```shell
$response = Invoke-RestMethod 'http://127.0.0.1:8080?power=20&VehAge=10&DrivAge=30&BonusMalus=10&VehGas=Regular&Area=D' -Method 'GET' -Headers $headers
$response | ConvertTo-Json
```


## Development

### Directory Structure

```plaintext
insurance-premium-api/
│
├── app/
│   ├── __init__.py
│   ├── main.py        # Main application file
│   ├── models.py      # Data models for request and response
│   ├── routes.py      # API route definitions
│   └── utils.py       # Utility functions for premium calculation
│
├── tests/             # Unit and integration tests
│
├── requirements.txt   # Python dependencies
└── README.md          # Project documentation
```

### Running Tests

Tests are located in the `tests/` directory. You can run tests using `pytest`:

```bash
pytest
```

## Contributing

Contributions are welcome! Please fork the repository and create a pull request with your changes.

### Steps to Contribute

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/your-feature-name`).
3. Commit your changes (`git commit -am 'Add some feature'`).
4. Push to the branch (`git push origin feature/your-feature-name`).
5. Create a new Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

If you have any questions or feedback, feel free to reach out to the project maintainers.
