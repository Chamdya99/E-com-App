E-Commerce Selenium Test Automation
A Python-based test automation framework for e-commerce applications using Selenium WebDriver and Pytest.
📋 Project Overview
This project contains automated tests for an e-commerce application, including:

User authentication (login/logout)
Shopping cart functionality
Dashboard operations

🛠️ Technologies Used

Python 3.x
Selenium WebDriver - Browser automation
Pytest - Testing framework
Page Object Model (POM) - Design pattern for maintainable test code

📁 Project Structure
ecom3/
│
├── pages/                      # Page Object Model classes
│   ├── cart_page.py           # Shopping cart page objects
│   ├── dashboard_page.py      # Dashboard page objects
│   └── login_page.py          # Login page objects
│
├── tests/                      # Test files
│   ├── test_cart.py           # Shopping cart tests
│   ├── test_dashboard.py      # Dashboard tests
│   └── test_login.py          # Login/logout tests
│
├── utilities/                  # Utility functions
│   └── wait_utils.py          # Wait helper functions
│
├── config/                     # Configuration files
│   └── config.py              # Test configuration
│
├── conftest.py                # Pytest fixtures and configuration
├── requirements.txt           # Python dependencies
├── pytest.ini                 # Pytest configuration
├── .gitignore                 # Git ignore file
└── README.md                  # This file
🚀 Getting Started
Prerequisites

Python 3.8 or higher
pip (Python package manager)
Chrome/Firefox browser installed

Installation

Clone the repository

bash   git clone https://github.com/YOUR_USERNAME/ecom-selenium-tests.git
   cd ecom-selenium-tests

Create a virtual environment

bash   python -m venv venv

Activate the virtual environment

On Windows:



bash     venv\Scripts\activate

On macOS/Linux:

bash     source venv/bin/activate

Install dependencies

bash   pip install -r requirements.txt
🧪 Running Tests
Run all tests
bashpytest
Run specific test file
bashpytest tests/test_cart.py
pytest tests/test_login.py
pytest tests/test_dashboard.py
Run with verbose output
bashpytest -v
Run with detailed output and show print statements
bashpytest -v -s
Run specific test
bashpytest tests/test_cart.py::test_cart_functionality
Run tests and generate HTML report
bashpytest --html=report.html
📝 Test Coverage
Login Tests (test_login.py)

✅ User login functionality
✅ Logout functionality
✅ URL verification after login

Cart Tests (test_cart.py)

✅ Add items to cart
✅ Remove items from cart
✅ Cart persistence

Dashboard Tests (test_dashboard.py)

✅ Dashboard accessibility
✅ Dashboard elements verification

⚙️ Configuration
Edit config/config.py to customize:

Base URL
Browser type
Timeouts
Test credentials

🤝 Contributing

Fork the repository
Create a feature branch (git checkout -b feature/AmazingFeature)
Commit your changes (git commit -m 'Add some AmazingFeature')
Push to the branch (git push origin feature/AmazingFeature)
Open a Pull Request

📄 Best Practices

Follow Page Object Model (POM) pattern
Keep tests independent and atomic
Use meaningful test and variable names
Add appropriate wait conditions
Clean up test data after execution

🐛 Troubleshooting
WebDriver Issues

Ensure ChromeDriver/GeckoDriver is installed and in PATH
Or install webdriver-manager: pip install webdriver-manager

Test Failures

Check if the application URL is accessible
Verify element locators are up to date
Ensure proper wait conditions are implemented


🙏 Acknowledgments

Selenium WebDriver documentation
Pytest documentation
Page Object Model design pattern
