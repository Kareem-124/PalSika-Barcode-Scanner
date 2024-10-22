# Barcode Scanning and Product Management Web Application

## Table of Contents

  

- Project Description

- Features

- Technologies Used

- Setup Instructions

- Usage

- Database

- Project Structure

- Contributing

- License

- Future plan

  

# Project Description

  

This is a Django-based web application that allows users to scan barcodes using a smartphone camera, retrieve product information from a database, and manage the product catalog. The project is divided into two phases:

  

Phase One: Building the barcode scanning functionality with product retrieval, allowing users to add, edit, or search for products.

Phase Two: Implementing a search page where all available products are listed in a table format with a search bar for quick lookup.

  

# Features

  

Barcode Scanning: Users can scan a product barcode and retrieve its details.

Product Management: Users can add and edit product details.

Product Listing: Displays all products in a searchable table format.

Mobile Compatibility: The application is optimized for mobile devices, especially the barcode scanning feature.

  

# Technologies Used

  

Backend Framework: Django

Frontend: HTML, CSS, JavaScript

Database: SQLite (default for Django projects)

Barcode Scanning Library: QuaggaJS

Responsive Design: CSS Media Queries for mobile compatibility

  

# Setup Instructions

  

To get the project up and running locally, follow these steps:

Prerequisites

  

Python 3.x must be installed on your system

Django should be installed (pip install django)

  

# Steps

  

Clone the repository:

  

```bash

git  clone  https://github.com/Kareem-124/PalSika-Barcode-Scanner.git

cd  barcode-scanning-app

```

Create a virtual environment:

  

```bash
  
python  -m  venv  venv

source  venv/bin/activate  # On Windows: venv\Scripts\activate

```

Install the required dependencies:

  

```bash
pip  install  -r  requirements.txt
```

Set  up  the  database:

```bash
python manage.py migrate
```

Create a superuser to access the Django admin:


```bash
python  manage.py  createsuperuser
```

Run the development server:

  

```bash
python  manage.py  runsslserver  0.0.0.0:8000
```
  

We  are  required  to  run  the  server  using  "https"  to  be  able  to  use  the  devices  cameras.

open  your  command  prompt  and  type:  ipconfig

search  for  the  IPv4  Address,  it  should  look  something  like  this:  192.168.10.5

Open  your  browser  and  go  to  https://192.168.10.5:8000 (This is  just  an  example  you  need  to  enter  you  IPv4  address) to view the application.


# Usage

## Phase One: Barcode Scanning

  

Scan Products: Click on the scan button, select the camera, and scan the barcode. The product details will be displayed.

Note: Some smart phones cameras auto focuse only once - when they are turned on- so make sure you point the camera to the required bar code before pressing the scan button.

Manage Products: You can add new products or edit existing ones if the barcode is unregistered or needs updating.

  

## Phase Two: Product Search

  

Search Products: Visit the /search page to search for products by name. The page displays a searchable table with all available products.

  

# Database

  

This project uses an SQLite database for storing product information. Each product has the following fields:

  

Product ID: The unique identifier for the product.

Name: The name of the product.

Customer Price: The price at which the product is sold to customers.

Retail Price: The retail price of the product.

Category: The category of the product.

Notes: Additional details about the product.

  

# Project Structure

  
  

barcode-scanning-app/

│

├── app_name/

│ ├── migrations/

│ ├── static/

│ ├── templates/

│ ├── views.py

│ ├── models.py

│ ├── urls.py

│ └── ...

│

├── db.sqlite3

├── manage.py

├── requirements.txt

└── README.md

  

# Key Files

  

views.py: Contains the view logic for handling barcode scanning and product listing.

models.py: Defines the Product model.

search_for_product.html: Front-end page for product search and listing.

urls.py: Defines URL routes for the app.

  

# Contributing

  

If you'd like to contribute to this project, feel free to submit pull requests or report any issues. Contributions are welcome!

Steps to Contribute:

  

Fork the repository.

Create a feature branch (git checkout -b feature/your-feature).

Commit your changes (git commit -am 'Add some feature').

Push to the branch (git push origin feature/your-feature).

Create a new Pull Request.

  

# License

  

This project is licensed under the MIT License.

  

# Future Plan

  

Features will be added:

- [ ] Back-end Validation.

- [x]  Cookies to save the last selected camera for the user.

- [x]  Change the "All-Products" page layout to improve the readability for the user when using small screens.

- [x]  Add delete/edit products at "All-Products" page.

- [x]  Adding 'beep' sound when scanning products.

- [x] Improving the security for the application to meet the web security standers.

- [x] Creating and adding Favicon.

- [ ] Try and make it compatible with iphone devices and older android devices.

# Demo (Work In Progress)
