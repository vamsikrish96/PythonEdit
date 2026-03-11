# Deaf AI - Flask API Server
# Receives flight information and returns an anonymized ASL video with text overlay.
#
# Setup:
#     pip install flask moviepy
#
# Run:
#     python app.py

from flask import Flask, request, jsonify, send_file
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip
from moviepy.config import change_settings
import os
import uuid

app = Flask(__name__)

# CONFIGURATION
IMAGEMAGICK_PATH = r"C:\Program Files\ImageMagick-7.1.2-Q16-HDRI\magick.exe"
VIDEO_PATH       = r"C:\Users\Hassa\Downloads\Code & Notebooks\deaf ai\updated_video.mp4"
OUTPUT_FOLDER    = r"C:\Users\Hassa\Downloads\Code & Notebooks\deaf ai\outputs"
FONT_NAME        = "Arial-Bold"

# SETUP
change_settings({"IMAGEMAGICK_BINARY": IMAGEMAGICK_PATH})
os.makedirs(OUTPUT_FOLDER, exist_ok=True)


def generate_overlay_video(airline, flight, destination, gate):
    video    = VideoFileClip(VIDEO_PATH)
    width    = video.w
    height   = video.h
    duration = video.duration

    print(f"Video dimensions: {width}x{height}, {duration:.1f}s")
    print(f"Generating: {airline} | {flight} | {destination} | {gate}")

    subclip = video.subclip(0, duration)

    # Airline - yellow, second 7, left side
    txt_clip1 = TextClip(airline, font=FONT_NAME, fontsize=150, color='yellow')
    txt_clip1 = txt_clip1.set_start(7).set_duration(3).set_position((400, 300))

    # Flight number - green, second 12, right side
    txt_clip2 = TextClip(flight, font=FONT_NAME, fontsize=150, color='green')
    txt_clip2 = txt_clip2.set_start(12).set_duration(3).set_position((2500, 450))

    # Destination - orange, second 17, left side
    txt_clip3 = TextClip(destination, font=FONT_NAME, fontsize=150, color='orange')
    txt_clip3 = txt_clip3.set_start(17).set_duration(3).set_position((400, 300))

    # Gate - red, second 26, right side
    txt_clip4 = TextClip(gate, font=FONT_NAME, fontsize=300, color='red')
    txt_clip4 = txt_clip4.set_start(26).set_duration(3).set_position((2550, 450))

    # Combine
    final = CompositeVideoClip([subclip, txt_clip1, txt_clip2, txt_clip3, txt_clip4])

    # Save with unique filename
    output_filename = f"deaf_ai_{uuid.uuid4().hex[:8]}.mp4"
    output_path     = os.path.join(OUTPUT_FOLDER, output_filename)

    final.write_videofile(output_path, codec='libx264', audio_codec='aac')

    video.close()
    final.close()

    return output_path


@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "status":  "running",
        "project": "Deaf AI ASL Video Overlay API",
        "version": "1.0"
    })


@app.route("/generate-video", methods=["POST"])
def generate_video():
    data = request.get_json()

    if not data:
        return jsonify({"error": "No JSON data received"}), 400

    required_fields = ["airline", "flight", "destination", "gate"]
    missing = [f for f in required_fields if f not in data]

    if missing:
        return jsonify({
            "error":    f"Missing fields: {', '.join(missing)}",
            "required": required_fields
        }), 400

    airline     = data["airline"].upper()
    flight      = data["flight"].upper()
    destination = data["destination"].upper()
    gate        = data["gate"].upper()

    print(f"\nNew request received:")
    print(f"  Airline:     {airline}")
    print(f"  Flight:      {flight}")
    print(f"  Destination: {destination}")
    print(f"  Gate:        {gate}")

    try:
        output_path = generate_overlay_video(airline, flight, destination, gate)
        print(f"  Output: {output_path}")

        return send_file(
            output_path,
            mimetype="video/mp4",
            as_attachment=True,
            download_name=f"deaf_ai_{flight}.mp4"
        )

    except Exception as e:
        print(f"  ERROR: {str(e)}")
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    print("==================================================")
    print("  Deaf AI API Server")
    print("  Running on http://localhost:5000")
    print("  Press CTRL+C to stop")
    print("==================================================")
    app.run(debug=True, port=5000)