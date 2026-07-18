from flask import Flask
app = Flask(__name__)
@app.route("/")
def hello():
    """Root endpoint — returns a greeting."""
    return "Hello, from Flask App!"
@app.route("/health")
def health():
    """Health-check endpoint for container orchestrators."""
    return {"status": "ok"}
if __name__ == "__main__":
    # host="0.0.0.0" binds to all interfaces so Docker can forward traffic
    app.run(host="0.0.0.0", port=5000)
