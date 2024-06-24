# LLM Dataset Generator

![Version](https://img.shields.io/badge/Version-0.2.0-blue)
![License: CC0-1.0](https://img.shields.io/badge/License-CC0%201.0-lightgrey.svg)
![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-🦜🔗-blue)
![NLP](https://img.shields.io/badge/NLP-Natural_Language_Processing-green)

## Overview

The LLM Dataset Generator is an open-source tool designed to facilitate the creation of text datasets using various language models. This repository provides a framework for generating and collecting text data, supporting research and development in natural language processing (NLP) and related fields.

## License

This project is released under the CC0 1.0 Universal license. It is freely available for use by anyone for research, personal development, or commercial purposes without restriction. For more details, please refer to the [LICENSE](LICENSE) file.

## Examples

Check the following for actual output examples:

- [article_1](phi-3-text-generator/out.example/article_1.txt)
- [article_2](phi-3-text-generator/out.example/article_2.txt)
- [article_3](phi-3-text-generator/out.example/article_3.txt)

For Jupyter Notebook execution results, see:

- [phi-3-text-generator.ipynb](phi-3-text-generator/phi-3-text-generator.ipynb)

# Setup Guide for Ollama and Phi-3 Text Generator

You can check the code from [`phi-3-text-generator/`](phi-3-text-generator).

## 1. Creating and Starting the Ollama Container

To start the Ollama container and install the Phi-3:14B model, follow these steps:

### Prerequisites

- Docker Desktop must be installed.

### Steps

1. Open a terminal and pull the Ollama Docker image from Docker Hub:

   ```sh
   docker pull ollama/ollama:latest
   ```

2. Run the Ollama container with the following command:

   ```sh
   docker run -d --gpus=all -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama
   ```

3. Verify that the container is running:

   ```sh
   docker ps
   ```

   Example output:

   ```sh
   CONTAINER ID   IMAGE                 COMMAND                  CREATED          STATUS          PORTS                     NAMES
   aa492e7068d7   ollama/ollama:latest  "/bin/ollama serve"      9 seconds ago    Up 8 seconds    0.0.0.0:11434->11434/tcp  ollama
   ```

4. Check if Ollama is running correctly:

   ```sh
   curl localhost:11434
   ```

   You should see a message indicating that Ollama is running.

5. Pull the Phi-3:14B model:

   ```sh
   docker exec -it ollama ollama pull phi3:medium
   ```

## 2. How to Use the Project

Before running `phi-3-text-generator.py`, you can modify several constants in the file.

### Constants to Set

- **OLLAMA_BASE_URL**:
  - If running inside the Docker container: `"http://host.docker.internal:11434"`
  - If running locally: `"http://localhost:11434"`
- **TARGET_SENTENCE_COUNT**: Specify the number of sentences to generate.
- **OUTPUT_FILE_COUNT**: Specify the number of output files to generate.
- **OUTPUT_DIRECTORY**: Specify the directory where the generated files will be saved.

### Execution Steps

1. Open the `phi-3-text-generator.py` file and set the constants as needed.
2. Install poetry
   ```sh
   pip install poetry
   ```
3. Install the project dependencies. Go to the root directory of the project, and run:
   ```sh
   poetry install
   ```
4. Activate the virtual environment:
   ```sh
   poetry shell
   ```
5. Run the script with the following command:

   ```sh
   python phi-3-text-generator.py
   ```

## 3. How to Check the Generated Files

By default, the generated files will be saved in an `out` directory created in the same directory as the script.

### Steps to Verify

1. Navigate to the directory where the script was executed.
2. Check for the `out` directory:

   ```sh
   ls out
   ```
