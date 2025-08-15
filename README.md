# pse-swe

## Overview

PSE Software Engineering LE4 and LE5

For the DDD course we use Python as programming language.

There are 2 project folders:
-solid
-ddd

And one paper folder with some intersting design, architecture and ddd papers and articles.

solid is an implementation of the SOLID patterns by Bob Martin. It need no special environment. Just a python >= 3.11. We used 3.11.

ddd is ean implementation of some ddd pattern. We use environment wir some extra libraries.

## Installation

```bash
conda create --name "pse-swe" python=3.11
conda activate pse-swe
pip install "fastapi[standard]"
pip install SQLAlchemy
pip install requests
```

or

```bash
conda create --name "pse-swe" python=3.11
conda activate pse-swe
pip install -r requirements.txt
```

## Run the FastAPI app

```bash
fastapi dev app.py
```

When running the fastapi CLI the default port is 8000, which can be overwritten with the --port flag.

Get Swagger docs with: <http://localhost:8000/docs>