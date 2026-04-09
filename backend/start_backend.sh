#!/bin/bash
export AWS_SESSION_TOKEN="FwoGZXIvYXdzECsaDI2F64yroB9HqaoJQyLBATD5dIs/0chyMZEdiB+UKjVLCd+AfUgAu3O7ff5IL+fRc18jJhgOoadszOphK+ByvmPGroocmk3/+G70XDdK8kwvA5UImh3fR8qV4vIbCxNc9YWjVT2W6UQebcRgYa1c3h1qHKk0mR6/to2d5Ln7Z9uI4WomalgP3c45MV/nQYOKuwOIjPnAwXl00WWVfReMAFlFFoPzqJXM9C9BJugy5GKaz6aCNg1taLol1vJPit4AA0UtJYgluJh6nDHyWcTf2SAohpLyzAYyLV8LSn4MMcrM9/CEOObXgWiPIwxqc1Scnw7bqZn9+If9CsmsT/6rCyB4r+qq6A=="
cd /home/diship-test/dish-chat/backend
source .venv/bin/activate
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
