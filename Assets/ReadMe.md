# Food Donation and Notification System

## Table of Content

- [Food Donation and Notification System](#food-donation-and-notification-system)
  - [Table of Content](#table-of-content)
  - [Overview](#overview)
  - [Key Features](#key-features)
  - [Technologies Used](#technologies-used)
  - [Getting Started](#getting-started)
    - [Prerequisites](#prerequisites)
    - [Installation](#installation)
    - [Usage](#usage)
  - [Contributing](#contributing)
  - [License](#license)
  - [Authors Info](#authors-info)

## Overview

The Food Donation and Notification System is a comprehensive platform designed to facilitate the donation of food items and funds between donors and recipients. The system optimizes the matching process based on geographical proximity, ensuring efficient food distribution.

## Key Features

- **User Authentication:** Secure registration and login for donors, agents, and recipients.
- **Matching Algorithm:** Efficiently connects donors with nearby recipients using geospatial data.
- **Notification System:** Alerts users of matched donations, system updates, and important events.
- **Flexible Donations:** Donors can contribute both food items and monetary donations via M-Pesa integration.

## Technologies Used

- Python
- Geopy
- Logging
- M-Pesa Daraja API

[Go Back to the top](#overview)

## Getting Started

### Prerequisites

- Python installed
- M-Pesa Daraja API credentials

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/food-donation-system.git

2. Install dependencies:

   ```bash
   pip install -r requirements.txt

3. Set up M-Pesa Daraja API credentials in config.py:

   ```bash
   M_PESA_API_KEY = 'your_api_key'
   M_PESA_PUBLIC_KEY = 'your_public_key'
   M_PESA_SERVICE_PROVIDER_CODE = 'your_service_provider_code'
   M_PESA_INITIATOR_NAME = 'your_initiator_name'

### Usage

1. Run the system:

   ```bash
   python food_donation_system.py

2. Follow the on-screen prompts to register, donate, view history, and more.

## Contributing

Contributions are welcome! Please follow the Contributing Guidelines.

## License

This project is licensed under the MIT License.

This project is licensed under the [MIT License](./License).

## Authors Info

`Linked` - [Richard Orito](https://www.linkedin.com/in/richie-orito/)

`Github` - [RICHIE ORITO](https://github.com/RichieOrito)

[Go Back to the top](#overview)
