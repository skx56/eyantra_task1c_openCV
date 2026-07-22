# eYantra OpenCV Map Processing

<p align="center">
<img alt="Python" src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge" />
  <img alt="OpenCV" src="https://img.shields.io/badge/OpenCV-5C3EE8?style=for-the-badge" />
  <img alt="Computer Vision" src="https://img.shields.io/badge/Computer%20Vision-5C3EE8?style=for-the-badge" />
</p>

<p align="center">
  <strong>A computer-vision task implementation for processing map imagery and extracting structured information with OpenCV.</strong>
</p>

This repository contains a focused OpenCV solution for an eYantra task. The project is intentionally compact, with the main implementation script handling image-processing logic for the provided map-processing challenge.

## Core Capabilities

- Processes map imagery through OpenCV-based logic.
- Implements task-specific extraction and analysis in a single Python script.
- Provides a clear starting point for extending into modular image-processing utilities.
- Documents setup and execution for reproducible review.

## Technical Architecture

The project centers on one Python implementation file. This keeps the challenge solution easy to run and inspect while leaving room for future modularization into preprocessing, detection, and reporting functions.

## Architecture Diagram

```mermaid
flowchart LR
  Map["Input Map Image"] --> Script["WD_3200_map.py"]
  Script --> Preprocess["Image Preprocessing"]
  Preprocess --> Detect["OpenCV Detection Logic"]
  Detect --> Extract["Structured Map Information"]
  Extract --> Output["Task Output"]
```

## Technology Stack

- Python implementation.
- OpenCV-based computer-vision workflow.
- Challenge-oriented script structure.
- Suitable for notebook or CLI expansion.

## Repository Structure

- `WD_3200_map.py` - Primary OpenCV task solution.

## Getting Started

```bash
python -m venv .venv
source .venv/bin/activate
pip install opencv-python numpy
```

```bash
python WD_3200_map.py
```

## Professional Context

This project demonstrates practical computer vision, challenge execution, and image-processing implementation discipline.
