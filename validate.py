#!/usr/bin/env python3
"""Contrôles de cohérence des positions et liens sourcés du projet Fouju."""
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parent
def read(path):
    return json.loads((ROOT/path).read_text(encoding="utf-8"))

actors=read("data/actors.json")
claims=read("data/claims.json")
relations=read("data/relations.json")
evidence=read("data/evidence.json")
sources=read("data/sources.json")
taxonomy=read("config/taxonomy.json")
synthesis=read("data/synthesis.json")
content=read("data/content.json")

def indexed(rows, kind):
    ids=[x["id"] for x in rows]
    assert len(ids)==len(set(ids)), f"Doublons d'ID : {kind}"
    return {x["id"]:x for x in rows}

A=indexed(actors,"acteurs")
C=indexed(claims,"positions")
R=indexed(relations,"relations")
E=indexed(evidence,"preuves")
S=indexed(sources,"sources")

def verified(ids, owner):
    assert ids, f"Aucune preuve : {owner}"
    for eid in ids:
        assert eid in E, f"Preuve introuvable {eid} : {owner}"
        sid=E[eid].get("source_id")
        assert sid in S, f"Source introuvable pour {eid} : {owner}"
        url=S[sid].get("url")
        assert isinstance(url,str) and url.startswith(("https://","http://")), f"URL absente : {owner}"

assert "project_fouju" in A
for actor in actors:
    if actor["id"] != "project_fouju":
        assert any(c["subject_id"]==actor["id"] for c in claims), f"Fiche sans documentation : {actor['id']}"
for x in claims:
    assert x["subject_id"] in A, x["id"]
    assert x["value"] in taxonomy["stances"] and x["value"]!="all", x["id"]
    verified(x.get("evidence_ids",[]),x["id"])
for x in relations:
    assert x["source_id"] in A and x["target_id"] in A, x["id"]
    verified(x.get("evidence_ids",[]),x["id"])
for field in ("griefs","vigilance"):
    for i,x in enumerate(synthesis[field]):
        verified(x.get("evidence_ids",[]),f"{field} {i}")
for field in ("milestones","fact_sheet"):
    for i,x in enumerate(content[field]):
        verified(x.get("evidence_ids",[]),f"{field} {i}")

print(f"OK — {len(A)} noeuds, {len(C)} fiches, {len(R)} relations, "
      f"{len(E)} preuves, {len(S)} sources et aucune reference non qualifiee")
