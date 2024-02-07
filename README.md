# Pseudogene Identifier

## Overview
The Pseudogene Identifier is a Django web application engineered for identifying pseudogenes through the analysis of gene sequence mappability. This innovative tool leverages a variety of bioinformatics resources to evaluate sequence homology, particularly focusing on the probability of gene resemblance with pseudogenes or repetitive regions. Additionally, it facilitates access to the latest research articles pertaining to the gene of interest, thereby assembling an exhaustive toolkit for researchers and clinicians dedicated to genetic analysis and testing.

## Features
- **Gene Mappability Analysis**: Employs a mappability metric to discern sequence similarities with pseudogenes, enhancing the accuracy of genetic analyses.
- **Literature Review**: Automatically curates and provides links to the latest scientific articles related to the gene of interest, supporting ongoing research and study.
- **Visualization**: Offers graphical representations of gene mappability profiles, aiding in the intuitive understanding of analysis results.

## Installation

### Prerequisites
- Python version 3.6 or higher
- Django version 2.2
- Additional Python libraries as specified in `requirements.txt`

### Setup Instructions
1. **Clone the Repository**: Clone the Pseudogene Identifier project to your local machine using the following command:
   ```
   git clone https://github.com/StewartONeill24/Pseudogene_Identifier.git
   ```
2. **Navigate to the Project Directory**:
   ```
   cd Pseudogene_Identifier
   ```
3. **Install Dependencies**: Install the required Python libraries by running:
   ```
   pip install -r requirements.txt
   ```
4. **Initialize the Database**: Set up the database with Django migrations using:
   ```
   python manage.py migrate
   ```
5. **Launch the Development Server**: Start the Django development server to run the application:
   ```
   python manage.py runserver
   ```
6. **Access the Application**: Open a web browser and navigate to `http://127.0.0.1:8000/` to use the Pseudogene Identifier.

## Usage
To utilize the Pseudogene Identifier:
1. Visit the homepage and input the HGNC symbol of the gene of interest.
2. Click on the "Search" button to initiate the query.
3. The results page will display the gene's mappability metric along with relevant research articles. Visualizations of the gene's mappability profile will be presented if available.

## Contributing
We warmly welcome contributions to the Pseudogene Identifier project. To contribute:
- **Propose Changes**: Utilize the GitHub pull request process for minor enhancements or corrections.
- **Discuss Major Changes**: For significant modifications, please initiate a discussion by opening an issue. This allows for collaborative decision-making prior to the implementation of substantial alterations.

## License
This project is released under the MIT License, promoting open-source accessibility and modification.

## Acknowledgments
Our heartfelt gratitude goes out to all individuals who have contributed to developing and refining the Pseudogene Identifier. Special acknowledgements are extended to the National Center for Biotechnology Information (NCBI), BioPython, and the numerous open-source bioinformatics resources that have made this project possible.
