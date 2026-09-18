import os
from dotenv import load_dotenv
from flask import Flask, jsonify, request, send_from_directory

from lib.answer_builder import generate_socratic_answer
from lib.knowledge import get_all_slides, get_slide_by_id

env_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(dotenv_path=env_path, override=True)

app = Flask(__name__, static_folder="public", static_url_path="")


@app.get("/api/health")
def health():
    return jsonify({
        "ok": True,
        "service": "tudaibotuc-socratic-tutor",
        "track": "Track A · VLearn Tutor (A1)",
        "model": "gemini-3.6-flash (Live API)",
        "slides_count": len(get_all_slides()),
    })


@app.get("/api/slides")
def slides():
    """Trả về danh sách tất cả slide bài giảng (Day 1 / Day 2) cho Slide Viewer."""
    return jsonify({"slides": get_all_slides()})


@app.post("/api/chat")
def chat():
    payload = request.get_json(silent=True) or {}
    question = str(payload.get("question", "") or "").strip()
    topic_id = str(payload.get("topic_id", "") or "").strip() or None
    selected_text = str(payload.get("selected_text", "") or "").strip() or None

    if not question and not selected_text:
        return jsonify({"error": "Vui lòng nhập câu hỏi hoặc bôi đen văn bản trên slide."}), 400

    result = generate_socratic_answer(
        question=question,
        topic_id=topic_id,
        selected_text=selected_text
    )
    return jsonify(result)


@app.route("/")
def index():
    return send_from_directory(app.static_folder, "index.html")


if __name__ == "__main__":
    port = int(os.getenv("PORT", "3000"))
    app.run(host="0.0.0.0", port=port, debug=False)
