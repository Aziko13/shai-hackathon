import hashlib, time
from typing import Dict, Tuple
import pandas as pd


class ArtifactStore:
    def __init__(self, ttl_sec: int = 3600, max_items: int = 128):
        self.ttl = ttl_sec
        self.max = max_items
        self._data: Dict[str, Tuple[float, pd.DataFrame]] = {}

    def put(self, df: pd.DataFrame) -> str:
        key = hashlib.sha1(
            f"{time.time_ns()}|{len(df)}|{list(df.columns)}".encode()
        ).hexdigest()[:16]
        if len(self._data) >= self.max:
            # drop oldest
            oldest = sorted(self._data.items(), key=lambda kv: kv[1][0])[0][0]
            self._data.pop(oldest, None)
        self._data[key] = (time.time(), df.copy())
        return key

    def get(self, key: str) -> pd.DataFrame | None:
        rec = self._data.get(key)
        if not rec:
            return None
        ts, df = rec
        if time.time() - ts > self.ttl:
            self._data.pop(key, None)
            return None
        return df.copy()


ARTIFACTS = ArtifactStore()

if __name__ == "__main__":
    df = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
    key = ARTIFACTS.put(df)
    print(key)
    df2 = ARTIFACTS.get(key)
    print(df2)
