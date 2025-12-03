from flask import Flask, render_template, request, redirect, jsonify, Response
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import (
    JWTManager, create_access_token, jwt_required,
    get_jwt_identity, get_jwt, set_access_cookies, unset_jwt_cookies
)
import datetime
import cv2
from ultralytics import YOLO
from collections import Counter
import os
from werkzeug.utils import secure_filename
import json


app = Flask(__name__, static_url_path="/static")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "static", "uploads")
INSTANCE_FOLDER = os.path.join(BASE_DIR, "instance")

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(INSTANCE_FOLDER, exist_ok=True)

DB_PATH = os.path.join(INSTANCE_FOLDER, "database.db")

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_PATH}"
app.config["SECRET_KEY"] = "secret123"
app.config["JWT_SECRET_KEY"] = "jwt_secret123"
app.config["JWT_TOKEN_LOCATION"] = ["cookies"]
app.config["JWT_COOKIE_CSRF_PROTECT"] = False

db = SQLAlchemy(app)
jwt = JWTManager(app)

@app.route("/")
def home():
    return redirect("/login2")

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

    def check_password(self, p):
        return self.password == p


with app.app_context():
    db.create_all()


model = YOLO("yolov8n.pt")
camera = cv2.VideoCapture(0)

latest_counts = {}
detection_active = True


def annotate(img, results):
    if not len(results):
        return img

    for box, cls in zip(results[0].boxes.xyxy, results[0].boxes.cls):
        x1, y1, x2, y2 = map(int, box)
        label = model.names[int(cls)]

        cv2.rectangle(img, (x1, y1), (x2, y2), (0,255,0), 2)
        cv2.putText(img, label, (x1, y1-10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,0), 2)
    return img

def detect(frame):
    return model.predict(frame, verbose=False)


def gen_frames():
    global detection_active, latest_counts
    while True:
        ok, frame = camera.read()
        if not ok:
            continue

        if detection_active:
            results = detect(frame)

            if len(results):
                labels = [model.names[int(c)] for c in results[0].boxes.cls.tolist()]
                latest_counts = Counter(labels)

            frame = annotate(frame, results)

        ret, buffer = cv2.imencode(".jpg", frame)
        if not ret:
            continue

        yield (
            b"--frame\r\n"
            b"Content-Type: image/jpeg\r\n\r\n" + buffer.tobytes() + b"\r\n"
        )

@app.route("/register2", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]

        if User.query.filter_by(email=email).first():
            return render_template("register2.html", error="Email already exists")

        db.session.add(User(name=name, email=email, password=password))
        db.session.commit()

        return redirect("/login2")

    return render_template("register2.html")

@app.route("/login2", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        user = User.query.filter_by(email=email).first()
        if not user:
            return render_template("login2.html", error="User not found")

        if not user.check_password(password):
            return render_template("login2.html", error="Wrong password")

        token = create_access_token(
            identity=user.email,
            additional_claims={"name": user.name},
            expires_delta=datetime.timedelta(hours=6)
        )

        resp = redirect("/dashboard")
        set_access_cookies(resp, token)
        return resp

    return render_template("login2.html")

@app.route("/logout")
def logout():
    resp = redirect("/login2")
    unset_jwt_cookies(resp)
    return resp


@app.route("/dashboard")
@jwt_required()
def dashboard():
    email = get_jwt_identity()
    claims = get_jwt()
    user = {"name": claims["name"], "email": email}
    return render_template("dashboard2.html", user=user)


@app.route("/video_feed")
def video_feed():
    return Response(gen_frames(), mimetype="multipart/x-mixed-replace; boundary=frame")

@app.route("/get_counts")
def get_counts():
    return jsonify({
        "count": latest_counts.get("person", 0),
        "details": dict(latest_counts)
    })

@app.route("/start_detection", methods=["POST"])
def start_detection():
    global detection_active
    detection_active = True
    return jsonify({"status": "started"})

@app.route("/stop_detection", methods=["POST"])
def stop_detection():
    global detection_active
    detection_active = False
    return jsonify({"status": "stopped"})


@app.route("/capture", methods=["POST"])
def capture():
    ok, frame = camera.read()
    if not ok:
        return jsonify({"status":"fail", "error":"Camera error"})

    results = detect(frame)
    frame = annotate(frame, results)

    filename = f"cap_{datetime.datetime.now().strftime('%H%M%S')}.jpg"
    path = os.path.join(UPLOAD_FOLDER, filename)
    cv2.imwrite(path, frame)

    counts = Counter([model.names[int(c)] for c in results[0].boxes.cls.tolist()]) if len(results) else {}

    return jsonify({
        "status": "success",
        "image_url": f"/static/uploads/{filename}",
        "counts": dict(counts)
    })

@app.route("/api/upload_image", methods=["POST"])
def upload_image():
    if "image" not in request.files:
        return jsonify({"status":"fail", "message":"No file"})

    file = request.files["image"]
    filename = secure_filename(file.filename)
    full = os.path.join(UPLOAD_FOLDER, filename)
    file.save(full)

    img = cv2.imread(full)
    results = detect(img)
    img = annotate(img, results)

    outname = "det_" + filename
    out_path = os.path.join(UPLOAD_FOLDER, outname)
    cv2.imwrite(out_path, img)

    counts = {}
    if len(results):
        labels = [model.names[int(c)] for c in results[0].boxes.cls.tolist()]
        counts = Counter(labels)

    return jsonify({
        "status":"success",
        "image_url": f"/static/uploads/{outname}",
        "counts": dict(counts)
    })


@app.route("/api/upload_video", methods=["POST"])
def upload_video():
    if "video" not in request.files:
        return jsonify({"status":"fail","message":"No video"})

    file = request.files["video"]
    filename = secure_filename(file.filename)
    full = os.path.join(UPLOAD_FOLDER, filename)
    file.save(full)

    cap = cv2.VideoCapture(full)
    if not cap.isOpened():
        return jsonify({"status":"fail","message":"Video error"})

    fps = cap.get(cv2.CAP_PROP_FPS) or 20
    w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    outname = "det_" + filename.split(".")[0] + ".mp4"
    out_path = os.path.join(UPLOAD_FOLDER, outname)

    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    out = cv2.VideoWriter(out_path, fourcc, fps, (w,h))

    counts = Counter()

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        results = detect(frame)
        frame = annotate(frame, results)

        if len(results):
            labels = [model.names[int(c)] for c in results[0].boxes.cls.tolist()]
            counts.update(labels)

        out.write(frame)

    cap.release()
    out.release()

    return jsonify({
        "status":"success",
        "video_url": f"/static/uploads/{outname}",
        "counts": dict(counts)
    })

if __name__ == "__main__":
    try:
        app.run(debug=True)
    finally:
        if camera.isOpened():
            camera.release()
        cv2.destroyAllWindows()
