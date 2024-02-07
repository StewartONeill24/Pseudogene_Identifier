#Pseudogene Identifier

###Overview
The Pseudogene Identifier is a Django web application designed to identify pseudogenes by analyzing gene sequence mappability. This tool integrates with various bioinformatics resources to assess sequence homology, focusing on the likelihood of gene similarity with pseudogenes or repetitive regions. It also offers access to recent research articles related to the gene of interest, providing a comprehensive toolkit for researchers and clinicians in genetic analysis and testing.

###Features
Gene Mappability Analysis: Calculates a mappability metric for genes to identify sequence similarity with pseudogenes.
Literature Review: Provides links to the most recent research articles related to the gene of interest.
Visualization: Generates plots to visually represent the mappability of gene sequences.

###Installation
####Prerequisites
Python 3.6 or higher
Django 2.2
Other Python libraries as listed in requirements.txt

###Steps
Clone the repository:

git clone https://github.com/StewartONeill24/Pseudogene_Identifier.git

Navigate to the project directory:

cd Pseudogene_Identifier

Install the required dependencies:

pip install -r requirements.txt

Run the Django migrations to set up the database:

python manage.py migrate

Start the Django development server:

python manage.py runserver

Open a web browser and go to http://127.0.0.1:8000/ to view the application.

###Usage
On the homepage, enter the HGNC symbol of the gene of interest in the provided text area.
Click the "Search" button to submit the query.

The results page will display the mappability metric for the gene and links to recent research articles. If available, a visualization of the gene's mappability profile will also be shown.

###Contributing
Contributions to the Pseudogene Identifier project are welcome. Please follow the standard GitHub pull request process to propose changes. For major changes, please open an issue first to discuss what you would like to change.

###License
MIT

###Acknowledgements
This project utilizes data and tools from NCBI, BioPython, and other open-source bioinformatics resources.
Special thanks to all contributors and users of the Pseudogene Identifier project.
