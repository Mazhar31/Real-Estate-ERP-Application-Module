# Real-Estate-ERP-Application-Module

## Overview

This Odoo module, developed by *Mazhar Shafiq*, aims to provide a comprehensive solution for managing real estate properties. The module covers various aspects of real estate management, including property details, offers, property types, and tags.

## Features

### Property Management

- **Property Details:** Capture essential details such as title, description, postcode, availability date, expected price, and more.
- **Property Types:** Categorize properties into different types for better organization and filtering.
- **Tags:** Associate tags with properties to highlight specific features or characteristics.

### Property State Workflow

Properties go through different states, reflecting their lifecycle:

- **New:** A property that is newly listed.
- **Offer Received:** When offers are made on a property.
- **Offer Accepted:** After accepting an offer.
- **Sold:** When the property is successfully sold.
- **Cancelled:** If the property is cancelled, it cannot be sold.

### Offers Management

- **Offer Details:** Record offers with information such as price, partner details, and status.
- **Offer Acceptance:** Accepting an offer automatically sets the buyer and selling price for the corresponding property.
- **Offer Refusal:** Refusing an offer updates its status accordingly.

### User Management

- **Salesperson Properties:** View properties linked to a salesperson directly in the user form.

## Installation

1. Install the module by uploading it to your Odoo instance.
2. Ensure that the module dependencies are met, including the base module.
3. Once installed, navigate to the "Real Estate" menu in Odoo to access the different features.

## Usage

- **Properties:** Add and manage properties, specifying details, property types, and tags.
- **Property Offers:** Record and manage offers on properties.
- **Property Types:** Categorize properties into different types.
- **Tags:** Define and associate tags with properties.
- **User Management:** View properties linked to a salesperson in the user form.

## Version Information

- Module Version: 1.0
- Odoo Version: 16.0
