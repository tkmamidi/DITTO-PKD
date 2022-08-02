# DITTO-PKD

## Table of Contents

- [DITTO-PKD](#ditto-pkd)
    - [Aim](#aim)
    - [Description](#description)
    - [Data](#data)
    - [Usage](#usage)
        - [Installation](#installation)
        - [Requirements](#requirements)
        - [Activate pip environment](#activate-pip-environment)
        - [Steps to run ](#steps-to-run)
            - [Run Streamlit App](#run-streamlit-app)
    - [Contact Info](#contact-info)

## Aim

Easy to use web interface for biologists to look for PKD1/2 variants and understand their deleteriousness using DITTO scores.

## Description

A web app where anyone can lookup variants from either of PKD1 or PKD2 genes and understand the mechanism/details of
these variants such as domain, function, DITTO deleterious score and Clinvar reported significance.

## Data

We are using PKD variants from dbNSFP database as well as PKDB. Annotations such as domain, function are extracted from
various public data sources like Interpro, Uniprot etc.,

## Usage

DITTO-PKD can be access at this streamlit [site](https://tkmamidi-ditto-pkd-srcpkd-app-pkd-6d7mf3.streamlitapp.com/).

### Installation

Installation simply requires fetching the source code. Following are required:

- Git

To fetch source code, change in to directory of your choice and run:

```sh
git clone -b pkd \
    https://github.com/tkmamidi/DITTO-PKD.git
```

### Requirements

*OS:*

Currently works only in Mac OS. Docker versions may need to be explored later to make it useable in Mac (and
potentially Windows).

*Tools:*

- Pip3

### Activate pip environment

Change in to root directory and run the commands below:

```sh
# create environment. Needed only the first time.
pip3 install -r requirements.txt
```

### Steps to run

#### Run Streamlit App

```sh
streamlit run src/pkd_app.py
```

## Contact Info

Tarun Mamidi | tmamidi@uab.edu

