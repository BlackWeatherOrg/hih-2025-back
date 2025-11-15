import argparse
import asyncio
import json
import logging
import re
from datetime import date
from pathlib import Path
from typing import Any

from internal.core.exceptions import NotFoundError
from internal.core.types.application import ApplicationCategoryEnum
from internal.repositories.application import ApplicationRepository
from internal.repositories.db.helpers import create_dsn
from internal.repositories.db.manager import db_manager


logger = logging.getLogger(__name__)


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Bulk import applications from JSON file.')
    parser.add_argument('--file', required=True, help='Path to JSON file with applications data.')
    parser.add_argument(
        '--update-existing',
        action='store_true',
        help='Update existing applications matched by name instead of skipping them.',
    )
    return parser.parse_args()


def _load_json(file_path: Path) -> list[dict[str, Any]]:
    with file_path.open('r', encoding='utf-8') as src:
        payload = json.load(src)
    if isinstance(payload, list):
        return payload
    if isinstance(payload, dict):
        data = payload.get('items')
        if isinstance(data, list):
            return data
    raise ValueError('JSON should represent a list of applications or contain it under "items" key.')


def _parse_float(value: Any) -> float | None:
    if value in (None, ''):
        return None
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, str):
        normalized = value.replace(',', '.')
        match = re.search(r'\d+(\.\d+)?', normalized)
        if match:
            return float(match.group())
    return None


def _parse_date(value: Any) -> date | None:
    if value in (None, ''):
        return None
    if isinstance(value, date):
        return value
    if isinstance(value, str):
        return date.fromisoformat(value)
    raise ValueError(f'Cannot parse date value: {value}')


def _parse_category(value: Any) -> ApplicationCategoryEnum:
    if value in (None, ''):
        raise ValueError('Category is required')
    candidates = re.split(r'[·|/]', str(value))
    for candidate in candidates:
        label = candidate.strip()
        if not label:
            continue
        try:
            return ApplicationCategoryEnum(label)
        except ValueError:
            continue
    raise ValueError(f'Unknown category: {value}')


def _normalize_entry(entry: dict[str, Any]) -> dict[str, Any]:
    name = entry.get('name')
    if not name:
        raise ValueError('Application name is required')

    try:
        category = _parse_category(entry.get('category'))
    except ValueError as exc:
        raise ValueError(f'{name}: {exc}') from exc

    rating = _parse_float(entry.get('rating'))
    popularity = _parse_float(entry.get('popularity'))
    created_at = entry.get('created_at')
    parsed_date = _parse_date(created_at) if created_at else None

    screenshots = entry.get('screenshots')
    if not isinstance(screenshots, list):
        screenshots = []

    return {
        'name': name.strip(),
        'rating': rating,
        'popularity': popularity,
        'editors_choice': entry.get('editorsChoice') or entry.get('editors_choice'),
        'category': category,
        'developer': entry.get('developer'),
        'age': entry.get('age'),
        'description': entry.get('description'),
        'downloads': entry.get('downloads'),
        'apk_size': entry.get('apk_size'),
        'screenshots': screenshots,
        'icon_link': entry.get('icon') or entry.get('icon_link'),
        'fun_fact': entry.get('funFact') or entry.get('fun_fact'),
        'apk_link': entry.get('apk_link') or entry.get('link')
    }


async def _import_applications(entries: list[dict[str, Any]], update_existing: bool):
    repo = ApplicationRepository()
    created = updated = skipped = 0

    for entry in entries:
        try:
            payload = _normalize_entry(entry)
        except ValueError as exc:
            logger.warning('Skipping entry: %s', exc)
            continue

        try:
            existing = await repo.get_one({'name': payload['name']})
        except NotFoundError:
            await repo.create(payload)
            created += 1
            logger.info('Created application "%s"', payload['name'])
            continue

        if update_existing:
            await repo.update(existing.id, payload)
            updated += 1
            logger.info('Updated application "%s"', payload['name'])
        else:
            skipped += 1
            logger.info('Skipped existing application "%s"', payload['name'])

    logger.info('Import finished: created=%s, updated=%s, skipped=%s', created, updated, skipped)


async def _run(file_path: Path, update_existing: bool = False):
    if not file_path.exists():
        raise FileNotFoundError(f'File not found: {file_path}')

    db_manager.init(create_dsn())
    try:
        entries = _load_json(file_path)
        await _import_applications(entries, update_existing)
    finally:
        await db_manager.close()


def main():
    logging.basicConfig(level=logging.INFO, format='%(levelname)s %(message)s')
    args = _parse_args()
    asyncio.run(_run(Path(args.file), args.update_existing))


if __name__ == '__main__':
    main()

