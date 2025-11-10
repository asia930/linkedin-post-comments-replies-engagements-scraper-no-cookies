import json
import os

class Exporter:
    def to_json(self, data, file_path):
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            print(f"[Exporter] Successfully saved JSON to {file_path}")
        except Exception as e:
            print(f"[Exporter Error] {e}")