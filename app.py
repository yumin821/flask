from flask import Flask, request, jsonify
import random

app = Flask(__name__)
user_store = {}

@app.route("/api/autosync", methods=["POST"])
def autosync():
    data = request.json
    roblox_id = data["robloxUserId"]
    code = data["code"]

    user_store[roblox_id] = {
        "code": code,
        "discordId": None
    }

    return jsonify({"message": "등록 완료", "code": code})

@app.route("/api/link", methods=["POST"])
def link_discord():
    data = request.json
    discord_id = data["discordId"]
    roblox_id = data["robloxUserId"]

    if roblox_id in user_store:
        user_store[roblox_id]["discordId"] = discord_id
        return jsonify({"code": user_store[roblox_id]["code"]})
    return jsonify({"error": "등록된 유저 없음"}), 404

@app.route("/api/code/<discord_id>", methods=["GET"])
def get_code(discord_id):
    for roblox_id, info in user_store.items():
        if info["discordId"] == discord_id:
            return jsonify({"code": info["code"], "robloxId": roblox_id})
    return jsonify({"error": "없음"}), 404

@app.route("/")
def home():
    return "✅ 서버 작동 중!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
