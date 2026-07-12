#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Cost flow 本地发布服务
- 静态文件服务（index.html / data/ 等）
- POST /api/publish ：接收前端发布的全量数据集，写入 data/costflow.json
注意：仅用于本地预览（127.0.0.1:8765），不做 git 推送；推送由每日自动化完成。
"""
import json
import os
import sys
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

ROOT = os.path.dirname(os.path.abspath(__file__))


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=ROOT, **kwargs)

    def _send_json(self, code, obj):
        payload = json.dumps(obj, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(payload)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(payload)

    def do_POST(self):
        path = self.path.split("?")[0].rstrip("/")
        if path == "/api/publish":
            try:
                length = int(self.headers.get("Content-Length", 0) or 0)
                if length <= 0:
                    raise ValueError("empty body")
                raw = self.rfile.read(length)
                data = json.loads(raw.decode("utf-8"))
                if not isinstance(data, dict) or "months" not in data:
                    raise ValueError("payload must be {version, months}")
                # 仅允许写入固定的 data/costflow.json，杜绝路径穿越
                out_dir = os.path.join(ROOT, "data")
                os.makedirs(out_dir, exist_ok=True)
                out_path = os.path.join(out_dir, "costflow.json")
                with open(out_path, "w", encoding="utf-8") as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                self._send_json(200, {"ok": True, "bytes": len(raw),
                                      "months": list(data.get("months", {}).keys())})
            except Exception as e:
                self._send_json(400, {"ok": False, "error": str(e)})
        else:
            self._send_json(404, {"ok": False, "error": "not found"})

    def log_message(self, fmt, *args):
        sys.stderr.write("[costflow-server] " + (fmt % args) + "\n")


if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8765
    httpd = ThreadingHTTPServer(("127.0.0.1", port), Handler)
    print(f"Serving {ROOT} on http://127.0.0.1:{port}")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nstopped")
