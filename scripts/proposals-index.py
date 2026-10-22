#!/usr/bin/env python3
"""proposals-index — ordena design-system/proposals/ por estado y regenera el índice del README.

Cada propuesta vive en la carpeta de su estado, para que se vea de un vistazo qué espera decisión:
    proposals/              draft y approved (pendientes): lo que hay suelto es lo que falta decidir
    proposals/aplicadas/    applied
    proposals/rechazadas/   rejected
El script mueve los archivos que no estén en su carpeta (git mv si el repo es git).

Agrupa las propuestas en pendientes (draft y approved sin aplicar), aplicadas y rechazadas,
para ver de un vistazo qué espera decisión. Lee el `status` y la `decision` de cada
`*.proposal.json` y reescribe solo el bloque entre
`<!-- ⚙️ GENERATED:start:index -->` / `<!-- ⚙️ GENERATED:end:index -->` del README.

Sin dependencias (solo stdlib). Uso:
    python3 scripts/proposals-index.py           # mueve lo que esté fuera de su carpeta y reescribe el índice
    python3 scripts/proposals-index.py --check   # solo comprueba: exit 1 si algo está fuera de su carpeta,
                                                 # el índice no coincide o hay un estado desconocido
Se ejecuta cada vez que se crea una propuesta o cambia su estado; el hook pre-commit y la CI
lanzan --check. Registra en governance/activity.jsonl lo que mueve y cuándo regenera el índice
(scripts/activity.py), como el resto de scripts que escriben.

`decision` admite dos formas: la del esquema, {status, by, at, note, appliedAt?}, y la antigua
{approvedBy, approvedAt, …} de proyectos anteriores a la 11.6.0. No se migra: se lee.
"""
import argparse
import glob
import json
import os
import re
import shutil
import subprocess
import sys

START, END = '<!-- ⚙️ GENERATED:start:index -->', '<!-- ⚙️ GENERATED:end:index -->'
FOLDER = {'draft': '', 'approved': '', 'applied': 'aplicadas', 'rejected': 'rechazadas'}
GROUPS = [
    ('⏳ Pendientes de decisión', ('draft', 'approved')),
    ('✅ Aplicadas', ('applied',)),
    ('❌ Rechazadas', ('rejected',)),
]


def short(text, n=140):
    text = re.sub(r'\s+', ' ', text or '').strip()
    first = re.split(r'(?<=\.)\s', text, maxsplit=1)[0]  # primera frase, si cabe
    text = first if len(first) >= 40 else text
    return (text[:n - 1].rstrip() + '…' if len(text) > n else text).replace('|', '\\|')


def build(folder):
    props = []
    paths = glob.glob(os.path.join(folder, '*.proposal.json')) + glob.glob(os.path.join(folder, '*', '*.proposal.json'))
    for path in sorted(paths, key=os.path.basename):
        with open(path, encoding='utf-8') as fh:
            d = json.load(fh)
        props.append((os.path.relpath(path, folder), d))
    total = len(props)
    out = [START, '', f'_{total} propuestas. Este bloque lo genera `scripts/proposals-index.py`: no se edita a mano._', '']
    for title, statuses in GROUPS:
        items = [(f, d) for f, d in props if d.get('status') in statuses]
        out.append(f'### {title} ({len(items)})')
        out.append('')
        if not items:
            out += ['Ninguna.', '']
            continue
        if statuses[0] == 'draft':
            out += ['| Propuesta | Qué pide | Estado |', '|---|---|---|']
            for f, d in items:
                out.append(f"| [{d.get('id', f)}](./{f}) | {short(d.get('summary'))} | {d.get('status')} |")
        else:
            out += ['| Propuesta | Qué pedía | Decisión |', '|---|---|---|']
            for f, d in items:
                dec = d.get('decision') or {}
                # dos formas de decision en el repo: {by, at} y {approvedBy, approvedAt}
                who = (dec.get('by') or dec.get('approvedBy') or '').split(' (')[0]
                at = dec.get('at') or dec.get('approvedAt') or '—'
                out.append(f"| [{d.get('id', f)}](./{f}) | {short(d.get('summary'))} | {at} · {who or '—'} |")
        out.append('')
    unknown = [(f, d.get('status')) for f, d in props if d.get('status') not in ('draft', 'approved', 'applied', 'rejected')]
    for f, s in unknown:
        out.append(f'> ⚠️ `{f}` tiene un estado desconocido: `{s}`.')
    out.append(END)
    return '\n'.join(out), unknown


def place(folder, root, check):
    """Mueve cada propuesta a la carpeta de su estado. Devuelve las que no estaban en su sitio."""
    moved = []
    paths = glob.glob(os.path.join(folder, '*.proposal.json')) + glob.glob(os.path.join(folder, '*', '*.proposal.json'))
    for path in paths:
        with open(path, encoding='utf-8') as fh:
            status = json.load(fh).get('status')
        if status not in FOLDER:
            continue
        dest = os.path.join(folder, FOLDER[status], os.path.basename(path))
        if os.path.abspath(dest) == os.path.abspath(path):
            continue
        moved.append((os.path.relpath(path, folder), os.path.relpath(dest, folder)))
        if check:
            continue
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        r = subprocess.run(['git', 'mv', path, dest], cwd=root, capture_output=True)
        if r.returncode != 0:
            shutil.move(path, dest)
    return moved


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--check', action='store_true')
    ap.add_argument('--root', default=os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    a = ap.parse_args()
    folder = os.path.join(a.root, 'design-system', 'proposals')
    readme = os.path.join(folder, 'README.md')
    if not os.path.isdir(folder) or not os.path.exists(readme):
        print('sin design-system/proposals/ (módulo design-system apagado o proyecto sin DS): nada que ordenar')
        sys.exit(0)
    with open(readme, encoding='utf-8') as fh:
        text = fh.read()
    moved = place(folder, a.root, a.check)
    block, unknown = build(folder)
    if START in text and END in text:
        new = text[:text.index(START)] + block + text[text.index(END) + len(END):]
    else:
        new = text.rstrip('\n') + '\n\n## Índice por estado\n\n' + block + '\n'
    if a.check:
        for src, dst in moved:
            print(f'fuera de su carpeta: {src} → {dst}')
        ok = new == text and not unknown and not moved
        print('índice al día' if ok else 'el índice no coincide con las propuestas: ejecuta scripts/proposals-index.py')
        sys.exit(0 if ok else 1)
    cambia = new != text
    if cambia:
        with open(readme, 'w', encoding='utf-8') as fh:
            fh.write(new)
    for src, dst in moved:
        print(f'movida: {src} → {dst}')
    print(f'índice regenerado en {os.path.relpath(readme, a.root)}' if cambia else 'índice al día')
    if moved or cambia:
        # rastro: qué movió y si regeneró el índice (nunca falla por esto)
        try:
            sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
            from activity import log
            detalle = []
            if moved:
                detalle.append('%d propuestas movidas a la carpeta de su estado (%s)' % (len(moved), ', '.join(f'{s}→{d}' for s, d in moved[:6]) + ('…' if len(moved) > 6 else '')))
            if cambia:
                detalle.append('índice por estado regenerado en proposals/README.md')
            log(a.root, 'script', 'proposals-index', '; '.join(detalle),
                files=[os.path.relpath(readme, a.root)] + [os.path.join('design-system', 'proposals', d) for _, d in moved])
        except Exception:
            pass
    sys.exit(1 if unknown else 0)


if __name__ == '__main__':
    main()
