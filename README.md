# GENDERIZE-CLASSIFY-API

A lightweight REST API that classifies the likely gender of a name using the [Genderize.io](https://genderize.io) dataset. Built with Flask and Gunicorn, containerized with Docker, and deployed to **AWS EC2 @ [http://54.90.242.22/api/classify](http://54.90.242.22/api/classify) 🚀 🧬 🎯**

---

## SUMMARY

This API exposes a single GET endpoint `/api/classify` that accepts a `name` query parameter and returns a processed gender prediction. Rather than returning the raw Genderize.io response, the API applies its own processing logic on top — renaming fields, computing a confidence score (`is_confident`), and generating a fresh UTC timestamp (`processed_at`) on every request.

Confidence is determined by two conditions that must **both** be true: a probability of **0.70 or higher** AND a sample size of **100 or more** records. If either condition fails, `is_confident` is returned as `false`.

Edge cases such as unknown names, missing parameters, and Genderize API failures are all handled with structured error responses following a consistent format. CORS headers are explicitly set on every response so the API can be consumed from any origin.

---

## TECHNOLOGY USED

- **Python**
- **Flask**
- **Gunicorn**
- **Docker**
- **AWS EC2**

---

## SETTING UP LOCALLY

To set up locally, follow the steps below:

- Clone the repository:
  ```bash
  git clone https://github.com/doluthegreat/STAGE-0.git
  ```

- Navigate into the cloned directory:
  ```bash
  cd STAGE-0
  ```

- Create and activate a virtual environment:
  ```bash
  python3 -m venv venv
  source venv/bin/activate  # On Windows: venv\Scripts\activate
  ```

- Install dependencies:
  ```bash
  pip install -r requirements.txt
  ```

- Start the development server:
  ```bash
  python app.py
  ```

If all of the above was done correctly, the server should start on `http://127.0.0.1:5000`.

---

## RUNNING WITH DOCKER (Recommended)

To run the application using Docker:

- Build and start the container:
  ```bash
  docker-compose up -d --build
  ```

- To stop the container:
  ```bash
  docker-compose down
  ```

The API will be available on port `80` of your host machine.

---



### Endpoint

```
GET /api/classify?name=<name>
```




## DEPLOYMENT (AWS EC2 + Docker)

```
Internet → EC2 (port 80) → Docker container (Gunicorn → Flask)
```

To redeploy after a code update:

```bash
git pull
docker-compose up -d --build
```
