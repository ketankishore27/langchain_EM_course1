from dotenv import load_dotenv
from flask import Flask, render_template, jsonify, request
from ice_breaker_linkedin import ice_break_with

load_dotenv()

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/process", methods=["POST"])
def process():
    name = request.form["name"]
    summary, profile_pic_url = ice_break_with(name=name)
    print(f"profile_pic_url url: {profile_pic_url}")
    if not profile_pic_url:
        profile_pic_url = "https://media.licdn.com/dms/image/v2/D4D03AQEoOIm-fzLVdg/profile-displayphoto-shrink_400_400/profile-displayphoto-shrink_400_400/0/1675868636282?e=1753920000&v=beta&t=M8-2c5a2SZj5AkfW27gX2fxNrkoAN1MbCjhK52XrjZM"
    print("Going to return the main Control")
    return jsonify(
        {
            "summary_and_facts": summary.to_dict(),
            "photoUrl": profile_pic_url
        }
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=5050)