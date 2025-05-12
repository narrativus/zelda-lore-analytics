# etl.py
"""
Light-weight ETL for Zelda Dungeon text dumps.
Usage from CLI:  poetry run python scripts/ingest.py
"""
import asyncio
import re
from pathlib import Path

import aiohttp
import pandas as pd
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (X11; Ubuntu; Linux x86_64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/125.0 Safari/537.36"
    )
}

DUMP_URLS = {
    # GameFAQs guides are plain HTML pages; we'll strip the body later.
    "Ocarina_of_Time": (
        "https://gamefaqs.gamespot.com/n64/197771-the-legend-of-zelda-"
        "ocarina-of-time/faqs/20240"
    ),
    "Majoras_Mask": (
        "https://gamefaqs.gamespot.com/n64/197949-the-legend-of-zelda-"
        "majoras-mask/faqs/25526"
    ),
}

RAW_DIR = Path(__file__).resolve().parents[2] / "data" / "raw"
PROCESSED_DIR = RAW_DIR.parent / "processed"
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)


async def _fetch(session: aiohttp.ClientSession, game: str, url: str) -> Path:
    raw_path = RAW_DIR / f"{game}.txt"
    RAW_DIR.mkdir(parents=True, exist_ok=True)

    async with session.get(url, headers=HEADERS, timeout=60) as resp:
        resp.raise_for_status()
        text = await resp.text(encoding="utf-8", errors="ignore")
        if "gamefaqs" in url:
            text = _extract_plain_text(text)
        raw_path.write_text(text)
    return raw_path


async def download_dumps(urls: dict[str, str]) -> list[Path]:
    async with aiohttp.ClientSession() as sess:
        return await asyncio.gather(
            *[_fetch(sess, game, url) for game, url in urls.items()]
        )


def _clean_line(line: str) -> str:
    # Drop speaker tags like “<navi>”, kill excessive whitespace
    line = re.sub(r"<[^>]+>", "", line)
    return re.sub(r"\s+", " ", line).strip()


def build_dataframe(raw_files: list[Path]) -> pd.DataFrame:
    records = []
    for fp in raw_files:
        game = fp.stem
        for i, raw_line in enumerate(
            fp.read_text(encoding="utf-8", errors="ignore").splitlines(), 1
        ):
            text = _clean_line(raw_line)
            if text:
                records.append({"game": game, "line": i, "text": text})
    return pd.DataFrame.from_records(records)


def _extract_plain_text(html: str) -> str:
    """GameFAQs keeps the guide inside <div id="faqtext">"""
    soup = BeautifulSoup(html, "lxml")
    node = soup.find(id="faqtext")
    return node.get_text("\n") if node else html


def run_etl() -> Path:
    raw_files = asyncio.run(download_dumps(DUMP_URLS))
    df = build_dataframe(raw_files)
    out = PROCESSED_DIR / "dialogue.parquet"
    df.to_parquet(out, index=False)
    return out
