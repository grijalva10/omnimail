# Omnimail

Omnimail is a custom Frappe application designed to connect to Amazon Web Services (AWS) for sending emails and tracking various email events such as bounces, complaints, opens, and clicks. This README file provides an overview of the application and guides you through its setup and usage.

## Table of Contents
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)
- [Doctypes](#doctypes)
- [Support](#support)

## Features

Omnimail offers the following features:
- Sending emails using the AWS Simple Email Service (SES).
- Tracking email bounces to monitor failed delivery attempts.
- Tracking email complaints to identify potential issues with email content or delivery.
- Tracking email opens and clicks to measure recipient engagement.

## Prerequisites

Before installing Omnimail, make sure you have the following prerequisites in place:
- A Frappe or ERPNext instance set up and running.
- An AWS account with access to the Simple Email Service (SES) and Simple Notification Service (SNS).
- AWS API credentials (access key and secret key) with appropriate permissions for SES and SNS.

## Installation

To install Omnimail, follow these steps:

1. Clone the Omnimail repository to your Frappe or ERPNext instance's `apps` directory:


    $ cd /path/to/frappe/apps

    $ git clone https://github.com/your-username/omnimail.git


2. Install the application using the Frappe Bench command:


    $ cd /path/to/frappe

    $ bench --site your-site-name install-app omnimail



## Configuration

After installing Omnimail, you need to configure it to connect to your AWS account. Follow these steps to set up the necessary configurations:

1. Open the Omnimail application in your Frappe or ERPNext instance.
2. Navigate to the **AWS Settings** page.
3. Enter your AWS API credentials (access key and secret key).
4. Save the configuration.

## Usage

Omnimail provides an intuitive user interface within your Frappe or ERPNext instance for managing email sending and tracking. Here's how to get started:

1. Log in to your Frappe or ERPNext instance.
2. Open the Omnimail application.
3. Use the provided options to compose and send emails using AWS SES.
4. Access the relevant sections to track and analyze email bounces, complaints, opens, and clicks.

## Contributing

We welcome contributions to enhance Omnimail and address issues. If you'd like to contribute, please follow these steps:

1. Fork the Omnimail repository.
2. Create a new branch for your feature or bug fix.
3. Make the necessary changes.
4. Test your changes thoroughly.
5. Submit a pull request explaining your changes and the problem they solve.

## License

Omnimail is open-source software licensed under the [MIT License](https://opensource.org/licenses/MIT). You are free to modify and distribute it as per the terms of the license.

## Doctypes

Omnimail utilizes the following doctypes to track and manage email events:

1. **Email Status**: Represents the status of an email sent through AWS SES, including information such as the AWS message ID, status (e.g., bounced, delivered, opened), and associated bounces, complaints, opens, and clicks.

2. **Email Bounce**: Captures details about bounced emails, including the email ID, bounce type, sub-type, and the email addresses of recipients who experienced the bounce.

3. **Email Complaint**: Tracks complaints received for emails, including the email ID, complaint feedback type (e.g., abuse, not-spam), and the email addresses of recipients who made the complaint.

4. **Email Open Event**: Records events when recipients open emails, storing the email ID, the IP address of the recipient who opened the email, and the date and time of the open event.

5. **Email Click Event**: Captures events when recipients click on links within emails, storing the email ID, the IP address of the recipient who clicked the link, the URL of the clicked link, and the date and time of the click event.

These doctypes enable tracking and analysis of email events and recipient engagement within Omnimail.

## Support

If you encounter any issues or have questions regarding Omnimail, please feel free to [open an issue](https://github.com/your-username/omnimail/issues) in the GitHub repository. We'll be glad to assist you.

Thank you for using Omnimail!
